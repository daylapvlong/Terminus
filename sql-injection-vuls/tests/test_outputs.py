#!/usr/bin/env python3
"""Test suite for SQL injection vulnerability fix."""

import sys
import sqlite3
from pathlib import Path

# Add app to path so we can import db module
sys.path.insert(0, "/app")
import db

DB_PATH = Path("/data/users.db")

def test_database_exists():
    """Database file should exist."""
    assert DB_PATH.exists(), "Database file not found at /data/users.db"

def test_database_has_users():
    """Database should contain test users."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count == 4, f"Expected 4 users in database, got {count}"

def test_get_valid_user():
    """Should return user data for valid username."""
    result = db.get_user("alice")
    
    assert result is not None, "get_user('alice') returned None"
    assert len(result) == 4, f"Expected 4 fields, got {len(result)}"
    
    user_id, username, email, role = result
    assert username == "alice", f"Expected username 'alice', got '{username}'"
    assert email == "alice@example.com", f"Expected email 'alice@example.com', got '{email}'"
    assert role == "admin", f"Expected role 'admin', got '{role}'"

def test_get_nonexistent_user():
    """Should return None for non-existent username."""
    result = db.get_user("nonexistent")
    assert result is None, f"Expected None for non-existent user, got {result}"

def test_get_another_valid_user():
    """Should return correct data for bob."""
    result = db.get_user("bob")
    
    assert result is not None, "get_user('bob') returned None"
    user_id, username, email, role = result
    assert username == "bob", f"Expected username 'bob', got '{username}'"
    assert role == "user", f"Expected role 'user', got '{role}'"

def test_blocks_sql_injection_or_statement():
    """Should block SQL injection with OR statement."""
    # This injection attempt tries to return all users
    result = db.get_user("' OR '1'='1")
    
    # Should return None instead of any user data
    assert result is None, \
        f"SQL injection not blocked! Got result: {result}. " \
        "The query should treat the entire string as a username and find nothing."

def test_blocks_sql_injection_comment():
    """Should block SQL injection with comment."""
    # This injection uses -- to comment out the rest of the query
    result = db.get_user("admin' --")
    
    assert result is None, \
        f"SQL injection with comment not blocked! Got result: {result}"

def test_blocks_sql_injection_union():
    """Should block SQL injection with UNION."""
    # This injection tries to union with another query
    result = db.get_user("' UNION SELECT 1,2,3,4 --")
    
    assert result is None, \
        f"SQL injection with UNION not blocked! Got result: {result}"

def test_special_characters_in_username():
    """Should handle usernames with special characters safely."""
    # Test various special characters that might break the query
    special_usernames = [
        "user'name",
        "user\"name",
        "user;DROP TABLE users--",
        "user\\name",
    ]
    
    for username in special_usernames:
        try:
            result = db.get_user(username)
            # Should return None (not found) without crashing
            assert result is None, \
                f"Username '{username}' should return None, got {result}"
        except Exception as e:
            raise AssertionError(
                f"Query crashed with username '{username}': {e}. "
                "Parameterized queries should handle special characters safely."
            )

def test_case_sensitive_username():
    """Usernames should be case-sensitive."""
    result_lower = db.get_user("alice")
    result_upper = db.get_user("ALICE")
    
    assert result_lower is not None, "get_user('alice') should return data"
    assert result_upper is None, "get_user('ALICE') should return None (case-sensitive)"

def test_empty_string_username():
    """Should handle empty string username."""
    result = db.get_user("")
    assert result is None, "Empty string username should return None"

def test_whitespace_username():
    """Should handle whitespace in username."""
    result = db.get_user("   ")
    assert result is None, "Whitespace username should return None"

def test_very_long_username():
    """Should handle very long username without crashing."""
    long_username = "a" * 10000
    
    try:
        result = db.get_user(long_username)
        assert result is None, "Very long username should return None"
    except Exception as e:
        raise AssertionError(f"Query crashed with long username: {e}")