# Data Structure Processor

A comprehensive tool for processing and analyzing JSON data structures. This tool provides functionality for extracting rawstring data, scrubbing sensitive information, and preserving structure for analysis and documentation purposes.

## Features

### Extract Mode
- Extracts `@rawstring` values from JSON arrays
- Filters out empty or invalid rawstrings
- Provides sample preview of extracted data
- Perfect for processing API responses with embedded JSON data

### Scrub Mode
- Anonymizes sensitive data while preserving structure
- Detects and anonymizes emails, URLs, IPs, phone numbers
- Preserves ID fields with consistent hashing (optional)
- Maintains data relationships and field names

### Structure Mode
- Replaces all data values with type placeholders
- Keeps field names intact for structure analysis
- Provides comprehensive field type statistics
- Perfect for documenting data schemas

## Installation

No external dependencies required! This tool uses only Python standard library modules.

```bash
# Clone or download the data_processor folder
cd data_processor
chmod +x combined_data_processor.py
```

## Usage

### Command Line Interface

```bash
# Extract rawstring data from JSON array
python combined_data_processor.py extract input.json

# Scrub sensitive data from rawstring file
python combined_data_processor.py scrub rawstrings.txt --preserve-ids

# Create structure-only version for analysis
python combined_data_processor.py structure rawstrings.txt

# Process with custom output file
python combined_data_processor.py scrub input.txt -o output.txt
```

### Programmatic Usage

```python
from combined_data_processor import extract_rawstring_data, process_rawstring_file

# Extract rawstring data
stats = extract_rawstring_data("input.json", "output.txt")

# Scrub sensitive data
stats = process_rawstring_file("data.txt", mode="scrub", preserve_ids=True)

# Create structure analysis
stats = process_rawstring_file("data.txt", mode="structure")
```

## Processing Modes

### Extract Mode
Extracts `@rawstring` values from JSON arrays where each element contains:
```json
{
  "_count": "1",
  "@rawstring": "{\"actual\": \"data\"}"
}
```

**Output**: One JSON object per line containing the parsed rawstring data.

### Scrub Mode
Anonymizes sensitive data while preserving structure:
- **Emails**: `user@example.com`
- **URLs**: `https://example.com`
- **IPs**: `192.168.1.1`
- **Phone Numbers**: `555-000-0000`
- **IDs**: Consistent hashing (when `--preserve-ids` is used)
- **General Text**: Replaced with `X` characters to preserve length

### Structure Mode
Replaces all values with type placeholders:
- `[STRING]` for text values
- `[NUMBER]` for numeric values
- `[BOOLEAN]` for true/false values
- `[NULL]` for null values
- `[]` for empty arrays
- `{}` for empty objects

## Command Line Options

### Global Options
- `mode`: Processing mode (`extract`, `scrub`, `structure`)
- `input_file`: Path to input file
- `-o, --output`: Output file path (optional)

### Scrub Mode Options
- `--preserve-ids`: Preserve ID fields with consistent hashing
- `--rawstring`: Process each line as a JSON rawstring

### Structure Mode Options
- `--rawstring`: Process each line as a JSON rawstring

## Output Examples

### Extract Mode Output
```json
{"alert_type": "phishing", "entity": {"name": "example.com"}}
{"alert_type": "malware", "entity": {"name": "test.org"}}
```

### Scrub Mode Output
```json
{
  "alert_type": "phishing",
  "entity": {
    "name": "example.com",
    "email": "user@example.com"
  }
}
```

### Structure Mode Output
```json
{
  "alert_type": "[STRING]",
  "entity": {
    "name": "[STRING]",
    "email": "[STRING]"
  }
}
```

## Statistics and Analysis

The tool provides comprehensive statistics for each processing mode:

### Extract Mode
- Total entries processed
- Valid rawstrings extracted
- Sample preview of extracted data

### Scrub/Structure Mode
- Total lines processed
- Field type breakdown (strings, numbers, booleans, nulls)
- Sample preview of processed data

## Use Cases

### Data Documentation
Use structure mode to create documentation of JSON schemas without exposing sensitive data.

### Data Analysis
Use scrub mode to analyze data patterns while maintaining privacy.

### API Response Processing
Use extract mode to process API responses that contain embedded JSON data.

### Schema Migration
Use structure mode to compare data structures across different versions or systems.

## Error Handling

The tool gracefully handles:
- Invalid JSON input
- Missing files
- Empty or malformed data
- Encoding issues

All errors are reported with clear messages and the tool continues processing valid data.