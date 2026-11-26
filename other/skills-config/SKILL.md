---
name: skills-config
description: "Creates or validates a repository's .agent-skills.json against the schema, detecting defaults from the repository and the tracker, and reporting any label the tracker is missing. Use when setting up a new repository for the work loop, or when asked to check, fix or generate the skills configuration."
---

# skills-config

Create or validate the per repository skills configuration, never the tracker's labels.

## When to use

- A repository has no `.agent-skills.json` and is about to use the work loop.
- Asked to check, fix or regenerate the configuration.

## Steps

1. No file present: detect sensible values, write a new `.agent-skills.json`.
2. File present: validate it structurally against `agent-skills.schema.json` with `jq`, report
   every key that fails the schema.
3. Detect `pr.base` from the repository's default branch.
4. Detect `verify`: `task check` when the Taskfile has a `check` target. Without one, the
   small targets (`lint:*`, `test:*`, `validate`) joined with `&&`. Without a Taskfile, the
   detected tool commands joined the same way.
5. Detect `release.tool` from `release-me.yaml` or release-please's config file, whichever
   exists. Neither existing leaves `release` unset.
6. Confirm every configured label exists on the tracker with `gh label list`.
7. A label the config names but the tracker lacks: report it as missing for the infrastructure
   repository to create. Never create it here.
8. Explain every key actually set, in one line each, before writing the file.
9. Read `AGENTS.md` for `## Deviations` and report every entry found, next to the explanation
   of the config keys.
10. Include the `$schema` key pointing at the schema's raw URL.
11. Write the file with the file tools, never with shell redirection.

## Guardrails

- Absent key means the schema default applies. Never invent a value the repository does not
  need.
- Labels are infrastructure as code. This skill reports a gap, it never closes one.
- Structural validation only: a value that parses but contradicts repository reality is named,
  not silently kept.
- Deviations are reported, never silently applied and never silently ignored.

## Config

This skill writes and reads `.agent-skills.json` itself; the schema is `agent-skills.schema.json`
at the root of the skills repository.

## References

- Schema: `agent-skills.schema.json`.
- Label defaults: `~/.claude/skills/README.md`.
