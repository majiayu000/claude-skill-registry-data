---
name: icaire-team-onboarding
description: Onboard an ICAIRE team member into the existing shared ICAIRE operating context, update their profile page, and capture first tasks. Use when a newly configured ICAIRE member has completed MCP setup, when a teammate needs first-time ICAIRE/Codex onboarding, or when the installer reaches the post-verification onboarding step.
---

# ICAIRE Team Onboarding

Onboard the authenticated ICAIRE member after the workbench and ICAIRE Cortex
MCP are installed. ICAIRE Cortex is the remote source of truth for this
workflow. Do not install or invoke a BigBrain CLI, create a local brain, or
initialize a new brain.

## Contract

- Use ICAIRE Cortex MCP, not local TODO files.
- Start with `me`. If the authenticated user is not an active member, stop and
  explain that ICAIRE membership must be configured before onboarding can write
  a profile or tasks.
- Read `filing_rules` before writing.
- Use `member.person_slug` from `me` as the profile page to update.
- Use ICAIRE MCP `read`, `create_page`, or `update_page` for the member profile
  page. Use `tasks/create` for task pages. Prefer slash tool names; use
  underscore aliases only if needed.
- Ask one onboarding question at a time and wait for each answer.
- Do not mention "ICAIRE brain" in the onboarding questions.
- Do not invent facts. Preserve uncertainty as notes, open questions, or
  underspecified tasks.
- Create task pages only when the member provides enough detail for a useful
  task.
- Use the workbench `README.md` catalog to match the member's role and expected
  workflows to role-specific skill sections.
- Do not install role-specific skills before showing the matched sections and
  getting explicit confirmation from the member.

## Workflow

1. Call `me` and confirm `member.person_slug` exists.
2. Call `filing_rules`.
3. Use ICAIRE MCP `read` on the member's `people/*` page when it exists. If it
   does not exist, prepare to create it with `create_page` from the interview
   answers.
4. Ask these questions exactly, one at a time:
   1. What's your full name and preferred name?
   2. What's your role at ICAIRE?
   3. Who do you report to?
   4. What's your background?
   5. Are there any tasks you know that you need to work on first? Tell me as
      much as you can so I can track these and help you complete them.
5. Optionally ask this follow-up only when the prior answers show a setup or
   access gap: `Anything missing or blocked in your setup?`
6. Update or create the member profile page through ICAIRE MCP `update_page` or
   `create_page` with concise, durable sections for:
   - role
   - reporting line
   - background
   - expertise, only when volunteered
   - current responsibilities or workstreams
   - collaboration or setup notes, only when volunteered
7. For concrete task answers, create ICAIRE task pages assigned to `me`.
   - Set `status: open`.
   - Set `readiness: ready` only when the task has a clear action and enough
     context for a fresh agent to start.
   - Set `readiness: underspecified` when important details are missing.
   - Link the task to the member profile page through `source` when useful.
8. If the member names another teammate while describing reporting lines,
   collaborators, or task owners, resolve that name against active ICAIRE
   members before assigning tasks. Ask for clarification when ambiguous and do
   not assign work to non-members.
9. Read back the updated profile and any created task pages, or otherwise
   verify the writes with the available ICAIRE MCP tools.
10. After the profile and task writes are verified, show the member the matched
    role-specific README headings and skill names. Explain the match briefly
    and ask which sections to install.
11. After explicit confirmation, invoke `icaire-skill-catalog` or the
    workbench `scripts/install_icaire_skills.py` installer with the exact
    confirmed README headings. Verify every installed skill resolves into the
    workbench checkout.

## Output

Report concisely:

- questions completed
- profile page created or updated
- tasks created, including whether each is ready or underspecified
- role-specific skills recommended and installed after confirmation
- setup blockers or unresolved questions
- verification read-back result

End by telling the member they can ask for `ICAIRE: What's Next`, `ICAIRE:
Status`, or the skill catalog when they want to continue.

## Guardrails

- Do not ask a long questionnaire or add extra onboarding questions by default.
- Do not expose private implementation instructions as public website or
  external-facing copy.
- Do not show other members' tasks unless the member explicitly asks and has the
  right context.
- Do not write secrets, credentials, OAuth tokens, or private keys into ICAIRE.
- Do not create tasks for vague goals without preserving the missing
  information as an open question.
