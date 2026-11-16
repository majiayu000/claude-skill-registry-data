---
name: mission-run
description: "Parallel multi-agent mission loop using yamtam-rt — decompose task into subtasks with deps, dispatch waves, collect reports, apply changes. Use when yana-classify returns route: complex. Triggers on: 'mission run', 'run mission', 'dispatch agents', 'parallel agents', 'multi-agent task', 'orchestrate agents', 'coordinate agents', 'agent mission', 'wave dispatch', 'mission loop', 'dispatch loop', 'parallel dispatch', 'yamtam-rt mission'."
source: yana-ai (src/mission/mod.rs)
tier: TIER 2 — CORRECTNESS
---

# mission-run — Parallel Multi-Agent Mission Loop
# Source: yana-ai internal (src/mission/mod.rs)

Chạy toàn bộ vòng lặp: tạo mission → khai báo tasks với deps → dispatch
wave-by-wave → collect reports → apply → repeat cho đến khi done hoặc blocked.

**Do NOT use for:** generic orchestration không dùng yamtam-rt → xem `plan-orchestrate`.
**Do NOT use for:** task SQLite queue → xem `kanban-dispatcher`.
**Do NOT use for:** task đơn lẻ < 3 subtasks → dùng `dynamic-workflow-mode`.

---

## Khi nào dùng

- `yana-classify` trả về `route: complex, gate: harness`
- Task cần nhiều agent chạy song song với dependency giữa chúng
- Cần track progress + evidence qua nhiều waves

---

## Bước 1 — Decompose thành subtask list

Trước khi tạo mission, khai báo rõ từng subtask:

```
name:         kebab-case
agent:        agent type (từ FleetView catalog)
owns:         files task này được phép sửa
produces:     artifact output (file paths)
consumes:     artifacts phải tồn tại TRƯỚC khi task chạy  ← tạo dependency
pass:         shell cmd exit 0 = done (tuỳ chọn)
instructions: custom brief (tuỳ chọn — override auto-generated)
```

Ví dụ decompose "implement user auth":

| Task | Agent | consumes | produces |
|------|-------|----------|----------|
| design-schema | database-expert | — | schema.sql |
| implement-auth | backend-developer | schema.sql | src/auth.ts |
| write-tests | test-engineer | src/auth.ts | tests/auth.test.ts |

---

## Bước 2 — Tạo mission + add tasks

```bash
RT="${YAMTAM_RT:-/tmp/yamtam-build/debug/yamtam-rt}"

# Tạo mission, lấy ID
RESULT=$("$RT" mission create "<mission-name>")
MID=$(echo "$RESULT" | awk '/id:/{print $2}')

# Add tasks — thứ tự không quan trọng, deps tự resolve
"$RT" mission task "$MID" "design-schema" \
  --agent database-expert \
  --produces schema.sql \
  --pass "test -f schema.sql"

"$RT" mission task "$MID" "implement-auth" \
  --agent backend-developer \
  --owns "src/auth.ts" \
  --consumes schema.sql \
  --produces src/auth.ts

"$RT" mission task "$MID" "write-tests" \
  --agent test-engineer \
  --owns "tests/auth.test.ts" \
  --consumes src/auth.ts \
  --produces tests/auth.test.ts \
  --pass "npx vitest run tests/auth.test.ts"
```

---

## Bước 3 — Dispatch loop

```bash
MAX_WAVES=10
WAVE=0

while [ $WAVE -lt $MAX_WAVES ]; do
  WAVE=$((WAVE + 1))
  echo "── Wave $WAVE ──"

  BRIEFS=$("$RT" mission dispatch "$MID" --max-parallel 3 2>&1)

  # Mission complete
  echo "$BRIEFS" | grep -q "all tasks done" && { echo "✓ Done"; break; }

  # No ready tasks (blocked or all running)
  if [ -z "$BRIEFS" ] || echo "$BRIEFS" | grep -qE "^⚠"; then
    "$RT" mission status "$MID"
    break
  fi

  # Spawn một agent cho mỗi brief trong wave này
  # (Yana thực hiện việc spawn — xem Bước 4)
  # Sau khi agents xong:
  #   "$RT" mission done "$MID" "<task>" --evidence "<path>"
  # hoặc:
  #   "$RT" mission fail "$MID" "<task>" --reason "<lý do>"
done
```

---

## Bước 4 — Spawn agent từ brief

Với mỗi JSON brief từ `mission dispatch`, Yana dispatch agent:

```json
{
  "task_name": "implement-auth",
  "agent": "backend-developer",
  "scope": {
    "owns":     ["src/auth.ts"],
    "consumes": ["schema.sql"],
    "produces": ["src/auth.ts"]
  },
  "pass_criteria": null,
  "instructions": "You are acting as: backend-developer\n...",
  "subagent_policy": "report-only — do not write files, return findings as plain text"
}
```

**Luật spawn (từ subagent-policy.md):**

```
Agent nhận brief → phân tích + đề xuất → trả plain text report
Yana nhận report → apply changes (vì subagent KHÔNG được sửa file)
Yana → "$RT" mission done "$MID" "<task>" --evidence "<evidence-path>"
```

---

## Bước 5 — Xử lý blocked / stuck

```bash
# Xem trạng thái
"$RT" mission status "$MID"

# Task fail → retry
"$RT" mission retry "$MID" "<task-name>"

# Agent bị kẹt (Running quá lâu) → cancel để dispatch lại
"$RT" mission cancel "$MID" "<task-name>"
```

---

## Quick reference

```bash
RT="${YAMTAM_RT:-/tmp/yamtam-build/debug/yamtam-rt}"

"$RT" mission create  <name>
"$RT" mission task    <mid> <name> [--agent X] [--owns A,B] [--produces C] \
                                   [--consumes D] [--pass CMD] [--instructions "..."]
"$RT" mission dispatch <mid> [--max-parallel 3]   # → JSON briefs + marks Running
"$RT" mission done    <mid> <task> --evidence <path>
"$RT" mission fail    <mid> <task> --reason <text>
"$RT" mission cancel  <mid> <task>                 # Running → Pending
"$RT" mission retry   <mid> <task>                 # Failed  → Pending
"$RT" mission status  [mid]
"$RT" mission list
"$RT" mission report  <mid>                        # full JSON
```

---

## Anti-fake-pass

```
❌ Claim mission done khi còn task pending/running
❌ Mark done mà không có evidence path thực tế trên disk
❌ Dispatch nhiều hơn max-parallel trước khi wave hiện tại xong
❌ Bỏ qua consumes dependencies — dispatch task chưa ready
❌ Subagent tự sửa file thay vì report-only (vi phạm subagent-policy)
❌ Dispatch loop không có MAX_WAVES guard (vòng lặp vô hạn)
❌ Tạo mission mà không parse MID từ output trước khi add tasks
```

---

## Xem thêm

- `yana-classify` — route task trước khi chọn harness
- `dynamic-workflow-mode` — per-task harness cho task đơn hơn
- `plan-orchestrate` — generative-only, không dùng yamtam-rt
- `kanban-dispatcher` — SQLite queue, multi-worker model khác
- `subagent-policy.md` — tại sao subagent chỉ report-only
