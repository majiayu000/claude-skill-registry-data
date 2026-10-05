---
name: memory-system
description: >
  Tiered, low-token project memory protocol for .toh/memory/ — 7 files across
  3 tiers (Tier 1 active.md + summary.md always read, ~800 tokens; Tier 2
  architecture/components for build work and changelog for debug work; Tier 3
  decisions/agents-log only on demand). Auto-saves after task completion with
  zero user effort; delegated agents receive context from the orchestrator
  instead of re-reading. Use at every session start and whenever loading or
  saving project memory or resuming context across sessions and IDEs.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🧠 Memory System Skill

> **Purpose:** Tiered, low-token memory — load only what the task needs, save what matters
> **Version:** 2.0.0
> **For:** Toh Framework v2.0.0+
> **Updated:** 2026-07-14

---

## Overview

Automatic memory that keeps AI in context across sessions with **zero user effort**. v2 replaces the old "read all files every time" mandate with **tiered loading**: Tier 1 is always read (~800 tokens), Tier 2 is read only for the relevant task type, Tier 3 only when explicitly referenced.

### Key principles
- ✅ **Zero config** — no setup required
- ✅ **Tiered** — Tier 1 always; Tier 2/3 on demand (no more ~3,000 tokens every time)
- ✅ **Auto save** — saves after task completion, never asks the user
- ✅ **Delegated agents don't re-read** — they receive context from the orchestrator
- ✅ **IDE & model agnostic**

---

## 📚 The Tiered Model (use this everywhere)

There are **7 memory files** across 3 tiers. Read by tier, not all at once.

| Tier | Files | When to read | Budget |
|------|-------|--------------|--------|
| **Tier 1** | `active.md` + `summary.md` | **ALWAYS**, at every session start | **~800 tokens** |
| **Tier 2** | `architecture.md` + `components.md` | Build / code work (creating pages, components, logic) | ~600 tokens |
| **Tier 2** | `changelog.md` | Debug work (to see previous attempts) | ~400 tokens |
| **Tier 3** | `decisions.md` + `agents-log.md` | Only when explicitly referenced / asked about | on demand |

> **This replaces the old "read ALL files (MANDATORY)" rule.** Never bulk-read all 7. Read Tier 1 always, add the Tier 2 files that match the task type, and touch Tier 3 only when needed.

**Delegated agents:** an agent invoked by the orchestrator **receives context from the orchestrator** and does NOT re-read memory itself. This avoids every agent re-reading the same files.

---

## 📁 Directory Structure

```
.toh/
├── config.json              # Toh configuration
└── memory/
    ├── active.md            # 🔥 Tier 1 — current task (~300 tokens)
    ├── summary.md           # 📋 Tier 1 — project shape (~500 tokens)
    ├── architecture.md      # 🏗️ Tier 2 — structure (build/code work)
    ├── components.md        # 📦 Tier 2 — component registry (build/code work)
    ├── changelog.md         # 📝 Tier 2 — change/attempt log (debug work)
    ├── decisions.md         # 🧠 Tier 3 — key decisions (when referenced)
    ├── agents-log.md        # 🤖 Tier 3 — agent activity (when referenced)
    └── archive/             # 📦 Historical — load only when asked
```

`agents-log.md` stays a **separate** file — it is NOT merged into `changelog.md`.

---

## 🔄 Read Protocol (session start)

```
STEP 1 — Ensure memory exists
        .toh/memory/ exists? → continue · missing? → create from templates

STEP 2 — Read Tier 1 (ALWAYS, in parallel)
        ├── active.md    → what we're working on
        └── summary.md   → what this project is
        Budget: ~800 tokens.

STEP 3 — Add Tier 2 by task type
        ├── Build / code (create page, component, logic)
        │     → also read architecture.md + components.md
        └── Debug (fix a bug)
              → also read changelog.md (see prior attempts)

STEP 4 — Tier 3 only if referenced
        User asks "why did we decide X?"  → read decisions.md
        User asks about past agent runs    → read agents-log.md

STEP 5 — Acknowledge briefly
        "Memory loaded 📚 — working on [X]. Just completed [Y]. Ready to continue."
```

