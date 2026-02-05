---
name: test-plan-formatting
description: Format concise, actionable test plans for Jira tickets using existing fptest tools and minimal MongoDB operations
tags: [testing, jira, documentation, fptest, mongodb]
---

# Test Plan Formatting

## When to Use This Skill

Use when creating test plans for Jira tickets that require:
- Manual testing with database setup
- Using fptest data generation tools
- MongoDB data verification
- Clear, concise steps without excessive explanation

## Core Principles

### 1. Be Concise, No Fluff
- Remove verbose explanations
- No excessive troubleshooting sections
- No repetitive validations
- One verification per test scenario

### 2. Use Existing Tools First
Use `fptest` commands instead of manual MongoDB document creation:

```bash
# Generate business objects
fptest data-gen gen-bo --bo-type detectedVulnerabilities --count 2 --sub-id <SUBID>
fptest data-gen gen-bo --bo-type riskOutcomes --count 4 --sub-id <SUBID>
fptest data-gen gen-bo --bo-type tasks --count 1 --sub-id <SUBID>
```

Only show manual MongoDB operations when:
- fptest doesn't support the operation
- Need to modify specific fields after generation
- Creating relationships between objects
- Adding custom fields (approvals, custom statuses, etc.)

### 3. Variable Placeholders
Wrap all variable placeholders in angle brackets:
- `<SUBID>` - Subscription ID
- `<RO1_ID>` - RiskOutcome ID
- `<DV_FINAL_STATUS_ID>` - Status selectizer ID
- `<FIELD_VALUE>` - Any dynamic value

### 4. Collection-Based Instructions
Specify what to add/modify, not how to run MongoDB commands:

**❌ Don't:**
```javascript
db.subscriptions.updateOne(
  { _id: "<SUBID>" },
  { $set: { "integrations.field": "value" } }
)
```

**✅ Do:**
```
Add to `subscriptions` collection:
{
  _id: "<SUBID>",
  "integrations.field": "value"
}
```

### 5. Assume Tester Knowledge
Testers have:
- Studio3T access and MongoDB familiarity
- Basic understanding of data structures
- Ability to query and modify documents

Don't over-explain:
- Basic MongoDB operations
- How to use Studio3T
- What a collection is

### 6. Manual Modifications After fptest
When fptest generates the base data, show only what needs changing:

```
2a. Create 2 Closed DVs

fptest data-gen gen-bo --bo-type detectedVulnerabilities --count 2 --sub-id <SUBID>

Manually set both DVs to closed in `businessObjects`:
{
  "info.isClosed": true,
  "info.status": "<DV_FINAL_STATUS_ID>"
}

Save the 2 DV `_id` values: <DV1_ID>, <DV2_ID>
```

### 7. Selectizer Configuration
When referencing selectizers, check if code requires subscription-specific config:

```
1. Configure Subscription

Add to `subscriptions` collection:
{
  _id: "<SUBID>",
  "integrations.riskOutcomesCloser.roFinalStatus": "<RO_FINAL_STATUS_ID>",
  "integrations.riskOutcomesCloser.dvFinalStatus": "<DV_FINAL_STATUS_ID>"
}

Get status IDs from `selectize_options` collection:
- Find {"type": "riskOutcomes-status", "subID": null} → copy option with "final": true → note its `id`
- Find {"type": "detectedVulnerabilities-status", "subID": null} → copy option with "final": true → note its `id`

*Note: Check if code requires subscription-specific selectizers (subID: "<SUBID>").
If defaults (subID: null) don't work, copy default docs to new docs with your subID.*
```

## Test Plan Structure

### Simple Step Format

