---
name: yq-simplify-code
description: 审计代码、测试或门禁是否重复、过度设计或失去用途。
---

# Find Code Simplifications

Turn a broad request to simplify a codebase into a small set of well-proven removals, consolidations, or demotions. Follow the code and repository decisions; prefer a few candidates with complete evidence over a long list of plausible guesses. This skill can produce an audit, durable proposals, targeted TODOs, or implementation when the user authorizes changes.

Simplification is reduced owned surface and cognitive load, not fewer lines at any cost. A wrapper that relocates the same complexity, a dependency that adds more glue than it removes, or a deletion that silently drops supported behavior is not a win.

## Establish repository context

1. Confirm the requested scope, output, and write authority. A review request reports findings; a fix or implementation request may change code within scope.
2. Read applicable agent instructions, `CONTEXT.md`, architecture docs, ADRs/RFCs/decision notes, package manifests, public API docs, compatibility policy, and testing guidance.
3. Identify protected seams and product commitments. Treat a recorded decision as rationale to test against current evidence, not eternal truth; treat tests as evidence of expected behavior, not proof that every pinned behavior remains valuable.
4. Inspect the actual checkout, branch/base, dirty state, generated sources, and runtime-loading paths before judging reachability.

Do not import another repository's architectural exceptions. A seam is protected only when this project's code, contract, or current decision evidence protects it.

## What makes a strong candidate

A strong candidate removes, folds, narrows, or demotes real surface area and shows that its ongoing cost exceeds its present value. Common forms include:

- a public method, event, config knob, extension hook, registry notification, helper, package, command, or durable field with no production consumer;
- tests or docs as the only consumers of behavior that is not a supported contract;
- two representations mirroring the same fact across state, events, caches, persistence, projections, or UI models;
- an interface method every implementation carries but no caller uses;
- a package or service split that exists only for fixtures, demos, or support code and adds publish, versioning, or dependency overhead;
- speculative generality such as unused multi-tenancy, background orchestration, invalidation, plugin hooks, fallback layers, or compatibility shims with no supported owner;
- defensive copies, validators, rollback paths, or expected-output inventories that protect an impossible or unsupported boundary;
- hand-rolled parsers, framing, retries, globbing, diffing, scheduling, or data structures already covered by a suitable runtime builtin or maintained dependency;
- an added-then-removed feature whose old implementation, tests, docs, migrations, or decisions still remain as sediment.

Thin observations are not durable simplification proposals: a typo, one unused local, one tool's unreviewed dead-code report, or “this looks complex” without consumer and contract evidence. When repository edits are authorized, fix tiny safe items or add a concise local TODO with a clear owner and action. Without write authority, report the candidate only.

## Survey broad scopes deliberately

For a broad audit, partition the codebase by real ownership boundaries rather than file count. Useful domains include:

- public APIs, domain services, commands, configuration, and extension points;
- state, events, persistence, caches, migrations, and replay;
- asynchronous lifecycle, cancellation, retries, readiness, disposal, and failure arbitration;
- adapters, integrations, protocol boundaries, serialization, and validation;
- frontend state, rendering contracts, and duplicated server/client models;
- build tooling, packages, scripts, examples, fixtures, snapshots, and generated artifacts.

Start with the largest production-code deltas and highest fan-out abstractions. An audit that stops after obvious unused symbols can miss duplicated lifecycle machinery carrying most of the cost.

Use repository-supported structural tools when configured, such as CodeGraph for indexed call paths and blast radius. Use `rg` for exact symbols, wire strings, config keys, dynamic registrations, docs, and cases structural indexes do not cover. When breadth requires several independent domains and delegation is allowed, give each subagent a non-overlapping boundary and require evidence and rejected candidates, not guesses.

When a code simplification makes comments, examples, decision prose, or implementation-heavy documentation obsolete, include their owner-first cleanup in the same candidate. Use `$yq-technical-writing` for proposition-preserving edits and `$yq-doc-maintenance` for duplicated or conflicting document ownership. Do not expand a focused code audit into a repository-wide prose cleanup without user scope.

## Audit trust and lifecycle boundaries

For every defensive copy, freeze, validator, callback capture, and schema check, name the data origin and next owner.

Same-process typed calls often borrow readonly values. Parsers, config loaders, queues, model/tool JSON, durable files, workers, processes, databases, and wire decoders own or validate their inputs. Tests using hostile getters, fake typed objects, callback replacement, or mutation after a same-process handoff can reveal a speculative contract; they do not automatically justify deletion.

For asynchronous code, draw the ownership graph. Map each sentinel, readiness promise, cancellation route, timeout, disposer, retry counter, and state flag to a distinct owner or transition. Several mechanisms that mirror the same liveness or settlement fact are candidates for one transaction or lifecycle controller. Preserve separate machinery when it protects genuinely different concerns such as synchronous publication and rollback, first-terminal-outcome arbitration, worker/process ownership, callback containment, or dispose-to-quiescence.

## Audit invariant companions

For every validator, consistency check, or regression assertion, identify the observations it compares and how each is produced. A strong invariant compares facts that can diverge independently—for example, a writer's output against a separately parsed readback, a primary crawl against an independent traversal, or runtime state against a durable receipt. A same-source comparison, service-presence assertion, fixed example copied from the implementation, or value rechecked by the same parser may only restate one fact twice.

Treat weak companion checks as simplification candidates, but first prove what failure they were intended to catch. Preserve or replace a check when it still detects a distinct corruption, race, compatibility break, or external disagreement. Do not count two differently named paths as independent evidence when they share the same producer or cached input.

## Audit tests and gates as one portfolio

When tests or validation gates are part of the reported complexity, evaluate the portfolio rather than adding another check by default. For each test family or gate, identify the supported contract or risk it owns, the failure it can uniquely detect, the evidence source it observes, its overlap with other checks, and its maintenance, runtime, and flake cost.

