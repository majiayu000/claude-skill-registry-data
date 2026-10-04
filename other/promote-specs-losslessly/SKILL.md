---
name: promote-specs-losslessly
description: Preserves every material detail when promoting drafts, design notes, or plans into canonical requirements and specifications. Use this skill when integrating draft material into canonical documents.
---
# Promote Specs Losslessly

## Promotion Principle

Treat promotion as a traceable semantic migration, not a summarization exercise.
Preserve meaning and specificity even when reorganizing, deduplicating, or rewriting source material.

## Establish Authority and Scope

1. Read repository instructions, documentation standards, lint configuration, and definitions of canonical and non-canonical document layers.
2. Identify every source document, canonical destination, related requirement, existing spec section, architecture decision, feature file, index, and cross-reference in scope.
3. Read each in-scope source completely before editing canonical documents.
4. Record the starting revision or preserve the original source text so later source edits cannot hide an omission.
5. Determine which source wins when drafts and canonical documents disagree.
   Use explicit repository authority, newer approved decisions, or user direction; never silently choose the most convenient wording.
6. Leave draft deletion, archival, or relocation out of scope unless the user explicitly requests it.

## Build a Promotion Ledger

Create a working ledger before making canonical edits.
Use a table, checklist, or other inspectable format appropriate to the repository and task size.

Break the source into independently meaningful details, including:

- Normative obligations and acceptance criteria.
- Interfaces, schemas, types, operations, inputs, outputs, and return values.
- Algorithms, ordering, state transitions, precedence, and concurrency behavior.
- Preconditions, invariants, defaults, limits, units, thresholds, and qualifiers.
- Error cases, status codes, recovery behavior, negative behavior, and side effects.
- Security, privacy, performance, compatibility, migration, and observability constraints.
- Rationale, rejected alternatives, examples, open questions, and follow-up work.
- IDs, anchors, citations, cross-references, and ownership boundaries.

For each detail, record:

- A stable source locator such as file, heading, line, bullet, or requirement ID.
- A precise semantic summary that retains modality and qualifiers.
- Its destination document and anchor or planned section.
- Its disposition: carried, consolidated, superseded, rejected, or deferred.
- The reason and authority for any disposition other than carried.
- Its verification status.

Do not use an omitted, miscellaneous, or implicitly covered disposition.
Map duplicate details to the same canonical target and mark them consolidated.
Treat unresolved details as deferred work with an explicit destination or blocker, not as permission to drop them.

## Classify Content by Canonical Layer

Follow local repository rules first.
When local rules do not decide placement, use these defaults:

- Put testable statements of required outcomes and constraints in requirements.
- Put design contracts, interfaces, data shapes, algorithms, processing order, errors, and implementation behavior in technical specifications.
- Put durable system boundaries and architectural decisions in architecture documentation.
- Put executable acceptance examples in feature files or the repository's acceptance-test layer.
- Put unresolved exploration and temporary sequencing in non-canonical working documents.

Preserve a single canonical source of truth for each fact.
Replace duplicated canonical prose with links only after confirming that the linked target carries the full meaning.
Never make a canonical document depend on a draft or temporary working document.

## Integrate Without Semantic Compression

Edit canonical documents only after the ledger covers the complete source.

- Preserve obligation strength exactly; do not turn `MUST` into `SHOULD`, required behavior into an example, or a prohibition into silence.
- Preserve scope, exceptions, conditions, actors, timing, ordering, quantities, units, defaults, and failure semantics.
- Preserve named contracts and stable identifiers unless the repository's canonical naming rules require a change; record every rename in the ledger.
- Preserve rationale that prevents future maintainers from repeating a rejected design or misreading a constraint.
- Separate normative requirements from implementation design without weakening either side.
- Rewrite and reorganize freely when meaning remains equivalent and every source detail stays traceable.
- Consolidate genuine duplication, but map every duplicated source location to the consolidated target.
- Split large canonical documents or introduce focused sections instead of shortening content to fit.
- Update IDs, anchors, indexes, backlinks, and cross-references as part of the same promotion.

When a draft conflicts with canonical material, document the conflict and its resolution in the ledger.
If authority is unclear and the choice changes observable behavior or obligations, stop that portion of the integration and ask for direction.

## Perform Independent Coverage Audits

Do not validate only by rereading the edited target.
Perform all of these passes against the preserved source and the final diff.

### Audit Source to Canonical Coverage

Walk every ledger entry and locate its final canonical expression.
Verify semantic equivalence, including qualifiers, negative cases, and obligation strength.
Require zero unmapped entries.

### Audit Canonical Provenance

Walk every material canonical addition or changed behavior in the diff.
Trace it to a source detail, an existing canonical rule, or an explicit approved decision.
Flag accidental invention, scope expansion, and unsupported obligations.

### Audit Cross-Document Consistency

Check requirements against technical specifications, architecture docs, feature files, indexes, and related specs.
Verify that IDs and links resolve, backlinks exist where required, terminology is consistent, and canonical docs do not link to non-canonical sources.

### Audit the Result Mechanically

Inspect the complete version-control diff, not only individual files.
Run the repository's documentation linters, link checks, spec validators, generated-index checks, and relevant tests.
Fix failures caused by the promotion and report any validation that could not run.

## Completion Gate

Do not declare promotion complete until:

- Every source detail has a verified disposition and canonical target or explicit approved deferral.
- Every semantic conflict has an authoritative resolution or is reported as a blocker.
- No requirement, constraint, edge case, error behavior, rationale, or traceability link disappeared implicitly.
- The forward coverage, reverse provenance, and cross-document audits pass.
- Relevant validation commands pass, or external blockers are stated precisely.
- The final report lists sources, canonical destinations, material reconciliations, explicit deferrals or rejections, and validation results.

Report preserved details and resolved conflicts concretely.
Never use a small diff, cleaner prose, or the existence of new canonical text as evidence that the promotion was lossless.
