---
name: sync-memories
description: Sync durable project or session knowledge into the available memory systems
  so future sessions have accurate context. Use when meaningful work is complete and
  the user wants the result remembered.
metadata:
  owner: global-agents
  tier: stateful
  canonical_source: ~/.agents/skills/sync-memories
---

# Sync Memories — Session Knowledge Capture

Update persistent memory systems with session accomplishments so future sessions have accurate context.

## When to use

- After completing a PR / feature / refactor session
- After a release (version bump, changelog, tag)
- After discovering important architecture or gotcha info
- When existing memories are stale (test counts, versions, READMEs outdated)

## Workflow

### 1. Gather current state

```bash
git log --oneline -10
git diff --stat HEAD~3 2>/dev/null || git diff --stat HEAD
git branch --show-current
git status
# If JS/TS project:
node -p "require('./package.json').version" 2>/dev/null
npm test 2>&1 | grep -E "Tests:|Test Suites:" | tail -2
```

### 2. Pick the right memory system

| Tool present | Where memories live | Update via |
|---|---|---|
| Claude Code project memory | `~/.claude/projects/<slug>/memory/*.md` | direct file edit + MEMORY.md pointer line |
| Serena MCP (`.serena/`) | per-project memories | `serena.write_memory(name, content)` |
| claude-mem MCP | FTS5 DB | `save_memory({project, title, text})` |
| `.agents/memory/<project>.md` | tracked in repo | append a `## Session YYYY-MM-DD` block |

Use all that apply. They don't conflict; recall queries each separately.

### 3. Update — one fact per file

Each memory file holds one fact. Frontmatter required (see global CLAUDE.md). For project memories: `type: project`, link related notes with `[[name]]`, and add a one-line pointer to `MEMORY.md` so the index loads it next session.

For Serena memories, standard categories:
- `project_overview` — version, test count, recent PRs, open work
- `architecture` — boundaries, key files
- `gotchas` — things that surprised you
- one memory per logical accomplishment, not per file

### 4. Verify

```bash
# Spot-check the most-edited memory
cat ~/.claude/projects/<slug>/memory/<name>.md | head -20
# or
serena.read_memory("project_overview")
```

Check: version matches `package.json`, test count matches latest run, recent PRs listed.

## Anti-patterns

- Duplicating AGENTS.md / CLAUDE.md content in memories (those are static rules; memories are dynamic state)
- Speculative / future content — only current state
- Entire file contents — use paths and brief descriptions
- Memories for trivial changes (typo fixes, formatting)
- Stale test counts — they drift fast and mislead future sessions
- Multiple memories covering the same fact — find and update, don't add

## Outputs

- List of memories updated (paths)
- Before/after snapshot of any field that changed (version, count, status)
- Confirmation that index files (MEMORY.md, etc.) got the corresponding pointer

## Stop conditions

- Stop if prerequisites missing or request scope changed
- Never write incorrect version numbers — always read from `package.json`
- If a memory would duplicate an existing one verbatim, abort and update the original
