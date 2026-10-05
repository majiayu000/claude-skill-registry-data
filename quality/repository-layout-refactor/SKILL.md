---
name: repository-layout-refactor
description: Refactor a working repository from broad, weakly owned modules into concept-owned packages and localized change surfaces while preserving behavior. Use when large or flat modules contain multiple independent responsibilities, agents repeatedly edit the same hotspots, ownership is ambiguous, or the user asks to redesign and implement the source or test layout. Do not use for LOC-only cleanup, formatting, a narrow bug, a greenfield package layout, or a read-only architecture review.
---

# Repository Layout Refactor

Refactor repository structure around authoritative concept ownership. The goal
is not more folders or shorter files; it is a repository where future changes
have an obvious owner, bounded context, predictable impact, and verified
behavior.

Example: [concept-owned package migration](examples/concept-owned-package-migration.md).

## Repository Layout Quality Criteria

Evaluate the current and target layouts by the outcomes they enable, not by
file count, line count, or directory depth:

1. **Concept discoverability:** A realistic change request should point to a
   likely owner from package and module names without requiring a broad search.
   Prefer capability names over vague names such as `manager`, `processor`, or
   `helper`.
2. **Ownership visibility:** Each important concept or capability should have
   one authoritative owner. Group code by meaningful ownership, not arbitrary
   file type or convenient colocation.
3. **Change locality:** A localized behavior change should remain within its
   owner, direct contracts, and focused tests. Repeated edits across unrelated
   modules are evidence that the boundary may be wrong.
4. **Context locality:** An agent should be able to load the smallest useful
   context for a change without reading unrelated behavior. Keep the rules,
   contracts, and collaborators needed to understand one responsibility near
   its owner.
5. **Dependency clarity:** The physical structure should expose the intended
   dependency direction, and actual imports should follow it. A tidy tree that
   hides cycles or cross-layer shortcuts does not have a good layout.
6. **Evolution path:** Likely new capabilities should have a predictable home
   within an existing concept boundary. Avoid layouts that naturally grow
   parallel managers, numbered services, or generic helper modules.
7. **Canonical terminology:** Name internal authoritative modules and packages
   with the repository's current domain terms. Keep a legacy name only at a
   verified compatibility boundary; do not let a compatibility alias remain
   the apparent internal owner of the canonical concept.

Treat these criteria as contextual checks, not a scorecard. A good layout makes
ownership and change impact visible; it does not merely produce more folders or
smaller files.

## Layout Migration Criteria

Use these criteria to judge the migration itself. This skill implements a
resolved ownership model; it does not invent new architectural authority:

1. **Resolved destination ownership:** Every target module or package has one
   accepted responsibility and cutover condition. Use `architecture-review`
   first when ownership or boundary decisions remain unresolved.
2. **Behavior-preserving slices:** Move one coherent responsibility at a time,
   keep the repository working after each slice, and validate through public
   behavior rather than the proposed internal tree.
3. **Complete consumer cutover:** Update real callers, imports, registries,
   bootstrap paths, generated discovery surfaces, and focused tests in the
   same slice as the moved owner.
4. **Single active authority:** Do not leave the old and new locations as
   competing implementations. Delete old ownership or retain only a verified,
   time-bounded compatibility surface with a retirement condition.
5. **Contract and dependency integrity:** Preserve in-scope public APIs,
   serialized shapes, import contracts, metadata, and dependency direction.
   Do not hide new cycles behind dynamic imports or indirection.
6. **Reviewable recovery:** Keep each slice small enough to review, validate,
   and reverse without discarding unrelated work. Record baseline failures and
   distinguish them from migration regressions.

A migration is incomplete when it only adds the target tree, re-exports the old
monolith, or postpones consumer cutover and cleanup indefinitely.

## When To Use

Use this skill when:

- a working repository has broad modules with several independent reasons to
  change
- one file or directory has become the default edit point for unrelated work
- concept ownership is ambiguous or scattered across layers
- common changes require loading or touching unrelated behavior
- source or test layout no longer exposes clear capability boundaries
- the user asks to implement a behavior-preserving package or module refactor

## When Not To Use

Do not use this skill for:

- splitting a file only because it crosses a line-count threshold
- adding folder depth without a clearer owner or change boundary
- formatting, naming cleanup, or a narrow bug fix
- greenfield architecture design without an existing behavior baseline
- a read-only ownership or boundary assessment; use `architecture-review`
- a standalone future-agent navigation audit; use `agent-legibility-review`
- a broad rewrite that intentionally changes product behavior

If the user asks only for evaluation or a plan, complete discovery and target
design but do not edit code.

## Inputs To Infer Or Request

Infer from repository evidence when possible:

- requested repository and scope
- local instructions and protected or generated areas
- current branch, revision, and working-tree state
- public APIs, import surfaces, schemas, migrations, serialized shapes, events,
  and other contracts
- test, lint, type-check, build, and packaging commands
- current concepts, owners, consumers, and hotspot modules

Stop or narrow the task when the target behavior, public contract, ownership
authority, or allowed mutation scope cannot be established safely from local
evidence and the user's request.

## Evidence Hierarchy

Use this order when sources conflict:

1. User's latest explicit scope and behavior requirements.
2. Local repository instructions and protected-surface rules.
3. Actual code paths, callers, schemas, migrations, runtime wiring, and public
   interfaces.
4. Passing tests and reproducible runtime behavior.
5. Architecture docs, ADRs, specifications, examples, and comments.
6. Naming, line count, directory depth, and architectural inference.

