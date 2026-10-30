---
name: ag-kit
description: "Use when asked to set up AI agent templates with coordinator mode, implement persistent agent memory, compress context for long-running agents, build multi-agent workflows with skills/agents/workflows structure, or use the .agents/ folder convention for AI-native editors. Triggers on: 'ag-kit', 'antigravity kit', 'coordinator mode agent', 'persistent agent memory', 'context compression agent', 'agent workflow template', 'multi-agent coordinator', '.agents folder', 'agent skills workflows', 'ag kit init', 'template đa agent', 'bộ nhớ agent lâu dài'."
---

# AG Kit Skill
# Source: vudovn/ag-kit (TypeScript, 7.6k★) — AI Agent templates with Coordinator Mode + Persistent Memory
# Tier: TIER 3 — PRODUCTIVITY

Template hệ thống multi-agent: Coordinator Mode, Persistent Memory, Context Compression.
Dùng `.agents/` folder — tương thích Claude Code, Cursor, Windsurf.

**Do NOT use for:** `agents-v2` (YAMTAM internal orchestration), `langgraph` (Python graph agents), `memgpt-virtual-context` (MemGPT protocol).

---

## Khi nào dùng

- Cần khởi tạo hệ thống multi-agent nhanh với template sẵn
- Muốn Coordinator Mode: 1 agent điều phối nhiều sub-agent
- Cần persistent memory qua các session
- Tối ưu context compression cho agent chạy lâu
- Dùng slash commands (`/plan`, `/debug`) trong Cursor/Windsurf

---

## Cài đặt nhanh

```bash
# On-demand (khuyên dùng)
npx @vudovn/ag-kit init

# Global
npm install -g @vudovn/ag-kit
ag-kit init
```

Lệnh trên inject thư mục `.agents/` vào project hiện tại.

---

## Cấu trúc `.agents/`

```
.agents/
  coordinator/     ← agent điều phối trung tâm
  skills/          ← kỹ năng chia sẻ giữa agents
  workflows/       ← workflow templates
  memory/          ← persistent memory store
```

---

## Coordinator Mode

```
User request
     ↓
Coordinator Agent
     ↓ phân tích + routing
  ┌──┴──┬──────┬──────┐
  │     │      │      │
Sub-A Sub-B Sub-C Sub-D
  └──┬──┴──────┴──────┘
     ↓ tổng hợp
  Output
```

Coordinator nhận yêu cầu → tách subtask → dispatch → merge kết quả.

---

## Dùng với nhiều repo (Global Symlink)

```bash
# Cài 1 lần tập trung
mkdir -p ~/.ag-kit && cd ~/.ag-kit
npx @vudovn/ag-kit init

# Link vào từng project
ln -s ~/.ag-kit/.agents .agents   # macOS/Linux
```

---

## Lưu ý với AI editors

Không thêm `.agents/` vào `.gitignore` nếu dùng Cursor/Windsurf —
editor cần index folder này để autocomplete slash commands.

Thay vào đó dùng `.git/info/exclude` để giữ local.

---

## Liên quan

- `agents-v2` — YAMTAM internal multi-agent orchestration
- `memgpt-virtual-context` — MemGPT virtual context protocol
- `task-orchestrator` — orchestrate complex multi-step tasks
- `multi-agent-coordinator` — coordinate parallel agent execution
