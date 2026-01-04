#!/bin/bash
set -e

# Create directories
mkdir -p /data /output

# Copy test data
cp /tests/data/app.log /data/app.log

# Install uv
curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh
source $HOME/.local/bin/env

# Check working directory
if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set."
    exit 1
fi

# Run pytest
uvx \
  -p 3.13 \
  -w pytest==8.4.1 \
  -w pytest-json-ctrf==0.3.5 \
  pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA

PYTEST_EXIT=$?

# Create reward file
if [ $PYTEST_EXIT -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit $PYTEST_EXIT
```

---

## 📄 `tests/data/app.log`
```
[INFO] Application started successfully
[INFO] Loading configuration from /etc/app/config.json
[ERROR] Database connection failed: timeout after 30s
[WARN] Slow query detected: SELECT took 5.2s
[INFO] Processing user request from 192.168.1.100
[ERROR] Failed to write to cache: Redis connection refused
[DEBUG] Cache miss for key: user_session_12345
[INFO] Request completed in 250ms
[ERROR] Unable to send notification: SMTP server unavailable
[WARN] Memory usage at 85%
[INFO] Background job started: cleanup_old_sessions
[ERROR] Task failed: InvalidArgumentException in process_payment
[DEBUG] Logging level set to INFO
[INFO] Shutting down gracefully