---
name: scoville-plan
description: Maintain, resume, audit and hand off repository Plans, Work Items and Decisions, including their wording. Use for Scoville Plan requests, repository-owned planning or Decisions, durable work across interruption or compaction, format-version-1 projects, messages during active planned work, and adding, removing, reordering or cleaning up Plan points. Exclude pure informational questions with no retained action, small contained tasks needing no durable Plan, and explicit opt-out.
compatibility: "Any Agent Skills host with repository read/write access. Direct Markdown/YAML planning needs no service or network. Selector and validator need Python 3.10+. Manual alternatives load only without Python. Helper errors remain errors. Developed for Codex and Claude Code. Other hosts are untested."
---

# Scoville Plan

Maintain native `format_version: 1` Plans, Work Items and Decisions by editing
Markdown/YAML directly. Use the repository's planning owner. A small reversible
task needs no new Plan unless required locally. On explicit opt-out, read no
references or records under this Skill and make no Skill-derived changes or
claims; report a conflicting repository requirement.

This Skill works independently. Other Scoville Skills are optional. Use an
available, active sibling only for its applicable concern; do not install,
simulate or require an absent sibling. Honor explicit user exclusions.

Relevant neighboring owners:

- `scoville-code`: implementation scope, risk, and validation outside Plan records.
- `scoville-handoff`: active-work transfer snapshots.

Plan owns its records' wording and lifecycle. It does not start Workflow or
choose dispatch routes. Run one editor at a time; do not change affected files
or executor model/reasoning settings concurrently. Reads and Skill upgrades
require no migration.

Keep Plans, Work Items and Decisions as short as possible and only as long as
necessary. Necessary information enables correct execution, verification or
continuation without hidden context: the outcome, binding constraints,
dependencies, acceptance, relevant decision reasons and current evidence limits.
Omit repetition and process history that no longer affects the work. Preserve
required historical records under their lifecycle rules, not as repeated context.

## Authority and evidence

1. Follow system/safety and explicit user instructions, repository rules, then
   the supported native profile. The agent's temporary task list is a disposable
   mirror of repository records.
2. Preserve actual scope, choices, dependencies and history. Source, silence,
   current behavior and structural validation are not authorization or proof
   that work occurred. Apply historical stops only to their recorded scope.
3. Ask only for a missing material choice: activation, cancellation, deletion,
   changed scope, weaker Acceptance, ambiguous succession or Decision transition.
   Already authorized directions need no repeated approval.
4. Record explicit material human choices as accepted Decisions. Unresolved material
   choices become proposals; report alternatives, tradeoffs and effect, and
   ask only before dependent work. Link Decisions to affected todo items, never
   unrelated items. Started items also link relevant proposals in Decisions and
   may link accepted Decisions. ADR status owns their state.
5. At work start run the proposal inventory below and read relevant proposals
   (all proposals for a full audit). Preserve unresolved choices at handoff.
6. Mark done only after observing every Acceptance criterion and retaining its
   evidence. Failed or partial work remains unfinished. Report observed checks
   separately from unverified behavior.
7. Stop affected execution on an explicit stop or invalidating correction.
   Answer informational questions and continue. Append additive work through
   edit.md. Direct Plan maintenance never creates a Work Item about maintenance.
8. Keep required facts once in their owning field, in the existing record's
   language unless the user chooses another. New records use the request or
   owning Plan's language. Keep format labels and identifiers unchanged.

## Proposal inventory

Follow Runtime helpers below for availability and failures. Run:

```text
python "<skill-directory>/scripts/select_context.py" --root "<project-root>" --proposals --format json
```

Read relevant Decisions from the returned paths. The inventory includes unlinked
proposals and works without an active Plan. Load [inventory details](references/read-only.md#surface-proposals)
only for output fields or selection-mode constraints.

## Work Item template

```text
### W-001 Observable outcome

Status: todo
Depends on: []
Blocked by: []
Decisions: []
Outcome: One independently resumable result.
Acceptance: Observable checks and their required results.
Instructions: []
Steps:
1. [status: todo] Perform one coherent unit at the known repository-relative paths and verify its result.
Evidence: []
```

New Work Items use one-line Instructions or [], at least one status-marked Step,
and no Next action. Work Item Status covers the whole outcome; Step status records
observed progress. Field details and legacy continuation are in edit.md. Steps
have no independent acceptance or dependencies.
Use [granularity](references/planning-granularity.md) only when outcome or Step
boundaries need judgment, not for a routine insertion with known boundaries.

## Load only the current route

| Operation | Additional reference |
| --- | --- |
| Insert, refine, order, select, progress, block, complete or cancel Work Items; ordinary recovery | [edit.md](references/edit.md) |
| Read direction, list records, select dispatch units | [read-only.md](references/read-only.md) |
| Create/restructure, activate, finish, cancel or delete Plan; change Goal | [native-project-lifecycle.md](references/native-project-lifecycle.md) and edit.md |
| Create, audit or transition Decisions | [native-decision-format.md](references/native-decision-format.md) and edit.md |
| Explicit request to inspect/repair/migrate recorded Plan/Step progress; never ordinary work or recovery | [repair.md](references/repair.md) |
| Audit wording | edit.md; Decision reference for Decision sections |
| Validate or diagnose structure | edit.md; operation reference only if a diagnostic needs it |

An unknown profile requires listing the root first. PROJECT_INDEX.md,
docs/plans and docs/decisions must form a complete supported profile. Initialize
only when all three are absent and a durable Plan was requested. Preserve
partial, foreign, unsupported or ambiguous state; repair only a representation
defect that changes no intent.

After every completed write operation, validate the complete resulting profile
using the command and diagnostic handling in edit.md.
See Runtime helpers below for the profile-specific runtime rule.
Report outcome, active or blocked work, actual evidence, unresolved choices and
the next action. These direct edits provide no locks or atomic transactions.

## Runtime helpers

Use the bundled helpers for their operations. Read their invocation instructions,
not their source, unless diagnosing a failure.
Only when Python is unavailable, load the matching optional reference below.
Missing scripts, missing dependencies or helper errors stop the operation;
they never enable the manual route. Do not load these references otherwise.

| Helper | Optional no-Python reference |
| --- | --- |
| `scripts/select_context.py` | [select_context](references/fallbacks/select_context-fallback.md) |
| `scripts/validate_profile.py` | [validate_profile](references/fallbacks/validate_profile-fallback.md) |
