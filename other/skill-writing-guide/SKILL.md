---
name: skill-writing-guide
description: Use when creating, reviewing, or refining Agent Skills for this repository
---

# Skill Writing Guide

## Overview

Use this guide to create Agent Skills that are easy to discover, quick to load, and reliable in repeated use. A skill should teach an agent how to perform a task, not record how one person solved it once.

## When To Use

Use this skill when:

- Creating a new `skills/<name>/SKILL.md`.
- Reviewing a pull request that adds or changes a skill.
- Turning repeated agent behavior into reusable instructions.
- Deciding whether content belongs in a skill, a script, or regular documentation.

Do not use it for one-off project notes, private runbooks, or generic documentation that agents can already infer from standard tools.

## Workflow

1. Define the trigger.
   Write the frontmatter `description` as a `Use when...` sentence that describes the situation where the skill should load.

2. Keep the skill operational.
   Prefer short instructions, decision points, verification steps, and concrete examples. Avoid essays and background stories.

3. Separate heavy material.
   Keep `SKILL.md` focused. Move long API references, generated examples, or reusable scripts into supporting files beside the skill.

4. Add one strong example.
   Use a realistic example that demonstrates the workflow end-to-end. Do not add several shallow examples.

5. Add verification.
   Explain how the agent should prove the skill was used correctly before claiming completion.

6. Run repository validation.
   Run `python3 scripts/validate-skills.py` before opening a pull request.

## Skill Checklist

- Folder name uses lowercase kebab-case.
- `SKILL.md` starts with YAML frontmatter.
- Frontmatter includes `name` and `description`.
- Frontmatter `name` matches the folder name.
- Description starts with `Use when`.
- Body explains workflow and verification.
- Public examples contain no secrets or private data.

## Verification

Before publishing a new or updated skill:

- Run `python3 scripts/validate-skills.py` and confirm zero errors.
- Confirm the frontmatter `name` matches the folder name exactly.
- Confirm the `description` starts with `Use when` and describes the trigger situation.
- Confirm at least one realistic example and one verification section exist in the body.
- Confirm no secrets, internal URLs, or private tool assumptions are in the public skill.

## Common Failures

- **Description summarizes the workflow**: descriptions are for discovery; the body is for process.
- **Skill is too broad**: split unrelated workflows into separate skills.
- **No verification**: the agent cannot know whether the workflow succeeded.
- **Too much copied reference material**: link to public docs or move concise references into supporting files.
- **Private assumptions**: public skills should not depend on private tools unless the trigger says so.

## Example

Bad description:

```yaml
description: Explains how to gather context, write a document, run checks, and open a PR
```

Better description:

```yaml
description: Use when drafting release notes from repository commits and pull requests
```

The better version tells the agent when to load the skill without tempting it to skip the actual instructions.
