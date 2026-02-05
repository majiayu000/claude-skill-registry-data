---
name: fuel-bill-processor
description: Process aviation fuel surcharge bills from Excel files. Supports both automatic detection and Claude-assisted modes. Detects headers, matches columns, parses dates/routes, and fetches contract numbers via API. Use when working with aviation fuel bills, Excel file processing, or when user mentions fuel surcharges,航空燃油账单, or 燃油差价费.
---

# Fuel Bill Processor

Process aviation fuel surcharge bills from Excel files with automatic format detection or Claude-assisted mode.

## Processing Workflow

### Step 1: Try Automatic Mode First

Always try automatic mode first:
```bash
python3 scripts/process.py input_file.xls [-o output.xlsx]
```

### Step 2: Claude-Assisted Mode (Only if Step 1 Fails)

Use when auto mode fails (header beyond row 15, non-standard columns, complex structure).

1. Analyze structure:
   ```bash
   python3 scripts/analyze.py input_file.xls
   ```

2. Execute suggested command:
   ```bash
   python3 scripts/process.py input_file.xls \
     --header-row 2 --date-column B --route-column C \
     --flight-column D --price-column E
   ```

Parameters: `--header-row` (0-based), `--date-column`, `--route-column`, `--flight-column`, `--price-column` (column letters like A/B/C or column names).

### Step 3: Verify Results

Confirm output file created with expected rows and populated fields.

## Configuration

Uses `assets/config.json` (ready out of the box). See [CONFIGURATION.md](references/CONFIGURATION.md) for details.

## Troubleshooting

| Symptom | Solution |
|---------|----------|
| "Column not recognized" warning | Add column name to `column_mappings` in [config.json](assets/config.json) |
| "Date parsing failed" errors | Add format to `date_formats` array in config |
| API timeout or empty response | Check API URL in config, test network connectivity |
| Output file has fewer rows than expected | Input may have invalid/summary rows being filtered |

For complex table issues, run `analyze.py` to diagnose structure.

## References

- [API_REFERENCE.md](references/API_REFERENCE.md) - Detailed API documentation
- [CONFIGURATION.md](references/CONFIGURATION.md) - Complete configuration guide
