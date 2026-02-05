---
name: wiki
description: Access and manage the local GitHub Wiki clone. Use this skill when you need to read wiki content (architecture, design docs, guides), update wiki documentation, check wiki status, or push wiki changes. The wiki contains high-level system design and architectural documentation.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion
---

# Wiki Management Skill

Manage a local clone of the GitHub Wiki at `docs/wiki/`. Humans read wiki online; AI tools read/write locally.

## When to Use This Skill

- User asks about architecture, system design, or high-level documentation
- User asks to read, update, or check wiki content
- User asks to push wiki changes
- You need architectural context not found in code

## Wiki Repository

| Property | Value |
|----------|-------|
| Local path | `docs/wiki/` (gitignored) |
| URLs | Derived from `git remote` (portable) |

## Deriving Wiki URLs

GitHub wikis follow a convention: `repo.wiki.git`. Derive URLs from the main repo:

```bash
# Get main repo remote URL
REPO_URL=$(git remote get-url origin 2>/dev/null)

# Derive wiki clone URL (works for both SSH and HTTPS)
WIKI_URL="${REPO_URL%.git}.wiki.git"

# Derive online wiki URL for fallback messages
ONLINE_URL=$(echo "$REPO_URL" | sed -E 's|git@github.com:|https://github.com/|; s|\.git$|/wiki|')
```

## Before Any Wiki Operation

1. **Check if wiki clone exists:**
   ```bash
   test -d docs/wiki/.git && echo "exists" || echo "missing"
   ```

2. **If missing, clone it:**
   ```bash
   REPO_URL=$(git remote get-url origin)
   WIKI_URL="${REPO_URL%.git}.wiki.git"
   git clone "$WIKI_URL" docs/wiki
   ```

3. **If clone fails:** Derive and provide the online wiki URL as fallback.

## Reading Wiki Content

1. **Auto-pull for freshness** (silently):
   ```bash
   git -C docs/wiki pull --quiet 2>/dev/null || true
   ```

2. **Read the requested file** from `docs/wiki/`

3. **If file not found**, list available pages:
   ```bash
   ls docs/wiki/*.md 2>/dev/null | xargs -n1 basename
   ```

## Wiki Status

Show the current state of the local wiki:

```bash
# Uncommitted changes
git -C docs/wiki status --porcelain

# Last commit
git -C docs/wiki log -1 --format="%h %s (%cr by %an)"

# Unpushed commits (fetch first)
git -C docs/wiki fetch origin 2>/dev/null
git -C docs/wiki log origin/master..HEAD --oneline

# Unpulled commits
git -C docs/wiki log HEAD..origin/master --oneline

# Available pages
ls docs/wiki/*.md 2>/dev/null | xargs -n1 basename
```

**Warn if unpushed changes exist.**

## Updating Wiki Content

1. **Pull first** to ensure working with latest
2. **Make the edits** as requested
3. **Commit with standard message:**
   ```bash
   git -C docs/wiki add -A
   git -C docs/wiki commit -m "Description of changes

   Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```
4. **Remind user:** Changes are local until pushed
5. **Never auto-push** - always require explicit request

## Pushing Wiki Changes

**CRITICAL: Requires explicit user approval. Wiki pushes go live immediately (no PR review).**

1. **Check for uncommitted changes:**
   ```bash
   git -C docs/wiki status --porcelain
   ```
   If changes exist, commit them first (or ask user for commit message).

2. **Check for unpushed commits:**
   ```bash
   git -C docs/wiki log origin/master..HEAD --oneline
   ```
   If none: "Nothing to push. Wiki is in sync with remote."

3. **Pull first** to avoid conflicts:
   ```bash
   git -C docs/wiki pull origin master
   ```

4. **Show diff preview:**
   ```bash
   git -C docs/wiki diff origin/master..HEAD
   ```

5. **Use AskUserQuestion for approval:**
   Present the diff and ask: "These changes will be pushed to the wiki and GO LIVE IMMEDIATELY. Proceed?"
   - Option 1: "Yes, push these changes"
   - Option 2: "No, cancel"

6. **If approved, push:**
   ```bash
   git -C docs/wiki push origin master
   ```

7. **Confirm success** with online wiki URL.

## Error Handling

| Scenario | Action |
|----------|--------|
| Clone fails (auth) | Provide online wiki URL as fallback |
| Push fails (auth) | Preserve local changes, show error, suggest fixes |
| Pull conflicts | Show conflicting files, ask user how to resolve |
| No wiki exists | Inform user, provide instructions to create one |

## Important Rules

- **Never auto-push** - wiki pushes go live immediately
- **Always pull before push** - prevents lost updates
- **Preserve local changes on failure** - user work should never be lost
- **Default to read-only** if auth fails - better than nothing
