---
zones:
  state:
    paths:
      - sigil-mark/soul-binder/canon-of-flaws.yaml
    permission: read-write
  config:
    paths:
      - .sigilrc.yaml
      - .sigil-setup-complete
    permission: read
---

# Canonizing Flaws

## Purpose

Interview the user about an emergent behavior that has become beloved or expected, and register it in the Canon of Flaws for protection against "optimization."

## Philosophy

> "Beloved 'bugs' are registered and protected from optimization"

The key insight is that a "perfect" implementation of the original design would often be worse than the imperfect reality users have come to love. This skill protects the emergent soul of products.

## Pre-Flight Checks

1. **Sigil Setup**: Verify `.sigil-setup-complete` exists
2. **Canon File**: Check `sigil-mark/soul-binder/canon-of-flaws.yaml` exists
   - If missing, create with empty flaws array
3. **Strictness Level**: Load from `.sigilrc.yaml`

## Workflow

### Step 1: Identify the Behavior

If `behavior_name` not provided, ask:

```
question: "What emergent behavior would you like to protect?"
header: "Behavior"
```

Explain what qualifies:
- Was not originally intended
- Users have come to expect or enjoy
- Removing would cause confusion or complaints

Examples:
- A UI quirk that became a feature
- An interaction pattern that emerged from user behavior
- A "bug" that users now rely on

### Step 2: Interview - Intended vs Emergent

**Question 2.1: Intended Behavior**
```
question: "What was the INTENDED behavior? What should have happened according to the original design?"
header: "Intended"
```

**Question 2.2: Emergent Behavior**
```
question: "What ACTUALLY happens (that became beloved)? Describe the behavior users have come to expect."
header: "Emergent"
```

**Question 2.3: Discovery**
```
question: "How did you discover this behavior was valued?"
header: "Discovery"
options:
  - label: "User complaints when it changed"
    description: "Users noticed and complained when behavior was modified"
  - label: "Community discussion"
    description: "Users discussed/documented the behavior"
  - label: "Usage analytics"
    description: "Data showed users relying on this pattern"
  - label: "Internal discovery"
    description: "Team noticed users expecting this behavior"
multiSelect: false
```

### Step 3: Interview - Protection Criteria

**Question 3.1: Usage**
```
question: "Approximately what percentage of users rely on this behavior?"
header: "Usage"
options:
  - label: "< 5%"
    description: "Small group, may not meet threshold"
  - label: "5-20%"
    description: "Significant minority, meets threshold"
  - label: "20-50%"
    description: "Large segment, strong candidate"
  - label: "> 50%"
    description: "Majority, critical to protect"
multiSelect: false
```

If < 5%, warn but allow proceeding with UNDER_REVIEW status.

**Question 3.2: Community Attachment**
```
question: "How would users react if this behavior was 'fixed'?"
header: "Attachment"
options:
  - label: "Mild confusion"
    description: "Low attachment - some users might notice"
  - label: "Complaints"
    description: "Moderate attachment - expect support tickets"
  - label: "Outrage/backlash"
    description: "High attachment - would damage trust"
multiSelect: false
```

**Question 3.3: Skill Expression (Optional)**
```
question: "Does this behavior reward skill or expertise?"
header: "Skill"
options:
  - label: "Yes - timing/learning based"
    description: "Requires learning, separates novice from expert"
  - label: "No - discovered by accident"
    description: "Random discovery, not skill-based"
  - label: "N/A"
    description: "Not applicable to this product type"
multiSelect: false
```

### Step 4: Define Protection

**Question 4.1: Affected Code**
```
question: "What code patterns might accidentally 'fix' this behavior?"
header: "Patterns"
```

Provide examples:
- `*submit*handler*`
- `*debounce*click*`
- `*animation*duration*`

Accept glob patterns that should trigger protection checks.

**Question 4.2: Protection Rule**
```
question: "Complete this sentence: 'Any change that __________ must be BLOCKED.'"
header: "Rule"
```

Example: "Any change that prevents the double-click animation must be BLOCKED."

### Step 5: Generate Entry

Generate the next flaw ID by reading existing entries:

```yaml
- id: "FLAW-{next_id}"
  name: "{behavior_name}"
  status: "PROTECTED"  # or UNDER_REVIEW if < 5% usage
  canonized_date: "{today}"
  canonized_by: "{user or 'Taste Owner'}"

  description: |
    {Brief description of the flaw}

  intended_behavior: |
    {From Q2.1}

  emergent_behavior: |
    {From Q2.2}

  why_protected: |
    - Discovery: {From Q2.3}
    - Usage: {From Q3.1}
    - Attachment: {From Q3.2}
    - {Additional context}

  affected_code_patterns:
    - "{pattern_1}"
    - "{pattern_2}"

  protection_rule: |
    {From Q4.2}

  de_canonization:
    requires_threshold: 70  # percent approval
    cooldown_days: 180
```

### Step 6: Confirm and Save

Show the user the generated entry:

```
Here's the Canon of Flaws entry I've prepared:

{formatted_entry}

Does this accurately capture the behavior to protect?
```

```
question: "Confirm this entry?"
header: "Confirm"
options:
  - label: "Save"
    description: "Add to Canon of Flaws"
  - label: "Edit"
    description: "Make changes before saving"
  - label: "Cancel"
    description: "Discard and exit"
multiSelect: false
```

On confirmation:
1. Load existing `canon-of-flaws.yaml`
2. Append new flaw to flaws array
3. Update `last_updated` timestamp
4. Save file

### Step 7: Report

```
{status_emoji} FLAW-{id} "{name}" has been added to the Canon of Flaws.

Status: {PROTECTED | UNDER_REVIEW}

The agent will now {BLOCK | WARN on} any change that matches:
  {affected_patterns}

Protection Rule:
  "{protection_rule}"

De-canonization process:
  - Requires 70% community approval via /consult
  - Requires Taste Owner sign-off via /approve
  - Update canon-of-flaws.yaml status to DE_CANONIZED

Next steps:
  - /craft will respect this flaw during implementation
  - Changes to affected patterns will be {blocked | flagged}
```

## Strictness Behavior

| Strictness | Protected Flaw Violation |
|------------|--------------------------|
| discovery | "Consider" - informational only |
| guiding | Warning with explanation |
| enforcing | BLOCK with override option |
| strict | BLOCK with override option |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Setup not complete" | Missing marker | Run `/setup` first |
| "Usage below threshold" | < 5% usage | Allow with UNDER_REVIEW status |
| "Similar flaw exists" | Duplicate pattern | Suggest updating existing flaw |
| "Canon file missing" | No canon-of-flaws.yaml | Create empty file first |

## Do NOT

- Automatically reject flaws with low usage
- Judge whether the behavior "should" be a flaw
- Require technical justification

## DO

- Trust user judgment about community attachment
- Capture the emotional context, not just technical details
- Make protection actionable with specific patterns
- Explain the de-canonization process clearly
