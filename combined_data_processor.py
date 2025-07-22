#!/usr/bin/env python3
"""
Data Structure Processor - Extract and analyze JSON data structures.

This script provides functionality for:
1. Extracting @rawstring data from JSON arrays
2. Scrubbing sensitive data while preserving structure
3. Providing comprehensive data structure analysis

Perfect for processing and analyzing JSON data structures for documentation and analysis.
"""

import json
import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Union
import hashlib
import argparse

class DataProcessor:
    """Comprehensive data processor for JSON structure analysis."""
    
    def __init__(self, preserve_ids: bool = False, preserve_lengths: bool = True):
        """
        Initialize the data processor.
        
        Args:
            preserve_ids (bool): Whether to preserve ID fields (with hashing)
            preserve_lengths (bool): Whether to preserve string lengths
        """
        self.preserve_ids = preserve_ids
        self.preserve_lengths = preserve_lengths
        self.id_mapping = {}
        self.string_counter = 0
        self.number_counter = 0
        self.boolean_counter = 0
        self.null_counter = 0
        
    def _hash_id(self, value: str) -> str:
        """Hash an ID value for consistent anonymization."""
        if value not in self.id_mapping:
            self.id_mapping[value] = f"ID_{len(self.id_mapping) + 1}"
        return self.id_mapping[value]
    
    def _get_placeholder(self, value: Any) -> str:
        """Get a placeholder based on data type."""
        if value is None:
            self.null_counter += 1
            return "[NULL]"
        elif isinstance(value, bool):
            self.boolean_counter += 1
            return "[BOOLEAN]"
        elif isinstance(value, (int, float)):
            self.number_counter += 1
            return "[NUMBER]"
        elif isinstance(value, str):
            self.string_counter += 1
            return "[STRING]"
        elif isinstance(value, list):
            return "[]" if not value else "[ARRAY]"
        elif isinstance(value, dict):
            return "{}" if not value else "[OBJECT]"
        else:
            return "[UNKNOWN]"
    
    def _scrub_value(self, value: Any) -> Any:
        """Scrub a single value while preserving type information."""
        if value is None:
            return None
        elif isinstance(value, bool):
            return value  # Keep boolean values as they are structural
        elif isinstance(value, (int, float)):
            return 0  # Replace numbers with 0
        elif isinstance(value, str):
            # Check for specific patterns
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                return "user@example.com"
            elif re.match(r'^https?://', value):
                return "https://example.com"
            elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
                return "192.168.1.1"
            elif re.match(r'^\d{3}-\d{3}-\d{4}$', value):
                return "555-000-0000"
            elif self.preserve_ids and any(keyword in value.lower() for keyword in ['id', 'uuid', 'guid']):
                return self._hash_id(value)
            else:
                if self.preserve_lengths:
                    return 'X' * len(value)
                else:
                    return "[STRING]"
        elif isinstance(value, list):
            return [self._scrub_value(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._scrub_value(val) for key, val in value.items()}
        else:
            return value
    
    def _structure_scrub(self, value: Any) -> Any:
        """Replace values with type placeholders for structure analysis."""
        if value is None:
            return "[NULL]"
        elif isinstance(value, bool):
            return "[BOOLEAN]"
        elif isinstance(value, (int, float)):
            return "[NUMBER]"
        elif isinstance(value, str):
            return "[STRING]"
        elif isinstance(value, list):
            if not value:
                return "[]"
            return [self._structure_scrub(item) for item in value]
        elif isinstance(value, dict):
            if not value:
                return "{}"
            return {key: self._structure_scrub(val) for key, val in value.items()}
        else:
            return "[UNKNOWN]"

def extract_rawstring_data(input_file: str, output_file: str = None) -> Dict[str, Any]:
    """
    Extract only the @rawstring values from the JSON array in the input file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output file (optional)
    
    Returns:
        Dict containing processing statistics
    """
    
    # Set default output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_rawstring_only{input_path.suffix}"
    
    try:
        # Read and parse the JSON array
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Input file must contain a JSON array")
        
        # Extract rawstring values
        rawstrings = []
        for item in data:
            if isinstance(item, dict) and '@rawstring' in item:
                rawstring = item['@rawstring']
                if rawstring and rawstring.strip():
                    rawstrings.append(rawstring)
        
        # Write extracted rawstrings to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for rawstring in rawstrings:
                f.write(rawstring + '\n')
        
        # Prepare statistics
        stats = {
            'total_entries': len(data),
            'valid_rawstrings': len(rawstrings),
            'output_file': str(output_file),
            'sample_preview': rawstrings[:3] if rawstrings else []
        }
        
        return stats
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {'error': str(e)}

def process_rawstring_file(input_file: str, output_file: str = None, mode: str = 'scrub', 
                         preserve_ids: bool = False) -> Dict[str, Any]:
    """
    Process rawstring data with specified mode.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output file (optional)
        mode (str): Processing mode ('scrub' or 'structure')
        preserve_ids (bool): Whether to preserve ID fields
    
    Returns:
        Dict containing processing statistics
    """
    
    # Set default output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        suffix = "_scrubbed" if mode == 'scrub' else "_structure_only"
        output_file = input_path.parent / f"{input_path.stem}{suffix}{input_path.suffix}"
    
    processor = DataProcessor(preserve_ids=preserve_ids)
    
    try:
        processed_lines = []
        total_lines = 0
        
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                total_lines += 1
                
                try:
                    # Parse the JSON rawstring
                    data = json.loads(line)
                    
                    # Process based on mode
                    if mode == 'scrub':
                        processed_data = processor._scrub_value(data)
                    elif mode == 'structure':
                        processed_data = processor._structure_scrub(data)
                    else:
                        raise ValueError(f"Unknown mode: {mode}")
                    
                    # Write processed data
                    processed_lines.append(json.dumps(processed_data, indent=2))
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON on line {line_num}: {e}")
                    continue
        
        # Write processed data to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for processed_line in processed_lines:
                f.write(processed_line + '\n')
        
        # Prepare statistics
        stats = {
            'total_lines': total_lines,
            'processed_lines': len(processed_lines),
            'output_file': str(output_file),
            'mode': mode,
            'string_fields': processor.string_counter,
            'number_fields': processor.number_counter,
            'boolean_fields': processor.boolean_counter,
            'null_fields': processor.null_counter,
            'sample_preview': processed_lines[:2] if processed_lines else []
        }
        
        return stats
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {'error': str(e)}

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Data Structure Processor - Extract and analyze JSON data structures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s extract input.json
  %(prog)s scrub rawstrings.txt --preserve-ids
  %(prog)s structure rawstrings.txt
        """
    )
    
    parser.add_argument('mode', choices=['extract', 'scrub', 'structure'],
                       help='Processing mode')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('--preserve-ids', action='store_true',
                       help='Preserve ID fields with consistent hashing (scrub mode only)')
    parser.add_argument('--rawstring', action='store_true',
                       help='Process each line as a JSON rawstring (scrub/structure modes only)')
    
    args = parser.parse_args()
    
    if args.mode == 'extract':
        stats = extract_rawstring_data(args.input_file, args.output)
    else:
        if args.rawstring:
            # Process as rawstring file
            stats = process_rawstring_file(args.input_file, args.output, args.mode, args.preserve_ids)
        else:
            # Process as regular JSON file
            stats = process_rawstring_file(args.input_file, args.output, args.mode, args.preserve_ids)
    
    # Print results
    if 'error' in stats:
        print(f"Error: {stats['error']}")
        sys.exit(1)
    
    print(f"Processing complete!")
    print(f"Output file: {stats['output_file']}")
    
    if args.mode == 'extract':
        print(f"Total entries: {stats['total_entries']}")
        print(f"Valid rawstrings: {stats['valid_rawstrings']}")
    else:
        print(f"Total lines processed: {stats['processed_lines']}")
        print(f"String fields: {stats['string_fields']}")
        print(f"Number fields: {stats['number_fields']}")
        print(f"Boolean fields: {stats['boolean_fields']}")
        print(f"Null fields: {stats['null_fields']}")
    
    if stats.get('sample_preview'):
        print(f"\nSample preview:")
        for i, sample in enumerate(stats['sample_preview'][:2], 1):
            print(f"  {i}. {sample[:100]}{'...' if len(sample) > 100 else ''}")

if __name__ == "__main__":
    main() 