---
name: plan-creation
description: Use when user says "plan story", "create plan", "plan next feature", "create implementation plan", "what's ready to plan", or asks to plan an approved story - looks up approved story-nodes from story-tree database, prioritizes which to plan first, creates detailed TDD-focused implementation plan, and saves to .claude/data/plans/ folder.
disable-model-invocation: true
---

# Plan Creation - TDD Implementation Plan Generator

Generate test-driven implementation plans for approved stories.

**Announce:** On activation, say: "I'm using the plan-creation skill to create the implementation plan."

**Database:** `.claude/data/story-tree.db`
**Plans:** `.claude/data/plans/`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## Design Principles

- **Task Granularity:** Each task = 2-5 minutes of focused work
- **Zero Context:** Assume implementer knows nothing about the codebase
- **Self-Contained:** Every task has exact file paths, complete code, exact commands
- **TDD Discipline:** RED (write failing test) → verify failure → GREEN (minimal impl) → verify pass → COMMIT
- **DRY/YAGNI:** No speculative abstractions, no premature optimization
- **Frequent Commits:** One commit per passing test cycle

## Mode Detection

**CI Mode** activates when:
- Environment variable `CI=true` is set, OR
- Trigger phrase includes "(ci)" like "plan story (ci)"

**CI Mode behavior:**
- No confirmation prompts - use reasonable defaults
- Compact plan template (shorter explanations)
- Skip implementation handoff options
- Structured summary output
- **Linux paths:** `source venv/bin/activate`, forward slashes

**Interactive Mode** (default):
- Pause for confirmation at key decisions
- Verbose plan template with full explanations
- Present implementation handoff options
- **Windows paths:** `venv\Scripts\activate`, backslashes

## Workflow

### Step 1: Query Approved Stories

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
stories = [dict(row) for row in conn.execute('''
    SELECT s.id, s.title, s.description, s.notes, s.project_path,
        (SELECT MIN(depth) FROM story_paths WHERE descendant_id = s.id) as node_depth,
        (SELECT GROUP_CONCAT(ancestor_id) FROM story_paths
         WHERE descendant_id = s.id AND depth > 0) as ancestors,
        (SELECT COUNT(*) FROM story_paths WHERE ancestor_id = s.id AND depth = 1) as child_count
    FROM story_nodes s
    WHERE s.stage = 'planning' AND s.hold_reason IS NULL AND s.terminus IS NULL
    ORDER BY node_depth ASC
''').fetchall()]
print(json.dumps(stories, indent=2))
conn.close()
"
```

### Step 2: Check Dependencies & Score

**Blocker keywords:** "requires", "depends on", "after", "needs", "once X is done"

**Scoring formula:**
```python
score = min(depth, 5) * 0.30 \
      + (1 if description else 0) * 0.25 \
      + (10 - min(len(criteria), 10)) / 10 * 0.20 \
      + (1 if not blocked else 0) * 0.25
