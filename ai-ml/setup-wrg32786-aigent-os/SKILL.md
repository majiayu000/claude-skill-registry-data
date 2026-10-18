---
name: setup
description: Configure or reconfigure aigent-OS identity, priorities, authority, projects, people, and decision logic
trigger: /setup
---

# aigent-OS setup and reconfiguration

`/start` owns the day-one onboarding arc. `/setup` is the deeper configuration flow and may also be used later to revise one section.

## Entry behavior

Read `.aigent/state.json` first.

- If state is missing or not `ready`, route through `/start` unless the operator explicitly requested advanced setup.
- If state is `ready`, ask which configuration area needs revision rather than replaying the entire interview.
- Never detect setup state by searching for placeholder prose in a Markdown file.

Before writing, set `status: setup-in-progress` while preserving any prior `completedAt`. On interruption, the next `/start` or `/setup` should resume from the last durably completed section.

## Interview

Ask one question at a time and write each completed section immediately.

### 1. Identity

Ask for the operator's role, responsibilities, preferred collaboration style, and risk posture. Update `system/00_identity.md` without replacing framework-owned doctrine.

### 2. Priorities

Ask for the top two or three active priorities, the most urgent outcome, operating mode, and blockers. Update `vault/memory/ACTIVE_PRIORITIES.md`.

### 3. Authority boundaries

Ask what the AI may handle autonomously, what needs confirmation, what is human-only, and whether spending has an escalation threshold. Update `system/12_authority_matrix.md`.

### 4. Decision logic

Ask what makes the operator accept or reject opportunities, their active-work limit, and their most common time trap. Update `system/14_decision_framework.md`.

### 5. Projects and people

For each active project, capture purpose, current state, priority, next action, and relevant people. Create or update notes under `vault/projects/` and `vault/people/`, then connect them from active priorities with wikilinks.

### 6. Specialist agents

Ask whether any specialized agents are useful now. For each accepted agent, capture name, scope, tools, model tier, escalation boundary, and success criteria. Store the definition in `vault/agents/` with valid `name:` and `tools:` frontmatter so the installer can register it in `.claude/agents/`.

## Completion

After all requested sections are durably written:

1. Summarize exactly what changed.
2. Append an idempotent setup entry to `vault/memory/SESSION_LOG.md`.
3. Set `.aigent/state.json` to:

```json
{
  "schemaVersion": 1,
  "status": "ready",
  "completedAt": "<ISO-8601 timestamp>"
}
```

4. Write `.aigent/first-run-done` for compatibility with older installs.
5. Teach or remind the operator of `/open`, normal work, and `/close`.

Do not mark the installation ready when required writes failed.

## Rules

- One section at a time.
- Adapt to information already supplied.
- Mirror the operator's language without inventing details.
- Preserve user-authored content and make precise edits.
- Sections may be deferred explicitly.
- Reconfiguration must not erase unrelated state.
