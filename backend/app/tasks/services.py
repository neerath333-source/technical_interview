from ..database import mongo
from datetime import datetime

def create_task_record(task_data):
    """Inserts a new task into the database."""
    return mongo.db.tasks.insert_one(task_data)

def get_tenant_tasks(tenant_id):
    """Retrieves all tasks belonging to a specific tenant."""
    return list(mongo.db.tasks.find({"tenant_id": tenant_id}))

def get_task_by_id_and_tenant(task_id, tenant_id):
    """Retrieves a specific task ensured by tenant isolation."""
    return mongo.db.tasks.find_one({
        "task_id": task_id,
        "tenant_id": tenant_id
    })

def update_task_record(task_id, update_fields):
    """Updates a task document with the provided fields."""
    return mongo.db.tasks.update_one(
        {"task_id": task_id}, 
        {"$set": update_fields}
    )

def delete_task_record(task_id, tenant_id):
    """Deletes a task confirmed by tenant ownership."""
    return mongo.db.tasks.delete_one({
        "task_id": task_id,
        "tenant_id": tenant_id
    })
