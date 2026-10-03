---
skill_id: memory-palace
name: Memory Palace
description: "Cross-session memory — store, recall and query project knowledge across sessions. Detects whatever persistent memory is available (MemPalace, claude-mem, or file-only fallback) and uses the best one present."
version: 1.1.0
category: memory-palace
office: All
lead_agent: session-memory (built-in)
triggers:
  - remember this
  - what did we decide
  - recall
  - cross-session memory
  - memory palace
collaborates_with:
  - session-memory
  - operator-profile
---

# MemPalace Integration — Maxim Memory Intelligence

> Domain: memory-palace | Office: All (cross-office, always active)
> Version: 1.1.0 | Created: 2026-04-12
> Optional dependency: MemPalace MCP server (milla-jovovich/mempalace)
> Optional dependency: claude-mem plugin (thedotmack/claude-mem)

---

## Overview

Maxim's memory intelligence layer that detects and leverages whatever persistent memory tools are available — MemPalace, claude-mem, or file-only fallback. Maps Maxim's 7 executive offices to structured memory rooms for cross-session recall.

**Design principle:** Maxim never requires MemPalace or claude-mem. It detects what's installed and enhances output with whatever memory tools are available. File-based session memory (`.claude-sessions-memory/`) is always the source of truth.

---

## Tool Detection Protocol (runs on every session)

On session start, Maxim checks for available memory tools in this order:

### 1. MemPalace (semantic search + knowledge graph)
**Detect:** Check if `mempalace` MCP tools are available (19 tools: palace reads, search, graph queries, diary, system)
- If available: use for semantic search, cross-project recall, temporal fact retrieval
- If not: skip silently

### 2. claude-mem (persistent cross-session memory)
**Detect:** Check if `claude-mem` plugin skills are available (`mem-search`, `smart-explore`, `timeline-report`)
- If available: use for searching previous session context, code exploration, project history
- If not: skip silently

### 3. File-based memory (always available)
**Always active:** `.claude-sessions-memory/` files are read/written regardless of other tools
- This is the source of truth — MemPalace and claude-mem supplement it, never replace it

### Detection Output
```
MEMORY TOOLS DETECTED
  MemPalace  : [available / not installed]
  claude-mem : [available / not installed]
  File memory: always active
```

---

## What Maxim Ships (in this repo)

These files ship with maxim and work without any external tools:

| File | Purpose |
|---|---|
| `.claude/skills/memory-palace/SKILL.md` | This file — detection protocol + office mapping |
| `.claude/skills/memory-palace/Maxim-WRAPPER.md` | Behavioral layer compliance |
| `.claude/commands/mxm-remember.md` | Store context (MemPalace + files) |
| `.claude/commands/mxm-recall.md` | Retrieve context (MemPalace + files) |
| `templates/session-memory/` | File-based memory templates (always used) |

**What Maxim does NOT ship:** MemPalace binaries, claude-mem plugin, database files, embeddings. Users install these separately if they want enhanced memory.

---

## How Maxim Uses Each Tool

### When MemPalace IS installed

| Maxim Action | MemPalace Tool Used |
|---|---|
| `/mxm-remember` | `mempalace_store` — stores fact with wing/room/tags |
| `/mxm-recall` | `mempalace_search` — semantic search across wings |
| Session end | `mempalace_store` — saves key decisions and state changes |
| Session start | `mempalace_search` — loads relevant recent context |
| Cross-project query | `mempalace_search` — searches by project tag across all wings |

### When claude-mem IS installed

| Maxim Action | claude-mem Skill Used |
|---|---|
| `/mxm-recall` | `mem-search` — searches persistent memory database |
| Understanding code | `smart-explore` — token-optimized AST code exploration |
| Project history | `timeline-report` — development history narrative |
| Planning | `make-plan` — phased implementation with doc discovery |

### When NEITHER is installed (file-only mode)

| Maxim Action | File-Based Fallback |
|---|---|
| `/mxm-remember` | Writes to `.claude-sessions-memory/decision-log.md` |
| `/mxm-recall` | Searches `.claude-sessions-memory/*.md` files by content |
| Session end | Writes all 6 session memory files (always) |
| Session start | Reads MEMORY.md + project_current_state.md + handoff.md |

