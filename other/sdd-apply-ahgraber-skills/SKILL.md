---
name: sdd-apply
description: |-
  Use when implementing tasks from a change's tasks.md. Triggers: "apply tasks", "implement the change", "work through tasks", "start implementing", "continue implementing", "apply the change".
---

# SDD Apply

Implement tasks from `SPECS_ROOT/changes/<name>/tasks.md`.
Check off each task as it completes.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write artifact updates, task notes, and commit bodies in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## Hard Gate

**If `tasks.md` does not exist for the active change: STOP.**

> "No tasks to implement. Run `sdd-propose` first to create the change artifacts."

Do not proceed without tasks.md.

**If the change directory has no proposal commit: STOP.**
Check with:

```bash
git log --diff-filter=A --format=%H -- .specs/changes/<name>/proposal.md
```

If the output is empty, tell the user:

> "The change artifacts are not committed. Commit `.specs/changes/<name>/` before implementing. Without that commit, the spec-drift check cannot tell which spec text you approved and which text changed during implementation."

Proceed without the commit only if the user explicitly says to.
In that case, state in every later verify and sync report that the spec-drift check could not run.

## Critical Constraints

**Never reference ephemeral scaffolding in any persisted artifact.**

Ephemeral scaffolding includes:

- Task IDs and task numbers (e.g. `Task 7.4`, `T12`)
- Group names and group numbers (e.g. `Group 8`, `G3`)
- Design-section IDs (e.g. `D12`, `design §4.2`)
- Other planning-artifact identifiers that won't outlive the change

These must not appear in:

- Code, symbols, or filenames
- Comments or docstrings
- Commit messages (subject, body, or footer)
- PR titles or descriptions
- Any other artifact that persists after the change is archived

Tasks, groups, and design-section IDs are scaffolding for the current change.
Once archived, only the spec name persists — references to ephemeral IDs become meaningless noise to future readers.
Name things after _what they do_, not where they came from in `tasks.md` or `design.md`.
If you catch yourself writing "D12 wiring" or "Task 7.4 implementation," restate it in terms of the behavior or component being changed.

**This applies whether or not the `commit-message` skill is available.**
When drafting a commit message during apply:

- Prefer invoking `commit-message` if it is loadable in this environment.
- Otherwise, draft a Conventional Commit (`type(scope): subject`) that describes _what changed and why_, and apply the constraints above.
- Do not paste design or task identifiers into the message even if they appear in the surrounding tasks/design files.
- If the commit edits spec text, list each spec change in the body, one line per change, prefixed with the capability (`references/sdd-change-formats.md` § 5.4).

## When to Use

- A change has `tasks.md` and implementation should begin or continue
- Resuming implementation after a pause

## When Not to Use

- No `tasks.md` exists — run `sdd-propose` first
- All tasks complete — run `sdd-verify`, then `sdd-sync`, then `sdd-archive`

## Invocation Notice

- Tell the user when this skill is running: `sdd-apply`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Process

### Phase 1: Load Context

1. Confirm which change to apply (ask if multiple active changes exist)
2. Read `.specs/changes/<name>/tasks.md` — full task list
3. Read `.specs/changes/<name>/design.md` — architectural decisions to follow
4. Read `.specs/changes/<name>/specs/` — delta specs for behavioral requirements
5. Read `.specs/specs/` — baseline specs for full context
6. Read `.specs/changes/<name>/proposal.md` § User Stories and `.specs/NORTH-STAR.md` — the value this work serves.
   Each requirement's `Serves:` backlink names the stories it advances; these bound scope (see **The story ceiling** below).
7. Check task ordering against `references/sdd-change-formats.md` § 4 — each task should depend only on capabilities built by earlier tasks.
   The schema-config rule below is the named instance: if `.specs/.sdd/schema-config.yaml` exists, identify tasks that define schema contracts (endpoint definitions, model schemas, DDL changes) and confirm they are sequenced before any tasks that consume them.
   Surface any ordering gaps to the user before implementing (advisory — the user may decide the order is intentional).
