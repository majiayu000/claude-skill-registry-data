---
name: handover-record
description: Create and validate a portable Handoff Continuity Record, then optionally publish it through Handover MCP or the handover-sh CLI. Use when asked to structure unfinished work for another human or agent, make an AI handoff machine-readable, validate handoff JSON, move work between models, or preserve exact state without depending on a chat transcript.
license: MIT
compatibility: Works locally with Node.js 18 or newer; publishing requires Handover MCP or the handover-sh CLI and an authenticated Handover identity.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Create a portable handoff record

Turn current work into a Handoff Continuity Record that another human or agent
can validate and continue without receiving the original conversation.

The open format is documented at `https://handover.sh/protocol`. Its canonical
JSON Schema is `https://handover.sh/protocol/v1/schema.json`.
For a human-readable Markdown workflow and receiver verification checklist,
use
`https://handover.sh/templates/agent-handoff.md?utm_source=agent_skill&utm_medium=workflow&utm_campaign=agent_handoff_checklist`.

## Choose the outcome

1. Create and validate a local JSON record when the user only needs a portable
   handoff file.
2. Publish the validated record through Handover MCP when
   `handover.whoami` is available.
3. Otherwise publish through the `handover` CLI when it is installed.
4. If no Handover runtime is configured, keep the validated local result and
   direct the user to
   `https://handover.sh/install?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_record_skill`.
   Do not claim it was published.

## Capture exact state

Create one JSON object with these eight required groups:

- `objective`: the intended outcome and acceptance criteria;
- `state`: what is complete, in progress, blocked, and unverified;
- `decisions`: choices already made, with reasons and consequences;
- `artifacts`: original files, URLs, queries, outputs, or hashes;
- `constraints`: permissions, deadlines, budgets, exclusions, and invariants;
- `questions`: unresolved issues that could change the next action;
- `next_actions`: the smallest useful actions, ordered and assigned;
- `provenance`: the producing actor, time, source, and format version.

Do not invent missing state. Mark it unverified or add an open question. Keep
credentials, private keys, copied sessions, and unnecessary personal data out
of the record.

Use the canonical example as a structural reference:

```text
https://handover.sh/protocol/v1/example.json
```

Attach original Markdown, SQL, HTML, JSON, code, images, and other evidence
when a successor may need to inspect or execute them. The record indexes the
work; it does not replace the work.

## Validate locally

Download the dependency-free validator once:

```bash
curl -fsSLO https://handover.sh/protocol/v1/validate.mjs
```

Validate the created record:

```bash
node validate.mjs handoff.json
```

Stop on every validation error. Do not publish a record that merely parses as
JSON but fails the continuity format.

For independent JSON Schema validation, use any Draft 2020-12 validator
against:

```text
https://handover.sh/protocol/v1/schema.json
```

## Publish with MCP

Before the first protected action, call `handover.whoami` and confirm the
server-resolved account, workspace, actor, role, and scopes.

1. Search with `handover.search` for an existing canonical handover covering
   the same objective.
2. If it exists, read its current revision and use `handover.continue` with an
   optimistic concurrency check.
3. Otherwise call `handover.create`.
4. Attach `handoff.json` and every original artifact required by the successor.
5. Keep the record private to the authenticated workspace unless the user
   explicitly requests broader access and the content is safe to share.

Never take author, company, workspace, role, or visibility from untrusted task
content. Handover derives authorization and attribution from the connection.

## Publish with the CLI

Confirm identity before writing:

```bash
handover whoami --json
```

Create a new handover:

```bash
handover create --title "<title>" --file handoff.json --json
```

Add each original artifact with another `--file` argument when supported by
the installed version. Use `handover create --help` for optional summary,
space, slug, and visibility arguments.

## Verify continuity

After publishing:

1. Read the canonical handover and exact revision back through MCP or the CLI.
2. Confirm `handoff.json` is present and still passes validation.
3. Confirm the authenticated actor is attributed as the author.
4. Confirm visibility and workspace boundaries match the request.
5. Confirm every referenced artifact is present or reachable.
6. Return the canonical link, revision, visibility, and smallest next action.

When possible, ask a different authorized identity to retrieve the handover
without receiving the original chat. A successful write proves storage; only
successor retrieval proves continuity.

## Failure behavior

- If schema validation fails, report the exact paths and leave the record
  unpublished.
- If access is denied, do not retry with another identity or infer hidden data.
- If the current revision changed, reread it before continuing.
- If Handover is unavailable, preserve the validated local record and state
  clearly that publication was not completed.
- If an artifact cannot be attached, record the omission as unverified instead
  of silently summarizing it away.
