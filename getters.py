import vk
import requests
import settings as ss


def auth():
    """
    Just auth for VK Api
    :return:
    """
    session = vk.Session(access_token=ss.TOKEN)
    vk_api = vk.API(session)
    return vk_api


def get_members(group_id, group_len, fields=ss.MEMBERS_FIELDS, debug=False):
    """
    :param debug: Debug mode on/off
    :param group_len: Members count
    :param fields: For example - sex,b_date,city.
    :param group_id: Group name.For example - bmstuinformer
    :return: info ( uses fields ) about all users in group
    """
    members = []  # List for members info.
    proc_name = "getAllMembers"  # Name of stored procedure in VK app

    # Fields, which we can get from users.
    fields_arg = "&fields={0}".format(fields)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    group_arg = "&groupLen={0}".format(group_len)
    id_arg = "&groupId={0}".format(group_id)

    # Concatenate all together and get link to post request
    post_url = ss.BASE_URL + proc_name + token_arg + fields_arg + group_arg + id_arg
    if group_len == 0:
        return None

    # We get the data about the users until we get everything (25 000 users for one cycle)
    while len(members) < group_len:
        proc_args = "&membersLen={0}".format(len(members))
        try:
            info = requests.post(post_url + proc_args).json()
        except requests.exceptions.RequestException as error:
            return error

        # Use the get() method to avoid use try/catch for KeyError exception
        members += info.get('response', 'empty')
        if debug:
            print("Get members:" + str(len(members)))
    return members


def get_posts(group_id, wall_len, debug=False):
    posts = []
    proc_name = "getAllPosts"
    domain_arg = "&domain={0}".format(group_id)
    token_arg = "?access_token={0}".format(ss.TOKEN)
    wall_arg = "&wallLen={0}".format(wall_len)
    post_url = ss.BASE_URL + proc_name + token_arg + wall_arg + domain_arg
    while len(posts) < wall_len:
        proc_args = "&postsLen={0}".format(len(posts))
        try:
            info = requests.post(post_url + proc_args).json()
        except requests.exceptions.RequestException as error:
            return error

        posts += info.get('response', 'empty')
        if debug:
            print("Get posts:" + str(len(posts)))

    return posts