```markdown
# <TICKET-ID> Test Plan

## Prerequisites
- Clean test subscription (<SUBID>)
- MongoDB access
- fptest CLI access

---

## 1. Configure Subscription

[What needs to be set in subscriptions collection]

## 2. Create Test Data

### 2a. Create X Business Objects
[fptest command]

[What to modify after creation]

### 2b. Create Related Data
[Manual additions to other collections]

## 3. Test Normal/Default Mode

**Run:**
[Command to execute]

**Expected Output:**
[Command output]

**Verify in `collectionName`:**
| Field | Expected Value |
|-------|---------------|
| ... | ... |

**✅ PASS:** [Success criteria]

## 4. Test Alternative Mode (Force/Special Case)

[Same structure as step 3]

## 5. Cleanup

Delete test data from:
- `businessObjects`: [what to delete]
- `otherCollection`: [what to delete]

---

## Summary

| Scenario | Condition | Expected Result |
|----------|-----------|-----------------|
| Test 1 | ... | ✅ Should pass |
| Test 2 | ... | ❌ Should fail |
```

### 8. Summary Tables
Show expected outcomes in table format at end, not scattered throughout:

```markdown
## Summary

| Scenario | Approval | Normal Mode | Force Mode |
|----------|----------|-------------|------------|
| RO1 | None | ✅ Closes | ✅ Closes |
| RO2 | Approved | ✅ Closes | ✅ Closes |
| RO3 | Requested | ❌ Blocked | ✅ Closes |
```

## Anti-Patterns to Avoid

### ❌ Don't: Show full MongoDB shell operations
```javascript
var timestamp = new Date().getTime();
var ro1_id = "test_ro_" + timestamp;
db.businessObjects.insert({
  _id: ro1_id,
  md: { type: "riskOutcomes", ... },
  info: { ... },
  // 50 more lines
})
```

### ✅ Do: Use fptest and show modifications
```
fptest data-gen gen-bo --bo-type riskOutcomes --count 1 --sub-id <SUBID>

Set in `businessObjects`:
{
  "related.detectedVulnerabilities": ["<DV1_ID>", "<DV2_ID>"]
}
```

### ❌ Don't: Repetitive validations
```
Verify RO1: db.businessObjects.findOne({_id: "..."})
Verify RO2: db.businessObjects.findOne({_id: "..."})
Verify RO3: db.businessObjects.findOne({_id: "..."})
```

### ✅ Do: Single verification with table
```
Verify in `businessObjects`:
| RO | Expected isClosed |
|----|-------------------|
| RO1 | true |
| RO2 | false |
```

### ❌ Don't: Excessive troubleshooting sections
```
## Troubleshooting

Issue: No ROs found
- Check DVs are closed
- Verify subscription config
- Check related array
- Ensure status is set
- Validate IDs are correct
[20 more lines...]
```

### ✅ Do: Keep it minimal or omit entirely
Test plans should be straightforward. If extensive troubleshooting is needed, the test is too complex.

## Example: Minimal Viable Test Plan

```markdown
# INT-1234 Test Plan

## Prerequisites
- Clean subscription (<SUBID>)
- MongoDB access
- fptest CLI

---

## 1. Configure Subscription

Add to `subscriptions` collection:
{
  "integrations.feature.enabled": true
}

## 2. Create Test Data

fptest data-gen gen-bo --bo-type riskOutcomes --count 2 --sub-id <SUBID>

Set in first RO in `businessObjects`:
{
  "info.customField": "test_value"
}

## 3. Test Feature

**Run:**
```bash
feature_command --sub-id <SUBID>
```

**Verify in `businessObjects`:**
| RO | Expected Result |
|----|-----------------|
| RO1 | `customField` updated |
| RO2 | Unchanged |

**✅ PASS:** RO1 processed, RO2 untouched

## 4. Cleanup

Delete from `businessObjects`: all ROs created in step 2
```

## Tool Integration

Test plans should reference Jira ticket using:
```bash
jira-update-ticket <TICKET-ID> --write-test-plan "$(cat test_plan.md)"
```

This automatically formats the test plan as a markdown code block in the Test Plan field (customfield_11003).
