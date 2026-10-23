---
name: receiving-review
description: "Use when feedback on your own change arrives (a reviewer's comments, a list of findings, a bot report) and before acting on any of it: verify each point against the code, stop on an unclear one, answer with substance instead of agreement. The detailed mechanics (order of fixes, pushback, thread replies) are receiving-review-pitfalls."
---

# receiving-review

The author's side of `review` (step 8 of `WORKFLOW.md`) and of `mr-conventions` §4. A reviewer judges a diff; this block
decides what the author does with the judgement. The failure it prevents runs in both directions: implementing a
suggestion that was wrong, and performing agreement instead of doing the work.

The longer treatment (reading order, applying fixes, pushback with evidence, thread replies) is `skills/receiving-review-pitfalls`; this block stays the short rule set.

## When
Any time a comment, a findings list or a bot summary about your change reaches you, from a human, a fresh-context
reviewer or a tool. Also when you are about to reply "done" to such a list.

## Steps
1. **Read the whole list before reacting to any item.** Items interact: a later comment often explains or
   contradicts an earlier one, and a fix made after reading half of them is rebuilt after reading the rest.
2. **Restate each item as a requirement in your own words.** If you cannot, the item is unclear; that is a
   finding about the feedback, not a gap in your effort.
3. **One unclear item stops all implementation.** List which items you understood and which you did not, ask
   about the second group, and change nothing until they are answered. Items are often coupled, and a partial
   understanding applied now is rework later.
4. **Verify each item against the code, not against the reviewer's description of it.** Open the lines. Does
   the problem exist as stated? Is there a reason the code is the way it is (a compatibility window, an earlier
   decision, a constraint the reviewer could not see)? A comment you have not checked is an opinion.
5. **Evaluate it for this codebase.** Would the change break existing behaviour? Is it correct for the versions
   and platforms in use? Does it contradict a decision the operator already took? If so, stop and raise it with
   the operator rather than silently choosing a side.
6. **Run the usage check on "do it properly" suggestions.** When a reviewer asks for a fuller version of
   something (metrics, an export, a configuration surface), search for who actually uses it. Unused: propose
   removing it. Used: do it properly. A feature added because a review made it sound professional is a feature
   nobody asked for.
7. **Implement in order, one item at a time:** blocking problems (breakage, security, data) first, then simple
   fixes, then structural ones. Run the covering test after each item, not once at the end.
8. **Answer each item with one of two outcomes**: the fix, stated in a line ("fixed: the guard now covers the
   empty case, line 42"), or a reasoned refusal ("left as is: the second caller needs the legacy shape, see
   the migration window"). Reply inside the thread the comment lives in, not as a separate top-level message.

## Output / checkpoint
Every item has either a verified fix with its test run, a reasoned refusal, or an open question to the
reviewer. No item is silently dropped, and no item was changed that was not understood.

## Guardrails
- **Nothing is implemented from feedback that has not been understood and checked against the code.** This is
  the law of the block; everything above applies it.
- **No performative reply.** Not "you are absolutely right", not "great catch", not thanks in place of a
  fix. The diff is the acknowledgement. If you notice yourself drafting a pleasantry, replace it with the
  change it was about to stand in for.
- **Pushback is technical and specific**: name the line, the test or the constraint, ask the narrow question.
  It is not defensive, and it is not avoided because it is uncomfortable; a wrong suggestion implemented to
  keep the peace is still wrong.
- **If you pushed back and were wrong, say so in one factual line** ("checked, the reviewer is right: the call
  returns null on a miss; fixing") and move on. No apology paragraph, no defence of the earlier answer.
- **Feedback you cannot verify is said to be unverifiable** ("cannot confirm without running the migration on
  production-shaped data; should I?"), never implemented on faith and never dismissed.
- **A reviewer's finding from an automated tool is a lead, not a verdict.** It gets the same check as a human
  comment, including the possibility that it is a false positive.
- Never resolve a thread you did not answer, and never resolve it before the code answers it.

| Thought | What to do instead |
|---|---|
| "I will just do all of them and ask later about the odd ones" | Step 3. The odd ones change how the others should be done. |
| "The reviewer clearly knows this part better than I do" | Step 4. Knowing the area is not the same as having read this diff against the code today. |
| "Arguing is not worth it for a small item" | Implementing a wrong small item costs a later revert and a confused history. Say it in one line. |
| "They asked for it, so it must be wanted" | Step 6. Check use before building. |
| "Saying thanks costs nothing" | It replaces the one thing that does: the change and its test. |

These excuses are predicted, not recorded. Replace them with the sentences a run without this block really
produced (`skills/testing-blocks` §1) when one exists.

## Origin
The `receiving-code-review` skill of `superpowers` (MIT, read 2026-10-02): the response order, the stop on an
unclear item, the usage check on suggestions that add scope and the ban on performative agreement. Rewritten
in our words and extended with the unverifiable-feedback case and the thread-reply rule. The review comment
style a reviewer writes in is `skills/mr-conventions` §4; this block starts where that one stops.
