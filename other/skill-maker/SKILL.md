---
name: skill-maker
description: Use this when creating, improving, auditing, running retrospectives for, or updating Codex Skills. This Skill turns a repeatable task into a compact reusable SKILL.md and keeps Skill changes based only on verified lessons.
---

# Skill Maker

## Purpose

Create and improve reusable Codex Skills.

A good Skill helps future Codex sessions perform a similar task with less repeated explanation, fewer repeated mistakes, and clearer success criteria.

A Skill is not a long SOP. It should not over-specify every mechanical step unless those steps are deterministic and easy to get wrong. Prefer describing what “good” means, what to avoid, what tools/resources are reliable, and how to verify the result.

## When to create a new Skill

Create a new Skill when the task:

- is likely to happen again;
- has reusable evaluation criteria;
- depends on user/team/client preferences;
- requires a repeated workflow;
- requires stable tools, commands, APIs, folders, credentials, file formats, or connectors;
- produced lessons that future Codex sessions should not rediscover.

Do not create a Skill for a small one-off task unless the user explicitly asks.

## Before creating a Skill

First inspect the task and answer:

1. What type of future task should trigger this Skill?
2. What final output should the Skill help produce?
3. What does a successful output look like?
4. What inputs does the user usually provide?
5. What mistakes should future Codex avoid?
6. What tools, paths, commands, references, examples, or templates are stable enough to mention?
7. How should future Codex verify the result?

If the answers are not fully known, create a minimal Skill and mark uncertain areas as “to be refined after use.”

## Audit mode

Use audit mode when the user asks to inspect whether a Skill setup is discoverable, valid, concise, and safe to maintain.

Audit mode is read-only unless the user explicitly authorizes repair mode. Check only task-relevant files and report pass items, risks, files to move or clean up, and minimal repair steps. Do not update a Skill during audit mode.

## Retrospective mode

Use retrospective mode after a Skill-worthy task to identify reusable lessons that were actually verified in the run.

Retrospective mode can propose Skill updates, but it should not change files unless the task or user explicitly permits update mode. Do not preserve speculation.

## Update mode

Use update mode only when file changes are authorized or the task requires maintaining a Skill.

Read the current Skill first, preserve useful guidance, and add concise verified lessons. For personal Windows Skills, use `%USERPROFILE%\.agents\skills\<name>\SKILL.md`; for project-specific Skills, use `.agents\skills\<name>\SKILL.md`.

## Required Skill format

Create Skills in this structure:

```md
---
name: <kebab-case-skill-name>
description: <Clear trigger description. Start with the main use case. Say when to use and, if helpful, when not to use.>
---

# <Human-readable Skill Name>

## When to use

Describe the task patterns that should trigger this Skill.

## Desired outcome

Describe the final artifact or end state.

## Success criteria

List the conditions that define a good result.

## Inputs and context to collect

List the information Codex should look for or ask about if missing.

## Workflow guidance

Describe the approach. Keep this at the level of judgment, strategy, and sequencing. Do not over-prescribe obvious micro-steps.

## Known pitfalls

Include only pitfalls that were actually observed, strongly implied by user feedback, or verified during execution. Do not speculate.

## Tools and deterministic operations

Document stable tools, commands, file paths, APIs, connectors, scripts, templates, or references.

For each tool, include:
- what it is for;
- when to use it;
- exact command or access path if known;
- prerequisites or environment notes;
- common failure modes if known.

## Verification

Explain how Codex should check whether the result is correct.

## Update policy

After each use, update this Skill only when there is a reusable lesson:
- add newly verified pitfalls;
- refine success criteria;
- add stable commands/tools/templates;
- remove stale or wrong guidance;
- keep the file concise.
```

## Creating a new task Skill

When creating a task Skill:

1. Choose a short kebab-case name.
2. Prefer the project location `.agents/skills/<name>/SKILL.md` for project-specific knowledge.
3. Prefer the user location `%USERPROFILE%\.agents\skills\<name>\SKILL.md` for personal cross-project knowledge.
4. Write a minimal but usable first version before executing the task.
5. Execute the user's task according to the new Skill.
6. After execution, update the Skill with lessons learned.

## Updating an existing Skill

When updating a Skill:

1. Read the current Skill first.
2. Preserve useful existing guidance.
3. Add only reusable, verified knowledge.
4. Do not add generic advice that any capable model already knows.
5. Prefer replacing vague rules with concrete success criteria or known pitfalls.
6. Keep descriptions concise because Codex may use them for skill selection.
7. Summarize the changes made.

## Retrospective template

At the end of a Skill-worthy task, answer privately first, then update the Skill if needed:

- Did the Skill help?
- What was missing from the Skill?
- What mistake, delay, or ambiguity happened?
- What user preference became clear?
- What command, file path, tool, or format was verified?
- What should future Codex do differently?
- Is this lesson general enough to preserve?

Only update the Skill when the answer contains reusable knowledge.

## Verification

Before finishing a Skill creation or update:

- confirm `SKILL.md` has valid frontmatter with `name` and `description`;
- confirm Markdown code fences are balanced;
- confirm any template code block is closed before adding more Skill guidance;
- confirm the final file is concise and trigger-focused.
