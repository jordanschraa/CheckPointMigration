# Python-Scripts-Check-Point

#### Scripts to demo the intergration with Python and Check Point's API

#### Dependencies
 - Python3
 - python requests
 - Check Point Management Server with API calls enabled
 
#### header.py
 - header.py can be used as the basis for python programs with Check Point API
 - contains two usefull functions authenticate and api_post
   - authenticate displays collects Check Point management credentials from the user and writes them to a file for easier logins in the future. Collection of credentials done with a menu style. Authenticate will also handle the first time login and will return dictonary that contians sessions id and logon credentials
   
   - api_post handles the api calls, you must provide the credentials that were returned by the authenticate method
   
   - ex: creds = authenticate()
         r, c = api_post(creds, "add-host", json-host)

#### create_policy.py
  - create_policy.py will use the data in objects.json and policy.json to create an example policy to demonstrate API capabilities


