---
name: code-validation
description: Use when verification passes and human judgment is needed - presents demo scripts, specific checkpoint questions, and captures approval decisions. This is for VALIDATION (human decides), not verification (AI executes) or review (AI inspects).
---

# Human Validation

## Overview

Facilitate human judgment after code verification passes. Validation is the final step where a human confirms "Did I see it work?" through subjective observation.

**Announce:** On activation, say: "I'm using the code-validation skill to prepare a validation checkpoint for your decision."

**Database:** `.claude/data/story-tree.db`

**Critical Distinction:** See `CLAUDE.md` section "Quality Assurance Terminology":

| Term | Method | Actor | This Skill? |
|------|--------|-------|-------------|
| Code Review | Inspection | AI reads | NO |
| Code Verification | Execution | AI runs | NO |
| **Code Validation** | **Judgment** | **Human decides** | **YES** |

## Purpose

Bridge the gap between automated verification and release by obtaining informed human approval. Humans cannot be bypassed—they must observe and judge.

## When to Use

- After `code-verification` reports PASS
- Before transitioning to `releasing` stage
- When AI exhausts autonomous testing (escalated hold)
- When human checkpoint is required by process

## Workflow

### Phase 1: Load Verification Evidence

1. **Query story status:**

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
story = dict(conn.execute('''
    SELECT id, title, description, stage, hold_reason, notes
    FROM story_nodes WHERE id = ?
''', ('STORY_ID',)).fetchone())
print(json.dumps(story, indent=2))
conn.close()
"
```

2. **Load verification report** from `.claude/data/reviews/` or story notes
3. **Extract key results:**
   - Passed criteria count
   - Any UNTESTABLE items needing human observation
   - Test execution evidence

### Phase 2: Generate Demo Script

Create a step-by-step script the human can follow to observe the feature working. Use GIVEN > WHEN > THEN format for clarity:

```markdown
## Demo Script: [Story Title]

**Script ID:** VAL-[Story ID]
**Duration:** ~[estimate] seconds
**Prerequisites:** [Required system state]

### Scenario

**GIVEN** [Initial context/state]
**WHEN** [Actions taken]
**THEN** [Expected outcome]

### Steps

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | [Action to take] | [What should happen] |
| 2 | [Action to take] | [What should happen] |
| 3 | **Observe:** [What to look for] | [Expected observation] |
| 4 | [Action to take] | [What should happen] |
| 5 | **Verify:** [Expected outcome] | [Final state] |

### Pass/Fail Criteria

**Pass:** Business process completes as expected, without workarounds
**Fail:** Any deviation from expected results, even if workaround exists

### What Would Indicate Failure

- [Bullet point of problematic behavior]
- [Bullet point of edge case]
```

**Demo script requirements:**
- Use imperative voice ("Click", "Open", "Navigate")
- Include Script ID for traceability
- Specify prerequisites (system state before testing)
- Use GIVEN > WHEN > THEN for scenario description
- Highlight observation points with **Observe:** or **Verify:**
- Include expected duration estimate
- Define explicit Pass/Fail criteria

### Phase 3: Present Validation Checkpoint

Display a forcing-function checkpoint with specific questions:

```
╔══════════════════════════════════════════════════════════════════════════╗
║  VALIDATION CHECKPOINT: Story [ID] - "[Title]"                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Verification passed. Human judgment required.                           ║
║                                                                          ║
║  Please confirm after following the demo script:                         ║
║                                                                          ║
║  1. Did you observe the feature working as described?     [ ] Yes  [ ] No║
║                                                                          ║
║  2. Does the behavior match the acceptance criteria?      [ ] Yes  [ ] No║
║                                                                          ║
║  3. Did you try anything beyond the demo steps?           [ ] Yes  [ ] No║
║     (Exploratory testing reveals edge cases)                             ║
║                                                                          ║
║  4. Is this acceptable for release?                       [ ] Yes  [ ] No║
║                                                                          ║
║  If any "No", please describe what needs to change:                      ║
║  > ________________________________________                              ║
║                                                                          ║
║  Approximate time spent on demo: ______ minutes                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Checkpoint requirements (see `references/checkpoint-design.md`):**
- 5-9 specific questions maximum
- Each question requires individual acknowledgment
- Include exploratory testing prompt (beyond the script)
- Capture approximate validation time (eyeball time)
- Include free-text field for rejection reasoning
- No vague "approve?" prompts

