---
name: dynamic-workflow-mode
description: "Task-local harness system — declare owns/consumes/produces/pass-fail before dispatch, extract to shared skill when repeated. Use instead of inline ad-hoc steps for any task spanning >1 session or >3 files. Triggers on: 'dynamic workflow', 'task harness', 'harness per task', 'custom harness', 'adaptive workflow', 'task-local harness', 'owns consumes produces', 'harness template', 'dynamic mode', 'workflow harness'."
source: affaan-m/ECC (MIT) — adapted for yana-ai
tier: TIER 2 — CORRECTNESS
---

# Dynamic Workflow Mode
# Source: affaan-m/ECC (MIT) — adapted with yana-ai integration

Biến mỗi task phức tạp thành một **harness có cấu trúc** thay vì chỉ run inline.
Harness khai báo rõ: làm gì, không làm gì, input là gì, output là gì, pass/fail thế nào.

Khác `eval-harness`: cái đó là project-level EDD framework. Cái này là per-task, nhẹ hơn, tạo trong lúc làm.

---

## Khi nào dùng

- Task cần `complex` route từ `yana-classify` (gate: harness)
- Task span > 1 session hoặc > 3 file
- Cần dispatch nhiều agent với scope khác nhau
- Task có external state, approval gate, hoặc safety risk
- Cùng một workflow lặp lại → extract thành shared skill

## Khi nào KHÔNG dùng

- Task one-shot đơn giản → làm inline, không cần harness
- Task < 15 phút, 1 file, không có side effect bên ngoài
- Đã có shared skill cover đúng use case → dùng skill đó

---

## Decision Tree — Tạo harness hay không?

```
Task mới
  │
  ├─ One-shot, 1 file, < 15 min?
  │    → Làm inline. Không tạo harness.
  │
  ├─ Lặp lại nhưng input thay đổi?
  │    → Tạo task-local harness trong .claude/harnesses/<task-slug>/
  │
  ├─ Lặp lại giữa nhiều session / repo?
  │    → Extract thành core/skills/<name>/SKILL.md
  │
  ├─ Có external state, queue, approval?
  │    → Harness + control pane checkpoints
  │
  └─ Có safety risk (rm, deploy, publish)?
       → Harness + eval gate + human gate (DIRECTION.md external route)
```

---

## Template Harness

Điền trước khi viết code hoặc dispatch agent:

```markdown
# Harness — [task-slug]
Created: YYYY-MM-DD

## Objective
- Ship:    [1 câu — kết quả hữu hình, đo được]
- Not ship: [explicitly scoped out — tránh scope drift]

## Inputs
- Repo/workspace: [path hoặc wildcard files được phép đụng]
- External:       [API, service, DB — nếu có]
- Credentials:    [không lưu secret — chỉ tên env var]

## Owns / Consumes / Produces
- owns:     [files/data task này có quyền sửa]
- consumes: [artifacts từ task khác phải có trước — tên + path]
- produces: [files/data/reports task này tạo ra]

## Loop
1. Discover current state (đọc, không sửa)
2. Generate/update smallest useful artifact
3. Run eval check
4. Record status + handoff
5. Stop on: gate fail | unclear ownership | unsafe external action

## Eval
- Command:  [lệnh cụ thể để verify pass/fail]
- Pass signal: [output hoặc exit code khi đúng]
- Fail owner:  [ai/gì chịu trách nhiệm khi fail]

## Handoff
- Status:     [DONE / BLOCKED / NEEDS_HUMAN]
- Evidence:   [path tới artifact hoặc output chứng minh]
- Next action: [việc tiếp theo nếu có]
```

Lưu tại: `.claude/harnesses/<task-slug>/harness.md`

---

## Eval Gates — chọn loại rẻ nhất đủ tin cậy

