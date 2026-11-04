---
name: plugin-audit
description: Audit vercel-plugin performance on real-world projects. Extracts tool calls from Claude Code conversation logs, tests hook matching against actual inputs, identifies pattern coverage gaps, and checks plugin cache staleness. Use when asked to audit, test, or investigate plugin skill injection on a real project.
---

# Plugin Audit

Audit how well vercel-plugin skill injection performs on real-world Claude Code sessions.

## Workflow

### 1. Locate conversation logs

Find JSONL conversation logs for a target project:

```bash
ls -lt ~/.claude/projects/-Users-*-<project-name>/*.jsonl
```

The path uses the project's absolute path with slashes replaced by hyphens and a leading hyphen.

### 2. Extract tool calls

Parse the JSONL log to extract all tool_use entries. Each line is a JSON object with `message.content[]` containing `type: "tool_use"` blocks. Extract `name` and `input` fields. Group by tool type (Bash, Read, Write, Edit).

### 3. Test hook matching

Use the exported pipeline functions directly — do NOT shell out to the hook script for each test. Import from the hooks directory:

```js
import { loadSkills, matchSkills } from "./hooks/pretooluse-skill-inject.mjs";
import { createLogger } from "./hooks/logger.mjs";
```

Call `loadSkills()` once, then `matchSkills(toolName, toolInput, compiledSkills)` for each tool call. This is fast and gives exact match results.

### 4. Identify gaps

Compare matched skills against what SHOULD have matched based on the project's technology stack. Common gap categories:

- **Path pattern gaps**: Files that should trigger a skill but don't (e.g., `src/db/schema.ts` not matching `vercel-storage`)
- **Bash pattern gaps**: Commands that should trigger but don't (e.g., missing package manager variants)
- **Dedup masking**: Skills that matched but were deduped before injection
- **Budget/cap drops**: Skills matched but dropped by the 12KB budget or 3-skill ceiling

### 5. Check plugin cache staleness

Compare the installed plugin cache against the dev version:

```bash
# Cache location
~/.claude/plugins/cache/vercel-labs-vercel-plugin/vercel-plugin/<version>/

# Compare skill content
diff <(grep 'pattern' skills/<skill>/SKILL.md) <(grep 'pattern' ~/.claude/plugins/cache/.../skills/<skill>/SKILL.md)
```

Check `~/.claude/plugins/installed_plugins.json` for version and git SHA.

## Report Format

Produce a structured report with:

1. **Session summary**: Project, date, tool call count, model
2. **Match matrix**: Table of tool calls × matched skills (with match type)
3. **Coverage gaps**: Unmatched tool calls that should have matched, with suggested pattern additions
4. **Dedup timeline**: Order of skill injections and what got deduped
5. **Cache status**: Whether installed version matches dev, with specific diffs

## References

- [Log format details](references/log-format.md)
- [Test script for batch matching](scripts/batch-match.mjs)
