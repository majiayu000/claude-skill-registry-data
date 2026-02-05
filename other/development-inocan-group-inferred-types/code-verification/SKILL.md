---
name: code-verification
description: Use when user says "verify code", "check acceptance criteria", "is story ready", or when a story at verifying stage needs execution-based verification - runs tests, checks acceptance criteria, verifies user journeys, generates pass/fail report with evidence, and updates story status.
---

# Code Verification - Execution-Based Testing

Verify that implemented code works correctly by **running the software** and observing behavior.

> **Critical Distinction:** This is verification (execution), not review (inspection) or validation (judgment).
> See `CLAUDE.md` section "Quality Assurance Terminology" for definitions.

**Announce:** On activation, say: "I'm using the code-verification skill to verify the implementation meets acceptance criteria."

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## Purpose

Bridge the gap between `verifying` and `implemented` stages by **executing tests and observing behavior**. This prevents incomplete implementations from being marked implemented. Stories transition: `stage='verifying'` -> `stage='implemented'` -> `stage='ready'`.

## Verification Phases

Verification covers four areas:

| Phase | What It Checks | Method |
|-------|---------------|--------|
| **1. Test Suite** | Unit/integration tests pass | Run pytest |
| **2. Acceptance Criteria** | Each criterion satisfied | Evidence gathering |
| **3. User Journeys** | Complete workflows work | E2E execution |
| **4. Sibling Integration** | No regressions in related stories | Cross-story tests |

All four phases must pass for full verification.

## Mode Detection

**CI Mode** activates when:
- Environment variable `CI=true` is set, OR
- Trigger phrase includes "(ci)" like "verify code (ci)"

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
      AND s.hold_reason IS NULL AND s.terminus IS NULL
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
python .claude/skills/code-verification/parse_criteria.py <story_id>
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
python .claude/skills/code-verification/find_evidence.py test "<criterion_text>" [project_path]
```

Look for:
- Test files that cover the criterion
- Assertions that validate the behavior
- Test names that match criterion keywords

#### 3b. Search for Implementation Code

```bash
python .claude/skills/code-verification/find_evidence.py code "<criterion_text>" [project_path]
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

### Step 5: Generate Verification Report

```bash
python .claude/skills/code-verification/generate_report.py <story_id>
```

**Report format:**
```
CODE VERIFICATION REPORT
========================

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
python .claude/skills/code-verification/update_status.py <story_id> <new_stage> "<verification_notes>"
```

### Step 7: Update Acceptance Criteria Checkboxes

For criteria that PASS, mark them as checked:

```bash
python .claude/skills/code-verification/update_status.py <story_id> mark-criteria 1,2,3
```

### Step 8: Verify User Journeys

If the story description includes user journeys (workflows), verify each by execution:

**Identify journeys in description:**
- Look for sections titled "User Journey", "Workflow", or "Steps"
- Look for numbered step sequences

**For each journey:**
1. Set up preconditions (required state)
2. Execute each step in sequence
3. Assert expected outcome at each step
4. Confirm final goal is achieved

**Journey verification checklist:**
- [ ] All steps execute without errors
- [ ] Intermediate states are correct
- [ ] Final goal is achieved
- [ ] No side effects on unrelated data

See `references/user-journey-testing.md` for detailed patterns.

### Step 9: Test Sibling Integration

Verify the story works correctly alongside its siblings:

**Find sibling stories:**

```sql
-- Siblings = stories with same parent that are already implemented
SELECT id, title FROM story_nodes
WHERE parent_id = (SELECT parent_id FROM story_nodes WHERE id = :story_id)
  AND id != :story_id
  AND stage IN ('implemented', 'released')
```

**Integration checks:**
1. **Shared resources** - No conflicts in database, config, files
2. **Data flow** - Data passes correctly between features
3. **Regression tests** - Existing sibling tests still pass

See `references/integration-testing-siblings.md` for detailed patterns.

## Output Format

### Full Verification Report (YAML)

```yaml
verification_report:
  story_id: "1.2.3"
  title: "Feature Title"
  verified_at: "2025-12-29T10:30:00Z"

  test_suite:
    executed: true
    passed: 42
    failed: 0
    skipped: 3

  acceptance_criteria:
    - criterion: "User can export data as CSV"
      status: pass
      evidence: "tests/test_export.py::test_csv_format passed"
    - criterion: "Export includes timestamps"
      status: pass
      evidence: "Verified timestamp column in output"

  user_journeys:
    - journey: "Export monthly report"
      status: pass
      steps_completed: 5/5
    - journey: "Filter and export"
      status: pass
      steps_completed: 3/3

  integration:
    sibling_stories_tested: ["1.2.1", "1.2.2"]
    regressions: none

  overall: pass  # pass | fail
```

### CI Mode Output (JSON)

**Success:**
```json
{
  "story_id": "1.7",
  "title": "Privacy & Data Security",
  "previous_status": "verifying",
  "new_status": "implemented",
  "test_suite": {"passed": 12, "failed": 0},
  "criteria_results": [
    {"criterion": "...", "status": "PASS", "evidence": "..."}
  ],
  "summary": {"passed": 5, "failed": 0, "untestable": 0},
  "recommendation": "IMPLEMENTED"
}
```

**Failure:**
```json
{
  "story_id": "1.7",
  "previous_status": "verifying",
  "new_status": "verifying",
  "test_suite": {"passed": 10, "failed": 2},
  "criteria_results": [
    {"criterion": "...", "status": "FAIL", "reason": "No implementation found"}
  ],
  "summary": {"passed": 3, "failed": 2, "untestable": 0},
  "recommendation": "NEEDS_WORK",
  "failures": ["Test: test_export_format", "Criterion 2: ..."]
}
```

## Evidence Collection

Verification requires evidence for human review. See `references/evidence-collection.md` for complete patterns.

**Minimum evidence per criterion:**
- Test file and function that validates it
- Code location implementing the behavior
- Pass/fail result with timestamp

## Exit Conditions

| Result | Transition |
|--------|------------|
| All phases pass | -> Update stage to `implemented` |
| Any phase fails | -> Keep at `verifying`, set `hold_reason='escalated'` |

## Do NOT

- Conflate with code review (inspection-based) - that's `code-review` skill
- Conflate with validation (human judgment) - that's `human-validation` skill
- Include retry loops or debug ladders - that's `debug-orchestrator` skill
- Skip running tests - verification requires execution

## References

### Skill Files
- **Parser:** `.claude/skills/code-verification/parse_criteria.py`
- **Evidence Finder:** `.claude/skills/code-verification/find_evidence.py`
- **Report Generator:** `.claude/skills/code-verification/generate_report.py`
- **Status Updater:** `.claude/skills/code-verification/update_status.py`

### Research Documentation
- **Acceptance Testing:** `references/acceptance-testing-best-practices.md`
- **User Journey Testing:** `references/user-journey-testing.md`
- **Integration Testing:** `references/integration-testing-siblings.md`
- **Evidence Collection:** `references/evidence-collection.md`

### External References
- **Database:** `.claude/data/story-tree.db`
- **Schema:** `.claude/skills/story-tree/references/schema.sql`
- **Three-Field System:** `.claude/skills/story-tree/SKILL.md`
- **QA Terminology:** `CLAUDE.md` (Quality Assurance Terminology section)
