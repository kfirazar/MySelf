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
    group_id = inner_function.generate_random_id()
    group_object = {
        "id": group_id,
        "name": group_name,
        # Add any additional parameters to the group object
        **kwargs
    }
    return group_object

# This function retrieves the group object from the JSON file based on the provided group name.
# Can return several group objects if there are multiple groups with the same name.
def get_group_object(group_name):
    with open('group.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Filter the group objects based on the provided group name
    group_objects = [group for group in data.values() if group.get("name") == group_name and group.get("type") == "group"]
    
    return group_objects




"""
 The data is saving/updating in a structured format, making it easy to read and access later.
 Currently, the type saved in _types object.
 If group object DOES NOT exist in the JSON file, it will be added to the file.
 If the group object already exists (based on the group id), it will be updated with the new information provided in the group_object parameter.
 The KEY value for a group object in the JSON file is the unique ID of the group, which is generated using the generate_random_id function.
"""
def save_to_json_file(group_object, filename='group.json'):
    with open(filename, 'r') as json_file:
        data = json.load(json_file) 
    
    # Get the group ID
    group_id = group_object.get("id")
    group_object.pop("id")  

    # Check if the group object already exists in the JSON file by checking if the ID exists as a key (O(1) operation)
    if group_id in data:
        # Update the existing group object with the new information
        data[group_id].update(group_object)
        
    else:
        # Add the new group object to the JSON file using its unique ID as the key
        data[group_id] = group_object

    # Write the updated data back to the JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    

g1 = create_group_object("Group 1", description="This is the first group",category="A")
save_to_json_file(g1)
g2 = create_group_object("Group 2", description="This is the second group")
save_to_json_file(g2)