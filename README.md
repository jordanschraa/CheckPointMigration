# Python-Scripts-Check-Point

#### Scripts to demo the intergration with Python and Check Point's API

#### Dependencies
 - Python3
 - python requests
 - Check Point Management Server with API calls enabled
 
#### header.py
 - header.py can be used as the basis for python programs with Check Point API
 - contains two usefull functions authenticate and api_post
   - authenticate displays collects Check Point management credentials from the user and writes them to credentials.json for easier logins in the future. Collection of credentials done with a menu style. Authenticate will also handle the first time login and will return dictonary that contians sessions id and logon credentials
   
   - api_post handles the api calls, you must provide the credentials that were returned by the authenticate method
   
   - ex: creds = authenticate()
         r, c = api_post(creds, "add-host", json-host)

#### create_policy.py
  - create_policy.py will use the data in objects.json and policy.json to create an example policy to demonstrate API capabilities
  
#### migration.py
  - migration.py is a program to help migration of a customer to Azure
  - it will go over a rule set one rule at time and find objects in the source and destination columns that match the regex rules that are defined in the function regex_rules()
  - if the object matches a regex rule it will have a tag of "Old" added to it this is for cleanup purposes later
  - once it finds a match to the regex rule it will create a duplicate object that changes the IP based on the regex rule and adds "-NEW" to the name of the object. This new object will have a tag of "New" added to it
  - then it inserts the new object into the same position in the ruleset
  - all the changes will be visible at the end when the session is published
  
#### migration-cleanup.py
  - migration-cleanup.py cleans up the rule set after migration.py has been run 
  - once you you have done the tests to determine that ruleset is functioning correctly after running migration.py you can run migration-cleanup.py to clean up the rule set again
  - this program goes over the rule set one rule at a time and finds objects with the old tag and removes them from the policy.
  - this object will not be deleted from the data base (may change this functionality later?)
  - it will edit the newly created objects to remove the "-NEW" from the name and remove the "New" tag
  - all the changes will be visible at the end when the session is published
  
#### TODO:
  - in migration.py make sure the "Old" tag is not added to newly created objects
  - migration-cleanup.py is a WIP
  - create a video demonstrating migration.py and migration-cleanup.py
  - fix logging on header.py (it is not logging some of the set API commands)
  - create a more sensible ruleset in objects.json and policy.json

