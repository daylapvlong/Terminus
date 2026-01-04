#!/bin/bash
set -e

# #region agent log
log_debug() {
  echo "{\"timestamp\":$(date +%s%3N),\"location\":\"test.sh:$1\",\"message\":\"$2\",\"data\":$3,\"sessionId\":\"debug-session\",\"runId\":\"run1\",\"hypothesisId\":\"A\"}" >&2
}
# #endregion

log_debug "$$" "Script started" "{\"PWD\":\"$PWD\"}"

# Create directories
mkdir -p /data /output
log_debug "$$" "Created directories" "{\"dirs\":[\"/data\",\"/output\"]}"

# #region agent log
log_debug "$$" "Checking source file" "{\"source\":\"/tests/data/app.log\"}"
if [ -d "/tests" ]; then
  log_debug "$$" "/tests exists" "{\"contents\":\"$(ls -la /tests 2>&1 | head -5 || echo 'error')\"}"
fi
if [ -d "/tests/data" ]; then
  log_debug "$$" "/tests/data exists" "{\"contents\":\"$(ls -la /tests/data 2>&1 || echo 'error')\"}"
else
  log_debug "$$" "/tests/data missing" "{}"
fi
if [ -f "/tests/data/app.log" ]; then
  log_debug "$$" "Source file exists" "{\"size\":\"$(stat -c%s /tests/data/app.log 2>&1 || echo 'error')\"}"
else
  log_debug "$$" "Source file missing" "{}"
fi
# #endregion

# Copy test data
cp /tests/data/app.log /data/app.log
log_debug "$$" "Copied file" "{\"source\":\"/tests/data/app.log\",\"dest\":\"/data/app.log\"}"

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