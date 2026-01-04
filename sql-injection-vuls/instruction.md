# Fix SQL Injection Vulnerability


## Background
The application queries user data from a SQLite database. The current implementation is vulnerable to SQL injection because it uses string formatting to build SQL queries.


## Your Task
Fix the SQL injection vulnerability in the function `get_user` located in `app/db.py`.


## Requirements
- Use **parameterized queries** instead of string formatting
- The function must continue to work for valid usernames
- SQL injection attempts must not return unintended data
- The application must not crash on special characters

## Problem
The current implementation uses string formatting to build SQL queries, which allows attackers to inject malicious SQL code. This can lead to unauthorized data access or database manipulation.

## Vulnerability Example
Current code:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

An attacker can input: `' OR '1'='1` to bypass authentication and access all user records.

## Requirements
1. Fix the SQL injection vulnerability in `/app/db.py`
2. Use parameterized queries instead of string formatting
3. The `get_user(username)` function should:
   - Return user data for valid usernames
   - Return `None` for non-existent users
   - Block SQL injection attempts (return `None` instead of exposing data)
4. Do not modify the function signature or return format
5. Do not modify any other files

## Files to Modify
- Input: `/app/db.py`
- Database: `/data/users.db` (pre-populated with test data)

## Testing
Test the fix with:
```bash
python /app/db.py
```

The fix is correct when:
- Normal queries work: `get_user("alice")` returns user data
- Injection attempts are blocked: `get_user("' OR '1'='1")` returns `None`
- No syntax errors occur

## Security Note
SQL injection is one of the most critical web application vulnerabilities (OWASP Top 10). Always use parameterized queries to prevent this type of attack.
Current code:
```python
An attacker can input: `' OR '1'='1` to bypass authentication and access all user records.

## Requirements

1. Fix the SQL injection vulnerability in `/app/db.py`
2. Use parameterized queries instead of string formatting
3. The `get_user(username)` function should:
   - Return user data for valid usernames
   - Return `None` for non-existent users
   - Block SQL injection attempts (return `None` instead of exposing data)
4. Do not modify the function signature or return format
5. Do not modify any other files

## Files to Modify

- Input: `/app/db.py`
- Database: `/data/users.db` (pre-populated with test data)

## Testing

Test the fix with:
```bash