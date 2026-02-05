---
name: oscal-ssp-validator
description: Validates OSCAL System Security Plan documents against NIST 800-18 Rev 1 requirements and FedRAMP baselines. Identifies missing elements, quality issues, and provides remediation guidance for achieving ATO compliance.
version: 1.0.0
author: euCann
tags:
  - oscal
  - ssp
  - validation
  - fedramp
  - nist-800-18
  - ato
  - compliance
---

# OSCAL SSP Validator

Perform comprehensive quality assurance on OSCAL System Security Plan (SSP) documents to ensure compliance with NIST 800-18 and FedRAMP requirements before submission.

## ⛔ Anti-Hallucination Policy

**CRITICAL: This skill handles compliance-critical information.**

### NEVER Use Training Knowledge For:
- FedRAMP baseline control requirements
- NIST 800-18 section requirements
- Control parameter values
- Specific validation rules

### ALWAYS Request Authoritative Sources:
When validating against a baseline, request the official source:

```
FedRAMP LOW:
https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LOW-baseline-resolved-profile_catalog.json

FedRAMP MODERATE:
https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_MODERATE-baseline-resolved-profile_catalog.json

FedRAMP HIGH:
https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_HIGH-baseline-resolved-profile_catalog.json
```

### Safe Operations (can use skill knowledge):
- OSCAL schema structure validation
- UUID format checking
- Cross-reference integrity
- Placeholder detection
- Structural completeness checks

### Unsafe Operations (require authoritative data):
- "Is control AC-2 required for FedRAMP Moderate?" → Fetch baseline
- "What parameters does SC-7 require?" → Fetch baseline
- "How many controls in FedRAMP HIGH?" → Fetch baseline

## When to Use This Skill

- **Pre-Submission Review**: Validate SSP completeness before FedRAMP submission
- **Continuous ATO**: Regular compliance checks during authority maintenance
- **Legacy SSP Modernization**: Assess inherited documentation quality
- **Gap Analysis**: Identify missing required elements systematically
- **CI/CD Integration**: Automated compliance checking in deployment pipelines

## Validation Categories

### 1. Structural Completeness (NIST 800-18 Rev 1 Compliance)

Verifies presence of all 16 required sections:
- **Section 1**: System Identification
- **Section 2**: System Categorization (FIPS 199)
- **Section 3**: System Overview
- **Section 4**: System Environment
- **Section 5**: System Interconnections
- **Section 6**: Laws, Regulations, and Policies
- **Section 7**: Minimum Security Controls
- **Section 8**: System Security Architecture
- **Section 9**: Security Control Selection and Implementation
- **Section 10**: Information Types
- **Section 11**: System Boundary
- **Section 12**: Network Architecture
- **Section 13**: Hardware and Software Inventory
- **Section 14**: Security Control Summary
- **Section 15**: Attachments and Supporting Documentation
- **Section 16**: Points of Contact

### 2. Content Quality Assessment

- **Description Completeness**: Key sections meet minimum length requirements (>50 words)
- **Placeholder Detection**: Identifies "TBD", "[FILL IN]", or incomplete descriptions
- **OSCAL Data Types**: Validates proper use of strings, UUIDs, dates, URIs
- **Cross-Reference Integrity**: All component/control UUIDs resolve correctly
- **Narrative Quality**: Descriptions are clear, specific, and actionable

### 3. FedRAMP Compliance Verification

- **Baseline Coverage**: Validates against Low/Moderate/High baselines
- **Template Conformance**: Matches FedRAMP SSP template structure
- **Required Attachments**: Checks for SAR, SAP, POA&M references
- **Control Enhancements**: Verifies required enhancements are addressed
- **Continuous Monitoring**: Validates CM strategy documentation

### 4. Security Control Implementation

- **Control Coverage**: All baseline controls have implementation statements
- **By-Component Assignments**: Each control mapped to responsible components
- **Responsible Roles**: Implementation roles clearly identified
- **Implementation Status**: Valid status (implemented, planned, inherited)
- **Parameters**: Required parameter values provided
- **Inheritance**: Clearly documents inherited vs. system-specific controls

