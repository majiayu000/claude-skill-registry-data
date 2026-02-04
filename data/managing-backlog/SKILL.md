---
name: managing-backlog
description: Automatically maintains project BACKLOG.md with deferred features, tech debt, bugs, and improvements. Adds items when work is deferred, marks complete when addressed. Used by other skills to track out-of-scope work.
---

# Managing Backlog

Automatically maintain a living BACKLOG.md document tracking deferred work, tech debt, bugs, and improvements.

**Core principle:** Backlog maintains itself. Users only interact to query status or make manual adjustments.

## When This Skill Activates

**Automatic (no user prompt):**
- Work is deferred during brainstorming
- Tasks identified but out of scope during planning
- Tech debt or improvements noted during code review
- Related bugs found during systematic debugging
- Issues discovered during implementation

**Manual (user request):**
- "Show me the backlog"
- "What's high priority?"
- "Add X to backlog"
- "Mark Y complete"

## BACKLOG.md Structure

**Location:** Project root (`BACKLOG.md`)

**Organization:**
- **Primary:** Priority (High → Medium → Low)
- **Secondary:** Type (Features, Tech Debt, Bugs, Improvements)
- **Completed:** Separate section at bottom with commit SHAs

**Format:**
```markdown
# Project Backlog

## High Priority

### Features
- [ ] Feature description (added: 2026-01-05)

### Tech Debt
- [ ] Refactor X (added: 2026-01-04)

### Bugs
- [ ] Fix Y (added: 2026-01-05)

### Improvements
- [ ] Optimize Z (added: 2026-01-03)

## Medium Priority
[same subsections...]

## Low Priority
[same subsections...]

---

## Completed

### Features
- [x] User profile (completed: 2026-01-03, commit: 3df7661)

### Tech Debt
- [x] Refactor auth (completed: 2026-01-04, commit: b82e439)

### Bugs
- [x] Fix race condition (completed: 2026-01-05, commit: c91a023)

### Improvements
- [x] Optimize queries (completed: 2026-01-02, commit: f4e8a12)
```

## Adding Items to Backlog

### Process

**1. Check for BACKLOG.md**
- If doesn't exist, create from template at `skills/managing-backlog/backlog-template.md`
- Announce: "Creating BACKLOG.md"
- Commit: `chore: initialize project backlog`

**2. Check for duplicates**
- Scan existing items for similar descriptions (>80% text similarity)
- If found, skip and announce: "Similar item already in backlog: {existing}"

**3. Determine priority and type**

Use context to set smart defaults:

| Context | Priority | Type |
|---------|----------|------|
| Bug found during debugging | Medium | Bugs |
| Deferred feature from brainstorming | Low | Features |
| Tech debt from code review (Minor) | Low | Tech Debt |
| Tech debt from code review (Important) | Medium | Tech Debt |
| Performance improvement noted | Low | Improvements |
| Security issue found | High | Bugs |
| Breaking change needed | High | Tech Debt |

**4. Insert item**
- Add to appropriate priority + type section
- Format: `- [ ] {description} (added: YYYY-MM-DD)`
- Preserve existing order (newest first within section)

**5. Announce and commit**
- Announce: "Adding to backlog as [Priority/Type]: {description}"
- Commit message: `chore: add backlog item - {description}`

### Example

```
During code review, you find magic numbers that should be constants.

You: "Adding to backlog as [Low Priority/Tech Debt]: Replace magic numbers with named constants in validation module"

[Updates BACKLOG.md automatically]
[Commits change]
```

### Edge Cases

**Malformed BACKLOG.md:**
- Attempt to preserve content while fixing structure
- Fall back to appending to correct section if can't parse
- Never lose user data
- Announce any structural fixes made

**Git conflicts:**
- If BACKLOG.md has merge conflicts
- Pause automatic updates
- Announce: "BACKLOG.md has merge conflicts. Please resolve before I can update it."

## Completing Items

### Detection Methods

**Explicit reference (preferred):**
- Task description: "Fix backlog item: {description}"
- Commit message: "Addresses backlog: {description}"
- User statement: "This completes the backlog item about X"

**Fuzzy matching (secondary):**
- Compare task/commit description to backlog items
- Strong similarity (>80% match) triggers auto-completion
- Use strongest match if multiple candidates

### Process

**1. Identify matching item**
- Scan all uncompleted items (High, Medium, Low priority sections)
- Find item matching work just completed
- If multiple matches, pick strongest (highest similarity)

**2. Mark complete and move**
- Check the checkbox: `- [ ]` → `- [x]`
- Move to appropriate Completed subsection (by type)
- Add completion info: `(completed: YYYY-MM-DD, commit: SHA)`
- Place at top of Completed subsection (newest first)

**3. Get commit SHA**

For git projects:
```bash
git rev-parse HEAD | cut -c1-7
```

For non-git projects:
- Use timestamp only: `(completed: YYYY-MM-DD)`

**4. Announce and commit**
- Announce: "Marking backlog item complete: {description}"
- Commit message: `chore: mark backlog item complete - {description}`

### Integration Points

Check for completed backlog items:

- **verification-before-completion** - Before declaring work done
- **subagent-driven-development** - After task completion and commit
- **finishing-a-development-branch** - Scan all commits before merge

### Example

```
You just implemented caching for API responses.

Backlog has: "- [ ] Add caching layer to API responses (added: 2026-01-03)"

You: "Marking backlog item complete: Add caching layer to API responses"

[Moves item to Completed section]
Item becomes: "- [x] Add caching layer to API responses (completed: 2026-01-05, commit: a7f3c21)"

[Commits change]
```

## Manual Commands

Users can manually interact with the backlog through these commands:

### Query Commands

**"Show me the backlog"**
- Read BACKLOG.md
- Present current state organized by priority
- Include item counts per section

**"What's high priority?" / "What's medium priority?" / "What's low priority?"**
- Filter and show specific priority section
- Include all types within that priority

**"What bugs are in the backlog?" / "What features..." / "What tech debt..." / "What improvements..."**
- Filter by type across all priorities
- Show priority level for each item

**"What's the backlog status?"**
- Summary of item counts:
  - High: X items (Y features, Z bugs, ...)
  - Medium: X items
  - Low: X items
  - Completed: X items

### Manual Adjustments

**"Add X to backlog as [priority/type]"**
- User specifies priority (High/Medium/Low) and type (Feature/Bug/Tech Debt/Improvement)
- Follow same addition process as automatic
- Announce and commit

**"Remove Y from backlog"**
- Find item matching Y
- Remove from BACKLOG.md
- Announce: "Removed from backlog: {description}"
- Commit: `chore: remove backlog item - {description}`

**"Mark Z complete"**
- Find item matching Z
- Follow completion process
- Move to Completed section with current commit SHA

**"Change X to [priority]"**
- Find item X
- Move to specified priority section (keep same type)
- Announce: "Changed priority: {description} → [New Priority]"
- Commit: `chore: reprioritize backlog item - {description}`

### Example Interactions

```
User: "What's high priority?"

You: "High priority items in backlog:

Features:
- Real-time notifications (added: 2026-01-04)

Bugs:
- Fix session cleanup (added: 2026-01-05)

2 total high priority items."
```

```
User: "Add support for PostgreSQL to backlog as High Priority Feature"

You: "Adding to backlog as [High Priority/Feature]: Support for PostgreSQL"
[Updates BACKLOG.md]
[Commits]
```
