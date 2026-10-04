---
name: docx
description: "Use this Canvas-owned clean-room skill for creating, reading, editing, reviewing, redlining, commenting, or repairing Word `.docx` documents. Trigger for Word documents, DOCX files, memos, reports, letters, templates, tracked changes, comments, table of contents, headers, footers, page numbers, and Google Docs-targeted documents that should be authored as DOCX first."
license: "Canvas Notebook Sustainable Use License"
---

# DOCX Documents

This skill covers Word-compatible `.docx` work in Canvas Notebook. It is a
clean-room Canvas skill; do not copy vendor skill material, hidden prompts, or
proprietary helper code into this folder.

## Core Contract

- Always edit a checked-out working copy. Call `checkout_docx` with the
  workspace-relative input path, edit only its returned `workingPath`, and
  publish with `commit_docx`. This applies even when overwriting is requested:
  the commit tool checks the original revision and edit lease.
- For a new document, use `checkout_docx` with `createOnly: true` and the
  desired `.docx` path. Create the returned working file with Python, then
  commit its checkout ID. An existing output is never silently overwritten.
- Use `CANVAS_AGENT_TEMP_DIR` for scripts, working copies, unpacked OOXML,
  conversions, and render previews. Publish DOCX working copies through
  `commit_docx`; use `copy_path` or `move_path` for requested non-DOCX exports.
- Preserve existing document style for targeted edits. For new documents, set
  explicit page size, margins, paragraph spacing, font choices, headings,
  tables, headers, and footers instead of relying on Word defaults.
- Prefer editable Word-native content: paragraphs, runs, tables, lists,
  sections, headers, footers, comments, and fields. Do not turn pages into
  screenshots unless the user asks for an image-only deliverable.
- Keep intermediate render images, PDFs, unpacked XML, and scratch files out of
  the final response unless the user asks for them.
- Store final user-facing files in the requested workspace path using a stable
  descriptive filename.

## Recommended Tools

- `python-docx` for normal document creation and structured edits.
- Standard library `zipfile` plus `lxml` for OOXML edits that `python-docx`
  cannot express, such as true comments, content controls, fields, or targeted
  XML repair.
- Pandoc for simple, text-oriented Markdown-to-DOCX or DOCX-to-Markdown
  conversion. Do not use it for format-faithful edits to an existing DOCX.
- LibreOffice `soffice` for DOCX-to-PDF conversion. Before invoking it, read
  [references/headless-libreoffice.md](references/headless-libreoffice.md).
- Poppler `pdftoppm` or `pdftocairo` when available for PDF to PNG rendering.

Use the installed runtime dependencies. Agent shell subprocesses can write only
to the current session temporary directory; workspace files are read-only there.
Do not try shell redirects, direct Python saves, copies, or custom scripts to
bypass publication. Never store API keys or secrets in a skill directory.

## Checkout, publication, and recovery

- Keep the `checkoutId`, `workingPath`, and `lockExpiresAt` returned by checkout.
  Use `inspect_docx_checkout` with `renewLease: true` before the lease expires
  during longer edits. Expired or replaced leases are never recreated by renewal.
- Finish and await all Python/render subprocesses before `commit_docx` reads the
  working copy. Pass only the checkout ID; never supply or replace its baseline.
- A committed result is idempotent. If publication returned a transient error
  with status `prepared`, retry the same checkout ID: its exact proposed bytes
  remain fixed even if scratch files changed afterward.
- If status is `conflict`, report the conflict and its `recoveryId`. The proposal
  is retained outside temporary cleanup. Use `inspect_docx_checkout` with
  `restoreWorkingCopy: true` to recover it in the same task; this replaces only
  the scratch copy. To keep a separate proposal, create a new `createOnly`
  checkout and copy the recovered content into that checkout's working path.
- Use `release_docx_checkout` when stopping without publication. It retains the
  current draft and releases the lease. Released checkouts cannot commit.
- If the lease belongs to another editor, explain who is editing when that
  information is available and preserve any proposed work. Never force release
  another editor or overwrite a newer version to complete a document task.

## Workflow

1. Identify whether the task is read/review, create, targeted edit, structural
   repair, comments/redlines, or conversion.
2. Check out the input or reserve a new output. If editing an existing document,
   inspect the working copy's current structure before
   changing it: headings, sections, tables, images, comments, tracked changes,
   headers, footers, and metadata.
3. Make the smallest reliable edit that satisfies the request. Use styles and
   reusable helper functions instead of scattered one-off formatting.
4. For visual deliverables, render the DOCX when possible and inspect page
   images for clipping, overlap, missing glyphs, broken tables, bad page breaks,
   header/footer issues, and inconsistent spacing.
5. If render output is wrong, fix the DOCX and render again. If rendering is
   unavailable, perform structural checks and clearly state that visual QA could
   not be completed.
6. Publish the validated working copy with `commit_docx` and verify that the
   returned status is `committed` before reporting the workspace file as saved.

## Common Tasks

- **Read or summarize:** extract text with `python-docx`; inspect tables and
  images separately; render if layout matters.
- **Create a new document:** build with `python-docx`, define styles up front,
  then add content. Use real tables and lists.
- **Targeted edit:** preserve existing formatting. Avoid document-wide restyles
  unless asked.
- **Comments:** use OOXML comments only when true Word comments are required.
  Otherwise, a review memo or inline markup may be safer.
- **Tracked changes:** true Word redlines require OOXML patching. If exact
  revision semantics matter, validate in Word-compatible tooling after writing.
- **Google Docs target:** create a clean `.docx` first. Avoid Word-only visual
  effects that import poorly, such as decorative title rules, complex floating
  objects, and brittle fields.

## Final Checks

- Final DOCX opens without repair warnings.
- No placeholder tokens, internal notes, or unresolved TODOs remain.
- Tables fit within margins and have readable column widths.
- Headers, footers, page numbering, links, and references are intentional.
- For high-stakes documents, mention any environment limitation that prevented
  render or Word-native validation.
