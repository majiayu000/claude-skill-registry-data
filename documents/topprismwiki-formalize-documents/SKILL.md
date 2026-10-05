---
name: topprismwiki-formalize-documents
description: Process approved local Office, PDF, image, Markdown, and related documents by evidence, version family, and formal admission rules. Internal child module of $topprismwiki.
---

# Document formalization

Process only sources in the approved registry. Preserve originals and record
path, hash, modification time, version family, sensitivity, and page/section
anchors. Office uses `officecli`; PDF and presentation pages require visual
review; images require a local or explicitly approved vision adapter.

Document outcomes are `formal_source`, `catalog_only`,
`duplicate_or_superseded`, `quarantined`, `excluded`, and `blocked`. Fact
outcomes are `formalized`, `duplicate`, `conflicting`, `relation_candidate`,
`evidence_insufficient`, and `non_durable`.

Route visual pages to `vision-reviewer`, bulk text to `bulk-worker`, and
ambiguous entities or relationships to `adjudicator`. A filename, directory,
brand co-occurrence, or ordinary Wikilink is not relationship evidence.

See [document-contract.md](../../references/document-contract.md) before
creating a review package.

## Execution contract

This module processes only an approved source registry entry. Preserve the
original outside Git, record its SHA-256, modification time, source root,
sensitivity and version-family identifier, and never use a filename or directory
as relationship evidence. Read [adapter-contracts.md](../../references/adapter-contracts.md)
for the public input boundary.

Route ordinary text and structure to `text-extractor`, visual pages to
`vision-reviewer`, low-risk independent units to `bulk-worker`, and ambiguous
entities, namespaces, conflicts or relationships to `adjudicator`. No worker
may modify `vault/wiki`.

The minimum route is: `doctor --capability documents` → freeze source registry
and versions → extract and hash → inspect page/section/table anchors → create a
coverage batch → review facts and relations → run authorized update → validate.
Office extraction is `adapter-required`; PDF/PPT/image processing additionally
requires a model with OCR, layout, table, chart and diagram understanding.

If the original is missing, unreadable, ambiguous, superseded or visually
unverified, preserve the history and mark the unit `source_unavailable`,
`quarantined`, `duplicate_or_superseded` or `blocked` as appropriate. Do not
silently replace it with a newer file. Use
[`docs/zh-CN/troubleshooting.md`](../../../../docs/zh-CN/troubleshooting.md)
for missing dependencies and review-schema errors.
