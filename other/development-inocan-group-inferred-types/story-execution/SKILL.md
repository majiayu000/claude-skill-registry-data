---
name: story-execution
description: Use when user says "implement plan", "implement story", "run plan for [ID]", "start implementation", or asks to implement a planned story - loads TDD implementation plan from .claude/data/plans/, follows RED-GREEN-COMMIT cycles for each task, updates story status through active->reviewing->implemented, verifies acceptance criteria, and outputs implementation report. (project)
disable-model-invocation: true
---

# Story Implementation

Load plan from story-tree database, review critically, implement TDD tasks, report for review.

**Announce:** On activation, say: "I'm using the story-execution skill to implement this plan."

## Mode Detection

**CI Mode** activates when:
- Environment variable `CI=true` is set, OR
- Trigger phrase includes "(ci)" like "implement plan (ci)"

**Interactive Mode** (default): Pause after each batch for human feedback.

## CI Mode Constraints

**CRITICAL for CI Mode - avoid commands requiring approval:**

1. **NEVER read `.db` files with Read tool** - SQLite databases are binary files
2. **NEVER use heredocs** (`<< 'EOF'`) - requires shell approval
3. **NEVER use `timeout` command** - requires shell approval
4. **For database operations:** Write a `.py` script file first, then run it with `python script.py`
5. **For module verification:** Use `python -c "import module; print('OK')"` instead of running modules directly

**Pattern - Database Query:**
```bash
# Step 1: Write the script
Write to .claude/skills/story-execution/temp-query.py

# Step 2: Execute it
python .claude/skills/story-execution/temp-query.py
```

**Pattern - Inline Python (simple one-liners only):**
```bash
python -c "import sqlite3; print(sqlite3.connect('.claude/data/story-tree.db').execute('SELECT id FROM story_nodes LIMIT 1').fetchone())"
```

**Pattern - Module Verification (instead of running module directly):**
```bash
# WRONG - requires approval:
# timeout 5 python -m syncopaid.tracker

# CORRECT - verifies module loads without running:
export PYTHONPATH=src && python -c "import syncopaid.tracker; print('Module loaded successfully')"
```

## CI Mode Pipeline

The CI pipeline has 5 semantically meaningful stages:

```
setup-and-plan → review-plan → decompose → implement → finalize
```

| Stage | Model | Purpose | Output |
|-------|-------|---------|--------|
| setup-and-plan | Bash/Python | Find plan, validate deps | plan_path, story_id |
| review-plan | Sonnet | Review critically, decide proceed/pause | ci-review-result.json |
| decompose | Opus | Assess complexity, split if needed | ci-decompose-result.json |
| implement | Sonnet | Follow plan's TDD steps directly | ci-implement-result.json |
| finalize | Bash/Python | Archive, commit, push, report | - |

### Stage: review-plan

Read the plan and determine if it's ready to implement.

**Output:** `.claude/skills/story-execution/ci-review-result.json`

```json
{
  "outcome": "proceed|pause|proceed_with_review",
  "blocking_issues": [],
  "deferrable_issues": [],
  "notes": "Brief summary of review findings"
}
```

**Outcomes:**
- `proceed`: No issues, implement the plan
- `pause`: Blocking issues found, stop and report
- `proceed_with_review`: Deferrable issues documented, implement but flag for review

### Stage: decompose

Assess plan complexity and split into sub-plans if needed.

**Complexity Levels:**
- `simple`: 1-3 tasks, straightforward changes
- `medium`: 4-6 tasks, moderate complexity
- `complex`: 7+ tasks OR high integration complexity

**Output:** `.claude/skills/story-execution/ci-decompose-result.json`

```json
{
  "complexity": "simple|medium|complex",
  "task_count": 5,
  "implement_plan": ".claude/data/plans/016_configurable-idle-threshold.md",
  "sub_plans_created": [],
  "notes": "Brief explanation"
}
```

**Decomposition Rules:**
1. If complex, split into sub-plans of 3-5 tasks each
2. Name with letter suffixes: 016A_..., 016B_..., 016C_...
3. Implement first sub-plan (A) now, save others for future runs
4. Each sub-plan must be independently implementable

### Stage: implement

Read the plan document directly and follow its TDD steps.

**Output:** `.claude/skills/story-execution/ci-implement-result.json`

```json
{
  "status": "completed|partial|failed",
  "tasks_completed": 5,
  "tasks_total": 5,
  "commits": ["abc1234", "def5678"],
  "notes": "Brief summary of implementation"
}
```

**TDD Discipline:**
1. Follow the plan's test code EXACTLY
2. RED: Write failing test, verify it fails
3. GREEN: Implement code, verify test passes
4. COMMIT: Stage and commit after each task

## Interactive Mode Workflow

### Step 1: Select and Load Plan

Scan `.claude/data/plans/` for earliest sequence-numbered plan file:

```python
python -c "
import os, re, json
plans_dir = '.claude/data/plans'
pattern = re.compile(r'^(\d{3})([A-Z])?_(.+)\.md$')
plans = []
for f in os.listdir(plans_dir):
    m = pattern.match(f)
    if m:
        plans.append({'filename': f, 'path': os.path.join(plans_dir, f), 'sequence': int(m.group(1)), 'letter': m.group(2) or ''})
plans.sort(key=lambda x: (x['sequence'], x['letter']))
print(json.dumps(plans[0] if plans else {'selected': None}))
"
```

**If no plans found:** Output "No plan files available for implementation" and exit.

### Step 2: Review Plan Critically

Load reference: `references/critical-review.md`

- Read the entire plan
- Identify concerns and classify as blocking or deferrable
- If concerns: Raise them before starting
- If no concerns: Create TodoWrite with tasks, proceed to implementation

### Step 3: Implement Tasks (3 at a time)

Load reference: `references/tdd-implementation.md`

For each task:
1. Mark as `in_progress`
2. Follow TDD cycle: RED -> GREEN -> COMMIT
3. Mark as `completed`

### Step 4: Report

When batch complete:
- Show what was implemented
- Display verification output

**Interactive:** Say "Ready for feedback." and wait.
**CI Mode:** Continue to next batch immediately.

### Step 5: Continue or Adjust

Based on feedback:
- Apply requested changes
- Execute next batch
- Repeat until complete

### Step 6: Complete and Verify

Load reference: `references/database-updates.md`

1. Run full test suite
2. Verify acceptance criteria
3. Link commits to story
4. Archive plan file to `.claude/data/plans/implemented/`
5. Update story status

## Database Integration

Load reference: `references/database-updates.md`

**Database:** `.claude/data/story-tree.db`
**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

## When to Stop

- Missing dependencies
- Failed tests that shouldn't fail
- RED phase passes (feature already exists)
- Repeated failures
- Regression detected

**Ask for clarification rather than guessing.** Don't force through blockers.

## Related Skills

- **story-planning:** Creates the plans this skill implements
- **code-verification:** Verifies acceptance criteria after implementation
- **story-tree:** Manages story hierarchy and status
