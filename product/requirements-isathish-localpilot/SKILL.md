---
name: requirements
description: Turn a vague idea or feature request into a concrete, testable requirements spec (goals, user stories, acceptance criteria, non-goals, open questions) before any code is written. USE WHEN the user describes what they want in product terms, says "spec", "requirements", "PRD", "user stories", "what should this do", or the request is too ambiguous to implement safely.
---

# Requirements

Goal: a short spec the user can approve in one read, precise enough that `design` and `implement` need no guessing.

## 1. Understand the ask
- Restate the request in one sentence. If the workspace already has code, skim it first (`list_dir`, `read_file` on README / package manifest / entry points) so the spec fits what exists instead of inventing a parallel world.
- Look for existing specs or docs: `file_search` for `docs/**`, `*.md`, `REQUIREMENTS*`, `SPEC*`, `PRD*`. Extend them rather than duplicating.
- If one decision materially changes the whole approach (platform, data store, auth, offline vs online), ask ONE focused question with `ask_user` and offer 2–3 options. Otherwise choose the simplest sensible assumption and write it down under "Assumptions".

## 2. Write the spec
Create or update `docs/requirements/<feature-slug>.md` (or the project's existing docs location). Keep it under ~120 lines:

```markdown
# <Feature name>
**Status:** draft · **Owner:** <user> · **Date:** <today>

## Problem
Who has the problem, when it happens, why it matters (2–4 sentences).

## Goals
- G1 …  (measurable where possible)
## Non-goals
- Explicitly out of scope so we don't drift.

## Users & stories
- As a <role>, I want <capability> so that <outcome>.

## Acceptance criteria
Given / When / Then — one block per story. Every criterion must be checkable by a test or a manual step.

## Constraints
Platform, performance, security/privacy, accessibility, compatibility, budget.

## Assumptions
Decisions made without asking; the user can override any of them.

## Open questions
Only those that block implementation.

## Rollout / success metric
How we know it worked.
```

## 3. Hand off
- Open the spec for the user with `show_markdown` (path of the file you wrote) and summarise it in 5 bullets in chat.
- Call `manage_todos` with the follow-up plan: "Design <feature>" → "Implement" → "Test" → "Ship" so the user sees the path forward.
- If the user approves, continue with the `design` skill (or `implement` for small changes) in the same session.

## Rules
- Prefer concrete numbers to adjectives ("loads in < 200 ms" not "fast").
- Never silently expand scope; put extras under Non-goals or a "Later" list.
- Keep the user's vocabulary — reuse their terms for features and roles.
