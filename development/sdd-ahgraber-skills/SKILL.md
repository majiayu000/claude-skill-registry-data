---
name: sdd
description: |-
  Use when the user wants any spec-driven development action — exploring before speccing, deriving specs from code or translating specs from another system, proposing a change, applying or implementing, verifying, syncing delta specs, or archiving. Triggers: 'spec this out', 'create a change', 'apply tasks', 'verify implementation', 'sync specs', 'archive change', or any mention of 'specs' or 'sdd'.
---

# SDD — Spec Driven Development

Route user intent to the correct `sdd-*` child skill.
Classify first, then confirm with the user before routing.

## Writing Style

Write every SDD artifact in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.
This applies to all `sdd-*` skills.

## Trigger Tests

Should trigger:

- "Spec this feature out"
- "I want to create a change proposal"
- "Apply the tasks in my change"
- "Verify that I implemented everything correctly"
- "Sync the delta specs into main"
- "Archive the auth-refactor change"

Should not trigger:

- "Help me brainstorm"
- "Write a commit message"
- "Debug this Python error"
- "Review my PR"

## Invocation Notice

- Tell the user when this skill is running: `sdd`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## What is a SPECS_ROOT?

A **SPECS_ROOT** is a directory whose direct children conform to the SDD layout: `specs/`, `changes/`, and `schemas/` (with optional `.sdd/`).
The conventional location is a hidden `.specs/` at a project root; in a monorepo, each package may have its own `<package>/.specs/`.

## Locate Specs Root

Before routing, run the discovery script and parse its JSON:

```sh
skills/sdd/scripts/find_specs_roots.py [--explicit PATH]
```

Pass `--explicit PATH` only if the user named a specific directory.
The script anchors at the repo root (or cwd when not in a git repo), discovers `.specs/` candidates, analyzes any `SPECS_ROOT` pointer files, and falls back to `specs/` discovery if no `.specs/` is found.

The agent — not the script — drives the user-facing dialogue.
See `references/find-specs-roots.md` for the **output schema, decision branches, and `SPECS_ROOT` pointer-file format**.

Summary of behavior:

- Multiple `.specs/` candidates → ask which to use.
- Single `.specs/` with a pointer → if multiple targets, list and ask which to use; if one target, follow it once; surface any malformed/broken/out-of-workspace pointer (or a target that exists but lacks the SPECS_ROOT layout — likely the user pointed at the parent of `.specs/` instead of the `.specs/` directory itself) instead of silently falling back.
- No `.specs/` but `specs/` fallback hits → confirm with user (default: parent of `specs/`).
- Nothing found → ask where to initialize.
- Always announce the resolved path; if a pointer was followed, announce both marker and target.

Call the resolved path `SPECS_ROOT`.
All child skills use `SPECS_ROOT` in place of `.specs/`.

## Route by Intent

| User Intent                              | Route           | Notes                  |
| ---------------------------------------- | --------------- | ---------------------- |
| Think before acting, explore ideas       | `sdd-explore`   | Always available       |
| Convert existing specs from another tool | `sdd-translate` | Bootstrap path         |
| Generate specs from codebase analysis    | `sdd-derive`    | Bootstrap or change    |
| Create a change with all artifacts       | `sdd-propose`   | Change path            |
| Implement tasks from tasks.md            | `sdd-apply`     | Requires tasks.md      |
| Verify implementation matches specs      | `sdd-verify`    | Requires active change |
| Merge delta specs into main specs        | `sdd-sync`      | Requires delta specs   |
| Complete and archive a change            | `sdd-archive`   | Requires active change |

## Routing Flowchart

> The chart focuses on intent routing. Discovery details (the `specs/` fallback and `SPECS_ROOT` pointer-file redirect) are described in **Locate Specs Root** above and elided here for readability.

