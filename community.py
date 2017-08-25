import vk
import requests
class group( object ):
    
    def __init__ ( self, domain = None  ):
        self.name = domain
        
    def fields( self ):
        return self.__dict__
    
    def allMembers( self, fields, groupId ):
        baseUrl       = "https://api.vk.com/method/execute."
        procedureName = "getAllMembers"
        members       = []
        groupLen      = vk_api.groups.getMembers( group_id = groupId ).get( 'count', 0 )

        while ( len( members ) < groupLen ):
            tokenArg  = "?access_token={0}".format( homeToken )
            fields    = "&fields={0}".format( fields )
            procArgs  = "&groupId={0}&membersLen={1}&groupLen={2}".format( groupId, len(members), groupLen )
            args      = tokenArg + fields + procArgs
            
            try:
                info  = requests.post( baseUrl + procedureName + args ).json()
            except requests.exceptions.RequestException as error:
                print ( error )
            
            # Use the get() method to avoid use try/catch for KeyError exception
            members  += info.get( 'response', 'empty' )
        
        self.membersInfo = members
        self.membersLen  = groupLen

    def allPosts( self, domain ):
        baseUrl       = "https://api.vk.com/method/execute."
        procedureName = "getAllPosts"
        posts         = []
        wallLen       = vk_api.wall.get( domain = domain )[0]
        
        while ( len( posts ) < wallLen ):
            tokenArg  = "?access_token={0}".format( homeToken )
            domain    = "&domain={0}".format( domain ) 
            procArgs  = "&postsLen={0}&wallLen={1}".format( len( posts ), wallLen )
            args      = tokenArg + domain + procArgs
            
            try:
                info  = requests.post( baseUrl + procedureName + args).json()
            except requests.exceptions.RequestException as error:
                print( error )
            
            posts    += info.get( 'response', 'empty' )
        
        self.postsInfo = posts
        self.postsLen  = wallLen
