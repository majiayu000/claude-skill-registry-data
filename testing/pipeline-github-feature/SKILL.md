---
name: pipeline-github-feature
description: >
  Feature development pipeline for GitHub repositories using Claude LLMs.
  Requirements engineer takes input from specs.md or user, creates a GitHub
  issue as feature request, then architect plans, tdd-developer implements,
  qa tests, and reviewer peer-reviews the pull request.
  Triggers on: github pipeline, github feature, claude pipeline, specs pipeline.
disable-model-invocation: true
---

## Pipeline: GitHub Feature Development (Claude LLMs)

```
specs.md / User Input
  │
  ├─ 1. requirements-engineer (Opus-tier)
  │     Read specs.md or user input → structured requirements
  │     → docs/context/specs/<id>-requirements.md
  │     → User validates requirements
  │
  ├─ 2. Create GitHub Issue
  │     Format requirements as feature request issue
  │     → gh issue create --title "..." --body "..."
  │     → Issue number becomes the tracking ID
  │
  ├─ 3. architect (Opus-tier)
  │     Read requirements → design solution
  │     → docs/context/specs/<id>-spec.md + <id>-todo.md
  │     → User approves plan
  │
  ├─ 4. tdd-developer (Sonnet-tier) — per step
  │     RED: write failing tests → commit
  │     GREEN: minimum code → commit
  │     REFACTOR: improve → commit
  │
  ├─ 5. qa (Opus-tier)
  │     Run affected unit + integration tests
  │     Report pass/fail with exact errors
  │
  ├─ 6. reviewer (Sonnet-tier) — per-step review
  │     Review code against requirements + conventions
  │     🔴 MUST FIX / 🟡 SHOULD FIX / 🟢 SUGGESTION
  │     → User triages: [F]ix / [T]ech debt / [I]gnore
  │     → Max 3 fix loops per step
  │
  ├─ 7. Create Pull Request (gh pr create)
  │     Push branch → create PR → link GitHub issue
  │     → "Closes #<issue-number>"
  │
  └─ 8. diff-reviewer (Opus-tier) — whole-PR diff review
        Review the created PR end-to-end against the issue's AC:
        quality, correctness, logic, conventions, security,
        landmines, best practices
        🔴 CRITICAL / 🟠 MAJOR / 🟡 MINOR / 🟢 NIT + verdict
        → Preview findings + confirm, then post inline comments
          on the diff (and conceptual threads) via gh
```

> **`reviewer` vs `diff-reviewer`:** `reviewer` is the interactive,
> per-step quality gate that runs *during* development (steps 4–6 repeat
> per todo step). `diff-reviewer` runs *once on the finished PR* — it reads
> the whole diff, ranks issues by severity, and posts them back onto the PR
> (after a preview/confirm gate). Step 8 is optional but recommended before
> requesting human review.

### Prerequisites
- GitHub repository with `gh` CLI configured
- Claude Code installed (agents run as Claude Code subagents)
- Optional: `specs.md` in repo root or provided path

### Usage

#### Step 1: Gather requirements

**From specs.md:**
```
Use requirements-engineer to analyze specs.md
```
The agent reads `specs.md` (or a specific path), extracts features,
and produces structured requirements.

**From user input:**
```
Use requirements-engineer: "We need user authentication with OAuth2,
supporting Google and GitHub providers, with role-based access control"
```

Review the generated `docs/context/specs/<id>-requirements.md`.
Validate acceptance criteria and assumptions.

#### Step 2: Create GitHub issue
```bash
gh issue create \
  --title "feat: <feature name>" \
  --body "$(cat docs/context/specs/<id>-requirements.md | head -n 100)" \
  --label "feature-request"
```
Or let the requirements-engineer format and create the issue directly:
```
Use requirements-engineer to create a GitHub issue from <id>-requirements.md
```

#### Step 3: Design the solution
```
Use architect to design the solution for <id>-requirements.md
```
Review the spec and todo. Approve before proceeding.

#### Step 4: Implement step by step
```
Use tdd-developer on Step 1 of <id>-todo.md
```

#### Step 5: Test after each step
```
Use qa to verify Step 1
```

#### Step 6: Review after each step
```
Use reviewer to review Step 1
```
Triage findings: [F]ix / [T]ech debt / [I]gnore.

#### Step 7: Create Pull Request
```
/pr
```
Or manually:
```bash
gh pr create \
  --title "feat(scope): description" \
  --body "Closes #<issue-number>"
```

#### Step 8: Review the pull request (diff-reviewer)
After the PR exists, review the whole diff and post feedback onto it:
```
Use diff-reviewer to review PR #<number>
```
The agent reads the diff (via the `gh-cli` skill) and the linked issue's
acceptance criteria, ranks findings 🔴 CRITICAL / 🟠 MAJOR / 🟡 MINOR /
🟢 NIT, then **previews the exact comments and asks you to confirm** before
posting inline comments + conceptual threads and submitting a verdict
(APPROVE / REQUEST_CHANGES / COMMENT). Nothing is posted until you say yes.

### specs.md Format

The requirements-engineer can process any structured document, but
the recommended `specs.md` format is:

```markdown
# Feature: <name>

## Problem
<what problem does this solve?>

## Users
<who benefits?>

## Requirements
- <requirement 1>
- <requirement 2>

## Constraints
- <technical or business constraints>

## Notes
- <additional context, references, prior art>
```

### Notes
- All agents run as Claude Code subagents (not Copilot CLI)
- The requirements-engineer → GitHub issue step ensures traceability
- The tdd-developer → qa → reviewer cycle repeats for each step in the todo
- Max 3 fix loops per step, then remaining issues go to tech debt
- GitHub issue is linked in the PR via "Closes #N" convention
