var posts = API.wall.get( {"v": "5.68","domain": Args.domain ,"count": "100","offset": parseInt( Args.postsLen ) } ).items; 
var offset = 100;
while ( offset < 2500 && ( offset + parseInt( Args.postsLen ) ) < parseInt( Args.wallLen ) )
{
posts = posts + API.wall.get( { "v": "5.68","domain": Args.domain ,"count": "100", "offset": ( parseInt( Args.postsLen ) + offset) } ).items;
offset = offset + 100;
};
return posts;
