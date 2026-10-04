---
name: storage-router
version: "1.1.0"
description: "Decide where to save any piece of information — monday.com, local file, daily notes, or MEMORY.md. Use this skill before saving anything to ensure the right destination. Prevents local clutter and ensures the owner can access all relevant content in monday.com."
---

# Storage Router

> **2026.4.10 update:** With Active Memory + Dreaming enabled, the default flow is now: raw fact → daily note first, Dreaming promotes later. `MEMORY.md` is for curated long-term rules, confirmed preferences, and critical exceptions.

Before saving anything, route it to the correct destination.

---

## Decision Table

| Content Type | Destination | Notes |
|---|---|---|
| Competitor research | monday.com — Competitive Analysis doc | your monday.com workspace |
| Product briefs, strategy docs | monday.com — relevant doc | your monday.com workspace |
| Meeting notes | monday.com — Notetaker / item update | |
| Project tasks / tracking | monday.com — board item | |
| PA rules & preferences | MEMORY.md | Long-term only, distilled |
| Lessons learned | `memory/daily/YYYY-MM-DD.md` first | Dreaming promotes later if strong/repeated |
| Daily event log | `memory/daily/YYYY-MM-DD.md` | Raw log, not curated |
| WhatsApp conversation context | memory/whatsapp/groups/ or dms/ | Per-conversation, local |
| Cron state / job state | local JSON (data/ or inbox/) | Runtime state only |
| PA contact list | PA_LIST.md (local) | Source of truth for PA sync |
| Config / credentials | local only, never monday | Security |
| Skill files | workspace/skills/ | Never monday |

---

## Persistent Layer Decision

| Layer | Best for | Why |
|---|---|---|
| **GitHub** (private repo) | Agent state, memory, skills, .context | Version history, automated backup, private |
| **monday.com** | Research, docs, tasks, strategy | Searchable, shareable, owner-accessible |
| **Local only** | Runtime state, credentials, cron state | Speed, security, no sync needed |

**Rule of thumb:**
- Owner needs to read/share it → monday.com
- Agent needs it across sessions → GitHub
- Ephemeral or secret → local only

---

## Rules

### ALWAYS → monday.com
- Research (competitors, market, technology)
- Documents the owner needs to access or share
- Project tracking, tasks, milestones
- Meeting summaries
- GTM, product, strategy content

### ALWAYS → GitHub (private repo)
- MEMORY.md, daily notes, .context files
- Skill files (SKILL.md → pa-skills public repo)
- Agent behavioral rules and preferences
- Lessons learned (daily note first, not direct to MEMORY.md by default)

### ALWAYS → local only
- Runtime state (cron jobs, inbox, heartbeat state)
- WhatsApp memory (per-conversation context)
- Credentials and config
- PA directory (PA_LIST.md)

### NEVER
- ❌ Save research/docs to local files only
- ❌ Save credentials or config to monday.com
- ❌ Save WhatsApp context to monday.com
- ❌ Duplicate content across layers

---

## Local Context

Load agent-specific IDs from `.context` file in this skill's directory:
```bash
CONTEXT_FILE="/path/to/workspace/skills/storage-router/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $WORKSPACE_ID, $FOLDER_RESEARCH, $DOC_COMPETITIVE_ANALYSIS, etc.
```
If `.context` doesn't exist — use Structure Index doc (DOC_STRUCTURE_INDEX) from monday.com to find current IDs.

---

## monday.com Workspace Map

**Workspace:** your monday.com workspace
**Structure Index Doc:** 39993682 (always check here for latest IDs)

| Content | Folder | Board/Doc ID |
|---|---|---|
| Competitor analysis | 📁 Research (20077300) | Board: 18406632346 / Doc: 39808656 |
| Market research | 📁 Research (20077300) | Board: 18406632334 |
| Technology deep dives | 📁 Research (20077300) | Per-tool board (see index) |
| Product brief | 📁 Product (20077301) | Board: 18406632301 / Doc: 39808645 |
| MVP planning | 📁 Product (20077301) | Board: 18406632217 |
| GTM strategy | 📁 GTM (20077298) | Board: 18406632223 |
| PA Rollout tracking | 📁 Operations (20077299) | Board: 18407159006 |
| Skills guide | 📁 Operations (20077299) | Board: 18407110746 |

> For full index with all IDs: read doc 39993682 in monday.com before saving anything new.

---

## How to Use

Before saving any file or content, ask:

1. **Will the owner need to access or share this?** → monday.com
2. **Is this runtime/operational state?** → local
3. **Is this a critical rule / owner correction / confirmed stable preference?** → MEMORY.md
4. **Is this a new lesson, event, or observation that may matter later?** → `memory/daily/YYYY-MM-DD.md`
5. **Is it repeated often enough for long-term memory?** → let Dreaming promote it; don't jump straight to MEMORY.md

When in doubt → monday.com for content, local for state, daily note before MEMORY.md for new learnings.

---

## Trigger Phrases
- "save this"
- "document this"
- "document this"
- Before writing any file with research, analysis, or docs
