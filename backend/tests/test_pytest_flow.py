import requests
import uuid
import pytest
import json

BASE_URL = "http://127.0.0.1:5000/api"

def print_json(data):
    """Helper to pretty print JSON"""
    print(json.dumps(data, indent=4))

@pytest.fixture(scope="module")
def test_data():
    """Generates unique data for the test run."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"pytest_{unique_id}@example.com",
        "username": f"user_{unique_id}",
        "password": "SecurePassword@123",
        "tenant_name": "PytestCorp"
    }

def test_full_application_flow(test_data):
    print("\n--- Starting Full Application Flow Test ---")
    
    # 1. Register User
    print(f"\nScenario 1: Registering user {test_data['email']}...")
    reg_url = f"{BASE_URL}/auth/register"
    reg_resp = requests.post(reg_url, json=test_data)
    print(f"Status Code: {reg_resp.status_code}")
    print_json(reg_resp.json())
    assert reg_resp.status_code == 201
    
    # 2. Login
    print("\nScenario 2: Logging in to obtain access token...")
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {"email": test_data['email'], "password": test_data['password']}
    login_resp = requests.post(login_url, json=login_payload)
    print(f"Status Code: {login_resp.status_code}")
    print("Token obtained successfully.")
    assert login_resp.status_code == 200
    
    token = login_resp.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Task
    print("\nScenario 3: Creating a new task...")
    create_url = f"{BASE_URL}/tasks/add_task"
    task_payload = {"title": "Pytest Task", "description": "Testing via pytest"}
    create_resp = requests.post(create_url, json=task_payload, headers=headers)
    print(f"Status Code: {create_resp.status_code}")
    print_json(create_resp.json())
    assert create_resp.status_code == 201
    task_id = create_resp.json().get('task_id')
    
    # 4. List Tasks
    print("\nScenario 4: Listing all tasks...")
    list_url = f"{BASE_URL}/tasks/list_tasks"
    list_resp = requests.get(list_url, headers=headers)
    print(f"Status Code: {list_resp.status_code}")
    print_json(list_resp.json())
    assert list_resp.status_code == 200
    
    # 5. Update Task
    print(f"\nScenario 5: Updating task {task_id} status to 'in-progress'...")
    update_url = f"{BASE_URL}/tasks/update_task/{task_id}"
    update_payload = {"status": "in-progress", "title": "Pytest Task - UPDATED"}
    update_resp = requests.put(update_url, json=update_payload, headers=headers)
    print(f"Status Code: {update_resp.status_code}")
    print_json(update_resp.json())
    assert update_resp.status_code == 200
    
    # 6. Delete Task
    print(f"\nScenario 6: Deleting task {task_id}...")
    delete_url = f"{BASE_URL}/tasks/delete_task/{task_id}"
    delete_resp = requests.delete(delete_url, headers=headers)
    print(f"Status Code: {delete_resp.status_code}")
    print_json(delete_resp.json())
    assert delete_resp.status_code == 200
    print("\n--- Full Flow Test Completed ---")

def test_invalid_login(test_data):
    print("\nScenario 7: Testing Invalid Login (Wrong Password)...")
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {"email": test_data['email'], "password": "WrongPassword!"}
    login_resp = requests.post(login_url, json=login_payload)
    print(f"Status Code: {login_resp.status_code}")
    print_json(login_resp.json())
    assert login_resp.status_code == 401

def test_unauthorized_access():
    print("\nScenario 8: Testing Unauthorized Access (No Token)...")
    list_url = f"{BASE_URL}/tasks/list_tasks"
    list_resp = requests.get(list_url)
    print(f"Status Code: {list_resp.status_code}")
    print_json(list_resp.json())
    assert list_resp.status_code == 401
