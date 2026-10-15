---
name: Skillify
description: Turn a repeatable workflow into a reusable local SKILL.md with explicit steps, criteria, and safe defaults.
requires:
  bins: []
  env: []
---

# Skillify

Capture a process that worked well and convert it into a reusable skill file.
Use this to scale team workflows without rewriting instructions every time.

## Use when

- The same workflow appears repeatedly across sessions.
- A process has stable inputs, ordered steps, and clear success criteria.
- You want to convert tacit know-how into a shared `SKILL.md`.

## Do not use when

- The process is one-off, exploratory, or still unstable.
- Key steps are unknown or depend on hidden tribal context.
- The user only wants a quick summary, not a reusable artifact.

## Input contract

- `workflow_name` (required): short name for the new skill.
- `source_scope` (optional): `current_task` (default) or `recent_session`.
- `target_location` (optional): default `skills/<slug>/SKILL.md`.
- `required_args` (optional): known runtime arguments to expose.
- `confirm_before_write` (optional): default `true`.

## Parsing rules (priority order)

1. Structured args override everything.
2. Else infer from user phrasing:
   - "make a skill for X" -> `workflow_name=X`
   - "from this session" -> `source_scope=recent_session`
   - "save under ..." -> `target_location=...`
3. Defaults:
   - `source_scope=current_task`
   - `target_location=skills/<slug>/SKILL.md`
   - `confirm_before_write=true`
4. If `workflow_name` is missing, ask for a concrete name.

## Canonical workflow

1. **Extract process skeleton**
   - Goal, inputs, step sequence, outputs, verification criteria.
2. **Identify constraints**
   - Required tools, risk boundaries, irreversible actions, approvals.
3. **Draft skill frontmatter + body**
   - Include `Use when`, `Do not use when`, input contract, workflow,
     guardrails, and output format.
4. **Review with user**
   - Show full draft and request approval before writing when
     `confirm_before_write=true`.
5. **Write skill artifact**
   - Create directory/file and persist final `SKILL.md`.
6. **Post-write validation**
   - Re-read file and confirm it is syntactically intact and complete.

## Guardrails

- Never overwrite an existing skill silently.
- Avoid over-broad automation promises; keep the skill bounded.
- Prefer minimal required tool surface over wildcard permissions.
- Mark ambiguous steps explicitly instead of guessing.
- Keep language implementation-oriented, not aspirational.

## Output format

Always return:

- `status`: `drafted` | `written` | `needs_user_input`
- `workflow_name`: normalized name
- `target_location`: final path
- `draft_summary`: what the generated skill covers
- `open_questions`: unresolved ambiguities
- `next_action`: required unless `status=written`

## Example

- `workflow_name="release-pr-handoff" source_scope="recent_session" target_location="skills/release-pr-handoff/SKILL.md"`
