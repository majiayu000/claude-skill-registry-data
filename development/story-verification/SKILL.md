---
name: story-verification
description: Use when user says "verify story", "check acceptance criteria", "validate implementation", "is story ready", or asks to verify that an implemented story meets its acceptance criteria - parses acceptance criteria from story description, verifies each with test/code evidence, generates pass/fail report, and updates story status based on results.
disable-model-invocation: true
---

# Story Verification - Acceptance Criteria Validator

Verify that implemented stories meet their acceptance criteria before marking ready.

**Announce:** On activation, say: "I'm using the story-verification skill to verify the implementation meets acceptance criteria."

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## Purpose

Bridge the gap between `verifying` and `implemented` stages by validating that acceptance criteria are actually satisfied. This prevents incomplete implementations from being marked implemented. Stories transition: `stage='verifying'` → `stage='implemented'` → `stage='ready'`.

## Mode Detection

**CI Mode** activates when:
- Environment variable `CI=true` is set, OR
- Trigger phrase includes "(ci)" like "verify story (ci)"

**CI Mode behavior:**
- No confirmation prompts
- Structured JSON output for automation
- Skip interactive review options

**Interactive Mode** (default):
- Present verification results for human review
- Allow manual override of failed criteria
- Offer guidance on addressing failures

## Workflow

### Step 1: Select Story to Verify

**Query stories ready for verification:**

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
stories = [dict(row) for row in conn.execute('''
    SELECT s.id, s.title, s.description, s.stage, s.project_path, s.human_review,
        (SELECT MIN(depth) FROM story_paths WHERE descendant_id = s.id) as node_depth
    FROM story_nodes s
    WHERE s.stage IN ('verifying', 'reviewing')
      AND s.hold_reason IS NULL AND s.disposition IS NULL
    ORDER BY node_depth ASC
''').fetchall()]
print(json.dumps(stories, indent=2))
conn.close()
"
```

**Selection rules:**
- If user specified ID: validate exists and stage is `verifying` or `reviewing` (not held/disposed)
- Otherwise: select first `verifying` story (shallowest first)
- Interactive only: Confirm selection with user

### Step 2: Parse Acceptance Criteria

Run the criteria parser:

```bash
python .claude/skills/story-verification/parse_criteria.py <story_id>
```

**Expected output:**
```json
{
  "story_id": "1.7",
  "title": "Privacy & Data Security",
  "criteria": [
    {"index": 1, "text": "All data stored locally with no network transmission", "checked": false},
    {"index": 2, "text": "Delete specific time ranges from activity history", "checked": false}
  ],
  "criteria_count": 5
}
```

**Checkbox format recognition:**
- `- [ ]` = unchecked criterion
- `- [x]` or `- [X]` = checked criterion (already verified)

### Step 3: Verify Each Criterion

For each unchecked criterion, gather evidence:

#### 3a. Search for Related Tests

```bash
python .claude/skills/story-verification/find_evidence.py test "<criterion_text>" [project_path]
```

Look for:
- Test files that cover the criterion
- Assertions that validate the behavior
- Test names that match criterion keywords

#### 3b. Search for Implementation Code

```bash
python .claude/skills/story-verification/find_evidence.py code "<criterion_text>" [project_path]
```

Look for:
- Functions/methods implementing the behavior
- Configuration handling for configurable features
- Error handling for edge cases

#### 3c. Run Related Tests

If tests exist:
```bash
python -m pytest <test_file>::<test_function> -v
```

### Step 4: Classify Each Criterion

| Status | Definition | Evidence Required |
|--------|------------|-------------------|
| `PASS` | Criterion fully satisfied | Tests pass + code exists |
| `PARTIAL` | Partially implemented | Some tests pass, gaps identified |
| `FAIL` | Not implemented | No evidence found |
| `UNTESTABLE` | Cannot verify automatically | Requires manual testing |
| `SKIP` | Already checked in description | Criterion marked `[x]` |

**Classification logic:**
```python
def classify_criterion(test_evidence, code_evidence, test_results):
    if criterion_already_checked:
        return 'SKIP'
    if not code_evidence:
        return 'FAIL'
    if not test_evidence:
        return 'UNTESTABLE'
    if test_results and all_pass:
        return 'PASS'
    if test_results and some_pass:
        return 'PARTIAL'
    return 'UNTESTABLE'
