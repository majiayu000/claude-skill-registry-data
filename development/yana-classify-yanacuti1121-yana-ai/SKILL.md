---
name: yana-classify
description: "Yana's task router — classify a task description into simple/complex/external and decide next action. Use before handling any non-trivial request. Triggers on: 'classify task', 'route task', 'yana classify', 'what kind of task', 'should I handle this myself', 'dispatch or handle', 'yana router', 'task type', 'route request', 'auto or agent'."
tier: TIER 2 — CORRECTNESS
source: yana-ai (yana-router, src/route.rs)
---

# yana-classify — Yana Task Router
# Source: yana-ai internal — src/route.rs (yana-router Rust subcommand)

Classify bất kỳ task description nào → **simple / complex / external** để Yana
quyết định tự xử lý hay cần dispatch agent / xin xác nhận anh.

---

## Khi nào dùng

Yana nên classify **trước khi** xử lý mọi task không rõ scope:
- Anh giao việc mơ hồ ("làm cái này đi")
- Task có thể là read-only hoặc có thể cần sửa file
- Không chắc có cần spawn agent không
- Muốn auto-route thay vì tự đoán

---

## Gọi yana-router

```bash
# Cách 1 — dev build (local)
BINARY="/tmp/yamtam-build/debug/yamtam-rt"

# Cách 2 — nếu yamtam-rt trong PATH
BINARY="yamtam-rt"

# Classify và lấy JSON
"$BINARY" route classify "<task description>" 2>/dev/null

# Plain text (debug)
"$BINARY" route classify "<task description>" --plain 2>/dev/null
```

**Fallback khi binary không có**: dùng keyword heuristic thủ công (xem bên dưới).

---

## Output JSON

```json
{
  "route": "simple | complex | external",
  "gate":  "auto  | harness | confirm",
  "confidence": 0.0–1.0,
  "reason": "...",
  "matched_signals": ["keyword(label)", ...],
  "suggested_agents": ["agent-name", ...]
}
```

---

## Quyết định theo route

### `simple` → gate: `auto`

Yana **tự xử lý**, không spawn agent, không cần xác nhận.

```
✓ Trả lời trực tiếp
✓ Đọc file, grep, git log, git diff
✓ Giải thích code, tóm tắt, liệt kê
✗ Không sửa file
✗ Không commit
```

### `complex` → gate: `harness`

Yana chọn **1 trong 2 path** tùy số subtasks và dependency:

#### Path A — Single agent (1–2 subtasks, không có dep giữa chúng)

Dispatch trực tiếp — không cần mission:

```
Agent(
  subagent_type: "<suggested_agents[0]>",
  prompt: """
    Task: <task description>

    Scope
    - owns (may modify):  <files>
    - produces (must create): <output files>
    - consumes (available input): <input files nếu có>

    Rules (subagent-policy: report-only)
    - Do NOT modify any file.
    - Do NOT run git commit or git push.
    - Return: plain-text findings + recommended changes with file:line refs.
  """
)
→ Nhận report → Yana apply changes → verify
```

**Khi confidence < 0.4**: hỏi anh một câu để xác nhận scope trước khi dispatch.

#### Path B — Multi-agent mission (3+ subtasks hoặc có dep A→B→C)

Dùng `mission-run` để dispatch theo wave:

```
Dấu hiệu cần Path B:
  □ suggested_agents có ≥ 2 loại khác nhau
  □ Output của task A là input của task B
  □ Task ước tính > 5 file thay đổi

Cách chạy:
  RT="${YAMTAM_RT:-/tmp/yamtam-build/debug/yamtam-rt}"
  
  # 1. Tạo mission
  MID=$("$RT" mission create "<tên>" | awk '/id:/{print $2}')
  
  # 2. Add tasks (lặp cho từng subtask)
  "$RT" mission task "$MID" "<name>" \
    --agent <agent> --owns <files> \
    --produces <out> --consumes <dep-out>
  
  # 3. Dispatch wave 1 — lấy JSON briefs
  BRIEFS=$("$RT" mission dispatch "$MID")
  
  # 4. Với mỗi brief → spawn Agent() như Path A
  #    → apply report → mark done/fail → dispatch wave tiếp
  #    (xem mission-run skill để biết full loop)
```

### `external` → gate: `confirm`

Yana **DỪNG** và hỏi anh trước khi làm bất cứ gì:

```
⚠ CONFIRM REQUIRED
Action : [task description]
Reason : [reason từ JSON]
Signal : [matched_signals]

Anh có muốn tiếp tục? (y/N)
```

Chỉ proceed sau khi anh trả lời "y" / "có" / "ok" rõ ràng.

---

## Fallback — khi binary không build được

Heuristic nhanh: external nếu có `push/deploy/publish/drop table` → complex nếu có `implement/fix/sửa/tạo` → simple.

---

## Ví dụ thực tế

```
Input:  "explain how yana-router works"
Output: simple → Yana tự giải thích từ code

Input:  "implement JWT refresh token"
Output: complex → dispatch backend-developer agent

Input:  "git push main và tạo release v0.41.0"
Output: external → hỏi anh xác nhận trước

Input:  "sửa bug login không redirect đúng"
Output: complex → dispatch debugger + backend-developer

Input:  "xem git log 10 commit gần nhất"
Output: simple → Yana chạy git log trực tiếp
```

---

## Integration với DIRECTION.md

Yana nên auto-classify **mọi task** ở đầu session nếu DIRECTION.md có rule:

```markdown
## Auto-routing (yana-classify)
- Mọi task anh đưa ra → classify trước → quyết định route
- Confidence < 0.3 → hỏi anh clarify
- External luôn confirm, không exception
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu classify "deploy to production" thành simple/complex
❌ FAIL nếu gọi binary mà không handle exit code ≠ 0
❌ FAIL nếu proceed external task mà không có explicit confirm
❌ FAIL nếu dispatch agent mà không tạo task brief trước
✅ PASS khi: route đúng loại + gate đúng + action tiếp theo đúng
```

---

## See also
- `mission-run` — full multi-agent loop (Path B chi tiết)
- `subagent-policy` — quy tắc dispatch agent (report-only, không tự sửa file)
- `conflict-resolution` — xử lý khi multi-agent đề xuất chồng chéo
- `agents-v2` — agent routing table đầy đủ
