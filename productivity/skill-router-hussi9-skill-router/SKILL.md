---
name: skill-router
description: Use when a [skill-router] route card appears in the turn, when no card appeared on a non-trivial task, or when a route looks wrong. Routes every prompt to the right installed skill, pairs it with a process skill, tiers enforcement, and briefs sub-agents. 79 local skills + plugin skills indexed.
---

# Skill Router (v4.2)

Routing runs from hooks. A `UserPromptSubmit` hook classifies every prompt
and injects a **route card** before your first action. Your job is to
*follow the card*, not to compute one.

## The route card

```
[skill-router] This is a BROKEN task — 2-step chain.
[skill-router] Chain: mac-doctor → superpowers:systematic-debugging
▶ mac-doctor  (inherit, in-session)
▶ superpowers:systematic-debugging  (inherit, in-session)
[skill-router] Gates before done: simulator screenshot
[skill-router] Memory: airbook_crash_root_cause  (read from ~/.claude/projects/-Users-airbook/memory/)
[skill-router] IRON RULE: call Skill(skill="mac-doctor") before any Edit/Write/Task.
```

- **First `▶` is the domain skill** — one of yours, or a plugin's. Load it first.
- **Second `▶` is the process skill** (debugging, planning, TDD). Load it next.
- **Gates** are completion conditions from the project. Check every one before "done".
- **Memory** names the memory file for this project. Read it before deciding.

## Two tiers

| Line on the card | Meaning |
|---|---|
| `IRON RULE: …` | **hard** — Edit/Write/Task are denied until the skill is loaded. BROKEN path, and project routes with gates. |
| `Soft route: …` | **soft** — nothing is blocked. If you finish without loading it, the Stop hook asks once; answer by loading it or by one line `[skill-router] skipped <skill>: <reason>`. |

Wrong route either way: `python3 ~/.claude/skills/skill-router/scripts/router_override.py "<reason>"`.
The user can also write `[no-router]` in their message.

## How the card is decided

1. **Project route** in `SKILL.personal.md` (`@economicalai`, `capgo`, …) — deterministic.
2. **Jev** (TypeSafe System One, `jev_choose.py`, ~0.4 s, cached) reads the whole enriched index (`~/.claude/skill_index.json`) in one call — no lexical pre-filter, so typos do not matter — and answers two Choice questions: domain skill, process skill. Confidence ≥ 0.8 routes; anything lower is silence (a 0.5–0.8 `Possible fit:` line exists behind `SKILL_ROUTER_JEV_SUGGEST=1`, off by default — it was right one time in three). When Jev answers, only Jev puts a skill on the card; a skill already loaded this session is never carded again.
3. **Fallback** when Jev fails or passes 1.2 s: lexical rank of the index (~50 ms), then a small model (Gemini Flash-Lite, ~1 s, cached) over the top candidates.
4. **Process table** (`references/routing-tables.md`) supplies the process leg on the fallback path only.

Questions, discussion and harness noise get no card. Silence is an answer.

## Which model does the work (v4.2)

The same Jev call answers a fourth question, **work tier**: `light`
(grep, list, summarise, rename, one fixed rule across files), `standard`
(routine work against a clear spec) or `heavy` (design, root cause, security,
anything ambiguous). Same 0.8 gate; below it, or `heavy`, nothing changes.

| Where | What happens |
|---|---|
| Sub-agent dispatch | The `Task`/`Agent` hook judges the sub-agent's *own* prompt and sets `model`: light → `haiku`, standard → `sonnet`, else inherits the session. An explicit `model=` in your call always wins. |
| Route card | `Work: light (jev 0.91) → sub-agents dispatch on haiku` — one line, only when the tier moves the model. Delegate the bulk part; it will come back on Haiku. |
| Quota strained | When the status line has reported a 5-hour or weekly window ≥ 80 % and the work is light/standard, the card adds one line pointing at Kimi: `bash scripts/kimi_offload.sh [--tier light] "<task>"` — a second `claude -p` on Moonshot (K2.7-code for light, K3 1M otherwise). Run it from Bash and use its output. Heavy work never goes to Kimi. Once per half hour per session; at ≥ 95 % the bar drops from 0.8 to 0.5. |

Knobs: `SKILL_ROUTER_SUBAGENT_MODEL=0` (never set a dispatch model),
`SKILL_ROUTER_KIMI=quota|always|off` (default `quota`),
`SKILL_ROUTER_QUOTA_HIGH=80`, `SKILL_ROUTER_QUOTA_CRITICAL=95`.
`scripts/quota.py` prints what the router currently believes.
The whole router stands down under `SKILL_ROUTER_OFF=1` (the Kimi child sets it).

## Sub-agents

Every `Agent(...)` dispatch gets the parent's route appended to its prompt
(skill, gates, memory) and its model set from the work tier above, and
`SubagentStart` briefs the agent with the skills paired to its type.
Enforcement never reaches inside a sub-agent.

## When there is no card

Non-trivial task, no `[skill-router]` line? Run the fallback yourself:
`python3 ~/.claude/skills/skill-router/scripts/router.py <<< "the prompt"`.
If that is silent too, routing may be dead: `python3 ~/.claude/skills/skill-router/scripts/doctor.py`.

## Maintenance

| Command | When |
|---|---|
| `scripts/doctor.py` | routing feels dead, or after a Claude Code upgrade |
| `scripts/build_index.py --enrich` | you installed or edited a skill |
| `scripts/index_match.py --all "<prompt>"` | a route looked wrong — see the ranking |
| `scripts/learn.py --show` | what has been learned |
| `scripts/check.sh` | after editing any routing logic |

Project routes, projects, gates: `SKILL.personal.md`. Full tables and protocols: `references/routing-tables.md`.
