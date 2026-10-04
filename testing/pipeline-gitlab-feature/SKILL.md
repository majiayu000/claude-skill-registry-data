---
name: pipeline-gitlab-feature
description: >
  Full feature development pipeline for GitLab repositories using
  Copilot CLI agents and Jira integration. Takes a Jira item through
  requirements engineering, test planning, architecture, TDD development,
  testing, and MR review.
  Triggers on: gitlab pipeline, gitlab feature, copilot pipeline.
disable-model-invocation: true
---

## Pipeline: GitLab Feature Development (Copilot CLI + Jira)

```
Jira Ticket
  │
  ├─ 1. requirements-engineer (Opus-tier)
  │     Fetch Jira ticket → analyze → structured requirements
  │     → docs/context/specs/<id>-requirements.md
  │     → User validates requirements
  │
  ├─ 2. qa (Opus-tier) — test planning
  │     Read requirements → create testing plan
  │     → Unit, integration, edge case scenarios
  │     → docs/context/specs/<id>-testplan.md
  │
  ├─ 3. architect (Opus-tier)
  │     Read requirements + test plan → design solution
  │     → docs/context/specs/<id>-spec.md + <id>-todo.md
  │     → User approves plan
  │
  ├─ 4. tdd-developer (Sonnet-tier) — per step
  │     RED: write failing tests → commit
  │     GREEN: minimum code → commit
  │     REFACTOR: improve → commit
  │
  ├─ 5. qa (Opus-tier) — test execution
  │     Run affected unit + integration tests
  │     Report pass/fail with exact errors
  │
  ├─ 6. reviewer (Sonnet-tier) — per-step review
  │     Review code against requirements + conventions
  │     🔴 MUST FIX / 🟡 SHOULD FIX / 🟢 SUGGESTION
  │     → User triages: [F]ix / [T]ech debt / [I]gnore
  │     → Max 3 fix loops per step
  │
  ├─ 7. Create MR (glab mr create)
  │     Push branch → create merge request → link Jira ticket
  │
  └─ 8. diff-reviewer (Opus-tier) — whole-MR diff review
        Review the created MR end-to-end against the Jira AC:
        quality, correctness, logic, conventions, security,
        landmines, best practices
        🔴 CRITICAL / 🟠 MAJOR / 🟡 MINOR / 🟢 NIT + verdict
        → Preview findings + confirm, then post inline comments
          on the diff (and conceptual threads) via glab
```

> **`reviewer` vs `diff-reviewer`:** `reviewer` is the interactive,
> per-step quality gate that runs *during* development (steps 4–6 repeat
> per todo step). `diff-reviewer` runs *once on the finished MR* — it reads
> the whole diff, ranks issues by severity, and posts them back onto the MR
> (after a preview/confirm gate). Step 8 is optional but recommended before
> requesting human review.

### Prerequisites
- GitLab repository with `glab` CLI configured
- Jira MCP server or `jira` CLI configured
- GitHub Copilot CLI installed (`copilot` command available)

### Usage

#### Step 1: Start with a Jira ticket
```bash
copilot --agent=requirements-engineer --prompt "Analyze Jira ticket PROJ-123"
```
Review the generated `docs/context/specs/PROJ-123-requirements.md`.
Validate acceptance criteria and assumptions.

#### Step 2: Create test plan
```bash
copilot --agent=qa --prompt "Create test plan from PROJ-123-requirements.md"
```

#### Step 3: Design the solution
```bash
copilot --agent=architect --prompt "Design solution for PROJ-123 using requirements and test plan"
```
Review the spec and todo. Approve before proceeding.

#### Step 4: Implement step by step
```bash
copilot --agent=tdd-developer --prompt "Step 1 of PROJ-123-todo.md"
```

#### Step 5: Test after each step
```bash
copilot --agent=qa --prompt "Run tests for Step 1 of PROJ-123"
```

#### Step 6: Review after each step
```bash
copilot --agent=reviewer --prompt "Review Step 1 of PROJ-123"
```
Triage findings: [F]ix / [T]ech debt / [I]gnore.

#### Step 7: Create Merge Request
```bash
glab mr create --title "feat(scope): description" --description "Closes PROJ-123"
```
Or use the `/pr` skill for auto-generated MR description.

#### Step 8: Review the merge request (diff-reviewer)
After the MR exists, review the whole diff and post feedback onto it:
```bash
copilot --agent=diff-reviewer --prompt "Review MR !<iid> for PROJ-123"
```
The agent reads the diff (via the `glab-cli` skill) and the linked Jira
ticket's acceptance criteria (via the `ticket` skill), ranks findings
🔴 CRITICAL / 🟠 MAJOR / 🟡 MINOR / 🟢 NIT, then **previews the exact
comments and asks you to confirm** before posting inline discussions +
conceptual threads and recording a verdict (approve / leave + summary
thread). Nothing is posted until you say yes.

### Notes
- Each step can be run independently — agents communicate via `docs/context/specs/` files
- The tdd-developer → qa → reviewer cycle repeats for each step in the todo
- Max 3 fix loops per step, then remaining issues go to tech debt
- All agents use Copilot CLI (`copilot --agent=<name>`)
