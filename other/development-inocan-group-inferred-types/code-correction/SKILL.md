---
name: code-correction
description: Use when code-verification fails - analyzes verification failures, identifies root causes, corrects the implementation, and re-verifies. This skill fixes code to meet acceptance criteria, not modifies requirements to match code.
---

# Code Correction - Fix Failed Verification

Correct code that failed verification so it passes acceptance criteria.

> **Critical Distinction:** This corrects **code** to meet **requirements** (stories remain unchanged).
> See `CLAUDE.md` section "Quality Assurance Terminology" for definitions.

**Announce:** On activation, say: "I'm using the code-correction skill to fix the implementation so it passes verification."

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## Purpose

Bridge the gap between failed verification and passing verification by **correcting the code implementation**. Stories and acceptance criteria remain the source of truth - only the code changes.

## When to Use

- After `code-verification` reports FAIL
- When story stage is `verifying` with `hold_reason='broken'`
- When acceptance criteria tests fail
- When user says "fix verification failures", "correct the code", "make tests pass"

## Workflow

### Step 1: Load Verification Failure Report

**Query story with failed verification:**

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
stories = [dict(row) for row in conn.execute('''
    SELECT s.id, s.title, s.description, s.stage, s.hold_reason, s.notes,
        (SELECT MIN(depth) FROM story_paths WHERE descendant_id = s.id) as node_depth
    FROM story_nodes s
    WHERE s.stage = 'verifying'
      AND s.hold_reason = 'broken'
      AND s.terminus IS NULL
    ORDER BY node_depth ASC
''').fetchall()]
print(json.dumps(stories, indent=2))
conn.close()
"
```

**Extract failure details from notes:**
- Parse verification report embedded in notes
- Identify which criteria failed
- Identify which tests failed
- Extract error messages and stack traces

### Step 2: Analyze Failure Root Cause

For each failed criterion/test:

1. **Read the failing test code** to understand expected behavior
2. **Read the implementation code** to understand current behavior
3. **Identify the gap** between expected and actual

**Failure categories:**

| Category | Description | Correction Strategy |
|----------|-------------|---------------------|
| Missing | Feature not implemented | Implement missing code |
| Incorrect | Wrong behavior | Fix logic error |
| Incomplete | Partial implementation | Complete the implementation |
| Broken | Previously worked, now fails | Fix regression |
| Integration | Works alone, fails with siblings | Resolve conflict |

### Step 3: Plan Corrections

Before making changes, create a correction plan:

```markdown
## Correction Plan for Story [ID]

### Failure 1: [Criterion/Test name]
- **Root Cause:** [Description of why it fails]
- **Files to Modify:** [List of files]
- **Changes Required:** [Description of changes]
- **Verification Method:** [How to confirm fix]

### Failure 2: ...
```

**Planning rules:**
- Address failures in dependency order (if A depends on B, fix B first)
- Keep changes minimal - fix only what's broken
- Avoid refactoring - this is correction, not improvement
- Don't change tests - the tests define expected behavior

### Step 4: Implement Corrections

For each failure in the plan:

1. **Make minimal code changes** to fix the specific failure
2. **Run the specific failing test** to verify the fix
3. **Run related tests** to check for regressions
4. **Commit the fix** with a clear message

**Commit message format:**
```
fix: [criterion/test name] - [brief description]

Story: [ID]
Criterion: [number]
```

### Step 5: Re-verify

After all corrections:

```bash
python .claude/skills/code-verification/generate_report.py <story_id>
```

**If verification passes:**
- Update story stage and clear hold
- Report success

**If verification still fails:**
- Analyze new failures
- Return to Step 2 (max 3 iterations)
- If still failing after 3 attempts, escalate to human

### Step 6: Update Story Status

**On successful correction:**

```python
python -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET hold_reason = NULL,
        notes = notes || '\n[Correction ' || datetime('now') || '] Fixed verification failures',
        updated_at = datetime('now')
    WHERE id = ?
''', ('STORY_ID',))
conn.commit()
conn.close()
"
```

**On correction failure (max attempts reached):**

```python
python -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET hold_reason = 'escalated',
        human_review = 1,
        notes = notes || '\n[Correction ' || datetime('now') || '] Unable to fix after 3 attempts - escalating',
        updated_at = datetime('now')
    WHERE id = ?
''', ('STORY_ID',))
conn.commit()
conn.close()
"
```

## Mode Detection

**CI Mode** activates when:
- Environment variable `CI=true` is set, OR
- Trigger phrase includes "(ci)" like "correct code (ci)"

**CI Mode behavior:**
- No confirmation prompts
- Structured JSON output
- Auto-escalate after max attempts

**Interactive Mode** (default):
- Present correction plan for approval
- Pause between corrections for review
- Allow human to guide approach

## Output Format

### Correction Report (YAML)

```yaml
correction_report:
  story_id: "1.2.3"
  title: "Feature Title"
  corrected_at: "2025-12-29T10:30:00Z"

  failures_addressed:
    - criterion: "User can export data as CSV"
      root_cause: "Missing CSV header row"
      files_modified: ["src/exporter.py"]
      tests_fixed: ["tests/test_export.py::test_csv_header"]

    - criterion: "Export includes timestamps"
      root_cause: "Timestamp format incorrect"
      files_modified: ["src/exporter.py"]
      tests_fixed: ["tests/test_export.py::test_timestamp_format"]

  verification_result: pass  # pass | fail
  attempts: 1
  commits: ["abc1234"]
```

### CI Mode Output (JSON)

**Success:**
```json
{
  "story_id": "1.7",
  "status": "corrected",
  "failures_fixed": 3,
  "attempts": 1,
  "commits": ["abc1234", "def5678"],
  "verification_result": "pass"
}
```

**Failure (escalated):**
```json
{
  "story_id": "1.7",
  "status": "escalated",
  "failures_remaining": 1,
  "attempts": 3,
  "reason": "Unable to fix criterion 2 after 3 attempts",
  "recommendation": "human_review"
}
```

## Correction Principles

### DO

- **Fix the code** - never modify acceptance criteria or tests
- **Keep changes minimal** - only fix what's broken
- **Preserve test intent** - tests define correct behavior
- **Document root causes** - help future debugging
- **Verify after each fix** - catch regressions early

### DO NOT

- Modify acceptance criteria to match broken code
- "Fix" tests to pass with broken implementation
- Refactor unrelated code while correcting
- Add features while correcting bugs
- Skip verification after corrections

## Exit Conditions

| Result | Transition |
|--------|------------|
| All failures fixed | Clear `hold_reason`, keep stage at `verifying` for re-verification |
| Max attempts reached | Set `hold_reason='escalated'`, `human_review=1` |

## Related Skills

- **code-verification:** Identifies failures this skill corrects
- **debug-orchestrator:** Handles complex debugging scenarios
- **code-review:** Reviews code quality (separate from verification)
- **human-validation:** Human judgment after verification passes

## References

- **Verification Skill:** `.claude/skills/code-verification/SKILL.md`
- **Database:** `.claude/data/story-tree.db`
- **QA Terminology:** `CLAUDE.md` (Quality Assurance Terminology section)