Do **not** read `archive/` during normal work — only when the user asks about past work or runs a history command.

---

## 💾 Save Protocol (after completing work)

```
STEP 1 — active.md            → ALWAYS update (current focus, in-progress, next steps)
STEP 2 — summary.md           → update when the PROJECT SHAPE changes
                                 (feature completed, tech/stack change, new major area)
STEP 3 — architecture.md      → update if structure changed (new route/module/service, data flow)
STEP 4 — components.md         → update if components/hooks/stores/utils changed
STEP 5 — changelog.md         → append what changed / what was attempted (esp. debug work)
STEP 6 — decisions.md         → add row only if a real decision was made
STEP 7 — agents-log.md        → append if agents were delegated
STEP 8 — Confirm: "✅ Memory saved"
```

**Write rules:** always update `active.md`; update `summary.md` when the project shape changes; update the rest **only when relevant** to what actually happened. Keep entries concise (1-2 lines). If `active.md` grows past ~50 lines, roll older content into `archive/YYYY-MM-DD.md`.

---

## 🗂️ File Reference

| File | Tier | Holds | Update when |
|------|------|-------|-------------|
| `active.md` | 1 | Current focus, in-progress, next steps | **Always** |
| `summary.md` | 1 | Project name, stack, completed features | Project shape changes |
| `architecture.md` | 2 | Entry points, modules, data flow, services | Structure changes |
| `components.md` | 2 | Pages, components, hooks, stores, utils registry | Components change |
| `changelog.md` | 2 | Chronological change & debug-attempt log | Every notable change |
| `decisions.md` | 3 | Date · Decision · Reason table | A real decision is made |
| `agents-log.md` | 3 | Which agent did what, when | Agents are delegated |

---

## 📝 Templates

### active.md (Tier 1)
```markdown
# 🔥 Active Task
## Current Focus
[Awaiting user instructions]
## In Progress
- (none)
## Next Steps
- (awaiting)
---
*Last updated: YYYY-MM-DD*
```

### summary.md (Tier 1)
```markdown
# 📋 Project Summary
## Overview
- Name: [Project]
- Stack: Next.js 16, Tailwind, shadcn/ui, Zustand, Supabase
## Completed Features
- (none yet)
---
*Last updated: YYYY-MM-DD*
```

### changelog.md (Tier 2 — debug)
```markdown
# 📝 Changelog
| Date | Change / Attempt | Result |
|------|------------------|--------|
| YYYY-MM-DD | [what changed or was tried] | [worked / failed because …] |
---
*Last updated: YYYY-MM-DD*
```

### agents-log.md (Tier 3)
```markdown
# 🤖 Agents Log
| Date | Agent | Task | Outcome |
|------|-------|------|---------|
| YYYY-MM-DD | [agent] | [task] | [result] |
---
*Last updated: YYYY-MM-DD*
```

> `architecture.md`, `components.md`, and `decisions.md` keep their existing table structures (entry points/modules, component registry, decision log).

---

## ⚠️ Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Bulk-read all 7 files every time | Read Tier 1 always; Tier 2/3 by need |
| Make delegated agents re-read memory | Pass context from the orchestrator |
| Read `archive/` during normal work | Only when the user asks about the past |
| Forget to save | Always update `active.md` after a task |
| Ask the user whether to save | Save automatically |
| Merge `agents-log` into `changelog` | Keep the 7 files distinct |

---

## 🔗 Integration

Every command applies this protocol: read Tier 1 at start, add Tier 2 for the task type, save `active.md` (+ relevant files) at the end. Delegated agents receive context and skip the re-read.

---

*Memory System v2.0.0 — tiered loading, ~800-token Tier 1, 7 files across 3 tiers*
