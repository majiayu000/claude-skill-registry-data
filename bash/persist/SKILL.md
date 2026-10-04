---
name: persist
tier: D
primitive: P12
category: orchestration
description: "bstack P12 — Persistent Loop Discipline. Cross-context restart loop where state lives in the filesystem (PROMPT.md + git tree + state.jsonl), not in the conversation. Each iteration spawns a fresh agent context. Solves the failure mode where work that must outlive one session loses its state when the session ends, and where a loop that keeps re-trying one fix never gets a clean start. Validation backpressure comes from compilers/tests/linters, not model self-grading. Use persist when: (1) starting work that must outlive the session (overnight, unattended), (2) the same fix failing repeatedly in one session, (3) coordinating long-horizon work that needs to survive crashes / context exhaustion, (4) running parallel work streams (one persist loop per worktree, composed with bstack P5). Triggers on 'persist', 'long-horizon loop', 'context restart', 'fresh-context iteration', 'P12', 'Ralph loop', 'filesystem-state loop'."
---

# persist — bstack P12 Persistent Loop Discipline

**Cross-context restart loop. State in filesystem, not conversation.**

The defining moves:
1. The agent writes a goal + state snapshot to `PROMPT.md`
2. `persist iterate PROMPT.md` spawns a fresh agent context per iteration
3. State persists in the filesystem (`PROMPT.md` + git tree + `state.jsonl`)
4. Validation backpressure: compilers/tests/linters, **not** model self-grading
5. Loop exits when success_condition fires OR budget exhausted OR user interrupts

## Why this exists

Work that must outlive one session needs state that survives the conversation. **Persist restarts the context every iteration** while keeping state in the filesystem, so the loop survives session ends, crashes and repeated failed attempts. METR's [Time Horizon 1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/) put Opus 4.6's 80%-reliability horizon at about an hour; that is a measurement of an older model, and current models run a 1M context with automatic compaction in Claude Code, so it is context for the design, not a trigger.

## When to invoke

The reflexive trigger rule (full text in workspace AGENTS.md §P12):

1. **Before starting work that must outlive this session** — write `PROMPT.md`, decide budget, pick success condition. Call `persist iterate` when it should run unattended (an overnight run); when it is paused for a later session, leave `PROMPT.md` for the session that resumes it.
2. **When the same fix has been attempted ≥3 times without convergence** — stop the in-context loop; write the diff history to `PROMPT.md` and start fresh.
3. **When orchestrating long-horizon work** — default to persist with periodic checkpoints; compose with P5 worktrees for parallel persist loops.

## CLI

```bash
persist iterate PROMPT.md \
  --max-iterations 50 \
  --max-wall-clock 14400 \
  --success-condition "grep:DONE:STATUS" \
  --agent-cmd "claude -p '{}'"

persist status                  # show open loops
persist status --json           # machine-readable
persist abandon <loop-id>       # terminal: mark ABANDONED, free slot
persist doctor                  # health-check (state dir, git available)
persist conformance             # run test battery
```

The `{}` token in `--agent-cmd` is replaced with the prompt file's contents. Default agent is `claude -p '{}'`. Codex: `--agent-cmd "codex {}"`. Gemini CLI: `--agent-cmd "gemini -p '{}'"`.

## Success conditions

Three forms:

- **`exit-code-0`** — last agent invocation returned 0
- **`file-exists:PATH`** — agent writes a sentinel file when done
- **`grep:PATTERN:FILE`** — agent writes a status line that matches PATTERN

The agent is responsible for **updating PROMPT.md or writing the sentinel file** at the end of each iteration. The script doesn't try to interpret agent output — that's the *backpressure must come from external signals* invariant.

## State machine

```
SPAWNED ──→ ITERATING ──→ ITERATING ──→ ... ──→ SUCCESS (terminal)
                  │                          ╲
                  ↓                           ↘ BUDGET_EXHAUSTED (terminal)
              PAUSED ──→ ITERATING            
                  │
                  ↓
              ABANDONED (terminal)
```

State events append to `~/.config/broomva/persist/state.jsonl` (JSONL append-only with `flock`).

## Composition with bstack

| primitive | composes via |
|---|---|
| **P5** Parallel Agents | run N persist loops, one per `git worktree` |
| **P7** CI Watcher | each iteration's pushed PR uses `p9 watch` for productive-wait |
| **P10** Worktree Hygiene | clean tree before iteration; janitor after each merge |
| **P11** Empirical Feedback | per-iteration validation; persist's success_condition is multi-modal evidence |
| **P6** Bookkeeping | persist loops produce graph-relevant material → `bookkeeping replay` between loops |

## Invariants

- **State lives in the filesystem.** Each iteration starts from PROMPT.md content, not conversation history.
- **Validation backpressure is external.** Don't ask the agent "are you done?" — check exit codes, file presence, or status pattern.
- **Budget bounds must be honored.** Default 50 iterations / 4h wall-clock.
- **State.jsonl is append-only.** Loop terminations are terminal — no resurrection. To restart, spawn a new loop with a new ID.
- **Each iteration is a fresh process.** `persist` calls the agent CLI in a subprocess; agent context never persists between iterations except via filesystem state.

## See also

- bstack workspace AGENTS.md §P12 — the binding reflexive trigger rule
- [bstack/references/primitives.md](https://github.com/broomva/bstack/blob/main/references/primitives.md) — full primitive contract

## Background

Pattern popularized by Geoffrey Huntley as ["everything is a ralph loop"](https://ghuntley.com/loop/) (Jan 2026). Anthropic shipped a [`ralph-wiggum` plugin](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md); OpenAI shipped [`/goal` in Codex CLI 0.128.0](https://simonwillison.net/2026/Apr/30/codex-goals/). bstack's P12 is the same mechanism with non-anthropomorphized naming and explicit composition with the rest of the bstack contract.
