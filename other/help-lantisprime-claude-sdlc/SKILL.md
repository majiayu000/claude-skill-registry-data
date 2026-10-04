---
name: help
description: Use this skill when the user runs /help, /help commands, or /help <command-name>. Shows plugin command reference. Read-only — writes nothing, modifies nothing.
config_requirements: []
---

# Help — Plugin Reference

Read-only. Never writes files. Never modifies artifacts. Never invokes other skills.

## Invocation modes

### No args: `/help`

Print a condensed command list — one line each — then a usage tip. Screen budget: ≤ 20 lines total.

```
SDLC Plugin — command reference

  /configure   set up config/tools.json and config/tools.local.json
  /start       guided intake; fix-fast eligibility check; hands off to /plan
  /plan        Phase 1 — classify task, validate scope, estimate effort
  /analyze     Phase 2 — requirements with stable REQ IDs
  /design      Phase 3 — architecture bundle, tech specs, test cases
  /build       Phase 4 — code + unit tests, scoped to plan
  /test        Phase 5 — test execution, defects, UX conformance
  /deploy      Phase 6 — deployment proposal and supervised execution
  /support     Phase 7 — observability wiring (logging, alerts, dashboards)
  /docs        Phase 8 — docs refresh and traceability matrix
  /status      show in-flight task state and pending sign-offs (read-only)
  /review      cross-cutting diff review (correctness + security)
  /fix-fast    compressed path for small bug fixes only (≤2 files, ≤50 LOC)

Run /help <command> for detail on any command.
Run /help commands for the full reference table.
```

### `/help commands`

Print the full command reference table.

Read each file in `commands/` and extract the YAML `description:` field. Format as a markdown table: `Command | Purpose`. Sort by phase order: configure, start, plan, analyze, design, build, test, deploy, support, docs, status, review, fix-fast, token-review.

### `/help <command>`

1. Read `commands/<command>.md`. Extract the YAML `description:` field and the first non-frontmatter paragraph.
2. Read `skills/<command>/SKILL.md` if it exists. Extract the first non-frontmatter paragraph.
3. If neither file exists, print: `No help entry found for /<command>.`
4. Assemble output (≤ 25 lines):

```
/<command> — <YAML description>

<first paragraph from commands/<command>.md or skills/<command>/SKILL.md>

Example:
  /<command> <inferred one-liner>
```

For the Example line: if the commands file contains a code block with a usage example, extract it. Otherwise construct one from the description — typically `/<command> "<short representative phrase>"` for phase commands, or `/<command> --<flag>` for commands with flags.

## What this skill must NOT do

- Do not write or modify any file.
- Do not invoke any other skill.
- Do not invoke any subagent.
- Do not call any hook.
