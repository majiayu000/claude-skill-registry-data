---
name: team-dispatch
description: Use when a request has two or more parts that can proceed independently — investigations, reviews, audits, comparisons, verification, or reading across several files — "look into these three", "review this from several angles", "audit all X", "sweep the codebase for Y", "why is this failing". NOT for single-file edits, sequential work, or tasks needing approval partway through.
---

# team-dispatch

Fan work out across teammates without waiting to be asked. Spawn on your own
judgement, announce what you are doing, and keep going.

## The test

All three must hold. If any fails, stay inline.

1. **Throwaway output** — the lane produces a lot of material you will not
   reuse. Reading twelve files to answer one question qualifies.
2. **Independent** — the lane can be understood without the others' findings.
3. **Read-heavy and self-contained** — no edits, no mid-flight decision from
   the user. A subagent cannot ask a question.

Shorthand: if the lane is "go find out X and tell me the answer", delegate it.
If it is "let's work on this together", keep it.

## Sizing

- **3–5 teammates** for most work. Three focused beat five scattered.
- **5–6 tasks per teammate** keeps everyone busy and lets you reassign.
- Fifteen independent tasks still means about three teammates, not fifteen.
- Decompose by **territory, not phase**. Splitting plan → build → test creates
  handoffs that lose context without isolating any.
- Two teammates must never own the same file.

## Cost

**Teams cost 3–10x a single session.** Read-only lanes are nearly free;
lanes running builds or test suites must be serialised — one at a time.

## Teammate or subagent

A named `Agent` call (`name` set, no `isolation`) is a teammate: its own
process in a tmux pane the user can watch, scroll back through after it
finishes, and type into; it stays alive and idle afterwards, keeping its
context for follow-ups via SendMessage. An unnamed call is a subagent: it
runs inside this session, returns one result, and is gone.

**Default to a named teammate.** Use one when any of these holds:

- the user might want to see or audit how the lane reached its answer;
- follow-ups on the same ground are likely;
- the lane is substantial — several steps or several minutes.

Reviews, investigations and audits nearly always qualify.

**Use an unnamed subagent only** for a one-shot lookup whose answer is all
you need, or when a skill or workflow you are following prescribes
subagents (for example a plan-execution pipeline of implementer and
reviewer). Teammates cannot spawn teammates, so inside a teammate use
subagents.

Before starting work on a request that has independent parts, state the
decision in one line — `Lanes: a, b, c → teammates`, `→ subagents`, or
`Inline: <reason>` — so skipping fan-out is a visible choice, not a default.

## Protocol

Reconcile, state the lanes, then spawn. Do not ask.

0. **Reconcile.** `~/.claude/skills/team-teardown/scripts/reap-teammates.sh --idle`
   (a dry run) prints one `IDLE <name> type=<agentType> cwd=<cwd>` line per
   idle teammate of this session. SendMessage any whose type and directory
   fit a lane — that lane is now covered. Then
   `reap-teammates.sh --idle --keep <reused,...> --yes` reaps the rest and
   records the reconcile (`--keep` is omitted when nothing was reused). With
   no idle teammates, the dry run lists none; skip straight to step 1.
   Then state the remaining lanes and spawn them in one message.
1. Name each remaining lane and what it will return, in one short line each.
2. Issue **every** spawn in a single message — multiple calls in one response
   run in parallel; one per response runs them in series.
3. Keep working. Do not block waiting for the first result.

Skip step 0 and the spawn gate (`spawn-gate.sh`, a `PreToolUse` hook on
`Agent`) stops you: while this session has idle teammates and no
`--idle --yes` reconcile has run in the last 120 seconds, it refuses a named
teammate spawn, lists the idle teammates, and marks the ones reusable for
that spawn (same directory and type). Reconcile once, then re-issue only the
spawns you still need.

## Briefing

Brief each lane like a colleague who just walked in.

- Give **file paths and line numbers**, the question, and the deliverable.
- For a lookup, hand over the exact command. For an investigation, hand over
  the question — prescribed steps become dead weight when the premise is wrong.
- Never write "based on your findings, fix it". That pushes synthesis onto the
  agent and returns shallow work. Synthesis is your job.
- For review lanes, give the code, not your conclusion. An agent handed your
  hypothesis tends to return it confirmed.
- State what NOT to do when a cheap wrong path exists.

## Verifying what comes back

Teammates report their final message as the deliverable. A bare "Done." means
read their report. Do not relay a lane's claim as fact — check load-bearing
claims yourself, especially numbers, star counts, and URLs.

## Obligation

**Reuse before you spawn.** Teardown happens at the next reconcile, not when
a lane finishes. A teammate whose lane is done stays alive and idle so the
next batch can reuse it; the reconcile in Protocol step 0 is where idle
teammates that fit are reused and the rest are reaped.

## Supported platforms

`scripts/session-start.sh` is tested on macOS (BSD `ps`, bash 3.2.57) and
Linux (Debian 13.6, procps-ng 4.0.4, bash 5.2.37, verified in a container via
`../team-teardown/tests/run-linux.sh`) — `test-session-start.sh` passes
identically (66/66) on both. Not tested: BusyBox `ps` (Alpine), WSL, or any
distro besides Debian — see the design doc's "Supported platforms" section
for exactly what was run and what wasn't.

## Related skills

- `team-teardown` — the other half: the reconcile (`reap-teammates.sh
  --idle`) that reuses or reaps idle teammates before a spawn, and the full
  request → verify → reap teardown for teammates a previous session left
  running
- `/cancel` — for OMC modes (`ralph`, `ultrawork`, `omc-teams`, `autopilot`,
  `swarm`), not native Claude Code teams