---

## Maxim Office-to-Wing Mapping (for MemPalace users)

MemPalace organizes memory into Wings > Rooms. Maxim maps its 7 executive offices:

| Maxim Office | MemPalace Wing | Rooms | What Gets Stored |
|---|---|---|---|
| CEO | `ceo` | `strategy`, `finance`, `investors`, `partnerships`, `governance` | Strategy decisions, investor context, financial models |
| CTO | `cto` | `architecture`, `tech-stack`, `deployment`, `apis`, `data`, `ai` | Architecture decisions, tech stack choices, deployment state |
| CMO | `cmo` | `brand-voice`, `content-calendar`, `seo`, `campaigns`, `metrics` | Brand voice rules, content calendar, marketing metrics |
| CSO | `cso` | `security`, `compliance`, `audits`, `threats`, `incidents` | Security findings, compliance audit results, threat models |
| CPO | `cpo` | `roadmap`, `user-feedback`, `features`, `research`, `ux` | Product roadmap, user feedback, feature priorities |
| COO | `coo` | `sprints`, `delivery`, `ops`, `support`, `experiments` | Sprint state, delivery metrics, operational procedures |
| CINO | `cino` | `research`, `emerging-tech`, `innovation`, `pocs` | R&D findings, emerging tech evaluations |

### Cross-Office Wing

| Wing | Room | Purpose |
|---|---|---|
| `maxim` | `handoffs` | Inter-agent handoff state across offices |
| `maxim` | `decisions` | Cross-office decision log with temporal validity |
| `maxim` | `project-state` | Project checkpoint snapshots |

---

## MemPalace Installation (optional — for users who want semantic memory)

### Windows
```powershell
# Requires Microsoft C++ Build Tools (for chromadb)
# Install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Create dedicated venv (Python 3.13 recommended — avoids 3.14 pydantic issues)
uv venv $HOME\.mempalace-env --python 3.13
uv pip install --python $HOME\.mempalace-env\Scripts\python.exe mempalace

# Register as MCP server
claude mcp add mempalace -s user -- "$HOME\.mempalace-env\Scripts\python.exe" -m mempalace.mcp_server
```

### Mac/Linux
```bash
pip install mempalace
claude mcp add mempalace -s user -- python -m mempalace.mcp_server
```

### Mining — Manual Only

**Mining is NEVER automatic.** Only mine when:
1. User explicitly runs `/mxm-ceo-setup` (asks about mining in Step 8)
2. User manually invokes `mempalace mine <path>`
3. User confirms their project folder is clean and organized

**Mine user projects, not the maxim framework repo.** The framework is reference code — mine the projects that use it.

```bash
# Mine a specific project
mempalace init --yes E:\Projects\my-project
mempalace mine E:\Projects\my-project

# Mine entire portfolio (only when folders are cleaned/organized)
mempalace init --yes E:\Projects
mempalace mine E:\Projects
```

**Local files (never committed, gitignored):**
- `config/mempalace.yaml` — project config
- `~/.mempalace/palace/` — global database

---

## Dual-Write Rule

Maxim writes to BOTH systems on every session end:
- `.claude-sessions-memory/` files — **always** (source of truth)
- MemPalace rooms — when available (supplements file memory)
- claude-mem — when available (supplements file memory)

If external tools are unavailable, fall back silently to file-only mode. Never block session end.

---

## Conflict Resolution

| Scenario | Resolution |
|---|---|
| MemPalace/claude-mem contradicts file state | **Files win** — files are source of truth |
| External tool has memory that files lack | **Supplements** — use as additional context |
| External tool unavailable | **Silent fallback** — file-only mode |
| Both MemPalace and claude-mem have results | **Merge and deduplicate** — present unified results |

---

## Commands

| Command | Description |
|---|---|
| `/mxm-remember` | Store important context (MemPalace + claude-mem + files) |
| `/mxm-recall` | Retrieve context by topic/project/office (searches all available tools) |

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
