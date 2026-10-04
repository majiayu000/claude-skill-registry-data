---
name: no-comments
description: "Use before review, or when asked to clean up comments. Spawns a comment reviewer with no attachment to the code, acts on what it flags, and offers to turn any real constraint into a type, test, or lint before deleting the comment that described it."
disable-model-invocation: true
---

# No comments

The agent that wrote the code will defend its comments. So spawn a reviewer that didn't write it, with one job: find comments that shouldn't exist. Then act on what it finds.

## Scope

The files or diff the caller names. Otherwise the current diff against the base branch, working tree included.

## Steps

1. **Spawn the reviewer.** One subagent with `references/reviewer-prompt.md` and the scope. It reports. It never edits application code.
2. **Audit the report.** Reject anything outside scope, any application-code edit, any deletion the keep list protects, any MUST KILL whose stated reason doesn't match the code. A keep survives only with proof it's about something we can't change. Check that scoped lint and type suppressions were covered. An ambiguous kill stays killed. A keep that's refuted or still ambiguous gets deleted. For a thin "IMPORTANT, do not remove", run `how` or `why` on the symbol before deciding. If the report is bad, rerun once with the failure named. A second bad report, stop and say so.
3. **Fix the easy flags directly.** Delete the dead path, drop the parameter, use the real API. If a flag needs a new shape, run `architect` once for the accepted set and stop at the sketch.
4. **Fix the causes, in scope.** Smallest root-cause fix. Remove every named workaround. If the cause is outside the diff, land the smallest in-scope fix and report the rest as open. Don't widen the fence.
5. **Constraint comments.** "Do not remove", "do not change wording", "talk to X first". Keep the ones about things we can't change. For the rest, offer the cheapest encoding: a type, a runtime check, a test, or a lint rule. If the human approves, encode then delete. If not, delete anyway and report the constraint as unenforced.
6. **Report.** Deletions, restored comments, reruns, any architect sketch, fixes, encodings offered and made, constraints left unenforced, other open work.
