---
name: plot
description: >-
  Git-native planning dispatcher. Analyzes current git state and suggests the next action.
  Activates on /plot or when managing planned work through git branches and PRs.
  Spoke commands: /plot-idea, /plot-approve, /plot-deliver, /plot-release.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git and gh CLI.
---

# Plot

Lean, git-native planning system. Plans are markdown files on branches, PRs are workflow metadata, git is the source of truth. Plans merge to main before implementation begins; one plan can spawn multiple parallel implementation branches.

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Archive directory:** docs/archive/

## Lifecycle

### Feature / Bug (full lifecycle)

```mermaid
flowchart LR
    subgraph Planning
        A["/plot-idea"] -->|draft PR| B["Refine &<br/>slice branches"]
        B -->|gh pr ready| C["Review plan"]
    end
    subgraph Approval
        C -->|"/plot-approve<br/>(or PR already merged)"| D["Plan merged<br/>impl PRs created"]
    end
    subgraph Implementation
        D --> E["Work on<br/>impl branches"]
        E -->|"draft → review → merge<br/>(standard code review)"| F["All impls<br/>merged to main"]
    end
    subgraph Delivery
        F -->|/plot-deliver| G["Plan archived"]
    end
    subgraph Release
        G -->|"/plot-release<br/>(1..n delivered plans)"| H["Version bump<br/>changelog, tag"]
    end
```

### Docs / Infra (live when merged)

```mermaid
flowchart LR
    A["/plot-idea<br/>(optional)"] -->|draft PR| B["Refine plan"]
    B -->|"/plot-approve<br/>(if planned)"| C["Impl branch"]
    C -->|"code review<br/>& merge"| D["Merged to main<br/>LIVE"]
    D -->|"/plot-deliver<br/>(if planned)"| E["Plan archived"]

    F["Direct branch<br/>(no plan)"] -->|"code review<br/>& merge"| D
```

### Direct Work (no planning step)

Small features, bug fixes, docs, and infra tasks go directly to a PR:

```
feature/<slug>  →  PR  →  merge
bug/<slug>      →  PR  →  merge
docs/<slug>     →  PR  →  merge
infra/<slug>    →  PR  →  merge
```

## Phases

| Phase | Meaning | Trigger |
|-------|---------|---------|
| Draft | Plan being written/refined | `/plot-idea` |
| Approved | Plan merged, impl branches created | `/plot-approve` |
| Delivered | All impl PRs merged, plan archived | `/plot-deliver` |
| Released | Included in a versioned release | `/plot-release` |

## Conventions

- **Branch prefixes:** `idea/` (plans), `feature/`, `bug/`, `docs/`, `infra/` (implementation)
- **Plan files:** `docs/plans/<slug>.md` — merged to main when approved
- **Archive:** `docs/archive/YYYY-MM-DD-<slug>.md` — dated for chronological sorting
- **Plan PR:** starts as draft (being refined), marked ready with `gh pr ready`, titled `Plan: <title>`
- **Impl PRs:** draft, created by `/plot-approve`, reference the plan on main

## Guardrails

- `/plot-approve` requires plan PR to be non-draft or already merged — no approving unreviewed plans
- `/plot-deliver` requires all impl PRs merged — no premature delivery
- `/plot-release` requires delivered (archived) plans — cannot release undelivered work
- `/plot` detects orphan impl branches (no approved plan) — prevents coding without context
- Phase field in plan files is machine-readable — every command checks current phase before acting

## Dispatcher

The `/plot` command analyzes current git state and suggests the next action.

### Decision Tree

```mermaid
flowchart TD
    Start["/plot"] --> ReadState["Read: current branch,<br/>active plans, open PRs"]
    ReadState --> OnIdea{On idea/* branch?}
    OnIdea -->|yes| PlanDraft["Show plan status<br/>Suggest: refine, gh pr ready,<br/>or /plot-approve"]
    OnIdea -->|no| OnImpl{On impl branch?}
    OnImpl -->|yes| HasPlan{Has approved plan?}
    HasPlan -->|yes| ImplStatus["Show impl PR status<br/>Suggest: keep working,<br/>mark ready, or /plot-deliver"]
    HasPlan -->|no| Orphan["Orphan branch!<br/>Suggest: /plot-idea first"]
    OnImpl -->|no| OnMain{On main?}
    OnMain -->|yes| ListPlans["List active plans +<br/>delivered plans awaiting release<br/>Suggest next action"]
    OnMain -->|no| Other["Show general status"]
```

### 1. Read State

Gather context in parallel:

```bash
# Current branch
BRANCH=$(git branch --show-current)

# Active plans on main
ls docs/plans/*.md 2>/dev/null

# Archived plans
ls docs/archive/*.md 2>/dev/null

# Open PRs on idea/ branches
gh pr list --json number,title,headRefName,isDraft,state --jq '.[] | select(.headRefName | startswith("idea/"))'

# Open PRs on impl branches (feature/, bug/, docs/, infra/)
gh pr list --json number,title,headRefName,isDraft,state --jq '.[] | select(.headRefName | startswith("feature/") or startswith("bug/") or startswith("docs/") or startswith("infra/"))'
```

Also run the bash helpers if a specific slug is in context:
- `./scripts/plot-pr-state.sh <slug>` — plan PR state
- `./scripts/plot-impl-status.sh <slug>` — impl PR states

### 2. Detect Current Context

**If on an `idea/*` branch:**
- Read the plan file from `docs/plans/<slug>.md` on this branch
- Check plan PR state (draft / ready / merged)
- Suggest:
  - If plan PR is draft: "Plan is still a draft. Refine it, then run `gh pr ready <number>` when ready for review."
  - If plan PR is non-draft (ready for review): "Plan is ready for review. Run `/plot-approve <slug>` to merge and create impl branches."
  - If plan PR is merged: "Plan is already approved. Run `/plot-approve <slug>` to create impl branches (if not already created)."

**If on an impl branch (`feature/*`, `bug/*`, `docs/*`, `infra/*`):**
- Check if there's a corresponding approved plan in `docs/plans/<slug>.md` on main
- If plan exists: show impl PR status, suggest keep working / mark ready / `/plot-deliver`
- If no plan exists: warn "Orphan branch — no approved plan found. Consider running `/plot-idea` first."

**If on `main`:**
- List all active plans with their phases
- List any delivered (archived) plans awaiting release
- Show overall status summary
- Suggest next action based on what's pending

**Otherwise:**
- Show general status: active plans, open PRs, recent archives

### 3. Detect Issues

Flag any problems found:

- **Orphan impl branches**: branches with `feature/`, `bug/`, `docs/`, `infra/` prefix that have no corresponding plan in `docs/plans/`
- **Phase mismatches**: plan says Draft but PR is non-draft, or plan says Approved but PR is still open
- **Stale drafts**: impl PRs that have been in draft state for a long time

### 4. Status Summary

Print a clear summary:

```
## Plot Status

### Active Plans
- `<slug>` — Phase: <phase> | Plan PR: #<n> (<state>) | Impl PRs: <count> merged / <count> total

### Issues
- <issue description>

### Suggested Next Step
> <specific command or action>
```
