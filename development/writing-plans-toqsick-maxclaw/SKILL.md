---
name: writing-plans
description: 'Write implementation plans: bite-sized tasks, paths, code.'
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: ['planning', 'design', 'implementation', 'workflow', 'documentation']
    related_skills: ['subagent-driven-development', 'test-driven-development', 'requesting-code-review']
lane: koenigin
reasoning_effort: xhigh
agent: Engineer
routing_hint: |
  **Agent-Scope:** Code-Tasks (build / fix / refactor / debug / review). Off-scope: visual design, long-form copy, data modeling — say 'this is Designer/Writer/Analyst's territory' and return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Writing Implementation Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When to Use

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

## GreyHack Mini-Spec Pattern

For GreyHack tools, write a mini-spec before implementation. The mini-spec should be shorter than a full implementation plan but must include:

- Goal and why this tool is next.
- Exact proposed file path.
- Dependencies and tools to avoid.
- API/function names, inputs, outputs, and error behavior.
- CLI/help/usage behavior.
- Safety boundaries: no real exploit PoCs, credentials, payloads, or external network targets.
- Build/test commands using `./scripts/ci-build.sh --out-dir /tmp/greybel-build ...`.
- Acceptance criteria: builds cleanly, no `main` changes, no unsafe content.

GreyHack branch rule:

- P0 has priority before P1-P4.
- Do not mutate `develop` directly; use a feature branch from `develop`.
- Never merge or touch `main` without explicit user approval.


## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

set -euo pipefail
**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

set -euo pipefail
## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

set -euo pipefail
### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

set -euo pipefail
**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

set -euo pipefail
**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

set -euo pipefail
````

## Writing Process

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use Hermes tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

set -euo pipefail
### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied

### Step 7: Save the Plan

```bash
mkdir -p docs/plans
# Save plan to docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: add implementation plan for [feature]"
```

set -euo pipefail
## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

set -euo pipefail
### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

set -euo pipefail
## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

### Plan-Wordlaut-Treue is a Trap (Path Drift Between Plan and Reality)

When a plan is written, file paths are *predictions*. By execution time (sometimes days later), reality may diverge:

- Skill created at a different path than predicted (`workflow-templates/` → `workflow-template/`)
- Reference file renamed mid-execution (`workflow-templates-standard-X.md` → `workflow-template-skill-X.md`)
- Code refactor moved a function or file mid-stream

**When writing outputs that reference plan-paths (Mnemosyne memories, system docs, code commits, README): trust the executed reality, not the plan text.** The plan is a hypothesis; the filesystem is ground truth.

**Recipe when executing tasks that reference plan-paths:**

1. Verify the actual path before writing the output: `ls -la <actual-path>` or `find ~/.hermes/skills -name "SKILL.md" -path "<pattern>"`
2. If actual differs from plan: use the actual path in the output, and update the plan retroactively with `(korrigiert YYYY-MM-DD)` so plan-history records the drift
3. **Never** copy a wrong path from the plan into Mnemosyne/system-docs — wrong memories poison future recovery silently

**Companion pitfall — `patch(replace_all=true)` on structured file-list blocks destroys verb-prefix structure.** When a plan's Files-list block uses a verb-prefix pattern (`Create:`, `Modify:`, `Read:`, `Test:`), a `replace_all` on a token inside the paths matches every occurrence *including* the verb-prefix line. The result is structurally broken:
```
**Files:**
- `~/.hermes/skills/orchestration/foo/SKILL.md` (was `Create: ...`)
- `~/.hermes/skills/orchestration/foo/README.md` (was `Create: ...`)
- Create: `~/.hermes/skills/orchestration/foo/templates/...md` (preserved)
```
**Recipe:** For token rename across a structured list block, use N separate single-replace patches (one per line), never `replace_all`. Each single-replace has enough context (`Create: \`<path>\``) to be unique; the verb-prefix survives.

**Verified 2026-07-06:** Plan `~/.hermes/plans/2026-07-05_workflow-templates-skill.md` predicted plural path; reality was singular. Mnemosyne memories + system-doc written with actual path; plan retroactively patched. Mnemosyne lookup for `workflow-template standard` resolved correctly on first try. If the plural path had been written into Mnemosyne, skill discovery would silently fail (Mnemosyne's vector recall might still find it by semantic match, but skill_view would 404).

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

When executing, use the `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