### 5. OSCAL Schema Validation

- **JSON/XML Syntax**: Well-formed OSCAL document
- **Schema Compliance**: Validates against OSCAL 1.1.2 schema
- **Enumeration Values**: Valid values for status, roles, types
- **Required Fields**: All mandatory OSCAL fields present
- **Cardinality**: Correct number of required/optional elements

## How to Use

### Basic Validation
```
Validate this OSCAL SSP against NIST 800-18 and FedRAMP Moderate baseline
```

### Detailed Analysis with Severity Ranking
```
Perform a detailed validation of this SSP and prioritize findings by severity (critical, high, medium, low)
```

### Gap Analysis Against Baseline
```
Compare this SSP against FedRAMP Moderate requirements and identify all gaps in control coverage
```

### Remediation Planning
```
Validate this SSP and provide specific remediation steps with effort estimates for each finding
```

### Section-Specific Review
```
Review the System Security Architecture section for completeness and provide improvement recommendations
```

### Pre-Submission Checklist
```
Run a pre-submission validation checklist for FedRAMP authorization and confirm readiness
```

## Input Requirements

**Supported Formats:**
- OSCAL JSON (`system-security-plan` model)
- OSCAL XML (`system-security-plan` model)
- FedRAMP SSP Template (if converted to OSCAL format)

**File Upload:**
- Single SSP file (up to 10MB)
- Or paste OSCAL JSON/XML content directly
- Or provide URL to SSP in repository

**Context Information (Optional but Helpful):**
- System name and authorization boundary
- Target FedRAMP baseline (Low/Moderate/High)
- Submission deadline
- Known issues or areas of concern

## Output Format

### 1. Executive Summary (Markdown)

```markdown
# OSCAL SSP Validation Report
**System:** Example Cloud Service
**Date:** 2025-12-31
**Baseline:** FedRAMP Moderate

## Overall Assessment
✅ Compliance Score: 78/100
⚠️ Critical Findings: 3
⚠️ High Priority: 12
ℹ️ Medium Priority: 28
ℹ️ Low Priority: 15

## Readiness Status
🟡 NOT READY FOR SUBMISSION
Estimated remediation effort: 40-60 hours

## Top Priorities
1. Add Authorization Boundary description (Critical)
2. Complete interconnection agreements (Critical)
3. Document 15 missing control implementations (High)
```

### 2. Detailed Findings (Structured JSON)

```json
{
  "validation_metadata": {
    "date": "2025-12-31T14:30:00Z",
    "validator_version": "1.0.0",
    "ssp_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "system_name": "Example Cloud Service",
    "baseline": "FedRAMP-Moderate"
  },
  "summary": {
    "overall_score": 78,
    "total_findings": 58,
    "critical": 3,
    "high": 12,
    "medium": 28,
    "low": 15
  },
  "findings": [
    {
      "id": "F001",
      "severity": "critical",
      "category": "structural_completeness",
      "section": "system-characteristics/authorization-boundary",
      "finding": "Missing Authorization Boundary Description",
      "requirement": "NIST 800-18 Rev 1, Section 11",
      "fedramp_requirement": "Section 2 - Authorization Boundary Diagram Required",
      "current_state": "Field is empty",
      "remediation": "Add a detailed description of the authorization boundary including all system components, data flows, and external connections.",
      "oscal_path": "system-security-plan.system-characteristics.authorization-boundary",
      "effort_estimate": "4-6 hours",
      "priority": 1
    }
  ]
}
```

### 3. Remediation Roadmap (Sprint Plan)

**Sprint 1 (Week 1): Critical + High Priority**
- [ ] Add authorization boundary description and diagram
- [ ] Document all system interconnections with agreements
- [ ] Complete missing control implementations
- [ ] Validate UUIDs and fix cross-reference errors

**Sprint 2 (Week 2): Medium Priority**
- [ ] Enhance control descriptions to meet quality standards
- [ ] Add responsible roles for each component
- [ ] Document parameter values for all controls
- [ ] Attach required evidence artifacts

