---
name: bb-close-issue
description: "Babel internal issue protocol — close a handoff after downstream agent picked it up or user signed off. Moves designs/<name>/.handoff/<label>.md to .handoff/closed/ (using mv per CLAUDE.md), appends to handoff_log.jsonl."
---

# bb-close-issue

## Inputs

- `--label <label>` — handoff label to close
- `--design-name <name>` — required
- `--reason <text>` (optional) — close reason
- `--close-gh` (flag) — also close paired gh issue

## Output Contract

| field | 值 |
|-------|----|
| `closed_path` | `designs/<name>/.handoff/closed/<label>_<stamp>.md` |
| `log_path`    | `designs/<name>/.handoff/handoff_log.jsonl` |
| `gh_closed`   | bool |
| `valid`       | bool |

## 4-Phase 执行

### Phase 1 — validate

```
src="designs/<name>/.handoff/<label>.md"
[ -f "$src" ] || exit 2  # nothing to close
```

### Phase 2 — move (mv 不 rm)

调 `Bash`：
```bash
STAMP=$(date -u +'%Y%m%d-%H%M%SZ')
mkdir -p designs/<name>/.handoff/closed
mv designs/<name>/.handoff/<label>.md designs/<name>/.handoff/closed/<label>_${STAMP}.md
```

### Phase 3 — append_log

```bash
LINE=$(printf '{"ts":"%s","action":"close","label":"%s","reason":"%s"}' \
  "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "<label>" "<reason>")
echo "$LINE" >> designs/<name>/.handoff/handoff_log.jsonl
```

### Phase 4 — gh (optional)

```bash
if [ "<close-gh>" = "true" ] && command -v gh >/dev/null 2>&1; then
  gh issue list --label "<label>" --state open --json number \
    | python3 -c "import sys,json; [print(i['number']) for i in json.load(sys.stdin)]" \
    | xargs -I{} gh issue close {} --comment "Closed by bb-close-issue: <reason>"
fi
```

## Failure Modes

| 状态 | 退出码 |
|------|--------|
| handoff 文件不存在 | 2 |
| mv 失败 | 4 |
| gh 不可用且 `--close-gh` 指定 | warning（exit 0） |
