---
name: literature-export
description: Export existing PDF, Zotero, or WoS records to Excel and CSV while preserving sources, evidence scope, and missing values.
---

# Literature Table Export

Read [shared contract](../../references/shared-contract.md). Use the spreadsheet skill when generating workbooks.

Use prepare_export.py --input STRUCTURED_JSON_OR_WOS_DIRECTORY --output OUTPUT to normalize records into tables.json and CSV files. Supported inputs are library.json, screening-records.json and a WoS analysis directory. Preserve evidence scope and null values; do not write summaries for records only screened by title.

Run `node export_tables.mjs OUTPUT NODE_RUNTIME_DIRECTORY` for XLSX when @oai/artifact-tool is available. Inspect every sheet preview and verify row counts. Otherwise deliver CSV and explain XLSX was not produced. Keep all document records; a selected-reference sheet must state that it contains only the network selection, with full references retained in the WoS CSV/JSON.

If no structured input exists, route first to the appropriate PDF, Zotero or WoS module. Exporting all records does not mean all documents have been read in full.
