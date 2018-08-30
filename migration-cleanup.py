from header import authenticate, api_post
import json
import pprint

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
            
            if object_type == "host":
                r,c = api_post(cred, "show-host", {"uid":item})
                print(r["name"])
                for tag in r["tags"]:
                    print(tag["name"])
                print("")
            
            #delete from rule
            #r,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, "source": {"add": new_host_uid}})
    
    #api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    return
    
if __name__ == "__main__":
    main()