---
name: clickmax-proposals
description: Use when the user wants to find, create, edit, version or consolidate Clickmax proposal templates (slide deck or Word document) and the proposals generated for contacts/opportunities.
---

## When this applies

Proposal work: a reusable TEMPLATE is built once, then CONSOLIDATED for one opportunity/contact into a frozen proposal with a public link.

Not this skill:

- the opportunity/contact itself (stage, value, custom fields) -> pipeline/lead skills first, then consolidate here
- sending the link by WhatsApp/e-mail -> messaging skills, with the `slug` link from here

## Key assumptions

- `kind` decides the content. `slide_deck` = HTML slides (`pages[].compiledHtml`), tokens `{{scope.field}}`. `document` = a Word `.docx`, tokens `{scope.field}` (one brace), no pages.
- A document's text is written by the user in the Word editor (Propostas → Templates) or imported as `.docx`; these tools cannot upload or rewrite a `.docx`. `documentKey` = public URL of its current file; `null` = never saved, so it cannot be consolidated yet.
- Every document save is an immutable version. Restoring appends a NEW version pointing at the old file; history is never rewritten.
- Variables (same keys in both kinds): `lead.name|email|telephone|document|address|city|state|profession`, `opportunity.title|value|origin` (value already in R$), `company.legalName|tradeName|taxId|address` (company linked to the opportunity, else to the contact), `brand.name`, `date.today|todayLong` (consolidation day), and `custom.<fieldName>` for lead/opportunity custom fields. A variable without a value comes out BLANK in the proposal — never as a literal token.
- Consolidation is a snapshot: editing or restoring the template later never changes proposals already generated. Re-consolidating creates a new proposal.

## Thought process

1. Find the template: `mcp__plugin_clickmax_clickmax__proposal_templates_list` (`kind`, `status`, `search`; `library: true` adds system templates).
2. Read it with `mcp__plugin_clickmax_clickmax__proposal_templates_get` before any edit or consolidation.
3. Slide deck edits → `mcp__plugin_clickmax_clickmax__proposal_templates_page_upsert` (one slide per call). Document → only metadata here; content changes are the user's, in the editor.
4. Consolidate for a concrete opportunity (preferred) or contact.

## Execute guide

- `mcp__plugin_clickmax_clickmax__proposal_templates_create` with `kind: "document"` creates an EMPTY Word template; tell the user to open it and write/import the text — then it can be consolidated after the first save.
- `mcp__plugin_clickmax_clickmax__proposal_templates_document_versions_list` to answer "who changed the contract and when"; `mcp__plugin_clickmax_clickmax__proposal_templates_document_version_restore` only when the user explicitly asks to go back to a version (it becomes the current one for FUTURE proposals).
- Before consolidating a document, check `config.document.variables` against the list above: a typo, a name with spaces (`{ lead.name }`) or a custom field that does not exist comes out blank — warn the user instead of consolidating silently.
- Consolidation fails with `PROPOSAL_DOCUMENT_MALFORMED_VARIABLE` when the Word text has a `{` never closed: tell the user to find and close it in the editor (body, header or footer), save, then consolidate again. Retrying unchanged fails the same way.
- `mcp__plugin_clickmax_clickmax__proposals_consolidate` with `templateId` + `opportunityId` (and/or `leadId`). Share the public link `/proposals/p/<slug>`; for a document it shows the filled Word with download and print buttons.
- `mcp__plugin_clickmax_clickmax__proposals_list` / `mcp__plugin_clickmax_clickmax__proposals_get` for status (`draft` → `viewed` on the client's first open).

## Report

- Consolidation: template name, for whom, the public link, and any variable that will be blank.
- Versions: version number, author, date; say restore creates a new version.
- CTA to open one template in the builder: `action="open-page"` with `path="/marketing/proposals/<templateId>"`.

## Anti-patterns

- Writing `{{lead.name}}` in a document or `{lead.name}` in a slide — each kind has its own brace count.
- Promising to "edit the Word text" through these tools; only the user edits a document's content.
- Consolidating a document template whose `documentKey` is null.
- Restoring a version to "see" it — restore changes the current template; listing versions is enough to inspect.

---

Clickmax skill revision: `b8294822a4d6`
