from header import authenticate, api_post
import json

def main():
    cred = authenticate()
    try:
        json_file = open("objects.json").read()
        objects = json.loads(json_file)
    except:
        print("No objects to delete")
        return
    
    errors = 0
    not_deleted = {}
    for key in objects.keys():
        a,c = api_post(cred, "delete-"+objects[key], {"name":key})
        
        #if there is an error count it and store the object
        #which was not deleted
        if c != 200:
            errors += 1
            not_deleted[key] = objects.keys()
        
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    if errors == 0:
        print("Cleanup Sucessful")
    else:
        print("There were " + errors + " errors the following objects were not deleted:")
        print(not_deleted)
        
    json_file = open("objects.json","w")
    json_file.write(json.dumps(not_deleted, indent = 4))
    json_file.close()
    
    return

if __name__ == "__main__":
    main()