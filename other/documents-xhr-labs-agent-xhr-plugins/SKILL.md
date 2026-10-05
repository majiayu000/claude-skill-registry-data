---
name: documents
description: Documents skill index for company document storage, upload, access permissions, employee document types, listing, and search. Use when the user asks how to manage documents or wants to browse or search company documents rather than generate a document from a template.
---

# Documents skill index

Use this file to choose the correct document leaf skill.

## Navigation contract
- This file is a parent/index node only.
- Select and read the child `SKILL.md` entrypoint(s) matching the user's intent — the smallest sufficient set. One leaf for a single intent; multiple leaves only when the request genuinely contains multiple intents.
- Do not read unrelated child skills. Do not execute this directory as a script skill.
- Execute only the child leaf scripts referenced by the chosen child leaf `SKILL.md` files.

## Child entrypoints
<!-- Descriptions are condensed from each child's frontmatter — keep in sync when a child changes. -->
- skills/documents/document_access_permissions_help/SKILL.md — How-to answers about document access, sharing, and AI-agent permissions. No live document actions.
- skills/documents/documents_help/SKILL.md — How-to answers about uploading or adding company documents. No live document actions.
- skills/documents/documents_storage_help/SKILL.md — Answers where company policies and HR files should be stored. No live document actions.
- skills/documents/employee_document_types_help/SKILL.md — Explains employee document types, categories, and why start/end date fields change by type. No live document actions.
- skills/documents/list_company_document/SKILL.md — Executes a script to list all company documents in the workspace.
- skills/documents/search_company_document/SKILL.md — Executes a script to search company documents by topic, keyword, or phrase.

## Routing rules
- Help vs execute: a question about how something works or how to do it selects a `*_help` leaf; a request to actually view or find documents selects an executable leaf.
- List vs search: a specific topic, keyword, or phrase selects `search_company_document`; browsing all documents with no search term selects `list_company_document`.
