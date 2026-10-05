---
name: constellation
description: >
  Multi-persona council system. Assembles 4-6 PI persona subagents to analyze
  any topic through diverse behavioral lenses. Use /constellation audit,
  /constellation discover, /constellation build, /constellation ship, or
  /constellation search.
---

# Constellation Command

Assembles a council of Otto's PI personas to analyze a topic. Each persona contributes their perspective, Captain synthesizes, Guardian holds veto authority.

## Commands

| Command | Lead | Purpose |
|---|---|---|
| `/constellation audit` | Guardian | Alignment check across repos |
| `/constellation discover <topic>` | Scholar | Research/brainstorm |
| `/constellation build <topic>` | Maverick | Innovation planning |
| `/constellation ship <topic>` | Guardian | Deployment readiness |
| `/constellation search <query>` | Captain | Free-form, auto-routed |
| `/constellation refresh repos` | — | Force refresh all repo relays |
| `/constellation refresh personas` | — | Force refresh all persona relays |

## Execution Protocol

### Step 1: Parse Command

Extract from the ARGUMENTS string:
- `command`: audit, discover, build, ship, search, or refresh
- `query`: everything after the command keyword
- `scope`: if `--scope X,Y` is present, parse as list; default to all repos
- `depth`: if `--depth shallow` is present, use shallow; default to deep

If command is `refresh`, handle it directly:
- `refresh repos`: Call `POST http://localhost:8100/constellation/relays/repos/refresh` and display results
- `refresh personas`: Display all persona relays from `GET http://localhost:8100/constellation/relays/personas`
- Return after refresh — no council needed.

### Step 2: Fetch Relay State

```bash
# Fetch repo relays
curl -s http://localhost:8100/constellation/relays/repos

# Fetch persona relays
curl -s http://localhost:8100/constellation/relays/personas
```

Check freshness. If any relay is stale (>30 min), refresh it:
```bash
curl -s -X POST http://localhost:8100/constellation/relays/repos/refresh
```

### Step 3: Select Council

Call the State Service or determine locally based on command type:

| Command | Council |
|---|---|
| audit | captain, guardian, analyzer, controller, operator |
| discover | captain, scholar, strategist, venturer, individualist |
| build | captain, maverick, venturer, artisan, persuader |
| ship | captain, guardian, operator, controller, analyzer |
| search | captain + 3-5 most relevant based on query analysis |

If `--depth shallow`, use only captain + lead + 1 expanded member.

### Step 4: Write Briefing

Compose a ~200 token briefing document containing:
- The original query
- Scope (which repos are in play)
- Key facts from repo relays (recent commits, health status, services)
- Key facts from persona relays (current concerns, opportunities)
- Context from the current repo (if relevant)

### Step 5: Dispatch Council (Parallel Subagents)

For each council member (excluding Captain), dispatch a subagent using the Agent tool. Use `model: "sonnet"` for cost efficiency.

Each subagent receives the council-prompt.md template with variables filled in:
- Persona profile data from `GET http://localhost:8100/persona/profiles/{id}`
- The briefing from Step 4
- Their persona relay cache
- The query

**IMPORTANT:** Dispatch ALL council subagents in a SINGLE message (parallel execution). Do NOT dispatch them sequentially.

Example for a discover council:

```
Agent 1 (Scholar — lead):
  prompt: [council-prompt.md filled with Scholar profile + briefing + query]
  model: sonnet
  description: "Scholar perspective"

Agent 2 (Strategist):
  prompt: [council-prompt.md filled with Strategist profile + briefing + query]
  model: sonnet
  description: "Strategist perspective"

Agent 3 (Venturer):
  prompt: [council-prompt.md filled with Venturer profile + briefing + query]
  model: sonnet
  description: "Venturer perspective"

Agent 4 (Individualist):
  prompt: [council-prompt.md filled with Individualist profile + briefing + query]
  model: sonnet
  description: "Individualist perspective"
```

### Step 6: Collect Perspectives

Parse JSON responses from each subagent. Each should return:
```json
{
  "persona": "scholar",
  "position": "...",
  "conviction": 8.4,
  "concerns": ["...", "..."],
  "opportunities": ["...", "..."],
  "recommends_action": true
}
```

### Step 7: Guardian Gate

Scan all perspectives for safety/sustainability/alignment concerns.
If any such concern has conviction ≥ 7.5, set guardian_gate to HARD_DISAGREE.
Otherwise PASS.

### Step 8: Captain Synthesis

As Captain, write the synthesis:
- Summarize the consensus (what do most personas agree on?)
- Highlight dissent (who disagrees and why?)
- Recommend next actions
- Set decision status: INFORMATIONAL, AWAITING_ZAC, or BLOCKED

### Step 9: Persist Report

**Primary:** Try the state service first:
```bash
curl -s -X POST http://localhost:8100/constellation/query \
  -H "Content-Type: application/json" \
  -d '{
    "command": "...",
    "query": "...",
    "scope": [...],
    "council": {...},
    "perspectives": [...],
    "briefing": "...",
    "synthesis": "...",
    "guardian_gate": {...}
  }'
```

**Fallback (always):** Write a YAML report file to the decision log regardless of whether the HTTP call succeeds. This is the durable record.

```
File: ~/Desktop/Airlock/repos/airlock-coordination/reports/YYYY-MM-DD-HH-MM-{command}-{slug}.yaml
Schema: ~/Desktop/Airlock/repos/airlock-coordination/reports/schema.yaml
Index: ~/Desktop/Airlock/repos/airlock-coordination/reports/INDEX.yaml
```

**IMPORTANT — Privacy rule:** The `request_summary` field must be a SYNTHESIZED generalization of the user's request, NOT verbatim input. The user's messages may contain personal, sensitive, or heartfelt content. Distill the intent to 1-2 neutral sentences. Example: "Evaluate whether the current auth architecture is ready for multi-tenant production" — not the user's exact words.

The report YAML must follow `schema.yaml`. After writing the report file, prepend an entry to the `reports` list in `INDEX.yaml` with: date, command, request_summary, decision_status, and filename.

Set `resolution.action` to `pending` initially. If the user responds with accept/override/dismiss, update the report file.

### Step 10: Render Report

Display the report in this format:

```
══════════════════════════════════════════════════
  CONSTELLATION REPORT
  Type: {command} | Query: "{query}"
  Date: {date} | Council: {count} personas
══════════════════════════════════════════════════

BRIEFING (Captain)
{briefing}

──────────────────────────────────────────────────

{PERSONA_NAME} ({EMOJI}) — Lead — Conviction: {N}
Position: {position}
Concerns:
  • {concern1}
  • {concern2}
Opportunities:
  • {opp1}
  • {opp2}

──────────────────────────────────────────────────

(repeat for each council member)

══════════════════════════════════════════════════
  CONSENSUS
  Avg Conviction: {N} | Agreement: {X}/{Y}
  Dissent: {persona} ({reason})

  GUARDIAN GATE: {PASS|HARD_DISAGREE}
  {if HARD_DISAGREE: reason}
══════════════════════════════════════════════════

CAPTAIN SYNTHESIS
{synthesis}

Decision Status: {status}
Override History: {history or "none"}
══════════════════════════════════════════════════
```

If HARD_DISAGREE: Prefix with "⚠ GUARDIAN HARD DISAGREE" and show the Guardian's reasoning prominently.

If AWAITING_ZAC: End with "What's your call? (accept / override / dismiss)"
