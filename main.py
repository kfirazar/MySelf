

from handle_function import create_group_object, create_task_object, remove_fields_from_object,save_object_to_json_file
from inner_function import reset_db



g1 = create_group_object("Group 1", description="This is the first group",category="A")
g1_id = g1["id"]
g1 = remove_fields_from_object(g1, "id")
save_object_to_json_file(g1, g1_id, 'group.json')


t1 = create_task_object(g1_id, "Task 1", description="This is the first task", priority="High")
t1_id = t1["id"]
t1 = remove_fields_from_object(t1, "id")
save_object_to_json_file(t1, t1_id, 'task.json')

