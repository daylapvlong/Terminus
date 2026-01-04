#!/bin/bash
set -euo pipefail

cd /environment

# Fix the EXPOSE directive to match the application port
sed -i 's/EXPOSE 8080/EXPOSE 5000/' Dockerfile