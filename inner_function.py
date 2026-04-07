import json
import os
import random
import uuid
import config

DB_DIR = config.get_db_dir()


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
    file_path = os.path.join(DB_DIR, 'virtual_address.json')
    try:
        with open(file_path, 'r') as json_file:
            virtual_address = json.load(json_file)
    except FileNotFoundError:
        virtual_address = {}
    
    if group_name in virtual_address:
        return virtual_address[group_name]
    else:
        virtual_id = generate_random_id()
        virtual_address[group_name] = virtual_id
        
        with open(file_path, 'w') as json_file:
            json.dump(virtual_address, json_file, indent=4)
        
        return virtual_id


#This function reset ALL files in the DB directory, it will delete all files in the DB directory and create new empty files for group and task.

def reset_db():
    list_filename = []
    for filename in os.listdir(DB_DIR):
        file_path = os.path.join(DB_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            list_filename.append(filename)
    
    # Create empty files for group and task
    for filename in list_filename:
        create_json_file(filename)



# This function creates a JSON file with the specified filename and initializes it with an empty dictionary.
def create_json_file(filename):
    
    data = {
       
    }
    
    file_path = db_file_path(filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)



def db_file_path(filename):
    return os.path.join(DB_DIR, filename)
