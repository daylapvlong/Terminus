#!/bin/bash
set -euo pipefail

cd /app

# Fix the regex pattern to match new format
sed -i "s/pattern = r'ERROR:'/pattern = r'\[ERROR\]'/" analyzer.py