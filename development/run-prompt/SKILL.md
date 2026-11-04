---
name: run-prompt
description: Run one or more Lanekeeper prompts end to end with subagents, spec first. Plans from the prompt, stops for human approval, implements task by task in an isolated worktree, runs the gates, has an independent reviewer check the branch, and fixes findings. Invoke as /run-prompt 04, /run-prompt 02 03a 04, or /run-prompt wave:1.
disable-model-invocation: true
argument-hint: "<NN ...> | wave:<N> [--pr] [--base REF] [--concurrency N]"
---

# /run-prompt

You are the orchestrator. You never write product code yourself. You create worktrees, spawn subagents, relay one human gate, and report. Keep your own context small: subagents return short summaries, and the files in the worktree hold the detail.

The spec chain is fixed: **prompt (spec) → plan (human approves) → one commit per task → evidence → independent review → PR.** A guard hook (`.claude/hooks/guard.mjs`) enforces the plan gate and the ownership rules inside the worktrees, so the subagents cannot skip steps.

Arguments: `$ARGUMENTS`

- Ids: `04`, `03a`, several ids, or `wave:N` (every build prompt in that wave).
- `--base REF`: branch to start from and to check dependencies against (default: the current branch).
- `--concurrency N`: how many prompts run at once (default 4).
- `--pr`: open a pull request when a prompt passes review. Without it, stop with the branch ready and the PR text written.

Helper: `node scripts/lk.mjs` (`list`, `info NN`, `deps NN`, `worktree NN`, `approve NN`, `status`). It prints JSON.

## 0. Select and check

1. Resolve the ids: `node scripts/lk.mjs list --wave N` for `wave:N`. Skip prompts whose wave is `v2` or `investigation`, and say so.
2. For each id, run `node scripts/lk.mjs deps NN --base REF`.
   - Unmet dependencies: do not start that prompt. Tell the user which prompts must merge first (a merged prompt shows up on the base branch as a commit whose subject starts `NN:`). Offer to run the others.
   - Manual conditions (design handoff, open questions): ask the user once whether each is satisfied. Continue only with a yes.
3. `node scripts/lk.mjs status` tells you where each prompt stands, so a re-run resumes: a draft plan goes to the gate, an approved plan continues at the next task without a commit, a finished evidence file goes to review.

## 1. Plan (parallel across prompts)

For each prompt, `node scripts/lk.mjs worktree NN [--base REF]` creates `.worktrees/NN-slug` on branch `agent/NN-slug`. Then spawn the `planner` subagent. Launch all planners in one message (respect `--concurrency`). Give each:

> Prompt `NN` (file from `lk info`). Worktree: `<path>`. Write the plan to `<path>/plans/NN-slug.md` from `plans/TEMPLATE.md`, commit it as `NN/plan: draft`, and return your summary.

Wait for all of them before the gate.

## 2. Human gate: approve the plans

This is the only routine stop. For each plan show, in a few lines: the task→commit list, `Extra-paths`, `Contract-change`, the open questions with their proposed defaults, and the path to the plan file so the user can read or edit it.

Ask with AskUserQuestion, one question per prompt (up to 4 per call), options:

- **Approve.** Run `node scripts/lk.mjs approve NN`.
- **Approve, including the listed Extra-paths and contract change.** Run `node scripts/lk.mjs approve NN --contract-change` when a contract change is listed; Extra-paths in the plan header are then approved with it. Say plainly what they are before you ask.
- **Needs changes.** Take the user's notes (an "Other" answer), re-run `planner` with them against the same worktree, and ask again.

Never approve for the user, never guess an answer to an open question that the plan marks "Needs a human", and never edit `Status` yourself.

## 3. Implement (task by task, fresh subagent each)

Pick the implementer from `lk info NN` → `stack`: `rust` → `rust-implementer`, `web` → `web-implementer`, `ops` → `ops-implementer`.

Run in rounds. In each round, for every active prompt, spawn one implementer for its next task, all in one message:

> Prompt `NN`. Worktree: `<path>`. Mode: `Tk`. Follow `.claude/protocols/implementer.md`.

Tasks of one prompt run strictly in order, because later tasks build on earlier commits. Prompts run in parallel with each other, since waves are designed to depend only on contracts and fakes.

Handle the result of each:

- `DONE`: confirm with `git -C <path> log --format=%s -1` that the commit `NN/Tk:` exists, then continue.
- `BLOCKED`: stop that prompt. Read `plans/NN-slug.blockers.md`, show the user the blocker and what you propose (a plan change needs a new approved plan; a missing path needs Extra-paths; a contract change needs the lanekeeper-contract-change process). Continue the other prompts.
- Anything else, or a missing commit: treat it as a failure. Retry the task once with the failure text. If it fails again, stop that prompt and report.

When the last task is done, spawn the same implementer once more with mode `FINAL`.

## 4. Review and fix (loop, at most 3 rounds)

1. Spawn `reviewer` (fresh context, read-only):

   > Prompt `NN`. Worktree: `<path>`. Base: `<base>`. Review the branch per `prompts/REVIEW.md` and return your verdict.

2. Save its output to `<path>/plans/NN-slug.review.md` and commit it as `NN/review: round R`.
3. `VERDICT: APPROVE` → go to step 5.
4. `CHANGES REQUESTED` → spawn the implementer with mode `FIX` and the blocking findings, then review again. After 3 rounds with blocking findings left, stop and report them to the user.

## 5. Finish

Write `<path>/plans/NN-slug.pr.md`: the PR body, following `.github/pull_request_template.md`, filled from the evidence file, and the reviewer's final verdict. Commit it as `NN/pr: body`.

- With `--pr`: push `agent/NN-slug` and open a pull request titled `NN: <prompt title>` with that body, using the GitHub tools available in this session. The `contract-change` label applies only when the plan's header says it was approved.
- Without it: do not push. Tell the user the branch, the worktree path and the PR text file.

Final report, per prompt: result (ready for human review, blocked, or failed), branch, commits (`NN/Tk:` count against the plan), gates, reviewer verdict and rounds, and anything that needs the human. Remind the user of the remaining human gates: review every PR, approve every `contract-change` PR, and answer the open questions.

## Rules for you

- Never edit product code, the plan file, hooks or settings. Never run `git push` unless `--pr`. Never force-push.
- Do not paste subagent transcripts back. Quote only verdicts, blockers and decisions.
- If a hook blocks something you did, that is the process working: report it, do not look for a way around.
