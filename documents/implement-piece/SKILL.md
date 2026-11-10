---
name: implement-piece
description: "Implement a writing Piece spec into its Deliverable, review it with /review-piece, fix the hard findings and report the rest, then commit its Agent draft. Invoked as /implement-piece <repo> <n>."
argument-hint: "<repo> <n>"
disable-model-invocation: true
---

`/implement-piece <repo> <n>` implements the Piece described by the spec or sub-issue `<repo>#<n>`.

Fetch it with `npm run issue:read -- <repo> <n> --body --comments` and state its title before starting. If the reference is ambiguous, ask. If the issue is Research, read [`.claude/skills/research-piece/SKILL.md`](../../../.claude/skills/research-piece/SKILL.md) and follow it on the same issue instead; it is user-invoked, so the Skill tool can't reach it.

**Work in the Piece's issue workspace.** If this session did not start at its root, run `npm run issue:start -- <repo> <n>` from the primary root and tell the developer to start `/implement-piece <repo> <n>` at the path it prints; stop there.

Draft by the rules under "Implementing a piece spec" in [`docs/pieces/rules.md`](../../../docs/pieces/rules.md): its text, its supporting material, when it may write without asking, its style and the Outline. On a sub-issue, write only the Sections it names.

Once drafted, read [`.claude/skills/review-piece/SKILL.md`](../../../.claude/skills/review-piece/SKILL.md) and follow it on the same issue. It is user-invoked, so the Skill tool can't reach it.

Then:

- **Fix every hard Spec finding** in the Deliverable. After fixing copied wording, rerun review-piece's Overlap command on the Deliverable as it is now, and judge any new hit the same way.
- **Report the Spec judgement calls, the Voice, Craft and Reader findings to the developer, unfixed.** They are judgement calls, and the developer's own edits are what `/to-writing-style` learns from.

Done when no hard finding is left, or each one left is reported with why.

**Last, save the Agent draft, every time, without offering.** Its path, its shape and how a save replaces its blocks are in [`docs/pieces/agent-draft.md`](../../../docs/pieces/agent-draft.md).

1. `get_doc_as_markdown` the Deliverable as it is now, after the fixes.
2. Save the Sections this issue drafted into the Agent draft. A later revision round saves the Sections it changed the same way.
3. Commit only the Agent draft, in `<repo>`'s clone in the workspace on its `issue-<n>-<slug>` branch: `git -C <clone> add writing/snapshots/<spec n>.md`, then `git -C <clone> commit -m "Agent draft of <repo>#<n> before review."`, "review" being the developer's.

**End with the landing, which waits for the developer's review.** Ask which model and effort pair ran this and each implementing session's peak `/context`. Then write the wrap-up facts per "Landing a spec" in [`docs/agents/git-workflow.md`](../../../docs/agents/git-workflow.md): the Piece's branch as the only branch, the Deliverable's link in the closing comment, and their answers as `pair` and `peakContext`. Tell them to run `npm run wrap-up -- <repo> <n>` once they've finished editing; it lands the Agent draft, records the outcome row and closes the issue.
