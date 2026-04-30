from flask import Blueprint, request, jsonify
from .utils import generate_uuid, hash_password, get_audit_fields, validate_email, validate_password, validate_name, check_password_hash, generate_token
from .services import find_user_by_email, find_user_by_username_or_email, create_user, update_user_last_login
from .schemas import UserRegisterSchema, UserLoginSchema, ValidationError
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

    # Pydantic Validation
    try:
        validated_data = UserLoginSchema(**request_data)
    except ValidationError as e:
        error_msg = e.errors()[0]['msg']
        if error_msg.startswith('Value error, '):
            error_msg = error_msg.replace('Value error, ', '')
        return jsonify({"error": error_msg}), 400

    email = validated_data.email
    password = validated_data.password

    # find user by email using Service
    user_document = find_user_by_email(email)

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

    # update last login in audit fields using Service
    update_user_last_login(user_document['user_id'])

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
    # Get request data
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "No data provided"}), 400

    # Pydantic Validation
    try:
        validated_data = UserRegisterSchema(**request_data)
    except ValidationError as e:
        # Extract the first error message for simplicity in response
        error_msg = e.errors()[0]['msg']
        # Clean up 'Value error, ' prefix if present
        if error_msg.startswith('Value error, '):
            error_msg = error_msg.replace('Value error, ', '')
        return jsonify({"error": error_msg}), 400

    username = validated_data.username
    email = validated_data.email
    password = validated_data.password
    tenant_name = validated_data.tenant_name

    # check if user already exists using Service
    existing_user = find_user_by_username_or_email(username, email)
    if existing_user:
        return jsonify({"error": "User with this username or email already exists"}), 409

    # New Tenant ID logic: {tenant_name}_{uuid}
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

    # manual storage using Service
    create_user(new_user_document)

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id,
        "tenant_id": final_tenant_id
    }), 201
