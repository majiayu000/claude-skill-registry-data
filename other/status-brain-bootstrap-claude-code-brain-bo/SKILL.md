---
name: status
description: Project status dashboard — CLAUDE.md budget, unfilled placeholders, lessons file size, hooks executability, jq availability, plugin states. One-glance health report.
---

# Status Skill — Project Dashboard

Give a one-glance status report of the Claude Brain setup for this repo.

Run these checks in order and report each as ✅ / ⚠️ / ❌:

## 1. CLAUDE.md budget
```bash
wc -c < CLAUDE.md 2>/dev/null || echo "MISSING"
wc -l < CLAUDE.md 2>/dev/null || echo "0"
```
- ✅ ≤ 32768 bytes (32KB) · ⚠️ 28000–32768 · ❌ > 32768 or missing

## 2. Unfilled placeholders
```bash
grep -rEc '\{\{[A-Z_]+\}\}' CLAUDE.md claude/ .claude/ 2>/dev/null | awk -F: '{s+=$2} END {print s+0}'
```
- ✅ 0 (end-user repo) · ⚠️ > 0 (bootstrap still has unfilled slots)

## 3. Lessons file size
```bash
wc -l < claude/tasks/lessons.md 2>/dev/null || echo "0"
```
- ✅ ≤ 400 lines · ⚠️ 401–500 · ❌ > 500 (archive to `claude/tasks/lessons-archive-YYYY.md`)

## 4. Hooks executability
```bash
for h in .claude/hooks/*.sh; do test -x "$h" || echo "NOT_EXEC: $h"; done
echo "HOOKS_DONE"
```
- ✅ all executable · ❌ any NOT_EXEC line

## 5. jq availability
```bash
command -v jq &>/dev/null && echo "PRESENT" || echo "MISSING"
```
- ✅ present · ⚠️ missing — `brew install jq` / `sudo apt install jq`

## 6. Plugin states
```bash
command -v uvx &>/dev/null && echo "uvx: installed" || echo "uvx: MISSING (uvx-based plugins unavailable)"
command -v npx &>/dev/null && echo "npx: installed" || echo "npx: MISSING (playwright unavailable)"
command -v ccc &>/dev/null && echo "cocoindex CLI (ccc): installed" || echo "cocoindex CLI (ccc): optional"
# codebase-memory, code-review-graph, serena, cocoindex-code-mcp-server all run via uvx
# playwright runs via npx
```
- ✅ uvx installed · ⚠️ missing (run `brew install uv` / `pip install uv`)

## 7. MCP servers
```bash
jq '.mcpServers | keys | length' .claude/settings.json 2>/dev/null || echo "0"
```
- ✅ ≥ 1 configured · ⚠️ 0 (add mcpServers block to `.claude/settings.json`)

## Report Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Claude Brain Status — <repo>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CLAUDE.md budget         ✅ 218 lines / 7.1KB (budget: 32KB)
  Placeholders             ✅ 0 unfilled
  Lessons file             ✅ 312 / 500 lines
  Hooks                    ✅ 9/9 executable
  jq                       ✅ present
  codebase-memory-mcp      ✅ installed
  cocoindex (ccc)          ⚠️ missing — run setup-plugins.sh
  code-review-graph        ✅ installed
  serena                   ✅ available via uvx
  playwright               ✅ available via uvx
  MCP servers              ✅ 3 configured
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Overall: ⚠️ healthy (1 warning)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After the table, list ⚠️/❌ items with one-line fix instructions.
