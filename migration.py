from header import authenticate, api_post
import json
import pprint

def host_duplicate(cred, host_uid):
    new_host = {}
    old_host,c = api_post(cred, "show-host", {"uid": host_uid})
    
    #check to see if ip matches regex rule
    new_ip, color = regex_rules(old_host["ipv4-address"])
    #if it doesn't match rule no change is needed
    if new_ip == None:
        return None
    
    new_host["ipv4-address"] = new_ip
    new_host["color"] = color
    new_host["comments"] = old_host["comments"]
    new_host["interfaces"] = old_host["interfaces"]
    new_host["name"] = old_host["name"]+"-NEW"
    new_host["nat-settings"] = old_host["nat-settings"]
    tags = []
    for tag in old_host["tags"]:
        tags.append(tag["name"])
    tags.append("New")
    new_host["tags"] = tags
    
    r,c = api_post(cred, "add-host", new_host)
    
    #if the new object already exsists
    if c != 200:
        r,c = api_post(cred, "show-host", {"name": new_host["name"]})
        
    new_uid = r["uid"]
    #add tag "Old" to old object for easy deletion later
    r,c = api_post(cred, "set-host", {"uid": host_uid, "tags": {"add": "Old"}})
    
    return new_uid

def network_duplicate(cred, network_uid):
    new_network = {}
    old_network,c = api_post(cred, "show-network", {"uid": network_uid})
    
    #check to see if ip matches regex rule
    new_ip, color = regex_rules(old_network["subnet4"])
    #if it doesn't match rule no change is needed
    if new_ip == None:
        return None
    
    new_network["subnet4"] = new_ip
    new_network["color"] = color
    new_network["broadcast"] = old_network["broadcast"]
    new_network["comments"] = old_network["comments"]
    new_network["mask-length4"] = old_network["mask-length4"]
    new_network["name"] = old_network["name"]+"-NEW"
    new_network["nat-settings"] = old_network["nat-settings"]
    tags = []
    for tag in old_network["tags"]:
        tags.append(tag["name"])
    tags.append("New")
    new_network["tags"] = tags
    
    r,c = api_post(cred, "add-network", new_network)
    
    #if the new object already exsists
    if c != 200:
        r,c = api_post(cred, "show-network", {"name": new_network["name"]})
        
    new_uid = r["uid"]
    #add tag "Old" to old object for easy deletion later
    r,c = api_post(cred, "set-network", {"uid": network_uid, "tags": {"add": "Old"}})
    
    return new_uid
    
def regex_rules(ip):
    s1, s2, s3, s4 = ip.split(".")
    
    #RULE ONE 10.0.1.* --> 10.5.1.*
    if s1 == "10" and s2 == "0" and s3 == "1":
        print("--- RULE ONE MATCH ---")
        new_ip = "10.5.1."+s4
        return new_ip, "blue"
    
    #RULE TWO 192.168.26.* --> 192.168.54.*
    elif s1 == "192" and s2 == "168" and s3 == "26":
        print("--- RULE TWO MATCH ---")
        new_ip = "192.168.54."+s4
        return new_ip, "dark sea green"
    
#    #RULE THREE 192.168.5.* --> 192.168.35.*
#    elif s1 == "192" and s2 == "168" and s3 == "5":
#        print("--- RULE THREE MATCH ---")
#        new_ip = "192.168.35."+s4
#        return new_ip, "gold"
    
    #NO RULE MATCH
    else:
        return None, None
    
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
        print(rule["name"])
        rule_uid = rule["uid"]
        #for each source item in that rule
        for item in rule["source"]:
            r,c = api_post(cred, "show-object", {"uid":item})
            object_type = r["object"]["type"]
            
            if object_type == "host":
                new_host_uid = host_duplicate(cred, item)
                #if object did not match regex rules no modification of rule needed
                if new_host_uid == None:
                    continue
                #else take new uid and add to rulebase
                else:
                    r,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, "source": {"add": new_host_uid}})
            
            if object_type == "network":
                new_network_uid = network_duplicate(cred, item)
                #if object did not match regex rules no modification of rule needed
                if new_network_uid == None:
                    continue
                #else take new uid and add to rulebase
                else:
                    r,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, "source": {"add": new_network_uid}})
                
            #more work to parse group
            elif object_type == "group":
                continue
                
            else:
                continue
                
        #for each destination item in that rule
        for item in rule["destination"]:
            r,c = api_post(cred, "show-object", {"uid":item})
            object_type = r["object"]["type"]
            
            if object_type == "host":
                new_host_uid = host_duplicate(cred, item)
                #if object did not match regex rules no modification of rule needed
                if new_host_uid == None:
                    continue
                #else take new uid and add to rulebase
                else:
                    r,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, "destination": {"add": new_host_uid}})
                    
            if object_type == "network":
                new_network_uid = network_duplicate(cred, item)
                #if object did not match regex rules no modification of rule needed
                if new_network_uid == None:
                    continue
                #else take new uid and add to rulebase
                else:
                    r,c = api_post(cred, "set-access-rule", {"uid": rule_uid, "layer": layer, "destination": {"add": new_network_uid}})
                
            #more work to parse group
            elif object_type == "group":
                continue
                
            else:
                continue
                

    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    return
    
if __name__ == "__main__":
    main()