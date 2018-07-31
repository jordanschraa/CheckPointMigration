from header import authenticate, api_post
import json

def main():
    cred = authenticate()
    json_file = open("objects.json").read()
    objects = json.loads(json_file)
    
    for key in objects.keys():
        print(key, objects[key])
        a,c = api_post(cred, "delete-"+objects[key], {"name":key})
        print(c)
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    return

if __name__ == "__main__":
    main()