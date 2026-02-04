---
name: brain-dump-assistant
source: brain-dump
description: Manage a personal knowledge capture system. Use when the user wants to capture ideas, track todos, organize projects, review their brain dump, or mentions "brain dump", "capture this", "add to my list", "what's on my plate", "what should I focus on", or "daily review".
---

# Brain Dump Assistant

A CLI for externalizing your working memory - capture ideas, projects, features, todos, and questions without the overhead of complex tools.

## Why?

Your brain is for having ideas, not holding them. But sticky notes get lost, notepads pile up unread, and tools like Asana are overkill for personal capture.

**brain-dump** solves this by providing:
- **Zero-friction capture** - dump thoughts in seconds
- **Structured retrieval** - find anything with search and filters
- **AI-assisted triage** - agents help you organize, prioritize, and act

## Agent Mindset

When assisting users with their brain dump:

1. **Capture first, organize later** - Never block on classification during fast capture. Get the thought out, refine later.

2. **Proactive triage** - Regularly surface raw entries needing processing. Don't let the inbox grow stale.

3. **Connect the dots** - Link related entries, identify patterns, consolidate ideas into projects.

4. **Reduce cognitive load** - Present summaries and prioritized lists, not exhaustive dumps.

5. **Preserve context** - Include enough detail for future recall. A cryptic note is useless later.

6. **Respect simplicity** - Simple thoughts don't need tags, priorities, and parents. Don't over-engineer.

## Operating Modes

Detect user intent and respond appropriately:

| Mode | Triggers | Behavior |
|------|----------|----------|
| **Capture** | "Add this...", "Remind me...", "I had an idea..." | Fast capture, minimal questions, default to idea type |
| **Review** | "What's on my plate?", "Daily review", "Show me..." | Stats + prioritized summary, grouped by type |
| **Triage** | "Process my brain dump", "What needs attention?" | Surface raw entries, help classify and prioritize |
| **Focus** | "What should I work on?", "Priority items" | P1 todos + active projects, clear next actions |
| **Cleanup** | "Archive completed", "Clean up old stuff" | Bulk operations with preview and confirmation |

## Quick Start

| Task | Command |
|------|---------|
| Capture idea | `brain add "your thought here"` |
| Add todo | `brain todo "task description"` |
| Add question | `brain question "what you're wondering"` |
| List active | `brain list` |
| See all | `brain list --all` |
| Search | `brain search "keyword"` |
| Show details | `brain show <id>` |
| Mark done | `brain done <id>` |
| Get stats | `brain stats` |

## Pre-flight Check

Before operations, verify the tool is ready:

```bash
brain --version   # Verify installed
brain stats       # Quick health check
```

If `brain: command not found`, the user needs to install: `npm install -g brain-dump`

## Command Reference

### Capture Commands

#### `brain add <content>`
Quick capture of a thought.

```bash
brain add "What if we used a graph database?"
brain add "Need to review the API design" --type todo --priority 1
brain add "Meeting notes from standup" --type note --tags "meetings,weekly"
brain add --type project --title "Website Redesign" "Complete overhaul of the marketing site..."
```

**Options**:
- `--type <type>`: idea, project, feature, todo, question, reference, note (default: idea)
- `--title <title>`: Short title (auto-extracted from first line if not provided)
- `--priority <1|2|3>`: 1=high, 2=medium, 3=low
- `--tags <tags>`: Comma-separated tags
- `--parent <id>`: Parent entry ID
- `--json`: JSON output

#### `brain todo <content>`
Shorthand for adding a todo.

```bash
brain todo "Review PR #42"
# Equivalent to: brain add "Review PR #42" --type todo
```

#### `brain question <content>`
Shorthand for adding a question.

```bash
brain question "Should we migrate to TypeScript?"
# Equivalent to: brain add "..." --type question
```

### Query Commands

#### `brain list`
List entries with filtering.

```bash
brain list                              # Active + raw (default)
brain list --all                        # All except archived
brain list --type todo                  # Only todos
brain list --status raw                 # Needs triage
brain list --priority 1                 # High priority only
brain list --tags work,urgent           # Has ALL specified tags
brain list --since 7d                   # Created in last 7 days
brain list --json                       # JSON output for parsing
```

**Options**:
- `--type <type>`: Filter by entry type
- `--status <status>`: raw, active, someday, done, archived (default: raw,active)
- `--tags <tags>`: Comma-separated, AND logic
- `--priority <1|2|3>`: Filter by priority
- `--parent <id>`: Children of specific entry
- `--orphans`: Only entries without parent
- `--since <duration>`: e.g., 7d, 24h, 2w
- `--all`: All statuses except archived
- `--done`: Include done entries
- `--archived`: Show only archived
- `--limit <n>`: Max entries (default: 50)
- `--sort <field>`: created, updated, priority
- `--reverse`: Reverse sort order
- `--json`: JSON output

