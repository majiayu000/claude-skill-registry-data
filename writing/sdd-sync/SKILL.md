---
name: sdd-sync
description: |-
  Use when merging delta specs from a change into the main baseline specs. Triggers: "sync specs", "merge delta specs", "update main specs", "apply the spec changes", "sync the change".
---

# SDD Sync

Merge delta specs from a change directory into the main baseline specs.
Applies each delta marker intelligently, preserving existing content not mentioned in the delta.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write any new baseline text and the sync report in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- After `sdd-verify` passes with no blocking findings — implementation is confirmed correct
- After `sdd-verify` reports only blockers that are explicitly overridden per `references/sdd-change-formats.md`
- Ready to finalize the change and update the source-of-truth specs

## When Not to Use

- Delta specs don't exist for this change — nothing to sync
- Implementation isn't verified — run `sdd-verify` first
- Blocking findings remain from `sdd-verify`

## Invocation Notice

- Tell the user when this skill is running: `sdd-sync`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Soft Gate

If no delta specs exist in `.specs/changes/<name>/specs/`, warn:

> "No delta specs to sync."

Stop unless the user confirms to proceed.

Before syncing, confirm verification status and any recorded override trail:

1. `sdd-sync` consumes the latest `sdd-verify` outcome; it does not reconstruct verification from `design.md`.
2. If the latest verify result is not in context, stop and tell the user to run `sdd-verify` first.
3. If sync is proceeding under override, read `.specs/changes/<name>/design.md` for `## Verification Overrides` and confirm each applicable entry has all required fields (finding, stage, reason, constraints, follow-up task, approved by, recorded).
   Stop if any required field is missing.
4. Any blocker from the current verify result that is not covered by a recorded override remains blocking.
   Stop and tell the user which blockers remain uncovered.

Then check `.specs/changes/<name>/tasks.md` for unchecked tasks.
Do not count a task that a recorded override names as its follow-up task; the override process requires that task to stay open.
If other unchecked tasks remain, warn:

> "{N} tasks are still incomplete. Sync will write their behavior into the baseline specs before it is implemented. Sync anyway?"

List the open tasks with the warning.
Wait for user confirmation before proceeding.

Then run the spec-drift check (`references/sdd-change-formats.md` § 5.5), even if verify already ran it.
Specs can change after verify.
If any spec edit lacks its recorded user approval, stop and list the edits.
Sync writes the delta specs into the baseline, so an unapproved edit becomes the project's contract.
If no proposal commit exists, the check cannot run; tell the user and wait for confirmation before proceeding.

## Process

### Phase 1: Identify What to Sync

1. Confirm the active change (ask if multiple active changes exist)
2. List all delta spec files in `.specs/changes/<name>/specs/`
3. For each delta spec, identify the corresponding main spec in `.specs/specs/`
4. If sync is proceeding under override, load the matching override entries and the referenced unchecked tasks from `tasks.md`

### Phase 2: Apply Each Delta

For each delta spec, read both files:

- Delta: `.specs/changes/<name>/specs/<capability>/spec.md`
- Main: `.specs/specs/<capability>/spec.md` (may not exist for new capabilities)

Apply delta markers:

| Delta marker              | Action                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| **ADDED** requirements    | Insert as new `### Requirement:` entries in the main spec                                              |
| **MODIFIED** requirements | Find the matching requirement by name and replace it — apply the **MODIFIED preservation guard** first |
| **REMOVED** requirements  | Find the matching requirement by name and delete it                                                    |
| **RENAMED** capabilities  | Rename the capability directory and update the spec header                                             |

**Preservation rule:** Content in the main spec not mentioned in the delta is never touched.

**Strip delta-only annotations:** When writing any requirement into a baseline spec — inserting an ADDED requirement, replacing a MODIFIED one, or creating a new capability (Phase 3) — strip its delta-only lines: the `> Previously: …` provenance line and any `Serves:` backlink.
Baseline specs carry contracts, not change provenance or value backlinks; the value layer (user stories and `Serves:` links) is change-scoped and stays in the change directory.

**MODIFIED preservation guard:** The preservation rule operates at requirement granularity — a MODIFIED requirement is replaced as a whole, so scenarios its delta block omits are _not_ preserved.
Before replacing, compare the baseline requirement's scenarios and sub-clauses against the MODIFIED delta block.
If the delta omits any baseline scenario that the change did not deliberately remove (no rationale in `design.md`), stop and surface it:

> "MODIFIED `<name>`: baseline scenario(s) `<…>` are absent from the delta block and will be deleted on sync. Restore the full post-change requirement, or confirm the removal is intentional."

Replace only after the omission is confirmed intentional, and strip the delta-only `> Previously: …` and `Serves:` lines — they do not belong in the baseline (see **Strip delta-only annotations**).

