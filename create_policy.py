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
    
    pkey = policies.keys()
    okeys = objects.keys()
    
    #each object is a list the first position is the type of object
    #the second position is the data
    '''
    for key in okeys:
        if key in okeys:
            r,c = api_post(cred, "add-"+objects[key][0], objects[key][1])
            print(c)
    '''
    #r,c = api_post(cred, "add-access-rule", policies["Management_Rule"][1])
          
    
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    return
    
if __name__ == "__main__":
    main()
    