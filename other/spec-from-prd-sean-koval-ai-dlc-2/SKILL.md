---
name: spec-from-prd
description: Use when translating a reviewed product brief or PRD into behavioral specifications and deliverable work.
---

# Spec From PRD

Read the canonical brief/PRD, actual review decision, scope, exclusions, stable
OUT/RQ IDs and material unknowns. A small reviewed brief is sufficient; do not
require a second PRD. Apply the configured specification provider's instructions.

## Deliverable contract

Use `docs/templates/delivery-slice.md` and the examples at
`docs/examples/delivery-slices/localized-export.md` and
`docs/examples/delivery-slices/compatibility-rehearsal.md` when present. ai-dlc
source copies live under `agents/templates/` and `agents/examples/`. Without
these assets, produce the following fields directly for each slice:

- **Identity and authority:** proposed local work ID (label it draft), owner,
  review status/source, canonical brief and scoped OUT/RQ references. Proposing a
  local slug does not create a remote ticket or imply approval.
- **Scope and exclusions:** one independently reviewable, finishable outcome,
  preserved contracts and excluded work.
- **Specification decision:** explicit `requires_spec` and `spec_reason`. Changed
  observable behavior normally requires a formal specification. A no-code
  verification item references existing behavior and records `requires_spec=false`
  with its reason; it does not create another behavior spec.
- **Traceability:** requirement → formal scenario (when needed) → work ID →
  implementation step → verification/evidence. Rationale stays in the brief/design;
  observable behavior belongs to the formal provider; work owns delivery/status;
  tasks are steps inside that work item.
- **Dependencies:** `depends_on` local work IDs, required interfaces, exact source
  references and observed completion status or explicitly unavailable status.
- **Acceptance and tasks:** measurable results, compatibility checks, and the
  implementation/test/documentation steps needed for this slice. For a behavior
  check, inspect the actual setup steps, declared checks, test configuration, CI
  commands and requirement sources before proposing a mapping. Record the
  requirement/check IDs, observable behavior, inspected sources, exact command
  and its source, prerequisites and reviewed setup action, required/optional
  choice, unknowns and review decision. Syntax, filenames and successful setup
  are not evidence that a behavior is checked.
- **Open decisions and next action:** separate approved facts from proposed
  semantics and missing evidence; end with proceed, investigate or stop and why.

Create one independently finishable OpenSpec change per behavior ticket. A parent
epic coordinates children; a shared epic specification must not prevent each
child from finishing. Tests, parser, documentation and refactoring checkboxes do
not each become tickets. Split when the result can be reviewed/released separately.

Map existing canonical IDs without renumbering. Work's `requirements` contains
identifiers, not copied specification prose; put the canonical document and exact
specification/evidence paths in `artifacts`. Keep missing formats or error behavior
as open decisions; incomplete draft scenarios are not accepted executable criteria.
Resolve material product choices with their owner before dependent implementation.

When a slice adopts a team check, preserve authored tests, required IDs and
unrelated commands. Present the source-grounded mapping and prerequisite changes
for review under the existing authorization before changing shared configuration.
Use the team's command and declared shell/runtime contract; checks do not install
tools or switch shells to make a command pass. The normal check runner requires
`mise` even when `.mise.toml` has an empty tools table. A missing runtime leaves
the check unrun and the evidence incomplete; direct shell execution is not an
equivalent receipt.

Follow `docs/workflows/brownfield.md#rehearse-a-reviewed-behavior-check` for the
external disposable-fixture pass, deliberate regression failure and restored-pass
rehearsal. Record a missed expected failure or failed isolation as incomplete.
Focused `--check` feedback does not replace the full required run or completion
receipt.

For a change affecting an HTTP interface, update `docs/api/openapi.yaml` in the same
PR as the behavior and reference the contract from the work record as
`artifacts.contract`. Run the backend capability's required `api-contract` check;
for supported FastAPI projects, also review any `api-contract-drift` diff.

## Validate and hand off

When the repository is adopted (has `ai-dlc.toml` at its root) and `ai-dlc` is on PATH, create the local draft with `ai-dlc work new WORK_ID --from-issue REF` when a tracker item exists, or explicit `--title`, `--scope` and repeated `--acceptance` flags for offline work. Drafts remain unreviewed; replace TODOs, record the specification decision, add artifact/requirement/dependency references and review before mutation. Existing records are never overwritten. Run
`ai-dlc work validate WORK_ID --root PATH` before publication. This read-only check
validates the selected dependency graph and local artifacts, not remote completion
or specification meaning. Do not invent successful validation when it was not run.

Start checks fresh status through each dependency's pinned provider. Only canonical
`closed` satisfies completion; cancelled, duplicate, incomplete, unpublished or
unavailable dependencies block starting the dependent branch. Prepare independent
local draft work while the missing contract/status is resolved; do not substitute
an assumed interface. Publication needs user authorization and reviewed scope.
Repeat publication preserves authored issue descriptions; changed scope does not
silently rewrite them. Required project checks and configured merged-revision
finish gates still apply to behavior and verification work. Unavailable live
access leaves its evidence pending, even when fixture checks pass.

Resolve provider-specific commands from the configured role provider’s instructions.
The agent supplies judgment; services store, validate, and link artifacts.
