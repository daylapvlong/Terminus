#!/usr/bin/env python3
"""Test suite for CSV parser delimiter fix."""

import json
import subprocess
from pathlib import Path

APP_DIR = "/app"
OUTPUT_FILE = Path("/output/parsed.json")
INPUT_FILE = Path("/data/sales.csv")

def cleanup():
    """Remove output file before each test."""
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

def run_parser():
    """Run the CSV parser."""
    result = subprocess.run(
        ["python", "parser.py"],
        cwd=APP_DIR,
        capture_output=True,
        text=True
    )
    return result

def test_parser_runs_successfully():
    """Parser should run without errors."""
    cleanup()
    result = run_parser()
    assert result.returncode == 0, f"Parser failed with error: {result.stderr}"

def test_output_file_created():
    """Parser should create output JSON file."""
    cleanup()
    run_parser()
    assert OUTPUT_FILE.exists(), "Output file /output/parsed.json not created"

def test_output_is_valid_json():
    """Output file should contain valid JSON."""
    cleanup()
    run_parser()
    
    try:
        with open(OUTPUT_FILE, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Output is not valid JSON: {e}")

def test_correct_number_of_rows():
    """Parser should read exactly 3 data rows."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, list), "Output should be a JSON array"
    assert len(data) == 3, f"Expected 3 rows, got {len(data)}"

def test_correct_column_names():
    """Each row should have id, product, and amount fields."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    expected_keys = {"id", "product", "amount"}
    
    for i, row in enumerate(data):
        actual_keys = set(row.keys())
        assert actual_keys == expected_keys, \
            f"Row {i} has wrong keys. Expected {expected_keys}, got {actual_keys}"

def test_first_row_data():
    """First row should contain correct laptop data."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    first_row = data[0]
    assert first_row["id"] == "1", f"Expected id='1', got '{first_row['id']}'"
    assert first_row["product"] == "Laptop", f"Expected product='Laptop', got '{first_row['product']}'"
    assert first_row["amount"] == "999.99", f"Expected amount='999.99', got '{first_row['amount']}'"

def test_all_products_parsed():
    """All three products should be correctly parsed."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    products = [row["product"] for row in data]
    expected_products = ["Laptop", "Mouse", "Keyboard"]
    
    assert products == expected_products, \
        f"Expected products {expected_products}, got {products}"

def test_no_extra_fields():
    """Rows should only contain the three expected fields."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    for i, row in enumerate(data):
        assert len(row) == 3, \
            f"Row {i} should have exactly 3 fields, got {len(row)}: {list(row.keys())}"

def test_amounts_are_strings():
    """Amount values should be preserved as strings."""
    cleanup()
    run_parser()
    
    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
    
    for i, row in enumerate(data):
        assert isinstance(row["amount"], str), \
            f"Row {i} amount should be string, got {type(row['amount'])}"
        assert "." in row["amount"], \
            f"Row {i} amount should contain decimal point"