```

### Step 5: Generate Verification Report

```bash
python .claude/skills/story-verification/generate_report.py <story_id>
```

**Report format:**
```
STORY VERIFICATION REPORT
=========================

Story: [ID] - [Title]
Status: [current_status]

ACCEPTANCE CRITERIA RESULTS:

1. [PASS] All data stored locally with no network transmission
   Evidence: tests/test_database.py::test_no_network_calls
   Code: src/syncopaid/database.py:45-60

2. [FAIL] Delete specific time ranges from activity history
   Missing: No implementation found for time-range deletion

3. [UNTESTABLE] Clear visual confirmation when sensitive data is deleted
   Reason: UI behavior requires manual verification

SUMMARY:
  Passed:     3/5 (60%)
  Failed:     1/5 (20%)
  Untestable: 1/5 (20%)

RECOMMENDATION: [READY | NEEDS_WORK | MANUAL_REVIEW]
```

### Step 6: Update Story Stage

Based on verification results:

| Result | Action |
|--------|--------|
| All PASS/SKIP | Update stage to `implemented` |
| Any FAIL | Keep stage at `verifying`, set hold_reason='escalated', human_review=1 |
| All PASS but some UNTESTABLE | Keep stage at `verifying`, set hold_reason='escalated', human_review=1 |
| Mixed results | Interactive: ask user; CI: keep at `verifying` with hold |

```bash
python .claude/skills/story-verification/update_status.py <story_id> <new_stage> "<verification_notes>"
```

### Step 7: Update Acceptance Criteria Checkboxes

For criteria that PASS, update the description to mark them checked:

```python
python -c "
import sqlite3, re
conn = sqlite3.connect('.claude/data/story-tree.db')
story = conn.execute('SELECT description FROM story_nodes WHERE id = ?', ('STORY_ID',)).fetchone()
description = story[0]
# Replace specific criterion's checkbox
updated = description.replace('- [ ] CRITERION_TEXT', '- [x] CRITERION_TEXT')
conn.execute('UPDATE story_nodes SET description = ? WHERE id = ?', (updated, 'STORY_ID'))
conn.commit()
conn.close()
"
```

## Output Format

**CI Mode - Success:**
```json
{
  "story_id": "1.7",
  "title": "Privacy & Data Security",
  "previous_status": "verifying",
  "new_status": "implemented",
  "criteria_results": [
    {"criterion": "...", "status": "PASS", "evidence": "..."},
    {"criterion": "...", "status": "PASS", "evidence": "..."}
  ],
  "summary": {"passed": 5, "failed": 0, "untestable": 0},
  "recommendation": "IMPLEMENTED"
}
```

**CI Mode - Failures:**
```json
{
  "story_id": "1.7",
  "title": "Privacy & Data Security",
  "previous_status": "verifying",
  "new_status": "verifying",
  "criteria_results": [
    {"criterion": "...", "status": "FAIL", "reason": "No implementation found"}
  ],
  "summary": {"passed": 3, "failed": 2, "untestable": 0},
  "recommendation": "NEEDS_WORK",
  "failures": ["criterion 2: ...", "criterion 4: ..."]
}
```

**Interactive Mode:** Conversational summary with options to:
- Accept results and update status
- Override specific criterion results
- Add manual verification notes
- Skip and keep current status

## References

- **Database:** `.claude/data/story-tree.db`
- **Schema:** `.claude/skills/story-tree/references/schema.sql`
- **Three-Field System:** `.claude/skills/story-tree/SKILL.md` (stage + hold_reason + disposition)
- **Shared Utilities:** `.claude/skills/story-tree/utility/story_db_common.py` (DB_PATH, etc.)
