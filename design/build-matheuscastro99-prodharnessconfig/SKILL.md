---
name: build
description: Block B of the harness workflow. Implements an approved plan sub-phase by sub-phase, then pushes a draft PR and writes the handoff. Use only when an approved plan in .harness/work/<issue>/plan.md says to invoke it.
argument-hint: <issue-number>
context: fork
agent: builder
background: false
---

# Build: Block B (autonomous)

The plan in `.harness/work/<n>/plan.md` is your scope and your only inherited context. Find `<n>` from the arguments (`$ARGUMENTS`), from the session-state line, or from the single plan under `.harness/work/`. Read the plan in full before anything else.

## You run as a forked subagent

The `builder` agent runs this skill on Sonnet (D12), apart from the main session, which only relays your reply.

- **Run every command in the foreground and wait for it.** Don't background a command or end your turn while one runs: ending your turn returns you to the main session. A finish guard sends you back unless there's a handoff, `BLOCKED`, or a `QUESTION:` line.
- **You can't ask the owner.** If rule 4 below stops you, commit nothing past the gap and end your reply with one line: `QUESTION: <the question>`. The main session relays it.
- **Resuming:** started again with an answer after the issue number in the arguments, treat each sub-phase already committed (one `(#<n>)` commit each, in plan order) as done and continue with the next.

## Start

1. If `.harness/work/<n>/BLOCKED` exists, stop and tell the owner. Don't work around it.
2. **Post the approved plan to the issue**, once: `gh issue comment <n> --body-file .harness/work/<n>/plan.md`. Save the comment URL in `.harness/work/<n>/plan-comment.txt`. Skip this if that file exists.
3. **Branch:** if you're on the default branch, update it and create `<type>/<n>-<short-name>` (`feat`, `fix`, `docs`, `chore`).

## For each sub-phase, in order

1. **Implement** what the plan says.
   - Keep to its "Invariants to preserve".
   - Don't re-explore its "Rejected approaches".
   - The file-check hook lints each edit; fix what it reports.
   - On a UI sub-phase, follow the project's `frontend-design` skill if it has one (T7).
2. **Need to read code the plan didn't cover?** Read only that code yourself, narrowly: search first, then the lines you need. You already run on Sonnet in a fresh context, so a subagent would only add a hop (D23).
3. **Run the sub-phase's check** through the runner: `node .claude/scripts/check.cjs <id>`. For an automated observable, run it and keep the evidence. Fix what fails.
   - **A UI check (T6):** run it yourself, on either tier; the browser pane and UI automation work from the fork. Don't hand it to the main session (D25).
   - Use the throwaway data the plan names. Never change the owner's real data while driving the app.
   - Save its screenshots under `.harness/work/<n>/ui/`; list them under the handoff's Checks.
4. **Docs:**
   - Stage the change, then run `node .claude/scripts/stale-docs.cjs --staged --record <n>`.
   - Update each candidate doc that is now wrong, in this same commit.
   - For a doc that is still accurate, add `ack: <doc> — <why>` to `.harness/work/<n>/stale-docs.md`.
   - Also check the docs the plan listed: the script can't see drift that names no path.
   - Update a doc line the change makes untrue even when the plan limits the files: the plan's file list scopes the code, not the docs it falsifies. List the line under the handoff's Docs.
5. **Commit**, one commit per sub-phase: `<type>: <summary> (#<n>)`. The docs gate blocks a commit while a flagged doc is neither updated nor acknowledged.

The Stop gate won't let you stop while fast checks fail. After 3 failures it writes `BLOCKED`. Then:

- write the handoff with `Status: BLOCKED` (below)
- don't push and don't open a PR
- stop

## Stop and ask (Working Agreements rule 5)

Anything the plan doesn't cover stops the work: a behaviour change, a new dependency, a scope change, or breaking a Small tier's criteria. Ask the owner and wait. A scope change goes into the issue before it goes into the code.

## Exit (only without BLOCKED)

1. Run `node .claude/scripts/check.cjs full`. Fix what fails.
2. Push: `git push -u origin <branch>`. Open a **draft** PR: `gh pr create --draft --title "<summary> (#<n>)" --body "Closes #<n>. Plan: <plan comment URL>"`.
3. **Bind the handoff to one commit:**
   - Wait for CI on the pushed head: `gh pr checks <pr> --watch --fail-fast`.
   - If a check fails, fix it, run `full` again, push, and wait again.
   - When CI passes, record `gh pr view <pr> --json headRefOid`.
4. **PR monitoring (Auto-fix) stays off from the handoff until the merge,** so nothing pushes after the handoff. You can't reach the app's PR tools from the fork, so end your reply with this line, which the main session acts on: `MAIN SESSION: turn off Auto-fix for <PR url> if it is on.`
5. **Handoff, on both tiers:**
   - Write `.harness/work/<n>/handoff.md` in exactly this shape. Every section is filled in or says "none":

     ```markdown
     # Handoff: #<n> → Review
     Status: READY | BLOCKED
     Plan: .harness/work/<n>/plan.md (issue comment: <url>) · Branch: <branch> · PR: <url> (draft)
     PR head: <sha> · CI on that head: pass | fail | none
     ## Commits
     ## Checks
     <check id> → pass/fail, with counts
     Not verifiable here: <what no check covers> (or "none")
     ## Deviations from the plan
     ## Decisions made inside the plan's latitude
     ## Docs
     Updated: <files>. Script-flagged but left unchanged: <doc — why> (copy the acks)
     ## Open questions for G2
     ## Known gaps / risks
     ```

   - Validate it with `node .claude/scripts/handoff-check.cjs .harness/work/<n>/handoff.md --verify-head`, and fix it until it passes.
   - Post it to the issue (`gh issue comment <n> --body-file …`). In the posted copy, replace anything security-sensitive with "withheld"; keep it in the local file.
6. **Then stop. Don't run `review` yourself:** G2 is triaged on Opus, outside the fork (D22). Take the tier from the plan's first line (`Tier: Standard` or `Tier: Small`) and end with that tier's line only (D25).
   - **Standard:** tell the owner to start Block C in a fresh session: `claude --model opus`, then `/review <n>`.
   - **Small:** end your reply with `MAIN SESSION: run the review skill for #<n> now (Small tier, this session).`

## Never

- Never push to the default branch, force-push, or merge.
- Never edit the hooks, the check scripts or `harness.json` to make a check pass.
- Never push or open a PR while `BLOCKED` exists.
