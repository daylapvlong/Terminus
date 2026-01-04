#!/usr/bin/env python3
"""Database query module with SQL injection vulnerability."""

import sqlite3
from pathlib import Path

DB_PATH = Path("/data/users.db")

def get_user(username):
    """
    Get user by username.
    
    Args:
        username: Username to search for
        
    Returns:
        Tuple of (id, username, email, role) if found, None otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # BUG: SQL injection vulnerability - using string formatting
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    
    return result

def list_all_users():
    """List all users in database (for testing)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Test queries
    print("Testing get_user function...")
    
    # Normal query
    user = get_user("alice")
    print(f"get_user('alice'): {user}")
    
    # SQL injection attempt
    try:
        injected = get_user("' OR '1'='1")
        print(f"get_user(\"' OR '1'='1\"): {injected}")
    except Exception as e:
        print(f"Error: {e}")
    
    # List all users
    print(f"\nAll users: {list_all_users()}")