**Sprint 3 (Week 3): Low Priority + Polish**
- [ ] Improve narrative quality in overview sections
- [ ] Add detailed hardware/software inventory
- [ ] Complete POC information for all roles
- [ ] Final validation and submission package prep

## Validation Rules Reference

The skill uses comprehensive validation rules based on:

1. **NIST SP 800-18 Rev 1** - Guide for Developing Security Plans for Information Systems
2. **FedRAMP SSP Template** - Rev 5 (latest) requirements
3. **OSCAL 1.1.2 Schema** - Official NIST OSCAL specification
4. **FedRAMP Baselines** - Low, Moderate, High control sets

### Severity Definitions

| Severity | Definition |
|----------|------------|
| **Critical** | Blocker for submission; missing required content |
| **High** | Likely to cause 3PAO finding or JAB rejection |
| **Medium** | Should be addressed; impacts quality/completeness |
| **Low** | Enhancement opportunity; not submission-blocking |

## Examples

### Example 1: Quick Pre-Submission Check

**User:** "I need a quick compliance check on this SSP - are we ready to submit?"

**Claude Response:**
```
I'll validate your SSP against FedRAMP Moderate requirements...

⚠️ NOT READY - Found 3 critical issues:
1. Missing authorization boundary diagram (Section 2)
2. 8 controls lack implementation statements
3. Interconnection agreements not documented

Estimated fix time: 24-32 hours
Recommended: Address these before submission
```

### Example 2: Detailed Gap Analysis

**User:** "Compare this against FedRAMP Moderate and show me every gap"

**Claude Response:**
```
Comprehensive Gap Analysis Results:

Structural Completeness: 85%
✅ 14/16 required sections present
❌ Missing: Interconnections, Attachments

Control Coverage: 72%
✅ 213/295 controls fully documented
⚠️ 67 controls have partial implementations
❌ 15 controls completely missing

[... detailed breakdown by control family ...]

Priority Actions: [ranked list]
```

### Example 3: Remediation Guidance

**User:** "Fix the AC-2 implementation issues"

**Claude Response:**
```
AC-2 (Account Management) Remediation Plan:

Current Issues:
- No by-component assignments
- Missing responsible roles
- Parameter values not specified

Recommended Fix:
1. Add these components:
   - IAM Service: Manages user accounts
   - App Layer: Enforces authentication
   - Database: Controls data access

2. Implementation Details:
- IAM: Automated provisioning via Terraform
- App: OAuth 2.0 + RBAC enforcement
- DB: Row-level security + audit logging

Effort: 2-3 hours
Priority: High (required for ATO)
```

## Limitations

**This skill cannot:**

- **Assess Actual Security**: Only validates documentation, not actual system security posture
- **Scan Infrastructure**: Cannot connect to systems to verify implementations
- **Convert Formats**: Requires OSCAL input; cannot convert Word/Excel SSPs
- **Evaluate Control Effectiveness**: Cannot assess if controls actually work
- **Sign or Certify**: Provides validation only; does not replace 3PAO assessment

**Requirements:**
- SSP must already be in OSCAL format
- Schema-valid JSON or XML required
- Cannot validate proprietary or classified content
- Works best with FedRAMP/NIST 800-53 frameworks

## Related Skills

| Skill | Use For |
|-------|---------|
| `oscal-validator` | General OSCAL document validation |
| `advanced-oscal-validator` | Deep validation with business rules |
| `risk-assessor` | Convert findings into POA&M items |
| `component-definition-builder` | Generate component definitions |
| `compliance-report-generator` | Generate audit-ready reports |

## Support & Documentation

- **OSCAL Documentation**: https://pages.nist.gov/OSCAL/
- **FedRAMP Resources**: https://automate.fedramp.gov/
- **NIST 800-18**: https://csrc.nist.gov/publications/detail/sp/800-18/rev-1/final
- **Validation Rules**: See `templates/oscal_validation_rules.json`
- **Examples**: See `examples/` directory

---

**Ready to validate your SSP? Upload your OSCAL JSON/XML file and ask!**
