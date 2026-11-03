---
name: development-plan
description: Tech Lead-posture skill for ongoing work. Reads change_spec.md + change_design.md + docs/adr/ + docs/fdr.md + docs/nfdr.md + the parts table of docs/SDD.md § 3, critically reviews the design against the spec, puts each new piece of logic in the task for the part that owns it, and produces tl_instruction.md — a scaffold the developer implements from failing tests.
license: MIT
metadata:
  version: "3.0.0"
  category: planning
  risk: safe
---

# Development Plan

## Purpose

Read `change_spec.md` (what was asked), `change_design.md` (the design delta), `docs/adr/` (the decision log — why the system is shaped as it is), `docs/fdr.md` (the behavioural contract, if it exists), `docs/nfdr.md` (the constraint set — the module set and its import graph, § 1.2), and `docs/SDD.md` § 3 (the parts table — which part owns which logic), then produce `tl_instruction.md` — a **scaffold** the developer implements from failing tests.

**This file says how the run reaches its inputs. How the plan is made is
`<CORE>/prompts/tech_lead_create_tl_instruction.md`** — the planning body this skill shares with
`ad-hoc-plan`, which reaches the same point from a brief instead. Read it in full and follow it once
§ *Enter the worktree* below has `$WORKTREE`. None of it is restated here.

## When to Use

- `development-design` has produced `change_design.md` in `system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/` (the records under `docs/adr/`, `docs/nfdr.md` and `docs/SDD.md` are used when present, but are not required — see the shared body's § *Pre-flight — Read decision files*)
- A `tl_instruction.md` is needed
- `development-plan` is explicitly requested

## Enter the worktree

development-specs created an isolated worktree for this change and landed the spec arc on the branch — it is **not** on `main`. development-design then committed `change_design.md` there. Before reading anything, derive the worktree from the **change key** and operate inside it for the whole run.

The **change key** is `<YYYY-MM-DD>_<slug>` — the Tobiishi folder (`journey/tobiishi/<key>/`) / branch name. You know it from the invocation (the change you were asked to plan). If multiple worktrees exist under `<repo>/.worktrees/` and the intended change is ambiguous, ask which one — once.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE="$REPO_ROOT/.worktrees/<key>"
test -d "$WORKTREE" || echo "No worktree for <key> — development-specs must run first."
```

If `$WORKTREE` does not exist, **STOP**: the upstream stages have not run for this change. Do not create it here and do not fall back to `main`.

**From here on, the worktree is the working root:** read every input from `$WORKTREE/` (`change_spec.md`, `change_design.md`, and the decision files), write `tl_instruction.md` under `$WORKTREE/`, and commit with `git -C "$WORKTREE"`. The change arc stays on the branch, never `main`. The path is derived from the key alone — identical convention to development-specs Step 4, development-design, and `ad-hoc-plan`; nothing is handed between sessions.

## Then plan

Follow `<CORE>/prompts/tech_lead_create_tl_instruction.md` from § *Resolve the product* to its
Step 4, with `--skill development-plan` at the commit. The skill is done when that commit lands.

## Critical Rules

- **The worktree is upstream's.** If `$WORKTREE` is absent, STOP — do not create it and do not fall
  back to `main`.
- **The planning rules are the shared body's.** Every other rule this run follows is
  `<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Critical Rules*.
