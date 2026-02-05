---
name: control-mapper
description: Map security controls between different compliance frameworks including NIST 800-53, ISO 27001, CIS Controls, PCI-DSS, HIPAA, SOC 2, and CMMC. Use this skill for gap analysis, multi-framework compliance, and control rationalization.
---

# Control Mapper Skill

Map security controls between compliance frameworks to support multi-framework compliance programs and gap analysis.

## When to Use This Skill

Use this skill when you need to:
- Map controls from one framework to another
- Perform gap analysis across frameworks
- Rationalize controls for multiple compliance requirements
- Identify equivalent controls across standards
- Build unified control frameworks

## Supported Frameworks

| Framework | Code | Description |
|-----------|------|-------------|
| NIST 800-53 | NIST-800-53 | Federal security controls |
| NIST CSF | NIST-CSF | Cybersecurity Framework |
| ISO 27001 | ISO-27001 | International security standard |
| CIS Controls | CIS-Controls | Critical security controls |
| PCI-DSS | PCI-DSS | Payment card security |
| HIPAA | HIPAA | Healthcare security |
| SOC 2 | SOC2 | Service organization controls |
| CMMC | CMMC | DoD cybersecurity maturity |

## Mapping Types

| Type | Confidence | Description |
|------|------------|-------------|
| **Exact** | 90-100% | Direct 1:1 mapping |
| **Partial** | 70-89% | Covers most requirements |
| **Related** | 50-69% | Conceptually similar |

---

## ⛔ CRITICAL: Authoritative Data Requirement

**Framework mappings require authoritative source documents.** Do NOT use training knowledge to map controls between frameworks.

### Why This Matters
- Incorrect mappings cause audit failures
- Framework versions change (ISO 27001:2022 differs from 2013)
- Mappings have nuances that training data cannot capture accurately
- Compliance decisions based on bad mappings create legal liability

### Required Documents for Mapping

| Mapping Task | Required Source |
|--------------|-----------------|
| NIST → ISO 27001 | NIST SP 800-53 Rev 5 mapping publication |
| NIST → CIS | CIS Controls mapping to NIST |
| NIST → PCI-DSS | PCI SSC mapping documentation |
| NIST → HIPAA | NIST crosswalk publications |
| Any framework mapping | Official mapping document from authoritative source |

### Authoritative Mapping Sources

1. **NIST Publications** — `https://csrc.nist.gov/publications`
2. **CIS Controls Mapping** — `https://www.cisecurity.org/controls`
3. **PCI SSC** — `https://www.pcisecuritystandards.org/`
4. **CSA Cloud Controls Matrix** — `https://cloudsecurityalliance.org/research/cloud-controls-matrix`

### Decision Tree

```
Need to map controls between frameworks?
                    │
                    ▼
    ┌───────────────────────────────┐
    │ Do you have the official      │
    │ mapping document?             │
    └───────────────┬───────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
    ┌───────┐               ┌───────┐
    │  Yes  │               │  No   │
    └───┬───┘               └───┬───┘
        │                       │
        ▼                       ▼
  Use the document         ⛔ STOP
  to create mappings       Request user provide
                          official mapping document
```

---

## Example Mapping Format

The tables below show the **output format** only — not authoritative mappings. Actual mappings must come from official sources.

### NIST 800-53 → ISO 27001 (Example Format)

| NIST Control | ISO Control | Type | Source Document |
|--------------|-------------|------|-----------------|
| AC-1 | A.5.1 | Partial | *Requires mapping doc* |
| AC-2 | A.5.16 | Exact | *Requires mapping doc* |

> ⚠️ **Note:** ISO 27001:2022 uses different control numbering than 2013. Always confirm framework version.

---

## How to Map Controls

### Step 1: Identify Source Framework
Determine the framework you're mapping FROM.

### Step 2: Identify Target Framework
Determine the framework you're mapping TO.

### Step 3: Look Up Mappings
For each source control:
1. Find known mappings in mapping database
2. Identify target control(s)
3. Note mapping type and confidence

### Step 4: Handle Gaps
If no mapping exists:
1. Analyze control requirements
2. Find conceptually similar controls
3. Mark as "related" with lower confidence
4. Note as potential gap

## Gap Analysis Process

### Step 1: List Source Controls
Get all controls from source framework that apply.

### Step 2: Map to Target
For each source control, find target mappings.

### Step 3: Identify Gaps
Controls without mappings or with only "related" mappings are gaps.

### Step 4: Report Findings

```
GAP ANALYSIS REPORT
==================
Source: NIST 800-53 (Moderate Baseline)
Target: ISO 27001

Fully Mapped: 180 controls (85%)
Partially Mapped: 25 controls (12%)
Gaps: 7 controls (3%)

GAPS REQUIRING ATTENTION:
- SI-4(5): No ISO equivalent for automated alerts
- CA-7: Continuous monitoring not explicitly covered
...
```

## Multi-Framework Mapping

When organization needs multiple frameworks:

### Step 1: Choose Primary Framework
Usually the most comprehensive (often NIST 800-53).

### Step 2: Map to All Targets
Create mappings from primary to each required framework.

### Step 3: Build Control Matrix

| Control ID | NIST | ISO | CIS | PCI |
|------------|------|-----|-----|-----|
| CTRL-001 | AC-1 | A.9.1 | 5.1 | 7.1 |
| CTRL-002 | AC-2 | A.9.2 | 5.2 | 7.2 |
...

### Step 4: Identify Rationalization Opportunities
Find controls that satisfy multiple frameworks with one implementation.

## Output Format

When mapping controls, provide:

```
CONTROL MAPPING
===============
Source: AC-2 (Account Management) [NIST 800-53]

Target Mappings:
1. ISO 27001 A.9.2.1 - User registration and de-registration
   Type: Exact | Confidence: 95%
   Notes: Direct mapping for account lifecycle

2. CIS Controls 5.1 - Establish and Maintain Inventory of Accounts
   Type: Partial | Confidence: 80%
   Notes: Covers account inventory aspect
   Source: CIS Controls v8 Mapping to NIST 800-53

3. PCI-DSS 7.1 - Limit access to system components
   Type: Related | Confidence: 70%
   Notes: Access limitation focus differs
   Source: PCI SSC NIST Mapping Document
```

## Example Usage

When asked "Map our NIST 800-53 controls to ISO 27001":

1. **Check for mapping document** — Do you have the official NIST-to-ISO mapping?
2. If NO: Request user provide the authoritative mapping document
3. If YES: Get list of implemented NIST controls from user's SSP
4. For each control, look up ISO mappings **from the authoritative document**
5. Group by mapping type (exact/partial/related)
6. Identify gaps (no mapping)
7. Provide mapping matrix with confidence levels and source citations

### If No Mapping Document Available

```
I cannot create accurate control mappings without an authoritative mapping document.

To map NIST 800-53 to ISO 27001, I need:
• NIST SP 800-53 Rev 5 to ISO 27001:2022 mapping document
• Or: CSA Cloud Controls Matrix (contains cross-framework mappings)

Please provide one of these documents, or I can help you locate official sources.

I will not create mappings from training data because:
• Compliance work requires authoritative, auditable sources
• Framework versions change and training data may be outdated
• Incorrect mappings create audit failures and security gaps
```
