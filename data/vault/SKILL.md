---
name: Vault
description: Read and write notes in the Obsidian vault. Use for task logs, knowledge capture, and building context.
---

# Vault (Obsidian Notes)

Location: `~/Documents/Notes/`

## Principles

1. **Obsidian vault for documents** - Detailed notes, task logs, project context
2. **Unix tools for fast search** - ripgrep (rg), fd, or mdfind for finding content efficiently
3. **WikiLinks for connections** - Build traversable knowledge graph
4. **ALWAYS**: New tasks should be in an `open` state

## Templates

Templates are in the skill directory, not the notes directory:

- `.claude/skills/vault/templates/knowledge-note.md` - For knowledge notes
- `.claude/skills/vault/templates/task.md` - For new tasks

## Bash Commands

```bash
# List in-progress tasks
rg --type md -l "^status:\s*in-progress" ~/Documents/Notes/Projects/*/Tasks

# Find project directory (handles YYYY[-MM] prefix)
fd -t d -d 1 -i "<project>" ~/Documents/Notes/Projects

# List project task files
fd -e md . ~/Documents/Notes/Projects/*<project>*/Tasks

# Find files by name
fd -e md -i "<name>" ~/Documents/Notes

# Recently modified (last 7 days)
fd -e md --changed-within 7d ~/Documents/Notes

# Find with Spotlight index
mdfind -interpret -onlyin ~/Documents/Notes "<concept>"
```

## Timestamps

Always use real timestamps, never placeholders:

```bash
# For task filename: YYYY-MM-DD HHMMSS
date +"%Y-%m-%d %H%M%S"

# For log entry header: YYYY-MM-DD HH:MM
date +"%Y-%m-%d %H:%M"

# For frontmatter (ISO-8601)
date -Iseconds
```

## Task File Path

`~/Documents/Notes/Projects/<YYYY[-MM] Project>/Tasks/<YYYY-MM-DD HHMMSS> <Title>.md`

## Linking Strategy

> Link if it improves the note, not just because it matches a term.

### What to search for

| Search for | Example (if writing about "Unison abilities") |
|------------|-----------------------------------------------|
| Direct terms | "abilities", "Unison abilities" |
| Parent concepts | "effect handlers", "functional programming" |
| Sibling techniques | "monads", "algebraic effects" |
| Tools/tech used | "UCM", "Jit" |

### Linking workflow

1. **Semantic discovery** — `mdfind -interpret` for related concepts
2. **Backlinks** — `rg "\[\[<concept>"` to find what links to your topics
3. **Tags overlap** — `rg "^  - <tag>$"` for notes sharing tags
4. Add discovered notes as WikiLinks using breadcrumb pattern: `[[Parent]] | [[Related]]`

## Capture Heuristics

**Worth capturing when:**

| Marker | Trigger |
|--------|---------|
| 📋 | Principle applies across multiple contexts |
| 🤔 | Caused debugging time or surprised me |
| ⚙️ | Method that could save time later |
| 📎 | Link to documentation or source |
| ☝️ | Non-obvious choice with reasoning worth preserving |

**Where to capture:**

| Destination | When |
|-------------|------|
| **Existing note** | Discovery extends/refines an existing topic (search firs ) |
| **New note** | Substantial, standalone, referenceable by other notes |
| **Task log only** | One-off detail that won't generalise |

## Note Locations

| Folder | Purpose | Examples |
|--------|---------|----------|
| `Development/` | Conceptual, non-project, topics, paradigms, architectural patterns | "Functional Programming", "Test Driven Development", "Unison Web Application Patterns" |
| `HowTo/` | Procedural guides, specific techniques, step-by-step instructions, unrelated to projects | "Unison Testing with Effect Handlers", "TDD with Functional Programming" |
| `Tools/` | Software tools and their usage | "Claude", "Git", "HTMX", "Obsidian" |
| `Projects/<project>/` | Project level knowledge  in an appropriate note in the project folder | |
| `Projects/<project>/Tasks/` | Task logs only — never knowledge notes | |
| `Projects/<project>/Glossary` | Glossary entries | |


## What NOT to include

- **DO NOT** include changed files
