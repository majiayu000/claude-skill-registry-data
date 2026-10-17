---
name: record-hypothesis-before-fix
description: Required before any production-code edit during the red phase. Forces externalization of "why I think this fix will work" with cited test_error_id and stack_frame_id evidence.
---

# Record a hypothesis before a fix

Before editing production code in response to a failing test, call:

```text
hypothesis (action: record)({
  content: "<your hypothesis>",
  tddTaskId: <the id returned by tdd_task (action: start)>,
  citedTestErrorId: <test_errors.id from test_errors>,
  citedStackFrameId: <stack_frames.id from the same error>
})
```

## Rules

1. Pass `tddTaskId` (the id returned by `tdd_task (action: start)`) — it binds the hypothesis deterministically to your task's session. Do **not** pass a `sessionId`: the field is a dev/test fallback the server ignores when host context is available, and passing the tddTaskId value under the `sessionId` key misattributes the hypothesis to an unrelated session. Without a `tddTaskId` the server still resolves the binding session from the recovered host context, so omitting both ids is acceptable; a wrong `sessionId` is not.
2. Both `citedTestErrorId` and `citedStackFrameId` are required. A hypothesis without specific evidence is a vibe.
3. The hypothesis should describe a causal claim. "The validation function returns null because the type guard runs before the input is normalized" is a hypothesis. "Fix the validation" is not.
4. After the fix, validate the hypothesis: `hypothesis (action: validate)({ id, outcome: "confirmed" | "refuted" | "abandoned" })`.

## Why externalize?

The act of writing the hypothesis forces you to commit to a specific causal claim before you change code. If you can't write the hypothesis, you don't know enough to fix the bug yet — and your fix is statistically more likely to be a guess.

## Reusable outside TDD

Flaky-triage and fix-failing-test workflows use this. The compliance hooks (Stop, SessionEnd) prompt for hypotheses if recent file_edits aren't cited.
