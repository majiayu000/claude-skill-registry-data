---
name: video-to-skill
description: >
  Watch a tutorial or demo video and generate a Claude Code skill from it.
  Activated when user says "create a skill from this video" or similar.
user-invocable: true
---

# Video to Skill

Watch a tutorial or demo video and generate a Claude Code skill from it.

## When To Use

- User says "create a skill from this", "make this into a skill", "turn this into a command"
- User shares a tutorial video and wants to automate the workflow shown

## Workflow

1. Run `/eyeroll:watch <source> --context "create a skill from this"`
2. Check the report metadata before generating anything:
   - Continue when `intent` is tutorial/how-to, feature demo, or a workflow walkthrough
   - Pause and summarize instead when the video is a bug report, question, docs lookup, or general notes
3. From the report, identify:
   - What workflow/process is demonstrated
   - What commands/tools are used
   - What inputs and outputs
   - Trigger phrases (when should this skill activate)
4. Check if `skills/` directory exists, read existing skills for patterns
5. Generate SKILL.md using the template below
6. Ask the user to review before finalizing

## SKILL.md Template

```markdown
---
name: {skill-name}
description: >
  {What this skill does and when to use it.}
---

# {Skill Name}

{One-liner description.}

## When To Use This Skill

{Bullet list of trigger conditions.}

## Workflow

{Numbered steps the agent should follow.}

## Example Interactions

{2-3 realistic examples.}

## Rules

{Guardrails and constraints.}
```

## Rules

- Always run `/eyeroll:watch` first — don't generate a skill without understanding the video
- Do not force every video into a skill; use the report intent and handoff recommendation to decide
- Keep SKILL.md under 500 lines
- The generated skill should be self-contained
- Ask the user to review before finalizing