Classify each item as:

- **Keep:** it uniquely protects a current contract, security boundary, compatibility obligation, recovery path, or independently produced fact.
- **Merge:** several checks prove the same fact from the same source and can share one owner without losing a failure signal.
- **Narrow:** a repository-wide check can target the packages, files, or behavior that actually own the risk.
- **Run on demand:** an expensive environment, release, migration, or provider rehearsal has value only for the changes that can affect it.
- **Remove:** it pins unsupported behavior, a dead API, implementation choreography, a duplicated snapshot, or a same-source assertion with no independent failure mode.

Count the production surface, fixtures, helper architecture, CI time, maintenance, and debugging burden on both sides of a proposed change. Do not optimize for test count, coverage percentage, or a green dashboard in isolation. This audit does not create tests, scripts, or gates; when evidence is missing, report the gap unless the user separately authorizes implementation.

## Evaluate dependency substitutions

A dependency or runtime builtin can simplify a codebase, but the comparison is net surface rather than implementation line count.

For each proposed substitution:

- identify the exact behavior the existing implementation owns and the residual semantics the replacement does not cover;
- check runtime and language-version compatibility, maintenance, adoption, license, security posture, transitive footprint, bundle/runtime cost, and operational constraints;
- prefer a stable builtin when it meets the contract;
- count implementation, dedicated tests, docs, update burden, and glue on both sides;
- preserve project-specific behavior that still has consumers rather than hiding it behind a misleading generic wrapper.

Reject a swap whose adapter and compatibility layer recreate the removed complexity.

## Prove or reject every candidate

Classify consumers before proposing a change:

- **Production:** shipped source, runtime configuration and loaders, public entry points, migrations, operational scripts, and real integration paths.
- **Non-production:** unit fixtures, snapshots, tests, examples, documentation, old plans, and generated expected output.
- **Ambiguous:** examples used as smoke paths, build-time plugins, scripts invoked by release or operations, dynamically loaded modules, reflection, and string-addressed events. Inspect them before classification.

Search the exact identifier and its aliases, import/export surface, method-call forms, wire strings, configuration names, serialized fields, and generated references. Read every credible call site. Static-analysis tools can nominate candidates; they cannot adjudicate public APIs, dynamic loading, reflection, schemas, or compatibility.

Reject or downgrade a candidate when:

- a supported production consumer exists and removal is a product decision rather than cleanup;
- the surface is required by a current public contract, compatibility window, migration, security boundary, or verified operational recovery path;
- current decision evidence explains the seam and the new evidence does not beat that rationale;
- the removal causes broad unrelated churn without reducing the public or conceptual surface;
- behavior loss, migration cost, or rollback risk exceeds the demonstrated maintenance benefit;
- the evidence is partial. Mark the missing evidence as `unknown`; do not report zero consumers from an incomplete scan.

For accepted candidates, state the current surface, production and non-production consumers, behavior given up, net deletion or consolidation, migration/compatibility impact, verification plan, confidence, and strongest counterargument.

## Choose the right output

- **Implement directly** when the user requested changes, the candidate is locally bounded, behavior is understood, and focused verification can prove the result.
- **Use a TODO/FIXME/XXX** only when repository edits are authorized, for a small local cleanup that is useful but not part of the current implementation. Give it a stable tag, reason, and concrete action. Otherwise report the suggested marker without writing it.
- **Write a durable proposal** only when repository edits are authorized, for public API removal, architecture consolidation, compatibility change, persistence/schema change, or cross-package work. Use the repository's existing ADR, RFC, issue, design-note, or proposal mechanism. Without write authority—or when no mechanism exists—report the candidate and proposed content instead of creating a document.

A durable proposal should name the problem and evidence, exact surface to remove or fold, strongest reason to keep it, behavior or optionality surrendered, migration, acceptance criteria, risks, and validation. Consolidate overlap into the current owning decision instead of creating a duplicate.

## Coalesce superseded decisions carefully

Audit old decisions only when requested or when the simplification makes an owning document obsolete.

1. Identify the current owner from shipped code, configuration, schemas, current docs, newer decisions, and inbound links. Dates and titles are discovery hints.
2. Distinguish full from partial supersession. Any surviving behavior, compatibility obligation, durable format, migration, or independently current rejected alternative makes the older record partially live.
3. Before removing a fully superseded record, transfer unique rationale, alternatives, consequences, verification evidence, reintroduction conditions, and named coverage gaps to the current owner.
4. Repair every inbound link and follow the repository's retention policy. Do not edit frozen archives to make active prose cleaner.

For an added-then-removed feature, full supersession requires absence from production code, configuration, public schemas, durable/wire formats, migrations, compatibility handling, current docs, and tests that present it as supported. Negative tests that enforce absence and rationale preventing accidental reintroduction may remain.

## Fold work from another branch or PR

Compare the sibling branch to its verified base or merge-base, not automatically to the current branch or `origin/main`. Port non-overlapping, well-proven changes; consolidate overlapping findings into the current owner. Do not preserve a candidate merely to preserve a count. Close or mutate external PR state only when the user requested it or that housekeeping is explicitly in scope.

## Validate and report

Select validation from the outgoing diff and repository tooling. Run focused owning tests, type or schema checks, build/package smoke when public or built surfaces change, documentation/link checks for proposals or comments, and `git diff --check`. Use broader suites when the change is cross-cutting, the user requests them, or narrow evidence cannot credibly cover the blast radius.

Report accepted candidates, rejected candidates with reasons, areas surveyed, areas not inspected, files or surfaces changed, behavior deliberately preserved, and checks actually run. Keep proposals separate from implemented and verified simplifications.
