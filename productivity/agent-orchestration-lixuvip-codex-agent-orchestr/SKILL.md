---
name: agent-orchestration
description: Coordinate Codex work across the current task, internal subagents, user-owned tasks, worktrees, handoffs, formal review gates, or recurring automation. Use for delegation, parallel roles, another Codex task, cross-repo work, QA/review handoffs, scheduled follow-up, or task inspection and continuation. Chinese triggers include 子Agent/子进程/子对话, 另一个对话接手, 并行处理, 分给QA, 多仓库收口, 巡检, 持续推进, 定时自动继续, 创建/读取/转交任务.
---

# Agent Orchestration

Use the least coordination that can safely finish the task. Prefer Codex's native task, subagent, thread, worktree, wait, and automation state over custom protocol.

## Default Route

- Keep one-owner work in the current task.
- Use one internal subagent for a bounded independent result that returns to the coordinator. Do not create task boards, callback JSON, heartbeat, leases, or manual status files.
- Create or continue a user-owned thread only when the user wants separate visibility or direct follow-up. Use fork only when completed history must carry over, a worktree for isolated writes, and handoff only to move the same task between Local and Worktree.
- Before delegation, say whether a new sidebar task will appear, where the result returns, and who owns follow-up.
- Choose the best-fit supported reasoning effort. Never set `model` unless the user requests it.

## Load Only When Needed

- Read one language version of `references/COORDINATION.md` only for multiple owners, cross-repo/worktree coordination, or formal QA/review/release gates.
- Read one language version of `references/AUTOMATION.md` only for recurring or delayed work that must survive the current turn.
- Do not load these references for a single bounded subagent. Never load both language versions.

## Core Guardrails

- Give every delegated task one owner and explicit editable/read-only/out-of-scope boundaries. Isolate or serialize overlapping writes.
- Before dispatch, verify the owner has the required read, write, execute, network, browser, and connector capabilities. Keep high-ambiguity planning read-only in the current task; do not assume a child inherits the parent's restrictions.
- Keep delegation flat by default. Use nested delegation only when the user or project explicitly needs it and ownership remains auditable.
- Trust native agent/thread status for lifecycle; inspect the returned result and real evidence before acceptance. Silence is not completion.
- Treat new user input as replace, add, or status. Update or interrupt affected owners, and mark late output from superseded scope as stale.
- Avoid duplicate work: targeted checks during implementation, one final relevant suite on the candidate artifact, and rerun only affected checks after changes unless project rules require more.
- Send progress updates only for meaningful state changes, blockers, decisions, or new evidence; do not narrate unchanged waiting.
- Do not merge, push, deploy, publish, spend, expose secrets, or expand scope without user/project authority.

## Delivery

Before final, map every user request and follow-up to current evidence or an explicit status, then audit active agents, tasks, commands, monitors, and automations so no work is silently orphaned. Report the result, participants, real verification, changed files/branches/commits, remaining risk, and anything intentionally left active. Keep project-specific contracts in the target repository.
