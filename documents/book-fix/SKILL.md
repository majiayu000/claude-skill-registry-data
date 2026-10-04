---
name: book-fix
description: >
  Generate or execute a comprehensive remediation prompt for a YELLOW or RED
  book identified by `/book-audit`. Writes a `fix-<book-slug>.md` to
  `docs/build/prompts/` enumerating every defect with verbatim PDF source
  text inlined for verbatim restoration, then optionally executes the prompt
  to bring the book to GREEN. Mirrors the exemplar structure of
  `fix-on-the-verge.md` and `fix-reframation.md`. Use after `/book-audit`
  returns YELLOW or RED. Trigger phrases: "fix this book", "remediate the
  conversion", "execute the fix prompt", "bring it to green".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  pipeline_phase: "qa-fix"
  reference: "docs/build/prompts/fix-on-the-verge.md"
---

# Book Fix — Remediation Prompt Generator + Executor

## Purpose

Take the findings from a `/book-audit` and convert them into a one-shot, end-to-end remediation prompt that another agent (or this one) can execute to bring the book to GREEN. Or, if the user prefers, execute the fix in place.

The output prompt MUST follow the structure established by [fix-on-the-verge.md](../../../docs/build/prompts/fix-on-the-verge.md) and [fix-reframation.md](../../../docs/build/prompts/fix-reframation.md):

1. **Header** — RED/YELLOW status declared, rationale, what's distinctive about this book's defects.
2. **INPUTS** — PDF path, target MD files, scratch dirs, archive dir.
3. **OPERATING PRINCIPLES** — verbatim only, PDF is source of truth, no fabrication.
4. **ISSUES TO FIX** — numbered, each with: file path, problem, current (wrong) text, PDF source (correct) text inlined, fix instructions, verification grep commands.
5. **EXECUTION ORDER** — strict dependency-ordered sequence.
6. **ACCEPTANCE CRITERIA** — checkbox list of every condition that must hold post-fix.
7. **DELIVERABLES** — what the executing agent must return.
8. **OUT OF SCOPE** — explicitly excluded items (summaries, vector store re-upload, translations).

## Invocation

`$ARGUMENTS` should specify:

- **`<book-slug>`** — Required.
- **`--audit <path>`** — Path to the prior `/book-audit` report. Default: most recent file under `docs/build/audits/<book-slug>-*.md`.
- **`--mode <generate|execute|both>`** — Default: `generate` (write the prompt without executing).
  - `generate` — write `docs/build/prompts/fix-<book-slug>.md` and stop.
  - `execute` — read existing fix prompt and execute every issue.
  - `both` — generate and execute back-to-back.
- **`--archive-dir <path>`** — Where to pre-archive the current MD before edits. Default: `corpus/alan_hirsch/_archive/<book-slug>-<YYYY-MM-DD>-<reason>/`.

## Process

### Generate mode

1. **Read the audit report.** Extract every numbered Sample with its findings, severity, and suggested fix.
2. **Group findings by class.** The exemplar prompts use these stable issue groupings (renumber as needed for the new book):
   - **CRITICAL correctness** — fabricated content, rewritten paragraphs, placeholder text, content rewrites.
   - **Notes-chapter restoration** — missing footnote prefixes, mislabeled chapters, missing chapter blocks, fabricated quotations.
   - **Multi-paragraph blockquote continuation drops.**
   - **Alternate-line content drops** in long-form quotations.
   - **Heading hierarchy collapse** (book-wide pass).
   - **Footnote-syntax standardization** (bracketed `[N]`, caret `^N`, Markdown `[^N]`).
   - **Page-header / page-footer bleed.**
   - **Kerning artifacts** (letter-spaced caps, joined words).
   - **Stray spaces / italic markup loss.**
   - **Misplaced section dividers.**
   - **Frontmatter integrity** (canonical_title, opening_excerpt, content_sha256, word_count).
   - **Comprehensive un-audited-chapter sweep.**
3. **Inline verbatim PDF source text** for every CRITICAL fix. Run `grep` against the source PDF text to copy the exact original passage. This is non-negotiable — the executing agent cannot restore content it cannot see.
4. **Provide verification commands** for every issue using `grep -c`, `grep -nE`, or Python one-liners. Each issue must have a binary pass/fail check.
5. **Write the prompt** to `docs/build/prompts/fix-<book-slug>.md`.
6. **Render a summary** to the user listing every issue number with its one-line description.

### Execute mode

1. **Read the prompt.** Verify it exists at `docs/build/prompts/fix-<book-slug>.md`.
2. **Pre-archive** the current MD to `corpus/alan_hirsch/_archive/<book-slug>-<YYYY-MM-DD>-pre-fix/`.
3. **Extract PDF reference text** to `/tmp/<book-slug>-fix/source.txt`.
4. **Walk the issues in execution order** as specified by the prompt. For each:
   - Apply the fix using `Edit` or `Write` tools.
   - Run the verification command immediately after.
   - If verification fails, do **not** advance — investigate and re-apply.
5. **After all issues are fixed:**
   - Re-run universal sweeps: trailing whitespace, kerning artifacts, word-joining, page-header bleed.
   - Recompute frontmatter `content_sha256`, `word_count`, `char_count`, `estimated_reading_time` for every edited file.
   - Update `book.json` totals.
6. **Run final acceptance verification.** Walk every checkbox in the prompt's Acceptance Criteria; report PASS/FAIL per item.
7. **Recommend the next skill.** If all PASS, advance to `/book-frontmatter` (Phase 02 schema validation) or directly to `/book-ingest` (Phase 03).

## Operating Principles

1. **The PDF is the source of truth.** Every restoration must be character-faithful to the PDF.
2. **Inline verbatim source text in the prompt.** The executing agent cannot restore what it cannot see; do not write "look up the original passage" — copy it.
3. **Provide verification commands for every fix.** Every issue gets a `grep -c` or equivalent that returns 0 or 1, not "review the diff".
4. **Issue ordering matters.** Fabrication fixes first (so the body is correct before structural passes run), Notes rebuild before footnote-syntax standardization (so refs can match definitions), heading hierarchy book-wide before per-chapter spot fixes.
5. **No speculative restoration.** If the PDF is unclear, leave a `<!-- TODO: verify against print PDF p.NN -->` and document it in the deliverables. Do not invent text.
6. **Pre-archive every time.** The current MD may contain hand-edits; preserve them under `_archive/` before any sed/script run.

## Anti-patterns

- ❌ Writing a fix prompt without inlining the verbatim PDF source text for fabrication fixes.
- ❌ Issuing fixes in non-dependency order (e.g., footnote-syntax conversion before Notes-chapter rebuild).
- ❌ Running automated sweeps (sed across all files) before the critical correctness fixes — sweeps may collide with hand edits or paraphrase content the script can't distinguish.
- ❌ Marking the book GREEN without re-running `/book-audit` against the post-fix MD.

## References

- [docs/build/prompts/fix-on-the-verge.md](../../../docs/build/prompts/fix-on-the-verge.md) — RED-status exemplar with 20 issues.
- [docs/build/prompts/fix-reframation.md](../../../docs/build/prompts/fix-reframation.md) — RED-status exemplar with 17 issues, footnote-syntax pivot.
- [docs/build/prompts/fix-fast-forward-to-mission.md](../../../docs/build/prompts/fix-fast-forward-to-mission.md) — YELLOW-status exemplar with 13 issues.