```dot
digraph sdd_router {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10];
    edge [fontname="Helvetica", fontsize=9];

    start [label="User intent", shape=ellipse];
    locate_root [label="Locate SPECS_ROOT\n(.specs/ directories)", shape=box];
    multi_specs [label="Multiple .specs/\nfound?", shape=diamond];
    ask_which [label="Ask user which\nto use", shape=box];

    explore_first [label="Wants to think\nbefore acting?", shape=diamond];
    explore [label="sdd-explore", shape=box];

    has_specs [label="SPECS_ROOT/specs/ exists?", shape=diamond];
    confirm_mode [label="Confirm intent\nwith user", shape=box];

    translate [label="sdd-translate", shape=box];
    derive [label="sdd-derive", shape=box];
    propose [label="sdd-propose", shape=box];

    has_change [label="Active change exists?", shape=diamond];
    which_change [label="Which change?\n(ask if multiple)", shape=box];
    has_tasks [label="tasks.md exists?", shape=diamond];
    stop [label="STOP:\nrun sdd-propose first", shape=octagon, style=filled, fillcolor=red, fontcolor=white];
    apply [label="sdd-apply", shape=box];
    verify [label="sdd-verify", shape=box];
    sync [label="sdd-sync", shape=box];
    archive [label="sdd-archive", shape=box];

    start -> locate_root;
    locate_root -> multi_specs;
    multi_specs -> ask_which [label="yes"];
    multi_specs -> explore_first [label="no (0 or 1)"];
    ask_which -> explore_first;

    explore_first -> explore [label="yes"];
    explore_first -> has_specs [label="no, ready to act"];

    explore -> has_specs [label="crystallized,\nready to act", style=dashed];

    has_specs -> confirm_mode;
    confirm_mode -> translate [label="convert existing specs"];
    confirm_mode -> derive [label="spec from code"];
    confirm_mode -> propose [label="new change"];
    confirm_mode -> has_change [label="apply/verify/\nsync/archive"];
    confirm_mode -> explore [label="think more"];

    has_change -> which_change [label="yes"];
    has_change -> propose [label="no", style=dashed];

    which_change -> has_tasks [label="apply"];
    which_change -> verify [label="verify"];
    which_change -> sync [label="sync"];
    which_change -> archive [label="archive"];

    has_tasks -> apply [label="yes"];
    has_tasks -> stop [label="no"];
}
```

## Routing Rules

1. **Resolve SPECS_ROOT first** — locate `.specs/` before routing; ask if multiple exist or user specifies a path
2. **Classify intent** — explore-or-act, then determine path
3. **Infer mode from directory state** — check `SPECS_ROOT/specs/` existence — but **always confirm with user** before routing
4. **One hard gate** — `sdd-apply` requires `tasks.md` at `SPECS_ROOT/changes/<change-name>/tasks.md`; if missing, stop and route to `sdd-propose`
5. **Prefer minimal next step** — don't run the full pipeline unless requested
6. **Explore is mode-agnostic** — available at every stage, before or after any action
7. **Multiple active changes** — ask which change before routing to apply/verify/sync/archive.
   If `SPECS_ROOT/changes/ORDER.md` exists, list first the changes whose **Starts after** entries are all met (`references/sdd-change-formats.md` § 6).

## Sequence Gates

| Action      | Expected prerequisite                | Warning if missing                                               |
| ----------- | ------------------------------------ | ---------------------------------------------------------------- |
| sdd-apply   | `SPECS_ROOT/changes/<name>/tasks.md` | **Hard block** — "No tasks to implement. Run sdd-propose first." |
| sdd-verify  | Some completed tasks in `tasks.md`   | "No completed tasks yet — verify output will be limited."        |
| sdd-sync    | Delta specs in change directory      | "No delta specs to sync."                                        |
| sdd-sync    | All tasks complete                   | "Incomplete tasks remain. Sync anyway?" (ask user)               |
| sdd-archive | All tasks complete                   | "Incomplete tasks remain. Archive anyway?" (ask user)            |
| design.md   | `proposal.md` exists                 | "Consider writing a proposal first for context."                 |

## Directory Convention

All SDD skills operate on `SPECS_ROOT` — resolved at session start (see **Locate Specs Root** above).
The default is `.specs/` at the project root, but monorepos or user preference may place it elsewhere (e.g., `packages/api/.specs/`, `services/auth/.specs/`).

