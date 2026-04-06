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
