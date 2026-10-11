---
name: revive
description: Bring cut-off work back exactly where it stopped after a usage limit, a crash, a restart or a compaction, without doing anything twice. Use when a session resumes after a limit or crash, when agents or background tasks died mid-work, or when asked to continue, resume or revive.
---

# revive

A limit or a crash stops work mid-stride. Some units finished, some died halfway through a commit, a merge or a pull
request, some never started. Reviving means every unit continues from its real **edge**, the last thing that
verifiably happened, and nothing is done twice or dropped.

The **world** decides. That means the actual state of the repositories, pull requests, CI, background tasks and
the clock. It outranks summaries, memory and your own earlier messages, which describe the moment before the cut.

## Order

1. **Read the clock and the world.** Run `date`; hours may have passed. Then gather every source that says what was
   running, because a unit nobody lists is forgotten work:
   - the conversation or its compaction summary: the latest requests, and every promise in your own last messages
     ("I'll…", "next…");
   - subagents, with their names and last reports;
   - background tasks and their output files;
   - loop or goal state files, status docs and worklogs the work keeps;
   - for each repository and worktree: `git fetch origin` and `git worktree list`, then `git status`,
     `git log origin/<branch>..HEAD` and `git log HEAD..origin/<default>`; when `origin/<branch>` does not exist,
     the branch was never pushed, so read `git log origin/<default>..HEAD` instead; then the open pull requests
     with their checks and the recent merges.

   Done when every unit any source names is listed.
2. **Write the ledger.** One row per unit, with its state and one line of evidence, taken from the world and never
   from the plan:

   | State | Evidence |
   |---|---|
   | done | a merged commit on the remote default branch, a closed ticket, a sent message you can see |
   | pushed | commits on the remote branch or an open PR, review or merge not finished |
   | partial | uncommitted edits, local unpushed commits, or a half-done merge or rebase (`UU` files, `MERGE_HEAD`) |
   | dead-clean | the worker died before touching anything |
   | not started | named in a plan or a promise, with no trace in the world |

   A review round in which any reviewer died is not run, never clean. A missing worktree with a merged PR is done;
   without one it is lost work, so partial or not started. A task with no end notice is live until the harness says
   it ended. Done when every row has a state and evidence, and no row relies on absence alone.
3. **Check the capacity.** A relaunch on the window that just closed dies again at once. Confirm the account or
   model can serve the work, and keep any model choice the user made. Done when the next launch can run.
4. **Revive each unit from its edge.**
   - A subagent that still has its context: continue it with a message that gives only the delta, what moved in the
     world while it was gone.
   - A worker that must start fresh: hand it its ledger row and this opening: the previous attempt died mid-work;
     before writing, run `git fetch origin`, `git status`, `git diff` and `git log origin/<branch>..HEAD` (or
     `origin/<default>..HEAD` for a branch never pushed) and read the PR's comments,
     keep every edit that is right and finish it, complete a half-done merge, then continue.
   - Never send a new message to a worker inside a running orchestrated run; that starts a second writer on the same
     branch. Stop the run and relaunch the unit with its edge.
   - A resumed run that replays cached steps: within a few minutes, list what is running. Only the dead or unstarted
     units should be live. If finished units are running again, stop the run and relaunch with each unit starting
     at its edge.
   - Watchers, monitors and holds died with the process. Re-arm each one that still guards something.

   Done when every row that is not done is running again or reported as deliberately left, with the reason.
5. **Write only through a world check.** Before each outward action, look at the world and act only on the gap:

   | Action | Check first |
   |---|---|
   | commit | `git status`, then `git log -S'<text>'` and `git diff origin/<default>`: is the change already there? |
   | push | `git log origin/<branch>..HEAD` is not empty |
   | open a PR | `gh pr list --head <branch>` shows none open |
   | merge | `gh pr view <n> --json state,mergeCommit`; if it is already merged, report that commit and move on |
   | comment, issue, message | search the existing ones for the same content |
   | release or tag | the tag and the release do not exist yet |

   This holds inside one worker too: one that died after pushing and before commenting resumes at the comment.
   Done when every write in the revive passed its check.
6. **Report.** What died and where each unit stood, what was revived and the proof the replay was clean, what was
   stopped or left and why. Put the ledger where the next session will find it: the work's status doc or worklog if
   it has one, otherwise the reply. Done when the user has the report and the ledger is saved.

## Rules

- Launch or resume work only in a turn whose latest user message asks you to act. When the latest message is a
  question, answer it and ask for a one-word go.
- The work already done is paid for. Read what a dead worker produced (pushed commits, its worktree, a half-written
  report) before deciding anything is lost, and never re-run a finished unit to be safe.
