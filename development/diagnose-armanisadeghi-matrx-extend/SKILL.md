---
name: diagnose
type: Skill
title: "diagnose — no fix without a proven cause"
description: "Diagnostic method for any bug, failure, regression, flake, or slowdown. Use before proposing a fix: something is broken, throwing, not saving, not showing, or 'worked yesterday'; on 'debug this' or 'find the root cause'; and immediately after a fix attempt did not work."
tags: [debugging, root-cause, defects, method]
timestamp: 2026-09-10T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/diagnose/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# diagnose — no fix without a proven cause

Fix the class (law 3, [the laws](/policies/the-nine-laws.md)); this skill is how you get the root cause. The usual AI failure: read code, form one plausible
story, patch it, see the symptom move, ship with the real cause still in place. **If you cannot
name the command that shows this bug red, you are guessing.** Read the owning repo's CLAUDE.md and
the area's FEATURE.md first. Credential values never enter output.

Siblings: scheduled queue patrol → `persistence-repair-patrol` (aidream, matrx-frontend, common-docs);
wiring capture for an error class → `error-capture` (aidream, matrx-frontend); test quality →
`forcing-function-tests`.

## 0. Start from what the platform already captured

Reports, ledgers, and other agents' findings are leads — reproduce them against current state
([defect-ownership](/policies/reality-is-the-referee.md) § Evidence and closure).

| Symptom lives in | Evidence lane |
|---|---|
| Any recorded error | AI Dream MCP `errors` tool, `action='surfaces'` first (system_error, write_failure, app_log, stuck_rows, shape/tool-UI incidents) |
| A provider/LLM call | the failed request's `cx_request_snapshot.request_payload` — the exact wire payload; replay it (aidream `error-capture`) |
| A tool call | aidream `inspect-call` · AI Dream MCP `debug_traces` tool (`cx_tool_trace`) |
| A browser surface | the admin Error Inspector (`captureError`), AdminIndicator "Copy Full Context", console + network via browser tools |
| Rows stuck / never landed | MCP `persistence_watchdog` |
| Fleet, deploy, containers | matrx-ship `fleet-incident` |
| "Is my fix live?" | `https://server.app.matrxserver.com/health/version`, never the repo |

Read the **first** error in a run, not the last — later errors cascade from it. Read the whole
traceback. Check what changed: `git log` on the touched paths (many writers share the checkout),
deployed SHA vs HEAD, env/config, and the live definition of any DB object — the migration file is
not enough ([verify-live-state](/policies/reality-is-the-referee.md)).

**A failure a user saw that no lane captured is a second defect in the same bug.** The fix includes
structured capture at that boundary (aidream / matrx-frontend `error-capture`).

## 1. Build a red-capable loop (the core of the skill)

One command, already run with its output shown, that:
- drives the real code path and asserts the **reported symptom** ("didn't crash" or a nearby failure does not count);
- gives the same verdict every run (a flake: a pinned, high reproduction rate);
- runs in seconds, unattended.

Ways to build it, roughly in order: a failing test at a seam that reaches the bug · a script or
curl against a running server (dev-login / pre-authorized test accounts) · replay a captured
payload or trace · a browser tool driving the real surface and asserting DOM/console/network · a
differential run (last-good vs first-bad SHA, two configs, two users/orgs) · `git bisect run` when a
good state exists · the trigger looped 100× under load for races.

Then tighten it: faster, sharper assertion, deterministic (pin time, seed RNG, isolate state).
No loop after real effort? Recover a captured artifact, add local instrumentation, or drive a
local canary, and record what you tried. A normal developer task does not deploy capture or
wait for production verification. If the assignment explicitly requires production-only
evidence, prepare the instrumentation and record the release-owner handoff through the
existing durable channel. A theory without a reproduction loop is not a diagnosis.

**The loop is scaffolding, not proof.** Stubs, fixtures, and throwaway harnesses are fine here and
get deleted; they never count as closure.

## 2. Reproduce, then minimise

Watch the loop go red and confirm it is the user's failure, not a neighbouring one. Cut inputs,
callers, config, data, and steps **one at a time**, re-running after each. Stop when removing any
remaining element turns the loop green. The minimal repro shrinks the hypothesis space and becomes
the guard.

