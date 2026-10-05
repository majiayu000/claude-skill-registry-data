---
name: mature-resolve-ticket
description: >
  Resolve a confirmed defect surfaced in the mature phase by running a scoped
  pass of the development cycle. Use when a triaged work item is a reproducible
  bug ready to fix: phrasings like "fix MN-42", "this defect is confirmed, go
  fix it", "resolve the bug from triage", "take this confirmed defect through
  the dev cycle", or when mature-analyze-ticket has handed off a confirmed
  reproduction. This is a thin entry point that frames the defect and delegates.
  Do NOT use to triage or confirm an issue first (that is mature-analyze-ticket),
  to build a new feature or make an ad-hoc code fix with no triaged ticket (use
  create-code-generation directly), or for a pure structural cleanup with no
  behaviour change (that is create-refactoring).
---

# Mature ticket resolution

Owned by the **Developer** persona (the resolve-ticket step). Invoked as `/mature-resolve-ticket`.

Resolve a confirmed defect from the mature phase by running a **scoped pass of the development
cycle**. This skill is deliberately a thin entry point: it does not re-implement the build steps.
It frames the fix around the triaged work item and its confirmed reproduction, then hands the full
sequence to `create-code-generation`.

The input is a **triaged, confirmed defect** from `mature-analyze-ticket`: a work item with a known,
reproducible failure. If the issue is not yet confirmed, stop and run `mature-analyze-ticket` first.

## Frame the defect (the only defect-specific work)

1. **Start from the triaged work item and its reproduction.** Restate the confirmed failure and
   verify the reproduction actually fails today before changing anything. Name the suspected root
   cause as a claim to confirm against the code.
2. **Branch first.** Create the development branch named for the work item key (the bare key,
   e.g. `MN-42`). Confirm the correct base branch first, pull it up to date, then branch off it.
3. **Write the failing test first (red).** Add a test that reproduces the defect and fails for the
   right reason. Tag it with the story ID (`[Trait("Story","MN-42")]`).
4. **Keep the fix minimal.** Change only what makes the red test green.
5. **Confirm green, both narrow and broad.** The new test passes, and the broader suite is still
   green.
6. **Ensure traceability.** The fix carries the `[Trait("Story", ...)]` tag and links back to the
   work item file.

## Delegate the rest to create-code-generation

Hand the sequence to `create-code-generation` (Developer): plan, TDD (from the failing test above),
coverage, docs, ADR if needed, work item enrichment, review, and PR. Do not re-document those steps
here.

## Guardrails

- **Thin entry point.** Frame the defect, write the red test, then delegate.
- **Red before green, always.**
- **Root cause, minimal scope.** Fix the cause; adjacent refactors go through `create-refactoring`.
- **Verify before asserting.** Run tests, do not assert by inspection.
- **No em-dashes, no AI attribution, no source line numbers.**

## Next steps

- `/create-code-generation` (Developer) - run the scoped cycle for this defect.
- `/governance-enrich-ticket` (any) - record the fix and root cause on the work item.
- `/create-verify-test-coverage` (QA) - confirm the regression test holds and coverage stays above C09.
