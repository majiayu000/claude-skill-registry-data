---
name: claudiodrews--memory-os
description: "Hệ thống bộ nhớ 7 lớp chạy local dành cho AI agent — SQLite + Qdrant + Fabric, zero cloud dependency. Agent nhớ project, decision, reasoning pattern xuyên session."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Memory OS biến Hermes Agent (hoặc bất kỳ LLM agent nào) thành collaborator dài hạn: nhớ đủ thứ giữa các session mà không cần cloud, không vendor lock-in.

## 7 Lớp Kiến Trúc

```
Layer 1 — Workspace Files
  MEMORY.md, USER.md, CREATIVE.md inject vào system prompt mỗi turn

Layer 2 — Session History
  SQLite + FTS5 full-text search — archive toàn bộ conversation

Layer 3 — Structured Facts
  Entity resolution + trust scoring + auto feedback loop

Layer 4 — Fabric (Cross-Session Extraction)
  LLM-powered summarization, 16 tools: fabric_recall, fabric_write, fabric_brief

Layer 5 — Vector Database
  Qdrant 4096-dim cosine + BM25 sparse, fallback: hybrid→dense→lexical→SQLite
  Weekly decay scan + semantic dedup (cosine > 0.92)

Layer 6 — Auto-Curated Wiki
  Self-organizing knowledge vault: concepts, entities, comparisons → Qdrant

Layer 7 — Ground Truth Hierarchy
  SOUL.md + rulebook.md — injected memory = authoritative
  Ngăn agent re-discover context đã có → tiết kiệm token
```

## Install

```bash
# One-command setup — Docker orchestrate Qdrant + Redis + ARQ worker
curl -fsSL https://raw.githubusercontent.com/ClaudioDrews/memory-os/main/install.sh -o /tmp/memory-os-install.sh
# Inspect first: head -40 /tmp/memory-os-install.sh — then run if safe:
bash /tmp/memory-os-install.sh
```

## Core Tools (Fabric Layer)

```python
fabric_recall(query, n=5)     # semantic search memory
fabric_write(content, tags)   # lưu fact mới
fabric_brief(session_id)      # summarize session → store
```

## Tích Hợp

```python
# Compatible với bất kỳ LLM provider nào Hermes support
# OpenRouter, OpenAI, Anthropic, Ollama, local models

# Databases:
# state.db — session history
# memory_store.db — facts + HRR (hierarchical relation)
# Qdrant — semantic vectors
```

## So Với Alternatives

| Feature | Memory OS | mem0 | Zep | Letta |
|---------|-----------|------|-----|-------|
| Fully local | ✅ | ❌ | ❌ | ❌ |
| Ground Truth layer | ✅ | ❌ | ❌ | ❌ |
| Trust-scored facts | ✅ | ❌ | ✅ | ❌ |
| Self-curating wiki | ✅ | ❌ | ❌ | ❌ |
| No subscription | ✅ | ❌ | ❌ | ❌ |

## Layer 7 — Quan Trọng Nhất

Nếu không có Ground Truth ranking: agent bỏ qua injected context, gọi API tìm lại thứ đã có trong prompt → waste token + slow.
Layer 7 force agent treat injected memory là authoritative source.

## Source

https://github.com/ClaudioDrews/memory-os · MIT
