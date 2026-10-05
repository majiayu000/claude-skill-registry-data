---
name: git-diff-browser
description: Use when asked to view changes, show a diff, review what changed, compare branches, or see recent commits in a rich browser interface. Supports unstaged changes, staged changes, branch comparisons, commit ranges, and live watch mode with auto-refresh.
---

# Git Diff Browser Viewer

Display rich, syntax-highlighted git diffs in your browser with a collapsible file tree sidebar.

## Overview

This skill generates beautiful, interactive git diffs using diff2html and opens them in your browser. It supports multiple diff modes, live-updating watch mode, and optional AI-generated summaries. The sidebar shows a file tree with change statistics, making it easy to navigate large changesets.

## When to Use

- Reviewing uncommitted changes before committing
- Comparing your branch to main/master
- Viewing what changed in recent commits
- Code review preparation
- Demonstrating changes to team members
- Live-monitoring changes during development (watch mode)

## Quick Reference

| User Request | Command |
|--------------|---------|
| "show diff" / "view changes" | `python3 diff-view.py` |
| "show staged changes" | `python3 diff-view.py --staged` |
| "compare to main" | `python3 diff-view.py --branch main` |
| "show last 3 commits" | `python3 diff-view.py --commit HEAD~3` |
| "live diff" / "watch changes" | `python3 diff-view.py --watch` |
| "watch diff vs main" | `python3 diff-view.py --watch --branch main` |

**Requirements:** `diff2html-cli` (install: `npm i -g diff2html-cli`)

## Implementation

**Note:** The `diff-view.py` script is included in this skill directory. Run it from the skill directory or use the full path to the installed skill.

### Fast Mode (Default - Static Diff)

For instant, one-time diffs, run the all-in-one script directly. No need to read git files or generate JSON manually - the script handles everything.

**Step 1: Determine diff arguments from user request**

| User Says | Script Args |
|-----------|-------------|
| *(empty/no args)* | *(no args)* |
| `staged` | `--staged` |
| `branch <name>` | `--branch <name>` |
| `commit HEAD~N` | `--commit HEAD~N` |
| `commit <sha>` | `--commit <sha>` |

**Step 2: Execute diff script**

```bash
python3 diff-view.py [args]
```

The script will:
1. Generate git diff
2. Convert to HTML via diff2html
3. Enrich sidebar with file tree and stats
4. Open in browser automatically

**Step 3: Optional AI summary**

For static diffs, if you want to add an AI summary:

1. Read the git diff:
   ```bash
   git diff [appropriate args]
   ```

2. Write a concise 2-4 sentence summary explaining the intent

3. Pass to script:
   ```bash
   python3 diff-view.py --summary "Your summary here" [other args]
   ```

The sidebar will show your summary instead of just the mechanical stats.

### Watch Mode (Live-Updating Diff)

When the user requests live/continuous viewing (watch mode), the diff auto-refreshes as files change.

**Step 1: Start watch server in background**

```bash
python3 diff-view.py --watch [args] &
```

The script prints:
```
Serving on http://127.0.0.1:12345 (PID: 67890)
Press Ctrl+C to stop, or it will auto-stop when this session ends.
```

**Step 2: Note the server URL and PID**

The URL (e.g., `http://127.0.0.1:12345`) is where the live diff is served.

**Step 3: Dispatch AI summary subagent (async)**

While the server runs, spawn a subagent to generate the AI summary:

**Subagent prompt:**
```
Generate an AI summary for the current git diff.

1. Read the diff with: git diff [appropriate args based on watch mode]
2. Write a concise 2-4 sentence summary explaining the intent of the changes
3. POST the summary to the watch server:

curl -s -X POST http://127.0.0.1:<port>/api/summary \
  -H 'Content-Type: application/json' \
  -d '{"summary":"Your summary text here"}'

The summary will appear in the browser sidebar without a page reload.
```

**Step 4: Explain watch mode behavior**

Tell the user:
- The page updates in-place via DOM patching (no full reload)
- Scroll position is preserved across updates
- Default refresh interval: 2 seconds
- Server auto-stops when the Claude session exits
- AI summary will appear once the subagent completes

### Diff Modes Explained

**Unstaged changes (default):**
```bash
git diff
```
Shows working tree changes not yet staged.

**Staged changes:**
```bash
git diff --staged
```
Shows changes in the staging area (ready to commit).

**Branch comparison:**
```bash
git diff main...feature
```
Shows changes in `feature` since it diverged from `main`.

**Commit range:**
```bash
git diff HEAD~3..HEAD
```
Shows last 3 commits worth of changes.

**Single commit:**
```bash
git show <commit-sha>
```
Shows changes in a specific commit.

### Sidebar Features

The sidebar displays:
- **File tree** - Collapsible directory structure
- **Change stats** - Additions/deletions per file
- **File status** - Modified (M), Added (A), Deleted (D), Renamed (R)
- **Mechanical summary** - File count and total changes
- **AI summary** - Intent and context (if provided)

**Example sidebar:**
```
Current Branch → Main
━━━━━━━━━━━━━━━━━━━━━━━

Summary
Refactored authentication flow to use JWT tokens instead of
session cookies. Added new middleware for token validation and
updated login/logout handlers.

3 files changed
+187 additions
-93 deletions

├─ src/
│  ├─ auth/
│  │  ├─ middleware.js [M] +125 -45
│  │  └─ tokens.js [A] +42 -0
│  └─ handlers/
│     └─ login.js [M] +20 -48
```

### Watch Mode API

The watch server exposes a JSON API:

**POST /api/summary** - Update AI summary
```bash
curl -X POST http://127.0.0.1:<port>/api/summary \
  -H 'Content-Type: application/json' \
  -d '{"summary":"New summary text"}'
```

**GET /api/update** - Poll for diff changes
```bash
curl http://127.0.0.1:<port>/api/update
```

Returns JSON with current diff hash and HTML if changed.

## Installation

**Install diff2html-cli:**
```bash
npm install -g diff2html-cli
```

**Verify installation:**
```bash
which diff2html
# Should output: /usr/local/bin/diff2html (or similar)
```

## Troubleshooting

**"diff2html: command not found"**
```bash
npm install -g diff2html-cli
```

**Empty diff shown:**
- Check if there are actually changes: `git status`
- For branch comparison, ensure branches exist: `git branch -a`
- For commits, verify reference: `git log`

**Watch mode not updating:**
- Check server is running: Look for process with PID printed at startup
- Verify port is accessible: `curl http://127.0.0.1:<port>`
- Check for file changes: `git status`

**Browser doesn't open:**
- Server still runs, manually visit `http://127.0.0.1:<port>`
- Check `$BROWSER` environment variable
- Try setting: `export BROWSER=open` (macOS) or `export BROWSER=xdg-open` (Linux)

## Platform Notes

This skill works with:
- **Claude Code**: Direct execution via Bash tool, Agent for subagents
- **Gemini CLI**: Use bash/subagent equivalents
- **Codex**: Use RunBash/SubAgent equivalents

**Dependencies:**
- Python 3 (built-in on most systems)
- diff2html-cli (npm install -g diff2html-cli)
- Git (standard)

The `diff-view.py` script is platform-independent (standard Python 3 libraries).

## Related Skills

- **git-commit** - Commit changes after review
- **git-pr** - Create pull request from reviewed changes
- **code-review** - Structured code review process
