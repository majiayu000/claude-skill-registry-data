---
name: feishu-doc-archiver
description: "Archive Feishu Wiki or Docs pages and their linked documents locally, preserve offline images at the best available source quality, and consolidate verified duplicates when requested. Use for document downloads, blurry-image re-export, or keeping only high-quality archive images; not for cloud publishing or bug investigation."
---

# Feishu Doc Archiver

Create a usable offline reading copy, with a traceable relationship between each
source illustration and the file that readers actually open. A successful text
export is not evidence that every image, embedded object, or linked page was saved.

## Scope and inputs

Use this skill for a new archive, a refresh of an existing archive, or an explicitly
requested image consolidation. Infer the destination, existing archive, requested
formats, browser choice, and link scope from the current conversation and local
rules. Respect a requested private workspace location such as `.manifest`.

Do not use it to edit remote documents, publish an archive, investigate a software
bug, or mirror an entire account merely because one page links to it.

- A request for one page does not authorize an unrestricted crawl.
- A request for all linked documents includes recursive document references unless
  the user states a shallower scope. Do not silently stop after a fixed depth.
  Maintain a visited set and an explicit frontier; cycles must not repeat work.
- Distinguish document references from navigation menus, personal profiles, runtime
  applications, repositories, large data folders, and non-image attachments. Record
  these separately when the requested scope includes them; never quietly treat
  them as completed documents.
- If a practical limit, access barrier, or expanding scope prevents completion,
  finish accessible work and report the exact outstanding frontier. Ask only for
  the missing scope decision that changes what can safely proceed.

Use source object identity, when observable, to reconcile different links to the
same document. Preserve meaningful version/query distinctions; matching titles
or stripping every query parameter is not a safe deduplication rule.

## Access and authority

Default behavior reads remote content and writes the requested local archive.
It never edits cloud content, changes sharing, requests access on someone else's
behalf, or uploads private material to another service.

An explicit browser choice is binding. For the in-app browser, read the available
`browser:control-in-app-browser` skill and its current runtime documentation before
using it. If no browser was specified, follow that skill's connector discovery and
surface-selection rules. This skill does not authorize another browser as a fallback.

Use the existing authenticated session without reading cookies, browser profiles,
local storage, or credentials. Export permission is separate from view permission.
If download/export is denied, record that barrier; a loaded-resource technique is
not permission to circumvent it. Never save signed URLs or authentication material
in reusable scripts, receipts, or reports.

Deletion is an optional higher-risk mode. The user's explicit instruction to keep
only verified high-quality copies authorizes that consolidation within the named
archive; do not ask for the same approval repeatedly. Without such authority,
produce a cleanup preview instead of deleting existing files. Never clean the
user's general Downloads folder or another task's outputs.

## Acquire and reconcile

1. Inspect the existing reading copies and source records before refreshing. For
   a new archive, obtain the best supported document export and retain source
   links plus access time. Choose Markdown/HTML for reading when appropriate;
   preserve native formats when they carry material absent from the reading copy.
2. Build a source inventory from both the document and its rendered media. Count
   illustration occurrences separately from distinct assets. Record embedded
   boards, spreadsheets, diagrams, and inaccessible placeholders explicitly.
3. Reconcile every occurrence to a local asset or a named limitation. Do not assume
   that a Word package, Markdown bundle, or screenshot contains all original media.
4. Resolve requested document references using the frontier above. Rewrite links
   only after the destination exists locally, keeping source provenance available.

For UI acquisition, read [browser-acquisition.md](references/browser-acquisition.md).
It covers full-size previews, asynchronous image changes, native board export,
download attribution, and resumable progress without fixed selectors or coordinates.

## Preserve fidelity, then consolidate

Prefer an original raster file for an ordinary image and a native board export for
a diagram. Where offered, obtain the highest useful PNG export and a vector format
that preserves readable text. Do not enlarge a thumbnail with interpolation or
generative tools and call the result an original or a sharper source.

Before replacing anything, verify that it is the same illustration and version,
that no content was clipped, and that the new file decodes. More pixels, a larger
file, or a PDF extension alone proves none of these properties. Tiny text should
be checked at readable scale; extracted text is supplementary evidence, not proof
of correct layout or a complete semantic transcription.

For a request to keep only high-quality copies, use
[retention-and-verification.md](references/retention-and-verification.md). Select
one canonical asset for verified equivalent images, including cross-document
duplicates. Update every dependent reference and validate it **before** deleting
superseded files. Keep the best available sole copy when no better source exists.

The read-only helper [inspect_media.py](scripts/inspect_media.py) reports file
digests, raster dimensions, decode failures, and byte-identical groups:

```bash
python <skill-directory>/scripts/inspect_media.py <archive-directory>
```

It requires Pillow for raster validation, makes no network calls, and writes JSON
only to stdout. It does not choose a keeper, inspect document links, compare crops,
inspect archive members, prove PDF/SVG fidelity, or delete files. Use the configured
workspace runtime when available; do not silently install packages into the project.
Inspection reports include archive-relative filenames; keep them with the private
archive. Do not publish generated reports or package interpreter caches with the skill.

## Completion and failure handling

Save a compact local receipt with source-to-file mappings, acquisition method,
actual exported dimensions and digest, validation status, and unresolved items.
Record deletion candidates, their replacement, and the reason before cleanup;
afterward, keep the record without retaining redundant image backups as deliverables.
Reuse existing metadata conventions instead of creating a second competing catalog.

Completion requires:

- every in-scope page and illustration accounted for, including repeated occurrences;
- all retained raster files decoded and all intended vector/text outputs checked;
- zero missing local image references, including relative links in other documents;
- no remote image dependency presented as an offline image;
- a visible check of representative dense diagrams and every ambiguous replacement;
- cleanup revalidation, updated counts/checksums, and a precise incomplete list.

Retry transient UI/download failures only after inspecting the changed state. Use
bounded batches and persist verified progress so a timeout does not force a restart.
If a requested browser or authentication is unavailable, retain the accessible
result and explain the required user action; do not bypass the access boundary.
If an embedded object has no usable export, label any screenshot or transcription
as a fallback. Never invent missing text or promise all text is perfectly parsed.

The final response should identify the local entrypoint, page/asset counts,
high-quality retention result, validation result, and exact failures or unvisited
links. Separate a page snapshot from a complete document and an available low-quality
fallback from a successful high-quality re-export. Do not claim full completion
while an unexplored frontier remains.
