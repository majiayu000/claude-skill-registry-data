---
name: smart-docs-updater
description: |
  Intelligently updates CHANGELOG.md and documentation by tracking work sessions.
  Accumulates multiple related changes into ONE coherent entry instead of fragmented updates.

  Use this when:
  - User says "start working on X" or "fixing Y" (session start)
  - User says "done", "ship it", "finished with X" (session end - trigger docs update)
  - User asks to update changelog after multiple commits

  DO NOT update docs after every small change. Wait for session completion.
---

# Smart Documentation Updater

## Philosophy

**Problem:** Multiple commits for one fix = fragmented changelog entries
**Solution:** Session-based tracking + intelligent summarization

## Session Lifecycle

### 1. Session Start (Implicit or Explicit)

**Explicit start:**
- User says: "I'm going to fix the login bug" or "Starting work on feature X"
- Record the current git HEAD as session baseline

**Implicit start:**
- First code change in a conversation = session start
- Track from that point

**State tracking** (in memory or `.claude/session-state.json`):
```json
{
  "session_id": "2025-12-25-login-fix",
  "started_at": "2025-12-25T12:00:00Z",
  "baseline_commit": "abc1234",
  "work_description": "Fixing login authentication flow",
  "changes_made": []
}
```

### 2. During Session (Accumulate, Don't Update)

As user works:
- Track files modified (from Edit/Write tool calls)
- Track commits made
- Note the problem being solved
- **DO NOT update CHANGELOG.md yet**

If user asks "update the changelog" mid-session:
- Ask: "Are you done with this work session, or still making changes?"
- If still working: "I'll wait until you're done to create one coherent entry"
- If done: Proceed to session end

### 3. Session End (Trigger Documentation Update)

**Trigger phrases:**
- "done", "finished", "ship it", "that's it", "complete"
- "update the docs now", "wrap this up"
- "commit and document this"

**Process:**

#### Step 1: Analyze All Changes Since Baseline
```bash
# Get all commits since session start
git log --oneline ${baseline_commit}..HEAD

# Get consolidated diff
git diff ${baseline_commit}..HEAD --stat

# Get detailed changes
git diff ${baseline_commit}..HEAD --name-status
```

#### Step 2: Intelligently Categorize

Group changes by TYPE (not by commit):

| Category | When to Use |
|----------|-------------|
| **Added** | New features, new files, new capabilities |
| **Fixed** | Bug fixes, error corrections |
| **Changed** | Refactors, behavior changes, updates |
| **Removed** | Deprecated features, deleted code |
| **Security** | Security-related fixes |
| **Performance** | Optimization changes |

#### Step 3: Create ONE Coherent Entry

**Bad (fragmented):**
```markdown
### Fixed
- Fix login button click handler
- Add null check to auth function
- Update error message for login
- Fix edge case in token validation
```

**Good (intelligent summary):**
```markdown
### Fixed
- **Authentication flow**: Resolved login failures caused by null token handling and edge cases in validation. Improved error messaging for failed attempts. (lib/auth/, components/login/)
```

#### Step 4: Update CHANGELOG.md

Insert under `## [Unreleased]` section:

```markdown
## [Unreleased]

### Fixed
- **Authentication flow**: Resolved login failures caused by null token handling
  and edge cases in validation. Improved error messaging.
  ([#issue] if applicable)
```

#### Step 5: Update README.md (If Applicable)

Only update if:
- New user-facing features added
- API changes that affect usage
- New dependencies or requirements
- Installation steps changed

Skip if:
- Internal refactors
- Bug fixes with no API changes
- Performance improvements

### 4. Multi-Problem Sessions

If user works on MULTIPLE unrelated issues in one session:

**Detection:**
- Commits touch completely different areas
- User explicitly mentions multiple issues
- Long time gaps between commit clusters

**Handling:**
- Create SEPARATE changelog entries for each logical unit
- Group by feature/area, not by time

**Example output:**
```markdown
## [Unreleased]

### Fixed
- **Authentication**: Resolved token validation edge cases (lib/auth/)
- **CRM Display**: Fixed company name truncation in sidebar (components/crm/)

### Changed
- **Memory System**: Optimized compression for large conversations (lib/memory/)
```

## Commands Reference

| User Says | Action |
|-----------|--------|
| "I'm fixing X" | Start session, record baseline |
| "Working on feature Y" | Start session, record baseline |
| "Done" / "Ship it" | End session, update docs |
| "Update changelog" | Ask if done, then update |
| "What have I changed?" | Summarize changes since baseline |
| "Nevermind, discard" | Clear session, no docs update |

## Quality Guidelines

### Changelog Entries Should Be:

1. **User-focused**: What impact does this have?
2. **Concise**: One line summary, details optional
3. **Grouped**: Related changes = one entry
4. **Traceable**: Include file paths or issue numbers
5. **Present tense**: "Fix X" not "Fixed X"

### Avoid:

- Entry per commit
- Implementation details users don't care about
- Duplicate entries for the same fix
- Updating docs before work is complete

## Edge Cases

### User Forgets to "End" Session
- If new unrelated work starts, auto-close previous session
- Or ask: "Should I document the previous work before we start this?"

### Work Spans Multiple Days
- Session state persists across conversations
- Use git history as source of truth
- Baseline commit is the key reference point

### Merge Conflicts in CHANGELOG
- Always read current CHANGELOG.md before updating
- Insert new entries at the TOP of [Unreleased]
- Preserve existing entries

## Integration with Sprint System

If project uses sprint tracking (like this one):
- Cross-reference sprint IDs in changelog entries
- Link to sprint docs where applicable

```markdown
### Added
- **Company Brain context optimization** (M50): Token-efficient company
  chats with searchable files. See [sprint docs](docs/sprints/completed/M50/)
```
