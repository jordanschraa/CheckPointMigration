from header import authenticate, api_post
import json

def main():
    cred = authenticate()
    print("authentication successful")
    
    #import objects and policies from json
    objects_file = open("objects.json").read()
    objects = json.loads(objects_file)
    policy_file = open("policy.json").read()
    policies = json.loads(policy_file)
    
    pkeys = policies.keys()
    okeys = objects.keys()
    
    
    #each object is a list the first position is the type of object
    #the second position is the data
    print("Objects")
    for key in okeys:
        r,c = api_post(cred, "add-"+objects[key][0], objects[key][1])
        print(c)
       
    print("Policies")        
    for key in pkeys:
        if policies[key][0] in ["access-layer"]:
            r,c = api_post(cred, "set-access-layer", policies[key][1])
        else:
            r,c = api_post(cred, "add-"+policies[key][0], policies[key][1])
        print(c)
        
    #space = input("Press space to change IPs: ")
    '''
    r,c = api_post(cred, "show-hosts", {"limit" : 100,"offset" : 0,"details-level" : "standard"})
    for i in range(len(r["objects"])):
        if "10.0." in r["objects"][i]["ipv4-address"]:
            print(r["objects"][i]["name"])
            one, two, three, four = r["objects"][i]["ipv4-address"].split(".")
            print(one+".67."+three+"."+four)
            r,c = api_post(cred, "set-host", {"name": r["objects"][i]["name"],"ipv4-address": one+".67."+three+"."+four, "color": "sky blue"})
            print(c)
            
    '''
    
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    return
    
if __name__ == "__main__":
    main()
    