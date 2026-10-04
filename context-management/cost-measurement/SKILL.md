---
name: cost-measurement
description: Measure token usage and USD cost for any Skill Heaven benchmark arm, dispatched worker, or session. Use whenever reporting spend, comparing the cost of two postures, or logging session token spend. Wraps gaia-research/skill-cost, the canonical cost basis for the whole ecosystem.
---

# Cost Measurement

**`gaia-research/skill-cost` is the canonical basis for every cost measure in the Gaia
ecosystem.** Do not hand-roll token accounting, do not read harness JSONL yourself, and do not
quote a price from memory. If a number is going into a report, it comes from here.

Repo: <https://github.com/gaia-research/skill-cost> · registry id `gaia-research/skill-cost`

---

## Why this and not self-reported numbers

`skill-cost` reads the **session logs the harness actually wrote** and prices every turn against
[BerriAI/litellm](https://github.com/BerriAI/litellm)'s canonical
`model_prices_and_context_window.json`, refreshed weekly. That means:

- Numbers are **persisted usage**, not a model's guess about its own consumption.
- Cache reads and cache writes are counted separately — which matters enormously, since cache
  reads routinely dominate total tokens and are priced very differently.
- Every harness is priced the same way, so cross-harness arms are comparable.

Asking a model how many tokens it used produces confabulation. Reading the log does not.

---

## Supported harnesses

| Harness | Session storage |
|---|---|
| pi | `~/.pi/agent/sessions/**/*.jsonl` |
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| OpenAI Codex | `~/.codex/sessions/**/*.jsonl` |
| opencode | `~/.local/share/opencode/**/*.jsonl` |
| Hermes Agent | `$HERMES_HOME/state.db` (SQLite, read-only; usage tables only, never transcripts) |

**Known gap: Grok is not supported.** If a Grok arm needs pricing, that is a
`parse_grok` function in `cost.py` — adding a line-oriented harness is one small parser. The
repo is part of our ecosystem and may be extended when a gap blocks a measurement.

---

## Run

```bash
cd ~/skill-cost

python3 cost.py                          # newest logical session across all harnesses
python3 cost.py --latest                 # latest session per harness in cwd
python3 cost.py --today --by-model       # today, per-model breakdown
python3 cost.py --all --list             # one line per session, everything
python3 cost.py --since 2026-08-01 --harness claude-code
python3 cost.py --cwd "$PWD"             # only sessions rooted at this directory
python3 cost.py --session 019f4e66       # substring match on session id
python3 cost.py --json                   # machine-readable
python3 cost.py --offline                # no network; use bundled prices.json
```

---

## Costing a benchmark arm

Each arm runs in its own pane with its own `--cwd` (see `herdr-benchmark-pane`). That `--cwd`
is what makes arms separable afterwards:

```bash
python3 ~/skill-cost/cost.py --cwd /path/to/arm-a --json
python3 ~/skill-cost/cost.py --cwd /path/to/arm-b --json
```

Rules that keep the comparison honest:

- **Price arms separately. Never average them.** The doorless benchmark floor and the doorful
  product floor are different objects (founder ruling V5-5); a blended number is meaningless.
- **Record the harness version** alongside every cost figure. A dose measured on one version
  does not carry to another.
- **Report cache reads and writes**, not just a total. Two arms with identical totals and
  different cache mixes cost very different amounts.

---

## Costing dispatched workers

Workers dispatched into herdr panes each get their own session log, keyed by the pane's `--cwd`.
Nested in-harness subagents are logged separately too, under
`.../<session-id>/subagents/agent-*.jsonl`. So a full session's spend — orchestrator plus every
worker plus every scout — is recoverable after the fact with `--today --by-model`.

This is what makes the required end-of-session spend log cheap: run one command, read the real
numbers.

---

## Session spend logging

Repo policy requires logging input/output token spend by model and date on every commit push,
reported to the operator at session close.

```bash
python3 ~/skill-cost/cost.py --today --by-model
```

Format the result as: `<date> <model> <effort>: <in> in, <out> out. ~$<usd>`

Use the tool's figures verbatim. Do not round them into vagueness and do not estimate a number
the tool can give you exactly.

---

## Anti-patterns

- **Asking a model to self-report its token usage.** It will confabulate.
- **Quoting a price from memory.** Prices move; the catalog refreshes weekly for a reason.
- **Reporting a total without the cache split.** Hides the dominant cost term.
- **Averaging two arms into one number.** Destroys the comparison the benchmark exists for.
- **Writing a new token counter.** It already exists; extend `cost.py` instead.
