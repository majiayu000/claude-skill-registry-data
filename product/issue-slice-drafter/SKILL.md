---
name: issue-slice-drafter
description: Draft implementation-ready vertical tracer-bullet slices from a plan, PRD, audit finding, or Goal Contract. Adapted from to-issues; produces draft issue bodies only and never publishes or labels issues without explicit approval.
---

# issue-slice-drafter

Source repo: https://github.com/mattpocock/skills
Source path: skills/engineering/to-issues/SKILL.md
Source commit: b8be62ffacb0118fa3eaa29a0923c87c8c11985c
Local adaptation note: Adapted from an issue-publishing workflow into a read-only drafting skill. It keeps vertical tracer-bullet slicing, HITL/AFK classification, dependencies, and acceptance criteria, while removing automatic issue tracker writes.

## Purpose

Turn an approved plan or clarified goal into draft slices that are independently understandable and verifiable.

Each slice should be a thin vertical tracer bullet through the relevant layers, not a horizontal task such as "build backend" or "write UI".

## Activation

Use when the user asks to break down work into issues, slices, implementation tickets, agent-ready tasks, or a next-action board.

This skill may also be used after a Goal Contract or audit finds a clear implementation backlog, but only as a drafting step.

## Slice Requirements

For each draft slice include:

```text
Title:
Type: HITL or AFK
Parent/source:
What to build:
Acceptance criteria:
Dependencies:
Verification:
Out of scope:
Evidence references:
```

Classification:
- HITL: requires human decision, product judgment, design review, credential access, approval, or high-risk interpretation.
- AFK: can be implemented and verified from available repo context and explicit acceptance criteria.

## Workflow

1. Gather source material from the current conversation, Goal Contract, plan, PRD, audit finding, or referenced file.
2. If repo evidence is needed to avoid vague slices, inspect the relevant code/docs first.
3. Draft the smallest useful set of vertical slices.
4. Mark dependencies explicitly.
5. Include acceptance criteria and verification commands or evidence expectations where known.
6. Ask for approval before any issue tracker action.

## Forbidden actions

- Do not publish GitHub issues, GitLab issues, Linear tickets, labels, comments, PRs, branches, commits, or pushes without explicit approval.
- Do not run `gh issue create` or equivalent issue tracker commands unless the user explicitly approves that exact action.
- Do not apply labels or mark anything ready-for-agent unless the user explicitly approves.
- Do not modify parent issues or source documents.
- Do not edit AGENTS, update CONTEXT.md, create ADR, deploy, git push, or run setup.
- Do not turn a narrow Goal Contract into a broad backlog.

## Stop conditions

Stop when:
- The source goal is not clear enough to slice safely.
- The requested output would require publishing rather than drafting and approval is absent.
- A slice cannot be made independently verifiable.
- The work is single-step and an issue breakdown would add noise.

## Output Pattern

```text
Issue Slice Drafts
Source:
Assumptions:
Slices:
1. <title>
   Type:
   Dependencies:
   Acceptance criteria:
   Verification:
Publishing status: draft only; no issue tracker writes performed
```
