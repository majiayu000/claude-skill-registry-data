---
name: oscal-parser
description: Parse OSCAL (Open Security Controls Assessment Language) documents in JSON, YAML, or XML formats and extract structured compliance data. Use this skill when working with security control catalogs, system security plans, component definitions, or other OSCAL document types.
---

# OSCAL Parser Skill

Parse OSCAL documents in any supported format (JSON, YAML, XML) and extract structured data for compliance analysis.

## When to Use This Skill

Use this skill when you need to:
- Read and parse OSCAL documents from files
- Detect the format and model type of an OSCAL document
- Extract metadata, controls, components, or other OSCAL elements
- Convert OSCAL data into a workable structure for further analysis

---

## ✅ Data Source Principle

This skill operates **only on documents you provide**. It reads and parses — it does not generate compliance data from training knowledge. All output comes directly from your OSCAL document.

---

## Supported Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| JSON | `.json` | Most common format, fastest parsing |
| YAML | `.yaml`, `.yml` | Human-readable, good for editing |
| XML | `.xml` | Legacy format, full schema support |

## OSCAL Model Types

The parser automatically detects these OSCAL model types:
- **Catalog** - Security control catalogs (e.g., NIST 800-53)
- **Profile** - Control baselines and overlays
- **System Security Plan (SSP)** - System security documentation
- **Component Definition** - Reusable component security capabilities
- **Assessment Plan** - Assessment procedures
- **Assessment Results** - Assessment findings
- **Plan of Action and Milestones (POA&M)** - Remediation tracking

## How to Parse an OSCAL Document

### Step 1: Identify the File
Confirm the file path and check the extension to determine format.

### Step 2: Parse the Content
Based on the format:
- **JSON**: Parse using standard JSON parsing
- **YAML**: Parse using YAML safe loading
- **XML**: Parse using XML to dictionary conversion

### Step 3: Detect Model Type
Examine the root keys to identify the document type:
- Look for keys like `catalog`, `profile`, `system-security-plan`, etc.
- The presence of specific keys indicates the model type

### Step 4: Extract Key Information
For each model type, extract:

**Catalog:**
- `metadata` - Title, version, OSCAL version
- `groups` - Control families
- `controls` - Individual security controls
- `back-matter` - Resources and references

**System Security Plan:**
- `metadata` - System identification
- `import-profile` - Baseline reference
- `system-characteristics` - System description
- `system-implementation` - Implementation details
- `control-implementation` - How controls are implemented

**Component Definition:**
- `metadata` - Component identification
- `components` - Individual components
- `capabilities` - Component capabilities

## Output Structure

When parsing is complete, provide:
1. **Format detected** (JSON/YAML/XML)
2. **Model type** (catalog, SSP, etc.)
3. **Metadata summary** (title, version, last modified)
4. **Content summary** (count of controls, components, etc.)
5. **Any parsing warnings or issues**

## Example Usage

When asked "Parse this OSCAL catalog and tell me what's in it":

1. Read the file content
2. Detect format from extension
3. Parse the content
4. Identify it as a catalog
5. Report:
   - Title and version
   - Number of control families
   - Total number of controls
   - OSCAL version used

## Error Handling

Handle these common issues:
- **File not found**: Verify the path is correct
- **Invalid format**: Check file extension matches content
- **Malformed content**: Report specific parsing errors
- **Unknown model type**: List root keys for manual identification
