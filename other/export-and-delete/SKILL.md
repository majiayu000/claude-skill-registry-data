---
name: export-and-delete
description: >
    How to export data and delete tables or objects using the Frontline CLI.
    Use when you need to download records as XLSX/CSV files or permanently
    remove a table or object and all its data.
allowed-tools: Bash(frontline:*)
---

# Export & Delete Operations

## Exporting Data

Export records from a table or object as an XLSX spreadsheet or CSV file.
Exports support the same query/search/sort filters used for listing.

### Export as XLSX

```bash
frontline table export xlsx <name> [--output file.xlsx]
frontline object export xlsx <name> [--output file.xlsx]
```

```bash
# Export all people
frontline object export xlsx people

# Export with filter (high-value deals only)
frontline object export xlsx deals \
  --query '{"path": "[Amount]", "operator": "gte", "value": 10000}' \
  --output big_deals.xlsx

# Export with search + sort
frontline table export xlsx sales_data \
  --search "enterprise" \
  --sort '[{"path": "[Revenue]", "type": "desc"}]' \
  --output enterprise_sales.xlsx
```

### Export as CSV

```bash
frontline table export csv <name> [--output file.csv]
frontline object export csv <name> [--output file.csv]
```

```bash
# Export all records as CSV
frontline object export csv people --output people_backup.csv
```

### Default Output

If `--output` is not specified:

- XLSX: `./<name>_export.xlsx`
- CSV: `./<name>_export.csv`

## Deleting Tables/Objects

> [!CAUTION]
> These operations are **destructive and irreversible**. All rows, fields,
> views, record types, and associated data will be permanently deleted.

### Delete a Table

```bash
frontline table delete <name>
```

### Delete an Object

```bash
frontline object delete <name>
```

### Response

```json
{ "deleted": true, "name": "my_table" }
```

## Workflow: Backup Then Delete

Always export before deleting:

```bash
# 1. Export everything
frontline object export xlsx legacy_deals --output legacy_deals_backup.xlsx

# 2. Verify the export file exists and looks right
ls -la legacy_deals_backup.xlsx

# 3. Delete the object
frontline object delete legacy_deals
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
