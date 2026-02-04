---
name: compliance-report-generator
description: Generate compliance reports from OSCAL assessment results, SSPs, and POA&Ms in various formats. Use this skill to create audit-ready documentation, executive summaries, and detailed compliance status reports.
---

# Compliance Report Generator Skill

Generate professional compliance reports from OSCAL documents for audits, management reviews, and continuous monitoring.

## When to Use This Skill

Use this skill when you need to:
- Create audit-ready compliance documentation
- Generate executive summary reports
- Produce detailed control implementation reports
- Create POA&M status reports
- Build compliance dashboards data

---

## ⛔ Authoritative Data Requirement

Compliance reports are generated **only from user-provided documents**.

### What This Skill Does
- Formats data FROM documents you provide into professional reports
- Calculates metrics based on YOUR document content
- Structures output for auditors and leadership

### What This Skill Does NOT Do
- Generate compliance status from training knowledge
- Make up control implementation data
- Assume compliance percentages without source documents

### Required Inputs
| Report Type | Required Documents |
|-------------|-------------------|
| Compliance Status | SSP |
| Gap Analysis | Baseline Profile + SSP |
| Assessment Report | SAR (Assessment Results) |
| POA&M Report | POA&M document |

### All Data Comes From Your Documents
```
To generate a compliance report, I need:
• Your SSP, POA&M, or assessment results document
• [For gap analysis] Your baseline profile

All metrics and status information will come directly from these
documents. I will not generate compliance data from assumptions.
```

---

## Report Types

| Type | Audience | Content |
|------|----------|---------|
| Executive Summary | Leadership | High-level metrics, risks, status |
| Compliance Status | Auditors | Control-by-control status |
| Assessment Report | Security Team | Detailed findings |
| POA&M Report | Program Managers | Remediation tracking |
| Gap Analysis | Implementers | Missing controls, recommendations |

## Report Formats

- **Markdown** - Portable, version-controllable
- **HTML** - Interactive, shareable
- **JSON** - Machine-readable, API-friendly
- **Text** - Simple, universal

## Report Components

### Executive Summary
- Overall compliance percentage
- Risk level summary
- Key findings (top 3-5)
- Trend comparison
- Next steps

### Compliance Metrics
```
Total Controls: 325
Implemented: 287 (88%)
Partially Implemented: 25 (8%)
Planned: 10 (3%)
Not Applicable: 3 (1%)
```

### Control Status Table
| Control | Title | Status | Evidence | Notes |
|---------|-------|--------|----------|-------|
| AC-1 | Policy | ✅ Implemented | DOC-001 | Complete |
| AC-2 | Account Mgmt | ⚠️ Partial | DOC-002 | MFA pending |

### Findings Summary
| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 2 | Immediate action required |
| High | 5 | 30-day remediation |
| Moderate | 12 | 60-day remediation |
| Low | 8 | Monitor and address |

## How to Generate Reports

### Step 1: Gather Data
From the OSCAL document, extract:
- Metadata (system name, date, version)
- Control implementations
- Assessment results (if available)
- POA&M items (if available)

### Step 2: Calculate Metrics
Compute:
- Implementation percentages by status
- Controls by family
- Findings by severity
- Trend data (if historical data available)

### Step 3: Structure Content

**For Executive Summary:**
1. System identification
2. Overall compliance score
3. Risk level
4. Top findings
5. Recommendations

**For Detailed Report:**
1. Introduction and scope
2. Methodology
3. Compliance by control family
4. Detailed findings
5. Evidence references
6. Recommendations
7. Appendices

### Step 4: Format Output

**Markdown Format:**
```markdown
# Compliance Assessment Report

## Executive Summary

**System:** Cloud Infrastructure
**Assessment Date:** 2024-01-15
**Overall Compliance:** 88%
**Risk Level:** Moderate

## Key Findings

1. **MFA Not Fully Deployed** (HIGH)
   - Impact: Credential theft risk
   - Recommendation: Deploy MFA to all users by Q1

2. **Log Retention Below Policy** (MODERATE)
   - Impact: Forensic capability limited
   - Recommendation: Extend retention to 90 days
```

## Document-Specific Reports

### From SSP
- System description
- Control implementation status
- Responsible parties
- Implementation narratives

### From Assessment Results
- Assessment findings
- Risk determinations
- Evidence collected
- Assessor observations

### From POA&M
- Open findings
- Remediation status
- Milestone tracking
- Resource allocation

## Compliance Score Calculation

```
Compliance Score = (Implemented + (Partial × 0.5)) / (Total - Not_Applicable) × 100
```

Example:
- Implemented: 280
- Partial: 20
- Planned: 10
- N/A: 15
- Total: 325

Score = (280 + (20 × 0.5)) / (325 - 15) × 100 = 93.5%

## Report Templates

### FedRAMP Status Report
```
AUTHORIZATION STATUS REPORT
===========================
System: [Name]
Authorization Date: [Date]
Sponsor: [Agency]

Current Status: [Authorized/In Progress]
Continuous Monitoring: [Active/Issues]

Control Summary:
- Baseline: [Moderate/High]
- Total Controls: [N]
- Implemented: [N] ([%])

POA&M Summary:
- Open Items: [N]
- Overdue: [N]
- Closed (30 days): [N]
```

### ISO 27001 Compliance Report
```
ISO 27001 COMPLIANCE REPORT
===========================
Organization: [Name]
Scope: [Description]
Report Date: [Date]

Statement of Applicability:
- Applicable Controls: [N]
- Implemented: [N] ([%])
- Excluded: [N] (with justification)

By Domain:
- A.5 Information Security Policies: [%]
- A.6 Organization of Information Security: [%]
...
```

## Example Usage

When asked "Generate a compliance report for this SSP":

1. Parse the SSP document
2. Extract metadata and system info
3. Count controls by implementation status
4. Calculate compliance percentage
5. Identify top risks and gaps
6. Generate formatted report
7. Include recommendations
