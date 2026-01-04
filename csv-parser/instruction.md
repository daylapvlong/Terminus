# Fix CSV Parser Delimiter Bug

Your task is to fix a bug in the CSV parser at `/app/parser.py` that causes incorrect data parsing due to using the wrong delimiter.

## Problem

The application processes sales data from `/data/sales.csv`, but the current implementation uses comma (`,`) as the delimiter when the file actually uses semicolon (`;`). This causes all rows to be read as single columns instead of properly separated fields.

## Requirements

1. Modify `/app/parser.py` to use the correct delimiter (`;`)
2. The parser should correctly read all 3 columns: `id`, `product`, `amount`
3. Output the parsed data to `/output/parsed.json`
4. Do not change the output JSON format
5. Do not modify any other files

## Input File

The CSV file at `/data/sales.csv` has this format:
```
id;product;amount
1;Laptop;999.99
2;Mouse;29.99
3;Keyboard;79.99
```

## Expected Output

The JSON file at `/output/parsed.json` should contain:
```json
[
  {"id": "1", "product": "Laptop", "amount": "999.99"},
  {"id": "2", "product": "Mouse", "amount": "29.99"},
  {"id": "3", "product": "Keyboard", "amount": "79.99"}
]
```

## Files to Modify

- Input: `/app/parser.py`
- Output: `/output/parsed.json` (automatically generated after fix)

## Testing

Run the parser with:
```bash
python /app/parser.py
```

The fix is correct when all test cases pass.