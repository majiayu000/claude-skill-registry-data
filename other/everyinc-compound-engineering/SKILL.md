---
name: everyinc--compound-engineering
description: "Compound Engineering plugin cho Claude Code + Cursor — 37 skills, 51 agents, triết lý 80% planning/review + 20% execution. Mỗi unit làm việc sau dễ hơn trước."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Compound Engineering: plugin Claude Code/Cursor với triết lý ngược technical debt — mỗi feature làm subsequent feature DỄ HƠN, không phức tạp hơn.

## Install

```bash
# Claude Code
/plugin marketplace add EveryInc/compound-engineering-plugin
/plugin install compound-engineering

# Local dev
alias cce='claude --plugin-dir ~/Code/compound-engineering-plugin/plugins/compound-engineering'
```

## Core Workflow

```
/ce-brainstorm [topic]   → interactive Q&A develop requirements
/ce-plan [requirements]  → detailed implementation plan
/ce-work                 → execute với task tracking
/ce-code-review          → multi-agent review trước khi merge
/ce-compound             → document learnings cho future reuse
```

## 37 Skills (chọn lọc)

```
/ce-strategy     — product strategy docs làm grounding cho mọi work
/ce-brainstorm   — Q&A trước khi implement (không code vội)
/ce-plan         — idea → detailed plan
/ce-work         — execute plan + track tasks
/ce-code-review  — multi-agent review
/ce-compound     — capture learnings → reusable knowledge
/ce-debug        — systematic reproduce + fix
/ce-product-pulse — usage + performance reports theo time window
/ce-setup        — initialize project config
```

## 51 Agents

Specialized agents hỗ trợ: review, research, workflow management, quality assurance.

## Triết lý

```
80% planning + review
20% execution

Mỗi unit of work:
  □ Có spec rõ trước khi code
  □ Có review trước khi merge
  □ Document lại learning sau khi xong
```

## Debug Cycle

```
/ce-debug [problem]
  → systematic reproduction
  → root cause analysis
  → fix + verify
/ce-compound  ← capture fix pattern
```

## Source

https://github.com/EveryInc/compound-engineering-plugin · MIT · +1752⭐/week