8. If `.specs/changes/ORDER.md` exists, find this change in it (`references/sdd-change-formats.md` § 6).
   If a **Starts after** gate is not met, or the change is under `## Not scheduled`, tell the user which gate or condition is open and its reason, and ask whether to proceed.
   If the change is in none of the sections, tell the user that its order has not been assessed.
   If the change appears under `## Shared requirements`, tell the user which requirements must rebase if the other change syncs first (§ 6.2).

### Phase 2: Identify Starting Point

Check tasks.md for already-completed tasks (`- [x]`).
Start from the first unchecked task.

If all tasks are complete:

> "All tasks are already complete. Run `sdd-verify` to confirm the implementation, then `sdd-sync` and `sdd-archive`."

Stop.

### Phase 3: Implement Task-by-Task

For each unchecked task:

1. **Read the task** — understand what it requires
2. **Check dependencies** — are earlier tasks complete?
   If not, implement them first
3. **Implement** — write the code to the depth the served story requires, no further (see **The story ceiling** below)
4. **Check for newly-emerged write-sites** — see § Write-site emergence below
5. **Test** — run the project's standard test command at its broadest reasonable scope (e.g. `pytest` with no `--ignore` / `--deselect` / `-m` filters).
   Inner-loop iteration may use a narrower scope, but the verification you act on — and any pass/fail count you report — must come from a broad-scope run.
   If you exclude any path, marker, or file, name the exclusion and justify it in the same message.
   "Not part of this change" is not a valid justification for a class or module rewrite — every test that imports the rewritten symbol is part of the change by definition.
   If a test fails, stop and resolve the failure before proceeding to the next step.
6. **Check off** — update `tasks.md`: `- [ ]` → `- [x]`

Follow design decisions in `design.md` — don't diverge without reason.
Follow behavioral requirements in delta specs — these define what "correct" means.
Apply the **Critical Constraints** above to every artifact you produce — code, comments, and commit messages alike.

If `.specs/.sdd/schema-config.yaml` exists and a task consumes a schema contract that is not yet defined, pause before implementing it.
Surface the dependency gap and confirm with the user whether to reorder tasks in `tasks.md` first.

### The story ceiling

Each requirement's `Serves:` backlink (and the stories in `proposal.md` § User Stories) names the user value the work exists to deliver.
That value is the **scope ceiling**: implement to the depth the served story requires, and no further.

When implementing surfaces behavior that no story motivates — extra configuration knobs, speculative generality, defensive paths beyond the contract, broader abstraction than the requirement needs — **stop and surface it** rather than building it silently.
It is likely over-engineering, the failure mode this ceiling exists to bound.
The user decides whether the extra work is justified (and, if so, which story it serves); the default is to leave it unbuilt.

A requirement you are implementing that carries no `Serves:` backlink is itself a flag — confirm it advances a real story before building to it.

### Write-site emergence

A SHALL requirement may end up with multiple code paths that produce or modify the contract-asserted value during implementation — not just the canonical path.
Common examples: deduplication shortcuts, cache fast-paths, retry/fallback branches, idempotency early-returns, merge or composition steps that write the same fields.

When implementing a task introduces such a path for an existing SHALL:

1. **Pause before checking off** the implementation task.
2. **Add a paired test task** to `tasks.md` that exercises the contract _through the new path_.
   The new test task must produce runnable evidence (test, schema check, or captured output) — same standard as the original SHALL coverage rule.
3. **Implement the test** as part of the same work, or sequence it as the immediately-following task.
4. **Then** check off the original implementation task.

A test exercising only the canonical path does not stand in for evidence on a shortcut, retry, or composition path.
This rule is what `sdd-verify`'s write-site enumeration is checking; cover it at apply time and verify has nothing to flag.

When unsure whether a path is contract-relevant, surface it to the user rather than skipping the test task silently.

### Phase 4: After All Tasks

**Before checking off the final task** (hard gate):

