---
name: book-publication-ops
description: Research, format, review, and package books for ebook and print publication. Use when preparing a manuscript for KDP or similar platforms, building a source-document conversion matrix, auditing compiled manuscripts, generating EPUB/PDF/cover specs, staging AI review lanes, or assembling upload-ready publication packets.
---

# Book Publication Ops

## Overview

Use this skill to turn one canonical manuscript into research-backed, format-validated publication assets.
Keep the source document stable, generate platform-specific outputs from it, and treat upload as the last step rather than the first.

## Workflow

1. Lock the publication contract.
- Capture target platforms, formats, trim targets, art scope, budget, and launch order.
- Default to `ebook first, print second` when budget or cover readiness is uncertain.

2. Establish the source-of-truth model.
- Use one canonical manuscript plus explicit metadata and output folders.
- Read `references/source-model.md`.

3. Research current platform rules before formatting.
- Prefer official platform docs over memory.
- Use arXiv only for typography, accessibility, and reading-experience context, not for platform acceptance rules.
- For arXiv discovery, use the AetherBrowser ArXiv lane first:
  - `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain arxiv.org --task research --engine playwriter`
  - `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title --url "<arxiv search or abs url>"`
  - `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot --url "<arxiv search or abs url>"`
- If the browser lane is blocked, fall back to standard fetch or official docs.
- Read `references/platform-research.md` and `references/toolchain.md`.

4. Build the conversion matrix.
- Decide how the source document becomes each target artifact:
  - reflowable ebook
  - print interior PDF
  - review DOCX or markdown packet
  - cover brief pack
- Avoid fixed-layout unless the whole book truly requires it.
- If the repo already contains a publication builder, prefer it before introducing a generic converter.

5. Audit the manuscript before export.
- Run `scripts/manuscript_audit.py` on compiled manuscripts before spending time on art or upload.
- Use the report to catch duplicate chapter numbers, compile notes, and meta leakage.

6. Produce publication assets.
- Generate:
  - ebook package
  - print package
  - review packet
  - upload packet skeleton

7. Run review lanes.
- Use device/format QA and reader-perspective QA separately.
- Read `references/review-lanes.md`.

8. Lock text before expanding art scope.
- Treat cover art as required for publishing.
- Treat interior ornaments, illustrated inserts, and deluxe touches as optional until text is stable.
- Read `references/cover-art.md`.

9. Build the upload packet.
- Collect metadata, keywords, categories, pricing sheet, rights, and final file paths.
- Keep upload automation behind a human confirmation step.

10. Publish last.
- Use browser automation only after the packet is stable and verified.
- If the run is long-lived or artifact-heavy, keep admin outputs and backups explicit.
- Read `references/admin-lane.md`.

## Quick Start

Audit a compiled manuscript:

```powershell
python C:\Users\issda\.codex\skills\book-publication-ops\scripts\manuscript_audit.py `
  --input C:\path\to\compiled-manuscript.md `
  --json-out C:\path\to\artifacts\publication\manuscript_audit.json
```

If the repo is `SCBE-AETHERMOORE` and the existing KDP builder is present, use it first:

```powershell
cd C:\Users\issda\SCBE-AETHERMOORE
python content\book\build_kdp.py
```

## Aethermoor Rule

For Aethermoor or `The Six Tongues Protocol` work:
- keep the world magic-first
- keep system structure legible without flattening wonder
- prefer artifact, ritual, and motif language over generic UI metaphors
- treat ravens, roots, flowers, crystal, witness, and six-tongue geometry as reusable packaging motifs

Read `references/cover-art.md` before generating book art for Polly, Aria, Alexander, or related world packaging.

## References

- `references/source-model.md`
  - Read first when setting up the canonical manuscript and output folders.

- `references/platform-research.md`
  - Read when verifying current KDP or adjacent platform requirements and when gathering official links.

- `references/toolchain.md`
  - Read when choosing between Pandoc, Sigil, Scribus, Kindle Previewer, Adobe, or hybrid workflows.

- `references/review-lanes.md`
  - Read when assigning AI reviewer personalities, device QA lanes, and acceptance criteria.

- `references/cover-art.md`
  - Read when creating cover briefs, ornament packs, motif sheets, and Aethermoor-specific art prompts.

- `references/admin-lane.md`
  - Read when turning publication work into long-running artifact-backed admin workflows.
