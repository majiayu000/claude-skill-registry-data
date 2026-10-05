---
name: memory-lora
version: 1.0.0
description: Cross-session memory with SQLite+FTS5 backend. Triggers on errors, pattern discoveries, corrections, task completions.
---

# Memory — Cross-Session Learning System

> "今天学会的明天不会忘。同错两次自动写规则。"

## Trigger

Memory writes (bounded, not every action):

| Event | Action | Score |
|-------|--------|-------|
| Error occurred | Store bug + fix | +0.3 |
| Pattern discovered | Store reusable solution | +0.2 |
| User corrected you | Store correction (high priority) | +0.5 |
| Task completed | Store decisions + lessons | +0.1 |
| Session start | Load index, decay scores, archive expired | — |

Memory recall:
- "上次"/"又"/"还是" → immediate search
- Similar error to known pattern → auto-suggest fix
- Session start → report active memory count

## Five-Layer Architecture

| Layer | What | Storage |
|-------|------|---------|
| L0 | Core rules (CLAUDE.md) | Always loaded |
| L1 | Route index (MEMORY.md) | Session start |
| L2 | Global facts | memory.db (SQLite + FTS5) |
| L3 | Task skills | skills/ directory |
| L4 | Session archive | Compressed summaries |

## Storage Backend

Single file: `~/.claude/memory.db` (SQLite 3.x + FTS5 BM25)

```powershell
scripts/memory-db.ps1 -Action store -EntityName "X" -EntityType "bug" -Content "..." -Score 0.9
scripts/memory-db.ps1 -Action search -Query "keyword" -Limit 10
scripts/memory-db.ps1 -Action stats
scripts/memory-db.ps1 -Action export -Query markdown
scripts/memory-db.ps1 -Action prune
```

## Three Engines

### 1. Hybrid Retrieval (from PMB + Hindsight)
Three parallel strategies, merged:
- **Keyword**: FTS5 BM25 full-text search
- **Temporal**: What was learned around the same time?
- **Entity**: Follow relation graph to connected memories

### 2. Outcome Scoring (from Roampal)
Each memory: -1.0 to +1.0 usefulness score.
- Applied successfully → +0.15
- Recalled but ignored → -0.05
- 30 days unaccessed → -0.10
- 60 days unaccessed → x0.5
- Below -0.5 → auto-archive

### 3. Token Compression (from NeuralMind)
- Storage: L4 sessions compressed 40-70x
- Recall: Total ≤5% context window budget

## Write Gate (from Vestige)

Before storing: is this surprising? novel? useful? actionable?
Default policy: if it passes any one gate (surprise, novelty, utility, or actionability), store. If it fails all four, skip. Storage is cheap; lost insight is expensive.

## Scope Isolation

- `global`: Universal lessons, shared across projects
- `project`: Project-specific, isolated
- `temporary`: 24h auto-expire

## Integration

| Partner | Status | What flows |
|---------|--------|-----------|
| precommit-pipeline | 🔜 | Bug caught → memory stored |
| reasoning-lora | 🔜 | Pattern found → memory stored |
| delegation-lora | 🔜 | Sub-agent queries memory first |
| second-brain | 🔜 | Brain 2 findings → memory if accepted |
| skill-judge | 🔜 | Verdicts → cross-session tracking |
| skill-auditor | 🔜 | Scores → baseline for future audits |

Integration planned. Currently via manual scripts/memory-db.ps1 calls. Goal: automatic hook triggers.
