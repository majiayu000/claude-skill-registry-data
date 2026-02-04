---
name: oscal-catalog-provider
description: Fetch official NIST 800-53 and FedRAMP OSCAL catalogs from authoritative sources
---

# OSCAL Catalog Provider

## Purpose

Provide access to official NIST and FedRAMP control catalogs without requiring user uploads. This skill knows where to fetch authoritative OSCAL content and how to use it.

## When to Use

Use this skill when:
- User needs to reference NIST 800-53 controls but hasn't uploaded a catalog
- Comparing an SSP against FedRAMP baselines
- Generating implementation narratives for specific controls
- Mapping controls between frameworks
- Any task requiring authoritative control definitions

## Official OSCAL Content Sources

### NIST 800-53 Rev 5 (Full Catalog)

| Resource | URL |
|----------|-----|
| **Catalog JSON** | `https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json` |
| **Catalog YAML** | `https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/yaml/NIST_SP-800-53_rev5_catalog.yaml` |
| **Repository** | `https://github.com/usnistgov/oscal-content` |

**Stats:** 1,193 controls (323 base controls + 870 enhancements) across 20 control families.

### FedRAMP Baselines (Rev 5)

| Baseline | Controls | URL |
|----------|----------|-----|
| **HIGH** | 421 | `https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_HIGH-baseline-resolved-profile_catalog.json` |
| **MODERATE** | 325 | `https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_MODERATE-baseline-resolved-profile_catalog.json` |
| **LOW** | 156 | `https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LOW-baseline-resolved-profile_catalog.json` |
| **LI-SaaS** | ~156 | `https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LI-SaaS-baseline-resolved-profile_catalog.json` |
| **Repository** | — | `https://github.com/GSA/fedramp-automation` |

### NIST Cybersecurity Framework (CSF)

| Resource | URL |
|----------|-----|
| **CSF 2.0 Catalog** | `https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/CSF/2.0/json/CSF_2.0_catalog.json` |

### CIS Controls

| Resource | URL |
|----------|-----|
| **CIS v8 Catalog** | `https://raw.githubusercontent.com/CISecurity/OCALCatalog/main/CIS_Controls_v8_catalog.json` |

## Instructions

### 1. Determine Required Catalog

Based on the user's request, identify which catalog is needed:

| User Mentions | Fetch This |
|---------------|------------|
| "NIST 800-53", "800-53", "NIST controls" | NIST 800-53 Rev 5 catalog |
| "FedRAMP High" | FedRAMP HIGH baseline |
| "FedRAMP Moderate", "FedRAMP" | FedRAMP MODERATE baseline |
| "FedRAMP Low" | FedRAMP LOW baseline |
| "FedRAMP LI-SaaS", "Low Impact SaaS" | FedRAMP LI-SaaS baseline |
| "NIST CSF", "Cybersecurity Framework" | NIST CSF 2.0 catalog |
| "CIS Controls", "CIS" | CIS Controls v8 catalog |

### 2. Attempt to Fetch the Catalog

**If you have web/fetch capabilities:** Retrieve the JSON from the appropriate URL above.

**If you cannot fetch (no network access):** You MUST ask the user to upload the catalog manually. Use this exact message format:

---

**I need the official OSCAL catalog to complete this task, but I can't fetch it directly.**

Please download and upload one of these files:

