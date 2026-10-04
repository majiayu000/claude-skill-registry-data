---
name: book-audit
description: >
  Run a deterministic, sample-based BookQuality audit comparing the original
  PDF/EPUB source against its converted Markdown in
  `corpus/alan_hirsch/<book-slug>/`. Pulls 8–10 representative samples
  (chapter openings, dense paragraphs, lists, footnotes, scripture quotes,
  figures), compares character-for-character and structure-for-structure,
  flags every discrepancy (missing text, OCR errors, lost formatting, broken
  links, fabricated content, alternate-line drops), and produces a
  GREEN / YELLOW / RED status report with a recommended fix strategy.
  Use after `/book-convert` + `/book-validate` complete, or before re-uploading
  to the OpenAI vector store. Trigger phrases: "audit this book", "grade the
  conversion", "BookQuality audit", "is this corpus production-ready".
allowed-tools: Read, Write, Bash, Grep, Glob
metadata:
  pipeline_phase: "qa"
  reference: "docs/build/prompts/fix-on-the-verge.md"
---

# Book Quality Audit — BookQuality Auditor v1.0

## Purpose

You are an expert technical auditor for a high-stakes missional content platform (Movemental.ai / Alan Hirsch). Your job is to perform a deterministic, sample-based quality audit comparing original source files against their converted Markdown.

This is the same audit pattern that uncovered:

- **On the Verge** — fabricated quotation in Notes, all Ch.1 footnotes missing, character-salad figures, mislabeled chapters (RED).
- **Reframation** — fabricated paragraph in Ch.1, rewritten HORSE quote in Ch.4, placeholder footnote text in Appendix 3, all Notes prefixes stripped (RED).
- **Fast Forward to Mission** — alternate-line drops in urban-tribe callout, lost frontmatter, table-cell merges (YELLOW).

Be ruthless about accuracy. This content represents a million words of apostolic leadership material that must be pristine for the platform.

## Invocation

`$ARGUMENTS` should specify:

- **`<book-slug-or-dir>`** — Either a slug (e.g. `on-the-verge`) or a full path to `corpus/alan_hirsch/<book-slug>/`. Required.
- **`--source <path>`** — Override source PDF/EPUB. Default: auto-detect from `_inbox/`, `archive/pdf/`, or `#archive/alan-books-old/pdf/`.
- **`--samples <N>`** — Number of samples to draw. Default: `9` (covers front matter, body, Notes, appendix).
- **`--report <path>`** — Where to write the report. Default: `docs/build/audits/<book-slug>-<YYYY-MM-DD>.md`.

If the book has no PDF/EPUB in any expected location, ask the user.

## Process

### Step 1 — Inventory

1. List all `.md` files in the target book directory.
2. Get line counts per file: `wc -l corpus/alan_hirsch/<book-slug>/*.md`.
3. Locate the source PDF/EPUB and run `pdfinfo` (PDF) or check spine (EPUB) to get total pages.
4. Extract source text once for grep / cross-reference:
   ```bash
   mkdir -p /tmp/<book-slug>-audit
   pdftotext -layout "<source.pdf>" /tmp/<book-slug>-audit/source.txt
   ```

### Step 2 — Pick samples

Aim for varied coverage. Required samples:

| # | Sample type | Target |
|---|---|---|
| 1 | Foreword opening | front matter ch |
| 2 | Preface or second foreword | front matter ch |
| 3 | Introduction opening | front matter ch |
| 4 | Chapter 1 opening + first body paragraphs | body ch |
| 5 | Mid-book chapter with dense prose | body ch |
| 6 | Body chapter with epigraphs / poems / multi-paragraph blockquotes | body ch |
| 7 | Body chapter with figures / tables / lists | body ch |
| 8 | Notes chapter — verify footnote numeric prefixes match body refs | back matter |
| 9 | Appendix or Afterword | back matter |
| 10 | (optional) Random body paragraph picked by `shuf` | body ch |

For each sample, locate **both** the PDF passage (by `grep` against `source.txt`) and the corresponding MD section.

### Step 3 — Compare each sample

For every sample, check **all** of:

- **Verbatim text fidelity** — character-for-character match on body prose. Any rewrite, paraphrase, or "improvement" is a HIGH-severity finding.
- **Paragraph breaks** — does the MD preserve blank lines where the PDF has paragraph breaks?
- **Heading hierarchy** — does the MD have exactly one `##` (chapter title) plus appropriate `###`/`####` sub-sections? Are byline / epigraph attributions / figure captions correctly NOT rendered as headings?
- **Footnote markers** — body refs use `[^N]` Markdown syntax, not bare `[N]`, raw `^N`, or stranded inline digits. Every body ref has a matching definition in the Notes file.
- **Multi-paragraph blockquotes** — when a quote spans multiple PDF paragraphs, does each paragraph have its `>` marker? Is the attribution inside the blockquote (em-dash) or outside (incorrect h2)?
- **Alternate-line drops** — long blockquotes where every other PDF line is missing, leaving fragments. Detect by reading `>` runs and checking each line ends mid-thought.
- **Figures** — character-salad fragments (`M A C S Y E / —I R H M O T —S T I A...`) indicate OCR/extraction failure. Mark for image extraction.
- **Page-header bleed** — `[a-z]- [0-9]+ Foreword by ...` style mid-sentence interruptions.
- **Kerning artifacts** — `Mc Neal`, `Mome ntu m`, `ser vice`, `C H U R C H` from InDesign tracked-out type.
- **Word-joining at line breaks** — `thebook`, `fastforward`, `Crossdomain`, `Amissional`, `Re Jesus`.
- **Stray spaces** — `Fool 's`, `_Missio Dei_ ,` (space inside italic markup).
- **Italic markup** — book titles, Latin terms (e.g. *On the Verge*, *Missio Dei*, *ecclesia*) consistently italicized.
- **Frontmatter integrity** — `canonical_title`, `display_title`, `chapter_title` match PDF; `Opening excerpt` reflects current body; `content_sha256` is current.
- **Placeholder text** — literal `Footnote reference 1`, `[PENDING-REVIEW]` strings in published content (the latter is acceptable per Phase 5 convention; the former is a bug).
- **Section dividers** — `Section One: A Reduction`-style part-divider headings should not be merged into the wrong chapter file.

