---
name: danielmiessler--personal-ai-infra
description: "Personal AI Infrastructure (PAI) — Life OS chạy trên Claude Code: 45 skills, 171 workflows, 37 hooks, ISA pattern, Telos (life direction), Pulse dashboard localhost:31337."
allowed-tools: Bash, Read, Write
user-invocable: true
---

PAI (Personal AI Infrastructure) của Daniel Miessler: Life Operating System — không phải chatbot, mà là OS tích hợp AI vào toàn bộ workflow cá nhân.

## Install

```bash
# Download and verify before executing (never pipe to a shell)
curl -sSL https://ourpai.ai/install.sh -o /tmp/pai-install.sh
# Inspect first: head -40 /tmp/pai-install.sh
# If the content looks safe, then run it:
bash /tmp/pai-install.sh
# Setup: Bun + Git + ElevenLabs voice (optional) + DA identity
```

## Setup

```
/interview    — Phase 1: TELOS (mission, goals, beliefs, mental models)
             — Phase 2: Ideal State articulation
             — Phase 3: Tool + working-style preferences
             — Phase 4: DA personality customization
```

## 3-Layer Architecture

```
Layer 1 — PAI Core
  skills/, memory/, algorithms/, identity/, telos/

Layer 2 — Pulse (dashboard)
  localhost:31337 — visualize state, goals, active work

Layer 3 — The DA (Digital Assistant)
  Personified AI, specific identity + voice + personality
```

## Memory System (5 tiers)

```
WORK          — active task docs
KNOWLEDGE     — typed graph: people, companies, ideas, research
LEARNING      — meta-patterns và insights
RELATIONSHIP  — DA-Principal interaction notes
OBSERVABILITY — tool calls, hooks, satisfaction signals
```

## The Algorithm v6.3.0 (7-phase loop)

```
OBSERVE → THINK → PLAN → BUILD → EXECUTE → VERIFY → LEARN
```

Task complexity: MINIMAL / NATIVE / ALGORITHM (E1–E5 tiers).

## ISA Pattern (Ideal State Artifact)

Template "done" rõ ràng cho mọi task sáng tạo:

```markdown
## Problem Definition
## Vision (what done looks like)
## Constraints
## Success Criteria (measurable)
## Test Strategy
## Verification Conditions
```

## Key Design Principles

- **Code > Prompts** — ưu tiên code execution, không wrap logic trong prompts
- **Filesystem as RAG** — plain-text + ripgrep thay vì SQL/embeddings
- **Containment Zones** — PreToolUse hooks ngăn cross-zone info leakage
- **Context > Model** — đúng context quan trọng hơn chọn model

## Scale

- 45 public skills
- 171 workflows
- 37 hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SessionEnd)

## Source

https://github.com/danielmiessler/Personal_AI_Infrastructure · MIT · +70⭐ today