| Loại task | Eval gate |
|-----------|-----------|
| Code feature | Test tập trung + lint + 1 integration path |
| UI / frontend | Browser smoke + screenshot + no overflow/error |
| Agent workflow | Fixture transcript với expected routing |
| Research / docs | Source check + claim checklist + publish-ready |
| Integration | Dry-run + config validation + no-secret scan |

Rule: không claim harness "reusable" cho đến khi eval có thể rerun bởi agent khác.

---

## Control Pane Checkpoints

Khi task span > 1 session, ghi checkpoint:

```markdown
## Plan
- Objective: [1 câu]
- Owner: [Yana / agent name]
- Accept criteria: [đo được]
- Risk: [external systems, irreversible actions]

## Queue
- [ ] [subtask 1] — [branch/worktree] — depends: []
- [ ] [subtask 2] — depends: [subtask 1]

## Run (cập nhật mỗi checkpoint)
- Step hiện tại: [bước trong loop]
- Eval result: [PASS/FAIL/PENDING]

## Gate
- Tests: [X/Y passed]
- Security: [no secrets, no path traversal]
- Human approval: [PENDING / APPROVED by ...]

## Handoff
- Done: [...]
- Failed: [...] — lý do
- Needs human: [...] — câu hỏi cụ thể
```

---

## Tích hợp với yamtam

### Sau yana-classify ra `complex`

```
yana-classify → complex → Yana tạo harness → dispatch agent
                                ↓
               .claude/harnesses/<slug>/harness.md
               (owns/consumes/produces filled in)
                                ↓
               Agent nhận harness → report-only (subagent-policy)
                                ↓
               Yana apply + chạy eval command
                                ↓
               Pass → merge / promote artifact
               Fail → stop, report, hỏi anh
```

### Dispatch agent với harness

```markdown
Nhiệm vụ: [task từ harness]
Scope:    [owns list]
Input:    [consumes list]
Output:   [produces list — path cụ thể]

Bạn KHÔNG được sửa bất kỳ file nào ngoài scope.
Bạn KHÔNG được chạy git commit/push.
Trả về: plain text report + evidence path.
```

### Eval command pattern

```bash
# Code grader (deterministic)
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# File existence check
[[ -f ".claude/harnesses/<slug>/output.md" ]] && echo "PASS" || echo "FAIL"

# Git diff guard (không vượt scope)
git diff --name-only HEAD | grep -vE "^(src/auth|docs/)" && echo "SCOPE_DRIFT" || echo "CLEAN"
```

---

## Extract thành Shared Skill

Promote harness → `core/skills/<name>/SKILL.md` khi ≥ 2 trong số:

```
□ Workflow lặp lại ở nhiều session / repo / người
□ Cần thứ tự tool/safety cụ thể
□ Failure lặp vì người dùng skip gate hoặc mất context
□ Có stable input/output contract
□ Cần control pane hoặc team handoff
```

---

## Anti-Patterns

```
❌ Tạo harness cho one-shot task — overhead không cần thiết
❌ Harness không có eval command — "nó chạy được" không phải pass
❌ dispatch agent mà không fill owns/consumes/produces — scope drift
❌ Chạy nhiều agent mà không có conflict policy — xem conflict-resolution rule
❌ Raw private data leak vào public docs qua harness output
❌ Không dùng subagent-policy (agent tự sửa file thay vì report-only)
```

---

## Output chuẩn khi dùng skill này

Kết thúc mỗi dynamic workflow với:

1. **Harness path** — `.claude/harnesses/<slug>/harness.md`
2. **Eval result** — lệnh + output (PASS/FAIL)
3. **Control pane / handoff artifact** — nếu span > 1 session
4. **Extraction candidate** — nếu workflow nên thành shared skill

---

## See also

- `eval-harness` — project-level EDD framework (eval-before-implement)
- `yana-classify` — route classification (complex → harness required)
- `subagent-policy` — agent dispatch rules (report-only)
- `conflict-resolution` — multi-agent edit conflicts
- `agents-v2` — agent routing table
