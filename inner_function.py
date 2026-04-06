import json
import random
import uuid

#inner data structure for the json file, it can be group or task
_types ={
    "group",
    "task"
}


#create a random id for the group or task
#Which is unique and not used before, you can implement this function to generate a random ID
def generate_random_id():
    return str(uuid.uuid4())



# This function get a common group name and generates a unique virtual ID.
# This Virtual ID is used for id for group objects.
# The mapping is getting saved in the virtual_address.json file, which is a dictionary that maps the common group name to the generated virtual ID.
def generate_virtual_id(group_name):
    with open('virtual_address.json', 'r') as json_file:
        virtual_address = json.load(json_file)
    
    if group_name in virtual_address:
        return virtual_address[group_name]
    else:
        virtual_id = generate_random_id()
        virtual_address[group_name] = virtual_id
        
        with open('virtual_address.json', 'w') as json_file:
            json.dump(virtual_address, json_file, indent=4)
        
        return virtual_id