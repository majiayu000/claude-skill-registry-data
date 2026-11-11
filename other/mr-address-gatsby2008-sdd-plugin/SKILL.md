---
name: mr-address
description: Work through open MR review comments with minimal per-thread guidance
allowed-tools: Read, Edit, Write, Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(glab:*), Bash(find .:*), Bash(grep -r:*), Bash(cat .specwork/_review/*), Bash(python3:*), Bash(command -v:*)
---

# Address MR Review

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/mr-address/SKILL.md`

---

## Description

Handle MR review threads one by one and track progress in
`.specwork/_review/<id>-mr-address.md`.

Use `glab` if available; otherwise switch to manual paste mode.
Keep prompts short and only show the current thread.

---

## Flow

1. Detect `glab`, branch, and MR
2. Load unresolved threads or manual comments
3. Skip already-handled items from the progress file
4. Handle threads one at a time
5. Update progress, then offer commit/push

---

## Manual Mode

Ask for one pasted comment at a time. Use `---` to confirm or `done` to stop.
Parse optional `file:` and `line:` hints. Use `manual-N` ids in the progress file.

---

## Thread Actions

Show only:
- author
- file/line if available
- comment text
- `fix / reply / defer / skip / done`

Actions:
- **fix**: make the change, show a minimal diff summary, confirm, resolve
- **reply**: capture the reply text, confirm, post or print it for manual paste
- **defer**: mark pending in the progress file
- **skip**: move on without recording
- **done**: stop the session

Read only the file or lines needed for the current thread.

---

## Progress File

Update `.specwork/_review/<id>-mr-address.md` after each handled thread.

```markdown
# Address MR Review: <id>

MR: !<iid>

## Addressed
- [x] <discussion-id>: @author — fixed
- [x] <discussion-id>: @author — replied

## Deferred
- [ ] <discussion-id>: @author
```

Reuse this file on later runs to skip handled threads.

---

## End of Session

```text
Session complete
  ✓ fixed: 3
  ✓ replied: 1
  ○ deferred: 1
  – skipped: 2
```

If files changed, offer one commit and an optional push.

---

## Requirements

- Run from the branch tied to the MR
- An open MR must exist
- `glab` is optional; manual mode is allowed

---

## Related Skills

- `mr` — creates the MR this skill reads from
- `commit` — commit addressed review changes
- `code-review` — internal review before the MR is open