| You Need | Download From |
|----------|---------------|
| **NIST 800-53 Rev 5** | [NIST_SP-800-53_rev5_catalog.json](https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json) |
| **FedRAMP HIGH** | [FedRAMP_rev5_HIGH-baseline-resolved-profile_catalog.json](https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_HIGH-baseline-resolved-profile_catalog.json) |
| **FedRAMP MODERATE** | [FedRAMP_rev5_MODERATE-baseline-resolved-profile_catalog.json](https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_MODERATE-baseline-resolved-profile_catalog.json) |
| **FedRAMP LOW** | [FedRAMP_rev5_LOW-baseline-resolved-profile_catalog.json](https://raw.githubusercontent.com/GSA/fedramp-automation/master/dist/content/rev5/baselines/json/FedRAMP_rev5_LOW-baseline-resolved-profile_catalog.json) |

**Quick steps:**
1. Right-click the link above → "Save Link As..."
2. Upload the downloaded JSON file to this conversation
3. I'll continue with your request

---

**IMPORTANT:** Always attempt the fetch first before asking the user to upload. Only show the upload instructions if fetching fails or is not available.

### 3. Parse and Use

Once you have the catalog content:

1. Parse the JSON structure (see `oscal-parser` skill)
2. Navigate to the requested controls
3. Extract required information (title, description, parameters, guidance)
4. Apply to the user's task

### 4. Cache Within Conversation

If you fetch a catalog, retain it in context for the duration of the conversation to avoid re-fetching.

## Control Families Reference

NIST 800-53 Rev 5 organizes controls into 20 families:

| ID | Family | Controls |
|----|--------|----------|
| AC | Access Control | 25 base + enhancements |
| AT | Awareness and Training | 6 base |
| AU | Audit and Accountability | 16 base |
| CA | Assessment, Authorization, Procedures | 9 base |
| CM | Configuration Management | 14 base |
| CP | Contingency Planning | 13 base |
| IA | Identification and Authentication | 12 base |
| IR | Incident Response | 10 base |
| MA | Maintenance | 7 base |
| MP | Media Protection | 8 base |
| PE | Physical and Environmental Protection | 23 base |
| PL | Planning | 11 base |
| PM | Program Management | 32 base |
| PS | Personnel Security | 9 base |
| PT | Personally Identifiable Information Processing | 8 base |
| RA | Risk Assessment | 10 base |
| SA | System and Services Acquisition | 23 base |
| SC | System and Communications Protection | 51 base |
| SI | System and Information Integrity | 23 base |
| SR | Supply Chain Risk Management | 12 base |

## FedRAMP Baseline Quick Reference

### What's in Each Baseline

**FedRAMP LOW (156 controls)**
- Basic security hygiene
- Suitable for: Public, non-sensitive data
- Key families: AC, AU, IA, SC

**FedRAMP MODERATE (325 controls)**
- Most common authorization level
- Suitable for: CUI, PII, business-sensitive data
- Adds: Enhanced monitoring, incident response, contingency planning

**FedRAMP HIGH (421 controls)**
- Maximum protection
- Suitable for: Law enforcement, healthcare, financial, critical infrastructure
- Adds: Advanced access controls, cryptography, supply chain protections

### Control Differences by Baseline

| Control | LOW | MODERATE | HIGH |
|---------|-----|----------|------|
| AC-2 | ✓ | ✓ + (1)(2)(3)(4) | ✓ + (1)(2)(3)(4)(5)(11)(12)(13) |
| AU-2 | ✓ | ✓ | ✓ + additional events |
| IA-2 | ✓ + (1)(2) | ✓ + (1)(2)(8)(12) | ✓ + (1)(2)(5)(8)(12) |
| SC-8 | — | ✓ | ✓ + (1) |
| SC-28 | — | ✓ | ✓ + (1) |

## Example Usage

### User Request
> "What does AC-2 require at FedRAMP Moderate?"

### Agent Response Using This Skill

1. Identify: FedRAMP Moderate baseline needed
2. Fetch: FedRAMP MODERATE baseline catalog
3. Locate: AC-2 and its required enhancements
4. Respond with:
   - AC-2 base control requirements
   - Required enhancements: AC-2(1), AC-2(2), AC-2(3), AC-2(4)
   - FedRAMP-specific parameters (ODPs)
   - Implementation guidance

### User Request
> "Compare our SSP controls against FedRAMP Moderate"

### Agent Workflow

1. Fetch FedRAMP MODERATE baseline
2. Parse user's SSP (use `oscal-parser`)
3. Extract implemented controls from SSP (use `controls-extractor`)
4. Compare against baseline control list
5. Report gaps and coverage percentage

## Version Information

| Catalog | Version | OSCAL Version | Last Updated |
|---------|---------|---------------|--------------|
| NIST 800-53 | Rev 5.1.1 | 1.2.0 | 2024 |
| FedRAMP Baselines | Rev 5 | 1.2.0 | 2024 |
| NIST CSF | 2.0 | 1.2.0 | 2024 |

## Fallback: When Fetch Is Not Available

If fetching is not possible and the user hasn't uploaded a catalog:

**You MUST ask the user to upload the catalog.** Use the message template in Step 2 above.

### ⛔ DO NOT Use Training Knowledge for Compliance

**Never use training knowledge or memory to provide control definitions, parameters, or requirements for compliance tasks.**

This is not a recommendation — it is a hard requirement. Using unofficial control information for compliance work is dangerous and could cause serious harm.

| Risk | Consequence |
|------|-------------|
| **Control text may be outdated** | Failed audit, security gaps |
| **Parameters (ODPs) may be wrong** | Non-compliant implementation |
| **Enhancements may be missing** | Incomplete security posture |
| **Baseline assignments may differ** | Wrong controls for authorization level |

Compliance decisions must be based on **authoritative sources only**:
- Official NIST OSCAL catalogs
- Official FedRAMP baseline profiles
- Documents directly from NIST, GSA, or the authorizing body

### What To Say If User Asks You To Proceed Without The Catalog

> ⚠️ **I cannot provide control definitions from memory for compliance work.**
> 
> Using unofficial or potentially outdated control information could result in:
> - **Failed audits** and authorization delays
> - **Security vulnerabilities** from incorrect implementations
> - **Regulatory non-compliance** and potential fines
> - **Legal and financial consequences** for your organization
> 
> Please upload the official OSCAL catalog. I can help you download it — just let me know which baseline you need (NIST 800-53, FedRAMP Low/Moderate/High).
>
> If you need help with something that doesn't require authoritative control text, I'm happy to assist with that instead.

## Decision Tree

```
User needs catalog data
        │
        ▼
Can I fetch from URL?
        │
    ┌───┴───┐
   YES      NO
    │        │
    ▼        ▼
 Fetch    Has user uploaded?
  it          │
    │     ┌───┴───┐
    │    YES      NO
    │     │        │
    │     ▼        ▼
    │   Use      Ask user to upload
    │  upload    (show download links)
    │     │        │
    ▼     ▼        ▼
 ┌────────────┐   User refuses to upload?
 │ Continue   │        │
 │ with task  │        ▼
 └────────────┘   ⛔ STOP
                  Do NOT proceed with
                  compliance tasks.
                  
                  Offer to help with
                  non-compliance tasks instead.
```

## Related Skills

- `oscal-parser` — Parse fetched catalog JSON
- `controls-extractor` — Extract specific controls from catalog
- `control-mapper` — Map between NIST and other frameworks
