from header import authenticate, api_post
import json
import pprint

def cleanup(cred, object_type, uid, layer, rule_uid, source_destination):
    r,c = api_post(cred, "show-"+object_type, {"uid":uid})
    #put tags into one list
    tag_list = []
    for tag in r["tags"]:
        tag_list.append(tag["name"])

    #remove object from rule 
    #TODO: edit this when the bug of added old to new instances is fixed
    if "Old" in tag_list and "New" not in tag_list:
        print("Removing "+ r["name"])
        delete,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, source_destination: {"remove": r["uid"]}})

    #we cannot rename the object unless we delete the old object
    '''    
    if "New" in tag_list:
        #remove the "-NEW" from the name
        new_name = r["name"][:-4]
        print("Renaming " + r["name"])
        edit,c = api_post(cred, "set-"+object_type, {"uid": r["uid"], "new-name": new_name})
    '''
    
def main():
    cred = authenticate()
    print("Authentication Successful")
    pp = pprint.PrettyPrinter(indent=4)
    policy_query = {
        "offset" : 0,
        "limit" : 20,
        "name" : "API_Policy Network",
        "details-level" : "full",
        "use-object-dictionary" : "true"
    }
    
    r,c = api_post(cred, "show-access-rulebase", policy_query)
    
    layer = "API_Policy Network"
    #for each rule
    for rule in r["rulebase"]:
        rule_uid = rule["uid"]
        #for each source item in that rule
        for item in rule["source"]:
            r,c = api_post(cred, "show-object", {"uid":item})
            object_type = r["object"]["type"]
            
            if object_type in ["host", "network"]:
                cleanup(cred, object_type, item, layer, rule_uid, "source")
        
        #for each destination item in that rule
        for item in rule["destination"]:
            r,c = api_post(cred, "show-object", {"uid":item})
            object_type = r["object"]["type"]
            
            if object_type in ["host", "network"]:
                cleanup(cred, object_type, item, layer, rule_uid, "destination")
                
    
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    return
    
if __name__ == "__main__":
    main()