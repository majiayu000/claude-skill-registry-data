---
name: brownfield-workflow
description: Structure brownfield change work across requirements, planning, design, manufacturing, and testing while surfacing unresolved items. Use when an existing codebase or system must be changed without treating its current implementation as the complete specification.
---
<!-- xid: A17C4E8B2D91 -->
<a id="xid-A17C4E8B2D91"></a>

# Brownfield Workflow

Use this Skill to carry one brownfield change through requirements, planning,
design, manufacturing, and testing. Preserve the upstream item as the
traceability anchor; do not create an independent task catalogue.

The Skill is an orchestration contract. Load detailed procedures from the
references only when the current item needs them:

- [Phase workflow](references/phase-workflow.md): phase inputs, outputs, gates,
  and handoffs;
- [Service, data, and impact investigation](references/service-data-impact.md):
  service ownership, DFD, Entity lifecycle, structure, and existing data;
- [Existing requirement validation](references/requirements-validation.md):
  validation of an existing Requirement's authority, freshness, consistency,
  testability, and human decision gate;
- [Specification reconciliation](references/specification-reconciliation.md):
  current specification, current behavior, and new requirement comparison
  before design approval;
- [Post-reconciliation detailed planning](references/delta-detail-planning.md):
  refinement of work, data, compatibility, test, evidence, and handoff plans
  from approved specification deltas;
- [IPA reconstruction guide mapping](references/ipa-reconstruction-guide-mapping.md):
  mapping from the human-oriented IPA reconstruction guidance to this Skill;
- [File-edit integrity](references/file-edit-integrity.md): encoding,
  concurrency, specification alignment, history, and new-file conformity;
- [Change test suite](references/change-test-suite.md): scope, white-box
  structure, pre/post comparison, existing data, and regression evidence;
- [Testability gate and AI case generation](references/testability-and-case-generation.md):
  design-time input completeness, traceable case candidates, and definition
  gaps before execution;
- [Reporting and closure](references/reporting-and-closure.md): overview/detail
  reports, evidence, unknowns, decisions, and handoff.

## Core contract

- Preserve the upstream item as the traceability anchor.
- Search applicable `knowledge/` before each phase judgment.
- Compare the change with the target's existing pattern and record
  `follows`, `adapts`, `introduces`, or `unknown`.
- Treat existing code and past Knowledge as evidence, not automatic business
  truth.
- Resolve service ownership and service-interaction/data-flow Knowledge before
  requirements become design.
- Keep current behavior, desired behavior, inference, and human decisions
  separate.
- Record every `unknown` with what is unknown, why, downstream impact, resolver,
  and owner. Do not turn missing evidence into "no impact".
- Do not create untraced work or approve human-owned requirements, design,
  release, or residual-risk decisions.

## Phase-based usage

Use the Skill for the phase that matches the current handoff. Carry the same
upstream item, evidence, unknowns, owners, and decisions forward; do not restart
the work as a new task catalogue.

| Phase | Ask the Skill to do | Main output | Stop when |
|---|---|---|---|
| `requirements` | Validate an existing Requirement or separate purpose, current behavior, desired behavior, acceptance, scope, normal/error/boundary conditions, and unresolved decisions | Requirement validation result, traced items, and decision questions | Requirement authority, meaning, scope, acceptance, or owner is missing or conflicting |
| `planning` | Create the initial work policy, then refine it from approved specification deltas | Initial work policy, post-reconciliation detail plan, impact scope, test inputs, gates, and handoff | Impact, data, owner, or delta-specific execution policy is unknown |
| `design` | Reconcile current specification, current behavior, and new requirement; then define the traced structural delta and contracts | Specification reconciliation, design-to-test handoff, testability result, case candidates, and definition gaps | A material delta lacks class, evidence, protected invariant, impact, owner, or human decision |
| `manufacturing` | Implement only approved design items while preserving file and concurrency integrity | Changed artifacts, integrity evidence, and exposed decisions | Implementation requires guessing or conflicts with the specification |
| `testing` | Execute the approved change-focused suite, collect evidence, compare pre/post results, and classify differences | Test results, evidence, residual risks, and retest needs | Expected result, evidence, or comparison basis is not approved |
| `closure` | Trace upstream items to results, classify unknowns, record decisions, and prepare the next handoff | Summary-first closure and residual-risk decisions | Any material unknown lacks impact, resolver, owner, or decision |

For a phase-specific request, state the phase explicitly, for example:
`Use $brownfield-workflow in planning phase to define the impact scope and
testability inputs for <upstream_ref>.` Load the detailed reference named in
the phase row only when needed.

## Inputs

- user request and upstream work items;
- current-system evidence, source, tests, logs, configuration, and DB data;
- service catalog and service-interaction/data-flow Knowledge;
- constraints, risks, decisions, and decision owners;
- existing architecture, API, event, ERD, DDL, data-flow, or test artifacts.
- design inputs needed to determine testability, including expected results,
  observation sources, fixtures, and owners.

If a required input is absent, record an impact-bearing `unknown` instead of
inferring it from a namespace, folder, one call site, or current behavior.

## Required item shape

Maintain each phase item with:

