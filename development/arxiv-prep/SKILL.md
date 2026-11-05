---
name: arxiv-prep
description: Prepare and validate LaTeX research papers for arXiv submission. Use when Codex must identify the complete TeX source graph, build a minimal source archive, create a deterministic manifest and checksum, verify arXiv filenames and dependencies, compile in a clean directory, inspect the resulting PDF, prepare metadata, or produce a final upload checklist. Also use for final arXiv-only submission readiness together with citation, provenance, terminology, and AI-disclosure audits.
---

# arXiv Prep

Prepare a source bundle that arXiv can compile independently and whose output matches the reviewed repository PDF. Treat formatting compliance, scholarly preflight, and author attestations as separate requirements.

## Required workflow

1. **Verify current rules.** Read `references/submission-checklist.md`. Before an actual upload, browse the official arXiv submission, TeX, metadata, licensing, category, and generative-AI pages because limits and policies can change. Cite the checked pages in the handoff or preflight report.
2. **Identify the authoritative paper.** Determine the root TeX file, compiler, included TeX files, bibliography mechanism, figures, local classes/styles, generated tables, and other runtime dependencies. Use the recorder file from a successful build when available, but inspect `\input`, `\include`, bibliography, and figure directives as well.
3. **Build and inspect the repository PDF.** Use the repository's documented compiler and `nice` for a heavy build. Resolve errors, undefined references or citations, rerun warnings, and overfull boxes introduced by current edits. Inspect the rendered title page, abstract, contents, representative equations, references, and final page. Do not generate HTML.
4. **Run scholarly preflights.** Use `$ai-slop-preflight` for citation support, provenance, conversation residue, defensive or promotional prose, terminology apologies, and disclosure. Use `$latex-jargon-auditor` when terminology remains a concern. An arXiv-compatible archive is not evidence that the mathematics or citations are ready.
5. **Construct a minimal allowlisted archive.** Prefer an existing project preparation script. Otherwise create a small project-local script with an explicit ordered source list. Include only files required to compile: TeX, bibliography or required `.bbl`, local classes/styles, figures, and indispensable data. Exclude ledgers, dashboards, literature caches, exploratory scripts, virtual environments, logs, auxiliary files, synchronization files, and the compiled paper PDF unless it is genuinely an input figure.
6. **Make packaging reproducible.** Store a human-readable source manifest and a SHA-256 checksum beside the archive. For deterministic archives, sort the allowlist and normalize tar ownership, permissions, and timestamps. Validate every included dependency and reject undeclared `\input` files.
7. **Audit the bundle.** Run:
   ```bash
   python3 .claude/skills/arxiv-prep/scripts/audit_arxiv_bundle.py archive.tar.gz --root main.tex
   ```
   Treat warnings as review prompts. The script cannot discover macro-generated paths or decide whether a PDF is a necessary figure.
8. **Clean-room compile.** Extract the finished archive into a new temporary directory and build from there with the intended engine. Do not rely on the repository's auxiliary files, environment, or sibling sources. Check the final log and compare the clean PDF with the reviewed PDF; compare rendered pages or extracted text when byte equality is not expected.
9. **Prepare metadata separately.** Create a concise submission sheet containing title, authors, abstract in arXiv-compatible TeX/ASCII, comments, compiler, top-level file, page/figure count, proposed primary category and cross-list, and license options. Count abstract characters against the current official limit. Keep journal reference and DOI blank unless they exist.
10. **Leave author decisions to the author.** Ask the author to confirm authorship and consent, category, license, disclosure accuracy, rights to all included material, and the arXiv-generated PDF preview. Never silently choose or attest to these items.

## Packaging principles

- Treat the explicit source manifest as the archive's source of truth.
- Preserve filename case exactly. Avoid spaces, hidden files, unsafe paths, duplicate archive members, and enclosing the submission in an unnecessary parent directory.
- Do not assume that a local successful build proves completeness; only the extracted archive build tests that contract.
- Do not assume source-only means “TeX only.” Include every local file TeX actually needs, including figures and local style files.
- Do not include the repository wholesale. Minimal bundles reduce accidental disclosure and arXiv processing failures.
- Keep the current generated PDF tracked when repository policy requires it, but do not put that output in the source archive merely because it is tracked.
- Regenerate the archive and checksum after every source change. Update page counts, abstract counts, reports, and metadata sheets after the final build.

## Completion standard

Report the root file and engine, archive path and checksum, file count, clean-build result, PDF page count, unresolved warnings, metadata status, scholarly-preflight status, and remaining author actions. Do not call the submission ready if the clean archive does not compile or if a required citation, disclosure, license, category, or author attestation remains unresolved.
