---
name: emperor-dispatch
description: >-
  Emperor Time — DISPATCH / Steal Chain. Consent-first enlistment of local
  CLIs (Claude Code, Kimi, Codex, Copilot, opencode, Ollama). Use when the user
  asks to use another agent, parallelize, or review via a different model.
license: MIT
metadata:
  version: 0.4.141
  chain: steal-chain
  part-of: emperor-time
---

# Emperor Dispatch (Steal Chain wrapper)

1. Read `chains/steal-chain/SKILL.md` → one aspect
   (`consent-protocol.md` first unless consent is already on the ledger).
2. Dowse the machine (`scripts/dowse.sh` / `dowse.ps1`) if the roster is stale.
3. Client consents per agent per task (or a standing policy they stated).
   **MUST — consent HARD-GATE:** before dispatch, run
   `scripts/emperor consent <task-dir>` (or `steal-consent`).
   Doctrine: `chains/steal-chain/consent-protocol.md`. Use
   `--reject-no-consent` / `--check-consent`. Missing CONSENT /
   header theater / uncovered enlisted agent → exit 1. G4 calls
   `scripts/lib/consent.py` when steal activity is present.
4. Workers receive the **work order + named files**, never the author's diary.
5. Capture to `.emperor/runs/<task>/<agent>/` (`prompt.md`, `out.txt`, `meta.md`).
6. Output is CONJECTURE until Judgment + `scripts/gate.sh g4`.
7. **MUST — quarantine HARD-GATE:** before merging worker output, run
   `scripts/emperor quarantine <task-dir>` (or `steal-quarantine`).
   Doctrine: `chains/steal-chain/quarantine.md`. Missing runs layout /
   CONJECTURE start / ADMITTED|REJECTED → exit 1. G4 calls
   `scripts/lib/quarantine.py` when steal activity is present.
8. Sign-in is the client's terminal. You never run interactive logins.
   **MUST — sign-in / dispatch / swarm HARD-GATE:** when claiming steal
   sign-in, dispatch, or swarm-emulate, run
   `scripts/emperor steal-flow <task-dir>` (aliases: `sign-in-handoff`,
   `steal-dispatch`, `swarm-emulate`). Doctrine leaves:
   `sign-in-handoff.md` / `dispatch.md` / `swarm-emulate.md`. Use
   `--reject-no-signin` / `--reject-no-dispatch-layout` /
   `--reject-unbounded-swarm` / `--check-signin` / `--check-dispatch` /
   `--check-swarm`. Missing SIGN-IN HANDOFF (or credential material),
   incomplete runs layout / OBJECTIVE+SCOPE, or unbounded swarm → exit 1.
   G4 calls `scripts/lib/steal_flow.py` when matching activity is present.

## MUST — parallel-dispatch checklist for independent domains

When facing 2+ *independent* tasks / failures / subsystems (disjoint writable
scopes, no shared root cause) — before launching concurrent agents — open
`skills/emperor-dispatch/parallel-dispatch-checklist.md`
(Chain Jail leaf from Superpowers `dispatching-parallel-agents` → Identify
Independent Domains / Focused Agent Tasks / Parallel Dispatch / Review and
Integrate only)
and/or run `scripts/emperor parallel` (prints the mechanical PARALLEL / STEP /
MUST card).

One agent per independent domain. Focused self-contained briefs. All dispatches
in the same response for true parallelism. Review and integrate before done.
Do not load whole `dispatching-parallel-agents`; ET + emperor-dispatch
orchestrate. Sequential plan tasks stay `emperor subagent` (no parallel
implementers on the same plan). Inline stays `emperor execute`.
