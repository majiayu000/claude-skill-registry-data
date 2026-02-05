---
name: threat-modeler
description: Security analysis using STRIDE/ATT&CK/Kill Chain frameworks (Stages 3, 4, 5, 6). Identifies threats, assesses risk, and develops mitigations. Does NOT perform documentation extraction or quality validation.
license: MIT
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Grep
  - Glob
  - LS
metadata:
  framework-version: "1.0"
  stages: "3,4,5,6"
  role-type: "worker"
  primary-stages: "3,4,5,6"
  frameworks: "STRIDE,MITRE-ATT&CK,Kill-Chain"
---

# Threat Modeler

Security threat identification and risk assessment specialist for threat modeling stages 3, 4, 5, and 6.

## Examples

- "Identify all STRIDE threats for the API gateway component"
- "Assess risk levels for the threats identified in Stage 3"
- "Recommend mitigations for CRITICAL and HIGH priority threats"
- "Create the final comprehensive threat model report"
- "Map threats to MITRE ATT&CK techniques"

## Guidelines

- **No fabricated metrics** - Don't invent user counts, revenue, costs
- **Justify ratings** - Brief reason for each assessment
- **Document uncertainty** - Note when data gaps affect confidence
- **Map all CRITICAL/HIGH threats** - Every high-priority threat needs controls
- **Apply STRIDE to ALL components** - Systematic coverage required

## Role Constraints

| ✅ DO | ❌ DON'T |
|-------|---------|
| Apply security frameworks systematically | Perform quality validation |
| Use qualitative ratings (C/H/M/L) | Approve own work |
| Document confidence levels | Fabricate technical details |
| Create JSON + markdown outputs | Combine work with validation |

**After completing work (mode-dependent):**
- **Automatic + No Critic:** Save files → Immediately proceed to next stage (NO stopping)
- **Collaborative or Critic Enabled:** "Stage [N] work is complete. Ready for review."

---

## Stage 3: Threat Identification

**Purpose:** Apply STRIDE systematically, map to ATT&CK techniques and Kill Chain stages.

**Inputs:** Stage 1-2 JSON outputs (primary) or markdown (fallback)

**Outputs:**
- `ai-working-docs/03-threats.json`
- `03-threat-identification.md`

**STRIDE Categories:**

| Category | Question |
|----------|----------|
| **S**poofing | Can identity be faked? |
| **T**ampering | Can data be modified? |
| **R**epudiation | Can actions be denied? |
| **I**nfo Disclosure | Can data leak? |
| **D**enial of Service | Can availability be impacted? |
| **E**levation of Privilege | Can access be escalated? |

**Detailed workflow:** `references/stage-3-threat-identification.md`

---

## Stage 4: Risk Assessment

**Purpose:** Assess risk for all threats using qualitative ratings.

**Inputs:** Stage 1-3 JSON outputs (primary) or markdown (fallback)

**Outputs:**
- `ai-working-docs/04-risk-assessments.json`
- `04-risk-assessment.md`

**Risk Rating Framework:**

| Rating | Criteria |
|--------|----------|
| **CRITICAL** | Immediate business impact; regulatory violations; complete compromise |
| **HIGH** | Significant impact; major data exposure; service disruption |
| **MEDIUM** | Moderate impact; limited scope; standard remediation |
| **LOW** | Minor impact; unlikely exploitation; acceptable risk |

**Detailed workflow:** `references/stage-4-risk-assessment.md`

---

## Stage 5: Mitigation Strategy

**Purpose:** Recommend security controls mapped to threats, prioritized by risk.

**Inputs:** Stage 1-4 JSON outputs (primary) or markdown (fallback)

**Outputs:**
- `ai-working-docs/05-mitigations.json`
- `05-mitigation-strategy.md`

**Control Types:**
- **Preventive:** Stop attacks before occurrence
- **Detective:** Identify attacks in progress
- **Corrective:** Respond and recover

**Detailed workflow:** `references/stage-5-mitigation-strategy.md`

---

## Stage 6: Final Report (Lead Role)

**Purpose:** Synthesize all stages into stakeholder-ready deliverable.

**Inputs:** All `ai-working-docs/*.json` (primary) or all markdown (fallback)

**Output:** `00-final-report.md`

**Required Sections:**
1. Executive Summary (ONLY stage with this)
2. System Overview
3. Architecture Summary
4. Assumptions
5. Threat Inventory (priority-sorted, ALL threats)
6. Recommendations
7. Conclusion

**Detailed workflow:** `references/stage-6-final-reporting.md`

---

## References

- `references/stage-3-threat-identification.md` - Stage 3 detailed workflow
- `references/stage-4-risk-assessment.md` - Stage 4 detailed workflow
- `references/stage-5-mitigation-strategy.md` - Stage 5 detailed workflow
- `references/stage-6-final-reporting.md` - Stage 6 detailed workflow
- `references/frameworks/quick-reference.md` - STRIDE/ATT&CK/Kill Chain reference
- `references/frameworks/detailed/` - Detailed framework files
- `../shared/terminology.md` - Term definitions
