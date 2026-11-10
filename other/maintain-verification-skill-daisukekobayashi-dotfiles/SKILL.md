---
name: maintain-verification-skill
description: Use only when the user explicitly invokes maintain-verification-skill to update an existing project verification skill and feature map against source and observed behavior.
license: MIT
disable-model-invocation: true
---

# Maintain a Verification Skill

Run only when explicitly invoked, for example `$maintain-verification-skill` in
Codex or `/maintain-verification-skill` in Claude Code. A generic verification
request or a reference from another skill does not activate this workflow.

Keep an existing verification procedure usable as the application changes.
Follow the same procedure on either agent; use the tools available in that
session without requiring a particular model, subagent type, or CLI.

## Establish the target

Locate the project-owned verification skill and its feature map. Check both
`.agents/skills/verify-*/` and `.claude/skills/verify-*/`, resolving links to
identify the canonical source. Follow the project's established layout when
different. If several targets fit and the request does not identify one, ask
which to maintain. If none exists, report that prerequisite and recommend
`create-verification-skill`; do not invoke it automatically.

Inspect repository instructions, working changes, execution wrappers, and the
verification skill's launch, readiness, driving, and cleanup procedures. Resolve
links before writing: a project skill may point into the user's global skill
view. Update only a project-owned target, preserving unrelated changes.

The editable scope is the verification skill's own instructions, feature map,
and helpers. Product code, dependencies, shared configuration, and other skills
require separate authorization. Treat maintained procedures as durable project
operational documentation; keep run evidence in ignored temporary storage.

## Reconcile the map with the source

Read the index and each feature's instructions. Check for missing, duplicate,
obsolete, and unlinked entries. Trace each feature's user-facing entry point in
the current source and note the behavior, prerequisites, and one observable
verification recipe. Add a missing feature only with a concrete source path
and a discoverable user contract.

Use the [verification contract](../create-verification-skill/references/verification-contract.md)
to resolve gaps in readiness, evidence, or cleanup. Source inspection can
identify likely drift; it does not establish that a procedure works.

Work directly for a small map. Delegate bounded, read-only source inspection
only when authorized and supported; the coordinator owns edits and live driving.
Independent app instances must not compete for the same port or data directory.

## Exercise the procedures

Run every mapped feature at least once using the documented execution boundary.
Combine compatible recipes into a small number of app states. For a requested
subset, name that subset and leave the rest explicitly unverified.

- Establish the artifact/revision, readiness, and ownership before driving.
  After an unexpected failure, restore a known state or recheck readiness
  before proceeding. A healthy process alone does not establish usable UI state.
- Use an owned long-lived instance for a service when appropriate, or a fresh
  isolated invocation for a short-lived CLI. Respect shared instances and data.
- Capture the action, expected and actual result, and retained evidence path for
  each feature. Record missing access or configuration and the attempted route;
  do not invent access, install dependencies, or claim the feature passed.
- Clean up owned processes and temporary state after failures as well as
  success. Confirm that logs, screenshots, and other evidence survive cleanup.

## Classify and correct

Separate three findings:

- **Procedure drift:** the documented command, selector, prerequisite, or map is
  outdated. Correct it within the target skill and run the corrected path again.
- **Helper gap:** the application behaves as intended but the skill's helper
  cannot drive it. Fix that helper within scope and rerun the affected path.
- **Product regression or unclear contract:** implementation disagrees with the
  established behavior, or the intended behavior cannot be established. Report
  evidence; do not weaken an assertion, delete coverage, or rewrite the expected
  result simply to make the procedure pass. Do not repair product code here.

An unexpected result alone is not proof of an intentional behavior change.
Ground changed expectations in an explicit requirement, specification, or
recorded decision. Preserve unresolved coverage in the map.

Use [prove-it-works](../prove-it-works/SKILL.md) before reporting. Review the
diff and report one outcome:

- **clean:** all mapped features ran successfully and no correction was needed.
- **changed:** the scoped corrections were exercised and all mapped features
  ran successfully.
- **blocked:** any mapped feature remains unverified, inaccessible, failing, or
  ambiguous. List successful paths, any verified corrections, and the concrete
  blocker separately. A subset check is not a clean result for the whole map.

Include the target, revision, changed files, per-feature results, and evidence
locations. Commit, publication, and review requests follow the user's existing
authorization; this skill does not initiate them automatically.

## Source

Adapted from Lauren Tan's [pstack maintain-verification-skill](https://github.com/cursor/plugins/blob/6714489fa233263f00e419f6cfc4759b07c81056/pstack/skills/maintain-verification-skill/SKILL.md).
Local changes: shared Codex/Claude instructions, explicit invocation, canonical
project ownership, bounded optional delegation, and incomplete-coverage outcomes.
See [LICENSE](LICENSE).
