#!/bin/bash
set -euo pipefail

cd /app

# Fix the delimiter from comma to semicolon
sed -i "s/delimiter=','/delimiter=';'/" parser.py