---
name: skill-creator
description: Use when creating or updating a reusable skill with task-specific instructions, supporting files and checks.
metadata:
  version: "2.1.0"
  channel: cli
---

# Skill Creator

Create a skill for the workflow the user asked to reuse. For an existing skill,
read its instructions and referenced resources before changing it.

## Choose the scope

Use the user's examples to identify when the skill applies and what result it
should produce. Preserve their chosen tools, destination and permissions. If the
installation location is unclear, inspect the current client's skill settings
or documentation. A phone, desktop and Python runtime use different directories;
do not assume one client's path configures another.

Bundled skills are managed by the app. Put a customized copy under a new name in
the user's skill directory rather than replacing the bundled original. Check
for an existing skill before creating files.

## Write the skill

Use a folder named after the skill with a `SKILL.md` file at its root:

```text
skill-name/
  SKILL.md
  scripts/       optional executable helpers
  references/    optional material read when needed
  assets/        optional files used in the output
```

Start `SKILL.md` with YAML frontmatter containing a lowercase, hyphen-separated
`name` and a short `description` of what it does and when to use it. Keep the name
under 64 characters. Preserve existing supported metadata when editing.

Write the body as instructions for the agent. Include details that change how
the task is done: required inputs, useful tools, fragile steps and observable
completion checks. Use provider-neutral language. Keep the main workflow short;
link supporting references where they are needed, using relative paths.

Create scripts when deterministic execution improves reliability or avoids
repeated work. Include only resources the workflow actually uses. Never embed
credentials, personal records or private service addresses in a shared skill.

## Check the result

Check the frontmatter, resource paths and script inputs. Exercise the workflow
on a representative example and, where a failed check could accept the wrong
result, on a counterexample. Test scripts with temporary fixtures before using
them on the user's files. Report what was checked and any remaining limits.

Loading or creating a skill does not grant permission to send messages, install
packages, change approval settings or take other external actions. Use the
available tools through their existing approval rules and the user's scope.
