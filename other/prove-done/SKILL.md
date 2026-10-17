---
name: prove-done
description: Shows evidence that a branch meets its spec's success criteria and lists every spec change since approval. Use when a branch's work is finished and reviewed, before finishing the branch or opening a pull request; also when asked to prove a change is done.
---

# Prove Done

A claim that work is done is only as good as the command output behind it. This step turns the spec's success criteria into evidence your partner can check, and shows every change of direction made since the spec was approved.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

1. Run the project's full test suite, linter and build fresh on the current state of the branch. Read the whole output and the exit codes.
2. List every change to the spec since it was approved, from its `Changed` notes, and, when the plan's `Spec:` line names a commit, check them against `git log -p <commit>..HEAD -- <spec>` and `git diff HEAD -- <spec>` for edits without a note.
3. For each success criterion in the spec as it stands now, name the test or command that shows it holds, and its result. With no spec, use the requirements the review used, or ask your partner for them. Mark any criterion nothing demonstrates. Where the code and the spec disagree, never mark that criterion as passed: ask your partner which side should change, with your recommendation. To change the code, use the `dietpowers:tdd` skill, which commits the fix, and run step 1 again. To change the spec, invoke the `dietpowers:update-spec` skill.
4. Report: pass or fail, the criteria with their evidence, the spec changes, and anything unmet. State only what the output shows.

Evidence for common claims:

| Claim | Evidence |
|---|---|
| Tests pass | Test command output showing 0 failures |
| Linter clean | Linter output showing 0 errors |
| Build succeeds | Build command exiting 0 |
| Bug fixed | The original symptom retested, now passing |
| Regression test works | Reverted the fix, watched the test fail, restored it |
| A subagent finished | The VCS diff, not the agent's report |
| Requirements met | Each spec success criterion paired with the test or command that shows it |

Terminal state: if the `dietpowers:handle-feedback` skill invoked you, return to it. Otherwise, if everything passed and every criterion is shown, invoke the `dietpowers:finish-branch` skill; if not, report what is unmet and stop.
