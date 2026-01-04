# Fix Log Analysis Regex Pattern

Your task is to fix the log analyzer that fails to count errors in the new log format.

## Problem

The application parses log files to count ERROR entries. The original log format used `ERROR:` as the error marker, but the new format uses `[ERROR]` with square brackets. The current regex pattern doesn't match this new format, resulting in zero errors being counted.

## Current Behavior

- **Old format (working)**: `ERROR: Database connection failed`
- **New format (broken)**: `[ERROR] Database connection failed`
- **Current regex**: `ERROR:` - only matches old format

## Requirements

1. Fix the regex pattern in `/app/analyzer.py` to match the new format `[ERROR]`
2. The function should correctly count lines containing `[ERROR]`
3. Do not change the function signature or output format
4. Do not modify any other files

## Files to Modify

- **Input**: `/app/analyzer.py`
- **Test data**: `/data/app.log` (contains new format logs)

## Expected Behavior

After the fix:
- Count all lines containing `[ERROR]` markers
- Ignore `[INFO]`, `[WARN]`, `[DEBUG]` lines
- Return the count as an integer
- Write result to `/output/error_count.txt`

## Example

Given log file:
[INFO] Application started
[ERROR] Database connection failed
[WARN] Slow query detected
[ERROR] Timeout occurred
[DEBUG] Processing request

Expected output: `2` (two ERROR lines)

## Testing

The fix is correct when:
1. Script runs without errors
2. Correctly counts ERROR entries in new format
3. Output file contains the right count
4. Does not count WARN, INFO, or DEBUG lines