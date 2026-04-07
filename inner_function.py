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
