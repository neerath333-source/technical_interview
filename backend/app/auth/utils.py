import uuid
import bcrypt
import re
import jwt
import os
from datetime import datetime, timedelta

def generate_uuid():
    """Generates a string representation of a UUID."""
    return str(uuid.uuid4())

def hash_password(password):
    """Hashes a plain text password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def validate_password(password):
    """Checks if password has 1 caps, 1 special char, and 1 number."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # manual regex check
    has_upper = re.search(r"[A-Z]", password)
    has_lower = re.search(r"[a-z]", password)
    has_number = re.search(r"\d", password)
    has_special = re.search(r"[@$!%*#?&]", password)

    if not has_upper:
        return False, "Password must contain at least one uppercase letter"
    if not has_number:
        return False, "Password must contain at least one number"
    if not has_special:
        return False, "Password must contain at least one special character (@$!%*#?&)"
    
    return True, "Valid"

def validate_email(email):
    """Checks for @ and ensures email is valid."""
    # check for @
    if "@" not in email:
        return False, "Invalid email: @ symbol is missing"
    
    # regex for basic email format
    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format or contains uppercase letters (must be lowercase)"
    
    return True, "Valid"

def validate_name(name_value):
    """Checks if the field contains only alphabetic characters."""
    if not name_value:
        return False, "Field cannot be empty"
    
    # regex for only letters and spaces
    if not re.match(r"^[a-zA-Z\s]+$", name_value):
        return False, "Field must contain only characters (no numbers or special characters allowed)"
    
    return True, "Valid"

from ..config import Config

def generate_token(user_payload):
    """Generates a JWT token for the user."""
    # secret key from config/env
    secret_key = Config.JWT_SECRET
    
    # set expiration from config
    hours_to_expire = Config.JWT_EXPIRY_HOURS
    expiration_time = datetime.utcnow() + timedelta(hours=hours_to_expire)
    
    token_payload = {
        "user_id": user_payload.get("user_id"),
        "tenant_id": user_payload.get("tenant_id"),
        "role": user_payload.get("role"),
        "exp": expiration_time
    }
    
    # encode token
    token = jwt.encode(token_payload, secret_key, algorithm="HS256")
    return token

import functools
from flask import request, jsonify

def token_required(wrapped_function):
    """Decorator to protect routes with JWT authentication."""
    @functools.wraps(wrapped_function)
    def decorator_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 401
        
        # Flexiblity: Support both 'Bearer {token}' and just '{token}'
        if auth_header.startswith('Bearer '):
            # Split and take the second part
            token_parts = auth_header.split(" ")
            if len(token_parts) < 2:
                return jsonify({"error": "Invalid Bearer token format"}), 401
            token = token_parts[1]
        else:
            # Assume the whole header is the token (helpful for Swagger/direct testing)
            token = auth_header
        
        try:
            # Decode token
            secret_key = Config.JWT_SECRET
            decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            # Add user/tenant info to the request for the route to use
            current_user_info = {
                "user_id": decoded_payload.get("user_id"),
                "tenant_id": decoded_payload.get("tenant_id"),
                "role": decoded_payload.get("role")
            }
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
            
        return wrapped_function(current_user_info, *args, **kwargs)
        
    return decorator_function

def check_password_hash(hashed_password, plain_password):
    """Verifies if the plain password matches the hashed one."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_audit_fields(user_identifier="system"):
    """Returns a dictionary with standard audit fields."""
    now = datetime.utcnow()
    return {
        "created_at": now,
        "updated_at": now,
        "created_by": user_identifier,
        "updated_by": user_identifier
    }
