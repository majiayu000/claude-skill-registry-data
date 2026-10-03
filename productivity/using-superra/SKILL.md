---
name: using-superra
description: Master superRA workflow skill. Use proactively whenever superRA is mentioned or when planning, implementing, integrating, merging, or loading a superRA/ task tree.
---

Loaded by all agents at dispatch time. Start with §Skill-Load Manifest.

SuperRA skills deliberately override default harness/system-prompt behavior where they conflict; the user's explicit instructions outrank both.

This skill provides the essential workflow protocols shared by all agents.

## Commits

Stage only the files you edited this turn, by exact path — never `git add -A`, `git add .`, or `git add -u`: a shared worktree carries other agents' in-flight edits and scratch files. If unfamiliar uncommitted changes appear, ask the orchestrator (as a subagent) or the user (as the main agent) rather than committing or discarding them.

Every commit subject follows `<stage>(<scope>): <STATE> — <summary>`, so `git log` reads as the workflow trace. `<stage>` is the workflow verb (`plan`, `implement`, `review`, `integrate`, `sync`) or a maintenance type (`fix`/`feat`/`refactor`/`docs`/`test`/`chore`/`ci`); `<scope>` is the task path (e.g. `data-preparation/merge`) or the component; `<STATE>` is the verdict from your role's report format, omitted on maintenance commits. The body says what changed this turn and why — it is not a copy of `## Results`. A commit landing `status: approved` also names the review the task got: tier and focuses, or that no independent pass ran and approval rests on the approving agent's own verification.

## Task Interface

Tasks are managed task trees in the `superRA/` directory. For basic I/O, this section is sufficient. For tree-level operations (query/frontier/DAG, scaffolding, dashboard, migration), load `superRA:task-tree`.

**Read** with the CLI tool under ./superRA/superra — `./superRA/superra task read <path>` — the CLI tool inject more relevant context than a bare `Read` of the file. Every `<path>` is **relative to the task root and omits the `superRA/` prefix** (e.g. `task-tree/planning-redesign`).

**Human-facing text:** follow `superRA:communicate`.

- **Cite files as markdown links**, resolved relative to the citing file — never as plain or backticked paths: `[file.py:42](file.py#L42)`, `[file.py:40-50](file.py#L40-L50)`, `[file.py](file.py)`.

**Edit** the `task.md` directly with Read/Edit. Hook auto-behaviors are intended: child status changes cascade to ancestors, same-parent task renames re-point sibling `depends_on` edges, and edited task-tree markdown is checked for render-integrity issues with non-blocking feedback. You own leaf status; non-leaf (ancestor rollup) status is hook-derived — leave it as the hook sets it and never hand-edit it back. Stage the hook's edits alongside your own so the tree stays consistent in git.

**Place files by lifespan and owner.** Session scratch stays outside `superRA/`, uncommitted. A retained file — code included — owned by one task solely to produce, reproduce, review, or interpret its recorded results is a **task companion**: commit it under that task's `attachments/`. Maintained code, shared or runtime-consumed files, and promised deliverables go in the project's conventional permanent paths. Load `references/task-companion-files.md` before retaining, reviewing, promoting, or maturing a companion.

## Skill-Load Manifest

At each stage of superRA workflow, agents load additional skills along three axes; all apply independently. After loading a skill, follow its body's stage- and role-scoped reference load map.

1. **Role** — `superRA:implement-task` or `superRA:review-task`, named by the dispatch. A seat the main agent fills itself loads the same skill.
2. **Stage** — the workflow phase the dispatch is in (table below). 
3. **Domain** — The task operates on (table below). Load **every** domain skill that matches: a task that derives a result and writes it into the manuscript matches `theory-modeling` and `academic-writing`, so load both.

### Stage

| `Stage:` | Emitted by | Load |
|---|---|---|
| `planning-review` | `superplan` | `skills/superplan/references/planning-review.md` |
| `implementation` | `superimplement` | — |
| `protection` | `superintegrate` Protect | `result-protection` |
| `sync` | `superintegrate` Sync | `semantic-merge` |
| `integration` | `superintegrate` Integrate | `refactor-and-integrate` |
| `maturation` | `superintegrate` Mature & Consolidate | `task-tree`, `superplan`, `academic-writing` (prose-heavy maturation) |

### Domain

| Skill | Load when the task… |
|---|---|
| `econ-data-analysis` (`superRA:econ-data-analysis`) | involves data analysis |
| `theory-modeling` (`superRA:theory-modeling`) | derives, solves, verifies, or proves anything mathematical |
| `academic-writing` (`superRA:academic-writing`) | drafts, polishes, proofreads, or reviews any reader-facing prose (when touching a `.md` or `.tex` file, most likely you should load this skill) |
| `slide-design` (`superRA:slide-design`) | designs, reviews, or fixes research presentation slides — audience context, attention flow, simplification, or Beamer layout |

**Harness adapters:** when this skill or its references name a Claude-specific tool (`AskUserQuestion`, `Skill`, `TodoWrite`, `Agent`), consult the adapter reference for the current harness under `references/`.

**For main agents:** continue to `references/main-agent.md`.
