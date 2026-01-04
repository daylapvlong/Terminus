#!/usr/bin/env python3
"""Initialize test database with sample data."""

import sqlite3
from pathlib import Path

DB_PATH = Path("/data/users.db")

def init_database():
    """Create users table and populate with test data."""
    # Remove old database if exists
    if DB_PATH.exists():
        DB_PATH.unlink()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    # Insert test data
    test_users = [
        (1, "alice", "alice@example.com", "admin"),
        (2, "bob", "bob@example.com", "user"),
        (3, "charlie", "charlie@example.com", "user"),
        (4, "admin", "admin@example.com", "admin"),
    ]
    
    cursor.executemany(
        "INSERT INTO users (id, username, email, role) VALUES (?, ?, ?, ?)",
        test_users
    )
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DB_PATH}")
    print(f"Created {len(test_users)} test users")

if __name__ == "__main__":
    init_database()