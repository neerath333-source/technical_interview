# Multi-tenant Task Management REST API (Flask)

A professional, secure, and multi-tenant backend built with Python Flask and MongoDB.

## Features
- **JWT Authentication**: Secure login and token-based access.
- **Multi-tenancy**: Data isolation based on `tenant_id`.
- **UUIDs**: All identifiers use random UUIDs for security.
- **Audit Logging**: Tracking `created_at`, `updated_at`, `created_by`, and `updated_by` for all records.
- **Standardized API**: RESTful endpoints with consistent JSON error handling.
- **Swagger Documentation**: Integrated API documentation via `/apidocs/`.

## Project Structure
```text
/backend
├── app/
│   ├── auth/             # Registration, Login, and JWT logic
│   ├── tasks/            # CRUD operations for Task management
│   ├── config.py         # Configuration management
│   ├── database.py       # MongoDB connection setup
│   └── __init__.py       # App Factory and Error Handlers
├── tests/                # Automated test scripts
├── .env                  # Configuration secrets
└── run.py                # Server entry point
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   python run.py
   ```
   The server will start at `http://127.0.0.1:5000`.

3. **API Documentation**:
   Visit `http://127.0.0.1:5000/apidocs/` to view and test the APIs via Swagger.

## Test Scripts
Run the following scripts in order to verify the system:
1. `python tests/test_auth_register.py` - Verify user registration.
2. `python tests/test_auth_login.py` - Verify login and token generation.
3. `python tests/test_tasks_crud.py` - Verify full CRUD flow with authentication.

## Interview Walkthrough Points
- **Security**: Explain the use of `bcrypt` for hashing and `HS256` for JWT tokens.
- **Scalability**: Highlight the "App Factory" pattern for modular development.
- **Data Privacy**: Stress how `tenant_id` prevents cross-tenant data access.
- **Validation**: Demonstrate manual regex validation for email, password, and names.
