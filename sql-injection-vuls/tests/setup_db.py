#!/usr/bin/env python3
"""Setup test database for SQL injection tests."""

import sqlite3
from pathlib import Path

DB_PATH = Path("/data/users.db")

def setup_test_db():
    """Create and populate test database."""
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
    
    print(f"Test database created at {DB_PATH}")

if __name__ == "__main__":
    setup_test_db()