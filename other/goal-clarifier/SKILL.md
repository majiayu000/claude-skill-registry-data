---
name: goal-clarifier
description: Minimal ambiguity-resolution interview for blocked engineering tasks. Adapted from grill-with-docs; use when Goal, Constraints, or Success Criteria are unclear enough to block safe execution, while preserving lifecycle/governance control.
---

# goal-clarifier

Source repo: https://github.com/mattpocock/skills
Source path: skills/engineering/grill-with-docs/SKILL.md
Source commit: b8be62ffacb0118fa3eaa29a0923c87c8c11985c
Local adaptation note: Adapted from an open-ended grilling and documentation-updating skill into a narrow clarification loop. It asks only the minimum questions needed to unblock execution and forbids inline documentation writes without explicit approval.

## Purpose

Clarify the smallest set of facts needed to proceed safely:
- Goal: what becomes true when the task is done.
- Constraints: what must not change or be touched.
- Success Criteria: what evidence proves the task is complete.

This skill is subordinate to AGENTS.md, project-lifecycle, repo-preflight, strict audit rules, and explicit user instructions.

## Activation

Use only when ambiguity blocks execution or would make assumptions risky.

Before asking the user, inspect available repo evidence if it can answer the question cheaply:
- AGENTS.md or equivalent local instructions.
- Existing docs, tests, code, prior artifacts, issue text, or user-provided files.
- Current worktree state when relevant.

Ask one question at a time. Include the recommended answer when useful, but do not ask for confirmation if repo evidence already resolves the ambiguity.

## Clarification Loop

1. State the blocking ambiguity in one sentence.
2. Check whether repo evidence can answer it.
3. If evidence answers it, proceed with the evidence and cite the path or command.
4. If evidence cannot answer it, ask exactly one question.
5. Stop after the minimum questions required to clarify Goal, Constraints, and Success Criteria.

## Forbidden actions

- Do not run a broad interview when execution is already safe.
- Do not update CONTEXT.md unless explicit EXECUTE approval is given.
- Do not create ADR unless explicit EXECUTE approval is given.
- Do not edit AGENTS, CLAUDE.md, docs/agents, issue trackers, labels, commits, PRs, or comments.
- Do not publish, deploy, git push, or run setup.
- Do not use this skill to replace the Goal Contract or lifecycle gates.

## Stop conditions

Stop when:
- Goal, Constraints, and Success Criteria are clear enough to proceed.
- The next question would be nice-to-have rather than blocking.
- The user says proceed, no more questions, audit only, or no planning.
- Local instructions make the next step read-only or execution-blocked.

## Output Pattern

```text
Goal Clarifier
Blocking ambiguity: <one sentence>
Evidence checked: <paths/commands or none>
Question asked: <one question or none>
Resolved working assumption: <if evidence supports it>
Stop condition: <why clarification ended>
```
