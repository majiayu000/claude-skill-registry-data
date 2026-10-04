---
name: pipeline-gitlab-incident
description: >
  Incident response pipeline for GitLab repositories using Copilot CLI,
  Jira, and troubleshooter. Takes a Jira incident, investigates root cause,
  optionally fixes via TDD, and reviews the merge request. User decides
  whether to fix or just document findings on the Jira ticket.
  Triggers on: gitlab incident, incident pipeline, troubleshoot gitlab.
disable-model-invocation: true
---

## Pipeline: GitLab Incident Response (Copilot CLI + Jira + Troubleshooter)

```
Jira Incident Ticket
  │
  ├─ 1. troubleshooter (Opus-tier)
  │     Fetch Jira ticket → gather evidence
  │     → ArgoCD status, kubectl logs, App Insights
  │     → Correlate timestamps → root cause diagnosis
  │     → Key findings + next action
  │
  ├─ 2. USER DECISION POINT
  │     ├─ Option A: Document only
  │     │   → Add key findings + next action to Jira ticket
  │     │   → Pipeline ends
  │     │
  │     └─ Option B: Fix the issue
  │         ↓
  │
  ├─ 3. tdd-developer (Sonnet-tier) — per step
  │     Step 1: write test that REPRODUCES the bug (RED)
  │     Step 2+: implement fix (GREEN → REFACTOR)
  │
  ├─ 4. qa (Opus-tier)
  │     Run affected tests → verify fix
  │     Ensure no regressions
  │
  ├─ 5. reviewer (Sonnet-tier) — MR review
  │     Review fix against diagnosis
  │     Verify bug reproduction test exists
  │     🔴 MUST FIX / 🟡 SHOULD FIX / 🟢 SUGGESTION
  │     → User triages
  │
  └─ 6. Create MR + Update Jira
        Push branch → create MR → link to incident ticket
        Transition Jira ticket status
```

### Prerequisites
- GitLab repository with `glab` CLI configured
- Jira MCP server or `jira` CLI configured
- GitHub Copilot CLI installed
- Azure CLI (`az`) for App Insights queries
- `kubectl` contexts configured for EMEA/APAC/NAM clusters

### Usage

#### Step 1: Investigate the incident
```bash
copilot --agent=troubleshooter --prompt "Investigate Jira incident PROJ-456"
```
Troubleshooter produces:
- `docs/context/specs/PROJ-456-bugfix.md` — diagnosis with key findings
- `docs/context/specs/PROJ-456-todo.md` — fix steps (if applicable)

#### Step 2: Decide next action

**Option A — Document only (no code fix needed):**
Add the diagnosis to the Jira ticket as a comment:
```bash
jira issue comment add PROJ-456 --body "## Root Cause Analysis
$(cat docs/context/specs/PROJ-456-bugfix.md)"
```
Pipeline ends here. The key findings and recommended next action are
now on the Jira ticket for the team to review.

**Option B — Fix the issue:**
Continue to Step 3.

#### Step 3: Implement the fix
```bash
copilot --agent=tdd-developer --prompt "Step 1 of PROJ-456-todo.md"
```
Step 1 always reproduces the bug as a failing test.

#### Step 4: Run tests
```bash
copilot --agent=qa --prompt "Run tests for PROJ-456 fix"
```

#### Step 5: Review the fix
```bash
copilot --agent=reviewer --prompt "Review PROJ-456 bugfix MR"
```

#### Step 6: Create MR and update Jira
```bash
glab mr create --title "fix(scope): description" --description "Fixes PROJ-456"
jira issue transition PROJ-456 "In Review"
```

### Troubleshooter Output Format

The troubleshooter produces a structured diagnosis:

```markdown
## Diagnosis: PROJ-456

### Key Findings
1. <finding with evidence>
2. <finding with evidence>

### Scope
<Regional or global? Which clusters affected?>

### Root Cause
<Identified root cause with evidence chain>

### Timeline
<deployment → first error → ticket report>

### Next Action
- [ ] <recommended action — fix, rollback, config change, etc.>

### Evidence
| Source | Region | Finding |
|--------|--------|---------|
| App Insights | EMEA | ... |
| kubectl logs | EMEA | ... |
```

### Notes
- The user decision point is critical — not every incident needs a code fix
- Rollbacks, config changes, or infrastructure fixes may be the right action
- If troubleshooter recommends rollback, do that FIRST before any code fix
- Key findings are always documented regardless of the chosen path