```

**Tie-breaker:** Shallower depth -> shorter title -> alphabetical ID

### Step 3: Select Story

- If user specified ID: validate exists and `stage = 'planning'` with no hold_reason/terminus
- Otherwise: select highest-scoring non-blocked story
- **Interactive only:** Confirm selection with user before proceeding

### Step 4: Research Codebase

**Goal:** Gather enough context to write a zero-context plan.

1. **Read the story** - full description, notes, acceptance criteria
2. **Locate affected files** - use `project_path` field or search by keywords
3. **Study existing patterns** - how do sibling features implement similar behavior?
4. **Check technical docs** - `ai_docs/technical-reference.md` for conventions
5. **Understand test patterns** - review existing tests in `tests/` for style

**Code Landmarks** (for targeted reads):
- `src/syncopaid/tracker.py:88-130` - ActivityEvent dataclass
- `src/syncopaid/tracker.py:204-260` - TrackerLoop init
- `src/syncopaid/database.py:1-50` - Schema and imports
- `src/syncopaid/config.py:15-45` - DEFAULT_CONFIG dict

**Research Output:** Before writing the plan, you should know:
- Exact files to create/modify (with line numbers for modifications)
- The function signatures and data structures involved
- How to test this feature (unit test location, fixtures needed)
- Any edge cases mentioned in story notes

### Step 4.5: Assess Complexity

**Goal:** Determine if this story needs a single plan or multiple incremental sub-plans.

**Complexity Indicators:**

| Indicator | Weight |
|-----------|--------|
| New database tables/migrations | +2 each |
| New module file | +1 each |
| UI changes (new dialogs, menus) | +1 each |
| Multiple files modified | +1 per 3 files |
| External dependencies added | +1 each |

**Calculate total score:**
```python
score = (
    new_tables * 2 +
    new_modules * 1 +
    ui_changes * 1 +
    (files_modified // 3) * 1 +
    external_deps * 1
)
```

**Thresholds:**
- **0-2 = LOW** → Single plan file (proceed to Step 5)
- **3-5 = MEDIUM** → 2-4 sub-plans (proceed to Step 4.6)
- **6+ = HIGH** → 4+ sub-plans (proceed to Step 4.6)

**Interactive Mode:** Report complexity assessment and ask for confirmation before proceeding.
**CI Mode:** Auto-decompose based on score.

### Step 4.6: Decompose into Sub-Plans (Medium/High Only)

**Skip this step for LOW complexity stories.**

**Goal:** Break the story into independently verifiable sub-plans, ordered for fail-fast bug discovery.

#### Fail-Fast Ordering Principle

Order sub-plans so each builds on a verified foundation. Errors surface immediately, not 3 steps later.

**Standard layer order:**
1. **Database/Schema** — Schema errors break everything downstream
2. **Core logic modules** — Can be unit tested in isolation
3. **Integration points** — Connect modules, test wiring
4. **UI last** — Depends on all prior layers working

**Example decomposition for "Import Clients & Matters":**
```
045: Database schema (foundation)
046: Folder parser (core logic, testable in isolation)
047: Dialog UI (depends on parser)
048: Menu integration (thin wiring)
049: Time assignment UI (extends feature)
```

#### Sub-Plan Sizing

Each sub-plan should be:
- **LOW complexity** when assessed individually (~15-30 min implementation)
- **2-5 TDD tasks**
- **Independently verifiable** with clear test/verification commands
- **Single responsibility** — one layer or concern per sub-plan

#### Determine Next Sequence Number

Query existing handovers to find next available number:
```bash
ls .claude/data/plans/*.md | tail -5
```

Use the pattern: `NNN_[story-slug]-[component].md`

**Example sequence:**
- `045_import-clients-matters-db-schema.md`
- `046_import-clients-matters-folder-parser.md`
- `047_import-clients-matters-dialog-ui.md`
- `048_import-clients-matters-menu-integration.md`

#### Generate Sub-Plan Outline

Before writing files, outline the decomposition:

```markdown
## Sub-Plan Decomposition

**Story:** [Story Title]
**Complexity Score:** [N] (MEDIUM/HIGH)
**Sub-Plans:** [count]

| # | File | Focus | Dependencies |
|---|------|-------|--------------|
| 045 | ...-db-schema.md | Database tables | None |
| 046 | ...-folder-parser.md | Core logic | 045 |
| 047 | ...-dialog-ui.md | UI component | 045, 046 |
| ... | ... | ... | ... |
```

**Interactive Mode:** Present outline for approval before generating files.
**CI Mode:** Generate all sub-plan files.

### Step 5: Create Plan File(s)

**For LOW complexity:** Single plan file → `.claude/data/plans/NNN_[story-slug].md`

**For MEDIUM/HIGH complexity:** Multiple handover files → `.claude/data/plans/NNN_[story-slug]-[component].md`

Query existing handovers to find next available number:
```bash
ls .claude/data/plans/*.md | tail -5
```

---

> **CRITICAL: Story ID in Header**
>
> Every plan file MUST include the Story ID in the header. Replace `[ID]` with the actual story ID from the database (e.g., `1.2.3`).
>
> The story-execution skill detects "orphan plans" (plans without valid Story IDs) and archives them. Plans missing the Story ID will be skipped during implementation.
>
> Format: `**Story ID:** X.Y.Z` (where X.Y.Z is the story's `id` field from `story_nodes` table)

---

#### LOW Complexity: Single TDD Plan

**Filename:** `.claude/data/plans/NNN_[story-slug].md`
- `NNN` = next available sequence number (e.g., 050, 051)
- `[story-slug]` = title in lowercase-kebab-case (max 40 chars)

#### Interactive Mode Template

```markdown
# [Story Title] - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:implementing-plans to implement this plan task-by-task.

**Story ID:** [ID] | **Created:** [YYYY-MM-DD] | **Stage:** `planned`

---

**Goal:** [One-sentence summary of what this achieves]
**Approach:** [2-3 sentences on technical approach]
**Tech Stack:** [Key modules/libraries involved]

---

## Story Context

**Title:** [title]
**Description:** [description]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Notes:** [Any notes from story]

## Prerequisites

- [ ] Virtual environment activated: `venv\Scripts\activate`
- [ ] Dependencies installed
- [ ] Related stories completed: [list or "None"]
- [ ] Baseline tests pass: `python -m pytest -v`

## Files Affected

| File | Change Type | Purpose |
|------|-------------|---------|
| `tests/test_x.py` | Create | Unit tests for feature |
| `src/syncopaid/x.py` | Modify | Core implementation |

## TDD Tasks

### Task 1: [Descriptive Name] (~N min)

**Files:**
- Create: `path/to/file.py`
- Modify: `path/to/existing.py:123-145`
- Test: `tests/path/to/test.py`

**Context:** [Why this task exists and what it enables for subsequent tasks]

**Step 1 - RED:** Write failing test
```python
# tests/test_x.py
def test_behavior():
    """[What this test verifies]"""
    result = module.func(input)
    assert result == expected
```

**Step 2 - Verify RED:**
```bash
pytest tests/test_x.py::test_behavior -v
```
Expected: `FAILED` - test fails because [specific reason]

**Step 3 - GREEN:** Write minimal implementation
```python
# src/syncopaid/x.py (lines 45-60)
def func(input):
    """[Brief docstring]"""
    return result
```

**Step 4 - Verify GREEN:**
```bash
pytest tests/test_x.py::test_behavior -v
```
Expected: `PASSED`

**Step 5 - COMMIT:**
```bash
git add tests/test_x.py src/syncopaid/x.py && git commit -m "feat: add behavior"
```

---

### Task 2: [Next Task] (~N min)

[Repeat structure...]

---

## Verification Checklist

- [ ] All new tests pass
- [ ] All existing tests pass: `python -m pytest -v`
- [ ] Module runs without error: `python -m syncopaid.[module]`
- [ ] Manual verification: [specific checks]

## Rollback Plan

If issues arise:
1. `git revert HEAD~N` (where N = number of commits)
2. [Any cleanup steps]

## Implementation Notes

[Edge cases, gotchas, future considerations]

## Implementation Handoff

Plan complete and saved to `.claude/data/plans/[filename]`.

**Two implementation options:**

**1. Subagent-Driven (this session)**
- I dispatch fresh subagent per task
- Code review between tasks
- Fast iteration with quality gates
- **REQUIRED SUB-SKILL:** superpowers:subagent-driven-development

**2. Parallel Session (separate)**
- Open new Claude Code session in this directory
- Batch implementation with checkpoints
- **REQUIRED SUB-SKILL:** superpowers:implementing-plans

**Which approach?**
```

#### CI Mode Template (Compact, Self-Contained)

```markdown
# [Story Title] - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:implementing-plans to implement this plan task-by-task.

**Story ID:** [ID] | **Created:** [YYYY-MM-DD] | **Stage:** `planned`

> **TDD Required:** Each task (~2-5 min): Write test → verify RED → Write code → verify GREEN → Commit
> **Zero Context:** This plan assumes the implementer knows nothing about the codebase.

---

**Goal:** [One sentence - what user-visible outcome does this achieve?]
**Approach:** [2-3 sentences on technical approach]
**Tech Stack:** [Modules/libraries involved]

---

## Story Context

**Title:** [title]
**Description:** [description]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Prerequisites

- [ ] venv activated: `source venv/bin/activate`
- [ ] Module importable: `pip install -e .` (if not already installed)
- [ ] Baseline tests pass: `python -m pytest -v`

## TDD Tasks

### Task 1: [Descriptive Name] (~N min)

**Files:**
- Create: `tests/path/test_x.py`
- Modify: `src/path/x.py:123-145`
- Test: `tests/path/test_x.py`

**Context:** [1-2 sentences: why this task exists, what it enables]

**Step 1 - RED:** Write failing test
```python
# tests/path/test_x.py
def test_behavior():
    """[What this test verifies]"""
    result = module.func(input)
    assert result == expected
```

**Step 2 - Verify RED:**
```bash
pytest tests/path/test_x.py::test_behavior -v
```
Expected output: `FAILED` (test should fail because [reason])

**Step 3 - GREEN:** Write minimal implementation
```python
# src/path/x.py (lines 123-145)
def func(input):
    """[Brief docstring]"""
    return result
```

**Step 4 - Verify GREEN:**
```bash
pytest tests/path/test_x.py::test_behavior -v
```
Expected output: `PASSED`

**Step 5 - COMMIT:**
```bash
git add tests/path/test_x.py src/path/x.py && git commit -m "feat: [message]"
```

---

### Task 2: [Next Task Name] (~N min)

[Repeat same structure...]

---

## Final Verification

Run after all tasks complete:
```bash
python -m pytest -v                    # All tests pass
python -m syncopaid.[module]           # Module runs without error
```

## Rollback

If issues arise: `git log --oneline -10` to find commit, then `git revert <hash>`

## Notes

[Edge cases discovered, follow-up work, dependencies on other stories]
```

**Quality Requirements (both modes):**
- **Exact file paths** with line numbers where modifying existing code
- **Complete code** - copy-paste ready, not "add validation here"
- **Exact commands** with expected output (not "run tests")
- **Zero ambiguity** - implementer makes no decisions, just implements
- **Zero context assumption** - explain why, not just what

**CI Mode Autonomy:**
In CI mode, the plan must be implementable without human guidance:
- No "choose between A or B" - make the decision in the plan
- No "verify manually" - provide automated verification commands
- No "ask if unclear" - the plan IS the clarity

---

#### MEDIUM/HIGH Complexity: Incremental Sub-Plans

**Output path:** `.claude/data/plans/NNN_[story-slug]-[component].md`

Each sub-plan is a focused, independently verifiable unit. Use this template:

```markdown
# NNN: [Story Title] - [Component Name]

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:implementing-plans to implement this plan task-by-task.

**Story ID:** [ID] | **Created:** YYYY-MM-DD | **Stage:** `planned`

## Task
[One sentence describing what this sub-plan accomplishes]

## Context
[2-3 sentences explaining why this component exists and how it fits the larger story]

**Design principle**: [Key architectural decision or constraint]

## Scope
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

## Key Files

| File | Purpose |
|------|---------|
| `path/to/file.py` | Brief description |
| `path/to/other.py:45-60` | Line-specific modification |

## Implementation Details

[Technical specification with code snippets, data structures, function signatures]

```python
# Example code block showing exact implementation
def function_name():
    pass
```

## Verification

```bash
source venv/bin/activate

# Test command 1
[command]
# Expected: [output]

# Test command 2
[command]
# Expected: [output]
```

## Dependencies
- Task NNN-1 (component name) should be complete first

## Next Task
After this: `NNN+1_[story-slug]-[next-component].md`
```

**Sub-Plan Quality Requirements:**
- Each sub-plan is **LOW complexity** when assessed individually
- **Clear dependencies** — explicitly list which prior sub-plans must complete first
- **Independent verification** — each sub-plan has its own test commands
- **Fail-fast order** — database → core logic → integration → UI
- **Link chain** — each sub-plan references the next in "Next Task" section

### Step 6: Update Stage

**For LOW complexity (single plan):**
```python
python -c "
import sqlite3
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET stage = 'implementing',
        notes = COALESCE(notes || chr(10), '') || 'Plan: .claude/data/plans/[FILENAME]',
        updated_at = datetime('now')
    WHERE id = '[STORY_ID]'
''')
conn.commit()
conn.close()
"
```

**For MEDIUM/HIGH complexity (sub-plans):**
```python
python -c "
import sqlite3
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET stage = 'implementing',
        notes = COALESCE(notes || chr(10), '') || 'Sub-plans: .claude/data/plans/[START]-[END]_[slug]*.md',
        updated_at = datetime('now')
    WHERE id = '[STORY_ID]'
''')
conn.commit()
conn.close()
"
```

### Step 7: Implementation Handoff (Interactive Only)

**Skip this step in CI mode.**

**For LOW complexity (single plan):**

Present two options:

**Option 1: Continue in this session** - Implement with tight feedback loops, interactive course correction

**Option 2: Fresh session** - Open new Claude Code session, say "Implement plan: .claude/data/plans/[filename]"

**For MEDIUM/HIGH complexity (sub-plans):**

Present sub-plan implementation order:

```
## Implementation Order

Complete sub-plans sequentially. Verify each before proceeding to next.

1. Implement: .claude/data/plans/045_[slug]-db-schema.md
   Verify: [verification command]

2. Implement: .claude/data/plans/046_[slug]-core-logic.md
   Verify: [verification command]

[... continue for all sub-plans ...]
```

**Option 1: Continue in this session** - Implement sub-plans sequentially with verification between each

**Option 2: Fresh session per sub-plan** - Each sub-plan in a new session for clean context

## Remember

When generating plans, always:
- **Exact file paths** - never "somewhere in src/"
- **Complete code** - not "add validation" but the actual validation code
- **Exact commands with expected output** - not just "run tests"
- **DRY, YAGNI, TDD** - test first, minimal code, frequent commits
- **One action per step** - each step takes 2-5 minutes max
- **Reference relevant skills** - use @ syntax for skill references

## Output Format

**CI Mode - LOW complexity Success:**
```
✓ Planned story [STORY_ID]: [Title]
  Complexity: LOW (score [N])
  Plan: .claude/data/plans/[filename].md
  Tasks: [N] TDD cycles
  Stage: planning -> implementing
```

**CI Mode - MEDIUM/HIGH complexity Success:**
```
✓ Planned story [STORY_ID]: [Title]
  Complexity: [MEDIUM|HIGH] (score [N])
  Sub-plans: [count] files
    - .claude/data/plans/[NNN]_[slug]-[component].md
    - .claude/data/plans/[NNN+1]_[slug]-[component].md
    - ...
  Implementation order: [NNN] → [NNN+1] → ... → [NNN+M]
  Stage: planning -> implementing
```

**CI Mode - No stories:**
```
✓ No planning stories available for planning
```

**Interactive Mode:** Conversational summary with handoff options.

## Quality Checks

Before completing the workflow, verify:
- [ ] All approved stories were fetched and analyzed
- [ ] Priority scoring was applied correctly
- [ ] Each task has exactly 5 steps: test, verify fail, implement, verify pass, commit
- [ ] All code examples are complete and copy-paste ready
- [ ] All commands include expected output
- [ ] No vague instructions like "add validation" or "handle errors"
- [ ] Implementation handoff options are presented at end (Interactive mode only)

## Common Mistakes

| Mistake | What To Do Instead |
|---------|-------------------|
| Using `sqlite3` CLI | Use Python's sqlite3 module |
| Writing multi-step tasks | Break into single-action steps (test/verify/implement/verify/commit) |
| Omitting expected output | Every command needs "Expected: [what success looks like]" |
| Vague code examples | Write complete, copy-paste ready code |
| Skipping implementation handoff | Always offer subagent-driven vs parallel session choice (Interactive mode) |
| Large commits at end | Commit after each task (RED-GREEN-REFACTOR cycle) |
