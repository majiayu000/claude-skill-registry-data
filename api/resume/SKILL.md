---
name: "resume"
description: "Resume a previous hunt. Shows hunt history, untested endpoints, memory-informed suggestions. Usage: /resume target.com"
---

# Resume

*Sourced from h-mmer-pentest-agents*

Resume hunt on: $ARGUMENTS

## What This Does
1. Read brain for target: `uv run python3 ../../tools/brain.py brief $ARGUMENTS`
2. Read brain exhausted: `uv run python3 ../../tools/brain.py exhausted $ARGUMENTS`
3. **Read chain-pending advisory**: `cat .claude/agent-memory-local/chain-pending.md 2>/dev/null` — feeder findings from prior session waiting for chain dispatch. SURFACE THESE FIRST — they have proven dollar value if chained, vs untested surface which is speculative.
4. **Generate / refresh chain plan**: `uv run python3 ../../tools/chain_plan.py $ARGUMENTS` — writes `evidence/<target>/CHAIN_PLAN.md` with 3-5 candidate next-links per pending feeder finding plus the agent to dispatch for each. Read this BEFORE picking the next vuln class — proven feeders trump speculative untested surface.
5. Read recon data from recon/ directory
6. Show what's been tested vs what remains
7. Suggest next techniques based on brain patterns

## Output
```
RESUME: target.com
═══════════════════

Brain Status:
  Confirmed findings: N
  Exhausted techniques: N
  Effective techniques: N

Untested Surface:
  1. /api/v2/users/{id}/export — not tested
  2. /api/v2/users/{id}/share — not tested
  ...

Suggestions:
  - Tech stack [X] matches pattern where IDOR was found before
  - Sibling endpoints of confirmed finding not yet tested

Actions:
  [h] /hunt target.com — resume hunting
  [s] /surface target.com — re-rank attack surface
  [r] /recon target.com — re-run recon (surface may have changed)
  [m] /monitor check — check for target changes since last session
```

## Top-Tier Resume Logic

Resume by value, not chronology.

Priority order:
1. `chain-pending` confirmed feeders with clear next link
2. validated partials needing one proof artifact
3. changed assets from `/monitor`
4. untested P1 crown-jewel endpoints
5. high-confidence class hypotheses from prior wins
6. stale recon refresh

Show what not to redo. If an area is exhausted, include the exact blocker and matrix coverage. A resumed hunt should start with a single best command, not a menu of every possible command.

