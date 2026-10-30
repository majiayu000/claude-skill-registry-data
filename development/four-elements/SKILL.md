---
name: four-elements
description: Team Avatar's 24 engineering principles, grouped by element. Air subtracts, Water adapts, Earth holds, Fire drives. Use for principles or a principle-<name> lookup (laziness protocol, prove it works, and the rest), or when sizing a diff or refactoring, tempted to add an abstraction, layer, guard, or validator, deleting dead code, tracing hard-to-read code, after two failed fixes on one premise, a UX or scope tradeoff, a novel design with no precedent, choosing data structures and types, writing stateful or branchy logic, a late requirement, debugging, crash-safe or retried commands, replacing a legacy API, wiring validation or error handling, concurrent writers to one file or branch, writing or keeping a test, declaring done, trusting a measured number, a planned migration, tempted to ask the human on reversible work, repeated or checkable work, multi-step sweeps and commit order, writing the same instruction twice, or a filling context window.
---

# The four elements

Each element is a stance. Read the element the moment calls for. Each bullet names when its principle applies and links the principle in full.

Read the linked reference in full before you apply a principle. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose reference you read this session.

## Air: subtract

The Air Nomads carry nothing they do not need. Lightness is the discipline.

- **[Laziness Protocol](references/laziness-protocol.md).** Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Make the smallest change that solves it, and give a repeated decision one source of truth.
- **[Subtract Before You Add](references/subtract-before-you-add.md).** Sequencing an addition, refactor, or rewrite. Delete dead code, stale flags, and speculative guards first. Design for observed usage. Then build on the simpler base.
- **[Minimize Reader Load](references/minimize-reader-load.md).** Reviewing or shaping code that is hard to trace. Count layers and hidden state, inline one-caller wrappers, and shrink mutable scope.
- **[Attack the Premise](references/attack-the-premise.md).** Two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before another fix. Aang found a third option when everyone said there were two.
- **[Experience First](references/experience-first.md).** Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience. Ship fewer, polished features.
- **[Exhaust the Design Space](references/exhaust-the-design-space.md).** A novel interaction or architectural decision with no precedent. Build two or three competing prototypes with `scouting-flight` and compare before committing.

## Water: adapt

Water takes the shape of what holds it and still finds the lowest point.

- **[Foundational Thinking](references/foundational-thinking.md).** Before writing logic. Get the core types and data structures right, do scaffold before features, and ask what concurrent actors share.
- **[Model the Domain](references/model-the-domain.md).** Stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a state machine, typed model, table, reducer, or the right collection instead of scattered conditionals.
- **[Redesign from First Principles](references/redesign-from-first-principles.md).** A new requirement arrives for an existing design. Design as if it had been there from day one. Do not bolt it onto the side.
- **[Fix Root Causes](references/fix-root-causes.md).** Debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate.
- **[Make Operations Idempotent](references/make-operations-idempotent.md).** Commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state when run twice or resumed after a crash.
- **[Migrate Callers Then Delete Legacy APIs](references/migrate-callers-then-delete-legacy-apis.md).** A new internal API while old callers exist. Move every caller and delete the old path in the same wave.

## Earth: hold

Earthbenders wait and listen, then strike once. Stability comes from what you have verified.

- **[Boundary Discipline](references/boundary-discipline.md).** Wiring validation, error handling, or framework adapters. Validate and parse at the edges (CLI, config, network, external APIs). Inside, trust the types and keep business logic pure.
- **[Type System Discipline](references/type-system-discipline.md).** Designing types or a signature in a typed language. Make illegal states unrepresentable, brand primitives that mean different things, and derive types from the schema that owns the shape.
- **[Separate Before Serializing Shared State](references/separate-before-serializing-shared-state.md).** Concurrent actors might write the same file, branch, key, or object. Give each its own write target first. Lock only when one shared writer is a real invariant.
- **[Prove It Works](references/prove-it-works.md).** After a task, before declaring done. Check the real artifact directly. A proxy, a cached screenshot, and an agent's report are not proof.
- **[Test Behavior, Not Implementation](references/test-behavior-not-implementation.md).** Writing, changing, or keeping a test. Assert what a caller can observe, so the test fails when behavior breaks and passes when only internals change.
- **[Explain the Number](references/explain-the-number.md).** Before you trust, report, or act on a measured speedup, regression, latency, or eval score. Find what limits it and rule out that it measured something else.

## Fire: drive

Iroh taught that fire is life, not destruction. Its source is breath, not rage.

- **[Outcome-Oriented Execution](references/outcome-oriented-execution.md).** Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture. Do not preserve throwaway compatibility states.
- **[Never Block on the Human](references/never-block-on-the-human.md).** Tempted to ask "should I do X?" on reversible work. Do it, show the result, and let them correct course. Save questions for product and preference calls.
- **[Build the Lever](references/build-the-lever.md).** Any non-trivial work. Write the script, codemod, generator, or shared brief that does or proves it. The tool is the artifact a reviewer can rerun.
- **[Sequence Work into Verifiable Units](references/sequence-verifiable-units.md).** Multi-step work and how you stack commits and PRs. Each step ends in a check, verified before the next. Land a failing test before its fix.
- **[Encode Lessons in Structure](references/encode-lessons-in-structure.md).** You catch yourself writing the same instruction a second time. Turn it into a lint, a flag, a runtime check, or a script instead of more text.
- **[Guard the Context Window](references/guard-the-context-window.md).** Context fills with large outputs, long files, repeated reads, or fan-out planning. Route bulk reading to a dispatched character. Keep summaries, not dumps, in the main thread.
