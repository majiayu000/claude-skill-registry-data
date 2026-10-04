---
name: memory-tiering
description: |-
  Multi-tiered memory management (HOT/WARM/COLD) for context compaction. Invoke ONLY for explicit
  compaction events: post-`/compact` cleanup, MEMORY.md tier promotion, archive batch, or "trim my context".
  NOT for general recall (use deep-recall) or routine memory writes (use storage-router).
  Triggers: "compact memory", "promote to durable", "archive old context", "tier this".
---

# Memory Tiering Skill 🧠⚖️

> **2026.4.10 Update:** OpenClaw now has two native memory systems — **Active Memory** (runs before every reply) and **Dreaming** (nightly consolidation at 3 AM IL). This skill covers what they DON'T handle — see section below.

## What Native Systems Now Cover (don't duplicate)

| Task | Who does it |
|---|---|
| Pull relevant context before each reply | Active Memory plugin (automatic) |
| Promote strong signals to MEMORY.md nightly | Dreaming / memory-core (automatic) |
| HOT.md pattern promotion after 2x mistakes | self-learning skill |

## What This Skill Still Handles

- Manual pruning when MEMORY.md grows >200 lines
- Archiving old `memory/daily/YYYY-MM-DD.md` files (30-day retention)
- Force-promoting critical owner corrections immediately (don't wait for Dreaming)
- **Graduation gate** — reviewing and filtering dream promotions before they land in MEMORY.md
- Post-compaction reorganization
- Enforcing store boundaries: daily notes = raw-first log, `MEMORY.md` = durable rules only, project docs = project-scoped

## The Three Tiers (for manual ops)

1.  **🔥 HOT (`memory/hot/HOT_MEMORY.md`)** — current session, active tasks
2.  **🌡️ WARM (`memory/warm/WARM_MEMORY.md`)** — stable preferences, configs
3.  **❄️ COLD (`MEMORY.md`)** — long-term, distilled, curated

## Workflow: `Organize-Memory` (Manual / Post-Compaction)

### Step 1: Check native systems first
```bash
openclaw memory status --deep   # see what Dreaming already promoted
/dreaming status                  # check last run
```

### Step 2: Ingest & Audit
- Read MEMORY.md + last 7 `memory/daily/YYYY-MM-DD.md` files
- Identify Dead Context: completed tasks, resolved issues, stale facts

### Step 3: Prune & Redistribute
- Remove stale COLD entries (if Dreaming already promoted better versions)
- Force-add critical owner corrections → MEMORY.md immediately (don't wait for Dreaming)
- Archive daily notes older than 30 days → `memory/archive/YYYY-MM/`

### Step 4: Verify
- MEMORY.md should be <200 lines after cleanup
- Check `DREAMS.md` — are Dreaming's promotions accurate? Prune bad ones.

## Progressive Context Compaction (inspired by Claude Code harness patterns)

Long sessions degrade quality as context fills. Apply progressive compression by conversation age:

### Compression Layers (oldest → newest)

| Layer | Age | Strategy | Detail Level |
|---|---|---|---|
| **HISTORY_SNIP** | >50 turns | Drop entirely or keep 1-line summary | ~5% |
| **Microcompact** | 30-50 turns | Aggressive: decisions + outcomes only | ~15% |
| **CONTEXT_COLLAPSE** | 15-30 turns | Medium: key exchanges, skip tool noise | ~40% |
| **Full Detail** | <15 turns | No compression | 100% |

### When to Apply
- Session exceeds 30 turns
- Context window pressure detected (tool responses getting truncated)
- After any `/compact` command

### How to Apply (Manual)
1. Identify turn count in current session
2. For turns older than 30: summarize into a single "Session context so far" block
3. For turns 15-30: keep decisions and outcomes, drop tool output and exploration
4. Keep last 15 turns at full detail
5. Always preserve: owner corrections, final decisions, error causes

### What Never Gets Compressed
- Owner corrections and preferences
- Permission decisions (approved/denied actions)
- Error root causes and fixes applied
- Active task state and pending items

### Gap vs. Claude Code
Claude Code does this in the harness layer (code, not prompt). We currently rely on manual `/compact` and prompt-level instructions. Future improvement: move compaction logic into OpenClaw's session management layer so it runs automatically without consuming agent tokens.

## Usage Trigger
- Trigger manually: "Run memory tiering" or when MEMORY.md >200 lines
- Trigger automatically after any `/compact` command

---

## Dreaming Integration (OpenClaw 2026.4.9+)

Dreaming is **already enabled** (`memory-core` plugin, `0 3 * * *` IL timezone).

**What Dreaming does automatically:**
- Light phase: ingests daily notes + session transcripts
- Deep phase: scores & promotes strong signals → MEMORY.md (weighted: relevance 0.30, frequency 0.24, recency 0.15)
- REM phase: extracts themes and patterns

**Manual CLI for inspection/intervention:**
```bash
openclaw memory status --deep          # what's queued for promotion
openclaw memory promote                # preview what would promote
openclaw memory promote --apply        # force apply now
openclaw memory promote-explain "term" # why something would/wouldn't promote
/dreaming status                        # last run summary
```

**What still requires manual action:**
- Owner corrections → MEMORY.md **immediately** (don't wait for Dreaming)
- Critical session-startup rules → MEMORY.md **manually**
- Pruning bad/stale Dreaming promotions → manual cleanup
- MEMORY.md growing >200 lines → prune manually

## Graduation Gate (inspired by agentic-stack)

Dreaming stages candidates. Nothing graduates to MEMORY.md without passing this gate:

### Minimum Requirements
- **Score >= 0.70** (weighted relevance + frequency + recency)
- **Recalls >= 2** (the signal was retrieved and used at least twice)
- **Status = staged** (raw candidates with status=staged only)
- **Content is a rule, preference, or durable fact** — not a raw conversation fragment, not a debug log, not a confidence=0.00 dream corpus entry

### Rejection Criteria (auto-reject)
- Confidence = 0.00 or status != staged
- Content is a raw session transcript or chat log (contains `Candidate: User:` or `Candidate: Assistant:` or `evidence: memory/.dreams/`)
- Duplicate of an existing MEMORY.md entry (same semantic content)
- Content is ephemeral (specific timestamps, one-off events, resolved issues)

### Review Process
1. Run `openclaw memory promote` to list candidates
2. For each candidate, check against minimum requirements and rejection criteria
3. **Accept** only with a one-line rationale: why this is durable and useful
4. **Reject** with a one-line reason: why this doesn't belong
5. Rewrite accepted content into clean, concise rule format before adding to MEMORY.md
6. Never paste raw dream output directly into MEMORY.md

### Post-Review Cleanup
- After review, clear processed candidates from DREAMS.md staging area
- Log review outcome in `memory/daily/YYYY-MM-DD.md`: `[HH:MM] Dream review: accepted N, rejected M`

### Safety Rules
- Content changes (MEMORY.md): require explicit review — never auto-apply
- Archiving old files: safe to run automatically
- `trash` > `rm` always

### Retention Policy
- Daily notes: keep 30 days → archive to `memory/archive/YYYY-MM/`
- Archive: keep 90 days → delete
- MEMORY.md: prune if >200 lines

### Health Indicators
- ✅ Healthy: MEMORY.md <200 lines, DREAMS.md updated nightly, daily notes exist
- ⚠️ Warning: MEMORY.md 200–300 lines, Dreaming didn't run in 48h
- ❌ Critical: MEMORY.md >300 lines, no Dreaming output in 7 days