1. Run the full suite as CI would — no programmatic exclusions unless they appear in the project's CI config.
2. `rg`/`grep` for tests that import any symbol you changed and confirm they ran in step 1.
   The blast-radius check is what catches tests pinned to rewritten classes or modules that a marker filter would silently skip.
3. Tests rendered obsolete by the change must be deleted or updated with reasoning recorded in the diff — not silently skipped.
4. Report results with scope alongside counts (e.g. "407 passed, 1 file excluded because…").
   Pass/fail counts without an exclusion list are not a verification report.

When the gate passes and all tasks are checked off:

> "All tasks complete. Recommended next steps:
>
> 1. Run `sdd-verify` to confirm implementation matches the change artifacts
> 2. Run `sdd-sync` to merge delta specs into main specs
> 3. Run `sdd-archive` to complete the change"

## Spec Changes During Implementation

Specs are the source of truth.
When the code or a test conflicts with a spec, change the code to match the spec.
Change the spec only as `references/sdd-change-formats.md` § 5 allows.
Read § 5 before you edit any spec text.

- **Tasks and design:** change `tasks.md` and `design.md` as the work requires, and keep each Decision entry current.
  A design decision that traces to a user decision is the exception: changing it is a requirement change.
- **Scenario changes:** add or revise a scenario without asking first, if the change does not narrow what its requirement guarantees and its rationale is not "the code does this".
  Record it in `design.md` § Spec Changes, labeled with its source: the upstream story, requirement, or decision, or `agent choice`.
  At the end of the turn, list the scenario changes for the user and ask for approval.
  If one turn produces 5 or more agent-choice scenarios, stop and ask the user before continuing.
- **Requirement changes:** adding, removing, or rewording a requirement, narrowing a scenario, a breaking change, or anything that touches Out of scope or Resolved Questions.
  Stop and get the user's approval before implementing.
  Record a Decision entry in `design.md` and a dated Resolved Questions line in the proposal, in the same commit as the code.
- **Scope changes:** a change to the proposal's scope is a requirement change.
- **Baseline errors:** do not edit `.specs/specs/` during implementation.
  Record the error in `design.md` § Baseline Errors; `sdd-sync` fixes it.

## Common Mistakes

- Implementing without reading design.md (misses architectural decisions)
- Gold-plating beyond the served story — building behavior no user story motivates instead of surfacing it (see **The story ceiling**)
- Not checking off tasks as they complete
- Implementing tasks out of order when dependencies exist
- Continuing past a failed task without resolving it
- Diverging from design decisions without documenting why
- Editing a spec to match the code when the spec traces to a story, the north star, or a user decision
- Recording a scenario change without its source label, or labeling an agent choice as following from an upstream source
- Implementing a requirement change before the user approves it
- Answering a refactor that forces a spec edit by swapping the method name in the spec, instead of restating the sentence as the outcome it protects (`references/sdd-change-formats.md` § 5.2)
- Starting implementation before the change directory has a proposal commit
- Adding a deduplication shortcut, cache fast-path, retry branch, or composition step for a SHALL-covered value without adding a paired test task that exercises the new write-site (see § Write-site emergence)
- Checking off the implementation task before the paired test task for a newly-emerged write-site is added and runnable
- Referencing ephemeral scaffolding — task IDs, group names, design-section IDs (e.g. `D12`) — in code, comments, commit messages, or PR descriptions (see **Critical Constraints**)
- Drafting a commit message inline without invoking `commit-message` when it is available, or without applying the **Critical Constraints** when it is not
- Excluding a test file, path, or marker from a verification run without naming the exclusion and justifying it in the same message — especially fatal when the change rewrites a class or module that the excluded tests pin
- Reporting "N passed, 0 failed" without also reporting what was excluded and why — scope must travel with the counts

## References

- `references/sdd-change-formats.md` — artifact formats, implementation ordering (§ 4), the rules for spec changes during implementation (§ 5), and change order across active changes (§ 6)
- `references/sdd-schema.md` — schema config format (§ 3) and lifecycle policy (§ 4)
