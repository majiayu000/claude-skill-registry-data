---
name: bb-create-issue
description: "Babel internal issue protocol — create a labeled handoff between pipeline agents. Writes designs/<name>/.handoff/<label>.md and appends to handoff_log.jsonl; best-effort gh issue create if gh available. Triggered by every guru/architect agent at handoff time."
---

# bb-create-issue

## Inputs

- `--label <label>` — one of `ready-for-rtl | ready-for-verification | ready-for-synth | ready-for-pd | signoff | arch-needs-fix | rtl-needs-fix | synth-needs-fix | escalate-user | pd-rework`
- `--artifact <path>` — canonical artifact path (e.g. `designs/<name>/mas/mas.json`)
- `--body-file <path>` (optional) — markdown body source
- `--correlation-id <sha256>` (optional) — sha256 of failing artifact for dedup (fix M-07)
- `--design-name <name>` (optional) — derived from artifact path if absent
- `--summary <one-liner>` (optional) — placed at top of body

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/.handoff/<label>.md` |
| `log_path` | `designs/<name>/.handoff/handoff_log.jsonl` |
| `gh_issue_url` | URL\|null |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — derive_design_name

```
if --design-name absent:
  parse from --artifact: matches "designs/([^/]+)/" → design_name
  if no match: error "cannot derive design_name", exit 2
```

### Phase 2 — write_handoff

LLM 直接调 `Write` 工具写出 `designs/<design_name>/.handoff/<label>.md`：

```markdown
# <label>
- timestamp: <ISO 8601 Beijing time>
- artifact: <path>
- correlation_id: <sha or NA>
- summary: <one-liner or "">
- body: <body-file content or stdin>
```

### Phase 3 — append_log

调 `Bash`：
```bash
mkdir -p designs/<design_name>/.handoff
LINE=$(printf '{"ts":"%s","label":"%s","artifact":"%s","correlation_id":"%s"}' \
  "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "<label>" "<artifact>" "<correlation_id_or_NA>")
echo "$LINE" >> designs/<design_name>/.handoff/handoff_log.jsonl
```

### Phase 4 — gh_best_effort

```bash
if command -v gh >/dev/null 2>&1; then
  gh issue create \
    --label "<label>" \
    --title "<label>: <design_name>" \
    --body-file designs/<design_name>/.handoff/<label>.md \
    2>/dev/null || true
fi
```

返回 `{artifact_path, log_path, gh_issue_url|null, valid:true}`。

## Failure Modes

- design_name 不可推导 → exit 2
- label 不在 allow-list → exit 3
- Write 失败 → 返回 `{valid:false, error:"write failed"}`

## 与 PostToolUse hook 联动

写入 `<label>.md` 后由 `bb-hook-pipeline-advance.sh` 自动提示用户下一步 agent；写 `*-needs-fix.md` 由 `bb-hook-create-fix-issue.sh` 记录 escalation。

## Allow-list

```
ready-for-rtl, ready-for-verification, ready-for-synth, ready-for-pd, signoff,
arch-needs-fix, rtl-needs-fix, synth-needs-fix, pd-rework, escalate-user
```
