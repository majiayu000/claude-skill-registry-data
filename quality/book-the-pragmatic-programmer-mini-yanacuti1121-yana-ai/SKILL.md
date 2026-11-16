---
name: book--the-pragmatic-programmer--mini
description: >-
  The Pragmatic Programmer (Hunt & Thomas) — Condensed rules — key principles distilled. Use when asked to apply The Pragmatic Programmer principles or review code against The Pragmatic Programmer standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY The Pragmatic Programmer by Andrew Hunt and David Thomas

## When to use

Use as a general engineering operating style when the goal is accountable delivery, adaptability, fast feedback, and code that remains easy to change.

## Primary bias to correct

Do not optimize only for the local edit, requested feature, or familiar ritual. Own the outcome by reducing duplicated knowledge, keeping concerns independent, proving assumptions early, automating repeated work, and making intent clear.

## Decision rules

- Be pragmatic, not dogmatic: choose the practice, formality, quality level, and stopping point that improves real outcomes for the users, risks, and codebase.
- Own the result. Surface tradeoffs, risks, uncertainty, and avoidable design costs instead of blaming tools, framework defaults, schedule pressure, or existing style.
- Think beyond the local edit: quick fixes that multiply future maintenance cost are usually a bad bargain; leave touched areas better where the cost is low.
- Keep one authoritative representation for each piece of system knowledge. Business rules, validation, status semantics, mappings, calculations, schemas, configuration meaning, generated output, and manual process steps should derive from or trace to one owner.
- Preserve orthogonality: keep components independent, responsibilities non-overlapping, interfaces narrow, collaborator knowledge small, and policy, mechanism, data, presentation, orchestration, and computation separated.
- Keep volatile decisions reversible where practical. Do not hard-code vendors, platforms, databases, deployment environments, policies, or requirements before evidence justifies the commitment.
- Use domain vocabulary and small domain languages only when they make rules clearer to the people who must validate or change them.
- Prefer thin end-to-end tracer bullets over piles of isolated pieces. Keep the first slice simple but real enough to validate architecture, integration, and assumptions.
- Use prototypes to learn, not to pretend the work is done. State what the prototype proves, what it does not prove, and which shortcuts must be discarded or hardened.
- Dig for real requirements. Separate durable needs and constraints from current implementation details, proposed solutions, growing prose specs, and unresolved team hesitation.
- Automate repetitive, error-prone, easy-to-forget, or ritualized work. Builds, tests, linting, formatting, packaging, deployment, setup, validation, and release should be reproducible and aligned with shared automation.
- Shorten feedback loops with relevant tests, automated checks, visible failures, and cheap early signals before late expensive surprises.
- Make contracts, assumptions, invariants, responsibilities, and caller/callee obligations explicit and close to the abstraction they protect.
- Distinguish programmer errors, contract violations, impossible states, expected domain failures, retryable failures, recoverable failures, and permanent failures; preserve diagnostic context and fail inside boundaries that prevent wider collapse.
- Treat resource ownership as a contract. Release every acquired allocation, handle, lock, or resource on success and failure paths, preferably opposite acquisition order.
- Prefer inspectable plain text, open formats, scripts, explicit serialization, and version-aware configuration when longevity, diffability, automation, migration, or interoperability matter.
- Treat shared mutable state, ambient context, globals, temporal coupling, and asynchronous complexity as costs that must earn themselves and be made visible.
- Use tooling as leverage for correctness and speed, but understand generated code, formal methods, specifications, and tool output before relying on them.
- Debug from reproduced facts: observe, isolate, explain, fix, and verify before guessing or blaming compilers, operating systems, libraries, or vendors.
- Break work into small deliverable increments with honest uncertainty, visible risk, and estimates that can be corrected by feedback.
- Communicate through code, names, docs, comments, commit messages, scripts, tests, and artifacts. Use comments for rationale, contracts, or non-obvious behavior, not as substitutes for encoded rules.
- Build pragmatic teams around shared responsibility, explicit expectations, automation, fast feedback, visible quality, and artifacts you are willing to stand behind.
- Apply the broken windows rule: fix or visibly contain small quality decay before bad code, unclear ownership, weak design, or broken process becomes normal.

## Trigger rules

- When the same fact appears in multiple artifacts, choose one owner and derive, generate, validate, or trace the rest.
- When one change requires edits in many unrelated places, repair the missing boundary or hidden coupling before it spreads.
- When volatile details are hard-coded, move them into validated, controlled, versioned configuration, metadata, or an explicit abstraction.
- When uncertainty is high or a decision is hard to reverse, reduce risk with tracer feedback, a prototype, a smaller reversible step, or a delayed commitment.
- When prototype code, generated scaffolds, diagrams, specs, formal models, or tool output start becoming production truth, inspect, understand, harden, replace, or reject them deliberately.
- When prose specifications keep growing without reducing uncertainty, build a working slice, example, or prototype that forces feedback.
- When hidden assumptions live only in comments, caller folklore, or tribal setup steps, move them into code, contracts, tests, scripts, or checked configuration.
- When an error or resource crosses a boundary, decide who can recover, what context survives, and who owns cleanup.
- When shared state, async behavior, locks, ordering, or temporal coupling appears, make ownership, synchronization, cleanup, and ordering requirements explicit.
- When repeated manual steps, human checks, environment rituals, or release procedures appear, automate and version them.
- When tests are slow, flaky, environment-dependent, or require excessive unrelated setup, improve the feedback path rather than normalizing skipped checks.
- When a human finds a bug, add or improve an automatic regression test around the protected contract.
- When code works for reasons nobody can explain, stop and prove the behavior with data before depending on it.
- When local decay appears in touched code, fix it if cheap or leave an explicit containment or cleanup path.

## Final checklist

- One authoritative owner for each system fact?
- Unrelated concerns independent and volatile choices reversible?
- Working feedback exists for risky assumptions?
- Prototype, generated, and tool-derived behavior deliberately accepted?
- Contracts, failures, diagnostics, resources, and cleanup explicit?
- State, concurrency, ordering, and coupling visible?
- Repeatable work automated, versioned, and aligned with shared checks?
- Tests automatic, relevant, and run before calling the change done?
- Names, comments, docs, scripts, tests, and commits communicate intent?
- Touched area better or explicitly contained?
