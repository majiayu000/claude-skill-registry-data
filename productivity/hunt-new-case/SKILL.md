---
name: hunt-new-case
description: Initialize a threat hunting case from a signal, detection, intel lead, or analyst suspicion
argument-hint: "[--auto] [--pack <id>]"
allowed-tools: Read, Bash, Write, Task, AskUserQuestion
---

<context>
**Flags:**
- `--auto` - Use the supplied signal brief as the starting point and ask only for missing critical facts.
- `--pack <id>` - Bootstrap the case from a built-in or local hunt pack. Use `thrunt-tools pack bootstrap <id>` to inspect the generated mission, hypothesis, and phase seed content.
</context>

<objective>
Initialize a threat hunting case.

These hunt-native artifacts are the source of truth for the case.

**Creates:**
- `.planning/config.json`
- `.planning/MISSION.md`
- `.planning/HYPOTHESES.md`
- `.planning/SUCCESS_CRITERIA.md`
- `.planning/HUNTMAP.md`
- `.planning/STATE.md`
- `.planning/QUERIES/`
- `.planning/RECEIPTS/`

Bootstrap should only scaffold the case. Do not seed sample queries, sample receipts, or completed phases.
Unknown scope details, data sources, operators, and constraints must remain `TBD` unless the operator confirms them.
Confirmed bootstrap facts such as the case name, mode, opened date, and initial phase/status must be filled immediately.

**After this command:** Run `/hunt-shape-hypothesis` or `/hunt-plan 1`.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-bootstrap.md
@.github/thrunt-god/templates/config.json
@.github/thrunt-god/templates/mission.md
@.github/thrunt-god/templates/hypotheses.md
@.github/thrunt-god/templates/success-criteria.md
@.github/thrunt-god/templates/huntmap.md
@.github/thrunt-god/templates/hunt-state.md
</execution_context>

<process>
Execute the bootstrap workflow from @.github/thrunt-god/workflows/hunt-bootstrap.md in case mode.
Focus on turning the input signal into a scoped case with explicit hypotheses, data sources, and evidence requirements.
When `--pack <id>` is present, use the pack bootstrap output as the default case skeleton and ask only for the missing pack parameters or signal-specific overrides.
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
</process>
