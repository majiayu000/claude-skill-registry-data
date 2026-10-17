---
name: implement-spec
description: Implement a whole spec by orchestrating subagents over its ticket graph; auto-detects the most recent task folder when no argument is given.
disable-model-invocation: true
argument-hint: [spec-or-task-folder-path]
---

## Flow at a glance

1. **Resolve input**: find the task folder and its tickets. Nothing there → stop
2. **[GATE]** spec concrete enough? Last chance to ask the user. Past this, unattended
3. **Task worktree**: own branch, the whole run happens there. User's checkout stays untouched
4. **[LOOP]** repeat until every ticket is done:
   - pick the ready tickets: those whose blockers are all done
   - run one implementer subagent per ready ticket, in parallel, each in its own worktree
     - inside each: implement with tests → run the checks → verify the ticket's criteria → done → commit
   - as each returns, land its work onto the task branch one at a time (linear history), keep its notes, drop its worktree
   - landed work may unblock more tickets → next round. A ticket that cannot be finished stops the whole run
5. **Wrap-up** (once): `/simplify` over the whole merged diff
6. **Fresh-context review** of the whole diff, fixes applied, then full project verification on the merged branch and the review record saved
7. **Clean up and report**: remove leftover worktrees and branches, tell the user what's done and where the branch is

Follows the `aiwork-protocol` skill. Don't enter plan mode: the spec and tickets are the plan.

## 1. Resolve input

`$ARGUMENTS` is a spec/PRD or task folder path. With no args, find the most recently modified task folder (per `aiwork-protocol` conventions). Resolve it to an **absolute path** and use that everywhere, including in subagent prompts. Locate the `tickets/` subfolder:

- **No tickets** → suggest `/to-tickets`, or `/implement <spec>` if the spec is small enough for one pass. Stop.
- **All tickets `done` but no `review.md`** → go straight to Wrap-up (§5).
- Nothing found → tell the user and stop.

## 2. Clarity gate

Before touching code, check the spec is concrete enough for an unattended run. **Warn and stop for confirmation** if any hold:

- Open questions, TBDs, or unresolved decisions
- Key technical choices (data model, API shape, file targets) unspecified
- Success criteria too vague to tell when "done"
- Content is contradictory, out of order, or otherwise corrupted
- An external service or credential the tickets depend on is unreachable or unset
- The spec has an Open Concerns section with anything in it
- The task folder has an `intent.md` whose `status` is not `accepted`

Measure that last one, do not read it off the spec: ping each service the spec names and assert the config keys the tickets need. A prerequisite that only fails mid-chain costs the whole run.

The gate runs **once**, against the spec, not per ticket. A badly specified ticket discovered mid-chain doesn't stop for confirmation: resolve it with best judgment and record the gap and resolution in `implementation-notes.md`.

This gate is the **last stop**. Past it, run unattended to the end.

## 3. Task worktree

Run the whole task in its own worktree so the user's checkout stays free. Skip this only when the session is already in a worktree or the user asked to stay in the checkout. If the task already has a worktree (`git worktree list`), enter that one instead of creating a second.

Every worktree this run creates, this one and the ticket worktrees in §4, lives under the **main checkout's** `.claude/worktrees/`, the only place a subagent can switch into. Before the first `git worktree add`, make sure git ignores that directory, or the worktree shows up as untracked and gets swept into a commit:

```bash
git check-ignore -q .claude/worktrees/x || echo '.claude/worktrees/' >> "$(git rev-parse --git-common-dir)/info/exclude"
```

