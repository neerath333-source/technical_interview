from ..database import mongo
from datetime import datetime

def find_user_by_email(email):
    """Finds a user by their email address."""
    return mongo.db.users.find_one({"email": email})

def find_user_by_username_or_email(username, email):
    """Checks if a user already exists with the given username or email."""
    return mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})

def create_user(user_data):
    """Inserts a new user document into the database."""
    return mongo.db.users.insert_one(user_data)

def update_user_last_login(user_id):
    """Updates the last login and updated_at timestamps for a user."""
    return mongo.db.users.update_one(
        {"user_id": user_id},
        {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )
