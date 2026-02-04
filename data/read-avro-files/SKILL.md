---
name: read-avro-files
description: Extracts and displays JSON data from Apache Avro files. Use this when the user wants to read, convert, or view the contents of an .avro file. Automatically deserializes nested JSON fields for better readability.
---

# Read Avro Files

## Overview
This skill helps extract JSON data from Apache Avro files and displays them in a readable format. It handles deserialization of nested byte strings and saves the output to a JSON file.

## When to Use This Skill
- User mentions they have an Avro file (.avro extension)
- User wants to convert Avro to JSON
- User wants to see the contents of an Avro file
- User provides a path to an .avro file

## Workflow

Copy and track progress:

```
Avro Conversion Progress:
- [ ] Step 1: Verify file path or ask user
- [ ] Step 2: Check dependencies (avro-python3)
- [ ] Step 3: Run conversion script
- [ ] Step 4: Verify JSON output created
- [ ] Step 5: Present results to user
```

### Step 1: Verify File Path

If the file path is not provided by the user:
- Use the AskUserQuestion tool to get the Avro file path
- Ask: "Please provide the full path to the Avro file you want to convert"

### Step 2: Check Dependencies

Install dependencies if needed:
```bash
pip install avro-python3
```

Only install if the avro module is not already available.

### Step 3: Run Conversion Script

Run the bundled script (do not read its contents):
```bash
python scripts/read_avro.py "<avro_file_path>"
```

The script will:
- Display each record as formatted JSON
- Deserialize the Body field if it contains nested JSON
- Save the output to a .json file in the same directory

For script implementation details, see [scripts/read_avro.py](scripts/read_avro.py).

### Step 4: Verify JSON Output Created

Check that the output file was created:
- Output file name: same as input but with .json extension
- Location: same directory as the input file

### Step 5: Present Results

Show the user:
- Where the JSON output was saved
- Number of records found
- Key information from the records if relevant

## Expected Output Format

The script produces:
- Console output showing each record with formatted JSON
- A .json file saved in the same directory as the input file
- Record count summary

## Common Use Cases

1. **Event Hub captured data**: Avro files from Azure Event Hub captures containing event metadata and body
2. **Kafka messages**: Avro-serialized Kafka messages
3. **Data pipeline debugging**: Inspecting intermediate Avro files in data processing pipelines
4. **Schema validation**: Viewing actual data structure for schema comparison

## Common Issues

**FileNotFoundError**:
- Verify the path exists
- Use absolute paths instead of relative paths
- Check for typos in the path

**Module not found (avro)**:
- Run: `pip install avro-python3`
- Verify installation: `python -c "import avro"`

**JSON decode error in Body field**:
- The Body field may have unexpected encoding
- Check Event Hub configuration if applicable
- The script will show a warning but continue processing

## Notes

- The script handles nested JSON in byte string format (common in Event Hub captures)
- Dates and complex types are converted to strings in the output
- Large files will show all records in console but save efficiently to JSON
- The bundled script is optimized for reliability and handles edge cases
