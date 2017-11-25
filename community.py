from collections import Counter
from math import floor, log

import getters
import settings
import requests
import exceptions as exc
import time
import logging

class Community:
    def __init__(self, group_id):
        self.group_id = group_id
        self.vk_api = getters.auth()
        self.members_count, self.posts_count = self.counters()

    def counters(self):
        members_count = self.vk_api.groups.getMembers(group_id=self.group_id).get('count', 0)
        posts_count = self.vk_api.wall.get(domain=self.group_id)[0]
        return members_count, posts_count

    def ad_ratio(self):
        posts = getters.get_posts(self.group_id, self.posts_count)
        ad = 0
        no_ad = 0
        unknown = 0
        for post in posts:
            if post['marked_as_ads'] == 0:
                no_ad += 1
            elif post['marked_as_ads'] == 1:
                ad += 1
            else:
                unknown += 1

        ad_data = {'marked as ad': ad, 'not ad': no_ad, 'unknown': unknown}
        return ad_data

    def sex_data(self):
        sex_data = getters.get_members(self.group_id, self.members_count, fields="sex")
        woman = 0
        man = 0
        unknown = 0
        for user in sex_data:
            if user['sex'] == 1:
                woman += 1
            elif user['sex'] == 2:
                man += 1
            else:
                unknown += 1
        sex_dict = {"Woman": woman, "Man": man, "Unknown": unknown}
        return sex_dict

    def platform_data(self):
        platform_data = getters.get_members(self.group_id, self.members_count, fields="last_seen")
        platform_count = []

        for user in platform_data:
            index = None
            last = user.get('last_seen', None)
            if last is not None:
                index = last.get('platform', None)
            if index is not None:
                platform_count.append(index)

        index_dict = dict(Counter(platform_count))
        platform_dict = {}
        for each in index_dict.keys():
            platform_dict[settings.PLATFORM[each]] = index_dict[each]

        platform_dict.update({'Apple': platform_dict['iPhone'] + platform_dict['iPad']})
        platform_dict.pop('iPhone')
        platform_dict.pop('iPad')

        to_pop = platform_dict.get('Windows 10', 0)
        platform_dict['Web'] += to_pop
        if to_pop:
            platform_dict.pop('Windows 10')

        system_dict = dict.fromkeys(['Web', 'Mobile'])
        system_dict['Web'] = platform_dict['Web']
        platform_dict.pop('Web')
        system_dict['Mobile'] = platform_dict['Mobile']
        platform_dict.pop('Mobile')

        return platform_dict, system_dict

    def likes_data(self):
        posts = getters.get_posts(self.group_id, self.posts_count)
        views = 0
        likes = 0
        reposts = 0
        likes_past = 0
        reposts_past = 0
        iter = 0
        for post in posts:
            try:
                views += post['views']['count']
                iter += 1
                likes += post['likes']['count']
                reposts += post['reposts']['count']
            except KeyError as error:
                likes_past += post['likes']['count']
                reposts_past += post['reposts']['count']

        funnel_value = {'Views': views,
                        "Likes": likes, 'Likes_past': likes_past,
                        'Reposts': reposts, 'Reposts_past': reposts_past}
        return funnel_value

    def age_data(self):
        age_data = getters.get_members(self.group_id, self.members_count, fields='sex, bdate')
        year = time.gmtime(time.time()).tm_year
        unknown = 0
        ages_male = []
        ages_female = []
        for user in age_data:
            date = user.get('bdate', None)
            if date:
                date = date.split('.')
                if len(date) < 3:

                    unknown += 1
                    continue
                else:
                    date = date[-1]
                    age = year - int(date)
                    if age >= 80 or age < 10:
                        unknown += 1
                    else:
                        if user['sex'] == 1:
                            ages_female.append(age)
                        elif user['sex'] == 2:
                            ages_male.append(age)
                        else:
                            unknown += 1
            else:
                unknown += 1

        if ages_female:
            age_female_max = max(ages_female)
            age_female_min = min(ages_female)
        else:
            age_female_max, age_female_min = 0, 0

        if ages_male:
            age_male_max = max(ages_male)
            age_male_min = min(ages_female)
        else:
            age_male_max, age_male_min = 0, 0
        age_num = len(ages_female) + len(ages_male)

        hist_step = 1 + floor(log(age_num, 2))
        # age_data = {(a, a + hist_step): None for a in range(age_min, age_max, hist_step)}
        xbins_female = dict(start=age_female_min, end=age_female_max, size=hist_step)
        xbins_male = dict(start=age_male_min, end=age_male_max, size=hist_step)
        return ages_female, xbins_female, ages_male, xbins_male, unknown

    def places_data(self):
        # info = getters.get_members(self.group_id, self.members_count, debug=debug, fields='country,city')
        info = self.vk_api.groups.getMembers(group_id=self.group_id, sort='id_ask', fields='country,city')
        info = info['users']

        cities = []
        countries = []

        for each in info:
            keys_city = 'city'
            keys_country = 'country'
            if keys_city in each.keys():
                cities.append(each['city'])
            if keys_country in each.keys():
                countries.append(each['country'])

        cities = dict(Counter(cities))
        countries = dict(Counter(countries))

        query = ''
        for country_id in list(countries.keys()):
            try:
                str_country = settings.COUNTRIES[country_id]
            except KeyError:
                if not country_id:
                    continue
                query += str(country_id)
                query += ','
            else:
                count = countries[country_id]
                countries.pop(country_id)
                countries.update({str_country: count})

        query = query[:-1]
        count = countries[0]
        countries.pop(0)
        countries.update({'Unknown': count})

        countries_names_id = self.vk_api.database.getCountriesById(country_ids=query)

        for country in countries_names_id:
            cid = country['cid']
            name = country['name']
            count = countries[cid]
            countries.pop(cid)
            countries.update({name: count})

        ids = str(cities.keys()).replace('dict_keys([', '').replace('])', '')
        city_names_id = self.vk_api.database.getCitiesById(city_ids=ids)

        for city in city_names_id:
            cid = city['cid']
            name = city['name']
            count = cities[cid]
            cities.pop(cid)
            cities.update({name: count})

        count = cities[0]
        cities.pop(0)
        cities.update({'Unknown': count})

        names_of_keys = list(cities.keys())
        names_of_keys.remove('Unknown')

        for city in names_of_keys:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address="
            url += city
            url += "&key="
            url += settings.GOOGLE_TOKEN
            city_info = requests.get(url)

            city_info = city_info.json()

            lat = city_info['results'][0]['geometry']['location']['lat']

            lng = city_info['results'][0]['geometry']['location']['lng']

            count = cities[city]
            cities.update({city: [(lat, lng), count]})

        return cities, countries

    def display(self):
        print("ID:" + str(self.group_id))
        print("Members:" + str(self.members_count))
        print("Posts:" + str(self.posts_count))


if __name__ == "__main__":
    try:
        pb = Community("bmstu_ctf")
        print(pb.group_id.upper(), "\n\n")
        print(pb.places_data())
    except exc.VkAPIError:
        print('Oops, get token, please')
    # print(pb.members_count, pb.posts_count)
    # pb.places_data(debug=False)

    # print(pb.likes_data())

