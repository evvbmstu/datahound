
# coding: utf-8

import json
import requests

# Return all members from group with fields
def getAllMembers( fields, groupId ):
    baseUrl       = "https://api.vk.com/method/execute."
    procedureName = "getAllMembers"
    members       = []
    groupLen      = vk_api.groups.getMembers( group_id = groupId ).get( 'count', 0 )
    
    while ( len(members) < groupLen ):
        token  = "?access_token={0}".format( workToken )
        fields = "&fields={0}".format( fields )
        args   = "&groupId={0}&membersLen={1}&groupLen={2}".format( groupId, len( members ), groupLen)
        #
        try:
            info = requests.post( baseUrl + procedureName + args ).json()
        except requests.exceptions.RequestException as error:
            print ( error )
        
        # Use the get() method to avoid use try/catch for KeyError exception
        members += info.get( 'response', 'empty' )
            
    return members

