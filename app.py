from flask import Flask, render_template, request, jsonify
import handle_function
import inner_function
import json
import os

app = Flask(__name__)


def normalize_group_fields(fields):
    if not isinstance(fields, list):
        fields = []

    normalized = []
    for field in fields:
        if not isinstance(field, str):
            continue
        field_name = field.strip()
        if not field_name or field_name in normalized:
            continue
        normalized.append(field_name)

    if 'name' in normalized:
        normalized = ['name'] + [field for field in normalized if field != 'name']
    else:
        normalized.insert(0, 'name')

    return normalized


def get_next_group_order():
    groups = handle_function.load_json_file('group.json')
    existing_orders = [
        group.get('order')
        for group in groups.values()
        if isinstance(group.get('order'), int)
    ]

    if existing_orders:
        return max(existing_orders) + 1

    return len(groups)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/groups', methods=['GET'])
def get_groups():
    try:
        return jsonify(handle_function.get_all_groups())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/groups/reorder', methods=['PUT'])
def reorder_groups():
    try:
        data = request.get_json(silent=True) or {}
        ordered_group_ids = data.get('ordered_group_ids')

        if not isinstance(ordered_group_ids, list) or not ordered_group_ids:
            return jsonify({'error': 'ordered_group_ids must be a non-empty list'}), 400

        if len(ordered_group_ids) != len(set(ordered_group_ids)):
            return jsonify({'error': 'ordered_group_ids contains duplicates'}), 400

        groups = handle_function.load_json_file('group.json')
        existing_ids = set(groups.keys())
        incoming_ids = set(ordered_group_ids)

        if existing_ids != incoming_ids:
            return jsonify({'error': 'ordered_group_ids must include all groups exactly once'}), 400

        for order_index, group_id in enumerate(ordered_group_ids):
            groups[group_id]['order'] = order_index

        with open(inner_function.db_file_path('group.json'), 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        return jsonify({'ordered_group_ids': ordered_group_ids})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/groups/<group_id>', methods=['PUT'])
def update_group(group_id):
    try:
        data = request.get_json(silent=True) or {}
        groups = handle_function.load_json_file('group.json')

        if group_id not in groups:
            return jsonify({'error': 'Group not found'}), 404

        updates = {}
        if 'name' in data:
            name = (data.get('name') or '').strip()
            if not name:
                return jsonify({'error': 'Group name is required'}), 400
            updates['name'] = name

        if 'description' in data:
            updates['description'] = (data.get('description') or '').strip()

        if 'category' in data:
            updates['category'] = (data.get('category') or '').strip()

        if not updates:
            return jsonify({'error': 'No valid group fields supplied'}), 400

        groups[group_id].update(updates)

        with open(inner_function.db_file_path('group.json'), 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        return jsonify({'id': group_id, **groups[group_id]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        return jsonify(handle_function.get_all_tasks())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_group', methods=['POST'])
def create_group():
    try:
        data = request.get_json(silent=True) or {}
        group_name = (data.get('name') or '').strip()
        description = (data.get('description') or '').strip()
        category = (data.get('category') or '').strip()

        if not group_name:
            return jsonify({'error': 'Group name is required'}), 400

        group = handle_function.create_group_object(
            group_name,
            description=description,
            category=category,
            fields=['name'],
            order=get_next_group_order()
        )

        # Save to group.json using the existing save function
        handle_function.save_object_to_json_file(
            handle_function.remove_fields_from_object(group.copy(), 'id'),
            group['id'],
            'group.json'
        )

        return jsonify(group)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_task', methods=['POST'])
def create_task():
    try:
        data = request.get_json(silent=True) or {}
        group_id = data.get('group_id')
        task_name = data.get('name')
        #getting the extra unexpected fields from the request body and pass them to the create_task_object function
        dynamic_field = {k: v for k, v in data.items() if k not in ['group_id', 'name']}

        if not group_id or not task_name:
            return jsonify({'error': 'Group ID and task name are required'}), 400

        groups = handle_function.load_json_file('group.json')
        group = groups.get(group_id)
        if not group:
            return jsonify({'error': 'Group not found'}), 404

        group_fields = normalize_group_fields(group.get('fields', []))
        for field in group_fields:
            if field == 'name':
                continue
            if field not in dynamic_field:
                dynamic_field[field] = ''

        task = handle_function.create_task_object(
            group_id,
            task_name,
            **dynamic_field
        )

        return jsonify(task)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/groups/<group_id>/fields', methods=['PUT'])
def add_group_field(group_id):
    try:
        data = request.get_json(silent=True) or {}
        field_name = (data.get('field_name') or '').strip()
        if not field_name:
            return jsonify({'error': 'Field name is required'}), 400

        groups = handle_function.load_json_file('group.json')
        if group_id not in groups:
            return jsonify({'error': 'Group not found'}), 404

        existing_fields = groups[group_id].get('fields', [])
        merged_fields = []
        if isinstance(existing_fields, list):
            merged_fields.extend(existing_fields)
        if field_name not in merged_fields:
            merged_fields.append(field_name)

        groups[group_id]['fields'] = normalize_group_fields(merged_fields)

        with open(inner_function.db_file_path('group.json'), 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        tasks = handle_function.load_json_file('task.json')
        changed = False
        for task in tasks.values():
            if task.get('group_id') != group_id:
                continue
            if field_name not in task:
                task[field_name] = ''
                changed = True

        if changed:
            with open(inner_function.db_file_path('task.json'), 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=4, ensure_ascii=False)

        return jsonify({'fields': groups[group_id]['fields']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rename_field', methods=['PUT'])
def rename_field():
    try:
        data = request.get_json(silent=True) or {}
        group_id = data.get('group_id')
        old_field_name = (data.get('old_field_name') or '').strip()
        new_field_name = (data.get('new_field_name') or '').strip()

        if not group_id or not old_field_name or not new_field_name:
            return jsonify({'error': 'group_id, old_field_name and new_field_name are required'}), 400

        if old_field_name == 'name':
            return jsonify({'error': 'Field "name" cannot be renamed'}), 400

        groups = handle_function.load_json_file('group.json')
        if group_id not in groups:
            return jsonify({'error': 'Group not found'}), 404

        group_fields = groups[group_id].get('fields', [])
        if not isinstance(group_fields, list):
            group_fields = []

        updated_fields = []
        for field in group_fields:
            if field == old_field_name:
                updated_fields.append(new_field_name)
            else:
                updated_fields.append(field)

        if old_field_name not in group_fields:
            updated_fields.append(new_field_name)

        groups[group_id]['fields'] = normalize_group_fields(updated_fields)

        tasks = handle_function.load_json_file('task.json')
        for task in tasks.values():
            if task.get('group_id') != group_id:
                continue
            if old_field_name in task:
                task[new_field_name] = task.pop(old_field_name)

        with open(inner_function.db_file_path('group.json'), 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4, ensure_ascii=False)

        with open(inner_function.db_file_path('task.json'), 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)

        return jsonify({'fields': groups[group_id]['fields']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json(silent=True) or {}
        # Load existing task
        tasks = handle_function.load_json_file('task.json')
        if task_id not in tasks:
            return jsonify({'error': 'Task not found'}), 404
        
        # Merge new data with existing task
        tasks[task_id].update(data)
        

        # Save back
        with open(inner_function.db_file_path('task.json'), 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
        
        return jsonify(tasks[task_id])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
