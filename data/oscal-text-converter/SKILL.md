---
name: oscal-text-converter
description: Convert OSCAL documents between formats (JSON, YAML, XML) and to human-readable formats like Markdown or plain text. Use for document transformation, reporting, and making OSCAL data accessible to non-technical stakeholders.
---

# OSCAL Text Converter Skill

Convert OSCAL documents between machine formats and to human-readable text for documentation, reporting, and accessibility.

## When to Use This Skill

Use this skill when you need to:
- Convert between OSCAL formats (JSON ↔ YAML ↔ XML)
- Generate human-readable documentation from OSCAL
- Create Markdown reports from OSCAL data
- Export controls to spreadsheet-friendly formats
- Produce plain-text summaries

---

## ✅ Data Source Principle

This skill transforms and formats **documents you provide**. All content in the output comes from your source OSCAL document — no compliance data is added from training knowledge.

---

## Supported Conversions

### Format Conversions
| From | To | Notes |
|------|-----|-------|
| JSON | YAML | Preferred for readability |
| JSON | XML | For legacy systems |
| YAML | JSON | For processing |
| YAML | XML | Less common |
| XML | JSON | Recommended |
| XML | YAML | Less common |

### Text Conversions
| From | To | Use Case |
|------|-----|----------|
| OSCAL | Markdown | Documentation |
| OSCAL | Plain Text | Quick review |
| OSCAL | CSV | Spreadsheets |
| OSCAL | HTML | Web publishing |

## Format Conversion Process

### JSON to YAML
1. Parse JSON document
2. Preserve all data structures
3. Output as YAML with proper indentation
4. Maintain OSCAL element ordering

### JSON to XML
1. Parse JSON document
2. Map to OSCAL XML schema
3. Add XML namespaces
4. Preserve all attributes

### XML to JSON
1. Parse XML document
2. Handle XML-specific elements (attributes, namespaces)
3. Map to OSCAL JSON structure
4. Validate output

## Human-Readable Conversions

### Catalog to Markdown

```markdown
# NIST SP 800-53 Rev 5

**Version:** 5.1.0
**Last Modified:** 2023-12-01
**OSCAL Version:** 1.1.2

## Control Families

### Access Control (AC)

#### AC-1: Policy and Procedures

**Control Statement:**
a. Develop, document, and disseminate to [Assignment: organization-defined 
personnel or roles]:
   1. An access control policy that:
      - Addresses purpose, scope, roles, responsibilities, management 
        commitment, coordination among organizational entities, and compliance
      - Is consistent with applicable laws, executive orders, directives, 
        regulations, policies, standards, and guidelines

**Discussion:**
Access control policy and procedures address the controls in the AC family...

**Related Controls:** PM-9, PS-8, SI-12

---

#### AC-2: Account Management

**Control Statement:**
a. Define and document the types of accounts allowed...
```

### SSP to Plain Text

```
SYSTEM SECURITY PLAN SUMMARY
============================

System Name: Cloud Application Platform
System ID: cloud-app-001
Authorization Status: Authorized
Authorization Date: 2024-01-15

SYSTEM DESCRIPTION
------------------
The Cloud Application Platform provides...

SECURITY CATEGORIZATION
-----------------------
Confidentiality: Moderate
Integrity: Moderate  
Availability: Low

Overall: Moderate

CONTROL IMPLEMENTATION SUMMARY
------------------------------
Total Controls Required: 325
Implemented: 287 (88%)
Partially Implemented: 25 (8%)
Planned: 10 (3%)
Not Applicable: 3 (1%)

TOP GAPS
--------
1. SI-4 - Security Monitoring (Planned)
2. CA-7 - Continuous Monitoring (Partial)
3. CP-9 - System Backup (Partial)
```

### Controls to CSV

```csv
Control ID,Title,Family,Status,Responsible Party,Implementation Summary
AC-1,Policy and Procedures,Access Control,Implemented,ISSO,Access control policy documented
AC-2,Account Management,Access Control,Implemented,IAM Admin,Azure AD manages accounts
AC-3,Access Enforcement,Access Control,Implemented,System Admin,RBAC enforced via policies
AC-4,Information Flow,Access Control,Partial,Network Admin,Firewall rules in place - DLP pending
```

## Conversion Templates

### Executive Summary Template

```markdown
# Executive Summary: [System Name]

## Authorization Status
**Status:** [Authorized/In Progress]
**Date:** [Date]
**Authorizing Official:** [Name]

## Compliance Overview
- **Framework:** [NIST 800-53 / FedRAMP / etc.]
- **Baseline:** [Low/Moderate/High]
- **Compliance Rate:** [X]%

## Key Metrics
| Metric | Value |
|--------|-------|
| Total Controls | [N] |
| Implemented | [N] |
| Open POA&M Items | [N] |
| Critical Risks | [N] |

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

### Control Implementation Template

```markdown
## [Control ID]: [Control Title]

**Implementation Status:** [Status]
**Responsible Role:** [Role]

### Requirement
[Control statement text]

### How We Implement This
[Implementation narrative]

### Evidence
- [Evidence item 1]
- [Evidence item 2]

### Related Controls
[List of related controls]
```

## Extraction Options

### Control Information
Extract and format:
- Control ID and title
- Statement text
- Guidance/discussion
- Parameters
- Enhancements
- Related controls

### Implementation Details
Extract and format:
- Implementation status
- Implementation narrative
- Responsible parties
- Evidence references
- Parameter settings

### System Information
Extract and format:
- System characteristics
- Authorization boundary
- Network diagrams (references)
- User types
- Data flows

## Output Formatting Options

### Markdown Options
- Headers (ATX style: #, ##, ###)
- Tables (pipe tables)
- Code blocks (for technical content)
- Lists (bulleted and numbered)
- Links and references

### Plain Text Options
- ASCII borders and dividers
- Fixed-width formatting
- Indentation for hierarchy
- Simple bullet points

### CSV Options
- Column headers
- Quoted strings
- Escaped commas
- Proper encoding (UTF-8)

## Example Usage

When asked "Convert this OSCAL catalog to readable Markdown":

1. Parse the OSCAL catalog
2. Extract metadata (title, version)
3. Iterate through groups (families)
4. For each control:
   - Format ID and title as header
   - Extract and format statement
   - Include guidance if present
   - List enhancements
5. Add table of contents
6. Output complete Markdown document

When asked "Export controls to CSV for spreadsheet":

1. Parse the OSCAL document
2. Determine relevant fields
3. Create header row
4. For each control, extract:
   - ID, title, family
   - Status (if SSP)
   - Description/summary
5. Format as CSV with proper escaping
6. Output for download/copy
