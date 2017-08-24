var fields = Args.fields;
var members = API.groups.getMembers( { "group_id": Args.groupId , "v": "5.68", "sort": "id_asc", "count": "1000", "fields":fields, "offset": parseInt( Args.membersLen ) } ).items; 
var offset = 1000;
while ( offset < 25000 && ( offset + parseInt( Args.membersLen ) ) < parseInt( Args.groupLen ) ) {
	members = members + API.groups.getMembers( { "group_id":Args.groupId, "v": "5.68", "sort": "id_asc", "fields":fields, "count": "1000", "offset": ( parseInt( Args.membersLen ) + offset ) } ).items;
	offset = offset + 1000;
};
return members;
