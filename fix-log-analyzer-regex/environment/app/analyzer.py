#!/usr/bin/env python3
"""Log analyzer for counting errors."""

import re
import json
from pathlib import Path

LOG_FILE = Path("/data/app.log")
OUTPUT_FILE = Path("/output/error_count.txt")
DEBUG_LOG = Path("/output/debug.log")

# #region agent log
def log_debug(location, message, data):
    """Write debug log entry."""
    try:
        entry = {
            "timestamp": int(__import__("time").time() * 1000),
            "location": f"analyzer.py:{location}",
            "message": message,
            "data": data,
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "B"
        }
        with open(DEBUG_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass
# #endregion

def count_errors(log_file):
    """Count ERROR lines in log file."""
    count = 0
    
    # Fixed: Pattern now matches new format "[ERROR]" instead of old "ERROR:"
    pattern = r'\[ERROR\]'
    
    # #region agent log
    import sys
    print(f"DEBUG: Pattern is: {repr(pattern)}", file=sys.stderr)
    print(f"DEBUG: Log file: {log_file}", file=sys.stderr)
    log_debug(36, "Starting count_errors", {"log_file": str(log_file), "pattern": pattern})
    # #endregion
    
    matched_lines = []
    with open(log_file) as f:
        for line_num, line in enumerate(f, 1):
            line_content = line.strip()
            # #region agent log
            match_result = re.search(pattern, line)
            if match_result:
                count += 1
                matched_lines.append({"line_num": line_num, "content": line_content})
                print(f"DEBUG: Line {line_num} MATCHED: {line_content[:80]}", file=sys.stderr)
                log_debug(45, "Matched line", {"line_num": line_num, "content": line_content[:100], "match": match_result.group()})
            else:
                print(f"DEBUG: Line {line_num} NO MATCH: {line_content[:80]}", file=sys.stderr)
            # #endregion
    
    # #region agent log
    print(f"DEBUG: Total count: {count}", file=sys.stderr)
    log_debug(51, "Finished counting", {"total_count": count, "matched_lines": matched_lines})
    # #endregion
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