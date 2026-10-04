---
name: obsidian-knowledge-net
description: Capture, synthesize, retrieve, update, and audit reusable development knowledge in a user-selected Obsidian vault. Use when documenting incidents, workflow failures, release lessons, troubleshooting patterns, runbooks, prior Codex threads, GitHub investigations, or when maintaining linked knowledge notes through the Obsidian CLI.
---

# Obsidian Knowledge Net

Use this skill to maintain a portable, provenance-aware knowledge graph in a selected Obsidian vault. Use the installed `obsidian-cli` and `obsidian-markdown` skills for Obsidian-specific operations and syntax; keep this skill focused on knowledge modeling, source traceability, lifecycle, approvals, and safety.

## Required operating rules

1. Require an explicit vault path from the user or current task. Never choose a vault implicitly.
2. Resolve the path to a registered Obsidian vault before reading or writing.
3. Require the Obsidian desktop app to already be running. Do not launch, restart, or switch vaults implicitly.
4. Keep normal note operations CLI-first. Use the bundled scripts for preflight, hashing, and broad validation.
5. Never modify `.obsidian/` during normal knowledge work.
6. Read and hash a file before updating it; re-read and compare immediately before writing. Abort on a mismatch.
7. Do not delete, rename, move, or broadly rewrite notes without explicit confirmation.
8. Preserve source links and concise evidence. Do not copy complete transcripts unless explicitly requested.
9. Treat claims from unverified conversation context as `provisional`; promote them only when evidence supports the conclusion.
10. After writes, read back changed notes and run the link/metadata audit.

Read the relevant reference before acting:

- Note fields and folders: [references/schema.md](references/schema.md)
- Mode workflows: [references/workflows.md](references/workflows.md)
- Safety and conflict handling: [references/safety.md](references/safety.md)

## Operation modes

Classify the request into one of these modes, while keeping the user-facing interaction conversational:

- **retrieve** — Search the selected vault and answer with linked notes and provenance.
- **capture** — Convert an event, incident, thread, issue, or workflow run into an event note.
- **synthesize** — Extract reusable patterns and runbooks from event notes.
- **update** — Make a targeted, conflict-safe change to an existing knowledge note.
- **audit** — Inspect links, metadata, IDs, lifecycle status, indexes, and graph health.

## Standard workflow

### Preflight

Run the preflight helper before any vault operation:

```bash
python3 scripts/vault_preflight.py --vault-path "/absolute/path/to/vault"
```

It must confirm that Obsidian is running, the path maps to exactly one registered vault, and the target is not `.obsidian/`. Treat Obsidian Sync status as informational only; iCloud synchronization is outside Obsidian Sync.

### Retrieve

Use the Obsidian CLI for scoped search, context, backlinks, properties, and note reads. Prefer the `Knowledge/` namespace unless the user asks for broader vault context. Return note links such as `[[Knowledge/Patterns/Cross-platform release diagnosis]]` and identify the source notes supporting the answer.

### Capture and synthesize

First produce a dry-run containing:

- proposed note paths and titles;
- note types and stable IDs;
- lifecycle status and confidence;
- source links and evidence;
- internal links to create;
- existing notes to update;
- unresolved or ambiguous claims.

Only write after the user explicitly requests the capture/update or confirms the dry-run. Create notes with `obsidian create ... silent`; do not overwrite an existing stable ID.

Use event notes for chronological facts, pattern notes for reusable lessons, and runbook notes for repeatable procedures. Link patterns and runbooks back to the event evidence that supports them.

### Update, rename, and repair

Before updating a note, capture its content hash with `scripts/conflict_check.py`. Re-read and compare the hash immediately before the CLI write. If it differs, stop and report a conflict.

Use Obsidian CLI `rename` or `move` only after confirmation and only after verifying that automatic internal-link updates are enabled in the target vault. For broad link repairs, generate a report first and request confirmation.

### Audit

Run:

```bash
python3 scripts/link_audit.py --vault-path "/absolute/path/to/vault" --scope Knowledge
```

Combine the helper report with CLI `unresolved`, `orphans`, and `deadends` results. Report duplicate IDs, malformed frontmatter, missing internal targets, orphaned knowledge notes, stale hub references, and lifecycle inconsistencies. Do not repair automatically during an audit.

## Write report

Every mutating operation must report:

- selected vault path and resolved vault name;
- operation mode;
- files read, created, modified, skipped, or conflicted;
- links added or proposed;
- sources and evidence used;
- audit results after writing;
- follow-up actions requiring confirmation.

Use `obsidian-bases` only when the selected vault supports Bases and the user requests a structured dashboard. Use `defuddle` for clean external web extraction when available. Use `json-canvas` only for an explicitly requested visual map; Markdown links remain canonical.
