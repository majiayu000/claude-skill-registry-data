---
name: controls-extractor
description: Extract and analyze security controls from OSCAL catalogs, profiles, and SSPs. Use this skill to get detailed information about control hierarchies, statements, parameters, and implementation status for compliance analysis.
---

# Controls Extractor Skill

Extract, analyze, and report on security controls from OSCAL documents including catalogs, profiles, and system security plans.

## When to Use This Skill

Use this skill when you need to:
- List all controls in a catalog or profile
- Extract control statements and guidance
- Analyze control families and hierarchies
- Find controls by ID, family, or keyword
- Get control statistics and coverage metrics
- Identify control enhancements

---

## ⛔ Authoritative Data Requirement

Control extraction works **only on user-provided OSCAL documents**.

### What This Skill Does
- Parses and extracts data from OSCAL documents you provide
- Analyzes structure and relationships within your documents
- Summarizes and reports on what's IN your documents

### What This Skill Does NOT Do
- Generate control lists from training knowledge
- Provide control definitions without a catalog document
- Assume what controls exist in a baseline you haven't provided

### Required Input
| Task | Required Document |
|------|-------------------|
| List controls | Catalog or Profile JSON/YAML/XML |
| Get control text | Catalog with the control definitions |
| Analyze SSP controls | SSP document |
| Compare baseline | Both baseline profile AND SSP |

### If User Asks Without Providing Document
```
I need the OSCAL document to extract controls from.

For NIST 800-53 controls, you can:
1. Upload the catalog file, or
2. I can fetch from: https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json

I cannot list controls from memory — compliance requires authoritative sources.
```

---

## Control Structure

OSCAL security controls have this hierarchy:

```
Control Family (Group)
└── Control (e.g., AC-1)
    ├── Statement (requirement text)
    ├── Guidance (implementation guidance)
    ├── Parameters (configurable values)
    ├── Parts (additional sections)
    └── Enhancements (sub-controls like AC-1(1))
```

## Control Families (NIST 800-53)

| Family | Name | Description |
|--------|------|-------------|
| AC | Access Control | User access management |
| AT | Awareness & Training | Security training |
| AU | Audit & Accountability | Logging and monitoring |
| CA | Assessment & Authorization | Security assessments |
| CM | Configuration Management | System configurations |
| CP | Contingency Planning | Disaster recovery |
| IA | Identification & Authentication | User identity |
| IR | Incident Response | Security incidents |
| MA | Maintenance | System maintenance |
| MP | Media Protection | Media handling |
| PE | Physical & Environmental | Physical security |
| PL | Planning | Security planning |
| PM | Program Management | Security program |
| PS | Personnel Security | Personnel controls |
| RA | Risk Assessment | Risk management |
| SA | System Acquisition | Development security |
| SC | System & Communications | Network security |
| SI | System & Information Integrity | Data integrity |

## How to Extract Controls

### Step 1: Identify Document Type
- **Catalog**: Contains control definitions
- **Profile**: Contains control selections/customizations
- **SSP**: Contains control implementations

### Step 2: Navigate to Controls

**From Catalog:**
```
catalog → groups → controls
```

**From Profile:**
```
profile → imports → include-controls
```

**From SSP:**
```
system-security-plan → control-implementation → implemented-requirements
```

### Step 3: Extract Control Details

For each control, extract:
- **id**: Control identifier (e.g., "AC-1")
- **title**: Human-readable name
- **class**: Control classification
- **parts**: Statement, guidance, etc.
- **parameters**: Configurable values
- **properties**: Baseline levels, etc.
- **controls**: Enhancements (nested)

### Step 4: Extract Parts

Control parts include:
- **statement**: The actual requirement
- **guidance**: Implementation guidance
- **objective**: Assessment objectives
- **assessment**: Assessment methods

To extract statement text:
1. Find part with `name="statement"`
2. Get `prose` field for text
3. If part has sub-parts, extract each

## Control Statistics

When analyzing controls, calculate:
- Total control count
- Controls by family
- Enhancement count
- Baseline distribution (LOW/MOD/HIGH)
- Parameter count

## Filtering Controls

### By Family
Find all controls where ID starts with family prefix (e.g., "AC-")

### By Baseline
Check properties for `baseline-impact` values:
- LOW
- MODERATE
- HIGH

### By Status (in SSP)
Check implementation status:
- implemented
- partially-implemented
- planned
- not-applicable

## Output Format

When extracting controls, provide:

```
CONTROLS SUMMARY
================
Total Controls: X
Enhancements: Y

By Family:
- AC (Access Control): N controls
- AU (Audit): N controls
...

Control Details:
- AC-1: Access Control Policy and Procedures
  Statement: [requirement text]
  Guidance: [implementation guidance]
  Enhancements: AC-1(1), AC-1(2)
```

## Example Usage

When asked "What access control requirements are in this catalog?":

1. Parse the catalog
2. Filter controls where ID starts with "AC"
3. For each control:
   - Extract ID and title
   - Get statement text
   - Note any enhancements
4. Report total count
5. List each control with key details

When asked "What controls are missing in this SSP?":

1. Parse the SSP
2. Identify the imported profile/baseline
3. Get required controls from baseline
4. Extract implemented controls from SSP
5. Compare lists
6. Report gaps with control IDs and titles
