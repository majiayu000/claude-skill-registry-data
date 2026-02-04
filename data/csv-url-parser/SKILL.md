---
name: csv-url-parser
description: Parse URLs in CSV files and extract query parameters as new columns. Use when working with CSV files containing URLs that need parameter extraction and analysis.
allowed-tools: Read, Write, Bash, Glob
---

# CSV URL Parser

This skill extracts query parameters from URLs in CSV files and adds them as new columns.

## Instructions

1. **Identify CSV files**: Look for CSV files in the current directory or specified path
2. **Analyze URL column**: Find the column containing URLs (looks for 'url' or 'URL' headers)
3. **Extract parameters**: Parse all query parameters from URLs
4. **Create new columns**: Add parameter names as new column headers
5. **Process data**: Fill new columns with parameter values (multiple values joined with '|')
6. **Save results**: Update the CSV file with new columns

## Implementation

The skill uses Ruby to process CSV files. Run the processing script:

```bash
ruby scripts/process_csv.rb [file1.csv file2.csv ...]
```

If no files are specified, it processes all CSV files in the current directory.

The script will:

- Read CSV files with headers
- Extract query parameters from URLs using URI parsing
- Handle multiple values for the same parameter (joined with '|')
- Preserve original data while adding new parameter columns
- Handle malformed URLs gracefully

For detailed examples, see [EXAMPLES.md](EXAMPLES.md).

## Usage Examples

**Process all CSV files in current directory:**
```
Parse URLs in my CSV files
```

**Process specific CSV file:**
```
Extract URL parameters from data.csv
```

**Analyze URL parameters:**
```
Show me what parameters are in the URLs from this CSV
```

## Requirements

- Ruby with standard libraries (CSV, URI, CGI)
- CSV files must have headers
- URL column should be named 'url' or 'URL'

## Output

- Original CSV file updated with new parameter columns
- Multiple parameter values separated by '|'
- Preserves all original data
- Handles empty/missing parameters gracefully
