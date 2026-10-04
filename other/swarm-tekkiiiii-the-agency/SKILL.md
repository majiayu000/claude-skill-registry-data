---
name: swarm
description: >
  Parallel dispatch to all Project Directors in the agency — one-shot status, blocker, or priority check across the entire portfolio without loading PD context into the parent session. Spawns each PD in a fully isolated subagent that reads only their heartbeat file and responds in one line. Trigger when: the user says "/swarm", "/swarm-blocker", "/swarm-continue", or "/swarm-all"; you need a portfolio-wide status across all active projects at once; the user asks "what is everyone working on" or "any blockers across the portfolio?"; doing a weekly check-in sweep; before a planning session to surface conflicts. Key capabilities: reads the agency-council team config to discover all PDs dynamically; dispatches all agents in parallel (not sequentially); handles silent PDs with one automatic respawn; formats a clean digest table per PD with their project and one-line response. Also for: cross-project priority conflicts, surfacing work that can continue without a blocked PD, getting a fast portfolio health snapshot before a client call. Parent session holds zero PD context until responses arrive — fast and cheap.
---

# /swarm — Portfolio-Wide PD Dispatch

**What it does:** Spawns all active PDs in parallel, each in an isolated subagent context. The parent session only holds the digest — not the full PD briefs. Fast and cheap.

## Command Variants

| Command | Question sent to each PD |
|---|---|
| `/swarm` | What are you currently working on? Any blockers? ETA for next deliverable? |
| `/swarm-blocker` | What is your current blocker? Who owns it? What's the workaround or path to resolution? |
| `/swarm-continue` | What can continue without you? Any pre-reqs you need from others? |
| `/swarm-priority` | What are your top 3 priorities right now? Any priority conflicts with other PDs? |
| `/swarm-all` | Full status dump — current work, blockers, wins, decisions pending, next steps. |

## How It Works

### Step 1 — Discover PDs

Read `~/.claude/teams/agency-council/config.json`. Extract member names that end in `-pd` (Project Directors). These are the inbox names for SendMessage.

For each PD, derive their project directory:
```
~/.claude/projects/{project-name}/   (most PDs)
~/Projects/{project-name}/memory/     (ltv)
~/projects/{project-name}/memory/     (website-pitch, sightsee)
```

If a PD has no known project, skip them.

### Step 2 — Dispatch All PDs in Parallel

Spawn one pd-coordinator subagent per PD. Each agent:
- Sets `team_name: agency-council` (so it can send back via SendMessage)
- Sets `run_in_background: true`
- Receives only: their inbox name, project directory, and the question
- Does NOT load the full PD-BRIEFING — only reads `heartbeat.md` and the question
- Responds directly to `team-lead` via SendMessage with a one-line status

**Agent prompt for each PD:**
```
You are checking in on {project-name} as a swarm dispatch from /swarm.

Do NOT load PD-BRIEFING.md or any other briefing files.
Read only: {project-dir}/memory/heartbeat.md

Answer this question in ONE LINE (under 80 chars for status/blocker, up to 2 lines for continue):
{question}

Include your PD name at the start of your response.
Send your response via SendMessage to "team-lead".

Example response format:
examplecrm-pd: BLOCKED — Railway auth needed from the operator; workaround is local dev
```

**Subagent config:**
- `subagent_type`: Explore
- `model`: sonnet

### Step 3 — Wait for Responses

Wait for all spawned agents to complete (they send back via SendMessage).

### Step 4 — Handle Silent PDs

If a PD does not respond within the agent's reasonable run time:
1. Note: `⚠️ {pd-name} silent — respawned`
2. Re-spawn the same PD agent once
3. If still silent after respawn: note `❌ {pd-name} did not respond after respawn`

### Step 5 — Present Digest

Format the digest as:

```
## /swarm — {command-variant} — {timestamp}

### Responding ({n})
| PD | Project | Response |
|----|---------|----------|
| {pd-name} | {project} | {one-line status} |

### Silent / Respawned ({n})
| PD | Project | Status |
|----|---------|--------|
| {pd-name} | {project} | silent → respawned / no response |

### Portfolio Summary
{1-2 sentence synthesis}
```

## Dispatch Isolation

Each PD agent runs in a completely isolated context:
- Only reads `heartbeat.md` (not the full CLAUDE.md/PROJECT.md/PROJECT-BRIEFING)
- No shared state between agents
- No mutual blocking between agents
- Parent session holds zero PD context until responses arrive

## PD Standard Protocol — Also Applies Here

Even for one-shot /swarm dispatches, PDs that receive work items must:
1. **Decompose** tasks into smallest independent sub-tasks
2. **Parallelize** — spawn one subagent per sub-task simultaneously
3. **Report** every sub-task completion to "team-lead" via SendMessage immediately

If a PD receives a task during a swarm check-in (not just a status query), apply the full
PD Standard Protocol from `/pd-resume`.

## PD Directory Map

| PD | Project Directory |
|---|---|
| my-app-pd | `~/.claude/projects/my-app/` |
| example-crm-pd | `~/.claude/projects/example-crm/` |
| landing-site-pd | `~/projects/landing-site/` |

If a project directory doesn't exist, skip that PD silently.

## Anti-Patterns

- DO NOT load all PD-BRIEFING files into the parent session before spawning
- DO NOT run PDs sequentially — that defeats the purpose
- DO NOT aggregate in the parent session — let each PD speak for themselves
- DO NOT include CLAUDE.md or PROJECT.md content in the digest — heartbeat only
- DO NOT chase silent PDs more than once — note and move on
