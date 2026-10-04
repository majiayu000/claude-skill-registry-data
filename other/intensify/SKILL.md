---
name: intensify
description: Philosophy-driven depth mining for any active zone. Spawns parallel agents to find high-yield intensification moves. Persists findings across sessions so value compounds. Use when user says /intensify, "what else can we do here", "go deeper", "mine this", or wants to extract more value from current work without adding bloat.
---

# /intensify

Replace "keep improving" with structured depth mining. Never builds new. Only deepens, wires, and resurfaces. Compounds across sessions.

## Input

`/intensify [zone] [--quick|--deep]`

- Zone: optional. If omitted, infer from conversation context.
- Depth: optional. If omitted, infer from zone size.

| Depth     | Agents                                        | Time  | When                                                  |
| --------- | --------------------------------------------- | ----- | ----------------------------------------------------- |
| `--quick` | 1 (cartography only)                          | ~30s  | Pulse check. Zone < 5 files or "anything obvious?"    |
| (default) | 2 parallel + 1 sequential                     | ~2min | Normal pass. Most invocations.                        |
| `--deep`  | 2 parallel + 1 sequential + cross-domain scan | ~5min | Large zone, first-ever run, or user wants exhaustive. |

**Auto-depth inference:** Count files in zone (`lib/{zone}/`, `components/{zone}/`, `app/**/{zone}/`). Under 5 = quick. 5-30 = normal. Over 30 = deep.

## Philosophy (Non-Negotiable)

Accretive Coherence (see `memory/project_foundational_philosophy.md`):

- Intensification over extension
- Connective cartography (find tether points)
- Saturation-based pacing (stop when yield drops)
- Never add noise. Never add bloat. Only add resolution.

## Persistence Layer

**Every run reads and writes `docs/intensify/{zone}.md`.**

Before spawning agents, check if `docs/intensify/{zone}.md` exists:

- If YES: read it. Pass prior findings to agents. They must only surface what's NEW or RESET (fresh data invalidated a prior conclusion).
- If NO: first run on this zone. Create the file after.

After presenting results, append to the zone file:

```md
## Run {date}

STATUS: {saturation status}
DEPTH: {quick|normal|deep}

SURFACED:

- {finding 1}
- {finding 2}

ACTED ON: (filled when user picks moves)

- {move chosen}

SKIPPED:

- {item}: {why}

NEXT TRIGGER: {what resets saturation here}
```

This makes the skill compound. Third run on same zone only shows what changed since second run.

## Execution

### Quick Mode (1 agent)

Spawn single agent (model: sonnet):

- Read zone files + prior intensify log
- Find 1-3 obvious unwired connections or fresh data
- Return in under 10 lines

### Normal Mode (2+1 agents)

**Phase 1: Spawn Agents 1 and 2 in parallel.**

#### Agent 1: Context Digest (model: haiku)

Produce structured summary of where we are.

```
Zone: {zone}
Prior runs: {summary from docs/intensify/{zone}.md or "first run"}

Tasks:
1. Read most relevant spec in docs/specs/ for this zone
2. git log --oneline -15 -- {relevant_paths}
3. Check docs/UNIFIED-BUILD-QUEUE.md for zone entries
4. Check docs/build-state.md

Output (structured, not prose):
ZONE: {name}
SPEC: {spec file or "none"}
FILE_COUNT: {number of files in zone}
BUILT: {bullet list of what exists}
RECENT: {last 3 meaningful changes}
ACTIVE: {in-flight items}
GAPS: {spec says but code doesn't have}
PRIOR_FINDINGS: {count of previously surfaced items from zone log}
```

#### Agent 2: Cartography (model: sonnet)

Find unwired tether points, unmined signal, fresh data. Adaptive to zone size.

