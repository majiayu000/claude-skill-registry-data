---
name: book-citations
description: >-
  Deterministic footnote/endnote restoration and citation-form cleanup for movemental
  books: extract from PDF/EPUB (PyMuPDF / ebooklib), match anchors, stage [^n] markers,
  compile to noteref HTML + chapter_notes, convert-hook assertions, review queue. Use when
  restoring citations, fixing [^n]n duplicates or bare digits, Phase 5 citation integration,
  convert_hook, or assert_notes_markers — never invent note bodies or marker positions.
disable-model-invocation: true
---

# Book citations

Restore and normalize footnotes/endnotes for one book at a time. **This is not an LLM
placement task.** Superscript detection and note bodies come from source geometry/markup;
the agent only runs scripts, clears form defects, and places residuals that already cleared
confidence gates (or human review).

**Primary repo:** books workspace with `scripts/citations/`  
**Database:** Supabase `vhaiiiykcukrlyvwlgip` (`movemental`) — ask before destructive writes  
**Companion cleanup:** [[book-faithful-cleanup]] (full PDF→Markdown recipe embeds this as Phase 5)

## Invocation

```
/book-citations {book_slug}                    # full extract → match → form → integrate
/book-citations {book_slug} form-only          # normalize [^n] form in corpus/cleanup MD
/book-citations {book_slug} phase5             # compile [^n] → noteref + assert vs notes JSON
/book-citations {book_slug} extract-only       # refresh data/citations/{slug}.json
```

Run from the **books** repo root (or pass absolute paths). One book per run.

## Prime directives

1. **Never guess a marker position.** Wrong sentence > missing citation. Below threshold → review queue, not DB.
2. **Never invent note bodies or CSL.** Empty `chapter_notes.body` is a failure mode (the 5Q bug).
3. **Idempotent.** Re-run must not duplicate notes or double-insert markers (`already_has_marker`).
4. **Snapshot before every DB write** (`recon.snap_chapter_content_citations` or equivalent).
5. **Canonical staging form in Markdown:** clean Pandoc `[^n]` only — not `[^n]n`, bare `6`, `^n`, or `[^n](Ibid.)`.
6. **Canonical loaded form in HTML/DB:** `<sup class="noteref" data-note="N">N</sup>` + `chapter_notes` rows.
7. **Scanned PDFs (no text layer):** out of scope. Report and stop.
8. Ask before destructive DB changes (wipe notes, replace book, delete chapters).

## Target models

| Layer | Marker | Notes storage |
|-------|--------|----------------|
| Cleanup / corpus MD | `[^n]` (no trailing duplicate digit) | `data/cleanup/{slug}/db/notes/` and/or `data/citations/{slug}.json` |
| Supabase HTML | `<sup class="noteref" data-note="N">N</sup>` | `chapter_notes` (`body` never empty; `note_type` ∈ footnote\|endnote\|sidenote) |
| Corpus `chNN-notes.md` + empty `citations: []` | Formatting reference for **prose only** | **Not** the Hirsch/movemental citation design |

## Scripts (do not reimplement)

| Job | Module |
|-----|--------|
| PDF extract (span geometry) | `scripts/citations/pdf_extract.py` |
| EPUB extract | `scripts/citations/epub_extract.py` |
| Normalize / anchors | `scripts/citations/normalize.py` |
| Match chapters | `scripts/citations/match.py` |
| Insert / idempotent load helpers | `scripts/citations/load.py` |
| Post-convert assert | `scripts/citations/assert_notes_markers.py`, `convert_hook.py` |
| Phase 5 compile MD→HTML | `scripts/citations/generic_phase5_compile.py` (or book-specific `*_cleanup_pipeline.py`) |
| Form normalize `[^n]n` / bare / caret / linkish | `scripts/corpus_fix_citations.py` |
| Defect scan (`dup_fn`, glued, caret) | `docs/problem-examples-two/_scan_defects.py` |
| Review queue CLI | `scripts/citations/review_cli.py` |

Install deps if missing: `pip install pymupdf pymupdf4llm ebooklib beautifulsoup4 lxml rapidfuzz`

## Match thresholds

| Score | Action |
|------:|--------|
| ≥ 0.95 | Auto-apply marker insert |
| 0.80–0.95 | `recon.citation_review_queue` |
| < 0.80 | Reject + report |
| Ambiguous (anchor hits >1 place) | Reject regardless of score |

## Progress checklist

```
book-citations:
- [ ] 0 Inventory source (text layer? PDF/EPUB path; prior JSON)
- [ ] 1 Extract → data/citations/{slug}.json (or author data/citations/)
- [ ] 2 Form cleanup on corpus + cleanup MD (dup_fn=0)
- [ ] 3 Match to chapters (seed/DB/working HTML or MD)
- [ ] 4 Apply notes + markers (snapshot first if DB)
- [ ] 5 Phase 5 compile / assert_notes_markers
- [ ] 6 Review queue residuals; convert_hook wired for future ingest
- [ ] 7 Report counts (extracted / matched / applied / queued / rejected / gaps)
```

---

## Phase 0 — Inventory

1. Resolve `book_slug`, `source_path` (PDF or EPUB), prior `data/citations/{slug}.json` if any.
2. Confirm text layer (`fitz`: empty `get_text()` ⇒ scanned ⇒ stop).
3. Note whether working tree is `data/cleanup/{slug}/`, corpus seed, and/or live Supabase chapters.
4. Record page count, format, ISBN vs `books.isbn` when edition risk exists.

