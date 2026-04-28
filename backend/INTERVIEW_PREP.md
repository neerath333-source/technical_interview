# Technical Interview Preparation Guide

This document outlines the key technical decisions, architectural patterns, and security measures implemented in this project. Use this to prepare for your technical walkthrough.

---

## 1. Project Architecture (The "App Factory" Pattern)

**Question:** Why did you use `create_app()` instead of just `app = Flask(__name__)`?

**Explanation:** This is called the **Application Factory Pattern**. 
- **Scalability:** It allows us to create multiple instances of the app with different configurations (e.g., one for testing, one for production).
- **Organization:** By using **Blueprints** (`auth_bp`, `tasks_bp`), we separate logic into modular components.
- **Avoids Circular Imports:** In large projects, keeping the app initialization separate from routes prevents the common "circular import" error.

**Example:**
```python
# app/__init__.py
def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config['MONGO_URI'] = "test_url"
    app.register_blueprint(auth_bp)
    return app
```

---

## 2. Multi-tenant Data Isolation

**Question:** How do you ensure Tenant A cannot see Tenant B's data?

**Explanation:** We use **Query-level Filtering**. 
- Every task in the database has a `tenant_id` field.
- When a user logs in, their `tenant_id` is encoded into the **JWT Token**.
- In every CRUD operation, we extract the `tenant_id` from the token and force it into the MongoDB query.

**Example Logic:**
```python
# Secure query: Even if a user knows a task_id, they can't see it unless the tenant_id matches.
task = mongo.db.tasks.find_one({
    "task_id": target_id, 
    "tenant_id": current_user['tenant_id'] 
})
```

---

## 3. Security: Password Hashing & JWT

**Question:** How are you handling authentication? Why not use Simple Cookies?

**Explanation:**
- **Password Hashing:** We use `bcrypt`. We never store passwords as plain text. Only the **salted hash** is stored. Even if the database is leaked, passwords remain secure.
- **JWT (JSON Web Tokens):** We use JWT because it is **stateless**. The server doesn't need to store session data in memory. All user info (IDs, roles, tenants) is securely signed inside the token.
- **Authorization Header:** We look for the token in the `Authorization: Bearer <token>` header, which is an industry-standard practice.

---

## 4. Security: Why UUID over Auto-Increment IDs?

**Question:** Why use UUIDs (string IDs) instead of integer IDs (1, 2, 3...)?

**Explanation:**
- **Insecurity of Integers:** If the ID of my task is `5`, I can guess that user `6` exists. This is called an **ID Enumeration Attack**.
- **Information Leak:** Sequential IDs leak information about how many records exist in the database.
- **UUIDs (Random IDs):** They are impossible to guess, making the API more secure and allowing for easier data migration or merging across multiple databases in the future.

---

## 5. Audit Tracking (Transparency)

**Question:** What are these `created_by` and `updated_at` fields?

**Explanation:** This is **Audit Logging**. 
- In a professional environment, you must know **WHO** did **WHAT** and **WHEN**.
- If a task is accidentally deleted or modified, we can look at these fields to find the root cause.
- **Database Consistency:** It ensures that every record contains its own history metadata.

---

## 6. Automated Testing (Pytest)

**Question:** How did you verify your code works?

**Explanation:**
- **Integration Testing:** I used `pytest` to automate the entire user lifecycle: Register -> Login -> CRUD -> Delete.
- **Test Database Separation:** I implemented a switch (`FLASK_TESTING=True`) that points the API to a **separate test database**. This prevents test data from polluting the real production data.
- **Response Validation:** We don't just check status codes; we verify the **JSON body** to ensure the data returned is what was actually requested.

---

## 7. Input Validation Logic

**Question:** How do you handle wrong inputs? Do you rely on the frontend?

**Explanation:**
- **Backend First:** I never trust the frontend. I implemented manual validation using **Regular Expressions (Regex)** for emails and strong password rules (Uppercase, Number, Special Character).
- **Custom Error Responses:** Instead of the app crashing, it returns a 400 Bad Request with a clear JSON error message, making it easy for frontend developers to debug.

---

## Summary for the Interviewer
"I have built a **Production-Ready**, **Multi-tenant** REST API. It uses **JWT** for secure sessions, **Bcrypt** for password safety, **UUIDs** for identifier security, and is fully covered by **Integration Tests** using Pytest. The code is modular, following the **App Factory** pattern, making it scalable for future features."