A mechanical backstop ships with the skill for the **dropped-scenario** half of this guard: run `scripts/check_modified_completeness.py <specs-root> --change <name>` (a `uv` script; deps are declared inline).
It compares scenario names only and exits non-zero when a MODIFIED delta drops a baseline scenario — sub-clause and body-text preservation is _not_ mechanically checked, so keep verifying that by reading.
Mark intentional scenario drops with a `<!-- modified-removes: ScenarioName -->` comment inside the delta block.

**Stale-copy guard:** A MODIFIED block is a copy of the baseline requirement as it was when the change was proposed.
If another change synced an edit to the same requirement after that, the copy is out of date, and replacing the requirement silently reverts the other change's edit.
For each capability with a MODIFIED or REMOVED requirement, list the baseline commits made after the proposal commit (`references/sdd-change-formats.md` § 5.5, step 1):

```bash
git log -p <proposal-commit>..HEAD -- .specs/specs/<capability>/spec.md
```

If a listed commit edited the requirement, stop and surface it:

> "MODIFIED `<name>`: the baseline requirement changed in `<commit>` after this change copied it. Copy the requirement again from the baseline, apply this change's edits to the copy, record the rebase, and run sync again."

Record the rebase as `references/sdd-change-formats.md` § 6.2 describes, so the spec-drift check accepts it.

The guard does not depend on `.specs/changes/ORDER.md`, but that file's `## Shared requirements` section names the changes at risk (`references/sdd-change-formats.md` § 6.2).

**Idempotency rule:** Applying the same delta twice produces the same result as applying it once.
For ADDED: check whether the requirement already exists by name before inserting — skip if already present.
For RENAMED: check whether the new directory name already exists before renaming — skip if already renamed.

**RENAMED processing order:** When a delta spec contains RENAMED alongside other markers, process the rename first (directory rename + spec header update), then apply any ADDED/MODIFIED/REMOVED markers against the already-renamed main spec.
The delta spec is always identified by the _old_ capability name — look it up before renaming.

### Phase 2a: Fix Recorded Baseline Errors

If `design.md` has a `## Baseline Errors` section, list each entry for the user and ask which fixes to apply.
Apply the confirmed fixes to `.specs/specs/`.
These fixes are not part of the change's delta, so keep them separate in the report (Phase 6) and in the commit body.

### Phase 3: Handle New Capabilities

If a delta spec covers a capability with no corresponding main spec:

1. Create `.specs/specs/<capability>/` directory

2. Create `spec.md` in baseline format (no delta markers), writing the full skeleton:

   ```markdown
   # {Capability} Specification

   ## Purpose

   {Why this capability exists and what its requirements cover}

   ## Requirements

   ### Requirement: {Name}
   ```

   A delta spec has no `## Purpose` and no `## Requirements`, so write both here.
   Purpose is prose, not a requirement; write it by `references/sdd-spec-formats.md` § 3.1.
   The proposal's Intent explains why the change is needed, so use it as a source for the capability's need, but do not copy it: Purpose describes the capability as it stands after the change.

3. Drop the `## ADDED`, `## MODIFIED`, `## REMOVED` section headings and put every requirement beneath them at `### Requirement: {Name}`, with its scenarios at `#### Scenario: {Name}`.
   Check the level; do not just strip the marker.
   If the delta fused the marker to a requirement heading (`## ADDED Requirement: {Name}` — malformed, see `references/sdd-spec-formats.md` § 4), removing the marker leaves the requirement at `##`, where no later change can match it by name.
   Fix the delta too.

See `references/sdd-spec-formats.md` for the baseline spec format.

If the delta spec contains only RENAMED and the old capability does not exist in main specs, create the capability under the new name using the ADDED requirements as baseline content.

### Phase 4: Update Schema Snapshots (if schemas configured)

If `.specs/.sdd/schema-config.yaml` exists and `schemas/after/` is present in the change directory:

1. Copy each schema file from `.specs/changes/<name>/schemas/after/<schema-type>` to `.specs/schemas/<schema-type>` (overwrite).

2. Update `.specs/schemas/.schema-sources.yaml` with the generation date and change name.

3. If the repo contains a committed authored schema (e.g., `docs/openapi.yaml`), surface a reminder — do **not** auto-update it:

   > "Authored schema at `<path>` may need updating to match the implementation.
   > Reference: `.specs/changes/<name>/schemas/after/`"

If no schema config exists but `.specs/schemas/` contains files and no `schemas/after/` directory exists in the change, emit a visible warning:

