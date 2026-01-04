#!/usr/bin/env python3
"""Test suite for log analyzer regex fix."""

import subprocess
from pathlib import Path

OUTPUT_FILE = Path("/output/error_count.txt")
LOG_FILE = Path("/data/app.log")

def run_analyzer():
    """Run the log analyzer."""
    result = subprocess.run(
        ["python", "/app/analyzer.py"],
        capture_output=True,
        text=True,
        cwd="/app"
    )
    return result

def test_analyzer_runs_successfully():
    """Analyzer should run without errors."""
    result = run_analyzer()
    assert result.returncode == 0, \
        f"Analyzer failed with error: {result.stderr}"

def test_output_file_created():
    """Analyzer should create output file."""
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    
    run_analyzer()
    assert OUTPUT_FILE.exists(), \
        "Output file /output/error_count.txt not created"

def test_output_is_integer():
    """Output should be a valid integer."""
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    
    run_analyzer()
    
    with open(OUTPUT_FILE) as f:
        content = f.read().strip()
    
    try:
        count = int(content)
    except ValueError:
        raise AssertionError(f"Output is not a valid integer: '{content}'")

def test_correct_error_count():
    """Should count exactly 4 ERROR entries."""
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    
    run_analyzer()
    
    with open(OUTPUT_FILE) as f:
        count = int(f.read().strip())
    
    assert count == 4, \
        f"Expected 4 errors, but got {count}. " \
        "Check that the regex pattern matches '[ERROR]' format."

def test_does_not_count_warnings():
    """Should not count WARN lines as errors."""
    # Count WARN lines in log
    with open(LOG_FILE) as f:
        warn_count = sum(1 for line in f if '[WARN]' in line)
    
    # Run analyzer
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    run_analyzer()
    
    with open(OUTPUT_FILE) as f:
        error_count = int(f.read().strip())
    
    # Error count should not include warnings
    assert error_count != warn_count, \
        "Analyzer is counting WARN lines as errors"

def test_does_not_count_info():
    """Should not count INFO lines as errors."""
    with open(LOG_FILE) as f:
        info_count = sum(1 for line in f if '[INFO]' in line)
    
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    run_analyzer()
    
    with open(OUTPUT_FILE) as f:
        error_count = int(f.read().strip())
    
    assert error_count != info_count, \
        "Analyzer is counting INFO lines as errors"

def test_empty_log_returns_zero():
    """Should return 0 for empty log file."""
    # Create empty log
    empty_log = Path("/data/empty.log")
    empty_log.write_text("")
    
    # Modify analyzer temporarily to use empty log
    result = subprocess.run(
        ["python", "-c", 
         f"import sys; sys.path.insert(0, '/app'); "
         f"from analyzer import count_errors; "
         f"print(count_errors('{empty_log}'))"],
        capture_output=True,
        text=True
    )
    
    count = int(result.stdout.strip())
    assert count == 0, \
        f"Empty log should return 0, got {count}"

def test_only_errors_log():
    """Should count correctly when log has only errors."""
    # Create log with only errors
    errors_only = Path("/data/errors_only.log")
    errors_only.write_text(
        "[ERROR] Error 1\n"
        "[ERROR] Error 2\n"
        "[ERROR] Error 3\n"
    )
    
    result = subprocess.run(
        ["python", "-c", 
         f"import sys; sys.path.insert(0, '/app'); "
         f"from analyzer import count_errors; "
         f"print(count_errors('{errors_only}'))"],
        capture_output=True,
        text=True
    )
    
    count = int(result.stdout.strip())
    assert count == 3, \
        f"Should count 3 errors, got {count}"

def test_mixed_case_not_matched():
    """Should not match if ERROR is in different case."""
    mixed_case = Path("/data/mixed_case.log")
    mixed_case.write_text(
        "[error] lowercase\n"
        "[Error] titlecase\n"
        "[ERROR] correct\n"
    )
    
    result = subprocess.run(
        ["python", "-c", 
         f"import sys; sys.path.insert(0, '/app'); "
         f"from analyzer import count_errors; "
         f"print(count_errors('{mixed_case}'))"],
        capture_output=True,
        text=True
    )
    
    count = int(result.stdout.strip())
    assert count == 1, \
        f"Should only match [ERROR] in uppercase, got {count}"