---
name: skill-author
description: Draft new Allbert skills from natural-language requirements and submit them through install quarantine.
provenance: external
intents: [task, meta]
metadata:
  trigger-patterns:
    - make me a skill
    - create a skill
    - build a skill
    - draft a skill
allowed-tools:
  - create_skill
  - list_skills
  - read_reference
---

# Skill Author

Use this skill when the operator wants Allbert to create a new skill or refine a skill draft.

## Intake Ritual

Collect enough detail before writing a draft:

1. Name: kebab-case, unique, and no more than 64 characters.
2. Description: a short user-facing summary.
3. Capability summary: what the skill does, required inputs, expected outputs, and any boundaries.
4. Script needs: recommend Python if the operator does not state a preference. Mention Lua only when embedded scripting is enabled and `lua` is allowed by policy.
5. Tool needs: choose the smallest useful `allowed-tools` fence.
6. Optional agent contribution: include only if the skill should expose a delegated agent.

Use `request_input` for missing details, `list_skills` to avoid name collisions, and `read_reference` only for references in already-active skills.

## Drafting Contract

- Always create drafts with `create_skill` and `skip_quarantine: false`.
- Never call `create_skill` with `skip_quarantine: true`; that path is reserved for first-party kernel seeding.
- Drafts must land under `~/.allbert/skills/incoming/<name>/` and carry `provenance: self-authored`.
- Explain that the operator must review and install the draft through the standard skill install preview before it becomes active.
- Keep raw transcript excerpts, secrets, credentials, and private tokens out of the skill body.

## Skill Body Guidance

Write the generated skill in clear operational prose:

- Start with when to use the skill.
- Name any required inputs.
- State safety boundaries and when to ask the operator before acting.
- If scripts are needed, explain what each script does and keep interpreter choices within the configured allowlist.
- Prefer simple markdown references over scripts when a skill only needs reusable instructions.
