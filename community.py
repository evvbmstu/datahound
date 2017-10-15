import getters
import settings
# import pandas as pd
from collections import Counter


class Community:
    def __init__(self, group_id):
        self.group_id = group_id
        self.members_count, self.posts_count = self.counters()
        # self.posts, self.posts_count = getters.get_posts(group_id)
        # self.members, self.members_count = getters.get_members(group_id,fields='sex')

    def counters(self):
        vk_api = getters.auth()
        members_count = vk_api.groups.getMembers(group_id=self.group_id).get('count', 0)
        posts_count = vk_api.wall.get(domain=self.group_id)[0]
        return members_count, posts_count

    def sex_dist(self):
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
        return platform_dict


if __name__ == "__main__":
    pb = Community("r_pics")
    print(pb.sex_dist())
    print(pb.platform_dist())

