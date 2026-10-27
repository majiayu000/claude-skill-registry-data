---
name: health
description: Verify Claude configuration health — CLAUDE.md, settings.json, hooks, agents, skills, secrets scan, and MCP reachability. Reports ✅/⚠️/❌ for each check.
---

# Health Skill — Claude Brain Configuration Validation

Verify that the Claude Brain configuration is healthy and complete.

## Steps

### 1. CLAUDE.md
- Exists and is not empty
- Line count: `wc -l < CLAUDE.md`
- Size: `wc -c < CLAUDE.md` (budget: ≤32KB = 32768 bytes)
- Contains key sections: Skills Roster, Exit Checklist, Terminal Rules

### 2. settings.json
- `.claude/settings.json` exists and is valid JSON: `jq . .claude/settings.json`
- Contains `hooks` configuration block

### 3. Hook Scripts
- All `.claude/hooks/*.sh` files exist and are executable:
  ```bash
  for h in .claude/hooks/*.sh; do test -x "$h" || echo "NOT_EXEC: $h"; done
  ```

### 4. Subagents
- All `.claude/agents/*.md` files exist and are non-empty:
  ```bash
  for f in .claude/agents/*.md; do [ -s "$f" ] || echo "EMPTY: $f"; done
  ```

### 5. Skills
- All `.claude/skills/*/SKILL.md` files exist
- Each has `name:` and `description:` in frontmatter:
  ```bash
  for f in .claude/skills/*/SKILL.md; do grep -q '^name:' "$f" || echo "BAD FRONTMATTER: $f"; done
  ```

### 6. Error Log
- `claude/tasks/CLAUDE_ERRORS.md` exists (warn if missing)

### 7. Secrets Scan
```bash
git ls-files | xargs grep -l 'BEGIN.*PRIVATE KEY\|password\s*=\s*[^{][^"\x27]\{8,\}' 2>/dev/null | head -10
```
Report any matches as ⚠️ warnings.

### 8. MCP Tool Reachability
Check that the required runtimes are available (all MCP tools run via `uvx` or `npx`):
```bash
command -v uvx &>/dev/null && echo "uvx: ✅" || echo "uvx: ❌ missing — install via: pip install uv"
command -v npx &>/dev/null && echo "npx: ✅" || echo "npx: ⚠️ missing — install Node.js (for playwright)"
command -v ccc &>/dev/null && echo "cocoindex CLI (ccc): ✅" || echo "cocoindex CLI (ccc): ⚠️ optional — install via: pip install cocoindex"
# uvx-based: codebase-memory-mcp, code-review-graph, serena, cocoindex-code-mcp-server (available when uvx installed)
```

## Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Claude Brain Health — <repo>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CLAUDE.md budget         ✅ 187 lines / 4.2KB (budget: 32KB)
  settings.json            ✅ valid JSON + hooks block
  Hook scripts             ✅ 9/9 executable
  Subagents                ✅ 5/5 non-empty
  Skills                   ✅ 49/49 have valid frontmatter
  Error log                ✅ CLAUDE_ERRORS.md exists
  Secrets scan             ✅ no leaks detected
  codebase-memory-mcp      ⚠️ missing — run setup-plugins.sh
  cocoindex (ccc)          ✅ installed
  code-review-graph        ✅ installed
  uvx (playwright/serena)  ✅ installed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall: ⚠️ healthy with 1 warning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After the table, list any ⚠️/❌ items with one-line fix instructions.
