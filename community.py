# import pandas as pd
from collections import Counter
from math import floor, log

import getters
import settings


# import numpy as np


class Community:
    def __init__(self, group_id):
        self.group_id = group_id
        self.members_count, self.posts_count = self.counters()
        # self.posts, self.posts_count = getters.get_posts(group_id)
        # self.members, self.members_count = getters.get_members(group_id,fields='sex')

    # def database_check(self):
        # conn = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB, charset='utf8', use_unicode=True)
        # cursor = conn.cursor()

    def counters(self):
        vk_api = getters.auth()
        members_count = vk_api.groups.getMembers(group_id=self.group_id).get('count', 0)
        posts_count = vk_api.wall.get(domain=self.group_id)[0]
        return members_count, posts_count

    def sex_dist(self, debug=False):
        sex_data = getters.get_members(self.group_id, self.members_count, debug=debug, fields="sex")
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

    def platform_dist(self):
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

    def likes_funnel(self, debug=False):
        posts = getters.get_posts(self.group_id, self.posts_count, debug)
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

    def age_dict(self, debug=False):
        age_data = getters.get_members(self.group_id, self.members_count, debug=debug, fields='sex, bdate')
        year = 2017
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
                        if user['sex'] == 1:  # female
                            ages_female.append(age)
                        if user['sex'] == 2:  # male
                            ages_male.append(age)

        # print(np.histogram(ages, bins='sturges'))
        age_female_max = max(ages_female)
        age_female_min = min(ages_female)
        age_male_max = max(ages_male)
        age_male_min = min(ages_female)
        age_num = len(ages_female) + len(ages_male)

        hist_step = 1 + floor(log(age_num, 2))
        # age_dict = {(a, a + hist_step): None for a in range(age_min, age_max, hist_step)}
        xbins_female = dict(start=age_female_min, end=age_female_max, size=hist_step)
        xbins_male = dict(start=age_male_min, end=age_male_max, size=hist_step)
        return ages_female, xbins_female, ages_male, xbins_male, unknown

    def display(self):
        print("ID:" + str(self.group_id))
        print("Members:" + str(self.members_count))
        print("Posts:" + str(self.posts_count))


if __name__ == "__main__":
    pb = Community("sbertech")
    # pb.age_dict()
    # print(pb.platform_dist())
    # print(pb.likes_funnel())

