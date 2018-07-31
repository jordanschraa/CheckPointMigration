from header import authenticate, api_post
import names
import random
import json

#variable to keep track of objects created
objects = {}

def generate_host(private = "", subnet = 0, tag = None):
    '''Create a new host dictonary and return credentials
    provide first two octects for private ip /24 network'''
    host = {}
    host["name"] = names.get_full_name()
    
    #create public ip
    if subnet == 0:
        host["ipv4-address"] = '{}.{}.{}.{}'.format(*__import__('random').sample(range(5,254),4))
    #create private ip
    elif subnet == 16:
        host["ipv4-address"] = private+".{}.{}".format(*__import__('random').sample(range(5,254),2))
    elif subnet == 24:
        host["ipv4-address"] = private+".{}".format(random.randint(5,254))
    
    if tag != None:
        host["tags"] = tag
        
    return host

def generate_network(name, mask, tag = None):
    '''generates a network object in dictonary format
    subnet can be either 8, 16, 24 just for demonstration purposes'''
    
    network = {}
    network["name"] = name
    
    if mask == 8:
        network["subnet"] = "{}.0.0.0".format(random.randint(5,254))
    elif mask == 16:
        network["subnet"] = "{}.{}.0.0".format(*__import__('random').sample(range(5,254),2))
    elif mask == 24:
        network["subnet"] = "{}.{}.{}.0".format(*__import__('random').sample(range(5,254),3))
        
    network["mask-length"] = mask

    if tag != None:
        network["tags"] = tag
    
    return network

def generate_object():
    '''generates one object'''
    return
def main():
    cred = authenticate()
    print("Sucessfully authenticated to managment server")
    print("SID: " + cred["sid"])
    
    host = generate_host("10.5",16,"API")
    objects[host["name"]] = "host"
    network = generate_network("Network1", 16, "MgmtAPI")
    objects[network["name"]] = "network"
    
    r,c = api_post(cred, "add-host", host)
    r,c = api_post(cred, "add-network", network)
    
    api_post(cred, "publish", {})
    api_post(cred, "logout", {})
    
    #write new objects to file for easier cleanup
    json_file = open("objects.json","w")
    json_file.write(json.dumps(objects, indent = 4))
    json_file.close()

if __name__ == "__main__":
    main()