#### `brain show <id>`
Show full entry details.

```bash
brain show a1b2c3d4
brain show a1b2c3d4 --with-children
brain show a1b2c3d4 --with-related
brain show a1b2c3d4 --json
```

#### `brain search <query>`
Full-text search across content and titles.

```bash
brain search "database"
brain search "meeting" --type note --since 30d
brain search "API" --json
```

### Modify Commands

#### `brain edit <id>`
Edit entry content.

```bash
brain edit a1b2c3d4                          # Opens $EDITOR
brain edit a1b2c3d4 --content "New text"     # Non-interactive
brain edit a1b2c3d4 --append "Follow-up"     # Add to existing
brain edit a1b2c3d4 --title "New title"
```

#### `brain set <id>`
Update entry metadata.

```bash
brain set a1b2c3d4 --type project
brain set a1b2c3d4 --status active
brain set a1b2c3d4 --priority 1
brain set a1b2c3d4 --tags "work,Q1"
brain set a1b2c3d4 --add-tags "important"
brain set a1b2c3d4 --remove-tags "draft"
brain set a1b2c3d4 --clear-priority
brain set a1b2c3d4 --parent b2c3d4e5
```

#### `brain link <id1> <id2>`
Create relationships between entries.

```bash
brain link a1b2c3d4 b2c3d4e5                # Add to related
brain link a1b2c3d4 b2c3d4e5 --as-parent    # Set hierarchy
brain link a1b2c3d4 b2c3d4e5 --unlink       # Remove relationship
```

### Bulk Commands

#### `brain done <ids...>`
Mark entries as done.

```bash
brain done a1b2c3d4
brain done a1b2c3d4 b2c3d4e5 c3d4e5f6       # Multiple
brain done --type todo --tags "sprint-1"     # By filter
brain done --dry-run --type todo             # Preview first
```

#### `brain archive <ids...>`
Archive entries (hides from default view).

```bash
brain archive a1b2c3d4
brain archive --status done --since 30d      # Old completed items
brain archive --dry-run --status done        # Preview
```

#### `brain delete <ids...>`
Delete entries (logged for undo).

```bash
brain delete a1b2c3d4
brain delete a1b2c3d4 b2c3d4e5 --confirm
brain delete --status archived --since 90d   # Permanent cleanup
brain delete --dry-run --type reference      # Preview
```

**Safety**:
- All deletions logged to enable restore
- >10 entries requires `--confirm` or `--force`
- Entries with children require `--force`

#### `brain restore`
Restore deleted entries.

```bash
brain restore --last 1                       # Most recent
brain restore --last 5                       # Last 5
brain restore --ids a1b2c3d4,b2c3d4e5        # Specific IDs
brain restore --list                         # Show deletion log
```

### Maintenance Commands

#### `brain stats`
Overview statistics.

```bash
brain stats
brain stats --json
```

#### `brain export`
Export entries.

```bash
brain export                                 # All to stdout
brain export --file backup.json              # To file
brain export --type todo --status active     # Filtered
```

#### `brain import <file>`
Import entries.

```bash
brain import backup.json
brain import backup.json --dry-run
brain import backup.json --merge             # Update existing + add new
brain import backup.json --skip-existing     # Only add new
```

## Workflow Patterns

### Daily Review

Run this each morning to get oriented:

1. **Health check**: `brain stats`
2. **Triage raw entries**: `brain list --status raw`
3. **Focus list**: `brain list --priority 1 --type todo`
4. **Help user decide** what to work on first

### Weekly Review

Run this weekly to maintain hygiene:

1. **Celebrate**: `brain list --done --since 7d` - show what was accomplished
2. **Check stalled**: `brain list --status active --sort updated` - find items not touched
3. **Review projects**: `brain list --type project` - are they progressing?
4. **Clean up**: `brain archive --status done --since 7d` - archive completed items

### Triage Workflow

When user has many raw entries:

1. **Fetch**: `brain list --status raw --json`
2. **For each entry**, determine:
   - Type (idea, todo, project, question, reference, note)
   - Priority (1, 2, 3, or none)
   - Tags (infer from content)
   - Parent (if belongs to existing project/feature)
3. **Update**: `brain set <id> --type todo --priority 1 --tags "work"`
4. **If entry is actually multiple items**, split and re-capture
5. **Mark refined**: `brain set <id> --status active`

### Capture Mode

When user is dumping thoughts rapidly:

