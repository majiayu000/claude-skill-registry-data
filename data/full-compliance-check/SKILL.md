---
name: full-compliance-check
description: Conduct comprehensive compliance screening using all available tools including sanctions, PEP, adverse media, UBO, and business registry checks for thorough due diligence
allowed-tools: ["Bash", "Read", "Write", "WebSearch"]
---

# Full Compliance Check Skill

## Purpose
This meta-skill orchestrates a complete compliance screening workflow, running multiple tools in sequence to provide comprehensive due diligence on individuals or organizations.

## When to Use This Skill
Activate this skill when the user:
- Requests a "full background check" or "comprehensive screening"
- Asks to "investigate" or "run due diligence" on an entity
- Needs complete compliance verification
- Uses terms like: "full check", "complete screening", "thorough investigation", "KYC", "AML check"

## Workflow

### 1. Initial Assessment
- Identify entity type (Person/Company)
- Extract entity name and any aliases
- Determine jurisdiction if known

### 2. Core Compliance Checks (Run in Sequence)
```python
# 1. Sanctions Screening
from src.tools import sanctions
sanctions_result = sanctions.check(entity_name)

# 2. PEP Screening (if individual)
from src.tools import pep_check
pep_result = pep_check.check(entity_name)

# 3. Adverse Media
from src.tools import adverse_media
media_result = adverse_media.check(entity_name)

# 4. Business Registry (if company)
from src.tools import business_registry
registry_result = business_registry.check(entity_name)

# 5. UBO Lookup (if company)
from src.tools import ubo_lookup
ubo_result = ubo_lookup.check(entity_name)
```

### 3. Risk Scoring
Aggregate findings to determine overall risk level:
- **High Risk**: Sanctions match, Level 1-2 PEP, serious adverse media
- **Medium Risk**: Potential sanctions, Level 3-4 PEP, moderate adverse media
- **Low Risk**: Clear on all checks, minor or no findings

### 4. Report Generation
Compile comprehensive report including:
- Executive summary with risk rating
- Detailed findings from each tool
- Recommendations for next steps
- Timestamp and sources

## Example Workflow

**User**: "Run full compliance check on Global Ventures LLC"

**Actions**:
1. Run sanctions check → Clear
2. Run business registry → Found, registered Delaware
3. Run UBO lookup → 3 beneficial owners identified
4. Run adverse media → Minor tax dispute 2019
5. Generate report → Low-Medium Risk

## Important Notes
- Always run core compliance tools first
- Document all findings for audit trail
- Consider running enhanced checks if initial screening raises concerns
- Timeouts may occur with multiple API calls - handle gracefully
- Results should be reviewed by compliance professionals for final determination