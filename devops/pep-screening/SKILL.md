---
name: pep-screening
description: Check if individuals are politically exposed persons (PEPs), their relatives, or close associates, identifying potential corruption and money laundering risks
allowed-tools: ["Bash", "Read", "Write"]
---

# PEP (Politically Exposed Person) Screening Skill

## Purpose
This skill screens individuals against PEP databases to identify politically exposed persons, their family members, and close associates who may pose elevated compliance risks.

## When to Use This Skill
Activate this skill when the user:
- Asks to check if someone is a PEP or politically exposed
- Requests PEP screening or political exposure check
- Needs to verify political connections or government affiliations
- Wants enhanced due diligence on high-risk individuals
- Uses keywords like: "PEP", "politically exposed", "government official", "political risk"

## How to Use

### 1. Extract Individual Information
- Identify the person's full name
- Note any known affiliations or countries
- Consider name variations

### 2. Run the PEP Check
Execute the PEP screening tool:
```bash
cd /Users/superfunguy/wsp/scolo/backend
python -c "from src.tools import pep_check; import json; result = pep_check.check('PERSON_NAME'); print(json.dumps(result, indent=2))"
```

### 3. Interpret Results
The tool returns:
- **is_pep**: Boolean indicating PEP status
- **pep_level**: 1-4 (1=Head of State, 2=Minister, 3=Regional, 4=Related)
- **positions**: Current and former political positions
- **jurisdiction**: Country/region of political exposure
- **confidence**: Match confidence score

### 4. Risk Assessment
- **Level 1 PEPs**: Highest risk (heads of state, prime ministers)
- **Level 2 PEPs**: High risk (ministers, legislators)
- **Level 3 PEPs**: Medium risk (regional officials)
- **Level 4 PEPs**: Related persons (family, associates)

## Examples

### Example 1: Check Political Figure
**User**: "Is Angela Merkel a PEP?"
**Action**:
```bash
python -c "from src.tools import pep_check; import json; result = pep_check.check('Angela Merkel'); print(json.dumps(result, indent=2))"
```

### Example 2: Screen Business Associate
**User**: "Check if John Smith has any political exposure"
**Action**:
```bash
python -c "from src.tools import pep_check; import json; result = pep_check.check('John Smith'); print(json.dumps(result, indent=2))"
```

## Important Notes
- PEP status doesn't imply wrongdoing, but requires enhanced due diligence
- Consider both current and former positions
- Check for family members and close associates
- PEP status can change over time - regular rescreening recommended
- Different jurisdictions have varying PEP definitions