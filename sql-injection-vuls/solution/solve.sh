#!/bin/bash
set -euo pipefail

cd /app

# Fix 1: Change query to use parameterized placeholder
sed -i "s/query = f\"SELECT \* FROM users WHERE username = '{username}'\"/query = \"SELECT * FROM users WHERE username = ?\"/" db.py

# Fix 2: Update execute call to use parameters
sed -i 's/cursor\.execute(query)/cursor.execute(query, (username,))/' db.py