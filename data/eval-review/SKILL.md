---
name: eval-review
description: Review LLM-generated diff classifications for the diffview eval system. Use when the user invokes this skill or pastes yanked case data from evalreview (containing "# Diff Classification Review" header). Evaluates whether classifications accurately help code reviewers, provides pass/fail verdict with detailed critique.
---

# Eval Review

Review diff classification cases to determine if the LLM correctly categorized hunks, identified change type, and told a coherent story.

## Why Classifications Matter

The classification drives a **story-guided review UI** where:

1. **PRs become "pages"** — Each story section is a page showing a subset of hunks with narration
2. **Categories control visibility**:
   - **core** → Shown prominently. Reviewer must see this.
   - **supporting** → Shown de-emphasized. Worth a glance.
   - **noise** → Suppressed. Don't waste reviewer attention.
3. **Narration guides understanding** — Section explanations tell the reviewer what they're looking at and why it matters

**The stakes**: A miscategorized hunk either hides something important (core → noise) or wastes attention on trivia (noise → core). The classifier's job is to help reviewers focus.

## Workflow

1. **Receive case data** — User pastes yanked content from evalreview (`y` key)
2. **Gather context** — Fetch additional context to verify claims
3. **Evaluate** — Apply criteria tables below
4. **Verdict** — Provide pass/fail with actionable critique

## Context Discovery

Before evaluating, gather this context (extract repo, branch, commit hashes from the input):

### 1. Beads Issue (intent)
```bash
bd show <branch>   # e.g., bd show diffview-7yu
```
Gives: Why was this change made? What problem does it solve?

### 2. Full Files at Commit (surrounding code)
```bash
git show <hash>:<filepath>   # e.g., git show abc123:pkg/auth/login.go
```
Gives: See functions around the changed hunks. Is a "systematic" hunk actually changing behavior?

### 3. PR Description (if exists)
```bash
gh pr list --head <branch> --json number,title,body --jq '.[0]'
```
Gives: Author's description of the change, which helps verify summary accuracy.

### 4. Recent History of Changed Files
```bash
git log --oneline -3 <filepath>
```
Gives: Is this a refactor of recent work, or new functionality?

**What each context verifies:**
- Beads issue → change_type, narrative pattern
- Full files → hunk categories (core vs systematic)
- PR description → summary quality
- File history → feature vs refactor distinction

## Evaluation Criteria

### Change Types

| Type | Correct when... | Misapplied when... |
|------|-----------------|-------------------|
| **bugfix** | Removes incorrect behavior or adds missing behavior that should have existed | Adds genuinely new capability (→ feature) |
| **feature** | Adds new capability that didn't exist before | Restructures existing capability (→ refactor) |
| **refactor** | Same behavior, different structure | Behavior actually changes |
| **chore** | Maintenance: deps, CI, build scripts. No functional changes | Includes functional changes |
| **docs** | Only docs/comments change | Code changes accompany doc changes |

### Narratives

| Pattern | Correct when... | Misapplied when... |
|---------|-----------------|-------------------|
| **cause-effect** | Clear problem → solution structure | No identifiable "problem" |
| **core-periphery** | One central change causes ripples | Changes are independent |
| **before-after** | Transformation from old to new pattern | No clear "before" state |
| **rule-instances** | Pattern defined once, applied N times | Each change is unique |
| **entry-implementation** | Public API defined, then implementation | No clear API boundary |

### Hunk Categories

| Category | Correct when... | Dangerous if wrong |
|----------|-----------------|-------------------|
| **core** | Changes program behavior. Must review | Marked systematic → hides bugs |
| **systematic** | Mechanical: renames, params, boilerplate | Marked core → wastes attention |
| **refactoring** | Code moves without behavior change | Behavior actually changes |
| **noise** | Formatting, whitespace only | Real changes hidden |

**Key test**: If skipping could cause a reviewer to miss a bug, it's **core**.

### Beads/Issue Tracker Changes

Beads files (`.beads/`) require special handling based on what they affect:

| Change Scope | Category | UI Treatment | Rationale |
|--------------|----------|--------------|-----------|
| Current issue status/closed | noise | Suppress | Reviewer is already reviewing this work |
| Current issue notes updated | noise | Suppress | Mechanical bookkeeping |
| Dependency edges added/removed | noise | Suppress | Graph maintenance |
| Wiring notes to *other* issues | supporting | Show (de-emphasized) | Documents decisions for future work |
| New issues created | supporting | Show (de-emphasized) | Discovered scope worth noting |

**The rule**: Changes scoped to `<current-branch-id>` → noise. Changes propagating context to other issue IDs → supporting.

**Mixed hunks**: If a beads hunk contains both current-issue bookkeeping and downstream wiring notes, categorize by dominant content. Pure status updates = noise; substantive wiring notes = supporting.

### Section Roles

| Role | Contains... |
|------|-------------|
| problem | What's broken/missing |
| fix | The solution |
| test | Test additions/modifications |
| core | Essential logic changes |
| supporting | Enables but isn't focus (including exceptions to patterns) |
| pattern | Repeatable approach being applied |
| interface | API/interface definitions |
| cleanup | Removing old code |

**Grouping test**: Hunks in a section should be semantically related, not just in the same file.

## Output Format

Use this structured format for consistent, scannable reviews:

```
## Verdict: PASS | FAIL

[One sentence summary of the classification quality]

## Evaluation

### Change Type: [type] — ✓ Correct | ✗ Wrong
[1-2 sentences explaining why this type fits or doesn't fit]

### Narrative: [pattern] — ✓ Correct | ✗ Wrong
[1-2 sentences explaining why this pattern fits or doesn't fit]

### Hunk Assignments
| Hunk | Assigned | Correct? | Issue |
|------|----------|----------|-------|
| file.go:H0 | core | ✓ | — |
| test.go:H0 | test | ✓ | — |
| .beads:H0 | supporting | ✓ | Could argue noise |

### Section Structure
[Are sections well-organized? Do explanations help reviewers?]

## Context Gathered
- `bd show <id>` — [what it revealed]
- `git log <file>` — [what it revealed]
```

**Formatting rules:**
- Use ✓ for correct, ✗ for incorrect
- Keep each evaluation to 1-2 sentences max
- The hunk table should list every hunk with quick assessment
- If FAIL, the "Issue" column should state what it should be
