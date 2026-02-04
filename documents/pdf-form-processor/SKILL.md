---
name: pdf-form-processor
description: This skill should be used when the user asks to "fill PDF form", "extract PDF fields", "process PDF forms", "analyze PDF structure", or mentions working with fillable PDF documents.
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# PDF Form Processor

Process fillable PDF forms: analyze fields, fill values, validate output.

## Capabilities

- Extract form field information
- Fill form fields programmatically
- Validate field mappings
- Verify output documents

## Quick Start

### Extract Fields

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

### Fill Form

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```

## Workflow

### Step 1: Analyze Form

Run analysis script to extract fields:

```bash
python scripts/analyze_form.py form.pdf
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

### Step 2: Create Field Mapping

Edit `fields.json` to add values:

```json
{
  "field_name": {
    "type": "text",
    "value": "John Doe"
  }
}
```

### Step 3: Validate Mapping

Check for errors before filling:

```bash
python scripts/validate_fields.py fields.json
# Returns: "OK" or lists issues
```

### Step 4: Fill Form

Apply values to PDF:

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```

### Step 5: Verify Output

Check filled document:

```bash
python scripts/verify_output.py output.pdf
```

If verification fails, return to Step 2.

## Progress Tracking

```
Task Progress:
- [ ] Step 1: Analyze form
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

## Requirements

Install dependencies:

```bash
pip install pypdf pdfplumber
```

## Additional Resources

### Reference Files

- **`references/field-types.md`** - Supported field types and properties
- **`references/troubleshooting.md`** - Common issues and solutions

### Scripts

- **`scripts/analyze_form.py`** - Extract form fields
- **`scripts/fill_form.py`** - Apply field values
- **`scripts/validate_fields.py`** - Validate mappings
- **`scripts/verify_output.py`** - Check output document
