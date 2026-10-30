---
name: clear-water
description: Katara clears the muddy water so the bottom shows. Use for no-comments, /no-comments, "remove the comments", "comment review", or before every review. Runs a fresh comment-reviewer pass over the diff, fixes the accepted findings at the root, and offers a type, test, or lint that encodes each claimed constraint so its comment can go.
---

# Katara clears the water

Clear water needs no label. You can see the bottom. Code is the same. When a comment explains a surprise in our own code, the surprise is the mud, and the fix is to reshape the code until it reads plainly.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Dispatch the comment reviewer, then act on the findings you accept. Defer to its fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch (default `main`), including the working tree.

## Steps

1. **Dispatch the reviewer.** Dispatch `team-avatar:katara` on the `katara` line of the avatar-setup sheet, with the brief [references/comment-reviewer.md](references/comment-reviewer.md). Tell her to read that file in full and follow it, and pass the scope. Do not restate its rules. Pick the reasoning effort for the job (the Agent tool's `effort` parameter on Claude Code). When you are already a subagent and cannot dispatch, run the brief yourself as a separate pass before you read your own earlier work, and say so in the report.
2. **Inspect its report and diff.** Reject application-code edits, scope escapes, deletions of comments the brief protects, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on surprises in our own code stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit any scoped lint and TypeScript suppressions it missed. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore a deletion only with an exact keep-list exception and scoped proof. Before accepting a thin kill or keep of an `IMPORTANT` or `do not remove` comment, run `seismic-sense` or `past-lives` on its symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. If you reject a report, revert it and rerun the reviewer once with the failure named. If you reject the second report too, report it open and fail the pass.
3. **Fix trivial accepted flags directly.** Delete a dead path, drop a parameter, or call the real API. If any fix needs a new shape, run `war-room` once for the accepted set and the code around it. Stop at the sketch. The war room shapes. Step 4 implements.
4. **Implement the smallest root-cause fix in scope.** Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. Fix Root Causes and Redesign from First Principles (Water in `four-elements`) guide intent only. Neither one widens the scope or authorizes fixing instances outside it. Never bolt on symptom guards.
5. **Encode constraint comments.** A constraint comment says `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. For the rest, offer the cheapest in-scope type, runtime check, test, or CI lint that enforces the constraint. Wait for approval in an interactive session. Unattended runs and evals need the caller's approval up front. If approved, encode the constraint, then delete the comment. Otherwise delete the comment, report the constraint open, and sketch the out-of-scope work.
6. **Report.** The deletion count, restored comments, reruns, the war-room sketch, fixes, encoding offers, encodings landed, constraints left unenforced, and other open work.
