---
name: run-handoff
description: Build a plan written by /handoff in one long-running session — keep PROGRESS.md, dispatch every unblocked item to a background subagent in its own worktree, re-run its acceptance yourself before fast-forwarding an integration branch, review at gates and over the whole branch. Checks in with the user at every gate by default; --auto runs unattended until done or blocked. Use when the user asks to run, build, execute or resume a handoff.
disable-model-invocation: true
argument-hint: "[handoff-dir] [--auto]"
---

# run-handoff

You are the lead and integrator. `HANDOFF.md` is the plan and is read-only to you; `PROGRESS.md` is yours. Execute the plan, don't redesign it.

**Mode.** By default, stop at every gate for the user. With `--auto`, gates are self-checked and only the stop conditions halt you. The mode is per invocation and never stored, so a gated start can resume with `--auto`.

## Start or resume

1. **Resolve the directory.** If none is given, take the most recently modified directory holding a `HANDOFF.md` under the user's agent-notes location (or `.agents/handoffs/`), and confirm it before starting.
2. **Read `HANDOFF.md` in full.** Amendments override everything above them. Read `research/` files only when an item needs them.
3. **Resume** if `PROGRESS.md` exists.
   - Check it against git: the integration branch, item worktrees and their commits. Where they disagree, git wins; fix `PROGRESS.md`.
   - Run the standard checks on the integration branch before dispatching anything. If a crashed session left it broken, fixing that comes first.
   - Continue from "Now".
4. **First run.**
   - Create the integration worktree, branch `<topic>`, off the base branch in Context. Use the user's worktree tooling, otherwise `git worktree add`. Never work in the primary checkout.
   - Create `PROGRESS.md` from the template below.
   - Run Context's build and test commands once, and record their durations.
   - Then do the bootstrap items and `G0` yourself.

## Loop

1. **Frontier.** Every item whose blockers are done and whose `Owns` doesn't overlap an item in flight.
2. **Dispatch** frontier items up to HANDOFF's concurrency cap (default 3). For each one:
   - create a worktree `<topic>-<id>` off the integration branch's current head;
   - start a background subagent with the item brief below.

   Do contracts and gates yourself. Claude Code: the Agent tool runs subagents in the background and notifies you. pi: `subagent` with `run_in_background: true`, joined with `get_subagent_result`.

3. **While items run,** do gate work or wait for completion notices. Don't poll.
4. **Route** each report by its status line:
   - `DONE`: integrate.
   - `DONE_WITH_CONCERNS`: read the concerns, then integrate or send back; log the call in the decision log.
   - `NEEDS_CONTEXT`: answer from HANDOFF or research and continue the subagent. If the answer is the user's to give, treat it as blocked.
   - `BLOCKED`: mark the item blocked with the reason.
5. **Integrate.**
   - Confirm the branch sits on the integration branch's current tip. If the tip moved since, have the subagent rebase again, or rebase it yourself if trivial.
   - On that tree, re-run the item's acceptance command yourself, plus the repo's standard checks. Never take the subagent's "it passes" as the result.
   - If it passes: fast-forward the integration branch, record the command, its result and the commit, and remove the item's worktree.
   - If it fails: send the failing output back to the same subagent, continuing it if the harness allows. After two send-backs, mark the item blocked with the last failing output.
6. **Re-check the frontier** after every integration and dispatch what opened up.
7. **Update `PROGRESS.md`** after every item and before any long operation. It is how you resume after a context reset, so keep it accurate, not optimistic.

Long commands go to the background with a deadline, and their output goes to files. Grep files for failures instead of reading whole logs. You can't feel time passing, so follow HANDOFF's budgets.

## Gates

A gate passes when its items pass acceptance on the integration branch and a reviewer signs off. After the last item, a final gate reviews the whole integration branch against its base; fix its confirmed findings in one pass.

**The reviewer** is a fresh, read-only subagent (a reviewer agent type if one exists). It gets the gate's diff since the previous gate (the final gate: since the base), the `HANDOFF.md` path, and the gate's item IDs. It does not get the subagents' reports. Ask it for defects, contract violations, scope drift, uncovered review-focus risks, and acceptance checks that pass without proving the outcome. Fix confirmed findings before the gate passes, and record the gate's commit and verdict.

**Default mode:** after each gate, post the gate, each item's acceptance result, the reviewer's verdict, surprises, and what the frontier opens next. Ask go or adjust, using the harness's question tool if there is one. When blocked, ask right away; items already running keep going.

**`--auto`:** continue past gates. When blocked, add the request to "Blocked on you", send a notification if the harness has a tool for it, and move on to other unblocked work.

## Stop conditions

Both modes stop when:

- no unblocked item remains;
- a locked decision proves wrong and blocks the critical path (put the evidence and a proposed alternative in `PROGRESS.md`);
- the next step would push, land, open a PR, call a real external service HANDOFF doesn't allow, or delete work you didn't create;
- a stop condition in HANDOFF fires.

Never edit `HANDOFF.md` to get unstuck. Propose the change in `PROGRESS.md` for the owner to amend.

## Item brief

Each item subagent's prompt contains:

- **Role:** builds one item. The lead owns `PROGRESS.md`, integration, contracts and gate reviews.
- **Where:** its worktree path. Work and commit only there, in small commits matching the repo's style.
- **What:** its item ID. Have it read `HANDOFF.md` itself (Context including its Skills line, Locked decisions, Contracts, Rules, Gotchas, its item and that item's research files) rather than paraphrasing them.
- **Boundaries:**
  - change only its item's `Owns`; name the paths owned by items now in flight as not its own;
  - never edit contracts, `HANDOFF.md` or `PROGRESS.md`;
  - no push, and no external services beyond what HANDOFF allows.

  If a contract or decision blocks it, it finishes what it can and reports the proposed change rather than working around it.

- **Done:** rebased onto the integration branch's current tip, then its acceptance command passes there, run by it, with the output reported.
- **Report:** first line exactly one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`. Then: branch and worktree; commits; the acceptance command and result; decisions made and why; anything contradicting HANDOFF; measured timings. Failures and skips stated plainly. Logs stay in files and the report gives their paths.

## PROGRESS.md

```markdown
# Progress: <topic>

## Now

<In flight, next up.>

## Items

| ID | Status | Worktree | Send-backs | Acceptance result | Commit |

## Gates

| ID | Commit | Reviewer verdict |

## Blocked on you

<Dated: what is needed, what it blocks, what continues meanwhile.>

## Decision log

<Dated choices made within HANDOFF's latitude, and why.>

## Surprises and failed approaches

## Measurements

## Handoff retro

<Written when the run ends: what HANDOFF got wrong, left out or over-specified, and which decisions or gotchas the build had to discover.>
```

## Final report

Write the handoff retro, then report: what is done and verified, with acceptance results; what is blocked and on what; failures and skips stated plainly; measured timings; the retro; the integration branch and any worktrees left. Landing is the user's call.
