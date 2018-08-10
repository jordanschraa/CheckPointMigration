from header import authenticate, api_post, generate_host, generate_network
import json

#variable to keep track of objects created
objects = {}

def generate_host_network(cred):
    '''Generates one host and one network object and publishes'''
    
    host = generate_host("10.5",16,"API")
    network = generate_network("Network0", 16, "API")
    
    r1,c1 = api_post(cred, "add-host", host)
    objects[host["name"]] = "host"
    r2,c2 = api_post(cred, "add-network", network)
    objects[network["name"]] = "network"
    
    if c1 == 200 and c2 == 200:
        print("Success: One host and network generated")
    
    api_post(cred, "publish", {})
    
def generate_100(cred):
    '''Generate 100 objects'''
    
    #create 30 hosts on 192.168.5/16 network
    for i in range(30):
        host = generate_host("192.168.5",24,"API")
        host["color"] = "dark blue"
        r, c = api_post(cred, "add-host", host)
        if c == 200:
            objects[host["name"]] = "host"
        else:
            print("error code: " + str(c))
    print("30 hosts generated")
    
    #generate 40 hosts on 10.0/16 network
    for i in range(40):
        host = generate_host("10.0", 16, "10.0/16")
        host["color"] = "violet red"
        r, c = api_post(cred, "add-host", host)
        if c == 200:
            objects[host["name"]] = "host"
        else:
            print("error code: " + str(c))
    print("40 hosts generated")
            
    #generate 20 /24 network objects
    for i in range(20):
        network = generate_network("Network"+str(i),24,"API")
        network["color"] = "burlywood"
        r, c = api_post(cred, "add-network", network)
        if c == 200:
            objects[network["name"]] = "network"
        else:
            print("error code: " + str(c))
    print("20 networks generated")
    
    #generate 20 /16 network objects
    for i in range(20):
        network = generate_network("Network"+str(i+30),16,"API")
        network["color"] = "light green"
        r, c = api_post(cred, "add-network", network)
        if c == 200:
            objects[network["name"]] = "network"
        else:
            print("error code: " + str(c))
    print("20 networks generated")
        
            
    api_post(cred, "publish", {})
    

def main():
    cred = authenticate()
    print("Sucessfully authenticated to managment server")
    
    generate_host_network(cred)
    generate_100(cred)
    
    api_post(cred, "logout", {})
    
    #write new objects to file for easier cleanup
    json_file = open("objects.json","w")
    json_file.write(json.dumps(objects, indent = 4))
    json_file.close()

if __name__ == "__main__":
    main()