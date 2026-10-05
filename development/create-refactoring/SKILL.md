---
name: create-refactoring
description: >
  Improve the internal structure of existing code without changing its
  observable behaviour. Use when the user says "refactor this", "clean this
  up", "simplify this", "extract a method/class", "rename for clarity", "reduce
  this duplication", or "tidy this without changing behaviour". The defining
  constraint is behaviour preservation: the tests pass before and after, and the
  public contract is unchanged. Do NOT use to add or change behaviour, fix a bug,
  or build a feature (that is create-code-generation), and do NOT use to delete
  dead code as the primary goal.
---

# Create Refactoring

Owned by the **Developer** persona (the create-refactoring step). Invoked as `/create-refactoring`.

Improve the internal structure of code that already works, **without changing what it does**.
The whole skill turns on one constraint: observable behaviour and the wire contract stay
identical. The proof is the tests, run green before you start and green again after every step.
If you find yourself wanting to change a return value, a status code, a JSON shape, or any
externally visible behaviour, that is a feature or a fix, not a refactor: stop and use
`create-code-generation` instead.

## Reuse the agent's refactor capability

Do not re-implement refactoring mechanics here. Drive the change through your agent's existing
refactor flow and let this skill enforce the discipline around it:
- In Claude Code: the `refactor-clean` skill, or `simplify` / `code-simplifier` for structural
  cleanups. Use whichever fits; this skill supplies the safety net and the constitution check.
- In Copilot or other agents: use the agent's own refactor / cleanup flow.

This skill's job is the guardrails, not the edits.

## Workflow

1. **Scope it.** State precisely what structure changes and why (readability, duplication,
   coupling), and what stays the same. The behaviour and the public surface are out of scope to
   change. Keep it small; one structural intent per pass.
2. **Establish the safety net (green BEFORE).** Run the tests for the affected projects and confirm
   they pass before touching anything (`dotnet test MindNova/MindNova.sln`, or the narrower project).
   Verify this; do not assume it. If coverage over the code you are about to move is thin, **write
   characterization tests first** that pin the current behaviour, and get those green before refactoring.
3. **Change in small steps.** Make one structural move at a time (extract, rename, inline, split,
   dedupe), re-running the relevant tests after each so a break is localised to the last step. Prefer
   many small verified steps over one large rewrite.
4. **Verify (green AFTER).** Run the full affected test suite again. It must pass with no test
   assertions changed to accommodate new behaviour: if a behavioural test needed editing, behaviour
   moved and this is no longer a refactor. Coverage on the changed projects must not drop below the
   C09 bar (>= 80%).
5. **Confirm contracts held.** The public API and the **PascalCase JSON wire format (C06)** are
   unchanged; logging still goes through `_logger.LogMindNova(...)` (**C05**); no clause in `AGENTS.md`
   is newly violated. If the move touched a controller, it stays thin and single-domain (C07).

## Guardrails

- **Behaviour preservation is the contract.** Green before, green after, no behavioural test rewritten.
  If you cannot keep the tests green without changing what they assert, this is not a refactor.
- **No behaviour-adding "improvements".** Stay scoped to structure. New validation, new fields, changed
  responses, or "while I am here" fixes belong in `create-code-generation`, not here.
- **Honour the constitution.** C05 (LogMindNova), C06 (PascalCase wire), C07 (thin controllers), C09
  (coverage) must survive the refactor intact.
- **Usually no new graph artifact.** A refactor opts nothing new into the artifact graph; it changes
  structure, not work products. If the refactor embodies a load-bearing structural decision (a new
  boundary, a pattern swap), record that as an ADR via `governance-author-adr` rather than burying it
  in the diff.
- **No em-dashes, no AI attribution, no source line numbers** in any artifact or commit text; reference
  code by file path + symbol.
- **Verify before asserting.** "The tests pass" and "behaviour is unchanged" are claims you confirm by
  running the suite, not by inspection.

## Next steps

- `/create-verify-test-coverage` (QA) - confirm coverage held and the characterization/behavioural tests still pass after the move.
- `/create-upsert-documentation` (Tech Writer) - only if internal-structure docs (architecture, libraries) reference what moved or was renamed.
- `/governance-author-adr` (Architect) - only if the refactor embodies a load-bearing structural decision worth recording.
