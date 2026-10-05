---
name: elaboration-upsert-user-story-acceptance-criteria
description: >
  Derive clear, testable acceptance criteria for a story and define the
  test-trait mapping that lets the deferred AC-coverage gate attach with no
  rework. Use when the user says "write the acceptance criteria", "define the
  ACs for MN-42", "what are the success criteria for this story", "make
  these criteria testable", "turn this story into checkable conditions", or
  "set up the AC-to-test mapping" - and when a story is being refined for build
  but its success criteria are vague or untestable. Do NOT use to CREATE the
  story (that is elaboration-upsert-user-story), to implement or tag the tests
  (that is create-code-generation), or to write the work item fields directly
  (defer that to governance-enrich-ticket).
---

# Acceptance Criteria

Owned by the **Product Manager** and **QA** personas (shared). Invoked as `/elaboration-upsert-user-story-acceptance-criteria`.

Turn a story's intent into acceptance criteria that are specific and checkable, and define
the trait scheme that maps each criterion to its covering test(s). The point is twofold:
the criteria tell the developer and reviewer when the story is genuinely done, and the
trait mapping is the hook the future AC-coverage gate keys off.

## What a good acceptance criterion is

- **Specific and observable.** Each criterion states a condition someone can check by
  looking at behaviour, not a feeling.
- **Outcome, not implementation.** Describe the behaviour the user gets, not the code path.
- **One assertion each.** Split compound criteria so each maps cleanly to a test.
- **Covers the edges.** Include the empty state, the identical case, the unaffected
  neighbour, and the error path.

## Where the criteria live

Acceptance criteria are the story's `## Success Criteria` section in its markdown file under
`docs/discovery/stories/`. They are written into the work item file by **read-merge-write**:
read the current file content, splice into the Success Criteria section without disturbing the
rest, confirm the full diff, then write. Use `/governance-enrich-ticket` for the write, or
apply the same read-merge-write discipline directly.

## The AC-to-test trait scheme (the gate hook)

Number the criteria stably (`AC-1`, `AC-2`, ...) and require each covering test to carry:

- `[Trait("Story","MN-42")]` - the story tag for traceability.
- `[Trait("AC","AC-3")]` - the per-criterion tag for the gate.

A criterion that is genuinely not unit-testable (a manual or visual check) is marked as such.

```
## Success Criteria

* AC-1: The user can choose a left and a right version from the list of versions.
* AC-2: Selecting two versions renders the aligned diff of exactly those two.
* AC-3: Selecting the same version on both sides shows a clear "identical version" state.
* AC-4: The existing automatic panel is unaffected.

(Test traits: each AC covered by xUnit tests tagged [Trait("Story","MN-42")] +
[Trait("AC","AC-n")]; AC-4 verified by the unchanged-panel regression test.)
```

## Workflow

1. **Resolve the story.** Take the key (e.g. MN-42) or the story file path. Read its goal,
   expected value, and current Success Criteria.
2. **Derive the criteria.** From the goal and value, write each condition as one specific,
   observable assertion. Add edge/error cases. Verify load-bearing claims against the codebase.
3. **Number and map.** Assign `AC-n` and state, per criterion, the covering test and its two
   traits (`Story` + `AC`). Flag any that is not unit-testable.
4. **Confirm before writing.** Present the full Success Criteria section and the trait mapping.
5. **Write via enrich-ticket or directly.** Splice into the story file, confirm the diff landed.

## Guardrails

- **Checkable, not vague.** Reject "works", "is fast", "is intuitive".
- **Read-merge-write, confirm before write.** Splice into the Success Criteria section only.
- **Keep the trait scheme intact.** Both `Story` and `AC` traits are load-bearing for the gate.
- **Verify before asserting.** Behavioural claims behind a criterion are checked against the
  code first.
- **No em-dashes, no AI attribution, no source line numbers.**

## Next steps

- `/create-code-generation` (Developer) - implement test-first against these criteria,
  tagging each test with the `Story` and `AC` traits defined here.
- `/governance-enrich-ticket` (any) - write the criteria onto the work item if they are not
  already there.
- `/create-verify-test-coverage` (QA) - verify each AC has a covering test.
