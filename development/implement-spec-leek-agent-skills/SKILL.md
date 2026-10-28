---
name: implement-spec
description: "Build a whole spec fast: parallel implementer subagents work the ticket frontier, each in its own worktree, merging onto one integration branch; then one review, one verification pass, and one PR or a stack of PRs."
disable-model-invocation: true
argument-hint: "A spec path (.scratch/<slug>/spec.md); a spec with no tickets gets them cut first. Optionally, how many implementers at once (default 4)"
---

# Implement Spec

Build every ticket of one spec in this session by **orchestrating**, not building: implementer subagents do the code, each in its own worktree; you own the tracker, the **integration branch**, the merges, and the final gates. The goal is the whole spec on one integration branch, every ticket closed, delivered as the user chose: one PR, a stack of PRs (one per ticket), or a pushed branch.

The tickets are not a list of steps. They are a **task graph**: `blocked-by` edges mean there is always a **frontier** of tickets ready to grab, and every ticket on it can be built at once.

Reach for the neighbours instead when they fit better: `/implement <spec> all` builds the same tickets one after another in this session, with no subagents (and is the fallback when the harness has none: say so and stop); `autopilot` drives the tickets through fresh top-level sessions while you are away.

Talk to subagents in **context pointers**: paths to the spec, the ticket, blocker resolutions, notes, commits. Never paste what a pointer already reaches. Ask them for sparse reports.

## Guardrails

- **Never** reset, roll back, drop, or truncate a database this run did not create, or run another destructive data operation on one, without explicit approval. Schema changes go in new migrations.
- Verify identifiers before using them: route names, config keys, enum values, package APIs.

**Stack references.** Identify the stack from its manifests. If a matching file exists below, read it before step 1 and pass its pointer into every implementer brief: it names that stack's destructive commands, worktree setup, test-config files, and formatter.

- Laravel (`laravel/framework` in `composer.json`): [`references/laravel.md`](references/laravel.md)

**Ticket board.** Report each ticket's status per [`ticket-board.md`](../wayfinder/references/ticket-board.md), with `kind: "spec"`: `ready` and `blocked` (note: the blockers) from step 1, `skipped` for tickets left out, `running` at dispatch, `fixing` when a failure goes back to its implementer, `merged` (note: the merge SHA), `released` (note: why), and `closed` in step 7, or `awaiting-deploy` (note: the after-deploy steps, in a few words) for a delivery ticket left at `ready-for-human`. From step 5 on, also send the `stage` at each change (`review and verify round 1`, `fix pass 1`, `review and verify round 2`, `fix pass 2`, `fix pass 3` when step 5's extra round runs, `final checks`, `deliver`) and each finding's status, so the pane never goes quiet after the last merge.

## Process

### 1. Load the task graph

Read the spec: its **Build Contract** section first, then what the tickets name. Read every ticket's frontmatter once (`status`, `blocked-by`, `deploy-gate`, `claimed-by`).

**No `tickets/` yet?** Cut them yourself with `to-tickets`' rules: its step 3 for the slicing, its step 4 for the open decisions, its step 5 and [Ticket template](../to-tickets/SKILL.md#ticket-template) to publish and commit. Vertical slices with honest `blocked-by` edges are what make the frontier wide; a chain of tickets each blocked by the last builds no faster than `/implement all`.

Open the ticket board now, before anything else in this step: load `mcp__leek-skills__ticket_board` with ToolSearch if it is deferred, and send every in-scope ticket with its `title` as `ready` or `blocked`, and the left-out ones as `skipped`.