| Field | Meaning |
|---|---|
| `id` | Stable item identifier |
| `upstream_ref` | Requirement or plan item realized |
| `target` | Source, DB, API, test, configuration, or operation |
| `phase_result` | Concrete current-phase result |
| `state` | `done`, `unknown`, or `out_of_scope` |
| `basis` | Evidence, source location, or decision basis |
| `knowledge_refs` | XIDs used for the item |
| `pattern_decision` | `follows`, `adapts`, `introduces`, or `unknown` |
| `pattern_basis` | Existing pattern, delta, evidence, and owner |
| `impact` | Downstream effect |
| `next_action` | Confirmation, analysis, implementation, test, or handoff |
| `owner` | Person or role needed for the next decision |

## Phase responsibilities

### Requirements

Separate change purpose, evidenced current behavior, desired behavior,
acceptance conditions, scope, normal/error/boundary conditions, assumptions,
and unresolved decisions. When an existing Requirement or equivalent upstream
definition is supplied, load [existing requirement validation](references/requirements-validation.md)
and validate its source, version, authority, owner, freshness, consistency,
and testability before using it for design or test generation. Do not rewrite or
approve business requirements on behalf of the responsible human.

### Planning

Define the initial work policy from the available Requirement and current-system
evidence: impacted targets, work units, dependencies, execution order,
compatibility/data/release/rollback policies, tools, versions, fixtures,
environment, test data, cleanup, result storage, risks, gates, and handoffs.
After specification reconciliation, load [post-reconciliation detailed planning](references/delta-detail-planning.md)
and refine the plan from approved delta rows before manufacturing or test-case
approval. Prepare test tools in planning; run the testability gate and generate
traceable case candidates in planning/design; execute approved tests in testing.

### Design

Define only the traced structural delta, responsibilities, API/message/DB/data
contracts, processing/state, transaction/idempotency/concurrency,
error/retry/timeout/rollback, compatibility/migration, observability, and
design-to-test handoff required by upstream items. After existing Requirement
validation, load [specification reconciliation](references/specification-reconciliation.md)
and compare the current specification, evidenced current behavior, and new
requirement before approving the design delta. Record protected invariants,
compatibility impact, downstream impact, and human decisions.
Confirm that each affected behavior has enough target, condition, expected
result, observation, evidence, and ownership information to define a
reproducible test case. Load [testability gate and AI case generation](references/testability-and-case-generation.md)
for the check and gap report.

### Manufacturing

Implement only approved design items. Preserve existing file conventions and
uncommitted work. Stop an item as `unknown` or `blocked` if implementation
exposes an unresolved requirement, design, compatibility, or data decision.
Load [file-edit integrity](references/file-edit-integrity.md) before editing.

Before replacement, write through an atomically replaced temporary file only
after the revision check passes.

#### Brownfield file editing integrity

Before editing an existing file, record its encoding, BOM, newline convention,
strict Unicode decoding, original bytes or hash, and approved spans. Preserve
the encoding/BOM/newline policy and verify the `after_bytes` round trip after
writing. This verifies encoding validity but does not hide pre-existing
mojibake. Use a compare-and-swap revision token: if the current bytes differ,
abort and do not overwrite concurrent work. Atomic replacement follows only
after the semantic edit contract and `semantic_alignment` are confirmed.

Treat the AI interpretation as a hypothesis, not authority; check the
authoritative specification, Knowledge, local pattern, schema, and tests.
When alignment is unclear, perform a bounded Historical conflict investigation
using Git history, `log`, `show`, `diff`, and `blame`, while
retaining current uncommitted and untracked state. Do not select the newest
revision as authority.

Apply the Uncommitted-file policy classifications
`pre_existing_human_or_unknown`, `ai_owned_current_work`,
`non_overlapping_changes`, and `mixed_or_overlapping`; never reset, checkout,
clean, or stash protected work without authorization. New-file extension conformity:
for new files, inspect same directory and same-extension peers, companion files,
extension-specific
rules, scope, cluster, majority, confidence, and repository-wide fallback.
Stop on a weak margin or unresolved pattern conflict.

### Testing

Create or refresh the test suite before the implementation change. Confirm the
testability gate and human decisions, then execute approved case candidates.
Confirm that changed behavior meets the approved specification and that
in-scope existing behavior is not unintentionally broken. Load [change test
suite](references/change-test-suite.md) for scope, data, structure, selection,
comparison, and reporting rules.

## Loading existing artifacts

Import existing service, flow, DB, or test artifacts before new discovery.
Preserve the source, search canonical Knowledge by identity and aliases,
classify `create`, `extend`, `refresh`, `split`, `reject_duplicate`, or
`proposal_only`, attach freshness and conflicts, and update canonical
Knowledge only under an authorized decision. Reuse an XID-bearing file under
`knowledge/` through `xref show`; do not duplicate it.

## Summary-first and closure

Every phase output starts with:

1. phase conclusion;
2. unresolved items ordered by downstream impact;
3. blockers and required decisions;
4. completed items;
5. next handoff;
6. links to detailed evidence.

Before closure, trace every in-scope upstream item to a result, attach evidence
and Knowledge/pattern basis, classify every unknown, record the next-phase input
package, and stop when proceeding would require guessing. Use the shared
[Skill Reporting Contract](../../docs/core/contracts/081_skill_reporting_contract.md#xid-6B2D9F4A1C73)
with `Status`, `Result`, `Evidence`, `Open Items`, and `Handoff` in that order.
