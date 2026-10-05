---
name: implement-chisel-processor
description: Document-driven workflow for implementing and reviewing Chisel processor and memory-subsystem RTL. Use when Codex must work from approved architecture and design documents, reason in synthesized-hardware terms, avoid redundant or overprotective logic, add focused verification, or perform a static or verification review assigned by a workflow Harness.
---

# Implement Chisel Processor

## Establish authority

Read repository instructions first. Then locate and read, in order:

1. Approved architecture and design documents.
2. The current Task Envelope, allowed paths, and acceptance criteria.
3. Current source, tests, generated reports, and relevant reference implementation.

Treat the user's latest correction as authoritative. Design documents define
target behavior after applying accepted corrections; source defines current
behavior. Report corrections not yet reflected in documents. Never silently
resolve a conflict. State the target, current implementation, and migration.

Do not modify approved Architecture or Design. Prefer their code fragments and naming. If a fragment has a syntax, type, timing, or semantic error, report the exact issue as a Design gap before changing its meaning.

## Confirm design closure

Use `$design-chisel-processor` when field semantics, ownership lifetime, cycle
boundaries, conflict priority, late-response handling, identity protection, or
acceptance criteria remain unresolved. Begin RTL work only after choices that
affect correctness or interfaces are closed.

Do not repeat questions already answered by the user's latest instruction or
accepted documents. Ask before adding a field, protocol, or identity mechanism
only when its necessity or semantics remain unresolved. Do not invent
unspecified protocols or conservative guards.

## Close the integration surface

Before editing, identify the real elaboration top, source set, immediate
dependencies, and downstream regression scope. Search for stale paths, duplicate
top-level definitions, and incompatible local copies of shared packages.

For every changed Bundle or protocol, trace definitions, constructors, storage,
all producers, all consumers, partial-write methods, tests, widths, encodings,
and port order. Separate mechanical ABI migration from semantic redesign.
Record which pipeline owns each writable field and which architectural side
effects consume it.

Trace a reference implementation through its complete producer-to-consumer path
before declaring a local fragment incorrect. Classify each mismatch as design,
interface, implementation, documentation, test, or tooling so the correct owner
and migration action are explicit.

## Implement as hardware

Read [hardware-rules.md](references/hardware-rules.md) before writing RTL.

Make the smallest change that preserves the documented semantics. Reuse the repository's reference processor structure when requested. Keep event generation parallel and centralize state-update priority. Use masks and one-hot selections for candidate networks. Mux only fields consumed on the critical path.

Before each added condition, field, register, or mux, determine whether existing invariants already imply it. Prefer an assertion for an upstream contract over duplicated runtime protection when the design assigns that responsibility upstream.

Organize substantial Scala source with the repository's required functional separators. Add concise comments only for cycle contracts, non-obvious invariants, intentional redundancy left for synthesis, and timing-sensitive choices.

## Respect workflow ownership

When a Harness provides a Task Envelope:

- treat Architecture, Design, allowed paths, verification mode, and gates in the envelope as authoritative;
- return only the artifact type requested by the assigned role;
- do not create `_codex.md`, handoff files, review reports, or state files unless the envelope explicitly allows them;
- submit a structured Design-gap response with a concrete counterexample when implementation cannot preserve the approved Design;
- leave formal state transitions, file writes, evidence projection, worker dispatch, and role rotation to the Harness.

## Verify and review

Read [verification-review.md](references/verification-review.md). Add focused assertions and directed corner cases, then run Verilator as the default ChiselTest backend. Compilation alone is not verification.

When assigned a static-review role, inspect source and documents for correctness, redundancy, overprotection, timing paths, dependency chains, assertion quality, and test gaps. When assigned a verification role, run or assess the approved commands and preserve commands, seeds, logs, failures, and concise conclusions.

Do not dispatch additional agents from this Skill. The Harness chooses `independent_workers` or `active_only`, creates the required roles, and records whether evidence is independent.

When an implementation task follows a failed review, address valid findings and rerun affected tests. Review roles report findings without modifying files. Do not report completion while required tests fail.

## Deliver

Report concisely:

- modified files and governing design documents;
- elaboration top, source set, affected dependents, and regression scope;
- reused reference structures and any new fields;
- event priority, assertions, and deliberately omitted redundant logic;
- timing risks and any remaining dependency chain with location and scale;
- Verilator commands, seeds, cycle counts, results, and log paths;
- Harness run ID, approved Design hash, and evidence paths supplied by the task;
- unresolved issues or unverified behavior.