**Stop and report** unless user said continue.

---

## Phase 1 — Extract (no DB writes)

```bash
# PDF
python -c "from scripts.citations.pdf_extract import extract_pdf; ..."
# EPUB
python -c "from scripts.citations.epub_extract import extract_epub; ..."
```

Or book pipelines / `phase1_ground_truth.py` when body oracle is also needed.

**PDF rules:** modal body font size per page; superscript = ~50–85% of body size + raised baseline + `^\d{1,3}$`; capture **~60 chars preceding text** as anchor (verbatim). Footnote bodies at page foot and/or endnotes section.

**EPUB:** real markup (`epub:type="noteref"`, `<sup>`, id/href). Prefer EPUB when same edition exists.

**Output:** `{book_slug, chapter_hint, note_number, marker_anchor_text, note_body, source_page}` → `data/citations/{slug}.json` (Brad/author trees may use `{Author}/data/citations/`).

Reuse existing JSON when source bytes + extractor version unchanged.

---

## Phase 2 — Citation form cleanup (Markdown)

Desired form: `…place.[^2]` — **not** `[^2]2`, bare `"…God."6`, `^2`, or `[^8](Ibid.)`.

```bash
python scripts/corpus_fix_citations.py --book {slug}          # or full corpus
python scripts/corpus_fix_citations.py --dry-run --book {slug}
```

Passes (in order):

1. Strip duplicate digits: `[^n]n` → `[^n]` (same number; use `(?!\d)` so `[^4]4The` matches)
2. Wrap residual bare endnote digits after closing punct/quote → `[^n]` (abbrev false-positive filter)
3. Fix `[^n](...)` linkish → `[^n]`; caret `^n` → `[^n]` when footnote-shaped

Gate: `dup_fn=0` in `_scan_defects.py` / remediation RG5. Do **not** delete glued digits without restoring via extract+match.

---

## Phase 3 — Match

1. Resolve chapter via title normalize + `sort_order` (DB `chapter_number` from source is not authoritative).
2. Normalize both sides (`normalize_for_match`: strip HTML, NFKC, collapse ws, smart quotes).
3. Locate anchor; exact then `rapidfuzz`.
4. Bucket auto / review / reject per thresholds above.

---

## Phase 4 — Load / apply

**Markdown working tree (preferred during cleanup):**

- Insert `[^n]` at matched points (idempotent).
- Persist note bodies under `data/cleanup/{slug}/db/notes/` (`_all.json` and/or per-chapter).
- Strip loose note-body paragraphs only after bodies are preserved in notes JSON.

**Supabase:**

1. Snapshot chapter HTML.
2. Upsert `chapter_notes` on `(chapter_id, note_number)` — **non-empty body only**.
3. Insert `<sup class="noteref" data-note="N">N</sup>` via `insert_marker` / skip if `already_has_marker`.
4. Remove redundant `<p><sup>N.</sup> …</p>` only for preserved note numbers.
5. Fix empty-bodied shells (fill from extract or delete) — never leave empty rows.

---

## Phase 5 — Compile + assert

```bash
python scripts/citations/generic_phase5_compile.py {slug}
# or book-specific pipeline phase5
python scripts/citations/assert_notes_markers.py --dir data/cleanup/{slug}/compiled_html
```

Compile maps `[^n]` → noteref. Report missing markers vs notes JSON. Numbering **gaps** are findings — do not renumber to hide them.

---

## Phase 6 — Review queue + convert hook

- Residuals → `recon.citation_review_queue` + `review_cli.py` (accept applies same insert).
- Wire future ingest: `scripts/citations/convert_hook.py` — extract on convert, emit noteref + notes in same transaction, **fail** if note bodies exist without markers. See [reference.md](reference.md).

---

## Failure forms (CIT taxonomy)

| Form | Example | Fix |
|------|---------|-----|
| Clean Pandoc | `.[^2]` | Keep |
| Duplicate digit | `.[^2]2` / `[^4]4The` | `corpus_fix_citations` pass 1 |
| Bare glued digit | `"…God."6` | Pass 2 or extract+match |
| Caret | `."^2` / `.^10` | Pass 3b |
| Linkish | `[^8](Ibid.)` | Pass 3a |
| Stuck / glued | `word12`, `.12` | Match pipeline — do not delete |
| Orphan `[^n]` no body | refs without notes plan | Extract + notes JSON |
| Loose bodies in HTML | `<p><sup>1.</sup> …` | Move to `chapter_notes`, then strip |
| Empty DB shells | 5Q-style | Fill or delete |

Evidence catalogs: `docs/problem-examples/05-broken-citations.md`, `docs/problem-examples-two/05-broken-citations.md`.

## Anti-patterns

- Sending chapter text to a model to “find the footnotes”
- Treating corpus notes chapters as the final citation store for movemental books
- Deleting glued digits instead of restoring noterefs
- Renumbering notes to hide gaps
- Loading without snapshot
- Skipping form cleanup so Phase 5 compiles `[^n]n` garbage

## Done report

Per book: extracted / matched / applied / queued / rejected / `dup_fn` / marker vs note equality / open gaps. Link review-queue IDs. State whether convert_hook is wired for the next ingest.

## Additional resources

- Convert hook + assertion contract: [reference.md](reference.md)
- Full cleanup recipe (Phases 0–7 + `/loop`): skill `book-faithful-cleanup`
