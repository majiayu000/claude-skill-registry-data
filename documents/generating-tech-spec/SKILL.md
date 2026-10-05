---
name: generating-tech-spec
description: Generates structured technical specifications including ADR (MADR), RFC, design documents, and proposals. Use when writing a spec, creating an ADR, drafting an RFC, or creating a design document.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: "[spec-type] [topic]"
  stability: stable
  content-hash: sha256:bfebebda014156697a02550dd54bb946b9ac01aed067bd6ccd6ee7ef63843072
  last-verified-cc-version: 1.0.34
---

# Technical Specification Generation

**Target**: $ARGUMENTS

Generate a structured technical specification document based on the requested type and topic.

## References (MUST READ)

Read these before proceeding:

- `references/tech-spec-formats.md` — ADR (MADR), RFC, design doc, and proposal templates

## Spec Types

| Type | Trigger phrases | Output directory |
|------|----------------|-----------------|
| **ADR** | "adr", "architectural decision record" | `docs/adr/` |
| **RFC** | "rfc", "request for comments" | `docs/rfc/` |
| **Design Doc** | "design doc", "design document", "tech spec" | `docs/specs/` |
| **Proposal** | "proposal", "technical proposal" | `docs/specs/` |

## Workflow

1. **Detect spec type** from arguments — default to Design Doc if ambiguous
2. **Read reference** for the matching template format
3. **Glob for existing specs** in the target directory to determine next sequence number:
   - ADR: `docs/adr/NNNN-*.md` (four-digit, e.g., `0001-use-postgres.md`)
   - RFC: `docs/rfc/NNNN-*.md`
   - Design Doc/Proposal: `docs/specs/<date>-<slug>.md`
4. **WebSearch** for relevant context if the topic references specific technologies
5. **Generate the document** using the appropriate template structure
6. **Output location** and suggest next steps (review, share, link to implementation)

## Output Naming

```text
ADR:      docs/adr/NNNN-<slug>.md        (e.g., 0003-use-event-sourcing.md)
RFC:      docs/rfc/NNNN-<slug>.md        (e.g., 0001-api-versioning.md)
Design:   docs/specs/<date>-<slug>.md    (e.g., 2026-03-01-auth-redesign.md)
Proposal: docs/specs/<date>-<slug>.md    (e.g., 2026-03-01-migrate-to-k8s.md)
```

## Rules

- Always read existing specs first to match formatting and numbering conventions
- Include YAML frontmatter with title, date, status, and author fields
- ADRs must follow MADR format (Context → Decision → Consequences)
- RFCs must include a "Status" field (Draft → Proposed → Accepted/Rejected)
- Never overwrite existing spec files — always create new ones
- Use `converting-doc-format` skill for PDF/HTML/DOCX export
