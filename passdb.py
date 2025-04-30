import json
import os

DB_FILE = "pass.json"
def save_pass(username, website, email, password, date):
    """Save password details under a username to JSON file"""
    users = load_pass()

    # Fix for old format (dict) or new format (list)
    if username not in users:
        users[username] = []
    elif isinstance(users[username], dict):
        # Convert old single-entry format to list
        users[username] = [users[username]]

    # Append new entry as a dictionary
    users[username].append({
        "website": website,
        "email": email,
        "password": password,
        "date": date
    })

    try:
        with open(DB_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving user: {e}")

def load_pass(username=None):
    """Load password details from the JSON file"""
    if not os.path.exists(DB_FILE):
        return {} if not username else []
    with open(DB_FILE, 'r') as f:
        data = json.load(f)
    if username:
        return data.get(username, [])
    return data
    