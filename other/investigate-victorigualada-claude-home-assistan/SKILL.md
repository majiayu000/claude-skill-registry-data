---
name: ha:investigate
description: Investigate bugs and errors in Home Assistant — root-cause analysis for unhandled exceptions, setup/config-entry failures, tracebacks, test failures. Use --parallel for deep 4-track investigation.
effort: high
argument-hint: <bug description> [--parallel]
---

# Investigate Bug

Investigate bugs using the Ralph Wiggum approach: check the
obvious, read errors literally.

## Usage

```
/ha:investigate Sensor stays unavailable after a reload
/ha:investigate Setup of integration acme is retrying forever
/ha:investigate Complex reauth bug --parallel
```

## Arguments

`$ARGUMENTS` = Bug description or error message. Add `--parallel`
for deep 4-track investigation.

## Mode Selection

Use **parallel mode** (spawn `deep-bug-investigator`) when:
bug mentions 3+ platforms, spans multiple integrations, is intermittent
or involves concurrency (event-loop blocking, races, coordinator
refresh storms, executor deadlocks), or user says `--parallel`/`deep`.

**Otherwise**: Run the sequential workflow below.

**Avoid confirmatory subagents**: Do NOT spawn parallel subagents
to "verify" findings you already identified in the main context.
If Step 3-4 already identified the root cause with high confidence,
present it directly — don't spend ~80K tokens on 4 subagents to
confirm what's already obvious (confirmed waste: session c135330a).

## Iron Laws

1. **Read the error message literally first** — Most bugs tell you exactly what's wrong; resist the urge to theorize before reading what the traceback is saying
2. **Check the obvious before going deep** — Missing `await`, blocking I/O on the loop, `None` state mismatches, and un-migrated config entries explain 80% of bugs; exhausting the Ralph Wiggum checklist saves hours
3. **Check config-flow / setup errors before UI debugging** — Silent "integration failed to set up" or a form that never creates the entry is almost always a `ConfigEntryNotReady` retry loop or an `AbortFlow`, not the frontend
4. **Consult compound docs before investigating fresh** — A previously solved problem saves the entire investigation cycle; always search `.claude/solutions/` first
5. **NEVER guess at a fix before reproducing** — Reproduce first, then identify root cause, then fix. Skipping steps causes wrong fixes
6. **DO NOT apply a fix without confirming root cause** — Verify your hypothesis with evidence (logs, tests, a temporary `_LOGGER.debug`) before changing code

## Investigation Workflow

### Step 0: Consult Compound Docs

Search `.claude/solutions/` for relevant keywords using Grep.

If matching solution exists, present it and ask: "Apply this
fix, or investigate fresh?"

### Step 0a: Runtime Auto-Capture (dev instance -- PRIMARY when available)

If a dev instance (`hass -c config`, devcontainer, or `script/develop`)
is detected in the project, **start here instead of asking the user
to paste errors**. Auto-capture runtime context:

1. Run the dev instance (or tail `config/home-assistant.log`) to
   capture the latest tracebacks and warnings
2. Parse tracebacks — they point straight at the `.py` file and line;
   correlate with source files
3. For state bugs: `hass.states.get("sensor.foo")` / Developer Tools →
   States, or inspect `entry.runtime_data` at a debugger breakpoint
4. For setup bugs: check the integration status on the Integrations page
   and grep the log for `ConfigEntryNotReady` / `Setup failed` / `Retrying`
5. For UI bugs: grep the frontend for the `ha-*` component tag to find
   its source file and check `render()`/`updated()`

Present pre-populated context to the user:

> **Auto-captured from runtime:**
>
> - Error: {parsed error from log/traceback}
> - Location: {file:line from traceback}
>
> Investigating this. Correct if wrong.

This eliminates copy-pasting errors between the instance and the agent.
**If no dev instance is available**: Fall through to Step 1.

### Step 1: Sanity Checks

Run `mypy homeassistant/components/<domain>/ 2>&1 | head -50`, then
`python3 -m script.hassfest --domain <domain>` (catches manifest/strings
drift and un-migrated config-entry versions before you chase a ghost).

### Step 2: Reproduce

Run `pytest tests/components/<domain>/test_<module>.py -v`. Then read the
last 200 lines of `config/home-assistant.log` (or the dev-instance output)
and search for `Traceback`, `ERROR`, or `Retrying setup` patterns.

### Step 3: Read Error LITERALLY

Parse the traceback — check `${CLAUDE_SKILL_DIR}/references/error-patterns.md`.

### Step 4: Check the Obvious (Ralph Wiggum Checklist)

File saved? Missing `await` on a coroutine? Blocking call in an
`async def` (P4)? State returning a sentinel instead of `None` (P8)?
Unique ID derived from a mutable value (P7)? Config entry needs a
version migration? Dev instance restarted after the edit?

**Integration fails to set up silently?** Check the setup path FIRST
— not the frontend. A connect error swallowed instead of raised as
`ConfigEntryNotReady` shows only "Retrying setup" in the log with no
UI feedback; a config-flow step that hits an unexpected exception
`AbortFlow`s the flow before it can reach `CREATE_ENTRY`.

### Step 5: _LOGGER.debug / breakpoint() / dev instance

### Step 6: Identify Root Cause

Find what's actually happening vs what should happen.

### Step 7: Hand Off

Present root cause + evidence. Then route by fix size:

- Small, contained fix → offer to apply directly or via `/ha:quick`
- Multi-file or risky fix → suggest `/ha:plan {root cause summary}` so
  the fix gets task structure and review
- Non-obvious root cause → after the fix lands, suggest `/ha:compound`

## Autonomous Iteration

Use `/ralph-loop:ralph-loop` for autonomous debugging with
clear completion criteria and `--max-iterations`.

## References

- `${CLAUDE_SKILL_DIR}/references/error-patterns.md` — Common errors and checklist
- `${CLAUDE_SKILL_DIR}/references/investigation-template.md` — Output format
- `${CLAUDE_SKILL_DIR}/references/debug-commands.md` — Debug commands and common fixes
