---
name: crav1-export-spec
description: Re-project an existing canonical spec.md into EARS, BDD, OpenSpec, YAML, JSON, and/or BMAD. Use when the spec already exists and the user wants another format. Do not change behavior. Do not write application code.
disable-model-invocation: true
icon: book-open
color: orange
---

# Export spec

Find `docs/specs/<slug>/spec.md` (user @-mention, else most recently edited spec excluding `_template`).

Read `references/formats.md` from skill `crav1-ideas-to-spec` (drop-in: `.claude/skills/crav1-ideas-to-spec/references/formats.md`; plugin: sibling `skills/crav1-ideas-to-spec/references/formats.md`) and write only the requested format(s) under `docs/specs/<slug>/export/`.

Rules:

- Do not add requirements that are not in `spec.md`, ADRs, or diagrams.
- If something cannot be expressed in the target format, put it under `open_questions` / Open Questions and say so.
- If `spec.md` is too vague to export, stop and tell them to `/crav1-tighten-spec` first.
- Keep IDs stable if `export/spec.yaml` or `export/spec.json` already exist.

Ask which format if they did not name one.
