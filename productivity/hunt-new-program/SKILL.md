---
name: hunt-new-program
description: Initialize a threat hunting program with an environment map, tool inventory, huntmap, and empty execution directories
argument-hint: "[--auto]"
allowed-tools: Read, Bash, Write, Task, AskUserQuestion
---

<context>
**Flags:**
- `--auto` - Use the provided brief as the primary source of truth and ask only for missing critical facts.
</context>

<objective>
Initialize a threat hunting program.

These hunt-native artifacts are the source of truth for the program.

**Creates:**
- `.planning/config.json`
- `.planning/MISSION.md`
- `.planning/HYPOTHESES.md`
- `.planning/SUCCESS_CRITERIA.md`
- `.planning/HUNTMAP.md`
- `.planning/STATE.md`
- `.planning/environment/ENVIRONMENT.md`
- `.planning/QUERIES/`
- `.planning/RECEIPTS/`

Bootstrap should only scaffold the program. Do not seed sample queries, sample receipts, or completed phases.
Unknown environment facts, tools, retention windows, and owners must remain `TBD` unless the operator confirms them.
Confirmed bootstrap facts such as the program name, mode, opened date, and initial phase/status must be filled immediately.

**After this command:** Run `/hunt-map-environment` to capture confirmed facts, or edit `.planning/environment/ENVIRONMENT.md` manually and continue later.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-bootstrap.md
@.github/thrunt-god/templates/config.json
@.github/thrunt-god/templates/mission.md
@.github/thrunt-god/templates/hypotheses.md
@.github/thrunt-god/templates/success-criteria.md
@.github/thrunt-god/templates/hunt-program-huntmap.md
@.github/thrunt-god/templates/hunt-state.md
@.github/thrunt-god/templates/environment-map.md
</execution_context>

<process>
Execute the bootstrap workflow from @.github/thrunt-god/workflows/hunt-bootstrap.md in program mode.
Drive the conversation through `.planning/environment/ENVIRONMENT.md` and the operator toolchain before defining later hunt phases.
Create `.planning/QUERIES/` and `.planning/RECEIPTS/` as empty directories only.
Do not load query-log or receipt templates during bootstrap; those belong to `/hunt-run` after real execution begins.
Default behavior is scaffold-first: write confirmed facts only and leave unknown values as `TBD` instead of inventing sample content.
Create `.planning/config.json` during bootstrap if it does not already exist so runtime, settings, and connector commands are immediately usable.
Never hand-write `.planning/config.json`; use `thrunt-tools config-new-program` and `thrunt-tools config-set` so the file stays valid THRUNT config.
Use built-in connector ids exactly as the runtime registers them, for example `splunk` and `elastic`; do not substitute `elasticsearch`.
When writing connector profiles, use `base_url` for the runtime URL field; do not invent or substitute `endpoint`.
Only configure connector profiles when auth type and secret ref names are confirmed. Never invent placeholder env vars or placeholder secrets for blocked connectors.
When writing `secret_refs`, each confirmed secret must use the THRUNT object shape `{ "type": "env", "value": "ENV_VAR_NAME" }` rather than a raw string.
Keep connector narrative, status notes, and access commentary in `ENVIRONMENT.md`, not in ad hoc config keys.
Do not leave bootstrap-known fields as `TBD` after writing the files.
Write the hunt artifacts directly.
Preserve any existing user-authored content unless the user explicitly wants a reset.
</process>
