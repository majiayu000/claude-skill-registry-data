---
name: revfactory--harness
description: "Claude Code plugin tự động thiết kế agent team + sinh skill từ domain description — 6 architecture patterns, tạo .claude/agents/ + .claude/skills/ tự động. +2098⭐/week."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Harness (revfactory): factory tạo multi-agent system từ domain description — phân tích domain → thiết kế team → sinh agent definitions + skills tự động.

## Trigger

```
"Build a harness for this project"
"Design an agent team for this domain"
"Set up a harness"
"하네스 구성해줘"  (Korean)
"ハーネスを構成して"  (Japanese)
```

## 6-Phase Workflow

```
1. Domain Analysis        — hiểu requirements
2. Team Architecture      — chọn pattern (xem bên dưới)
3. Agent Definition       — tạo .claude/agents/ files
4. Skill Generation       — tạo .claude/skills/ với Progressive Disclosure
5. Orchestration          — thiết lập inter-agent communication + error handling
6. Validation             — dry-run tests + comparative analysis
```

## 6 Architecture Patterns

```
Pipeline          — sequential dependent tasks (A→B→C)
Fan-out/Fan-in    — parallel independent tasks → consolidate results
Expert Pool       — selective agent invocation theo context
Producer-Reviewer — generation → QA review loop
Supervisor        — central coordinator với dynamic task distribution
Hierarchical      — top-down recursive delegation
```

## Execution Modes

```
Agent Teams (default)
  Dùng: TeamCreate, SendMessage, TaskCreate
  Khi: 2+ agent cần collaborate

Subagents
  Dùng: Agent tool trực tiếp
  Khi: standalone tasks, không cần inter-agent comm
```

## Output Structure

```
.claude/
  agents/
    <agent-name>.md    ← agent definitions
  skills/
    <skill-name>.md    ← generated skills với Progressive Disclosure
```

## So với yamtam harness

Harness này: generate từ domain description (top-down)
yamtam harness: pre-built curated patterns (bottom-up library)

## Source

https://github.com/revfactory/harness · MIT · +2098⭐/week
