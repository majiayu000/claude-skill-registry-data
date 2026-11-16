---
name: subagent-dependency
description: "Use when orchestrating multiple subagents with dependencies between them, running agents in parallel, or managing complex multi-agent workflows. Triggers on: 'orchestrate agents', 'chạy song song', 'parallel agents', 'agent dependency', 'subagent graph', 'multi-agent flow', 'agent pipeline', 'which agents can run in parallel', 'agent coordination'."
---

# Subagent Dependency Management Skill

Khi codebase lớn, một task thường cần nhiều subagent. Skill này dạy cách
xây dựng dependency graph, xác định agent nào chạy song song được, và merge
kết quả an toàn — theo subagent-policy (read-only).

## Mô hình dependency

### DAG (Directed Acyclic Graph)

Mỗi agent là một node. Mũi tên = "phải xong trước".

```
Ví dụ: feature audit

    [code-auditor]──────┐
    [security-auditor]──┤──► [architecture-auditor] ──► [report-merger]
    [dependency-analyzer]┘
         ↕
    (song song)
```

- `code-auditor`, `security-auditor`, `dependency-analyzer` → **parallel** (không phụ thuộc nhau)
- `architecture-auditor` → **sequential** (cần output của 3 cái trên)
- `report-merger` → **sequential** (cần tất cả)

## Phân loại dependency

| Loại | Ý nghĩa | Ví dụ |
|------|---------|-------|
| `none` | Độc lập hoàn toàn | code-auditor + security-auditor |
| `data` | B cần output của A | architecture-auditor cần audit results |
| `exclusive` | Không chạy cùng lúc (write conflict) | 2 agents cùng analyze 1 file lớn |
| `soft` | Tốt hơn nếu A xong trước, nhưng không bắt buộc | context-synthesizer trước spec-executor |

## Workflow xây dựng dependency graph

### Step 1 — Liệt kê agents cần dùng

Từ task description, xác định agents:
```
Task: "Full codebase security + performance review"

Agents cần:
1. security-auditor     → tìm lỗ hổng bảo mật
2. performance-auditor  → tìm bottleneck
3. dependency-analyzer  → kiểm tra deps lỗi thời/nguy hiểm
4. code-auditor         → chất lượng code
5. architecture-auditor → tổng hợp findings, đề xuất
```

### Step 2 — Xác định dependencies

Với mỗi cặp agents, hỏi: "B có cần kết quả của A không?"

```
security-auditor     → performance-auditor: none
security-auditor     → dependency-analyzer: none
performance-auditor  → dependency-analyzer: none
code-auditor         → [3 cái trên]: none
architecture-auditor → [tất cả 4 cái trên]: data (cần kết quả)
```

### Step 3 — Vẽ execution plan

```
Wave 1 (parallel):
  - security-auditor
  - performance-auditor
  - dependency-analyzer
  - code-auditor

Wave 2 (sequential, sau Wave 1 xong):
  - architecture-auditor [input: Wave 1 outputs]
```

### Step 4 — Dispatch theo waves

**Wave 1 — Dispatch song song:**
```
Dispatch tất cả 4 agents cùng lúc với instruction:
  "Nhiệm vụ: [đọc/phân tích] X.
   Bạn KHÔNG được sửa bất kỳ file nào.
   Trả về: report text theo format chuẩn."

Chờ tất cả 4 hoàn thành.
```

**Wave 2 — Dispatch sau khi Wave 1 xong:**
```
Dispatch architecture-auditor với:
  Input: [Wave 1 reports merged]
  Instruction: "Tổng hợp 4 reports trên. Tìm pattern chung,
                xếp hạng risk, đề xuất action plan."
```

### Step 5 — Merge results

Main agent merge theo priority:

```markdown
## Merged Analysis Report

**Critical findings (action required):**
[từ security + dependency — highest risk]

**Performance findings:**
[từ performance-auditor]

**Code quality findings:**
[từ code-auditor]

**Architecture recommendations:**
[từ architecture-auditor — synthesis]

**Action plan (ordered by impact):**
1. [highest impact, lowest effort]
2. ...
```

## Anti-patterns cần tránh

| Anti-pattern | Vấn đề | Fix |
|-------------|---------|-----|
| Sequential khi parallel được | Tốn thời gian | Vẽ DAG trước khi dispatch |
| Parallel khi có data dependency | Agent B nhận input rỗng | Kiểm tra dependency loại `data` |
| Quá nhiều agents một lúc | Context window của main agent bị overflow | Tối đa 4–5 agents / wave |
| Subagent tự merge kết quả | Vi phạm subagent-policy | Main agent luôn là người merge |
| Không ghi rõ scope cho mỗi agent | Agent đọc quá nhiều file, tốn token | Scope xuống path cụ thể |

## Template dispatch instruction

```
Subagent: [tên agent]
Scope: [file/directory cụ thể cần đọc]
Nhiệm vụ: Phân tích [X] và báo cáo [Y].
Bạn KHÔNG được sửa bất kỳ file nào.
Bạn KHÔNG được chạy git commit hoặc git push.
Format báo cáo:
  ## Findings
  ## Risk level: [HIGH | MEDIUM | LOW]
  ## Recommended actions for main agent
  ## No files were modified.
```

## Sizing guide

| Codebase size | Recommended max waves | Max agents/wave |
|---|---|---|
| < 10K LOC | 2 waves | 3 agents |
| 10K–100K LOC | 3 waves | 4 agents |
| > 100K LOC | 4+ waves | 5 agents (context budget cẩn thận) |

Với codebase lớn: ưu tiên scope agents xuống module/directory nhỏ
thay vì cho mỗi agent đọc toàn bộ repo.