1. Just capture with `brain add "..."` - don't interrupt for classification
2. Use default type (idea) and status (raw)
3. After the brain dump session, offer to triage

## Classification Rules

### Type Detection Heuristics

| Indicator | Likely Type |
|-----------|-------------|
| Starts with action verb ("Build", "Write", "Fix", "Review") | `todo` |
| Contains "?" or seeking information | `question` |
| Multi-step initiative, long-term scope | `project` |
| Specific capability/enhancement within a project | `feature` |
| Link, quote, or factual information | `reference` |
| Observation with no clear action | `note` |
| Speculative, "what if", creative | `idea` |

### Priority Assignment

| Priority | Criteria |
|----------|----------|
| P1 (high) | Blocking other work, deadline within 48h, explicitly urgent |
| P2 (medium) | Important but not urgent, this-week scope |
| P3 (low) | Nice-to-have, someday-maybe, learning/exploration |
| None | Truly unprioritized, needs triage |

## Safety Rules

**Non-negotiable constraints**:

1. **Never auto-delete** - Always show what will be deleted and confirm
2. **Preserve context** - Don't summarize away important details during capture
3. **Log before delete** - All deletions are recoverable via `brain restore`
4. **Confirm bulk operations** - Operations affecting >10 entries require confirmation
5. **Don't over-organize** - Simple thoughts don't need tags, priorities, and parents

## Two-Step Pattern for Bulk Operations

Critical for preventing accidental mass changes:

1. **Preview**: `brain delete --status archived --since 90d --dry-run`
2. **Confirm**: Show user what will be affected, get explicit approval
3. **Execute**: `brain delete --ids "<specific-ids>" --confirm`

**Principle**: Filters are for DISCOVERY, IDs are for EXECUTION.

## Common Request Patterns

| User Says | Interpretation | Action |
|-----------|----------------|--------|
| "Add this to my brain dump" | Fast capture | `brain add "<content>"` |
| "I need to remember to..." | Todo item | `brain todo "<content>"` |
| "What's on my plate?" | Need overview | `brain stats` + `brain list --priority 1` |
| "What should I focus on?" | Need priorities | `brain list --priority 1 --type todo` |
| "Process my brain dump" | Triage needed | Run triage workflow on raw entries |
| "This is done" / "I finished X" | Mark complete | `brain done <id>` |
| "Archive old stuff" | Cleanup | `brain archive --status done --since 30d` |
| "What did I do this week?" | Review completions | `brain list --done --since 7d` |
| "Find anything about X" | Search | `brain search "X"` |
| "Link these together" | Create relationship | `brain link <id1> <id2>` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `brain: command not found` | Run `npm install -g brain-dump` |
| Empty brain dump | Start with `brain add "My first thought"` |
| Too many raw entries | Run triage workflow |
| Can't find entry | Use `brain search "<keyword>"` |
| Accidentally deleted | Use `brain restore --last 1` |
| Wrong type/status | Use `brain set <id> --type <type> --status <status>` |

## Testing / Evaluation Scenarios

| Scenario | Expected Behavior | Failure Indicator |
|----------|-------------------|-------------------|
| User says "capture this" | Immediate `brain add`, no questions | Asking for type/priority during fast capture |
| User says "what's on my plate" | Stats + prioritized summary | Listing all 50 entries individually |
| User says "clean up" | Preview + confirmation | Auto-archiving without preview |
| Large deletion (>10 items) | Show count, ask confirmation | Proceeding without confirmation |
| User mentions deadline | Suggest P1 priority | Not detecting urgency |
| User's idea relates to existing project | Suggest linking | Not checking for related entries |

## JSON Output Schemas

### Entry Object

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "content": "The full text of the entry",
  "title": "Short title (optional)",
  "type": "idea|project|feature|todo|question|reference|note",
  "status": "raw|active|someday|done|archived",
  "priority": 1|2|3|null,
  "tags": ["tag1", "tag2"],
  "parent": "parent-id|null",
  "related": ["id1", "id2"],
  "createdAt": "2026-01-05T08:30:00.000Z",
  "updatedAt": "2026-01-05T08:30:00.000Z",
  "source": "cli|agent|import"
}
```

### List Response

```json
{
  "success": true,
  "entries": [...],
  "total": 47,
  "returned": 12,
  "query": {
    "status": ["raw", "active"],
    "limit": 50
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Entry not found: a1b2c3d4",
  "code": "ENTRY_NOT_FOUND"
}
```

## Remember

- The goal is to **externalize working memory**, not build a perfect system
- Capture is king - never block a brain dump
- Structure serves retrieval, not organizational perfection
- The best system is one that gets used
