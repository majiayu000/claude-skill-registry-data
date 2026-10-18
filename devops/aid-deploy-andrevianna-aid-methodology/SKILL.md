---
name: aid-deploy
description: >
  Package completed deliveries into a release. Use when deliveries are complete and ready to
  ship. It selects the eligible deliveries, verifies the combined build, packages according
  to the project's own infrastructure, generates the release notes, and updates each
  artifact's status.
allowed-tools: Read Glob Grep Bash Shell Terminal Write
---

# Package & Ship

State machine: IDLE → SELECTING → VERIFYING → PACKAGING → DONE.

Package completed deliveries into a release.

## Agents Involved

- **Default executor:** `aid-operator` (orchestrates the release: verifies build, packages artifacts, updates statuses).
- **Specialist consults (optional):** `aid-tech-writer` for release notes / changelog, `aid-operator` if CI/CD configuration changes are needed during release, `aid-reviewer` for final pre-release verification.

## Argument-Hint

```
/aid-deploy work-NNN
/aid-deploy "<free-form description of what to ship>"
```

**Two invocation modes** (invocation-context detection; see `## ⚠️ Pre-flight Checks`
Step 0):

- **`work-NNN` present** -- the existing pipeline path below runs unchanged
  (`IDLE -> SELECTING -> VERIFYING -> PACKAGING -> DONE`, post-Execute). Required: work
  ID. If only one work exists, auto-select it.
- **No `work-NNN`, a free-form description instead** -- the Lite-path direct-entry
  shortcut: binds `{name}=aid-deploy`, `{verb}=deploy`, `{artifact}=""` (bare verb),
  `{description}=<the given text>`, then delegates to the shared shortcut engine
  (`.aid/runtime/templates/shortcut-engine.md`, `INTAKE -> ... -> APPROVAL-HALT`),
  scaffolding a flattened Lite work and running the grading gates. **Never executes** --
  it halts for approval; this shortcut entry does not replace the pipeline role below,
  it adds a second, independent entry point to the same skill directory.

## Workspace

```
.aid/
  knowledge/
    STATE.md                   ← Q&A, Review History (settings → .aid/settings.yml), Q&A (Pending)
.aid/works/{work}/
  STATE.yml                     ← Deploy State (current operation status, history)
  packages/                    ← product (one file per release)
    package-001-{name}.md
    package-002-{name}.md
  PLAN.md                      ← deliveries and sequencing
  deliveries/delivery-NNN/tasks/task-NNN/  ← full path: task files with statuses
  tasks/task-NNN/                          ← lite path: task files with statuses (no delivery-NNN/ nesting)
  features/                    ← feature SPECs
```

> **Accuracy note (schema shape mismatch, not resolved by this task).** `work-state-template.yml`
> does carry a `deploy` key, but its shape is a sequence of **per-delivery** records
> (`delivery` / `state` / `pr` / `kb_updated` / `tag` / `notes`, "aid-deploy only... never
> derived from child files"), not the single Status/Active-Package/History state machine
> this skill's Deploy State below describes (Idle -> Selecting -> Verifying -> Packaging ->
> Done, with an active-package pointer). The two shapes do not line up key-for-key; this is
> a schema gap surfaced by the refactor, flagged here rather than papered over. The `deploy`
> key is the closest real target and the sole legal AUTHORED write point for this skill's
> state, but a literal "Status:"/"Active Package:" read/write against it does not map
> one-to-one onto its declared fields.

## ⚠️ Pre-flight Checks

### Step 0: Invocation-context mode detection

- **`work-NNN` argument present** → proceed with Steps 1–6 below (the existing
  pipeline path; untouched).
- **No `work-NNN` argument, but a free-form description was given instead** → the
  shortcut-scaffold path (see `## Argument-Hint` above): bind `{name}=aid-deploy`,
  `{verb}=deploy`, `{artifact}=""`, `{description}=<the given text>`, then delegate
  directly to `.aid/runtime/templates/shortcut-engine.md § State: INTAKE` — Steps 1–6
  below do not run for this path (that pre-flight belongs to the post-Execute pipeline
  role, not the shortcut entry).
- **Neither `work-NNN` nor a description** → print the `## Argument-Hint` usage block
  and exit.

