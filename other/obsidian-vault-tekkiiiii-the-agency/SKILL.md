---
name: obsidian-vault
description: "Long-term memory layer — forwards architectural decisions, project learnings, skill creations, and generated assets to the Obsidian vault, and reads from it before starting work on known projects. Handles eviction from medium-term memory (30-day inactive projects, 7-day old decisions) into the vault. Vault structure: Projects/, Skills/, Learnings/, Files/, Reference/. Always forward decisions immediately when made; link liberally with [[note-name]] syntax. Best for: engineers working across multiple projects who need long-term memory that survives beyond session logs, and anyone who wants Obsidian as the canonical source for architectural rationale and project context. Also for: cross-project pattern recognition, skill provenance tracking, and decision audit trails."
---

# Obsidian Vault — Long-Term Memory & Data Vault

The Obsidian vault is Claude's long-term memory. Anything worth keeping beyond a single
conversation — decisions, learnings, project context, files, and references — goes here.

---

## Vault Structure
```
/Vault/
  /Projects/
    /[project-name]/
      overview.md          ← stack, decisions, current phase
      decisions-log.md     ← all architectural decisions + rationale
      skills-used.md       ← which skills were imported/created for this project
  /Skills/
    index.md               ← mirror of ~/.claude/skills/INDEX.md
    /[skill-name].md       ← human-readable notes on each skill
  /Learnings/
    [YYYY-MM-DD]-[topic].md ← insights, patterns, mistakes worth remembering
  /Files/
    /[project-name]/       ← exported files, reports, generated assets
  /Reference/
    [topic].md             ← reusable reference notes (APIs, tools, services)
```

---

## What to Forward to the Vault

### Always forward:
- **Architectural decisions** — stack choices, API design, repo structure, storage decisions
  and the reasoning behind them
- **Skill creations and updates** — whenever /skill-creator produces a new skill, log it with:
  - Skill name, date, tool (Skill Seekers CLI)
  - Enhancement level (1-5) and mode (api/local)
  - Framework preset used (e.g. claude-code-unified.json)
  - Target platform
  - Trust level (agent-authored, pending review)
  - Provenance: skill-seekers
- **Skill Seekers imports** — when /skill-import pulls from an external URL via Skill Seekers install-agent, log the derived skill name and source URL
- **Project setup** — when a new project starts, create a project overview note
- **Lessons learned** — mistakes caught, patterns that worked, approaches that failed
- **Generated files** — reports, exports, imports that the user may need later
- **Resolved conflicts** — when a skill import conflict was resolved, log what won and why

### Forward when asked:
- Full conversation summaries
- Research findings
- Reference documentation for tools or APIs used

### Never forward:
- Credentials, API keys, secrets, passwords
- Raw database dumps
- Temporary or intermediate files
- Content the user explicitly marks as session-only

---

## How to Write to the Vault

When forwarding content, always:

1. **Check if the note already exists** — update rather than duplicate
2. **Use the correct folder** based on content type (see Vault Structure above)
3. **Use this frontmatter** at the top of every note:
```markdown
---
date: [YYYY-MM-DD]
project: [project-name or "global"]
tags: [relevant, tags]
source: claude-session
---
```

4. **Write in plain language** — notes are for humans to read later, not just Claude
5. **Link related notes** using Obsidian `[[note-name]]` syntax where relevant

---

## How to Read from the Vault

Before starting work on a project Claude has seen before:
- Read `PROJECT.md` in the project root for instant status context
- Read `/Projects/[project-name]/overview.md` in the vault for long-term memory
- Read `/Projects/[project-name]/decisions-log.md` for prior decisions
- Cross-reference `/Skills/index.md` against the project stack

Before creating a new skill:
- Check `/Skills/index.md` to see if a relevant skill already exists

---

## Decisions Log Format

Every architectural or technical decision forwarded to the vault goes in
`/Projects/[project-name]/decisions-log.md` using this format:
```markdown
## [Decision Title]
- **Date:** YYYY-MM-DD
- **Decision:** What was decided
- **Alternatives considered:** What else was on the table
- **Rationale:** Why this option won
- **Impact:** Which files or folders this affects
```

---

## Eviction Bridge (Medium-Term → Vault)

The vault also serves as the destination for medium-term memory eviction. When medium-term content reaches its TTL:

| Content type | Condition | Action |
|---|---|---|
| Active project | No session activity > 30 days | Archive to `/Projects/[name]/overview.md`, remove from medium-term |
| Recent decision | > 7 days old | Forward to vault `/Projects/[name]/decisions-log.md` |
| Session log | > 5 entries | Discard oldest (never forward — too granular) |

**Process**: Before removing stale content from medium-term, always check if it belongs in the vault. Project overviews and architectural decisions go to vault. Session logs and ephemeral notes are discarded.

---

## Key Rules

- **PROJECT.md first** — always read the project's `PROJECT.md` before exploring code or reading vault overview. `PROJECT.md` is the authoritative source for current state.
- **Write immediately** — don't wait until end of session, forward as decisions are made
- **Update don't duplicate** — always check for an existing note before creating a new one
- **Link liberally** — use [[note-name]] to connect related decisions and projects
- **Vault is source of truth for long-term memory** — vault overview and decisions-log capture context that should persist across sessions. `PROJECT.md` is the session-start snapshot.
- **Vault sync on demand** — after updating `PROJECT.md`, sync to vault overview only at end of day or on explicit user request
- **Never store secrets** — credentials and keys never enter the vault under any circumstance

---

## Integration: Understand-Anything → Obsidian Vault

**Combined workflow for code comprehension + persistent vault notes:**

1. Run `/understand <project-path>` to produce `.understand-anything/knowledge-graph.json`
2. Convert to Obsidian notes:
   ```bash
   node ~/.claude/tools/understand-anything/integrations/to-obsidian.mjs \
     <project-path>/.understand-anything/knowledge-graph.json \
     --slug <project-slug>
   ```
3. Notes land in `~/Documents/Obsidian Vault/Codebases/{slug}/`:
   - `index.md` — hub note with project overview and links to sections
   - `architecture.md` — layer structure and high-complexity nodes
   - `modules.md` — files, functions, classes, modules
   - `infrastructure.md` — services, endpoints, config, schema
   - `domains.md` — business domains, flows, process steps (from /understand-domain)
   - `knowledge.md` — articles, entities, topics, claims (from /understand-knowledge)

**Galaxy graph rules respected:**
- Max 12 `[[wikilinks]]` per note (prevents mesh-link explosion in graph view)
- Hub-and-spoke topology: index.md is the hub, section files are spokes
- Each section file links back to `[[{slug}/index]]`

**Dry-run first:**
```bash
node ~/.claude/tools/understand-anything/integrations/to-obsidian.mjs \
  .understand-anything/knowledge-graph.json --slug myproject --dry-run
```

**Glue script:** `~/.claude/tools/understand-anything/integrations/to-obsidian.mjs`
- Input: `knowledge-graph.json` from understand-anything
- Output: Obsidian-formatted markdown notes with frontmatter + wikilinks

See also: `~/.claude/skills/understand/SKILL.md` for the understand-anything base skill.
See also: `~/.claude/memory/obsidian.md` for vault access conventions.