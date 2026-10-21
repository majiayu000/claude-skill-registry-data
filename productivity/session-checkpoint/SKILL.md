---
name: session-checkpoint
description: Maintain a compact continuation checkpoint for a long-running assistant project when its configured turn counter is due, a substantial task ends, or the user asks to prepare continuation. Not for unrelated chats or ordinary answers. It does not write or reorganize the memory base, which is personal-secretary-memory.
version: 1.0.2
---

# Session Checkpoint

Maintain a small, factual disk checkpoint for a project that has a local AGENTS.md and a canonical memory area. This does not delete chat, change permissions, archive sessions, or trigger platform context compression.

## When to use

- Use the project's configured counter for substantive user turns; do not count tool updates, subagent messages, or no-information "continue" messages.
- Run at the configured interval, a meaningful milestone, a workstream switch, or an explicit request.
- If no run evidence exists, do not claim that automatic maintenance occurred.

## Workflow

1. Read the current checkpoint and only the task-relevant memory entry. Use the checkpoint format in references/checkpoint-format.md; do not reread the entire archive.
2. Record the current goal, user-confirmed facts, evidence-backed outputs, authorization, unresolved blockers, and 1–3 next actions.
3. Keep user statements, tool checks, suggestions, and unverified claims separate. Do not store secrets, company material, private relationship transcripts, or hidden chain-of-thought.
4. Validate the checkpoint independently, then reset the counter only after the file is updated. Never clear a new turn with an old checkpoint.

## Script

Use scripts/session_checkpoint.py:

    python scripts/session_checkpoint.py --state <local-state.json> tick --turn-key <stable-key>
    python scripts/session_checkpoint.py --state <local-state.json> status
    python scripts/session_checkpoint.py --state <local-state.json> complete --checkpoint <checkpoint.md>

The state is local machine metadata. Do not copy it into a public memory repository.

## Example

The checkpoint file stays small and factual:

```markdown
# checkpoint 2026-10-07

当前任务：整理技能仓库 README
已完成：13 个 skill 的 frontmatter 补 version
未决：Remotion 两个 skill 是否拆得更细
下一步：给没有示例的 skill 补 Example
证据：git log 89f3cd0
```

No chat history, no permissions change, no claim that maintenance ran automatically.
