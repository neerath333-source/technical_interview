from flask import Blueprint, request, jsonify
from ..database import mongo
from .utils import generate_uuid, hash_password, get_audit_fields, validate_email, validate_password, validate_name, check_password_hash, generate_token
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Login API
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserLogin
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "No data provided"}), 400

    email = request_data.get('email')
    password = request_data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and Password are required"}), 400

    # Strong Email Validation (Check format)
    email_valid, email_error = validate_email(email)
    if not email_valid:
        return jsonify({"error": email_error}), 400

    # find user by email
    user_document = mongo.db.users.find_one({"email": email})

    if not user_document:
        return jsonify({"error": "Invalid email or password"}), 401

    # check password
    is_password_valid = check_password_hash(user_document['password_hash'], password)
    if not is_password_valid:
        return jsonify({"error": "Invalid username or password"}), 401

    # create JWT token
    user_payload = {
        "user_id": user_document['user_id'],
        "tenant_id": user_document['tenant_id'],
        "role": user_document['role']
    }
    access_token = generate_token(user_payload)

    # update last login in audit fields
    mongo.db.users.update_one(
        {"_id": user_document["_id"]},
        {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "Bearer",
        "user_id": user_document['user_id'],
        "tenant_id": user_document['tenant_id']
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User Registration API
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserRegistration
          required:
            - username
            - email
            - password
            - tenant_name
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
            tenant_name:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Validation error
      409:
        description: User already exists
    """
    # manual input retrieval
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "No data provided"}), 400

    username = request_data.get('username')
    email = request_data.get('email')
    password = request_data.get('password')
    tenant_name = request_data.get('tenant_name')

    # manual validation
    if not username or not email or not password or not tenant_name:
        return jsonify({"error": "Missing required fields (username, email, password, tenant_name)"}), 400

    # Strong Email Validation
    email_valid, email_error = validate_email(email)
    if not email_valid:
        return jsonify({"error": email_error}), 400

    # Strong Password Validation
    password_valid, password_error = validate_password(password)
    if not password_valid:
        return jsonify({"error": password_error}), 400

    # Character-only Validation for Name fields
    tenant_name_valid, tenant_name_error = validate_name(tenant_name)
    if not tenant_name_valid:
        return jsonify({"error": f"Tenant Name error: {tenant_name_error}"}), 400

    # check if user already exists
    existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        return jsonify({"error": "User with this username or email already exists"}), 409

    # New Tenant ID logic: {tenant_name}_{uuid}
    # Sanitize tenant name (lowercase and remove spaces)
    sanitized_tenant_name = tenant_name.lower().replace(" ", "_")
    unique_uuid = generate_uuid()
    final_tenant_id = f"{sanitized_tenant_name}_{unique_uuid}"

    # prepare user document
    user_id = generate_uuid()
    hashed_password = hash_password(password)
    audit_data = get_audit_fields(user_identifier="self_register")

    new_user_document = {
        "_id": user_id,
        "user_id": user_id,
        "tenant_id": final_tenant_id,
        "username": username,
        "email": email,
        "password_hash": hashed_password,
        "role": "user",
        "is_active": True,
        "last_login": None,
        "created_at": audit_data["created_at"],
        "updated_at": audit_data["updated_at"],
        "created_by": audit_data["created_by"],
        "updated_by": audit_data["updated_by"]
    }

    # manual storage
    mongo.db.users.insert_one(new_user_document)

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id,
        "tenant_id": final_tenant_id
    }), 201
