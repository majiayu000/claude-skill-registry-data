---
name: skill-with-scripts
description: A template for skills that include executable code for deterministic operations.
version: 1.0.0
dependencies:
  - python>=3.8
---

# Skill With Scripts

## Overview

This template demonstrates how to create a skill that includes executable scripts for operations that benefit from deterministic code execution rather than token generation.

## Instructions

When the user requests [specific task]:

1. Analyze the request to determine required parameters
2. Execute the appropriate script from the `scripts/` directory
3. Process and format the results
4. Present the output to the user

## Available Scripts

### `scripts/process_data.py`

Use this script when the user needs to process structured data.

```bash
python scripts/process_data.py --input <file> --output <format>
```

### `scripts/validate.py`

Use this script to validate user input before processing.

```bash
python scripts/validate.py --check <type> --data <input>
```

## Examples

### Example: Data Processing

**User Request:**
"Process the CSV file and generate a summary"

**Steps:**
1. Validate the input file exists
2. Run `process_data.py` with appropriate flags
3. Format and present results

## Guidelines

- Always validate input before processing
- Handle errors gracefully and inform the user
- Use scripts for deterministic operations
- Generate responses for creative/analytical tasks