1. Verify `.aid/` workspace exists.
2. Resolve work directory: if the `work-NNN` argument was given, use that work
   directory; if not (single-work auto-select), enumerate works **cross-worktree**:
   run `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git
   worktree; never the local `.aid/works/` glob, which is empty on `master`), taking
   each record's field-1 `work_id` — single record → auto-select; multiple records →
   list them, ask user to choose; zero records on any worktree → **STOP.** "No works
   found. Run `/aid-describe` first." **Then locate + enter the work's
   worktree**, before item 3 below reads work `STATE.yml`: follow
   `.aid/runtime/templates/downstream-worktree-entry.md` to normalize the work id to its bare
   `work-NNN` branch name, `locate` the worktree (which **always exits 0** and returns
   `<path>\t<status>`), and enter the returned path. Keep the defensive empty-path/non-zero
   backstop that stops rather than operate blindly — it should not fire against the real helper.
   Never create a new worktree — creation belongs to the work-starting skills only. (Applies only
   to this `work-NNN` pipeline path — the free-form shortcut mode in Step 0 does not reach here.)
3. Read work `STATE.yml`'s Deploy State (`deploy` key -- see the Workspace accuracy note
   above) (or create it if absent).
4. Read `PLAN.md` — identify deliveries and their statuses.
5. Check work `STATE.yml`'s Tasks State (derived view) — check statuses and grades.
6. If Deploy State shows an active package → resume from that step (see State Detection).

## State Detection

Read work `STATE.yml`'s Deploy State (`deploy` key):
- **Status: Idle** → IDLE state (start new package; see `references/state-idle.md`)
- **Status: Selecting** → SELECTING state (resume delivery selection; see `references/state-selecting.md`)
- **Status: Verifying** → VERIFYING state (resume verification; see `references/state-verifying.md`)
- **Status: Packaging** → PACKAGING state (resume packaging; see `references/state-packaging.md`)
- **Status: Done** → Re-run mode (see Re-run section)

Print the state-entry line and "you are here" map:

**IDLE / first run:**
```
[State: IDLE] — No active release; begin assessing eligible deliveries.
aid-deploy  ▸ you are here
  [● IDLE ] → [ SELECTING ] → [ VERIFYING ] → [ PACKAGING ] → [ DONE ]
```

**SELECTING:**
```
[State: SELECTING] — Presenting eligible deliveries for user to include in this release.
aid-deploy  ▸ you are here
  [✓ IDLE ] → [● SELECTING ] → [ VERIFYING ] → [ PACKAGING ] → [ DONE ]
```

**VERIFYING:**
```
[State: VERIFYING] — Running full build, tests, and lint against selected deliveries.
aid-deploy  ▸ you are here
  [✓ IDLE ] → [✓ SELECTING ] → [● VERIFYING ] → [ PACKAGING ] → [ DONE ]
```

**PACKAGING:**
```
[State: PACKAGING] — Producing release artifacts per infrastructure.md § Deployment.
aid-deploy  ▸ you are here
  [✓ IDLE ] → [✓ SELECTING ] → [✓ VERIFYING ] → [● PACKAGING ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Release complete; all deliveries and tasks marked Shipped.
aid-deploy  ▸ you are here
  [✓ IDLE ] → [✓ SELECTING ] → [✓ VERIFYING ] → [✓ PACKAGING ] → [● DONE ]
```

## Inputs

- `.aid/works/{work}/PLAN.md` — deliveries, sequencing, success criteria
- Per-task `DETAIL.md` — task scope; full path: `.aid/works/{work}/deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`; lite path: `.aid/works/{work}/tasks/task-NNN/DETAIL.md`
- `.aid/works/{work}/REQUIREMENTS.md § 11` — the `### Feature NNN` sections; what was specified
- Work `STATE.yml` `## Tasks State` table — task statuses and review grades per task (both paths derive into this same rollup)
- `known-issues.md` — if exists, check for Critical/High blockers
- **KB via INDEX.md** — Read `.aid/knowledge/INDEX.md`, pull:
  - `infrastructure.md` § Deployment — how to package, where to publish
  - `infrastructure.md` § Source Control — VCS commands, branching strategy
  - `technology-stack.md` § Commands — build, lint, test commands
  - Any other docs INDEX summaries indicate are relevant

## Dispatch Protocol

This skill follows the L1+L2+L3 subagent-visibility protocol (heartbeats, ETA timers,
calibration). The full checklist lives in
`.aid/runtime/templates/dispatch-protocol-checklist.md`; read it before any subagent
dispatch in this skill.

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| IDLE | `references/state-idle.md` | `aid-operator` | → SELECTING |
| SELECTING | `references/state-selecting.md` | `aid-operator` | → VERIFYING |
| VERIFYING | `references/state-verifying.md` | `aid-operator` | → PACKAGING |
| PACKAGING | `references/state-packaging.md` | `aid-operator` | → DONE |
| DONE | `references/state-done.md` | `inline` | → halt |
| RE-RUN | `references/state-re-run.md` | `inline` | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

## Quality Checklist

- [ ] All selected deliveries have all tasks complete
- [ ] All task grades meet minimum (from `bash .aid/runtime/scripts/config/read-setting.sh --skill deploy --key minimum_grade --default A`)
- [ ] No Critical/High known-issues unresolved
- [ ] Full build passes (not incremental)
- [ ] Full test suite passes
- [ ] Lint/format clean
- [ ] Package created per infrastructure.md § Deployment
- [ ] Package file saved with all sections filled
- [ ] Release notes generated in package file
- [ ] KB updates routed to `.aid/knowledge/STATE.md` `## Q&A (Pending)` (not direct edits)
- [ ] Delivery and task statuses updated to Shipped in work STATE.md
- [ ] Work STATE.md `## Deploy State` updated (Done + History entry)
