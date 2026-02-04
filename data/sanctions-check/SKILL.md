---
name: sanctions-check
description: Screen entities against OFAC SDN, UN, EU, and other sanctions lists to identify compliance risks and regulatory violations
allowed-tools: ["Bash", "Read", "Write"]
---

# Sanctions Screening Skill

## Purpose
This skill enables comprehensive sanctions screening against multiple global sanctions databases including OFAC SDN, UN Security Council, EU Consolidated List, and other international sanctions lists.

## When to Use This Skill
Activate this skill when the user:
- Asks to check if a person or company is sanctioned
- Requests sanctions screening or OFAC compliance check
- Needs to verify sanctions status of an entity
- Wants to run compliance checks on individuals or organizations
- Uses keywords like: "sanctions", "OFAC", "SDN", "blacklist", "restricted parties"

## How to Use

### 1. Extract Entity Information
- Identify the entity name from the user's request
- Determine entity type (Person, Company, Organization)
- Note any additional context (country, aliases)

### 2. Run the Sanctions Check
Execute the sanctions tool using Python:
```bash
cd /Users/superfunguy/wsp/scolo/backend
python -c "from src.tools import sanctions; import json; result = sanctions.check('ENTITY_NAME'); print(json.dumps(result, indent=2))"
```

### 3. Interpret Results
The tool returns:
- **status**: "clear", "potential", or "match"
- **confidence**: Score from 0-100
- **findings**: List of matching sanctions records
- **sources**: Databases checked

### 4. Present Findings
- For **clear** status: Entity not found on sanctions lists
- For **potential** status: Possible matches requiring review
- For **match** status: Confirmed sanctions hit requiring immediate attention

## Examples

### Example 1: Check Individual
**User**: "Check if Vladimir Putin is sanctioned"
**Action**:
```bash
python -c "from src.tools import sanctions; import json; result = sanctions.check('Vladimir Putin', 'Person'); print(json.dumps(result, indent=2))"
```

### Example 2: Check Company
**User**: "Screen Acme Corporation for sanctions"
**Action**:
```bash
python -c "from src.tools import sanctions; import json; result = sanctions.check('Acme Corporation', 'Company'); print(json.dumps(result, indent=2))"
```

## Important Notes
- Always treat sanctions matches seriously - they have legal implications
- Consider name variations and transliterations
- Document all checks for audit purposes
- If uncertain, recommend professional compliance review