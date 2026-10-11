---
name: file-upload-patterns
description: "Upload files in LWC: lightning-file-upload, manual multipart, large-file chunked upload, and ContentDocument associations. NOT for ContentDocument query patterns."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
triggers:
  - "lightning file upload lwc"
  - "chunked upload salesforce lwc"
  - "large file upload apex"
  - "contentdocumentlink lwc"
tags:
  - file-upload
  - content-document
  - lwc
inputs:
  - "max file size"
  - "target record"
outputs:
  - "component with appropriate upload strategy + server-side Apex"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# LWC File Upload Patterns

LWC file upload has three tiers: (1) `<lightning-file-upload>` for ≤2GB files associated with a record; (2) custom input + fetch for more control; (3) chunked upload for very large files using ContentVersion.VersionData. This skill picks the right tier and shows the minimal implementation.

## When to Use

Any file intake UI. Choose tier by max size, auth model, and UX requirements.

Typical trigger phrases that should route to this skill: `lightning file upload lwc`, `chunked upload salesforce lwc`, `large file upload apex`, `contentdocumentlink lwc`.

## Recommended Workflow

1. Start with `<lightning-file-upload record-id="…">` if files are ≤2GB and tied to one record.
2. For custom flows: `<input type="file" @change=...>` → FileReader → POST to @AuraEnabled Apex with base64.
3. For files >12MB via Apex: chunk at 4.5MB and assemble ContentVersion with multiple ContentBody chunks via server-side concat.
4. Always validate MIME type client-side AND server-side.
5. Enforce size caps in Apex; don't trust client.

## Key Considerations

- Apex heap is 6MB / 12MB (transaction). Base64 adds 33%. For larger files chunk or use the direct REST upload.
- `lightning-file-upload` creates ContentDocumentLink automatically; custom flows must do this.
- Virus scanning is not automatic; many orgs run a Lambda on ContentDocument insert.
- Content types: validate with magic-bytes, not extension.

## Worked Examples (see `references/examples.md`)

- *Simple record attachment* — Attach PDF to Case
- *Chunked 50MB upload* — Legal contract

## Common Gotchas (see `references/gotchas.md`)

- **Heap exceeded** — Error at 12MB file.
- **No MIME validation** — User uploads .exe renamed .pdf.
- **Missing ContentDocumentLink** — File uploaded but not visible on record.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Base64-in-Apex for 100MB
- Trusting client MIME
- Skipping ContentDocumentLink

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-wire-service-about.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
- SLDS 2 — https://www.lightningdesignsystem.com/2e/
