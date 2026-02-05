---
name: gh-pr-comments
description: List and resolve GitHub PR review comments. Use when working with PR feedback, addressing review comments, or marking threads resolved.
allowed-tools: Bash, Read
---

# GitHub PR Comments

List unresolved PR review comments and mark them resolved after addressing feedback.

## Setup

Run once in the skill directory:
```bash
cd ~/.claude/skills/gh-pr-comments && bun install
```

## List Comments

```bash
bun run ~/.claude/skills/gh-pr-comments/scripts/list-comments.ts [options]
```

### Options
- `--unresolved` - Only show unresolved comments (uses GraphQL)
- `--no-bots` - Exclude bot comments (Copilot, etc.)
- `--repo owner/name` - Specify repository (auto-detected if omitted)
- `--pr NUMBER` - Specify PR number (auto-detected if omitted)

### Examples

```bash
# List unresolved comments for current branch's PR
bun run ~/.claude/skills/gh-pr-comments/scripts/list-comments.ts --unresolved

# List all human comments
bun run ~/.claude/skills/gh-pr-comments/scripts/list-comments.ts --no-bots

# List unresolved human comments for specific PR
bun run ~/.claude/skills/gh-pr-comments/scripts/list-comments.ts --unresolved --no-bots --pr 123
```

### Output Format
```json
[{
  "thread_id": "PRRT_kwDOxxx",
  "user": "reviewer",
  "body": "Comment text",
  "diff_hunk": "@@ -10,6 +10,8 @@...",
  "line": 42,
  "start_line": 40
}]
```

## Resolve Comment

After addressing feedback, mark the thread resolved:

```bash
bun run ~/.claude/skills/gh-pr-comments/scripts/resolve-comment.ts <thread_id>
```

### Example
```bash
bun run ~/.claude/skills/gh-pr-comments/scripts/resolve-comment.ts PRRT_kwDOLsFqtM5kv0rG
```

### Output
```json
{ "resolved": true }
```

## Workflow

1. List unresolved comments: `bun run ~/.claude/skills/gh-pr-comments/scripts/list-comments.ts --unresolved`
2. Address each comment in the code
3. Resolve each thread: `bun run ~/.claude/skills/gh-pr-comments/scripts/resolve-comment.ts <thread_id>`