### Step 4 — Score and report

Use the rubric:

| Issues found | Status |
|---|---|
| 0 critical, ≤ 3 low-severity | 🟢 GREEN — production-ready |
| 0 critical, > 3 low / any medium | 🟡 YELLOW — minor fixes needed |
| any HIGH or CRITICAL (rewrite, fabrication, missing chapter, alternate-line drops, missing footnote prefixes book-wide, placeholder text in published content) | 🔴 RED — significant issues, do not use yet |

Compute an overall accuracy estimate (subjective, sample-weighted).

### Step 5 — Output the report

Strictly follow this structure:

```markdown
# BOOK QUALITY AUDIT — <Book Title>

**Source PDF:** <path>
**Converted MD:** corpus/alan_hirsch/<book-slug>/ (<N> files, <N> lines)
**Samples taken:** <N> across <areas>.

---

## BOOK STATUS SUMMARY

- **Overall Accuracy Estimate:** ~XX% (based on samples)
- **Status: 🟢 GREEN | 🟡 YELLOW | 🔴 RED — <one-line verdict>**

<2–4 sentence summary of what's broken vs intact>

---

## DETAILED FINDINGS

### Sample 1 — <description, e.g. "Foreword by X (front matter)">
- **Original (PDF p. N):** "<verbatim PDF text>"
- **Converted (line N):** "<actual MD text>"
- **Issues found:** <list every discrepancy>
- **Severity: Low | Medium | High**

[Repeat for all samples]

---

## PATTERN ANALYSIS

**Most common error types (highest impact first):**
1. ...
2. ...

**Estimated total impact across the full book:**
- ...

**Recommended fix strategy:**
1. ...
2. ...

---

## NEXT ACTIONS

- **Immediate — do NOT run any automated fix script on these files yet.** OR (for GREEN books) **Production-ready, advance to /book-frontmatter or /book-ingest**.
- **Manual review needed for:** <list>
- **Recommended:** <re-convert | targeted fix | re-archive>
- **Archive current MD:** Move to `_archive/<book-slug>-<YYYY-MM-DD>-<reason>/` before re-conversion.

**END OF AUDIT**
```

### Step 6 — Persist the report

Write to `docs/build/audits/<book-slug>-<YYYY-MM-DD>.md` (create the directory if needed) AND emit the same content to the user.

### Step 7 — Recommend the next skill

- 🟢 GREEN → `/book-frontmatter` (Phase 02) or `/book-ingest` (Phase 03)
- 🟡 YELLOW or 🔴 RED → `/book-fix <book-slug>` to generate or run a remediation prompt
- If the audit found content rewrites or alternate-line drops that suggest the **conversion itself** is at fault, recommend re-running `/book-convert` with a different strategy.

## Operating Principles

1. **The PDF is the source of truth.** When MD and PDF disagree, the MD is wrong.
2. **Verbatim only.** Any rewrite or paraphrase, however minor, is a HIGH-severity finding. Hirsch's voice is the corpus's value.
3. **No false positives.** Every flagged issue must be reproducible — quote both the PDF and the MD verbatim with line/page numbers.
4. **Look for invisible damage.** Heading hierarchy, footnote-syntax mixing, character-salad figures, and page-header bleed are the bugs that pass spell-check but break RAG.
5. **Cross-reference everything.** Every body footnote ref must have a Notes-file definition; every section divider must be in the right chapter file; every figure caption must have visible text.

## Anti-patterns

- ❌ Reporting "looks fine" without quoting the actual PDF and MD passages side by side.
- ❌ Counting only sentence-level diffs and ignoring structural defects (heading levels, footnote syntax, attribution formatting).
- ❌ Skipping the Notes chapter — it's where the worst damage usually hides (missing prefixes, fabricated quotes).
- ❌ Calling something GREEN without verifying at least one Notes cross-reference works end-to-end.

## References

- [docs/build/prompts/fix-on-the-verge.md](../../../docs/build/prompts/fix-on-the-verge.md) — exemplary remediation prompt
- [docs/build/prompts/fix-reframation.md](../../../docs/build/prompts/fix-reframation.md) — second exemplar
- [docs/build/prompts/fix-fast-forward-to-mission.md](../../../docs/build/prompts/fix-fast-forward-to-mission.md) — earliest exemplar
- [docs/html/books-pipeline.html#validation](../../../docs/html/books-pipeline.html#validation)
