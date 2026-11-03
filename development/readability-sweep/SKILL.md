---
name: readability-sweep
description: >
  Three-pass readability cleanup of application source: remove inline comments, extract cohesive
  blocks into intent-named private methods, and challenge every class and method name. Use whenever
  the user says "readability sweep", "no inline comments", "remove comments", "check naming",
  "make the code readable", "extract private methods", or asks to scan the project for readability
  violations. Edits allowed. Scope is application source only (not tests/config) unless told
  otherwise. Runs lint and the full test suite after changes.
---

# Readability Sweep — Three Passes

Code must read through its names, not through narration. Run the passes in order, report per pass. Scope: application source directories only — leave tests, config, and vendor code alone unless explicitly included.

## Pass A — Comments

1. Find every inline `//` and `/* */` comment in scope.
2. Apply per comment:
   - **What-comment** (restates the next line) → delete.
   - **Genuine why** (race condition, idempotency gate, security rationale, external quirk, legal constraint) → lift into the enclosing **method PHPDoc/docstring**, then delete the inline form.
   - **Commented-out code** → delete outright.
   - **Bare `//` placeholders and trailing data annotations** → delete; move rationale to class doc if it matters.
3. Class-level doc blocks always stay. Method-level docs only where they carry a why or a non-obvious contract.

## Pass B — Extract Method

1. Inside each method, find self-contained blocks of **4+ lines** that take input → transform → produce one output.
2. Extract each into a `private` method with an **intent name** — the name states what comes out, not how (`priorComposites`, `buildRequestLine`, `advanceStatus`).
3. **Do NOT extract** — over-extraction reads worse than inline code:
   - guard clauses and early returns
   - single statements or simple assignments
   - blocks mutating two or more enclosing-scope locals
4. Keep paired classes symmetric: if two sibling drivers/paths share a shape, give both the same extractions.

## Pass C — Naming

1. For every class and public method in scope: read what it actually does, then judge the name against it.
2. Enforce the house rules:
   - class names carry type suffixes (`Controller`, `Job`, `Service`, `Event`, `Listener`, `Factory`)
   - queued classes carry the `Job` suffix; trigger-listeners are `{Verb}On{Event}Listener`
   - plain services use intent-named primary methods (`check`, `create`, `process`, `store`) — never `handle()`, which is reserved for framework contracts
   - enum cases are `ALL_CAPS_SNAKE_CASE`
3. Where a better name exists, propose current → suggested with a one-line justification. Apply renames only after the user picks; a rename is never silent.
4. **Renames rot static-analysis baselines** (entries embed symbol + path). After any applied rename, flag that the baseline needs regenerating.

## Post-flight

Run the project's formatter and full test suite. Both must be clean before reporting.

## Output Contract

Per pass: files touched and a compact change list (Pass A: comments deleted/lifted; Pass B: methods extracted with names; Pass C: renames proposed vs applied). Then: formatter + test results, and any baseline-regeneration flag. No essays.
