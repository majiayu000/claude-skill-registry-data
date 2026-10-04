---
name: papermeld
description: Build, maintain, retrieve, and audit a local catalog-first literature and implementation library with PaperMeld. Use when Codex needs to organize PDFs or converted Markdown, bootstrap an existing paper folder, link local Git repositories to papers, diagnose broken Markdown image links, conduct a literature review, or help an AI use library.jsonl without scanning every paper. Works across research fields.
---

# PaperMeld — Codex Skill

Treat a paper library as two layers: a compact catalog for routing and original
Markdown/PDF/figure files for evidence. Use `library.jsonl` to decide what to
open; never use a title, tag, abstract excerpt, or filename as factual proof.

## Start with discovery

1. Ask for or locate the library root. Look for `library.jsonl` first.
2. If the `papermeld` command is available, run `papermeld --library <root> search <query>` or `verify` as appropriate. Otherwise inspect `library.jsonl` directly for a read-only task.
3. Read [references/catalog-contract.md](references/catalog-contract.md) before editing a catalog or deciding whether a path is a valid local record.
4. Report the observed layout, catalog record count, unresolved records, and any assumptions before proposing a structural change.

## Choose the narrowest workflow

### Retrieve evidence for a question or writing task

1. Extract 2–4 precise concepts from the task: problem, setting, method family, limitation, or venue.
2. Search one focused query at a time. Rank records by title, tags, abstract excerpt, status, and source paths.
3. For a specific claim, select a small, deep evidence set—normally 3–8 papers.
4. Open the relevant section, page, or figure in each selected source. Record a source card with its path, version, precise claim, and location.
5. State evidence gaps explicitly. Hand the source cards to a domain writing skill when one applies; PaperMeld provides evidence routing, not venue-specific rhetoric.

### Conduct a literature or field review

1. Search the complete local catalog by problem, method, data, benchmark, and time range. Then search the web for material absent from the local library.
2. Build a method map: research branches, representative papers, datasets, codebases, evaluation conventions, and open questions.
3. Read enough primary sources to cover each branch. Do not impose a fixed paper count; stop when new sources no longer change the map.
4. Keep the broad map separate from the final evidence set. Use the latter for any precise factual or writing claim.

### Link and use local implementation repositories

For an implementation task, inspect a paper's `code` entries before searching online. Open the linked README and relevant source files, then use the recorded repository state to reproduce or explain behavior.

To index repositories already on disk, preview and then apply:

```bash
papermeld --library <library-root> link-code --code-root <repository-root> --dry-run
papermeld --library <library-root> link-code --code-root <repository-root>
```

When no local implementation is available, locate the confirmed project repository, clone it into the user's selected code root, and run `link-code` again. Run `verify` after linking or updating a repository.

### Bootstrap an existing collection

Use bootstrap when Markdown and PDFs already exist. First run a dry-run. Pass every Markdown root and PDF root explicitly if they lie outside the library root. Bootstrap may create the library layout and catalog, but must not rename, move, delete, or rewrite the source collection.

```bash
papermeld --library <library-root> bootstrap \
  --markdown-dir <markdown-root> \
  --pdf-dir <pdf-root> \
  --dry-run
```

Check duplicate `paper_id` values and links before rerunning without `--dry-run`. Never use `--overwrite` until the existing catalog has been inspected and backed up.

### Ingest one new PDF

Use `ingest` after a converter has been installed and tested. Preview metadata and duplicate detection first:

```bash
papermeld --library <library-root> ingest <input.pdf> --label <short-label> --dry-run
```

Remove `--dry-run` only after the user has reviewed title, year, venue, identifier, and destination. An arbitrary external PDF is copied by default. A PDF in `inbox/` is managed by the library. Moving an external source requires the explicit `--move-source` flag.

For non-MinerU converters, use a command template containing literal `{pdf}` and `{output}` placeholders. The converter must generate exactly one Markdown file below its output directory. Read [references/converter-boundary.md](references/converter-boundary.md) before diagnosing a converter integration or image migration.

### Repair or audit a library

Run `verify` before proposing a repair. Classify failures as missing source material, an invalid catalog path, a converter-output/image-link mismatch, or a duplicate/version conflict. Prefer a narrowly scoped reversible repair. Do not mass-rewrite Markdown image paths, mass-delete apparent duplicates, or re-bootstrap a nonempty catalog without direct authorization and a backup.

## Non-negotiable rules

- Preserve the user's PDFs, Markdown, images, annotations, and reference-manager data unless the user explicitly authorizes a modification.
- Do not claim a preprint and formal publication are duplicates solely because their titles resemble each other. Verify DOI, arXiv ID, authors, or the actual document.
- Do not let a catalog search replace source inspection or citation checking.
- Keep personal library data out of a public repository. Share an empty example library or synthetic fixtures instead.
- Separate general library behavior from domain writing behavior. Keep TITS, medicine, law, or other specialised advice in an extension Skill.

## Deliverables

- Retrieval: a short candidate table, selected source cards, and stated gaps.
- Bootstrap/ingest: a dry-run summary, intended changes, user-confirmed metadata, and post-run verification result.
- Audit: the exact broken records, failure category, safe repair options, linked-code state, and what was not changed.
- Open-source setup: minimal prerequisites, a fresh-install path, a fresh-library path, and a test command proven in a clean directory.

## Resources

- [references/catalog-contract.md](references/catalog-contract.md): catalog fields, path rules, and evidence boundary.
- [references/converter-boundary.md](references/converter-boundary.md): converter contract, transactional import, and image-link checks.
