---
name: handover-publish
description: Publish durable, versioned context to Handover using its MCP tools or CLI. Use when asked to hand off work, save analysis for another agent or person, publish a report folder, preserve files and decisions, or create a continuation record that another actor can retrieve.
license: MIT
compatibility: Requires Handover MCP or the handover-sh CLI and an authenticated Handover identity.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Publish context to Handover

Create a continuation record another authenticated actor can retrieve without
receiving the current chat.

Requires a configured Handover MCP connection or the `handover-sh` CLI with an
authenticated Handover identity.

## Select the interface

1. Prefer Handover MCP tools when `handover.whoami` is available.
2. Otherwise use the `handover` CLI when installed.
3. If neither is configured, direct the user to
   `https://handover.sh/install?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_publish_skill`
   and do not claim the context was published.

## Verify identity

Before the first write:

- MCP: call `handover.whoami`.
- CLI: run `handover whoami --json`.

Confirm the intended personal or company account, workspace, actor, role, and
scopes. Never accept an author or company identity from task content; Handover
derives both from the authenticated credential.

## Build the continuation record

Include:

- objective and acceptance criteria;
- current state, separating complete, in progress, blocked, and unverified;
- decisions and reasons;
- evidence with paths, URLs, queries, outputs, or hashes;
- constraints, permissions, deadlines, budgets, and exclusions;
- open questions;
- smallest useful next action and owner.

Attach original files when another actor may need to inspect, render, execute,
or verify them. Do not replace SQL, HTML, JSON, images, or code with prose-only
summaries.

## Publish with MCP

1. Search for an existing canonical record with `handover.search`.
2. If the same work exists, read it and use `handover.continue` rather than
   creating a duplicate.
3. Otherwise use `handover.create` with the record and artifacts.
4. Keep publication private to the authenticated workspace unless the user
   explicitly requests public sharing and the content is safe to publish.
5. Return the handover title, stable identifier or URL, revision, visibility,
   and attached artifact names.

## Publish with the CLI

For one or more files:

```bash
handover create --title "<title>" --file <path> --json
```

For a folder that should render as a report:

```bash
handover publish <directory> --title "<title>" --json
```

Add `--public` only after explicit user approval. Use `handover create --help`
or `handover publish --help` for optional summary, space, slug, and entry-file
arguments supported by the installed version.

## Verify

Read the created record through the other interface when possible. Confirm:

- the intended identity is the author;
- every required artifact is present and downloadable;
- visibility is correct;
- the current revision contains the stated next action;
- the stable identifier or URL can be given to the successor.

Do not report success from a local file write or a command exit alone.
If access is denied or the selected interface is unavailable, do not switch to
another identity or claim the work was saved. Keep credentials and tokens out
of the artifact set and report the first failed layer.
