---
name: bb-list-issues
description: "Babel internal issue protocol — list open handoffs by label. Scans designs/*/.handoff/*.md (filtered by label) and best-effort merge with gh issue list. Used by all guru/architect agents at startup to pick up work."
---

# bb-list-issues

## Inputs

- `--label <label>` (optional) — filter; absent = all
- `--design-name <name>` (optional) — filter; absent = all designs
- `--limit <int>` (optional, default 20) — max returned
- `--include-fixed` (flag) — include closed handoffs from `.handoff/closed/`

## Output Contract

| field | 值 |
|-------|----|
| `issues` | `[{design_name, label, artifact, correlation_id, file, ts}]` |
| `count` | int |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — scan_fs

调 `Bash`：
```bash
PATTERN="designs/*/.handoff/*.md"
[ -n "<label>" ] && PATTERN="designs/*/.handoff/<label>.md"
[ -n "<design-name>" ] && PATTERN="designs/<design-name>/.handoff/*.md"
find . -path "./$PATTERN" -type f 2>/dev/null | sort -r | head -n "<limit>"
```

### Phase 2 — parse_md_frontmatter

调 `Read` 工具读每个匹配 md，按 `- timestamp:` / `- artifact:` / `- correlation_id:` 提字段。filename basename 即 label。

### Phase 3 — gh_merge (best-effort)

```bash
if command -v gh >/dev/null 2>&1 && [ -n "<label>" ]; then
  gh issue list --label "<label>" --limit "<limit>" --json number,title,url 2>/dev/null
fi
```

合并 fs + gh 结果，按 ts 倒序。

### Phase 4 — return

返回 JSON。`count == 0` 时返回 `{issues:[], count:0, valid:true}`。

## 用法示例

```
Skill(bb-list-issues, args="--label ready-for-rtl --limit 5")
Skill(bb-list-issues, args="--design-name uart")
```
