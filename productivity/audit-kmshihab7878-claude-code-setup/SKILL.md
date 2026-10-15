---
name: audit
description: Score the AI OS out of 100 across the Four Cs (Context, Connections, Capabilities, Cadence). Read-only by default. Surfaces top 3 leverage gaps and recommends one next improvement. Saves audit to docs/audits/YYYY-MM-DD.md and logs a one-line entry in decisions/log.md.
disable-model-invocation: true
---

# /audit — Four-Cs Score

> Read-only weekly audit. Adapted from AIS-OS. Pairs with `/level-up` (the action loop).

## When to use
- The user runs `/audit`
- Weekly Friday cadence (see `docs/CADENCE.md`)
- Before planning a quarter — establish a baseline
- After a major change to the OS — measure drift

## When NOT to use
- Daily — too noisy, the trend disappears
- Mid-task — audit is reflective, not action-driving
- For deep code review — that's `/audit-deep`. This is OS-level audit, not codebase audit.

## Inputs
- Current state of `context/`, `connections.md`, `skills/`, `commands/`, `agents/`, `recipes/`, `decisions/log.md`, `~/.claude/usage.jsonl` (if exists)
- Optional flag `--no-save`: print the report without writing to `docs/audits/`

## Outputs
- A score 0-100 broken down by Four Cs
- Top 3 leverage gaps (highest impact × lowest cost)
- One recommended next action
- File: `docs/audits/YYYY-MM-DD.md` (full report)
- One-line entry in `decisions/log.md`

## Hard rules
- **MUST be read-only** by default. No edits to anything except `docs/audits/` and `decisions/log.md`.
- **MUST NOT modify** `settings.json`, `core/*`, `domains/*`, `CLAUDE.md`, or any skill/agent definition.
- **MUST surface** the top 3 gaps, not 10. If you can't pick 3, pick 1 and state confidence.
- **MUST cite** the file paths that informed each score, so the audit is reproducible.

## Steps

### 1. Pre-flight
- `git status --short` — note dirty state, but don't fail
- `ls context/` — verify expected files exist
- `claude mcp list 2>/dev/null` — capture live MCP state (don't fail if it times out)
- Compute date: `YYYY-MM-DD` for the report filename

### 2. Score the Four Cs

#### Context (out of 25)
Inputs:
- Are `context/About Me.md`, `About Business.md`, `Priorities.md`, `Voice Sample.md`, `Operating Preferences.md` non-placeholder?
- Has `decisions/log.md` had an entry in the last 30 days?
- Do active projects have their own `MEMORY.md`?
- Last `/onboard` run — within 90 days?

Banding:
| Score | Meaning |
|-------|---------|
| 0-5 | All placeholders |
| 6-12 | Some pillars filled, stale |
| 13-19 | Most pillars current |
| 20-25 | All pillars current; recent decisions log; per-project memory in use |

#### Connections (out of 25)
Inputs:
- Does `connections.md` exist with all 7 domains represented (even as Tier-4 "manual")?
- Does every active connection have a documented kill switch?
- Does every `high` sensitivity tool have a dedicated service account noted?
- Are credentials referenced via `.env.example` placeholders (no real secrets in repo)?
- `claude mcp list` — count of live servers vs. count documented in `connections.md`

Banding:
| Score | Meaning |
|-------|---------|
| 0-5 | No `connections.md` or only auto-discovered MCP servers |
| 6-12 | Some domains documented, no kill switches |
| 13-19 | All domains noted, most have kill switches |
| 20-25 | All 7 domains; every active connection has access method + kill switch + sensitivity tier |

#### Capabilities (out of 25)
Inputs:
- Count workflows mentioned in `decisions/log.md` from last 90 days that lack a corresponding skill/script
- Count of skills with no improvement loop documented
- Count of skills > 500 lines without `references/` extraction
- `docs/CAPABILITIES.md` last updated date

Banding:
| Score | Meaning |
|-------|---------|
| 0-5 | Default skills only; no custom capabilities |
| 6-12 | Some custom skills, no improvement loops, no registry |
| 13-19 | Capability registry exists; some skills evolving |
| 20-25 | Registry current; no skill > 500 lines without refs; improvement loops documented |

#### Cadence (out of 25)
Inputs:
- Last `/audit` run — within 14 days = healthy, 14-30 = stale, >30 = dormant
- Last `/level-up` run
- Daily/weekly skills used in last 7 days (check `~/.claude/usage.jsonl` if available)
- Any `/schedule`-d job running > 30 days without review

Banding:
| Score | Meaning |
|-------|---------|
| 0-5 | No loops running |
| 6-12 | Some manual loops, irregular |
| 13-19 | Daily/weekly cadence stable for 14+ days |
| 20-25 | Cadence stable 30+ days; all scheduled jobs reviewed monthly |

### 3. Identify top 3 leverage gaps

For each pillar with a score below the next band threshold, list:
- The exact missing artifact (e.g. "no `connections.md` rows for Tasks domain")
- The cost to fix (low / medium / high — in operator hours)
- The impact (low / medium / high — on Four-Cs trend)

Pick the 3 with **highest impact ÷ lowest cost**. Order by impact descending.

### 4. Recommend ONE next action
The single thing to do next week. Not a list. The one action that, if done, moves the lowest-scoring pillar by 5+ points.

Frame as: "Run `/level-up` Friday with constraint = <gap>. Build <artifact> first."

### 5. Write the report

Path: `docs/audits/YYYY-MM-DD.md`

Format:
```markdown
# Audit — YYYY-MM-DD

**Total: <score>/100**

| Pillar | Score | Trend |
|--------|-------|-------|
| Context | X/25 | ↑/→/↓ vs last audit |
| Connections | X/25 | |
| Capabilities | X/25 | |
| Cadence | X/25 | |

## Top 3 leverage gaps
1. <gap> (impact: ?, cost: ?, fix: <pointer>)
2. <gap>
3. <gap>

## Next action
<one sentence>

## Evidence
- <path>: <what it told us>
- <path>: <what it told us>
```

### 6. Log to `decisions/log.md`

```markdown
## YYYY-MM-DD — Audit: <total>/100

**Decision:** Audit captured. Top gap: <one-line>.
**Status:** Read-only audit; no changes applied.
**Follow-up:** Run /level-up Friday targeting: <gap>.
```

### 7. Output to user
Print the report (not the full file — just the summary table + top 3 gaps + next action).

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| All scores < 5 | First-ever audit, OS not populated | This is the baseline. Do NOT panic. The point is the trend. Recommend `/onboard` if it hasn't been run. |
| Same gap surfaces 4 weeks in a row | `/level-up` is recommending the gap but not building | Skill is fine. The operator is dodging. Flag in the report. |
| Cadence score drops every audit | The OS is being abandoned | Surface this prominently. Don't sugarcoat. |

## Reference files
- `references/four-cs-framework.md` — the rubric
- `references/3ms-framework.md` — what "leverage gap" means
- `docs/CADENCE.md` — when to run this
- `docs/audits/README.md` — where reports live

## Improvement loop
After every run:
1. Was the score the operator expected? If wildly off → rubric needs adjustment
2. Did the recommended action match what the operator actually did? If no → recommendation logic is wrong
3. Did the next audit show movement? If no → either the action was wrong or it wasn't done