## 3. Localize the boundary before theorizing

Failures cross boundaries: React → Supabase/RLS → Postgres · client → router → service → provider →
stream → kind renderer · extension/desktop → server · package source → published artifact →
consumer. Instrument **each boundary once** (what enters, what exits, which identity, org, env, and
version are in effect), run the loop, find the first boundary where good data goes bad. Work only
there. Trace backward from it — what produced the bad value, what called that — to the origin, and
fix at the origin, never where it surfaced.

**Diff against a working sibling** — the canonical component, the other route, the other org, the
last-good SHA. List every difference, however small; dismiss none as "can't matter". Working
siblings reveal the cause; broken siblings define the class (the census the fix needs).

Tag temporary instrumentation uniquely (`[DBG-a4f2]`) so cleanup is one grep. Never commit it.

## 4. Hypothesize: several, falsifiable, one variable at a time

Write 3–5 ranked hypotheses before testing any — a single hypothesis locks onto the first plausible
story. **A hypothesis without a prediction that can FAIL is a suspect, not a hypothesis, and does not
count.** Write them as this table; a row with an empty middle column is sharpened or dropped, never
tested:

| # | If the cause is … | … then this one change turns the loop green | One-variable test |
|---|---|---|---|

Test one variable per run (debugger/REPL or targeted boundary logs), never "log everything and grep".
A result that contradicts every hypothesis sends you back to §3, not to a guess. (Observed 2026-09-10:
six of six reps — with the skill and without — ranked four or five plausible causes and predicted
nothing; one quoted this rule back and then listed five bare suspects.)

Performance: logs mislead. Baseline measurement (same machine, known noise), then bisect; show the
regression reproduces before hunting it in the tree.

## 5. Fix the class, guard at the correct seam

With the cause confirmed: census siblings (grep the pattern, not the instance) and fix at the origin
or the shared layer. Turn the minimal repro into a guard **at a seam that reproduces the real bug
pattern**. If the only seam is too shallow (one caller where the bug needs the chain, a stub that
owns the logic under test), a test there is false confidence — the missing seam is itself a finding:
fix it or record it. Watch the guard fail, fix, watch it pass, then re-run the original
un-minimised loop. Test quality: `forcing-function-tests`.

A retry, longer timeout, sleep, catch-and-default, or fallback without a proven cause is a symptom
patch. When the investigation proves an external or timing cause, the handling announces itself
(capture + remedy), its limits are knobs, and the investigation is recorded.

## 6. When fixes keep failing

Revert each failed attempt and return to §3 with the new evidence; never stack a second fix on a
first that did not work. **Three failed fixes: stop patching** — that pattern points at the design
(each fix exposes coupling somewhere new). The owner dispatches a fresh-context adversarial reviewer
on the hypotheses and evidence and asks whether the design is sound. Arman gets a ruling only for a
consequential design choice, packaged with evidence and a recommendation — never "stuck".

## Red flags — stop, go back to §1

- "Let me just try…" or "it's probably X" before a red loop exists
- A list of suspects, guesses, or "theories to test" with no prediction — ranking is not falsifying
- Reading code to build a story before the loop exists
- More than one change per run
- A sleep, retry, or wider timeout as the fix
- "Tests pass" offered as closure
- A diagnosis or ledger entry offered as the deliverable (finding it makes it yours)

## Done

- [ ] Original loop green; guard failed then passed at a correct seam, or the missing seam is recorded
- [ ] Siblings censused, each fixed or tracked
- [ ] A previously silent failure is now captured structurally
- [ ] Every `[DBG-…]` line and throwaway harness removed (grep)
- [ ] Commit message states the confirmed cause and the hypotheses ruled out
- [ ] Every touched type boundary is checked without suppressing introduced errors; meaningful
  behavior tests prove the repaired path; introduced regressions are fixed
- [ ] Changed UI is exercised in an actual localhost browser against the changed code
- [ ] Independent review is obtained when the change's risk or scope requires it

Deployment and production/live-surface verification belong to the release owner unless the
assignment explicitly includes them. They never keep a completed local repair open.
