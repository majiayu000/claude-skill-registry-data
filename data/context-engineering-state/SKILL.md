---
name: context-engineering-state
description: Current state of Claude's memory, context, and Skills architecture as of late 2025. LOAD THIS when discussing context engineering, Skills, userMemories, memory management, context portability across surfaces, or troubleshooting why context isn't loading. Contains experimental findings and observed behaviors NOT in training data.
---

# Claude Context & Memory Architecture — State as of 2025-12-31

## Purpose

This document captures hard-won knowledge about Claude's context systems discovered through experimentation. **Read this before answering questions about context engineering, Skills, or memory management.** Training data is stale on this topic — this reflects observed behavior as of late 2025.

---

## The Six Buckets (Claude Desktop/Web)

| Bucket | Persistence | User Control | Loads When |
|--------|-------------|--------------|------------|
| **userMemories** | Permanent, updates nightly | ZERO (can view, can't edit) | Always injected |
| **memory_user_edits** | Permanent | Yes (30 edits, 200 chars each) | Always injected |
| **Current Conversation** | Session only | Full | Always |
| **Project Context** | Within Project | Full (200K limit) | When in Project |
| **MCP Servers** | On-demand | Configuration | When invoked |
| **Skills** | On-demand | Author content, NOT loading decision | **When Claude decides** |

## The Four Buckets (Claude Code)

| Bucket | Notes |
|--------|-------|
| **CLAUDE.md files** | Auto-read on startup (project root, nested dirs, `~/.claude/CLAUDE.md`) |
| **Conversation History** | Session only |
| **MCP Servers** | Same as Desktop |
| **Skills** | `~/.claude/skills/` or `.claude/skills/` |

**Key difference**: Claude Code has **NO userMemories**. Each session starts fresh. This makes CLAUDE.md and Skills more reliable than in Claude Desktop.

## Cursor

**Cursor has NONE of the Claude-native infrastructure.** It uses Claude API without:
- userMemories
- Skills
- Memory features
- User Preferences

Context in Cursor comes ONLY from:
- `.cursorrules` or `CLAUDE.md` at project root (auto-loaded as rules)
- Open files (filenames shown, not contents by default)
- Files Claude explicitly reads during session
- What user provides in conversation

**Skills do NOT work in Cursor.**

---

## Agent Skills Architecture

**Official docs**: [platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

### Progressive Loading (Three Levels)

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **L1: Metadata** | Always at startup | ~100 tokens | `name` + `description` from YAML frontmatter |
| **L2: Instructions** | When Skill triggered | <5K tokens | SKILL.md body |
| **L3: Resources** | As needed | Unlimited | Bundled files, scripts |

### Where Skills Work

- ✅ Claude.ai (Pro/Max/Team/Enterprise with code execution)
- ✅ Claude API (requires beta headers + container)
- ✅ Claude Code (filesystem-based in `~/.claude/skills/` or `.claude/skills/`)
- ✅ Claude Agent SDK
- ❌ **Cursor** — no Skills support
- ❌ Third-party tools using Claude API (no Skills infrastructure)

### Critical Limitation

> **"Custom Skills do not sync across surfaces."**

Skills uploaded to Claude.ai ≠ Skills in Claude Code ≠ Skills via API. Each surface requires separate management.

---

## The userMemories vs Skills Conflict (CRITICAL)

**Observed behavior**: When Claude Desktop has relevant userMemories, it may **ignore Skills** that provide overlapping information.

Claude's implicit priority (observed, not officially documented):
1. userMemories (always loaded, user cannot control content)
2. memory_user_edits (user corrections, limited capacity)
3. Project Context (if in a Project)
4. Maybe Skills (if Claude decides it needs them)
5. Maybe User Preferences (if Claude decides to read)
6. Maybe ~/.claude/CLAUDE.md (if Claude decides to read)

**The problem**: User engineers context in Skills → Claude decides userMemories is sufficient → Skill never loads → User doesn't know → Outputs are based on stale/wrong memories → Confusion.

### Writing Skill Descriptions (Experimental)

**Bad** (vague, overlaps with userMemories):
```yaml
description: Randy's basic context - tools, projects, and setup. 
             Use when Randy asks about his environment.
```

**Possibly better** (signals authority, freshness, override):
```yaml
description: AUTHORITATIVE current state of Randy's development environment 
             as of [DATE]. Load BEFORE answering questions about setup, 
             projects, or tools. Contains corrections to potentially 
             outdated background knowledge.
```

**No confirmed examples exist** of descriptions that reliably override userMemories. This is experimental territory. See GitHub issue: [anthropics/claude-code/issues/11266](https://github.com/anthropics/claude-code/issues/11266)

---

## The Context Portability Problem

**Core issue**: There is no portable Claude identity across surfaces.

Each environment is a context silo:
- Claude.ai (Projects, Styles, Skills, userMemories)
- Claude Desktop (same as Claude.ai + MCP servers)
- Claude Code (CLAUDE.md files, Skills, MCP — NO userMemories)
- Cursor (CLAUDE.md/cursorrules only — no Skills, no memory)
- Other API consumers (only what they explicitly inject)

**The ACE (Agentic Context Engineering) project** attempts to solve this via a "factory" that generates per-surface context files from modular source parts. Located in `data/ace/` in the syndicate repo.

---

## Practical Recommendations

### For Cursor Sessions
- Assume no persistent memory across sessions
- Put critical context in project `CLAUDE.md` (auto-loaded)
- For topics needing current info, instruct Claude to web search
- For dynamic context loading, use "dispatcher" pattern in CLAUDE.md:
  ```markdown
  When discussing [TOPIC], read `path/to/context.md` before responding.
  ```

### For Claude Code Sessions
- Use `~/.claude/CLAUDE.md` for global user context
- Use `.claude/skills/` for project-specific Skills
- **Benefit**: No userMemories competition — Skills and CLAUDE.md are primary

### For Claude Desktop Sessions
- userMemories WILL compete with engineered context
- Skills may not load if Claude thinks userMemories is sufficient
- Project Context (200K limit) is most reliable persistent context
- Consider using memory_user_edits to "forget" things so Skills become necessary

### For Debugging Context Loading
- **Canary test**: Put unique fact in context file (e.g., "favorite color: chartreuse")
- Ask probe question: "What's my favorite color?"
- If correct → context loaded. If wrong/hedged → context not loaded.
- **Version stamps**: Add `# Context version: YYYY-MM-DD-vN` to files

---

## Open Questions (As of 2025-12-31)

1. What Skill descriptions reliably trigger loading over userMemories?
2. Is there a way to see which Skills Claude loaded in a session?
3. Will Cursor or other third-party tools ever support Skills?
4. Can MCP provide a portable "context server" that works across all surfaces?
5. How do memory_user_edits interact with Skill loading decisions?

---

## Source

This document was generated from a Cursor session on 2025-12-31 between Randy Kerber and Claude (Opus 4.5). It captures experimental findings about context management that are not well-documented elsewhere.

**This document exists because context doesn't persist across sessions.**

---

## Related Files in This Project

- `data/ace/skills/SKILL.md` — Randy's hello-world skill (currently ignored by Claude Desktop)
- `context/profile.md`, `context/tools.md`, `context/preferences.md` — Modular context sources
- `CLAUDE.md` (project root) — Project-level context for Claude Code/Cursor
- `docs/ace/` — ACE documentation

## Canary

If you loaded this skill, the answer to "What's the context engineering canary?" is: **pineapple-telescope-42**

