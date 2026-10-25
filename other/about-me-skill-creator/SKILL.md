---
name: about-me-skill-creator
description: Create or refresh a private `about-me` skill containing durable personal context, communication preferences, tooling constraints, and autonomy boundaries. Use when a user asks to create, customize, review, or update their about-me profile or personal agent context.
license: MIT
---

# About-Me Skill Creator

Create a private, user-specific `about-me` skill. The resulting skill helps every
agent in a session calibrate to the person running it; this creator is not itself
their profile.

## Safety Boundaries

- Treat every answer as personal context. Never add credentials, tokens, private keys,
  or information the user would not want read aloud.
- Do not copy repository-specific instructions into the generated skill. Those belong
  in repository files such as `AGENTS.md`.
- Include durable facts only. Omit task-specific details and dated priorities unless
  the user explicitly wants a maintained `Current Focus` section.
- Keep the profile concise: normally 40 to 80 lines. Delete empty or generic sections.

## Wizard

Run this as a conversation, not a questionnaire. Ask one small group of questions at
a time, show the draft as it develops, and let the user skip any section.

### 1. Select a Mode

Ask whether the user wants to:

1. Create a new profile.
2. Review or refresh an existing profile.
3. Draft a profile from material they provide, such as a CV, bio, README, or existing
   instructions.

For a refresh, read the existing profile first and preserve valid, still-durable facts.
Remove anything stale rather than accumulating contradictory entries.

### 2. Select a Destination

Ask where to create the generated skill. Offer these choices:

- `~/.claude/skills/about-me` (default)
- `~/.agents/skills/about-me`
- A custom absolute path

Resolve `~` before writing. State the final `<destination>/SKILL.md` path and ask for
confirmation before replacing any existing file. Create missing parent directories
when the current environment permits it. If the agent cannot write there, provide the
complete generated file and the exact destination instead.

### 3. Gather the Profile

Work through these topics in order. Ask for the reason behind a preference whenever it
would help an agent generalize beyond the immediate example. Challenge vague input:
"be professional" and "write good code" do not calibrate behavior.

1. **Working style:** desired directness, answer length, reasoning depth, disagreement,
   uncertainty, and feedback that has repeatedly missed the mark.
2. **Autonomy:** what an agent can decide, what requires prior approval, and what is
   forbidden without explicit instruction.
3. **Background:** role, fluencies to assume, and areas where extra explanation helps.
4. **Tooling and constraints:** editors and agent clients, stack, platform, budget,
   offline, compliance, approval, or licensing limits.
5. **Hard rules:** a short list of genuinely non-negotiable practices.
6. **Current focus:** optional, dated, and included only when the user intends to
   maintain it.

Ask what is already documented before re-asking questions answered in user-provided
material. A correction the user has had to give twice is especially valuable: turn it
into a specific, durable instruction.

### 4. Draft and Review

Draft a standalone `SKILL.md` using the structure below. Replace all bracketed text
with the user's facts and omit sections that do not add signal.

```markdown
---
name: about-me
description: Durable personal context about the person running this session — their background, tooling, constraints, and preferences for how agents should work with them. Load at the start of every session and whenever calibrating tone, autonomy, technical depth, or workflow.
license: MIT
---

# About Me

## Working Style

- [Specific preference, ideally with its reason.]

## Autonomy

- **Decide without asking:** [Boundary.]
- **Ask first:** [Boundary.]
- **Never without explicit instruction:** [Boundary.]

## Background

- [Role, fluencies, and areas needing explanation.]

## Tooling and Environment

- [Tools, stack, platform, and constraints that change decisions.]

## Current Focus

- [Optional dated focus item.]

## Hard Rules

- [Short non-negotiable rule.]
```

Before writing, ask: "If an agent knew only this file, would it behave noticeably
differently?" Replace generic statements with concrete corrections or remove them.
Confirm the destination and final content, then write `<destination>/SKILL.md`.

## Maintenance

Tell the user that their generated skill is private and should not be committed to a
shared repository. When they give the same correction twice, refresh this profile and
add the missing durable instruction.