Leave out closed tickets and tickets claimed by someone else (name them in the report). When the branch `<slug>` already exists and is unfinished, this run resumes an earlier one. It is finished when `origin/<default>` contains it or its PR merged or closed (`gh pr list --head <slug> --state all --json state`); then this run starts fresh on the next free `<slug>-<n>` (a deploy gate's dependents, a later re-run) and uses that name wherever this skill says `<slug>`. Resuming, read the frontmatter from the old integration worktree when one exists (earlier claims sit there uncommitted until step 7), otherwise with `git show <slug>:<path>`. A claim from that earlier run (`implement-spec-<slug>-*`) is no proof it stopped, since a long test writes no file: ask the **Resume** question below. Each claim taken over is rewritten with this run's id. Never dispatch the delivery ticket (`delivery: true`) to an implementer: you work it in steps 6–7. A `deploy-gate: true` ticket bounds the run: build up to and including it, then stop at step 7 with a PR; its dependents start after that PR is deployed. When dependents would wait behind a gate, ask once, here, before the first dispatch (not after the gate PR opens): stop at the gate, or build the dependents in this run on a second integration branch `<slug>-2` cut from the gate branch's tip. Before dispatching the first contract/drop ticket on `<slug>-2`, confirm the gate branch `<slug>` has no remaining writes or reads to the columns or tables `<slug>-2` drops. `<slug>-2` takes changes only by merging `<slug>` (the gate ticket and its review fixes), never by merging or cherry-picking any other branch, and once the gate PR merges, move `<slug>-2`'s delta onto fresh `origin/<default>` for a second PR.

**Sweep for open decisions first.** Run one read-only subagent over the spec, every in-scope ticket, and the spec's `decisions/` and `research/` (a domain-expert agent type when the harness offers one for the spec's domain). Its brief: list every choice the build will have to make that these documents do not settle, each with the tickets it touches, the line that leaves it open, and a recommended answer. Settled choices (including those `to-tickets`' sweep already wrote to `decisions/`) and pure implementation detail are not open decisions. Most questions a run would otherwise raise mid-build come from here, and asking them now keeps the frontier moving. Skip the sweep when `decisions/` holds a committed **Build decisions** ticket from `to-tickets` and no commit after the one that added it (`git log -1 --diff-filter=A --format=%H -- <its path>`) touched the spec or a ticket (`git log --format=%h <that commit>..HEAD -- .scratch/<slug>/spec.md .scratch/<slug>/tickets` prints nothing): that sweep already covered these documents.

Before the first dispatch, ask these in one `AskUserQuestion` call where available (a second call when they pass four; otherwise one message in chat), and nothing else:

- **Open decisions** from the sweep, recommended answer first, in as many further `AskUserQuestion` calls as they need (at most 4 questions each). Step 2 commits the answers to the integration branch; pass that pointer in every implementer and review brief so a reviewer never reopens a settled choice.
- **Worktree**: build the integration branch in a worktree at `.claude/worktrees/<slug>` (recommended: this checkout stays as it is), or switch this checkout to `<slug>`. Skip it when the tree is dirty (the worktree is the only option; say so) or the request already says. Each implementer gets its own worktree either way: that is what lets them build in parallel.
- **Delivery**: `implement`'s [delivery question](../implement/references/spec-run.md#choose-the-delivery-shape) for a whole spec: one PR, stacked PRs, or the branch with no PR.
- **Deploy gate**, when one applies (above).
- **Local `<default>`**, when its only commits ahead of `origin/<default>` touch `.scratch/<slug>` (`git log --format=%h origin/<default>..<default> -- . ':!.scratch/<slug>'` prints nothing, and `git rev-list --count origin/<default>..<default>` is not `0`). Step 2 can move `<default>` back to `origin/<default>` once it has carried the spec over (recommended), or leave `<default>` as it is. If it stays, pulling `<default>` after the merge conflicts.
- **Resume**, on a resumed run with claims of its own: take them over, or leave them. Recommend take-over when none of its worktrees changed a file in the last 30 minutes.
- **Cleanup**: at the end, remove what step 8 would otherwise ask about (a refused or released ticket's worktree and database, and the verify setup) without asking (recommended), or list them for a choice then. A worktree holding uncommitted work beyond agent notes is always listed, and a branch with unmerged commits always stays.

Finish when every in-scope ticket and its edges are known, the ticket board lists them (where the tool exists), the open decisions are answered, the worktree, delivery and cleanup choices are made, and the first frontier is listed.

### 2. Create the integration branch

Make a notes directory outside every worktree: `notes="$(git rev-parse --path-format=absolute --git-common-dir)/implement-spec/<slug>"`.

When the branch `<slug>` already exists, this run resumes an earlier one. Its integration checkout is the worktree that already has `<slug>` checked out (`git worktree list`), otherwise `git worktree add <main checkout>/.claude/worktrees/<slug> <slug>`, or `git switch <slug>` when step 1 chose this checkout. Read `base_sha` back from `$notes/base_sha`; without that file, it is the first parent of `<slug>`'s first ticket merge (the first line of `git rev-list --first-parent --merges --reverse origin/<default>..<slug>`, then `^1`). Keep the PRs a stack already opened, and open the integration PR per that reference's step 6 when `gh pr list --head <slug>` finds none. Otherwise follow `implement`'s [PR delivery: before step 1](../implement/references/spec-run.md#pr-delivery-before-step-1-claims-anything): branch `<slug>` from fresh `origin/<default>`, in `.claude/worktrees/<slug>` when step 1's worktree answer (or a dirty tree) says so, with the spec's `.scratch/<slug>/` carried over. Record `base_sha`, and write it to `$notes/base_sha`. Either way, this checkout is the **integration checkout**.

When step 1 answered open decisions, write them in the integration checkout as one closed decision ticket in `.scratch/<slug>/decisions/`, in the format `to-tickets`' Publish step gives its **Build decisions** ticket, and commit it (`docs(scratch): <slug> build decisions`, unless the repo ignores `.scratch`) before `base_sha` is recorded (between that reference's steps 3 and 5), so every ticket worktree carries the answers and no ticket's PR shows them.

When several tickets need the same exploration (an unfamiliar module, a package's docs), run one read-only **exploration subagent** first that writes its findings to `$notes` as Markdown, so implementers build instead of explore.

### 3. Dispatch the frontier

For each frontier ticket, up to the concurrency limit (default 4: each one runs a test suite). A ticket whose `## Files` share a path with a running ticket's waits until that one merges, so the two never conflict; dispatch the next frontier ticket instead.

1. **Claim** it in the integration checkout per the tracker's Claim operation, with `claimed-by: implement-spec-<slug>-<run id>`. Only you write `.scratch/`; claims stay uncommitted until step 7.
2. **Worktree.** `git worktree add -b <slug>--<NN> <main checkout>/.claude/worktrees/<slug>--<NN> <integration tip>` (the main checkout's `.claude/worktrees/`, never one inside the integration worktree), then make it runnable (install dependencies, copy local env config) the way the project's docs say, or as the stack reference says. When the tests need a real database, give it its own (`<app db>_spec_<slug>_<NN>`, never a name the main checkout's env or test config uses) and register it the moment you create it:

   ```bash
   printf '%s\t%s\t%s\t%s\n' "$(date +%s)" <pgsql|mysql> <database> "<worktree path>" \
     >> "$(git rev-parse --path-format=absolute --git-common-dir)/scratch-databases"
   ```

3. **Implementer subagent**, in the background where the harness allows (Claude Code: subagents run in the background by default and wake you on completion; pass `run_in_background: true` where the Agent tool offers it; give each a `name` of `<slug>--<NN>` so you can address it later; Codex: `spawn_agent`, keeping each returned agent id against `<slug>--<NN>`, and `wait_agent` to collect reports; elsewhere, any sub-agent the harness offers). Its brief gives pointers (worktree path, ticket path, the spec's Build Contract, the decisions answered in step 1, direct blockers' reports from step 4, the notes directory) and these rules:
   - Work only in that worktree (enter it with `EnterWorktree({path})` where available, otherwise use absolute paths into it). Confirm `git merge-base --is-ancestor <integration tip> HEAD` before starting.
   - Choose seams with the `tdd` skill's **Seams: where tests go** rules and state them; then call the Skill tool with `tdd` and build the ticket test-first. Focused tests and configured static analysis end green.
   - Run tests in the foreground and wait for the result. Never send a test run to the background and go idle on it: an idle implementer may not wake when the run ends. A run too long for the tool's timeout is too broad; run fewer files.
   - Format touched paths with the repo's configured formatter, commit by explicit path. Never touch `.scratch/`, never push, never write another branch.
   - Before reporting, merge the current integration tip into the branch and rerun the focused tests.
   - Report in at most ten lines: commit SHAs, touched paths, seams (name any public seam a dependent ticket should reuse), the focused test command and result, deviations from the ticket, any decision built on an assumed answer, and anything blocking.

Then end the turn and let completion notifications wake you; never poll. An idle notification with no report and no new commit is a stall, not progress: message that implementer at once (`SendMessage` in Claude Code, `followup_task` in Codex) to finish or say what blocks it. One that repeats a report you already acted on needs nothing: end the turn without a reply.

A hung tool call sends no notification at all. So whenever the run waits on a single implementer (the others have reported, or nothing else is ready), arm one 20-minute wake-up the harness offers (Claude Code: a `Monitor` whose command exits once that worktree has gone 20 minutes with no file change; otherwise check that worktree's last file change whenever anything wakes you). Woken with no new commit, message it to report what it is waiting on, and stop the hung call when it cannot.

### 4. Merge as each implementer lands

With **Stacked PRs**, review the ticket on its branch first, per `implement`'s [Stacked PRs](../implement/references/spec-run.md#stacked-prs) step 1: its PR must hold every commit it will ever get. Then, in the integration checkout: `git merge --no-ff --no-commit <slug>--<NN>`. On a conflict, call the Skill tool with `resolving-merge-conflicts`. Rerun that ticket's focused tests on the merged tree, then commit the merge; on a failure, `git merge --abort`, so `<slug>` only ever holds green merges. With **Stacked PRs**, push and open the ticket's PR right after its merge commit, per `implement`'s [Stacked PRs](../implement/references/spec-run.md#stacked-prs). A failure goes back to the same implementer with the output, so it keeps its worktree and ticket context (`SendMessage` to its name in Claude Code, `followup_task` to its agent in Codex; otherwise brief a fresh implementer with the worktree path, the ticket, and the failure output); a ticket that reports itself blocked is released (the tracker's Release), and its dependents stay out of this run.

Keep each implementer's report in `$notes/<NN>.md`: it feeds dependents' briefs and the ticket's `Resolution`. A merged ticket counts as done for its dependents' `blocked-by`, so recompute the frontier and dispatch what it unblocked (step 3).

After each merge, update the ticket board, and post one progress line so the user never has to ask for status: `<NN> merged (<k> of <M>); running: <NNs>; next: <NNs>`, with ` · PR #<n>` after `merged` in a stack. Skip the line when the board's pane shows the run.

**A question never stops the run.** A decision the sweep missed (one that only shows once code exists) is built on its recommended answer when that answer is reversible: the implementer or fixer records it as an assumption in its report, and you ask it at the next merge, so a different answer becomes a follow-up fix, not a wait. When the choice is not reversible (a schema shape a later ticket builds on, a data migration), release that ticket and its dependents, keep building the rest of the frontier, and ask the open questions together at the next merge, or in the final report when nothing else is running. Stop and wait only when every remaining ticket is blocked on an answer.

Finish when every in-scope ticket but the delivery ticket is merged or released, and no implementer is running.

### 5. Review and verify once, over the whole branch

Start both at the integration tip, at once: call the Skill tool with `code-review` against `base_sha` on the integration branch, scoped to every path the run touched, and dispatch one verifier subagent (Claude Code: `Agent`; Codex: `spawn_agent`, then `wait_agent`) that calls the Skill tool with `verify` (otherwise follows the `verify` skill) and checks every ticket's acceptance criteria in one pass, reporting each failure and its screenshots' paths. A harness with no sub-agents runs `verify` inline once the review returns. Verification needs no review fix to start, and its failures join the same fix batch instead of a second cycle. With **Stacked PRs**, every ticket's commits were already reviewed on all three axes before their merge, so pass `code-review` only the Correctness and Spec axes, its Correctness brief aimed at what crosses tickets: shared seams, ordering, and one ticket's change breaking another's path.

Fix both sets of findings as one batch, grouped into **fixers** per [Parallel fix batch](../triage-github-pr/references/parallel-fixes.md) steps 1–4 (its merged-tree test run included; the re-review below is its pre-push review, and nothing is pushed): each fixer in a detached worktree `<main checkout>/.claude/worktrees/<slug>--fix-<k>` off the integration tip, named `<slug>--fix-<k>` (its database, when it needs one, `<app db>_spec_<slug>_fix<k>`), merged back into the integration checkout. A batch below that file's threshold goes to a single fixer, `<slug>--fix`, working in the integration checkout. Later rounds reach a fixer by `SendMessage` to its name in Claude Code or `followup_task` in Codex (otherwise brief a fresh one with its worktree path and the findings), and a fixer merges the integration tip into its worktree before a later round, so it builds on every earlier fix. Fixers work through `tdd` and commit each finding on its own, with a subject that says what it fixed. Mark the findings `fixing` at the handoff, and `fixed` (note: the SHA) for each one whose commit `git log` shows whenever you wake. When you tell the user about findings, name each by what is wrong and where, never by a made-up code (`C2`, `S1`) the user has no key for; once the fixes are merged, re-run `code-review` as a re-review, passing the previous round's findings and head, and re-run `verify` only on the criteria that failed or whose code the fixes touched. A finding that needs the user's decision never holds the round: send every other finding now, ask that one in parallel, and pass the answer on as a follow-up. Two rounds is the budget. When the second still has BLOCKING or MAJOR findings, fix those in one more round without asking, its re-review covering only them; name whatever is left in the final report and the PR, with the commit each round reviewed (if the user asks to ship them in a follow-up PR, open **one** follow-up PR for all remaining findings, never one PR per finding, after step 7, based on the integration branch while that PR is open (in a stack, on the closing PR's `<slug>-stack-fixes`, since the remote `<slug>` holds no ticket until triage lands them); once it has merged, retarget per [Follow-up on a delivered PR](../implement/references/spec-run.md#follow-up-on-a-delivered-pr)). Finish when review and verification report nothing actionable, or when the rounds are spent; a verification failure an external dependency blocks is named, and its tickets stay open.

### 6. Final checks

Run `implement`'s step 6 once over the whole range. Skip the full-suite question when the repo's rules or the user's saved preferences already settle it (CI runs the suite, or "do not run the full suite unless asked"); otherwise ask once. A declined full suite is never replaced by a broad sweep of many test files: each ticket's focused tests stand as the evidence. A failure the run caused goes to step 5's fixers. Then, when the spec has a delivery ticket, run its pass 1 per [`DELIVERY-TICKET.md`](../to-tickets/DELIVERY-TICKET.md): the full suite and step 5's verify pass count toward its Before merge list, and a coverage gap goes to step 5's fixers like a product failure. Finish when the checks passed and pass 1 is done, or name the exact external blocker and leave those tickets open.

### 7. Close and deliver

For each verified ticket: append `## Resolution` (what was built, deviations, verification evidence, its implementation commits, seams for successors, from `$notes/<NN>.md`) and set `status: closed`; re-read to confirm. The delivery ticket closes, or goes to `ready-for-human` with its after-deploy steps copied into the PR body, per its file. Commit the tracker separately (`docs(scratch): <slug> resolutions`), never folded into code. Then follow [PR delivery: after step 8](../implement/references/spec-run.md#pr-delivery-after-step-8) for the chosen shape: push, open the PR (or, for a stack, whose ticket PRs opened as each ticket merged and whose integration PR opened in step 2, open the closing PR and fill in the integration PR's body per its [Stacked PRs](../implement/references/spec-run.md#stacked-prs) step 4), and read review threads once, except on a stack.

### 8. Clean up

Run cleanup from the integration checkout, so `git branch -d` checks each ticket branch against `<slug>`. For each ticket merged into the integration branch, clean up only the environment this run created, in order: `herd unlink <name>` from inside the worktree if the bootstrap linked it; carry any change under its `.claude/agent-memory/` into the main checkout's copy (reviewer notes are append-only: add the lines the main copy lacks), then restore the tracked notes (`git checkout -- .claude/agent-memory`, when any are tracked) and delete the untracked ones you carried (`git status --porcelain --untracked-files=all -- .claude/agent-memory` lists them); `git worktree remove <path>` (no `--force`), then `git branch -d <slug>--<NN>`, then drop its registered `<app db>_spec_<slug>_<NN>` database and parallel-testing copies (`<database>_test_<N>`). Delete each `scratch-databases` line only after its database was successfully dropped. If worktree removal refuses, stop cleanup for that ticket: retain its branch, database, parallel-testing copies, and registry entries together. `git branch -d` is the only branch delete. When it refuses, the branch stays with whatever remains, and the report names the refusal. Git's force-delete hint (`-D`) is not a go-ahead. If a database drop fails, retain the remaining resources and registry entries and report the failure. A fixer worktree `<slug>--fix-<k>` whose commits are merged goes the same way, with no branch to delete. List each successful removal.

What is left that you created (a refused environment, the environment of an unmerged or released ticket, and the verify setup: the Herd link, database or worktree `verify` made for the run, when it made any) follows step 1's cleanup answer. When it was to remove them, remove each by the same ordered cleanup: a worktree that holds uncommitted work beyond agent notes is listed instead, and a branch `git branch -d` refuses stays and is named in the report. Otherwise ask once (`AskUserQuestion` where available: a `multiSelect: true` question with one option per ticket's retained environment, naming its worktree, branch, database and copies, nothing pre-ticked, at most 4 per question and further questions for the rest; otherwise a plain yes/no question in chat: "Can I delete these too?"). Remove only selected environments, following the same ordered cleanup above, never with `--force`. Keeping a worktree keeps its associated resources. Skip the question when nothing is left. Keep the integration worktree: it holds the PR branch (leave it with `ExitWorktree({action: "keep"})` if you entered it). Anything kept is `repository-cleanup`'s job later.

## Stopping mid-run

Merge what has landed. Ask which running implementers to cancel (`AskUserQuestion` with `multiSelect: true` where available, one option per name; otherwise in chat); stop each chosen one with `TaskStop({task_id: <name>})` in Claude Code or `interrupt_agent` in Codex, and release its ticket (the tracker's Release), keeping its worktree and branch. Where nothing can stop them, leave them running. Running implementers keep their claims. Report per ticket: merged (with its PR in a stack), in flight (worktree path), stopped (worktree path), released, or not started. A re-run on the same spec resumes: a `<slug>--<NN>` branch with a report in `$notes/<NN>.md` is merged first instead of rebuilt; one without (a stopped implementer) goes to a fresh implementer briefed to finish it in its worktree.

## When you're done

Print the end-of-session block using the frame in [`wayfinder/references/pipeline-end-block.md`](../wayfinder/references/pipeline-end-block.md):

```text
---
Pipeline: decide → spec → tickets → **build**   (4 of 4)
Done: <tickets closed of total, integration branch, PR, verification state>
Next:
  • <condition> → /<skill> <ref>
```

- **A PR is open and review bots are still running** → `/resolve-review-comments <PR>` once they post
- **A stack of PRs is open** → `/triage-github-pr <every PR, bottom-up>` to land it bottom-up with merge commits
- **Stopped at a deploy gate** → deploy the PR, then `/implement-spec <spec>` for the dependents
- **The delivery ticket is at `ready-for-human`** → merge and deploy, then `/implement <delivery ticket>` for its after-deploy steps; list them
- **Tickets released or left open** → `/implement <ticket>` for each, or `/implement-spec <spec>` again
- **The build exposed a decision nobody made** → `/grill-me` on it, then re-run `/to-spec`
- **The run went sideways** → `/retro this` before clearing
