# Fix XML to JSON Nested Elements

Your task is to fix the XML to JSON converter that fails to handle nested elements correctly.

## Problem

The converter currently only processes top-level XML elements and ignores nested child elements. When converting XML with nested structure, all child data is lost.

## Current Behavior

Given XML:
```xml
<user>
    <name>Alice</name>
    <address>
        <city>New York</city>
        <country>USA</country>
    </address>
</user>
```

Current output (broken):
```json
{
  "name": "Alice",
  "address": ""
}
```

Expected output (correct):
```json
{
  "name": "Alice",
  "address": {
    "city": "New York",
    "country": "USA"
  }
}
```

## Requirements

1. Fix `/app/converter.py` to handle nested XML elements recursively
2. Preserve the complete nested structure in JSON output
3. Output to `/output/output.json`
4. Do not modify the function signature

## Files to Modify

- **Input**: `/app/converter.py`
- **Test data**: `/data/input.xml`

## Expected Behavior

After the fix:
- All nested elements are converted to nested JSON objects
- Text content is preserved correctly
- Empty elements become empty strings or objects
- Output is valid JSON

## Testing

The fix is correct when:
1. Converter runs without errors
2. Output JSON contains all nested data
3. Structure matches XML hierarchy
4. No data is lost in conversion