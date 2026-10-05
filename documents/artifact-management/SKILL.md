---
name: artifact-management
description: |
  Create, retrieve, query, and update Artifacts — tangible deliverables
  produced by the project. Use when storing or retrieving documents,
  designs, datasets, build outputs, slide decks, or any completed
  deliverable that should be registered in the project catalog.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-artifact-management
    version: "1.0.0"
    created: 2026-04-11T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Artifact]
      mcp_tools: [create_artifact, get_artifact, query_artifacts, update_artifact]
---

# Artifact Management

## Intro

Artifacts are tangible deliverables — documents, design files,
datasets, build outputs, slide decks, videos, or external URLs.
Unlike Notes (thoughts in transit), Artifacts are completed
deliverables registered in the project catalog. Unlike WorkItems
(units of tracked work), Artifacts have no state lifecycle — they
exist or they don't.

Two storage patterns are equally valid:

- **Self-hosted**: the artifact content is the Markdown body of the
  entity file; `spec.location` may reference the file's own path or
  be omitted. Use for documents that belong in the repository (PRDs,
  runbooks, research reports, work instructions).
- **Pointer**: the deliverable lives elsewhere (external URL, cloud
  storage, build artifact); `spec.location` is the canonical address.
  processkit stores only the metadata card.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10
> on PATH). Agent harnesses may reach it directly from this skill's
> `mcp/mcp-config.json` or through the processkit gateway. Gateway
> deployments must surface only the processkit servers present in the
> installed/merged MCP configuration; this skill does not imply that
> unrelated processkit tools are available.

## Overview

### Artifact kinds

`spec.kind` classifies the artifact:

| kind       | When to use                                             |
|------------|---------------------------------------------------------|
| `document` | Prose documents — PRDs, runbooks, reports, guides       |
| `design`   | Design files — Figma, Excalidraw, wireframes            |
| `dataset`  | Structured data — CSV, JSON, Parquet                    |
| `build`    | Compiled outputs — binaries, bundles, tarballs          |
| `slides`   | Presentation decks — PPTX, PDF slide decks              |
| `video`    | Recorded content — demos, walkthroughs                  |
| `spec`     | Formal specifications — OpenAPI, JSON Schema, proto     |
| `diagram`  | Architecture and flow diagrams                          |
| `url`      | External web resources, dashboards, hosted tools        |
| `other`    | Anything that doesn't fit the above                     |

### When to create an Artifact

Create an Artifact when:

- A deliverable is complete enough to reference and share.
- Something produced by the project should be discoverable later
  (a report, a shipped binary, an approved design).
- A Note has been promoted to a finished document.
- A work item produced a document or design that should be cataloged.

Do **not** create Artifacts for in-progress work — use a WorkItem
or a Note while the thing is still being made.

### Creating

1. Choose `kind` from the table above.
2. Write a short, descriptive `name`.
3. Provide `slug_summary` when available: 4-6 meaningful words that
   summarize the durable deliverable. The server validates this shape
   and turns it into the ID slug; if omitted, the name remains the
   backwards-compatible fallback.
4. Set `location` for pointer artifacts (URL, path, bucket key).
   Omit or set to the entity file path for self-hosted artifacts.
5. Set `produced_by` to the WorkItem or other producing entity ID.
6. Set `owner` to the responsible Actor ID.
7. Add `tags` for retrieval (topic, project, format, etc.).
8. Write the file to `context/artifacts/ART-<id>.md`.
9. Log `artifact.created`.

### Querying

Common queries via `query_artifacts`:

- All artifacts of a given kind (e.g., all `document` artifacts)
- All artifacts owned by an actor
- All artifacts tagged with a given tag
- Full-text search via `index-management`

### Updating

Use `update_artifact` to revise metadata (new version, updated
location, changed owner). Pass `touch_updated_at=false` for
metadata-only updates that should not restamp `metadata.updated` and
invalidate an agent's prior body-read freshness checks. To replace the
body content of a self-hosted artifact, update the Markdown body via
`update_artifact` or by editing the file directly followed by reindex.

## Gotchas

Agent-specific failure modes:

- **Creating an Artifact for in-progress work.** An Artifact is a
  completed deliverable. If the thing isn't done yet, use a WorkItem
  (for tracked work) or a Note (for an idea still forming). Premature
  Artifact registration pollutes the catalog with incomplete items.
- **Omitting `location` for pointer artifacts.** If the content lives
  outside the repository (a URL, a cloud bucket path, a release
  binary), `location` is the only way to find it. Omitting it makes
  the catalog entry useless as a pointer.
- **Duplicate registration.** Before `create_artifact`, run
  `query_artifacts` and check for an existing entry with the same
  name or location. Duplicates create confusion about which entry is
  canonical.
- **Using Artifact for ephemeral build outputs.** Not every build
  artifact needs a catalog entry. Register the ones that matter for
  the release, for compliance, or for future reference. Registering
  every intermediate build output creates noise.
- **Forgetting `produced_by`.** Linking the artifact back to the
  WorkItem or other entity that produced it is cheap and makes the
  catalog navigable. Always set it when the provenance is known.

## Full reference

### Full field list

See `src/context/schemas/artifact.yaml` for the authoritative schema.

| Field         | Required | Description                                           |
|---------------|----------|-------------------------------------------------------|
| `name`        | yes      | Human-readable name                                   |
| `kind`        | yes      | Subtype (see table above)                             |
| `location`    | no*      | Path, URL, or storage key (* required for pointers)   |
| `format`      | no       | File format or MIME type (e.g. `pdf`, `image/png`)    |
| `version`     | no       | Version identifier for the artifact                   |
| `checksum`    | no       | Hash for integrity verification                       |
| `owner`       | no       | Actor ID responsible for the artifact                 |
| `produced_by` | no       | Entity ID that produced this, usually a WorkItem      |
| `produced_at` | no       | ISO 8601 datetime when the artifact was produced      |
| `tags`        | no       | Freeform tags for retrieval                           |

### Note vs Artifact decision rule

| State                           | Use       |
|---------------------------------|-----------|
| Idea, half-formed thought       | Note      |
| In-progress document            | Note or WorkItem body |
| Finished, shareable deliverable | Artifact  |
| External resource to reference  | Artifact (pointer) |

### Relationship to WorkItems

A WorkItem is the unit of work that produces an Artifact. Link the
two via `spec.produced_by` on the Artifact (pointing to the WorkItem
ID). This gives a navigable trail from deliverable back to the work
that created it.
