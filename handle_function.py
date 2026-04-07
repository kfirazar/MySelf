import json
import os
import inner_function
import config

DB_DIR = config.get_db_dir()




# This function create a group instance with at least a name and a randomy generated id.
# The function can also accept additional parameters, which can be used to customize the group object further.
# For time complexity, the ids will be keys in the JSON file, so we can directly access the group object using its unique ID without needing to loop through the entire file. This allows for efficient retrieval and updating of group objects based on their unique IDs.
def create_group_object(group_name, **kwargs):
    group_id = inner_function.generate_random_id()
    group_object = {
        "id": group_id,
        "name": group_name,
        "type": "group",
        "tasks": [],
        # Add any additional parameters to the group object
        **kwargs
    }
    return group_object

# This function creates a task and adds it to the specified group object.
def create_task_object(group_id, task_name, filename='task.json', **kwargs):
    task_id = inner_function.generate_random_id()
    task_object = {
        "id": task_id,
        "name": task_name,
        "group_id": group_id,
        "type": "task",
        **kwargs
    }
    
    file_path = inner_function.db_file_path(filename)
    # Load data
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    
    # Add task to data
    data[task_id] = task_object
    
    # Save task data
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # Update the group's tasks list in group.json
    group_file_path = inner_function.db_file_path('group.json')
    try:
        with open(group_file_path, 'r') as json_file:
            group_data = json.load(json_file)
    except FileNotFoundError:
        group_data = {}
    
    # Find the group and add the task_id to its tasks list
    if group_id in group_data and group_data[group_id].get("type") == "group":
        if "tasks" not in group_data[group_id]:
            group_data[group_id]["tasks"] = []
        group_data[group_id]["tasks"].append(task_id)
        
        # Save updated group data
        with open(group_file_path, 'w') as json_file:
            json.dump(group_data, json_file, indent=4)
    
    
    return task_object



# This function retrieves the group object from the JSON file based on the provided group name.
# Can return several group objects if there are multiple groups with the same name.
# The extraction of the group name will 


# This function removes specific fields from the given object dictionary
# The fields to remove are given by *args
def remove_fields_from_object(obj, *args):
    for field in args:
        if field in obj:
            del obj[field]
    return obj


# This next function meant to be a base function function for saving an object in Json file
# All valadiation will occurs ahead of the function in other logic secton
# The "id" of the wanted ovbject will be given as a parameter
def save_object_to_json_file(object_to_save, object_id, filename):
    file_path = inner_function.db_file_path(filename)
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    
    # Check if the object already exists in the JSON file by checking if the ID exists as a key (O(1) operation)
    if object_id in data:
        # Update the existing object with the new information
        data[object_id].update(object_to_save)
        
    else:
        # Add the new object to the JSON file using its unique ID as the key
        data[object_id] = object_to_save

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)



    
