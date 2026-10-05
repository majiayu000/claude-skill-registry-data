---
name: session-start
description: Use this skill at the start of every session to load context from Hindsight and orient in the codebase with CGC. Run before any task.
---

### Session Start Protocol

Run these steps at the beginning of every session, before any task work.

#### 1. Load directives

Call `mcp__hindsight__recall` with:
- bank_id: `adam-global`
- query: `durable directives preferences workflow defaults coding standards model strategy`

Then call `mcp__hindsight__recall` again with:
- bank_id: the current derived `project-*` or `workspace-*` bank
- query: `repository conventions architecture commands failures patterns`

Read all results. The global bank carries durable user/workflow rules; the project/workspace bank carries repository-specific context.

#### 2. Load mental models

Call `mcp__hindsight__recall` with:
- bank_id: the current derived `project-*` or `workspace-*` bank
- query: `mental model primitives agents workflows integrations architecture`

Read all results. This is your architectural map.

#### 3. Recall task-specific context (if task is known)

Call `mcp__hindsight__recall` with:
- bank_id: the current derived `project-*` or `workspace-*` bank
- query: `<the specific module, feature, or component you are about to work on>`

#### 4. Orient with CGC

Call `mcp__codegraphcontext__get_repository_stats` to confirm the graph is current.

If the task involves specific files/functions, also call `mcp__codegraphcontext__find_code`
for the target to understand its position in the graph.

#### 5. Acknowledge

State briefly what you loaded — directives active, mental models loaded, current graph
stats — so the user knows the session started warm.

#### Session End: Retain

Before ending the session or after completing a significant task, call
`mcp__hindsight__retain` with the appropriate bank and content covering:
- `adam-global` for durable cross-project preferences or reusable workflow patterns
- the current derived `project-*` or `workspace-*` bank for repository-specific decisions, failures, commands, and architectural insights

Use this format for the content:
```
[type: decision|pattern|failure|insight] <what happened>
Rationale/why: <the reason>
Context: <module or area affected>
```
