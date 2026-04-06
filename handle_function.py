import json
import inner_function


# This function creates a JSON file with the specified filename and initializes it with an empty dictionary.
def create_json_file(filename='group.json'):
    data = {
       
    }
    
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# This function create a group instance with at least a name and a randomy generated id.
# The function can also accept additional parameters, which can be used to customize the group object further.
# For time complexity, the ids will be keys in the JSON file, so we can directly access the group object using its unique ID without needing to loop through the entire file. This allows for efficient retrieval and updating of group objects based on their unique IDs.
def create_group_object(group_name, **kwargs):
    group_id = inner_function.generate_virtual_id(group_name)
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
def create_task_object(group_id, task_name, filename='group.json', **kwargs):
    task_id = inner_function.generate_random_id()
    task_object = {
        "id": task_id,
        "name": task_name,
        "group_id": group_id,
        "type": "task",
        **kwargs
    }
    
    # Load data
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    
    # Add task to data
    data[task_id] = task_object
    
    # Add task_id to group's tasks list
    if group_id in data and data[group_id].get("type") == "group":
        data[group_id]["tasks"].append(task_id)
    
    # Save data
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    return task_object


# This function retrieves the group object from the JSON file based on the provided group name.
# Can return several group objects if there are multiple groups with the same name.
def get_group_object(group_name, filename='group.json'):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return []
    
    # Filter the group objects based on the provided group name
    group_objects = [group for group in data.values() if group.get("name") == group_name and group.get("type") == "group"]
    
    return group_objects



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
    try:
        with open(filename, 'r') as json_file:
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
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)



    

g1 = create_group_object("Group 1", description="This is the first group",category="A")
g1_id = g1["id"]
g1 = remove_fields_from_object(g1, "id")
save_object_to_json_file(g1, g1_id, 'group.json')

g2 = create_group_object("Group 2", description="This is the second group")
g2_id = g2["id"]
g2 = remove_fields_from_object(g2, "id")
save_object_to_json_file(g2, g2_id, 'group.json')