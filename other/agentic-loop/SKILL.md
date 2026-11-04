---
name: agentic-loop
description: This skill should be used when the user asks to "start working on issue", "run the agentic loop", "work on issue #N", "start a new task", or "begin the workflow for this issue". Orchestrates the full 9-phase loop from a GitHub Issue to a merged PR using specialized agent roles and artifact-based handoffs.
---

# Skill: agentic-loop

Orchestrates the complete development workflow from a GitHub Issue to a merged PR. Invokes phase skills in sequence, routing through the appropriate profile based on task complexity.

## Prerequisites

- `gh` CLI authenticated and repo on GitHub.
- `git` >= 2.5 (worktree support).
- Issue number available (passed as argument or read from context).
- Plugin installed and `.claude/imat-agentic.local.md` configured (run `/imat-agentic:configure` first if missing).

## Worktree convention

Each issue always runs in its own git worktree — never in the main working tree.

- Worktree path: `../imat-worktrees/issue-<N>-<slug>` (sibling of repo root)
- All subsequent steps execute with `cwd = <worktree-path>`
- Artifacts at `.claude/agentic/issue-<N>-<slug>/` live inside the worktree

## Phase sequence

### Phase 0 — Recall (optional)

If `recall_before_explore: true` in `.claude/imat-agentic.local.md`, invoke `@recall` to search `.claude/knowledge/` for related patterns, ADRs, and solutions before spending tokens on exploration.

Recall results feed directly into Phase 3 as prior knowledge.

### Phase 0.5 — Flow Router

Invoke `@flow-router` to classify the task and select a phase profile:

| Profile | Phases included |
|---|---|
| `full` | Recall → Explore → Clarify → Design → Gate → Implement → Review → Finalize → Capture |
| `balanced` | Explore → Design → Gate → Implement → Review → Finalize → brief Capture |
| `quick` | Recall → (skip Explore) → Design → Gate → Implement → Review → Finalize |
| `trivial` | Implement → harness → Finalize (no explore/design overhead) |
| `review-only` | Review existing changes → Finalize |

The flow router outputs a `profile` and `skipped_phases` list. Use these to gate each subsequent phase.

### Phase 1 — Intake (Orchestrator)

```
gh issue view <N> --json number,title,body,labels
```

Fetch base and create worktree + branch:
```
git fetch origin
git worktree add -b issue-<N>-<slug> ../imat-worktrees/issue-<N>-<slug> origin/main
```

If branch already exists, omit `-b`. Verify with `git worktree list`.

Initialize `.claude/agentic/issue-<N>-<slug>/state.yaml` from `references/templates/state.yaml`. Fill in `task.id`, `task.title`, `task.branch`, `task.worktree`, `task.phase: explore`, `config_used.profile`.

### Phase 2 — Explore (Explorer)

Skip if profile is `quick`, `trivial`, or `review-only`.

Invoke `@codebase-exploration`. Produces `exploration.md`.

### Phase 3 — Clarification (Orchestrator)

After exploration, review `exploration.md` for blocking open questions. If any questions would block design or implementation, surface them to the user via `AskUserQuestion` before proceeding.

Persist answers to `.claude/agentic/issue-<N>-<slug>/clarifications.md` (use `references/templates/clarifications.md`).

Skip if no blocking questions.

### Phase 4 — Architecture Design + Gate (Architect)

Skip if profile is `trivial` or `review-only`.

Invoke `@design-gate`. Produces `plan.md` with a gate verdict.

- `PASS` → continue to Phase 5
- `DISCUSS` → pause and present specific questions to user. Wait for explicit OK.
- `RETHINK` → return to Phase 2 with restrictions noted in `plan.md`. Maximum 2 rethink cycles.

### Phase 5 — Implementation (Implementer)

Skip if profile is `review-only`.

Invoke `@implementation`. Executes each step in `plan.md`, running the harness after each. If PostToolUse hook is active, harness feedback arrives automatically.

### Phase 6 — Code Review (Reviewer)

Invoke `@code-review`. Confidence threshold from config (default: 80).

- `approved` → Phase 7
- `changes_requested` → return to Phase 5. Maximum 2 retry cycles.

### Phase 7 — Finalize (Orchestrator)

From worktree (`cwd = ../imat-worktrees/issue-<N>-<slug>`):

```
git add -A
git commit -m "tipo(scope): descripción en español"
git push -u origin issue-<N>-<slug>
gh pr create --title "<title>" --body "Closes #<N>" --draft
```

Update `state.yaml`: `phase: done`, `status: completed`, `pr.url`.

### Phase 8 — Knowledge Capture (Knowledge)

Skip if profile is `trivial`.

Invoke `@knowledge-capture`. Produces ADRs/patterns if new learning emerged.

## Config defaults (`.claude/imat-agentic.local.md`)

| Key | Default | Description |
|---|---|---|
| `quality_preset` | `sonnet` | Model tier |
| `parallel_explorers` | `2` | Exploration instances |
| `confidence_threshold` | `80` | Review filter (70/80/90) |
| `max_review_retries` | `2` | Review loop cap |
| `harness_profile` | `full` | full / light / off |
| `recall_before_explore` | `true` | Run recall before exploration |
| `auto_advance` | `false` | Skip confirmations (ship-it only) |

## Additional Resources

- **`references/phases.md`** — detailed per-phase instructions and edge cases
- **`references/templates/state.yaml`** — state artifact template
- **`references/templates/clarifications.md`** — clarification artifact template
