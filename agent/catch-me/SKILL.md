---
name: catch-me
description: Start or refresh domain onboarding for the current project. Generates persona, lexicon, signaling, anti-patterns, first-week plan, and a project-specific playbook for a chosen profession.
disable-model-invocation: true
context: fork
agent: role-onboarder
---

# catch-me

Entry point for the catch-me-if-you-can onboarding flow. The user wants to rapidly pass as — and think like — a practitioner in some domain, so they can direct Claude better on this specific project.

## What happens when this skill fires

1. The `role-onboarder` subagent (bundled at `${CLAUDE_PLUGIN_ROOT}/agents/role-onboarder.md`) takes over in a forked context.
2. It asks up to three short questions (role + flavor, depth, project context) — skipping any already supplied in the invocation args.
3. It generates 6 role artifacts + `meta.json` inline, following `${CLAUDE_PLUGIN_ROOT}/skills/catch-me/templates/role-generation-prompt.md`.
4. It pipes the output through `${CLAUDE_PLUGIN_ROOT}/skills/catch-me/scripts/write_role_files.sh <slug>`, which writes atomically to the user's project at `$(pwd)/.claude/catch-me/roles/<slug>/` and updates `$(pwd)/.claude/catch-me/active-role.json`.
5. It returns a compact cover-story summary (≈15 lines) to the user.

## Invocation patterns

- `/catch-me` — ask everything from scratch.
- `/catch-me <role>` — role given, ask depth + project context.
- `/catch-me "<free-text description>"` — parse what you can from the description, ask the rest.

## Notes

- User input may be in any language, but generated artifacts are always English (v1 scope).
- All role state lives inside the user's current project at `.claude/catch-me/` — nothing is written outside the project. Different projects get independent role state.
- If the requested role already exists under `.claude/catch-me/roles/`, the subagent offers resume / regenerate / replace instead of blindly overwriting.
- After activation, the passive `active-role` skill auto-attaches the persona on role-relevant prompts — no further action needed from the user.
