---
name: run-task
description: Run tasks or fixes end to end. OpenCode (or Claude) implements, a reviewer of another model family reviews, the main session merges and reports. Main session only.
---

# /run-task [T<nn> | #<issue> ...]

Read `docs/process.md` §3–§6 first. Given ids, run them in order; given none, take the first
`status:ready` task in `docs/tasks/README.md`. Report after each task; stop at any escalation.
For `#<issue>` of a bug labelled `fix`, the bug body replaces the task file, the branch is
`fix/<issue>-<slug>` (`--fix <issue>` in the scripts), and there is one review round.

0. **Check.** The issue is `status:ready` and every Merge-after task is merged. Run
   `gh issue list --label triage:needed --state open`; triage anything that names this task first.
   If `harness.json` has cutoffs for `breaks-play`, route those issues through Jev first (`/jev`
   step 4). Act on its confident ends and triage the middle yourself; exit 3 means triage it all.

   Run every Done-when line yourself: it must fail on `main` and pass on a mock fix (a scratch
   change, then discarded). A line that cannot is amended on `main` before dispatch (L45).

1. **Brief.** Write it to a temp file: the task file **pasted in full**, then `docs/process.md` §4's
   block, then (on rework) the review comment's URL. Never a pointer to the task file.

   **Watching background work (L48).** While any job runs in the background (an implement or
   review run, an agent, a long command), arm a watch: Claude Code's Monitor (30 minutes,
   re-armed until the work ends), or a background `until` loop where there is none. It reports
   each job's start and end, and flags a job whose log or output file has not grown for 10
   minutes as possibly stuck; check it is alive on its exact PID. The runner kills its own run at
   the idle limit (L10), so for an implement or review run the flag is a warning to read the
   output, not a reason to kill it; for an agent or a plain command it is the only watchdog.
   Never wait with `while pgrep -f '<pattern>'`: the waiting shell's command line contains the
   pattern, so it matches itself and waits forever. Chain jobs in one background command, or
   wait on the PID with `while kill -0 <pid>`. Tell the user at each start, end and flag.

2. **Implement.** Label `status:in-progress`. Use the task file's Implementer:
   - `opencode` (the default): run
     `node tools/harness/implement.mjs --task T<nn> --slug <slug> --issue <n> --brief <file>`
     with `run_in_background`, and watch it (below); never poll with sleep.
     - Exit 0: a PR is open. Note the `implemented by:` line.
     - Exit 1: read the log it names. An implementer that stopped and reported goes to step 5,
       or to a task-file amendment on `main` and a re-run.
     - Exit 3: OpenCode unavailable, its model not listed, or Go not logged in (the message gives
       the login command). Use the task file's Claude fallback (Sonnet by default), and say so in
       a comment on the issue.
   - **Read before you retry (L55).** Before a retry, a re-route to another model, or calling a
     run a failure, read what it returned; never retry blind. An OpenCode exit 1 with an empty
     diff looks the same for an early end and for a run that stopped and reported a blocker, and
     the log's tail shows only the last tool output. Read the model's final message from the
     session record, read-only (never `auth.json` in that directory), with the `session ses_…` id
     from the run's log:
     ```bash
     python3 - <<'EOF'
     import sqlite3, json, os
     home = os.environ.get('HARNESS_OPENCODE_HOME') or os.path.expanduser('~/.local/share/harness-opencode')
     db = 'file:' + os.path.join(home, 'data', 'opencode', 'opencode.db') + '?mode=ro'   # the scripts' data directory
     c = sqlite3.connect(db, uri=True)
     sid = 'ses_...'   # the "session ses_..." line in the run's log
     parts = [json.loads(d) for (d,) in c.execute("select data from part where session_id=? order by time_created", (sid,))]
     texts = [p for p in parts if p.get('type') == 'text']
     print(texts[-1]['text'] if texts else 'no text part')
     EOF
     ```
     For a Claude agent, read its final report in full. A run that stopped and reported gets an
     answer to its report (amend the task, decide, or escalate), and the report is posted on the
     task's issue so it is kept.
   - `claude`: `Agent(subagent_type: "implementer", isolation: "worktree")`, Sonnet unless the
     task file names opus, with the brief. The agent file (`.claude/agents/implementer.md`) carries
     §4's block and the run mechanics, and its hook refuses `git stash`, `git worktree`, a
     force-push and `gh pr merge`.

