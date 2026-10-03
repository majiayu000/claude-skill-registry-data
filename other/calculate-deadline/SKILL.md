---
name: calculate-deadline
description: "Calculates legal deadlines from trigger events using Victorian legislation rules. Use when Mandy says 'calculate deadline', 'when is the deadline', 'limitation period', 'how long do we have', 'conciliation deadline', or needs to know any time limit for a matter."
---

# Calculate Deadline

## Important
- Manual-only. NEVER guess deadlines — always read from `rules/deadlines.json`.
- Show calculation steps for special_calc rules.

## Instructions

### Step 0: Resolve Matter

### Step 1: Parse Event
Get event-type and event-date from arguments.
If not provided: "What event triggered this deadline? (e.g., insurer_decision, date_of_injury, conciliation_outcome) And what date did it occur?"

### Step 2: Calculate
Read `matter.json` and `rules/deadlines.json`. Find matching rule for claim type + event type.
If no match: "No deadline rule found for '{event_type}' on {claim_type} claims."
For `special_calc` rules: show calculation steps, ask Mandy to confirm.

### Step 3: Present
```
DEADLINE: {name}
TRIGGER: {event} on {date}
DUE DATE: {calculated} ({days} remaining)
LEGISLATIVE BASIS: {act} {section}
CONSEQUENCE: {what happens if missed}
```
If already passed: ALERT prominently with ⚠️.

### Step 4: Update and Commit
Add/update `matter.json` deadlines array. Update index. Offer Outlook calendar push if MCP available. Log and commit. Proactive check.
