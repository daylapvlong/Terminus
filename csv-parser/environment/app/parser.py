#!/usr/bin/env python3
"""CSV parser for sales data."""

import csv
import json
from pathlib import Path

INPUT_FILE = Path("/data/sales.csv")
OUTPUT_FILE = Path("/output/parsed.json")

def parse_csv():
    """Parse CSV file and output JSON."""
    results = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        # BUG: Using wrong delimiter (comma instead of semicolon)
        reader = csv.DictReader(f, delimiter=',')
        
        for row in reader:
            results.append(dict(row))
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Parsed {len(results)} rows")
    return results

if __name__ == "__main__":
    parse_csv()