3. **Review.** Label `status:in-review`. Use the task file's Reviewer, never the implementer's
   family:
   - `opencode` (the default, GPT-5.6 Luna on the direct OpenAI route): `node tools/harness/review.mjs
     --pr <pr> --brief <file> --exclude <implemented by> --issue <n> --apply-label`, in the
     background; a hard task adds `--hard` (GLM-5.3, then another provider when it cannot run,
     L39), and a guard task or the last round (`review-round:2`, `:1` for a fix) also `--sol`
     (GPT-6.1 Sol at low effort first, L41). Name the PR's head in the brief only after the push
     has landed: take it from the local branch (`git rev-parse <branch>`). A brief whose block
     before the task file names another commit exits 2 before anything runs (L33).
     - Exit 0: posted and labelled.
     - Exit 3: no review came back, or OpenCode or its login is unavailable (read the run's final
       message first, as under step 2's *Read before you retry*). Nothing was posted:
       run the Claude reviewer (Opus). If a Claude agent implemented the PR, Claude may not
       review it either (the family rule): escalate (step 5).
     - Exit 4: a review was posted whole under a note (it may be cut off, its verdict is
       unreadable, its verdicts differ, or a finding follows its closing verdict), or an approve
       left a Done-when line unaccounted for or not run (L32). No label was applied. For a
       missing `DW` line, run a supplementary review of those lines alone, or send it to rework. Read it on the PR
       and decide: apply the label it supports, or escalate. Never pay for a second review just
       because the first was flagged.
   - `claude` (the fallback): first `git fetch origin pull/<pr>/head`, since the reviewer has no
     GitHub credentials (#68); then `Agent(subagent_type: "reviewer", isolation: "worktree")` (Opus),
     with §5's brief filled in. The agent file carries the rest; its hook refuses every write. It
     **returns** its review: save its final message to a file, then post it with
     `node tools/harness/post-review.mjs --pr <pr> --brief <brief> --review <file>
     --by "claude (opus)" --issue <n> --apply-label`. Its exits are review.mjs's, but 1 means no
     review was in the message: re-run the reviewer once, then escalate.
   - Architecture task: also `/code-review <pr>`, always with the number.

4. **Decide** on the label the reviewer applied.
   - `status:approved`:
     1. Wait for green CI.
     2. Re-run the check the approval rests on most (the Done-when line or the mutation that
        proves the task) on the PR's head yourself. A different result is rework, not a merge (L46).
     3. `gh pr merge <pr> --squash --delete-branch`, then label `status:merged`.
     4. File one `T<nn> follow-up` issue (`triage:needed`) for the non-blocking findings.
     5. Unblock the tasks whose Merge-after are now all merged.
     6. Remove the task's worktrees.
     7. Post §9's measurement comment on the PR.
     8. Report the merge, the findings, the follow-ups and what is ready next.
   - `status:rework`:
     1. Check that every finding names a file in `gh pr diff <pr> --name-only`. A review that
        does not reviewed the wrong tree: discard it, say so, and re-review.
     2. At `review-round:2` (at `review-round:1` for a fix), go to step 5.
        A reviewer that reports one blocking finding per round despite the brief's one-pass
        section (L49): after the second such round, stop. Request no further review until you
        have gone through the whole diff yourself for that class and fixed what you found, and
        recorded the pattern in the model-trials record. The review after that is the task's last
        before escalation (step 5).
     3. **A heavy review moves the implementer up (L38)**, decided before the next round starts.
        The review just posted is heavy when it asks for rework with three or more blocking
        findings, or when it brings new blocking findings of a class the previous round raised:
        the same kind of defect again, in new or unchanged code (a sibling the last round missed
        counts). Then the next round goes one step up the ladder: a light OpenCode model → a
        heavy one → a Claude Opus agent (where the owner pairs by difficulty: GLM-5.3 Flash →
        MiMo V2.6 Flash → Opus), and Sonnet → Opus; never down within a task. At the top
        there is no stronger model: the round fixes the class as below, and changes the approach
        when the class needs it (as golden screenshots did in malpaco T02), saying so on the task file.
        - The round count does not reset, and the reviewer stays of another family: with Opus
          implementing, no Claude reviewer may review; if the OpenCode reviewers fail, go to step 5.
          The Done-when is never weakened for the stronger model.
        - Hand-over: stop the current implementer if it is mid-round; save its unpushed work as a
          patch (`git add -N` new files, then `git diff > <patch>`); start the new implementer on
          the pushed branch with the task file pasted in full, every review so far (the current
          one pasted in full), the patch path "to weigh, never to apply blindly", and the
          instruction to fix the class of the findings, not each instance, then sweep its own
          code for the same class and list the sweep in the PR body.
        - Record the change on the task file's Implementer line, committed on `main`, with the
          reason: the blocking counts, and for a repeated class, the class and the finding ids of
          both rounds (e.g. "R1–R2 of round 0 and R3 of round 1: an alias at write time"). After
          the round, the measurement comment (§9) gives the models, the trigger, the classes, the
          blocking counts before and after, and whether it converged.
     4. Set the next round and return to step 1, with the full review's URL in the brief (and,
        after step 3, the hand-over's). The implementer script resumes the branch.

5. **Escalate** (`docs/process.md` §7): label `status:escalated`, comment the evidence on the issue,
   and bring the user the decision with options and a recommendation. Stop.
   A defect found in merged code outside the task is filed as a bug (`triage:needed`). If it
   blocks the task: a one-file mechanical fix may ride this PR, declared under Scope; otherwise
   label the task `status:blocked` and stop.

Never:
- merge without an approving review and green CI;
- weaken a Done-when;
- let the implementer's model family review its PR;
- relay part of a review;
- dispatch a `model-driven` task before its carve-out's table and gate are merged (process.md §10, L63);
- force-push or rewrite `main`.
