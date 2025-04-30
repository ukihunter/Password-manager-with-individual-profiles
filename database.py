import json
import os

DB_FILE = "users.json"

def save_user(username, password):
    """Save user to JSON file"""
    users = load_users()
    users[username] = password
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving user: {e}")

def load_users():
    """Load all users from JSON file"""
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        with open(DB_FILE, 'r') as f:
            # Check if file is empty
            content = f.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading users: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def validate_user(username, password):
    """Check if user exists and password matches"""
    users = load_users()
    return users.get(username) == password