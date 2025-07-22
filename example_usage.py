#!/usr/bin/env python3
"""
Example usage of the Data Structure Processor

This script demonstrates how to use the data processor programmatically
for different use cases.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path so we can import the processor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from combined_data_processor import extract_rawstring_data, process_rawstring_file

def example_workflow():
    """Demonstrate a complete workflow from extraction to analysis."""
    
    print("Data Structure Processor - Example Workflow")
    print("=" * 50)
    
    # Example input file (you would replace this with your actual file)
    input_file = "../test copy.txt"
    
    if not os.path.exists(input_file):
        print(f"Example file not found: {input_file}")
        print("Please ensure the example file exists or update the path.")
        return
    
    print(f"Processing file: {input_file}")
    print()
    
    # Step 1: Extract rawstring data
    print("Step 1: Extracting rawstring data...")
    extract_stats = extract_rawstring_data(input_file)
    
    if 'error' in extract_stats:
        print(f"Error during extraction: {extract_stats['error']}")
        return
    
    print(f"Extracted {extract_stats['valid_rawstrings']} rawstrings from {extract_stats['total_entries']} entries")
    print(f"Output saved to: {extract_stats['output_file']}")
    print()
    
    # Step 2: Create structure analysis
    print("Step 2: Creating structure analysis...")
    structure_stats = process_rawstring_file(extract_stats['output_file'], mode='structure')
    
    if 'error' in structure_stats:
        print(f"Error during structure analysis: {structure_stats['error']}")
        return
    
    print(f"Processed {structure_stats['processed_lines']} lines")
    print(f"Field breakdown:")
    print(f"  - String fields: {structure_stats['string_fields']}")
    print(f"  - Number fields: {structure_stats['number_fields']}")
    print(f"  - Boolean fields: {structure_stats['boolean_fields']}")
    print(f"  - Null fields: {structure_stats['null_fields']}")
    print(f"Output saved to: {structure_stats['output_file']}")
    print()
    
    # Step 3: Scrub sensitive data
    print("Step 3: Scrubbing sensitive data...")
    scrub_stats = process_rawstring_file(extract_stats['output_file'], mode='scrub', preserve_ids=True)
    
    if 'error' in scrub_stats:
        print(f"Error during scrubbing: {scrub_stats['error']}")
        return
    
    print(f"Processed {scrub_stats['processed_lines']} lines")
    print(f"Output saved to: {scrub_stats['output_file']}")
    print()
    
    print("Workflow complete!")
    print("Generated files:")
    print(f"  - Raw data: {extract_stats['output_file']}")
    print(f"  - Structure analysis: {structure_stats['output_file']}")
    print(f"  - Scrubbed data: {scrub_stats['output_file']}")

def example_programmatic_usage():
    """Demonstrate programmatic usage of the processor."""
    
    print("Programmatic Usage Example")
    print("=" * 30)
    
    # Example JSON data
    sample_data = [
        {"_count": "1", "@rawstring": '{"name": "John Doe", "email": "john@example.com", "id": 123}'},
        {"_count": "2", "@rawstring": '{"name": "Jane Smith", "email": "jane@company.org", "id": 456}'}
    ]
    
    # Create temporary file
    temp_input = "temp_sample.json"
    with open(temp_input, 'w') as f:
        import json
        json.dump(sample_data, f)
    
    try:
        # Extract rawstring data
        print("Extracting rawstring data...")
        extract_stats = extract_rawstring_data(temp_input)
        print(f"Extracted {extract_stats['valid_rawstrings']} rawstrings")
        
        # Scrub the data
        print("Scrubbing sensitive data...")
        scrub_stats = process_rawstring_file(extract_stats['output_file'], mode='scrub')
        print(f"Scrubbed {scrub_stats['processed_lines']} lines")
        
        # Create structure analysis
        print("Creating structure analysis...")
        structure_stats = process_rawstring_file(extract_stats['output_file'], mode='structure')
        print(f"Analyzed structure with {structure_stats['string_fields']} string fields")
        
    finally:
        # Clean up temporary files
        for file in [temp_input, extract_stats['output_file'], scrub_stats['output_file'], structure_stats['output_file']]:
            if os.path.exists(file):
                os.remove(file)
    
    print("Programmatic example complete!")

if __name__ == "__main__":
    print("Data Structure Processor Examples")
    print("=" * 40)
    print()
    
    # Run the workflow example
    example_workflow()
    print()
    
    # Run the programmatic example
    example_programmatic_usage() 