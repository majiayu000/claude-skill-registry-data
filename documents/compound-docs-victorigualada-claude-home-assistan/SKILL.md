---
name: compound-docs
description: "Searchable Home Assistant solution documentation system with YAML frontmatter — coordinator, config flow, entity, and frontend fixes. Builds institutional knowledge from solved problems. Use when consulting past solutions before investigating new issues."
effort: low
user-invocable: false
---

# Compound Docs — Institutional Knowledge Base

Searchable, categorized solution documentation that makes each
debugging session easier than the last.

## Directory Structure

```
.claude/solutions/
├── coordinator-issues/
├── lit-issues/
├── service-action-issues/
├── asyncio-issues/
├── security-issues/
├── testing-issues/
├── integration-issues/
├── pr-process-issues/
├── performance-issues/
└── build-issues/
```

## Iron Laws

1. **ALWAYS search solutions before investigating** — Check
   `.claude/solutions/` for existing fixes before debugging
2. **YAML frontmatter is MANDATORY** — Every solution needs
   validated metadata per `${CLAUDE_SKILL_DIR}/references/schema.md`
3. **One problem per file** — Never combine multiple solutions
4. **Include prevention** — Every solution documents how to
   prevent recurrence

## Solution File Format

```markdown
---
module: "shelly.coordinator"
date: "2026-07-01"
problem_type: asyncio_issue
component: coordinator_update
symptoms:
  - "Detected blocking call to open inside the event loop by integration 'shelly'"
root_cause: blocking_call_not_offloaded_to_executor
severity: medium
tags: [blocking-io, executor, event-loop]
---

# Blocking Connect Call in Shelly Coordinator Update

## Symptoms
HA logs "Detected blocking call to open inside the event loop" on
every coordinator refresh; the event loop stalls for ~2s per update.

## Root Cause
The library's `connect()` does blocking socket I/O and was awaited
directly in `_async_update_data` instead of being offloaded.

## Solution
Wrapped the call: `await hass.async_add_executor_job(client.connect)`.

## Prevention
Use blocking-io-check skill before shipping coordinator update paths.
```

## Searching Solutions

Use Grep to search `.claude/solutions/` by symptom (e.g., `blocking call`), by tag (e.g., `tags:.*executor`), or by component (e.g., `component: coordinator`).

## Integration

- `/ha:compound` creates solution docs here
- `/ha:investigate` searches here before debugging
- `/ha:plan` consults for known risks
- `learn-from-fix` feeds into this system

## References

- `${CLAUDE_SKILL_DIR}/references/schema.md` — YAML frontmatter validation schema
- `${CLAUDE_SKILL_DIR}/references/resolution-template.md` — Full solution template
