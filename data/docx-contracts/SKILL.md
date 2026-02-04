---
name: docx-contracts
description: Fill Word document templates (contracts, forms) with structured data using docxtpl. Use when user uploads a .docx template with {{variables}} and provides data to fill it, or requests contract/form generation from template.
---

# docx-contracts

Automated contract and form filling using docxtpl library.

## Workflow

Be shure, that you recieve docx file. Don't try to read it.

1. **Extract schema**: Run `scripts/extract_schema.py <template.docx>` to get variables list and JSON schema. Don't read file. Just launch script.
2. **Gather data**: Extract values from user message context, matching schema fields. Use Claude completion for extraction if needed
3. **Handle missing data**: If any required field is missing or uncertain, ask user directly. Do not guess
4. **Fill template**: Create JSON file with data, then run `scripts/fill_template.py <template.docx> <data.json> <output.docx>`
5. **Deliver**: Move result to `/mnt/user-data/outputs/` and provide download link. Please don't read output file.

## Key Points

- Template must use Jinja2 syntax: `{{VARIABLE_NAME}}`
- All required fields from schema must be filled
- Ask user for missing data - never invent values
- Install docxtpl if needed: `pip install docxtpl --break-system-packages`