Do not let a target tree, style preference, or line-count goal outrank observed
behavior and real consumers.

## Workflow

### 1. Establish The Baseline

- Read repository instructions and inspect the worktree before editing.
- Map the current package tree, entrypoints, public contracts, tests, generated
  areas, persistence registration, and runtime/bootstrap imports relevant to the
  scope.
- Run focused baseline tests and record pre-existing failures.
- Treat large files, flat layout, and repeated edits as investigation signals,
  not conclusions.

### 2. Build The Ownership Map

For each hotspot, record:

- concepts and capabilities it currently owns
- independent reasons it changes
- authoritative rules and lifecycle decisions
- callers, consumers, side effects, and validation anchors
- whether responsibility is cohesive or only colocated

Use `architecture-review` when ownership or boundary decisions are unresolved.
Use `agent-legibility-review` when the key question is whether future agents can
discover the owner, relevant context, hidden rules, or impact surface.

### 3. Design The Target Ownership

Define a target package tree and ownership matrix. Each proposed module or
package must have:

- one primary concept or capability owner
- a name aligned with the repository's canonical domain term, with any legacy
  public alias isolated at an explicit compatibility boundary
- a clear reason to change
- explicit inbound and outbound dependencies
- contract-preservation requirements
- a cutover and deletion condition
- focused validation

Preserve the existing top-level architecture unless evidence supports changing
it. Prefer concept-owned packages inside established layers over a big-bang
architectural rewrite.

Reject a target layout when it merely:

- splits by arbitrary line ranges
- produces `service1.py`, `service2.py`, or similarly meaningless names
- introduces generic `utils.py`, `common.py`, or `helpers.py` dumping grounds
- adds re-exports or facades while the old monolith remains the real owner
- creates many shallow modules with hidden shared state

### 4. Plan Vertical Migration Slices

Sequence work by concept or capability, not by file type:

1. Freeze the public behavior and import contract for the slice.
2. Move one coherent responsibility and its tests or validation anchors.
3. Cut real consumers over.
4. Remove old ownership.
5. Run focused validation.

Each slice must be reviewable, reversible, and leave the repository in a
working state. Use `prd-to-issues` when the user wants a durable,
dependency-aware implementation issue set.

### 5. Migrate Green-To-Green

Use the `tdd` Behavior-Preserving Refactor Mode:

- add characterization tests only for material behavior that lacks coverage
- move one responsibility at a time
- test through public behavior, not the proposed internal layout
- update imports, registries, bootstrap paths, and generated discovery surfaces
  together
- remove the old implementation before starting the next slice
- preserve compatibility only for verified public consumers or rollout
  constraints, with a retirement condition

Do not maintain duplicate implementations as a safety strategy.

### 6. Complete The Cutover

Verify that:

- the old hotspot is deleted or materially reduced to a justified stable facade
- every moved concept has one authoritative owner
- dead imports, obsolete tests, temporary adapters, and unused exports are
  removed
- tests are organized around public capabilities rather than private module
  layout
- documentation and navigation entrypoints point to the new owner when needed
- internal imports and ownership names use the canonical term while retained
  compatibility aliases remain visibly boundary-only

### 7. Validate The Repository

Run the strongest checks available for the changed surface:

- focused tests after each slice
- full relevant test suite
- lint, formatting, type checking, build, and packaging checks
- import-cycle or dependency-boundary checks
- API/OpenAPI, serialization, schema, migration discovery, or metadata checks
  when those contracts are in scope
- repository diff checks

Report skipped, unavailable, or inconclusive checks. Do not claim improved
maintainability, speed, token use, or model accuracy without measurements.

## Validation Requirements

Before claiming completion:

- behavior is preserved at the public interface
- baseline failures are distinguished from new failures
- the old owner no longer contains duplicate active behavior
- the target ownership map matches the implementation
- representative changes have an obvious owner and bounded context
- the physical structure exposes dependency direction and predictable extension
  points
- no generic dumping ground or unjustified wrapper was introduced
- focused and full available checks pass
- the final diff contains real cutover and cleanup, not only new facades

## Output Contract

Report:

1. scope and baseline state
2. current and target ownership maps
3. migration slices completed
4. old files or ownership removed
5. public contracts intentionally preserved
6. exact validation commands and results
7. remaining debt, skipped checks, and unresolved risks

## Side-Effect Policy

Default and maximum normal level: `git-working-tree`.

- User intent to refactor or implement authorizes scoped working-tree edits.
- A review-only or planning request remains read-only.
- Do not stage, commit, push, create branches, or publish without explicit user
  instruction or an already established repository workflow.
- Preserve unrelated user changes and avoid destructive Git operations.
- Use the diff and validation output as the normal post-edit review surface.

## Failure Modes

- **Baseline tests fail:** record the existing failure, narrow validation where
  possible, and do not claim the refactor caused or fixed it without evidence.
- **Public contract is unclear:** pause that slice or preserve the current
  surface until real consumers and repository guidance establish authority.
- **Target layout adds indirection without ownership:** reject or redesign it.
- **Circular dependencies appear:** move the boundary or extract a true
  contract owner; do not hide the cycle behind dynamic imports.
- **Compatibility cannot be retired:** identify the real consumer and record a
  bounded transition instead of leaving an unowned wrapper.
- **The task requires behavior change:** separate that change from the
  behavior-preserving refactor and obtain the appropriate product decision or
  test contract.
