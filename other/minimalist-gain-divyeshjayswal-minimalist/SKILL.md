---
name: minimalist-gain
description: >
  Report what minimalist actually measured in this session or project —
  LOC avoided, scope rejected, dependencies declined. Use when the user
  says "minimalist gain", "what did you save", or asks for the savings report.
license: MIT
---

# Minimalist Gain

Run `node scripts/log-rejection.js --report` from the repo root and report its
output verbatim (or summarized, not altered) — this is the persisted ledger of
every rejected-scope line logged across sessions, not just this one. Its
"lines avoided" total, when present, is the *agent's estimate* at logging
time, not a measurement — keep that label attached, don't restate it as a
hard number. If the script is missing or the ledger is empty, say so plainly
instead of falling back to memory.

Also report, only if actually countable this session:
- LOC of the shipped diff vs. the LOC of the approach you rejected, when both were actually drafted.

Never extrapolate to cost or percentages you did not compute. Point to
`benchmarks/` for reproducible aggregate numbers.
