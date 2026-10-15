---
name: dtsx-workflow-analyzer
description: "Analyze DTSX files (SSIS/KingswaySoft packages) to reverse engineer integration workflows between Dynamics on-premise and cloud. Use when the user uploads DTSX files and wants workflows, data mappings or table relationships documented. Triggers: DTSX, SSIS, KingswaySoft, ETL."
---

# DTSX Workflow Analyzer

Reverse engineer SSIS/KingswaySoft DTSX packages into comprehensive workflow documentation.

## Workflow

### Step 1: Parse DTSX Structure

Run the parser script to extract structured data:

```bash
python scripts/parse_dtsx.py /path/to/file.dtsx
```

This outputs JSON with:
- Package metadata (name, creation date, creator)
- Connection managers (source/destination systems)
- Data flow tasks and components
- Column mappings with lineage
- Transformation logic

### Step 2: Review Parser Output

Examine the JSON output to identify:
- **Source components**: Where data originates (Dynamics CRM Source, OLE DB Source, etc.)
- **Destination components**: Where data lands (Dynamics CRM Destination, etc.)
- **Transformations**: Derived columns, lookups, conditional splits
- **Column mappings**: Source → destination field relationships

### Step 3: Generate Documentation

Create a markdown analysis document using the template from `references/output-template.md`.

Key sections to complete:
1. **Package metadata**: Name, purpose, connections
2. **Table mappings**: Source entity → destination entity with all columns
3. **Transformations**: Any derived columns, lookups, or data modifications
4. **Relationships**: Foreign keys implied by lookups or reference fields
5. **Flow narrative**: Step-by-step description of what happens

### Step 4: Identify Patterns

Document these DTSX-specific patterns:

**KingswaySoft Components**:
- `CrmSourceComponent`: Reads from Dynamics CRM/Dataverse
- `CrmDestinationComponent`: Writes to Dynamics CRM/Dataverse
- ActionType values: 0=Create, 1=Update, 2=Delete, 5=Upsert

**Column Mapping Detection**:
- `cachedName`: Source column name
- `externalMetadataColumnId`: Contains destination column reference
- `lineageId`: Traces back to origin component

**Connection Managers**:
- Look for `connectionManagerRefId` to identify source/destination systems
- Project-level connections in format `Project.ConnectionManagers[name]`

## Output Requirements

Save analysis to `./docs/dtsx-analysis/[PackageName]-Analysis.md` (create directory if needed), or adapt to the project's existing documentation structure.

The document must:
- Use clear section headers
- Include complete column mapping tables
- Document all transformations with logic
- Note any disabled components (check `DTS:Disabled="True"`)
- Identify relationship implications from lookups

## Quick Reference

### Extract Package Name
XPath: `/DTS:Executable/@DTS:ObjectName`

### Find Data Flow Tasks
XPath: `//DTS:Executable[@DTS:CreationName="Microsoft.Pipeline"]`

### Get Column Mappings
Look in: `component/inputs/input/inputColumns/inputColumn`
- `cachedName`: Source field
- Parse `externalMetadataColumnId` for destination field

### Identify Connections
XPath: `//DTS:ConnectionManager` or `component/connections/connection`

## Resources

### scripts/parse_dtsx.py
Python script that parses DTSX XML and extracts structured workflow data as JSON.

### references/output-template.md
Complete markdown template for analysis documentation.