Child skills replace `.specs/` with `SPECS_ROOT` in all paths.

```text
<SPECS_ROOT>/          # e.g. .specs/ or packages/api/.specs/
├── NORTH-STAR.md                   # Product elevator pitch — durable singleton; change user stories ladder to it
├── specs/                          # Main specs (source of truth)
│   └── <capability>/
│       └── spec.md
├── schemas/                        # Schema snapshots (generated from code)
│   ├── .schema-sources.yaml        # Manifest: generation date and source per schema
│   └── <schema-type>               # e.g., openapi.yaml, db-schema.sql, schema.graphql
├── changes/
│   ├── ORDER.md                    # Optional: order and shared requirements across active changes
│   ├── <change-name>/              # In-progress changes (kebab-case)
│   │   ├── proposal.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   ├── .verify/                # Transient verify scratch (self-gitignored) — test log + report; never committed or archived
│   │   ├── schemas/                # Schema snapshots scoped to this change
│   │   │   ├── before/             # Snapshot taken at propose/derive time
│   │   │   ├── after/              # Snapshot taken at verify time
│   │   │   └── expected.md         # Prose: expected schema changes
│   │   └── specs/                  # Delta specs
│   │       └── <capability>/
│   │           └── spec.md
│   └── archive/                    # Completed changes (schemas travel with change)
│       └── YYYY-MM-DD-<name>/
├── .sdd/                           # SDD tooling metadata
│   ├── schema-config.yaml          # Project schema extraction config
│   └── suggested-tools             # Tracks one-time tool suggestions
```

An **active change** is any directory directly under `SPECS_ROOT/changes/` (not under `archive/`).
Archived changes live in `SPECS_ROOT/changes/archive/YYYY-MM-DD-<name>/`.
Schema snapshots travel with the change directory into the archive — no separate schema archive path is needed.

`changes/ORDER.md` is optional and is not a change.
It records which active changes must wait for others, and which changes edit the same requirement, so that a later sync does not revert an earlier one.
`sdd-propose`, `sdd-apply`, `sdd-sync`, and `sdd-archive` maintain it; `references/sdd-change-formats.md` § 6 defines its format.

Everything in a change directory is durable and committed — proposal, design, tasks, delta specs, and schema snapshots all travel into the archive as the change's record.
The one exception is `.verify/`: run-scoped scratch (the captured test output and any persisted verification report) that `sdd-verify` regenerates on each run.
It is self-gitignored — `sdd-verify` writes a `.gitignore` containing `*` into the directory — so it never enters a commit or the archive.
A verification report is a derived snapshot, not a source of truth: its durable consequences (waivers, overrides, remediation tasks) are written back into `design.md` and `tasks.md`, which are committed.

`NORTH-STAR.md` is the product elevator pitch — a durable, project-global singleton that names the product's reason for being.
It is the apex of the value chain **north star → user story → requirement**: each change's user stories (in `proposal.md`) ladder up to it, and each delta requirement's `Serves:` backlink points at a story.
It is seeded once (see `sdd-propose`) and changes rarely.
Unlike baseline specs, it carries product intent, not contracts — keep it short.

## References

- `references/sdd-spec-formats.md` — baseline spec, delta spec, scenario formats
- `references/sdd-change-formats.md` — proposal, design, tasks, and `ORDER.md` formats
- `references/sdd-schema.md` — schema artifacts and lifecycle policy
- `references/sdd-router.dot` — canonical DOT source for the routing flowchart above
- `references/find-specs-roots.md` — output schema for the discovery script used in **Locate Specs Root**
- `scripts/find_specs_roots.py` — discovery script that resolves `.specs/`, fallback `specs/`, and `SPECS_ROOT` pointer files
- `scripts/check_spec_format.py` — checks a spec's heading structure against `sdd-spec-formats.md` § 3 and § 4; symlinked into `sdd-propose`, `sdd-derive`, `sdd-sync`, and `sdd-translate`
