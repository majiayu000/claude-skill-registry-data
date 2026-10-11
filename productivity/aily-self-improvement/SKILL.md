---
name: aily-self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) An operation or tool fails unexpectedly, (2) User corrects the agent, (3) User requests a capability that doesn't exist, (4) A better approach or knowledge gap is discovered. Also review learnings before major tasks."
---

# Aily Self-Improvement Skill

Log learnings and errors to markdown files for continuous improvement. Important learnings get promoted to workspace memory.

`<WORKSPACE>` = `~/.aily/workspace/` — all paths below are relative to this root.
```
<WORKSPACE>/
├── AGENTS.md              # Multi-agent workflows, delegation patterns
├── SOUL.md                # Behavioral guidelines, personality, principles
├── TOOLS.md               # Tool capabilities, integration gotchas
├── MEMORY.md              # Long-term memory
└── memory/
    └── learnings/         # This skill's log files
        ├── LEARNINGS.md
        ├── ERRORS.md
        └── FEATURE_REQUESTS.md
```


## Quick Reference

| Situation                   | Action                                              |
|-----------------------------|-----------------------------------------------------|
| Operation or tool fails     | Log to `ERRORS.md`                                  |
| User corrects you           | Log to `LEARNINGS.md` with category `correction`    |
| User wants missing feature  | Log to `FEATURE_REQUESTS.md`                        |
| Knowledge was outdated      | Log to `LEARNINGS.md` with category `knowledge_gap` |
| Found better approach       | Log to `LEARNINGS.md` with category `best_practice` |
| Similar to existing entry   | Link with `**See Also**`, consider priority bump    |
| Broadly applicable learning | Promote to `AGENTS.md`, `SOUL.md`, `TOOLS.md`, or `MEMORY.md` |
| Workflow improvements       | Promote to `AGENTS.md`                              |
| Tool gotchas                | Promote to `TOOLS.md`                               |
| Behavioral patterns         | Promote to `SOUL.md`                                |

## Setup

1. Copy the learning templates (paths are relative to this skill's directory):

```bash
cp -r references/learnings/ <WORKSPACE>/memory/
```

2. Append the following to `## Memory` section in `<WORKSPACE>/AGENTS.md` so the agent is always aware of this skill:

```markdown
### Aily Self-Improvement

When you notice these signals, read the `aily-self-improvement` skill for detailed instructions:

- An operation or tool fails unexpectedly
- User corrects the agent
- User requests a capability that doesn't exist
- A better approach or knowledge gap is discovered
```

## Logging Format

### Learning Entry

Append to `LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: pkg_manager_mismatch | auth_config_missing (optional, for recurring-pattern tracking)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### Error Entry

Append to `ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] short_error_label

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed

### Error
````
Actual error message or output
````

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)

---
```

### Feature Request Entry

Append to `FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `ERR` (error), `FEAT` (feature)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250115-001`, `ERR-20250115-A3F`, `FEAT-20250115-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Reference**: commit, PR, link, or note
- **Notes**: Brief description of what was done
```

Other status values:
- `in_progress` - Actively being worked on
- `wont_fix` - Decided not to address (add reason in Resolution notes)
- `promoted` - Elevated to `AGENTS.md`, `SOUL.md`, `TOOLS.md`, or `MEMORY.md`
- `promoted_to_skill` - Extracted as a reusable skill via `skill-creator`

## Promoting to Project Memory

When a learning is broadly applicable (not a one-off fix), promote it to permanent project memory.

### When to Promote

- Learning applies across multiple tasks or contexts
- Knowledge any contributor (human or AI) should know
- Prevents recurring mistakes
- Documents project-specific conventions

### Promotion Targets

| Learning Type         | Promote To  | Example                                |
|-----------------------|-------------|----------------------------------------|
| Behavioral patterns   | `SOUL.md`   | "Be concise, avoid disclaimers"        |
| Workflow improvements | `AGENTS.md` | "Spawn sub-agents for long tasks"      |
| Tool gotchas          | `TOOLS.md`  | "Git push needs auth configured first" |
| Key facts & decisions | `MEMORY.md` | "Weekly report deadline is every Friday" |

### How to Promote

1. **Distill** the learning into a concise rule or fact
2. **Add** to appropriate section in target file
3. **Update** original entry: `**Status**: promoted`, add `**Promoted**: AGENTS.md`

### Promotion Examples

**Learning** (verbose):
> Project uses pnpm workspaces. Attempted `npm install` but failed.
> Lock file is `pnpm-lock.yaml`. Must use `pnpm install`.

**In `AGENTS.md`** (concise):
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" memory/learnings/`
2. **Link entries**: Add `**See Also**: ERR-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring issues often indicate:
   - Missing documentation (→ promote to workspace files)
   - Missing automation (→ add to `AGENTS.md`)
   - Systemic problem (→ flag for deeper review)

## Periodic Review

Review `memory/learnings/` at natural breakpoints:

### When to Review
- Before starting a new major task
- After completing a task
- When working in an area with past learnings
- Weekly during active work

### Quick Status Check
```bash
# Count pending items
grep -h "Status\*\*: pending" memory/learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" memory/learnings/*.md | grep "^## \["
```

### Review Actions
- Resolve fixed items
- Promote applicable learnings
- Link related entries
- Escalate recurring issues

## Detection Triggers

Automatically log when you notice:

**Corrections** (→ learning with `correction` category):
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."

**Feature Requests** (→ feature request):
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."
- "Why can't you..."

**Knowledge Gaps** (→ learning with `knowledge_gap` category):
- User provides information you didn't know
- Documentation you referenced is outdated
- Actual behavior differs from your understanding

**Errors** (→ error entry):
- Operation fails or returns unexpected result
- Exception, stack trace, or error message
- Timeout or connection failure
- Tool produces incorrect output

## Priority Guidelines

| Priority   | When to Use                                                   |
|------------|---------------------------------------------------------------|
| `critical` | Blocks core functionality, data loss risk, security issue     |
| `high`     | Significant impact, affects common workflows, recurring issue |
| `medium`   | Moderate impact, workaround exists                            |
| `low`      | Minor inconvenience, edge case, nice-to-have                  |

## Best Practices

1. **Log immediately** - context is freshest right after the issue
2. **Be specific** - future agents need to understand quickly
3. **Include reproduction steps** - especially for errors
4. **Link related files** - makes fixes easier
5. **Suggest concrete fixes** - not just "investigate"
6. **Use consistent categories** - enables filtering
7. **Promote aggressively** - if in doubt, add to workspace files
8. **Review regularly** - stale learnings lose value

## Skill Extraction

When a learning is valuable enough to become a reusable skill, use `skill-creator` to extract it.

### When to Extract

- Has `See Also` links to 2+ similar issues (recurring)
- Status is `resolved` with working fix (verified)
- Required actual debugging/investigation to discover (non-obvious)
- Not project-specific; useful across workspaces (broadly applicable)
- User says "save this as a skill" (user-flagged)

### How to Extract

Call `skill-creator` with the learning content. Update the original entry:
- Set `**Status**: promoted_to_skill`
- Add `**Skill-Name**: <name of new skill>`
