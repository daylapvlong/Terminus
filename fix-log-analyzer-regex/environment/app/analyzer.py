#!/usr/bin/env python3
"""Log analyzer for counting errors."""

import re
from pathlib import Path

LOG_FILE = Path("/data/app.log")
OUTPUT_FILE = Path("/output/error_count.txt")

def count_errors(log_file):
    """Count ERROR lines in log file."""
    count = 0
    
    # BUG: Old format was "ERROR:", new format is "[ERROR]"
    pattern = r'ERROR:'
    
    with open(log_file) as f:
        for line in f:
            if re.search(pattern, line):
                count += 1
    
    return count

def main():
    """Main function."""
    error_count = count_errors(LOG_FILE)
    
    # Write result
    with open(OUTPUT_FILE, 'w') as f:
        f.write(str(error_count))
    
    print(f"Found {error_count} errors")

if __name__ == "__main__":
    main()