1. Commit the task folder, or at least the spec and tickets. A worktree only sees committed work.
2. Run `git worktree add .claude/worktrees/<task-slug> -b <task-branch> HEAD`. Branch from `HEAD`, not `origin/main`, so the task folder's commit is in it. Name the branch after the task slug.
3. Enter it with the `EnterWorktree` tool, passing `path` (not `name`, which creates its own worktree off `origin/<default>`). This skill is the instruction that authorizes the tool.
4. Bootstrap it. A manually created worktree gets no `.worktreeinclude` files and no `SessionStart` hooks. The plugin's script does both, matching `.worktreeinclude` patterns the way Claude Code does. A zero exit means the worktree is ready:

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/bootstrap-worktree.sh <main-checkout> <worktree>
   ```

5. Re-resolve the task folder to its absolute path **inside the worktree** and use that path everywhere from here on, including in subagent prompts.

This worktree is the base for the whole run. Per-ticket worktrees in §4 branch off it and merge back, and `implementation-notes.md` is written only here.

## 4. Execution

This session acts as **orchestrator** and spawns one subagent per ticket, always, even for a lone ticket. Subagents keep the orchestrator's context clean. Parallelism is a bonus when the frontier allows it. Invoking this skill is itself the user's explicit request to spawn subagents. The `blocked_by` graph defines a **frontier** of ready tickets (`status: ready`, all blockers `done`), often several at once.

If `spec.md` (or the current `plan*.md` when there is no spec) carries a `status` field, keep it current as the run moves: `in-progress` before the first implementer, `agent-done` in wrap-up, `blocked` with `blocked_by:` if the chain stops. Never set a spec to `done`: that is the human's sign-off after they check the feature, the UX and the code.

1. When tickets call for exploration, or the spec names a library the repo does not already use, spawn one **exploration subagent** up front (`model: sonnet`). It saves markdown notes into the task folder. Commit them before the first implementer and put their path in every implementer prompt, so nobody researches the same internals twice.
2. Spawn an **implementer subagent** for every frontier ticket, in parallel, each with its ticket path and the `<ticket-loop>` below as its instructions. Tickets that touch dependencies or the lockfile never run in parallel with other tickets: hold them until they can run alone.

   A **lone frontier ticket works directly in the task worktree**. Only when the frontier holds more than one ticket does each subagent get its own worktree. Branch it off the **task branch's current tip** (not `origin/main`, not another ticket's branch) so it starts from everything merged so far:

   ```bash
   git -C <main-checkout> worktree add .claude/worktrees/<task-slug>-<NN-ticket-slug> -b <task-slug>-<NN-ticket-slug> <task-branch>
   ```

   Bootstrap it with the §3.4 script, task worktree as source.

   Never spawn an implementer with the Agent tool's `isolation: worktree`: it creates a worktree off the wrong base that the orchestrator cannot rebase or merge, and it leaks. Create the worktree yourself as above. The orchestrator owns every worktree's lifecycle, so subagents never create or remove one.

   Pass each subagent its worktree's absolute path and tell it to enter that path with `EnterWorktree` before doing anything else, stating that the prompt authorizes the tool. It stays inside that path, using absolute paths or `git -C` rather than assuming a working directory.

3. When a subagent returns, confirm the ticket says `status: done` and a commit landed. Then integrate it **linearly**, without merge commits: rebase the ticket branch onto the task branch's tip (`git -C <ticket-worktree> rebase <task-branch>`), resolving conflicts against the spec. Then fast-forward the task branch onto it (`git merge --ff-only <ticket-branch>` in the task worktree). Append the returned notes that clear the bar below and drop the rest. Then delete the ticket worktree and branch. Integrate one ticket at a time so a conflict is attributable. A lone ticket that worked directly in the task worktree has no branch to merge and no worktree to remove, so only its notes apply.

4. Recompute the frontier (merged work may have unblocked tickets) and spawn implementers for the newly ready ones. Repeat until no ticket remains.

   Never sleep-poll a subagent or background task: the harness notifies on completion.

5. If a ticket cannot be completed (tests won't pass, blocker discovered), let in-flight subagents finish, then stop the chain and report the state. Never mark it done. Stop every background task the run started (`TaskStop`) before reporting: pollers left running keep waking the orchestrator with news it already has.

<ticket-loop>

1. Set ticket `status: in-progress`.
2. Implement. Use `/tdd` where possible, at the seams recorded in the spec's Testing Decisions section.
3. Tidy the diff yourself: naming, duplication, dead scaffolding. Not `/simplify`, it runs once in wrap-up.
4. Run the project's check command (see its scripts). Green before anything below.
5. Run `/verify <ticket-path>` so it verifies the ticket's acceptance criteria and the surfaces it changed, nothing wider. The full sweep runs once in wrap-up. Check off `- [ ]` → `- [x]` for each criterion it passed.
6. Set ticket `status: done` and `verified:` to the passes that ran (`checks`, `behaviour`, `ux`). Commit. Do not ask.

Returning is hooked: `verified-gate` holds the turn when a ticket goes to `done` without that evidence (see below). Set the frontmatter because the passes ran, never to get past the hook.

When a check fails because an external service is unreachable, do not poll for it. Retry once, wait at most 60 seconds, then commit what works, leave the ticket `in-progress` with the unverified criteria listed, and return. Whether to wait for infrastructure is the orchestrator's call, not yours.

Throughout: keep `implementation-notes.md` in the task folder (an `aiwork-protocol` artifact) as a short log for the maintainer. One test decides what goes in: the reader has to act on it, or would be misled without it. Write each entry when it happens.

- Work only a human can finish: a service that is down, a credential the user must set, a console change agents cannot reach. Say what to do and where.
- Anything left unverified, and what would close it.
- A decision you took where the spec was silent, and why.
- A deliberate deviation from the spec or ticket.
- A fact that contradicts the spec, a ticket, or an earlier note.
- An accepted limit, open question, or a stopped chain.

Leave out what you built, files touched, tests run, and checks that passed. Cite a file, commit, or test name instead of pasting output. Notes for later tickets belong in those tickets.

A few bullets per ticket is the budget. A ticket that went to plan and left nothing to do reports nothing at all.

Never edit `implementation-notes.md` directly: the orchestrator owns it and appends the entries you return in your final report. Likewise, never create, merge, or remove a worktree or branch. Entering the one you were given is the only worktree action that is yours. Work only in that root, commit there, and let the orchestrator merge.

If verifying needed a launch or observation recipe the project's run or verify skill lacks, add it to that skill and commit it with the ticket. Later tickets inherit it.

If a blocker forces work beyond the ticket's stated scope, make the smallest deviation that unblocks it and flag it in your returned notes. If the deviation would touch another ticket's territory, stop and return the decision to the orchestrator instead.

</ticket-loop>

## 5. Wrap-up

Runs **once**, after the last ticket, never per ticket. Skip it if `review.md` exists in the task folder and no ticket finished since. If tickets did finish after a review, run wrap-up again and save the new review as the next number (`review_2.md`).

1. Run `/simplify` once over the merged diff, its reviewers as fresh subagents (a fork inherits the orchestrator's context and costs about three times as much).
2. Review the whole branch diff with `/code-review xhigh --fix`. It reviews and applies fixes in its own subagent, so the verdict comes from a fresh context. Never review the diff by hand instead, and keep `xhigh`: lower levels skip the removed-behaviour and cross-file angles. Fix any findings it left unapplied. A finding deliberately left unfixed goes into `implementation-notes.md` with the reason.
3. Run the project's full verification gate (tests, lint, build, whatever the project defines), then `/verify` over the whole branch. It runs after the two passes above so it covers their fixes too, and it is the first check of the merged branch as a whole: per-ticket passes saw one slice each and merges ran nothing. Anything it turns up gets fixed and the gate re-run.
4. Commit the remaining fixes, then save the review outcome as `review.md` per `aiwork-protocol`, with `reviewed_sha:` set to the branch tip the green gate covered. Its presence marks wrap-up complete.
5. If the spec (or plan) carries a `status` field, set it to `agent-done` and `verified:` to the passes that ran across the run. Never `done`: the human accepts.
6. Remove any leftover ticket worktrees (`git worktree list`) **and their branches** (`git branch --merged` catches them), then commit remaining changes. Sweep only what this run created, plus stray `.claude/worktrees/agent-*` worktrees and `worktree-agent-*` branches whose commits are merged; leave any other worktree alone. Leave the task worktree on disk. Don't merge it into the user's branch or delete it.
7. Report tickets completed, commits made, review outcome, and anything left open. Say the spec is `agent-done` and awaits their check of the feature, the UX and the code before it becomes `done`. End with the **absolute path** of the task worktree and its branch name on their own line.

## The verified-gate hook

Driving the app and judging the code are agent work; code cannot enforce that they happened well, but it can enforce that the **evidence** exists. The plugin's `hooks/verified-gate.mjs` runs on `Stop` and `SubagentStop`, over tickets and review reports touched recently in any worktree. It holds the turn open when:

- a ticket is `status: done` and `verified:` has no on-app pass (`behaviour`, `ux` or `human`)
- a ticket is `status: done` with acceptance criteria still `- [ ]`
- a `review*.md` has no `reviewed_sha:`, or names a commit unreachable from `HEAD`

It is active whether or not this skill ran and reaches the implementer subagents. It fails open and has no bypass.

When the hook holds you, run the missing pass. Do not edit frontmatter or tick criteria to satisfy it. If a pass genuinely cannot run, the ticket is not done: set it back to `in-progress`, record why in `implementation-notes.md`, and commit that.
