---
name: report-grimoire-issue
description: Draft and optionally file a GitHub issue for a Grimoire documentation, skill, plugin packaging, Codex harness, or workflow change. Use when a user wants to report a reusable Grimoire problem or improvement upstream.
---

# Report Grimoire Issue

Use this skill when the user wants to report a reusable problem, ambiguity, or improvement for Grimoire itself.

This is an explicit-invocation workflow. In Codex, invoke it as `$report-grimoire-issue`.

The upstream GitHub repository for issue search and posting is `hon454/grimoire`.

## Goal

Turn a fuzzy Grimoire concern into a clean GitHub issue draft, then post it only after the user explicitly approves the exact title and body.

## Scope

Use this skill for Grimoire-side changes:

- skills under `plugins/*/skills/`
- plugin manifests and packaging metadata
- Codex harness behavior
- repository instructions and maintenance policy
- README or install guidance
- validation scripts, publishing checks, or issue templates

Do not use this skill for:

- one-off behavior that belongs only in the user's current project
- private repository prompt wording or domain-specific workflow preferences
- broad roadmap ideas without a concrete skill, plugin, documentation, or packaging change
- issues that would make Grimoire less generally reusable

Return `MODE=local` when the issue is project-local rather than Grimoire-side.

## Interaction Rules

- Ask one question at a time when required information is missing.
- Prefer summarized reproductions over raw transcript excerpts.
- Never include secrets, private repository names, internal URLs, access tokens, customer data, or absolute local paths in the issue.
- Before presenting the final draft, sweep the title and body for private or project-local details.
- Never post an issue without first showing the exact draft and receiving explicit confirmation.
- If GitHub access is unavailable, return `MODE=draft` with the issue text for manual reuse.

## Tool Use

Follow the `using-grimoire`
[GitHub Operations](../using-grimoire/references/github-operations.md) rules.

When using `gh`, target `hon454/grimoire` explicitly.

## Minimum Payload

Capture enough information to fill the Grimoire change-request issue shape:

- issue title in Conventional Commit style, such as `docs(readme): clarify install steps`
- problem: the gap, drift, bug, or ambiguity
- expected behavior: what should be true after the issue is completed
- scope: concrete work that is in scope
- acceptance criteria: observable checkboxes
- affected areas: likely files, directories, manifests, skills, or docs
- non-goals: what the issue must not do

If the user cannot provide every field, continue with an incomplete draft and mark unknowns clearly.

## Duplicate Check

Before presenting a new draft, search open `hon454/grimoire` issues for likely duplicates.

Search using only Grimoire-side terms, such as the affected skill name, plugin name, manifest area, validation command, or documentation topic. Do not search with private project names, usernames, hostnames, local paths, or internal ticket IDs.

If a likely duplicate exists, offer three paths:

- reuse the existing issue
- create a new issue with a short note explaining why it is distinct
- stop without posting

## Draft Shape

Use the current repository issue template when available. Otherwise use this body:

```markdown
## Problem

...

## Expected behavior

...

## Scope

- ...

## Acceptance criteria

- [ ] ...

## Affected areas

- ...

## Non-goals

- ...
```

Title rules:

- Use Conventional Commit style.
- Choose the smallest durable scope affected by the change.
- Use `fix(...)` for incorrect behavior.
- Use `docs(...)` for documentation-only changes.
- Use `feat(...)` for new user-visible skill or workflow capability.
- Use `chore(...)` for packaging, metadata, or validation maintenance that does not change user-facing behavior.

## Posting

After showing the draft, ask for explicit confirmation before posting.

If the user confirms, create the issue in `hon454/grimoire`. Return the issue number and URL.

If posting fails, preserve the exact title and body and explain the failure.

## Output Contract

End every invocation with exactly one outcome token:

- `MODE=local`: the report belongs in the user's current project, not Grimoire
- `MODE=needs-input`: one required detail is missing; ask the next single question
- `MODE=reused`: the user chose to reuse an existing issue; include the URL
- `MODE=draft`: provide the exact title and body, plus any likely duplicates
- `MODE=posted`: the issue was created successfully; include the URL
- `MODE=posted-needs-followup`: the issue was created, but a follow-up action failed
