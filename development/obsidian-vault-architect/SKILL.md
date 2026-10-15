---
name: obsidian-vault-architect
description: "Design, configure and optimize Obsidian vaults: structure, plugins (Templater, Dataview, Git, Tasks), templates, sync, Claude/MCP integration, LYT/ACE/PARA. Use for \"Obsidian\", \"vault\", \"wikilinks\", \"Dataview\", \"Templater\", \"daily notes\", \"MOC\"."
---

# Obsidian Vault Architect

Expert skill for designing, building, and optimizing Obsidian vaults.

## Core Reference

For detailed specifications, query patterns, and template code:
→ **See [references/obsidian-technical-reference.md](references/obsidian-technical-reference.md)**

## Decision Framework

### Vault Architecture Selection

1. **Single vault** (default): Cross-pollination of ideas, unified search, one sync config
2. **Multiple vaults**: Only when privacy separation required, conflicting plugin configs, or performance issues

### Folder Strategy Selection

| User Context | Recommended Pattern |
|-------------|---------------------|
| Minimal structure preference | Root-based (Steph Ango style) with `/References`, `/Attachments` only |
| Multi-project work | ACE Framework: `/+ (Inbox)`, `/Atlas`, `/Calendar`, `/Efforts`, `/x (Extra)` |
| Developer documentation | Numbered prefixes: `/00 Journals`, `/01 Meetings`, `/02 Projects`, `/03 References` |
| Project-heavy workflow | Top-level `/Projects/` with subfolders per project |

### Organization Tool Selection

- **Folders**: File types, project boundaries, archivable units (one location per note)
- **Tags**: Multi-dimensional categorization, status markers (`#status/active`), filtering
- **Links**: Relationships between ideas, contextual connections
- **Properties**: Structured metadata for queries (dates, status, priority)

**Recommendation**: Folders for types, tags for topics, links for relationships, properties for metadata.

## Plugin Configuration Workflow

### Phase 1: Foundation (Week 1)
Enable core plugins only: Backlinks, Quick Switcher, Daily Notes, Tags View, Outline, Properties, Page Preview.

### Phase 2: Templates (Week 2-4)
1. Install Templater (disable core Templates)
2. Create `/Templates/` folder
3. Configure folder templates in Templater settings
4. Enable "Trigger Templater on new file creation"

### Phase 3: Power Features (Month 2+)
Add only when specific need arises:
- **Dataview**: When dynamic queries needed
- **Tasks**: When managing todos in vault
- **Obsidian Git**: When version control needed
- **Calendar + Periodic Notes**: When weekly/monthly reviews needed

## Template Creation Patterns

### Daily Note (Templater)
```markdown
---
created: <% tp.file.creation_date() %>
tags: [daily-note]
---

# <% moment(tp.file.title,'YYYY-MM-DD').format("dddd, MMMM DD, YYYY") %>

<< [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>]] >>

## Focus
- [ ] <% tp.file.cursor() %>

## Notes
```

### Interactive Templates
Use `tp.system.prompt()` for text input, `tp.system.suggester()` for dropdown selection.

## Sync Strategy Selection

| Priority | Recommended Solution |
|----------|---------------------|
| Cross-platform simplicity | Obsidian Sync ($4-10/mo) |
| Developer with version history | Git (desktop) + Sync/Syncthing (mobile) |
| Privacy-focused, local-only | Syncthing peer-to-peer |

**Critical**: Never mix sync solutions on same vault (causes conflicts/corruption).

## MCP Integration for Claude

Three options for Claude ↔ Obsidian connection:

1. **obsidian-claude-code-mcp** (iansinnott): Native plugin, Claude Code `/ide` auto-discovery
2. **mcp-obsidian** (MarkusPfundstein): Uses Local REST API plugin, broader client support
3. **obsidian-mcp-tools** (jacksteamdev): Semantic search via Smart Connections plugin

## Anti-Pattern Detection

When reviewing a vault, check for:

| Anti-Pattern | Solution |
|--------------|----------|
| Pre-emptive empty folders | Add folders only when notes exist |
| Deep hierarchy (>3 levels) | Flatten; use MOCs and tags instead |
| 20+ plugins installed | Keep ~10 well-understood plugins |
| Dataview queries on startup pages | Move queries to dedicated dashboards |
| Isolated notes (no links) | Every note should link to at least one other |
| Mixing Templates + Templater | Disable core Templates when using Templater |
| No capture habit configured | Set up QuickAdd or mobile inbox |

## Dataview Query Optimization

- Always specify `FROM "folder"` or `FROM #tag` — never scan entire vault
- Limit queries per page in large vaults (1,500+ notes)
- Avoid Dataview on startup/home pages
- Use local images instead of external URLs in tables

## MOC (Map of Content) Guidelines

Create MOCs at the "mental squeeze point" — when 5+ notes on a topic exist and navigation becomes difficult. MOCs emerge from usage, not planned upfront.

```markdown
# Topic MOC

## Core Concepts
- [[Note 1]]
- [[Note 2]]

## Related
- [[Other MOC]]
```
