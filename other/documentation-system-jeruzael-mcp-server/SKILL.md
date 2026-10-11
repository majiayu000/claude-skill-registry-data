---
name: documentation-system
description: Create, organize, review, and reuse professional business and technical documentation for Exorex client work, app development, AI automation projects, internal operations, and handover. Use when Codex needs to draft or structure client discovery docs, proposals, quotations, scopes of work, workflow maps, automation blueprints, app requirements, API contracts, meeting minutes, testing checklists, deployment notes, handover docs, maintenance support docs, service packages, or internal decision records.
---

# Documentation System

Use this skill to turn repeated business and project information into clear, versioned, reusable documents.

## Core Principle

`Clear information + reusable structure + versioning + easy access = better execution`

Documentation must be useful to the actual audience. Client-facing documents should be polished and business-readable. Internal documents may include assumptions, risks, estimates, implementation notes, and decision history.

## Workflow

1. Identify the document type and audience.
2. Collect source information from discovery notes, meetings, client messages, tickets, code, or deployment records.
3. Choose the closest template from `references/document-templates.md`.
4. Separate client-facing content from internal-only content.
5. Draft the document with clear purpose, scope, assumptions, exclusions, responsibilities, timeline, and next steps.
6. Add version metadata:
   - version
   - date
   - prepared by
   - prepared for
   - status
   - revision notes
7. Review for clarity, scope control, missing details, and reuse potential.
8. Store or name the document consistently.

## Naming Convention

Use:

`[ClientOrProject]_[DocumentType]_v[Version]_[YYYY-MM-DD]`

Examples:

- `TipidSulit_Proposal_v1.0_2026-05-30`
- `LabadaGo_ScopeOfWork_v1.1_2026-05-30`
- `Exorex_ClientDiscoveryTemplate_v1.0_2026-05-30`

## Status Labels

Use one of:

- Draft
- For Internal Review
- For Client Review
- Revised
- Approved
- Signed
- Archived
- Superseded

## Quality Checklist

Before handoff, verify:

- Purpose and audience are clear.
- Scope, exclusions, assumptions, and responsibilities are explicit.
- Timeline and pricing, if present, are realistic and clearly explained.
- Technical terms are translated into business language when client-facing.
- Version, date, status, and revision notes are present.
- Next steps are included.
- Internal-only notes are not included in client-facing output.
- The document can be reused as a future template.

## Output Contract

When using this skill, provide:

1. Recommended document type and audience.
2. Draft document or reusable template.
3. Required inputs still missing.
4. Version/status metadata.
5. Review checklist or next steps.
