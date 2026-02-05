---
name: audit-resolution
description: Use when presenting audit discrepancies to user for decision (HITL). For each discrepancy show file path, diff (template vs actual), and ask user what to do - [1] apply template, [2] update template (PR), [3] ignore, or [4] custom instruction. Records decisions for remediation phase.
---

# Audit Resolution

**Purpose:** Present audit discrepancies to user and capture decisions for each finding (HITL).

**Use when:** Investigation phase has completed and you have audit discrepancies that need user decisions before remediation.

**Critical:** This is a HITL skill - EVERY discrepancy requires a user decision. NO auto-fixes.

---

## Workflow

1. **Present Summary**
   - Total files audited
   - Total discrepancies found
   - Breakdown by severity (critical, warning, info)

2. **Sort Discrepancies**
   - Order: critical → warning → info
   - Within severity: alphabetical by file path

3. **For Each Discrepancy (Loop)**
   - Show file path and line number
   - Show diff in table format:
     | Aspect | Template | Actual |
     |--------|----------|--------|
     | field | expected | found |
   - Show severity level
   - HITL: Ask user "What should I do?"

4. **Present Decision Options**

   ```
   [1] Apply template - Fix file to match template
   [2] Update template - Template is wrong, create PR to update it
   [3] Ignore - Accept this deviation
   [4] Custom - Provide specific instruction
   ```

5. **Capture User Decision**
   - Record: discrepancy ID, action choice, custom instruction (if [4])
   - Validate choice is 1-4
   - If [4], prompt for custom instruction

6. **Record All Decisions**
   - Build decisions array for remediation phase
   - Count decisions by type
   - Prepare summary for next phase

---

## Input

From `/skill audit-investigation`:

```typescript
{
  discrepancies: [
    {
      id: string,              // Unique identifier
      file: string,            // Absolute path
      line: number,            // Line number
      field: string,           // Config field name
      expected: string,        // Template value
      actual: string,          // Current value
      severity: "critical" | "warning" | "info",
      agent: string,           // Config agent that found it
      template_source: string  // Path to template file
    }
  ],
  summary: {
    files_audited: number,
    total_discrepancies: number,
    by_severity: {
      critical: number,
      warning: number,
      info: number
    }
  }
}
```

---

## Output

```typescript
{
  decisions: [
    {
      discrepancy_id: string,
      action: "apply" | "update_template" | "ignore" | "custom",
      custom_instruction?: string,  // Only if action === "custom"
      discrepancy: {                // Copy of original discrepancy
        file: string,
        line: number,
        field: string,
        expected: string,
        actual: string,
        severity: string,
        agent: string,
        template_source: string
      }
    }
  ],
  summary: {
    total_discrepancies: number,
    apply_count: number,
    update_template_count: number,
    ignore_count: number,
    custom_count: number
  }
}
```

---

## Presentation Format

### Summary Block

```markdown
## Audit Results Summary

- Files audited: {files_audited}
- Total discrepancies: {total_discrepancies}
  - Critical: {critical_count}
  - Warning: {warning_count}
  - Info: {info_count}

I will now walk through each discrepancy for your decision.
```

### Per-Discrepancy Block

```markdown
---

### Discrepancy {n}/{total} [{severity}]

**File:** `{file}`
**Line:** {line}
**Field:** `{field}`
**Agent:** {agent}

**Difference:**
| Aspect | Template | Actual |
|--------|----------|--------|
| {field} | {expected} | {actual} |

**Template source:** `{template_source}`

**What should I do?**

1. Apply template - Fix file to match template
2. Update template - Template is wrong, create PR to update it
3. Ignore - Accept this deviation
4. Custom - Provide specific instruction

Your choice (1-4):
```

### After All Decisions

```markdown
## Resolution Summary

Decisions captured for {total_discrepancies} discrepancies:

- Apply template: {apply_count}
- Update template: {update_template_count}
- Ignore: {ignore_count}
- Custom: {custom_count}

Proceeding to remediation phase.
```

---

## Validation Rules

1. **Every discrepancy gets a decision** - No skipping
2. **Invalid choice → re-prompt** - Must be 1-4
3. **Custom requires instruction** - If [4], must collect free-text
4. **Sort by severity first** - Critical issues presented first
5. **Copy full discrepancy** - Decisions include all context for remediation

---

## Example

**Input:**

```json
{
  "discrepancies": [
    {
      "id": "disc-001",
      "file": "/path/to/eslint.config.js",
      "line": 23,
      "field": "rules.no-console",
      "expected": "error",
      "actual": "warn",
      "severity": "warning",
      "agent": "eslint-agent",
      "template_source": "plugins/metasaver-core/skills/config/eslint/templates/base.js"
    }
  ],
  "summary": {
    "files_audited": 1,
    "total_discrepancies": 1,
    "by_severity": {
      "critical": 0,
      "warning": 1,
      "info": 0
    }
  }
}
```

**Presentation:**

```markdown
## Audit Results Summary

- Files audited: 1
- Total discrepancies: 1
  - Critical: 0
  - Warning: 1
  - Info: 0

I will now walk through each discrepancy for your decision.

---

### Discrepancy 1/1 [WARNING]

**File:** `/path/to/eslint.config.js`
**Line:** 23
**Field:** `rules.no-console`
**Agent:** eslint-agent

**Difference:**
| Aspect | Template | Actual |
|--------|----------|--------|
| rules.no-console | error | warn |

**Template source:** `plugins/metasaver-core/skills/config/eslint/templates/base.js`

**What should I do?**

1. Apply template - Fix file to match template
2. Update template - Template is wrong, create PR to update it
3. Ignore - Accept this deviation
4. Custom - Provide specific instruction

Your choice (1-4):
```

**User response:** `1`

**Output:**

```json
{
  "decisions": [
    {
      "discrepancy_id": "disc-001",
      "action": "apply",
      "discrepancy": {
        "file": "/path/to/eslint.config.js",
        "line": 23,
        "field": "rules.no-console",
        "expected": "error",
        "actual": "warn",
        "severity": "warning",
        "agent": "eslint-agent",
        "template_source": "plugins/metasaver-core/skills/config/eslint/templates/base.js"
      }
    }
  ],
  "summary": {
    "total_discrepancies": 1,
    "apply_count": 1,
    "update_template_count": 0,
    "ignore_count": 0,
    "custom_count": 0
  }
}
```

---

## Edge Cases

| Scenario                            | Behavior                                           |
| ----------------------------------- | -------------------------------------------------- |
| Zero discrepancies                  | Skip this phase, proceed to report                 |
| User enters invalid choice          | Re-prompt with error message                       |
| User enters [4] without instruction | Prompt for instruction text                        |
| Same file multiple discrepancies    | Present each separately, allow different decisions |
| Critical severity                   | Highlight in presentation, but still user decides  |

---

## Integration Points

**Inputs from:** `/skill audit-investigation`
**Outputs to:** `/skill audit-remediation`, `/skill template-update`

**Phase order:**

1. Investigation (READ-ONLY, collects findings)
2. **Resolution (HITL, captures decisions)** ← This skill
3. Remediation (WRITE, applies decisions)
