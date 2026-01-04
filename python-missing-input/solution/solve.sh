#!/bin/bash

# Navigate to the application
cd /app

# Fix the bug by editing the file
sed -i 's/def process(data):/def process(data):\n    if not data:\n        return []/' main.py

# Verify the fix
python -c "from main import process; assert process('') == []"

# Step 4: Any cleanup or final steps
echo "Task completed successfully"