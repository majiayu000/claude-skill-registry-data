---
name: sync-md-json
description: >
  Bidirectional sync between .json (authoritative source of truth) and .md (human-readable derivative) files — command-triggered, always writes fresh data from the source to the target. Trigger when: the user says "sync index", "sync md-json", "sync to md", or "sync to json"; a project status update needs to be committed to both formats; the user asks to "make sure index.json and index.md are in sync"; a new project was added or archived and both files need to reflect it. Key capabilities: JSON is always the authoritative source (never merge-and-keep-both); preserves version and updated timestamp on every JSON write; preserves non-data sections in the markdown (footnotes, section headers); supports both directions with clear, safe overwrite semantics; enforces ISO date format. Also for: recovering from a corrupted markdown view of the data, auditing what changed between sync cycles by diffing the JSON. Ideal for: project portfolio indexes, any machine-readable + human-readable dual-format records that need to stay in sync without manual maintenance.
---

# Sync MD-JSON

Syncs data between `.json` (source of truth) and `.md` (human-readable) files.
JSON is primary. On command, the target format overwrites with data from source.

## When Invoked

- User says "sync index" / "sync md-json" / "sync to md" / "sync to json"
- On-demand project status requested (sync status to JSON for compact storage)
- Any time you need to ensure both formats are in sync

## Sync Direction

**JSON → MD (default, most common):**
1. Read the `.json` file
2. Generate a readable Markdown table from it
3. Overwrite the `.md` file with the new content
4. Preserve any non-data sections (e.g., section headers, footnotes)

**MD → JSON (use when JSON is stale):**
1. Parse the Markdown table into structured data
2. Overwrite the `.json` file with the new data
3. Preserve schema fields not present in the Markdown

## Index File Conventions

Source of truth: `{project-root}/projects/index.json`
Derived: `{project-root}/projects/index.md`

Schema:
```json
{
  "version": 1,
  "updated": "YYYY-MM-DD",
  "pdInboxRoot": "path/to/inboxes/{team}/{pd-name}.json",
  "projects": [
    {
      "name": "string",
      "pd": "string|null",
      "path": "string|null",
      "stack": ["string"],
      "purpose": "string",
      "aliases": ["string"]
    }
  ]
}
```

## Markdown Output Format

Always use a table with these columns:
```
| Project | PD | Path | Stack | Purpose |
```

Archived entries go under `### Archived` section, not in the table.

## Key Rules

- JSON is the **authoritative source** — always prefer JSON for reads
- Only overwrite the target file, never merge and keep both
- Preserve `version` and `updated` fields on every JSON write
- Use ISO date format (YYYY-MM-DD) for all dates
