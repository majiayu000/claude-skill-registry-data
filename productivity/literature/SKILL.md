---
name: literature
description: "Literature: retrieve document-level scientific evidence from publications, clinical-trial registries, and patent sources. Use for PubMed records, reproducible searches, trial registrations, patent evidence, abstracts, study metadata, stable identifiers, and citation provenance."
category: literature
license: Mixed
metadata:
  access-mode: remote
  collection: literature
---

# Literature

Build traceable evidence from publications, clinical trials, and patents while preserving each
document type's identifiers, search fields, status semantics, and evidentiary role. The `resource`
tool exposes source metadata and instructions; the Agent constructs the task-specific search.

## Workflow

1. Define the question, document type, date range, organism or population, intervention or exposure,
   study design, identifiers, language constraints, and required metadata. This step is complete
   when the search protocol and unresolved constraints are explicit.

2. Browse the relevant document source:

   `resource({ action: "list", category: "literature/publications" })`

   This step is complete when `kind` is `resource_metadata` and every returned source has been
   compared against the protocol.

3. Load the selected source instructions using its exact exposed name:

   `resource({ action: "read", name: "biomarker-pubmed" })`

   This step is complete when the exact query interface, fields, pagination, identifiers, and output
   schema and package-relative scripts, references, and assets are known.

4. Execute reproducible fielded queries through all result pages. Preserve raw responses, query
   syntax, retrieval date, and stable identifiers such as PMID, NCT, and patent publication numbers.
   This step is complete when every page has been retrieved or a concrete failure is recorded.

5. Deduplicate by stable identifiers and label every record by document type and evidentiary role.
   Emit citations exclusively from retrieved metadata. This step is complete when every retained
   record has traceable provenance and every selected source has a result, valid empty result, or
   concrete failure.

Write search logs, raw metadata, normalized tables, and citation exports to the Session workspace;
use package directories as read-only sources.
