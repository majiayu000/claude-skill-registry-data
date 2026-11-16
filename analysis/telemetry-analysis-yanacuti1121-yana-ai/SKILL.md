---
name: telemetry-analysis
description: "Use when asked to analyze hook activity, token usage, audit logs, or agent behavior patterns. Triggers on: 'xem log', 'hook nào fire nhiều', 'token usage', 'audit trail', 'what hooks fired', 'session summary', 'telemetry report', 'hook health', 'agent activity'."
---

# Telemetry Analysis Skill

Đọc và phân tích dữ liệu telemetry local của YAMTAM để hiểu sức khỏe hệ thống,
pattern hook, và chi phí token — không cần network, không cần external service.

## Nguồn dữ liệu

| File | Nội dung | Format |
|------|---------|--------|
| `.claude/state/audit-chain.log` | Mọi tool call theo thứ tự thời gian | JSONL, hash-chain |
| `.claude/state/telemetry.jsonl` | Chi tiết từng hook: tool, decision, duration | JSONL |
| `.claude/state/session-trust.json` | Trust score hiện tại + lịch sử decrement | JSON |
| `.claude/session-read-log.txt` | Files đã đọc trong session | Plain text |

## Workflow phân tích

### Step 1 — Kiểm tra file tồn tại

```bash
ls -la .claude/state/ 2>/dev/null || echo "No state dir — YAMTAM not applied yet"
wc -l .claude/state/audit-chain.log 2>/dev/null || echo "No audit log"
wc -l .claude/state/telemetry.jsonl 2>/dev/null || echo "No telemetry"
```

### Step 2 — Hook activity summary

```bash
# Hook nào fire nhiều nhất
jq -r '.hook // "unknown"' .claude/state/telemetry.jsonl 2>/dev/null \
  | sort | uniq -c | sort -rn | head -10

# Tỉ lệ block vs allow vs warn
jq -r '.decision // "unknown"' .claude/state/telemetry.jsonl 2>/dev/null \
  | sort | uniq -c | sort -rn
```

### Step 3 — Tool call pattern

```bash
# Tool nào được gọi nhiều nhất
jq -r '.tool // "unknown"' .claude/state/audit-chain.log 2>/dev/null \
  | sort | uniq -c | sort -rn | head -10

# Timeline: 10 tool call gần nhất
jq -r '[.ts, .tool, .agent] | @tsv' .claude/state/audit-chain.log 2>/dev/null \
  | tail -10
```

### Step 4 — Trust score health

```bash
cat .claude/state/session-trust.json 2>/dev/null | jq '.'
```

Diễn giải:
- Score ≥ 80: Healthy — agent hoạt động tốt
- Score 50–79: Caution — một số unverified claim
- Score < 50: 🔴 LOW TRUST — require double evidence cho mọi claim

### Step 5 — Expensive operations

```bash
# Hook nào tốn thời gian nhất (nếu có duration field)
jq -r 'select(.duration_ms != null) | [.duration_ms, .hook] | @tsv' \
  .claude/state/telemetry.jsonl 2>/dev/null \
  | sort -rn | head -10
```

### Step 6 — Bypass usage

```bash
# Có env var bypass nào được dùng không
jq -r 'select(.input | strings | contains("YAMTAM_BYPASS") or contains("APPROVED")) | .input' .claude/state/audit-chain.log 2>/dev/null | sort | uniq -c
```

## Report format

Sau khi chạy tất cả steps, xuất report:

```
=== Telemetry Report — [date] ===

Hook activity:
  Most fired: [hook] (N times)
  Block rate:  N% | Warn rate: N% | Allow rate: N%

Tool calls:
  Most used: [tool] (N times)
  Total calls: N

Trust score: N/100 — [HEALTHY | CAUTION | LOW TRUST]
  Decrements this session: N

Top expensive hooks: [list if available]

Bypass usage: [N bypasses detected | None]

Recommendations:
  - [nếu block rate cao: xem xét hook đang quá strict]
  - [nếu trust thấp: review claim verbs trong session]
  - [nếu hook im lặng: kiểm tra hook có được wire đúng không]
```

## Khi không có dữ liệu

Nếu `.claude/state/` không tồn tại:
1. YAMTAM chưa được apply vào project này
2. Hoặc agent đang chạy từ engine repo, không phải target project
3. Hướng dẫn: `unzip releases/yana-ai-latest.zip -d .claude/`
