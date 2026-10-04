---
name: stakeholder-intake
category: pm
description: Use when a stakeholder sends a request - route it to backlog tasks, an analiz task, or a focused question, decide ask-vs-assume with a Definition of Ready, and ask only what a wrong guess would actually cost
source: github/spec-kit specify/clarify templates (MIT), VoltAgent/awesome-claude-code-subagents backlog-grooming/assumption-mapping (MIT), obra/superpowers brainstorming (MIT), adapted
---
# Stakeholder Intake

## Overview

A stakeholder request is raw intent. Your job is to convert it into the right board action without over-asking or guessing. The two failure modes are asking questions the request already answers (or that a read tool or an analiz task could answer) and creating implementation tasks before the approach is understood.

**Core principle:** Look it up first. Ask only when a wrong guess would cost more than a revision cycle. Otherwise assume, write the assumption down, and move.

## Routing order

1. **Can a read tool answer it?** `list_repositories`, `list_projects`, `list_board_tasks`, `get_board_summary`, `list_team` — look it up, never ask.
2. **A product decision blocks ALL work** (see the ask-vs-assume rule below)? → `ask_user`.
3. **Technical approach unknown?** → an analiz task to system-architect, `todo` (always safe to start, no approval needed).
4. **Otherwise** → create the backlog tasks.
5. **Partially clear?** → create the tasks that are clear now, and ask only about the one blocking unknown — never hold everything hostage to one open question.

## Ask-vs-assume rule

Ask a product question only when **all three** hold:
- (a) the answer changes a Then-clause or the Out-of-scope line of what you're about to create;
- (b) there are several reasonable answers and no safe default;
- (c) a wrong guess costs more than one revision cycle.

Typical cases that clear the bar: who may see or do something, money and pricing, legal or compliance copy, data deletion or retention, brand identity for a new product, an irreversible migration.

Otherwise **assume** — write the assumption under `Assumptions:` in the task `description` and list it in your approval message to the stakeholder, so they can correct it cheaply instead of you asking for it expensively.

## Reasonable defaults — never ask about these

- The existing app's auth and design system.
- Friendly error messages, in the content language.
- Responsive from 360px to 1440px.
- Loading/empty/error states are present.
- The existing app's own conventions for pagination, dates and units.

## Look it up before you ask

Repository/codebase access, which repos or projects exist, board contents and team members are system facts — call `list_repositories`, `list_projects`, `list_board_tasks`, `get_board_summary` or `list_team` first, never the stakeholder.

Registered repositories are already checked out and fully accessible to the team — never ask for repo URLs, git/CMS credentials, or a contact for the dev team; the agent team IS the dev team. If a named product has no repository yet, create a board task to set one up instead of asking.

❌ "Does the team already have access to the Acme repository, or do we need repo/CMS credentials?" — `list_repositories` answers this.
✅ `list_repositories` → repo `acme-web` exists → proceed. Not listed → create a task to register the repo, then ask only the product question that's still open.

**Forbidden question topics** (incident lessons — never ask these, look them up or route them instead):
- Developer skills or personal technical ability.
- DIY builders, or which platform the stakeholder will personally host or use.
- Technical implementation choices — route to an analiz task for the architect.
- Repository or codebase access, repo URLs, git hosting, CMS logins, deploy credentials, or "who is your dev team / who can we contact" — the platform holds the access and the agent team IS the dev team.
- Anything already visible on the board.

Red-flag phrases in a draft question: "do you have access", "repo URL", "credentials", "your dev team" — any of these means you should be calling a tool, not asking.

## Question craft (for ask_user)

- Choice mode with 2–4 concrete options, the recommended one first and labelled "(recommended)".
- A one-sentence "why it matters" in `context`.
- Text mode only for URLs and copy the stakeholder must supply verbatim.
- Never a question about a stylistic preference — draft it yourself (see implementation-task-spec's design brief).
- At most 3 questions per call. After answers arrive, act immediately — never re-ask the same topic.

## Definition of Ready

Before a task leaves `backlog`, it has:
- a concrete persona and outcome in the user story;
- every criterion passing the testability gate (acceptance-criteria-gwt);
- a negative/edge criterion where the feature takes input or checks permission;
- an Out of Scope line;
- a design brief, for UI work;
- `repository`, `project`, `assignee` and `task_type` set;
- its order declared with `blocked_by` / `deploy_depends_on`, not implied in prose;
- its assumptions listed.

## Worked Examples

- "Refresh the Acme website." → `list_repositories` finds `acme-web`; `get_repo_tree` finds an existing design system → no question, write "follow the existing design system", draft the real copy yourself, list assumptions (e.g. "assuming the current page structure stays, only visuals and copy refresh").
- "We need reporting." → Vague, but is it a product or technical unknown? The *scope* of "reporting" is a product decision that blocks all work → `ask_user`: "Which report unblocks you first: (a) tasks-per-project, (b) throughput over time, (c) per-assignee load? (a recommended — most requested type)". Once they pick, the *how* (query? materialized view?) is a technical unknown → analiz task, not more stakeholder questions.

## Common Mistakes

- Asking the stakeholder a technical question the architect/code should answer.
- Creating implementation tasks for an unclear approach instead of an analiz task.
- Asking what a reasonable default already covers.
- Question lists in chat instead of `ask_user`.
- Re-asking something already answered.
- Burying an assumption in `technical_description` instead of the `description`'s `Assumptions:` line.

## Red Flags

- More than 3 questions in one call, or any non-product (technical) question to the stakeholder.
- Implementation tasks created before the approach is understood.
- The question contains "do you have access", "repo URL", "credentials", or "your dev team".
- A 4th question when 3 would do.
