---
name: quick-screen
description: Perform rapid initial screening using only sanctions, PEP, and adverse media checks for quick risk assessment
allowed-tools: ["Bash", "Read", "Write"]
---

# Quick Screen Skill

## Purpose
This skill performs a rapid initial risk assessment using the three most critical compliance tools: sanctions, PEP, and adverse media screening.

## When to Use This Skill
Activate this skill when the user:
- Needs a "quick check" or "rapid screening"
- Requests initial risk assessment
- Has time constraints
- Uses terms like: "quick screen", "fast check", "initial assessment", "preliminary screening"

## Workflow

### 1. Rapid Checks (Run in Parallel if Possible)
```python
# Run these three checks
from src.tools import sanctions, pep_check, adverse_media

# 1. Sanctions - Most critical
sanctions_result = sanctions.check(entity_name)

# 2. PEP - Political exposure
pep_result = pep_check.check(entity_name)

# 3. Adverse Media - Reputation
media_result = adverse_media.check(entity_name)
```

### 2. Quick Risk Assessment
- **Red Flags**: Any sanctions hit, Level 1-2 PEP, serious adverse media
- **Yellow Flags**: Potential matches, Level 3-4 PEP, moderate adverse media
- **Green Flags**: All clear

### 3. Recommendations
- **Red Flags** → Recommend full compliance check immediately
- **Yellow Flags** → Suggest enhanced due diligence
- **Green Flags** → Standard onboarding can proceed

## Example

**User**: "Quick screen John Smith"

**Actions**:
1. Sanctions check → Clear ✓
2. PEP check → Not a PEP ✓
3. Adverse media → No findings ✓
Result: Low risk, clear to proceed

## Important Notes
- This is for initial screening only
- Not sufficient for high-risk transactions
- Always escalate if any red flags found
- Full compliance check recommended for material relationships