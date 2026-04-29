from flask import Blueprint, request, jsonify
from ..auth.utils import token_required, generate_uuid, get_audit_fields
from .services import create_task_record, get_tenant_tasks, get_task_by_id_and_tenant, update_task_record, delete_task_record
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/add_task', methods=['POST'])
@token_required
def create_task(current_user):
    # these also for swagger tagnames and more
    """
    Create Task API
    ---
    tags:
      - Task Management
    security:
      - APIKeyHeader: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: CreateTask
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Task created successfully
      401:
        description: Unauthorized
    """
    request_data = request.get_json()
    title = request_data.get('title')
    description = request_data.get('description')

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task_id = generate_uuid()
    audit_data = get_audit_fields(user_identifier=current_user['user_id'])
    
    new_task = {
        "_id": task_id,
        "task_id": task_id,
        "tenant_id": current_user['tenant_id'], # Auto-link to current user's tenant
        "title": title,
        "description": description,
        "status": "pending",
        "created_at": audit_data['created_at'],
        "updated_at": audit_data['updated_at'],
        "created_by": audit_data['created_by'],
        "updated_by": audit_data['updated_by']
    }

    # Use Service to create task
    create_task_record(new_task)
    
    # Returning the created task object (excluding Mongo _id) for better visibility
    created_task_info = new_task.copy()
    del created_task_info['_id']
    created_task_info['created_at'] = created_task_info['created_at'].isoformat()
    created_task_info['updated_at'] = created_task_info['updated_at'].isoformat()

    return jsonify({
        "message": "Task created successfully", 
        "task_id": task_id,
        "task_data": created_task_info
    }), 201

@tasks_bp.route('/list_tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    # these also for swagger tagnames and more
    """
    List all tasks for current tenant
    ---
    tags:
      - Task Management
    security:
      - APIKeyHeader: []
    responses:
      200:
        description: List of tasks
    """
    # Use Service to fetch tasks
    tenant_tasks_list = get_tenant_tasks(current_user['tenant_id'])
    
    tasks_to_return = []
    for task_document in tenant_tasks_list:
        tasks_to_return.append({
            "task_id": task_document['task_id'],
            "title": task_document['title'],
            "description": task_document.get('description', ''),
            "status": task_document['status'],
            "created_at": task_document['created_at'].isoformat()
        })

    return jsonify({
        "total_count": len(tasks_to_return),
        "tasks": tasks_to_return
    }), 200

@tasks_bp.route('/view_task/<task_id>', methods=['GET'])
@token_required
def get_task_by_id(current_user, task_id):
    # these also for swagger tagnames and more
    """
    Get a specific task
    ---
    tags:
      - Task Management
    security:
      - APIKeyHeader: []
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Task details
      404:
        description: Task not found
    """
    # Use Service to find a specific task
    task_document = get_task_by_id_and_tenant(task_id, current_user['tenant_id'])

    if not task_document:
        return jsonify({"error": "Task not found or access denied"}), 404

    return jsonify({
        "task_id": task_document['task_id'],
        "title": task_document['title'],
        "description": task_document.get('description', ''),
        "status": task_document['status'],
        "tenant_id": task_document['tenant_id'],
        "audit": {
            "created_at": task_document['created_at'].isoformat(),
            "updated_at": task_document['updated_at'].isoformat(),
            "created_by": task_document['created_by']
        }
    }), 200

@tasks_bp.route('/update_task/<task_id>', methods=['PUT'])
@token_required
def update_task_endpoint(current_user, task_id):
  # these also for swagger tagnames and more
    """
    Update a task
    ---
    tags:
      - Task Management
    security:
      - APIKeyHeader: []
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
      - name: body
        in: body
        schema:
          properties:
            title:
              type: string
            status:
              type: string
            description:
              type: string
    responses:
      200:
        description: Task updated successfully
    """
    request_data = request.get_json()
    
    # Verify ownership using Service
    existing_task = get_task_by_id_and_tenant(task_id, current_user['tenant_id'])

    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    # Prepare update logic
    update_fields_dict = {
        "updated_at": datetime.utcnow(),
        "updated_by": current_user['user_id']
    }
    
    if 'title' in request_data:
        update_fields_dict['title'] = request_data['title']
    if 'status' in request_data:
        update_fields_dict['status'] = request_data['status']
    if 'description' in request_data:
        update_fields_dict['description'] = request_data['description']

    # Use Service to update
    update_task_record(task_id, update_fields_dict)
    
    return jsonify({
        "message": "Task updated successfully",
        "updated_fields": request_data,
        "task_id": task_id
    }), 200

@tasks_bp.route('/delete_task/<task_id>', methods=['DELETE'])
@token_required
def delete_task_endpoint(current_user, task_id):
    """
    Delete a task
    ---
    tags:
      - Task Management
    security:
      - APIKeyHeader: []
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Task deleted successfully
    """
    # Use Service to delete
    result_status = delete_task_record(task_id, current_user['tenant_id'])

    if result_status.deleted_count == 0:
        return jsonify({"error": "Task not found or access denied"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200