> **WARNING:** Schema baseline exists at `.specs/schemas/` but this change has no after-snapshot. The schema baseline may be stale. Run `sdd-derive` or create `.specs/.sdd/schema-config.yaml` to enable schema tracking.

If no schema config exists and `.specs/schemas/` is empty or absent, skip silently.

### Phase 5: Validate Output

- [ ] All ADDED requirements appear in the main spec
- [ ] All MODIFIED requirements reflect the updated behavior (old version removed) with no baseline scenario dropped unintentionally
- [ ] All REMOVED requirements are gone from the main spec
- [ ] No delta markers (ADDED/MODIFIED/REMOVED/RENAMED), `> Previously:` provenance lines, or `Serves:` backlinks remain in main specs
- [ ] Content not mentioned in deltas is unchanged
- [ ] `scripts/check_spec_format.py` passes on every synced baseline spec

```bash
uv run --quiet <skill_root>/scripts/check_spec_format.py .specs/specs/<capability>/spec.md
```

Fix any failure before reporting.
Each message names the rule and its section in `references/sdd-spec-formats.md`.

### Phase 5a: Find Affected Changes

Find, for the report:

- Each other active change whose delta specs MODIFY or REMOVE a requirement that this sync changed.
  Search every active change's delta specs, whether or not `.specs/changes/ORDER.md` exists.
  Each one must rebase before it syncs (`references/sdd-change-formats.md` § 6.2).
- If `ORDER.md` exists, each change whose **Starts after** entries are now all met.

Do not edit `ORDER.md` here; `sdd-archive` removes the change from it.

### Phase 6: Report

List each capability synced:

```text
Synced:
- auth/          → 2 requirements added, 1 modified
- payments/      → 1 requirement removed
- notifications/ → new capability created (3 requirements)
Schema snapshots updated:
- openapi.yaml   → 2 endpoints added, 1 model modified
- Reminder: authored docs/openapi.yaml may be stale (schema sync did not update it)

Synced under overrides:
- `pip audit` failure for `litellm` → stage: `verify`; reason: upstream fix unavailable in current environment; constraints: no ignore added; follow-up remains open in `tasks.md`

Baseline errors fixed (not part of this change):
- auth/          → corrected token lifetime in "Session expiry"

Ready to start:
- `session-limits` (all Starts after entries met)

Must rebase before sync:
- `token-rotation` → auth: "Session expiry"
```

When committing the sync, list each spec change in the commit body, one line per change, prefixed with the capability (`references/sdd-change-formats.md` § 5.4).
List the baseline-error fixes after the change's own edits, under their own heading.

## Common Mistakes

- Replacing the entire main spec instead of merging selectively
- Leaving delta markers (ADDED/MODIFIED/REMOVED) in the main spec after sync
- Stripping a fused marker in place (`## ADDED Requirement: X` → `## Requirement: X`) instead of writing `### Requirement: X`
- Creating a new capability's baseline from the delta's requirements alone, with no `## Purpose` and no `## Requirements`
- Touching content not mentioned in the delta
- Replacing a MODIFIED requirement without first checking that its delta block preserves the baseline's still-applicable scenarios — the wholesale replace silently deletes any scenario the delta did not restate
- Carrying the delta-only `> Previously: …` provenance line into the baseline spec
- Carrying a delta-only `Serves:` backlink into the baseline spec — like `> Previously:`, it is change-scoped and must be stripped at sync
- Reconstructing the verify outcome from `design.md` instead of consuming the latest `sdd-verify` result plus any recorded overrides
- Syncing before `sdd-verify` clears all blockers, whether by a clean pass or a recorded override
- Syncing with open tasks in `tasks.md` without asking the user, or counting override follow-up tasks as open
- Treating a blocker as non-blocking without a recorded `design.md` override and an unchecked remediation task in `tasks.md`
- Syncing without running the spec-drift check, or relying on an earlier verify run when specs changed after it
- Mixing baseline-error fixes into the change's own edits in the report or commit body
- Replacing a MODIFIED requirement whose baseline another change edited after this change copied it — the replacement reverts the other change's edit

## References

- `references/sdd-spec-formats.md` — baseline spec format for new capabilities created during sync
- `references/sdd-change-formats.md` — change directory artifact formats (proposal, design, tasks), spec-drift check (§ 5.5), spec commit format (§ 5.4), and change order (§ 6)
- `references/sdd-schema.md` — schema lifecycle policy (§ 4) and `.schema-sources.yaml` format (§ 3)
- `scripts/check_spec_format.py` — checks each synced baseline spec's heading structure; exits non-zero on a malformed spec
- `scripts/check_modified_completeness.py` — mechanical dropped-scenario check (scenario names only, not body sub-clauses); exits non-zero on dropped baseline scenarios, wireable as a pre-commit/CI gate
