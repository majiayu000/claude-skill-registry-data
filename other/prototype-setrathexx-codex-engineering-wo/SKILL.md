---
name: prototype
description: Plans and creates approved throwaway prototypes for UI, state model, or business logic questions before production implementation. Use when the user wants to test an idea, compare UI options, validate behavior, or explore uncertainty without committing to production code.
---

# Prototype

Use a prototype to answer a question quickly before changing production behavior.

A prototype is temporary. It should have a clear question, success criteria, and exit decision.

## Read First

Inspect relevant context:

- `docs/agents/domain.md`
- `docs/agents/test-commands.md`
- `CONTEXT.md`
- relevant ADRs under `docs/adr/`
- existing UI routes, components, modules, tests, or scripts near the idea

If setup docs are missing, infer local conventions from the repo and say what is unknown.

## Choose Prototype Type

Pick one:

### Logic Prototype

Use when the question is about:

- state transitions,
- business rules,
- validation behavior,
- data transformations,
- edge cases,
- algorithm shape.

Typical shape: a small local script, REPL-friendly module, or isolated route through existing public functions.

### UI Prototype

Use when the question is about:

- layout,
- interaction flow,
- component composition,
- navigation,
- visual variants,
- user feedback states.

Typical shape: a temporary route, page, story, or local-only component variant.

If the type is ambiguous, recommend one and explain why.

## Workflow

### 1. Define The Experiment

State:

- question being answered,
- prototype type,
- audience or actor,
- success criteria,
- constraints,
- what will not be tested.

If success criteria are unclear, ask the user before creating files.

### 2. Inspect Local Conventions

Find where a temporary prototype would fit without confusing production code.

Look for:

- existing scripts,
- playground routes,
- storybook stories,
- examples directories,
- test fixtures,
- local-only dev pages.

Do not invent a new convention when the repo already has one.

### 3. Propose Path And Command

Before writing, propose:

- files to create,
- files to touch,
- how to run it,
- how it will be marked temporary,
- how it will be removed or promoted.

Ask for approval before creating files.

### 4. Build Small

When approved:

- keep state local unless persistence is the experiment,
- avoid production integration by default,
- mark temporary files clearly,
- expose relevant state in the UI or console,
- skip polish that does not answer the question,
- avoid new dependencies unless approved.

Do not connect the prototype to production flows without explicit approval.

### 5. Evaluate

Run or describe the fastest verification:

- command,
- route,
- manual interaction,
- screenshot if UI verification is needed,
- expected outcome.

Capture what was learned.

### 6. Decide Exit

End with one decision:

- `discard`: prototype answered the question and should be removed.
- `promote to implementation`: idea is valid and should move into production work.
- `revise`: experiment needs another pass.

If promoting, recommend `tdd` for direct implementation or `to-issues` for slicing larger work.

See `references/prototype-exit-checklist.md`.

## Logic Prototype Guidance

Use `references/logic-prototype-guide.md` when the experiment is behavior/state/rules.

Prefer:

- simple input cases,
- printed state after each action,
- deterministic fixtures,
- no hidden network or persistence.

## UI Prototype Guidance

Use `references/ui-prototype-guide.md` when the experiment is layout/interaction.

Prefer:

- visible variants,
- minimal routing,
- local-only naming,
- no production data writes.

## Safety Rules

- Do not create files without approval.
- Do not overwrite production paths casually.
- Do not add persistence unless it is the question.
- Do not run destructive git or filesystem commands.
- Do not leave temporary code unmarked.
- Do not claim success without running or explaining verification.

## Verification

Before finishing:

- State the prototype question.
- State files created or proposed.
- State how to run or inspect it.
- State verification result or blocker.
- State exit decision: discard, promote, or revise.
- State next skill: usually `tdd` or `to-issues`.