```
Zone: {zone}
Prior findings to SKIP (already surfaced): {list from docs/intensify/{zone}.md}

Adaptive strategy:
- Small zone (< 10 files): read all imports, trace all connections exhaustively
- Medium zone (10-30 files): scan interfaces and boundaries, check recent git activity
- Large zone (30+ files): sample top-level exports, focus on cross-domain boundaries

Tasks:
1. Identify 3-5 NEARBY domains (read lib/ structure, imports, shared types)
2. For each: is data/signal flowing INTO this zone? Or disconnected?
3. Recent additions (git log --since="2 weeks ago" -- lib/) that created NEW nodes
4. CIL/PIE/intelligence layer signal relevant but not consumed
5. Patterns where this zone duplicates logic that exists better elsewhere
6. EXCLUDE anything in the "already surfaced" list unless fresh data reset it

Output (structured):
TETHER_POINTS:
- source: {x}, target: {y}, enables: {what}, stable: {yes/no}

FRESH_DATA:
- node: {x}, offers: {what}, since: {date or commit}

REDUNDANCIES:
- pattern: {x}, better_version: {location}

DEAD_ENDS:
- connection: {x}, premature_because: {reason}
```

**Phase 2: Spawn Agent 3 with output from 1+2.**

#### Agent 3: Saturation Ranker (model: haiku)

Rank by yield. Filter diminishing returns. Produce final move list.

```
Zone: {zone}
Context: {Agent 1 output}
Cartography: {Agent 2 output}
Prior run count: {N}
Prior saturation status: {from zone log}

Tasks:
1. Score each finding: HIGH (new structural understanding), MEDIUM (incremental), LOW (diminishing)
2. Remove LOW items entirely
3. Check if zone was recently audited (look for audit docs). Note what's ALREADY SATURATED.
4. For HIGH items: is endpoint stable enough to wire NOW?
5. Compare to prior runs: is yield DECLINING? If yes, flag zone as approaching saturation.

Output (structured):
SATURATION: {fresh | partially-mined | near-saturated | saturated-until-reset}
YIELD_TREND: {increasing | stable | declining}

MOVES:
- rank: 1, action: {x}, yield: HIGH, stable: {yes/no}, reason: {why high-yield}
- rank: 2, action: {x}, yield: HIGH, stable: {yes/no}, reason: {x}
- rank: 3, action: {x}, yield: MED, stable: {yes/no}, reason: {x}

SKIP:
- item: {x}, reason: {premature|low-yield|already-saturated}

NEXT_PAUSE: {concrete trigger that resets saturation, e.g. "after invoice spec lands" or "when CIL adds event signals"}
```

### Deep Mode

Same as Normal, plus Agent 2 gets expanded scope:

- Scan ALL of lib/ for cross-domain connections (not just nearby 3-5)
- Check graphify-out/GRAPH_REPORT.md for architectural edges
- Look at docs/CLAUDE-DOMAINS.md for categorized domain relationships

## After Swarm Returns

Present to user:

```md
## /intensify: {zone}

**Status:** {saturation} | **Trend:** {yield trend} | **Run:** #{n}

**Moves:**

1. {action} — {reason} {stable: yes/no}
2. ...
3. ...

**Skip:** {premature items, one line each}

**Pause when:** {concrete trigger}

**Prior runs:** {count} | **New this run:** {count of genuinely new findings}
```

Then persist to `docs/intensify/{zone}.md`.

Do NOT auto-execute. Present list. User picks. Mark chosen moves in zone log.

## Anti-Patterns

- NEVER suggest "add a new feature" — intensify means deepen existing
- NEVER suggest cosmetic/UI polish unless it wires a real connection
- NEVER suggest documentation as an intensification move
- NEVER surface findings already in the zone log unless fresh data reset them
- NEVER wire to unstable endpoints — flag as SKIP with concrete "stable when" trigger
- NEVER spawn 3 agents for a quick pulse — match effort to scope
- Move count scales with depth: quick = 1-2, normal = 3-4, deep = up to 6