### Phase 4: Capture Decision

Collect human response and record:

```yaml
validation_result:
  story_id: "[ID]"
  story_title: "[Title]"
  script_id: "VAL-[ID]"
  decision: approved | rejected | needs_work
  checkpoint_responses:
    - question: "Did you observe the feature working as described?"
      answer: yes | no
    - question: "Does the behavior match the acceptance criteria?"
      answer: yes | no
    - question: "Did you try anything beyond the demo steps?"
      answer: yes | no
    - question: "Is this acceptable for release?"
      answer: yes | no
  exploratory_notes: "[What was tried beyond demo]"
  time_spent_minutes: [number]
  human_notes: "[Free-text feedback]"
  validator: "[Who validated]"
  timestamp: "[ISO 8601]"
```

### Phase 5: Transition Story

Based on decision:

| Decision | New Stage | Hold Reason | Notes Update |
|----------|-----------|-------------|--------------|
| Approved | `releasing` | `NULL` | Append validation record |
| Rejected | `implementing` | `broken` | Append rejection reason |
| Needs Work | `implementing` | `polish` | Append improvement notes |

```python
python -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET stage = ?, hold_reason = ?, notes = notes || '\n\n' || ?
    WHERE id = ?
''', (
    'NEW_STAGE',
    'HOLD_REASON_OR_NULL',
    f'[Validation {datetime.now().isoformat()}] DECISION: notes here',
    'STORY_ID'
))
conn.commit()
conn.close()
"
```

---

## Preventing Rubber-Stamping

Validation must be meaningful, not perfunctory. Implement forcing functions:

| Technique | Implementation |
|-----------|----------------|
| **Specific questions** | Not "approve?" but "Did you see X happen?" |
| **Individual acknowledgment** | Each criterion requires explicit response |
| **Variable presentation** | Highlight different elements each time |
| **Accountability** | Log validator identity with decision |
| **Rejection path** | Make it easy to say "no" with structured feedback |
| **Eyeball time tracking** | Note elapsed time from demo start to decision |
| **Exploratory prompt** | Ask "Did you try anything beyond the demo steps?" |

### Detection Signals

Watch for rubber-stamping indicators:
- Validation completed in under 30 seconds
- All questions answered identically (all yes/no)
- No comments or notes provided
- Pattern of all-approvals with no rejections ever

### Cultural Reinforcement

When coaching validators:
1. Show examples of thorough validations in standups
2. Highlight when validation catches real issues
3. Coach individuals showing rubber-stamp patterns one-on-one
4. Celebrate rejections that prevent production issues

**See `references/preventing-rubber-stamps.md` for research.**

---

## Checklist Format

For complex stories, expand the checkpoint to 5-9 items:

```markdown
### Validation Checklist

| # | Question | Response |
|---|----------|----------|
| 1 | Did the export complete without errors? | [ ] Yes  [ ] No |
| 2 | Does the output file open correctly? | [ ] Yes  [ ] No |
| 3 | Are all expected columns present? | [ ] Yes  [ ] No |
| 4 | Is the data formatted correctly? | [ ] Yes  [ ] No |
| 5 | Would you ship this to users? | [ ] Yes  [ ] No |

**Overall Decision:** [ ] Approved  [ ] Needs Work  [ ] Rejected

**Notes:** _____________________
```

---

## Output Format

### CI Mode (Non-Interactive)

CI mode is NOT supported for validation. Human judgment cannot be automated.

If `CI=true` is detected, output:

```json
{
  "error": "validation_requires_human",
  "message": "Validation requires human judgment and cannot run in CI mode",
  "story_id": "[ID]",
  "recommendation": "Run validation interactively after CI verification passes"
}
```

### Interactive Mode

1. Display demo script
2. Wait for human to follow demo
3. Present checkpoint questions
4. Capture responses
5. Record decision with timestamp
6. Transition story stage

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/uat-best-practices.md` | Industry UAT checklist patterns |
| `references/checkpoint-design.md` | HITL approval workflow patterns |
| `references/preventing-rubber-stamps.md` | Forcing functions for meaningful review |

## Invocation

### Standard Usage
```
/code-validation --story-id=[ID]
```

### Bootstrap (First-Time or Refresh)
```
/code-validation --bootstrap
```

### After Verification
```
Story [ID] verification passed. Ready for human validation.
```
