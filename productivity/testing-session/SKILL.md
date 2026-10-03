---
name: testing-session
description: Start, inspect, log, and stop isolated project testing sessions in ace-workflows. Use when the operator asks for testing mode, a project-scoped read-only run, a slash-callable testing-session slug, or durable per-session logs under project testing-session artifacts.
---

# Testing Session

Use this skill as the canonical testing-mode entrypoint. A testing session is
the agent actively using a selected project workflow while normal project state
remains read-only. The only allowed writes are the testing-session index and the
selected session folder.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: testing mode is exposed through `$testing-session`.
The state helper is internal support for deterministic session files, not the
operator-facing way to call this skill.

## Required Reading

Before acting:

1. Read root `AGENTS.md`.
2. Read `registry/agents-md.json`.
3. Read `projects/<project-slug>/AGENTS.md`.
4. Read `projects/<project-slug>/project.json`.
5. Read `projects/<project-slug>/tasks/index.json`.
6. Query testing-session summaries through the read-only state helper when the
   project slug is known.

Do not create or continue normal tasks from this skill.

## Invocation Contract

Use one canonical slug with explicit actions:

```text
$testing-session action:start project:<slug> [goal:"..."]
$testing-session action:status session:<session-id> [project:<slug>]
$testing-session action:log session:<session-id> type:<event-type> [...]
$testing-session action:stop session:<session-id> [project:<slug>]
```

The operator surface may expose this as a slash-style entry, but `.agents/skills`
remains the source of truth. Do not add legacy command shims.

Allowed event types:

```text
started, preload_complete, decision, tool_run, artifact_read, finding, blocked, completed
```

## Start

For `action:start`:

1. Require `project:<slug>`.
2. Accept optional `goal:"..."`.
3. Load the project state read-only.
4. Call the helper's start operation defined under `Internal Support`.
5. Report only the session id, status, index path, session path, and next action.
6. Do not recommend tasks, edit tracker JSON, or change normal workflow files.

The script creates:

```text
projects/<project-slug>/artifacts/testing-sessions/index.json
projects/<project-slug>/artifacts/testing-sessions/<session-id>/session.json
projects/<project-slug>/artifacts/testing-sessions/<session-id>/events.jsonl
projects/<project-slug>/artifacts/testing-sessions/<session-id>/notes.md
```

## Log

During a testing session, log each meaningful state transition through the
helper's log operation defined under `Internal Support`.

Use `type:decision`, `type:tool_run`, `type:artifact_read`, `type:finding`,
`type:blocked`, or `type:completed` as the run proceeds. Include `read:` and
`write:` comma-separated path lists when useful.

Log what happened. Do not include recommendations or next-task proposals in the
testing-session state.

Treat every testing-session file as publishable repository state. Record only
workflow behavior, fixture identifiers, repository-relative paths, and redacted
outcomes. Replace user conversation details with neutral fixture language before
logging. Keep PHI, medical or insurance circumstances, financial status,
credentials, contact information, and machine-specific absolute paths out of
goals, summaries, rationales, notes, and path lists. If a useful finding cannot
be expressed safely, report `private-session-detail-withheld` and keep the detail
in chat rather than durable session state.

The helper's sensitive-text patterns are defense in depth, not proof that text
is safe to publish. Do not rely on a passing pattern screen to sanitize free
text. The agent must redact first, use neutral fixtures, and withhold any detail
whose publication safety is uncertain.

## Status

For `action:status`, call the helper's status operation defined under
`Internal Support`.

Return the lightweight session summary only. Do not load the full event stream
unless the user asks for exact evidence.

## Stop

For `action:stop`, call the helper's stop operation defined under `Internal
Support`.

The stop action updates only `session.json`, `events.jsonl`, and the project
testing-session `index.json`.

## Internal Support

Use these deterministic helper calls only after `$testing-session` has selected
the corresponding action:

```bash
node scripts/testing-session-state.mjs action:start project:<slug> [goal:"..."]
node scripts/testing-session-state.mjs action:log session:<session-id> type:tool_run summary:"..." result:ok rationale:"..."
node scripts/testing-session-state.mjs action:status session:<session-id>
node scripts/testing-session-state.mjs action:stop session:<session-id>
```

## Output Boundary

Report captured state, not recommendations. A normal task may later inspect the
testing-session index during preload, but this skill must not create tasks,
continue tasks, edit ordinary project artifacts, or change skills/scripts except
when the selected task explicitly approves implementation work.

Before reporting a session as valid, require the helper to confirm that every
persisted path is repository-relative and every persisted text field passes its
best-effort sensitive-pattern screen. This check supplements, but never replaces,
the redaction and neutral-fixture rule above. Stop with
`testing-session-privacy-rejected` when that gate fails.
