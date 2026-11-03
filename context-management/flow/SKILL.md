---
name: flow
description: "Run a medium or large request on the main thread: parallel research, interview, build in slices, oracle review. Use before building anything that touches several files, an unfamiliar area or an open behaviour choice; not for a one-file change or an explicit /ac/plan."
---
<!-- ported-from: plugins/ac/skills/flow/SKILL.md sha256:ade5f1ba96005064505e558832978040e448aa77bff2cbce47f25c9311b4d0a8 -->

# flow

The default build flow for a request the working rules sized M or L. You stay on the main thread: research runs on cheap subagents, the user settles what only they can, you build (L: through tiered workers), and one `ac/oracle` reviews the result. No plan file is written. `/ac/plan` and `/ac/coordinate` start only when the user asks for them.

## Standing rules

These hold for the whole run and sit before the procedure so a compaction keeps them.

- Sizes are the working rules' S, M and L. Between two sizes take the larger; when research changes the picture, resize and say so in one line.
- Spend. Research runs on `ac/explore` (this repository) and `ac/librarian` (anything external), building on `ac/plan-worker-*`, review on `ac/oracle`. Never a general-purpose agent: it is the costliest way to run a slice.
- One message per fan-out. Every independent `subagent` call of a phase goes out together. Each brief names one angle; two angles are two briefs.
- Every subagent runs with `background: true`. After a fan-out, end the turn with a one-line status; each completion arrives as a notification that starts your next turn, and when one arrives while others still run, end the turn again. Never wait with a `sleep` or `until` loop, a file-stability check, or repeated reads of an output file.
- A subagent report is a claim. Open what it cites before it changes a decision.
- The review in phase 6 is the only reviewer. Do not spawn an agent to re-check your own work.
- Ceiling. More than six slices, or work that will not finish in this sitting: stop before phase 4 and ask once with `question` whether to continue here or to hand the work to `/ac/plan` or `/ac/coordinate`. Do not start either yourself.
- A failed subagent moves down its model chain; it is not a question. A `subagent` call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Recover by continuing the same child, not by a fresh spawn: call the `subagent` tool again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read and wrote (a fresh spawn repeats all of it). When it answered nothing or broke off mid-stream (`provider.invalid-output`, an empty report), continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config), since that is often a one-off; a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well (the child switches to it and keeps its context), and give that model the same number of attempts. A rate limit was retried 10 times inside the call, and the plugin gives one model 30 across continuations: `wait:<seconds>` means that model has retries left, so wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. The tool bounds those waits itself. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report or ask about. Asking the user whether to retry wastes a round on a provider fault the chain exists to absorb.

## 1. Size and success check

State both in one line: "M: <what changes>; done when <checkable condition>". The success check is what phase 5 and 6 hold you to.

## 2. Research (M and L)

M: one to three briefs in total. L: three to five `ac/explore` and one or two `ac/librarian`. Skip an angle one or two reads would settle, and skip the phase when the request names every file and line.

Brief shape, one block per angle:

```
CONTEXT: why this research, one or two sentences; cite the file or symbol you started from
GOAL: the specific question to answer
DEPTH: quick | medium | thorough
BUDGET: explore: a pass count. librarian: a number of web searches, five is the working ceiling
DOWNSTREAM: how you will use the result
REQUEST: what to return, the format, what to skip
```

`DEPTH` and `BUDGET` are required: an agent cannot apply a depth you did not send, and a blank field returns the thin default pass. Anything the user told you to leave out of research goes into the brief.

## 3. Interview

Answer from the code and the research first; ask only a preference, a priority, a tradeoff or an outward action.

- M: only the decisions that block the build, in one `question` call of up to three questions.
- L: walk the decisions that shape the result in rounds of up to three questions, until each has an answer or an accepted default. Record the defaults you assumed.
- Each option carries the concrete artifact (the snippet, path, value or consequence), your recommendation first, in the user's language.
- A decision that blocks nothing: take your recommendation, say so, carry on.

## 4. Build

M: implement it yourself, in the order that keeps each step verifiable.

L: write the slice table in your reply; it is also the progress list. Mark a row as it lands.

| # | Goal | Files | After | Tier | Done when |
|---|------|-------|-------|------|-----------|

- Files are disjoint across slices that run together. Two slices that touch one file are one slice, or run in order.
- Tier: the lowest that fits the slice, from the table in `references/worker-brief.md`.
- Dispatch each ready wave (slices whose `After` is met, files disjoint) as `ac/plan-worker-<tier>` calls, at most three at once, with the brief from `references/worker-brief.md`. Fill every section; a worker never opens anything you did not put in the brief.
- After a wave: compare `git diff --stat` with the slice file lists. A hunk no worker claimed, or a file outside a list, is yours to fix or revert. Then run, once for the wave and in parallel, the per-file checks on the wave's touched files, their related tests and one project-wide static analysis; never the full suite here (`../execute/references/verification.md`).
- Fix remediation yourself. Re-spawn a worker only for a `[BRIEFING GAP]` (repair the brief) or a tier mismatch (one tier up).

## 5. Verify

Hold the result to the success check from phase 1: the changed files clean by their CLI analyzer (a `<diagnostics>` block is a hint that can be stale; confirm it before you fix or dismiss it), the tests covering the change green (if nothing covers it, say so), and anything user-visible exercised the way a person would. Stop what you started.

## 6. Review

Start the full test suite and the repo-wide lint with `background: true` on the `shell` call, whether or not an oracle runs; both must be green before you report, and a failure there is a finding like the oracle's. One `ac/oracle`, in the same message, when the change crosses more than one file or is hard to reverse; a single-file M skips it. Send the diff and the claims it rests on: the success check, the interview decisions, the research sources. Fix what it confirms and say which findings you left and why.

## 7. Report

Result first: what changed, what the review found and what you did about it, the defaults you assumed, and what stayed unverified. When user-facing work landed, name `/ac/qa` as the next step. When the run settled a convention every later session must follow, or changed the architecture, name the file it belongs in and its writer (AGENTS.md, written by the user; the `architecture-md-writer` skill; the `design-md-writer` skill; the `project-md-writer` skill) instead of writing it unasked.

## References

| File | Read when |
|---|---|
| `references/worker-brief.md` | Phase 4, for every worker spawn and the tier table |
