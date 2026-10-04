---
name: pocketpolyglot-bookmaker
description: Use when creating PocketPolyglot/LinguaLeaf-style multilingual pocket books from bilingual or trilingual sources, including aligned JSON, ruby/furigana/pinyin, grammar colors, bidirectional main/comment editions, color and black-white PDFs, covers, queues, and resumable long-running generation.
triggers:
  - PocketPolyglot
  - LinguaLeaf
  - interlinear pocket book
  - bilingual book
  - trilingual book
  - ruby furigana pinyin
  - grammar-colored text
  - paired language PDF
  - multilingual JSON chunks
---

# PocketPolyglot Bookmaker

Use this skill for multilingual learning books where one language is the main text and one or more languages are aligned comments. The goal is a readable pocket-size PDF, not a raw translation dump.

## Core Rules

- Preserve completeness first: every chapter, paragraph, sentence, and chunk must be accounted for.
- Use source translations directly when available. Generate missing language only when no reliable source exists.
- Keep data and rendering separate. Generate durable JSON first; compile PDFs from JSON without regenerating text.
- For each language pair, compile both directions when renderers exist, and produce color and black-white variants.
- Do not trust page count alone. Validate manifest coverage, stale chunks, TOC, line overflow, ruby placement, and sample pages.
- For final LinguaLeaf/PocketPolyglot PDFs, default to the larger Shiji AgInTi-style font profile for readability. Name this neutrally as `large-font` / `大字版`; do not use Shiji-specific wording in public artifact names unless the book is actually Shiji.

## Data Model

Use resumable, chunk-level JSON. Prefer paragraph or small section chunks, not arbitrary huge blocks.

Required fields should include:

- stable chunk id and source location;
- chapter/section title;
- main-language text tokens with reading annotations;
- comment-language text tokens with reading annotations;
- optional third-language reference or modern translation;
- grammar role per token using one normalized vocabulary: `subject`, `predicate`, `object`, `attributive`, `adverbial`, `complement`, `topic`, `function`;
- status, reviewer notes, and validation evidence.

For Japanese, furigana goes only over kanji-bearing tokens. For Chinese, pinyin goes over the matching Chinese token. For English, preserve spaces between words during grammar coloring.

## Generation Workflow

1. Prepare sources:

```bash
find sources/<book> -maxdepth 2 -type f
```

Convert EPUB/PDF/Markdown to reviewed Markdown, then split into a manifest with stable chunk ids. Keep source references broad enough to recover context, usually chapter-level for references and chunk-level for generated output.

When a real translation PDF/EPUB exists, register it as a preferred reference before generating missing languages. If `pdftotext` yields only page chrome or too little text, create an OCR/text cache first and mark the source as OCR-required instead of silently treating it as absent. Do not let HTML, Wikisource boilerplate, PDF page headers, archive labels, copyright/public-domain notices, or OCR noise enter chunk text.

Do not split source by raw webpage/PDF line breaks. Join line-wrapped prose into paragraphs first, then split by semantic sentence or small paragraph units. Generated overlay rows should be coherent single-line prose for each unit; preserve spaces in English and avoid copying reference line breaks.

2. Generate incrementally:

- Write one chunk JSON file per chunk or shard.
- Reuse existing valid fields; do not flush old translations/ruby/grammar when adding a new feature.
- Support parallel writer workers by assigning disjoint chunk ranges and output paths.
- Keep review/sanitize asynchronous and non-destructive.

3. Review dynamically:

- Detect schema errors, missing source text, non-target-language output, HTML/wiki/page boilerplate, source layout linebreaks copied into prose, overlong ruby, missing spaces, all-one-color grammar, truncated comments, and line-alignment failures.
- Pass concrete issues to the reviewer, revalidate, and loop until fixed or marked blocked with evidence.

4. Compile:

- Main/comment directions: `zh-main`, `jp-main`, `en-main`, etc.
- Variants: `color` and `blackwhite`.
- Final share/export builds should use the larger pocket-book font profile by default, with ordinary-size builds kept only as working previews or legacy variants.
- Include title page, author with ruby when useful, cover image, TOC, and LazyingArt/AgInTiFlow credit when requested.
- Copy final PDFs to the requested book folder using clean filenames.

### Nutstore / Cloud Filename Safety

- Nutstore may accept a PDF locally but reject the cloud upload with
  `NotAcceptableByServer` when the filename contains server-unsafe characters.
  Before copying to Nutstore Share/Projects, sanitize public filenames for
  ASCII `< > : " / \ | ? *`, control characters, and trailing spaces/dots.
- Keep public titles readable by replacing unsafe ASCII punctuation with
  fullwidth equivalents, especially `:` -> `：`. Do this in the sync script
  before export, not as a manual post-copy repair.
- In this repo, new sync/export scripts should call
  `scripts/books/nutstore_paths.py:nutstore_safe_filename()`. After sync, scan
  the target tree for unsafe filenames and inspect
  `/home/lachlan/.nutstore/logs/client.log` when files exist locally but are
  missing from Nutstore cloud.
- For Share exports, keep the folder flat and user-facing, but still encode the
  language shape clearly in the filename, for example `English-日本語-中文`,
  `文言文-English-日本語-中文`, or `日本語-中文`.

## Monitoring

### PocketPolyglot Studio Browser

For visible Studio supervision, reuse the dedicated persistent browser instead
of launching temporary Chrome profiles:

```text
tmux: pocketpolyglot-studio-browser
display: :95
VNC: 127.0.0.1:5925
noVNC: http://127.0.0.1:6125/vnc_lite.html?host=127.0.0.1&port=6125&autoconnect=1&scale=1
CDP: http://127.0.0.1:9365
profile: ~/.cache/pocketpolyglot-studio-chrome
Studio: http://127.0.0.1:8766
```

Start or attach and operate it through the repository CLI:

```bash
./studio/pocketpolyglot browser start
./studio/pocketpolyglot browser status
./studio/pocketpolyglot browser progress --project PROJECT
./studio/pocketpolyglot browser chat PROJECT --read-only --profile fast "Check queue health."
```

The first explicit start persists this identity under
`.pocketpolyglot-studio/browser/config.json`; later starts reuse it. Do not
delete or replace the profile during repair. The browser supervisor recovers
Xvfb, x11vnc, noVNC, and Chrome failures without touching the independent book
job. Use `browser stop` only when explicitly requested.

Long runs should use tmux or another observable runner:

```bash
tmux capture-pane -pt SESSION -S -120
python scripts/.../report_progress.py --manifest ... --chunk-dir ...
```

If a model limit or external blocker appears, pause gracefully, keep all generated JSON, and resume from the manifest after recovery. A monitor may recompile previews from reviewed and unreviewed chunks, but it must not erase valid current data.

Quota monitoring is reactive: workers detect Codex usage exhaustion from command
output such as `usage limit`, `purchase more credits`, or `try again at`, then
sleep/retry or write a `usage_limit` status record for later resume. Use
`CODEX_USAGE_LIMIT_WAIT_SECONDS` for the retry interval, reduce `WORKERS` when
quota is scarce, and inspect `candidates/status/*.json` plus worker logs before
treating stopped chunks as real failures.

### Queue Stage Recovery

- When an interrupted book has partial current-manifest coverage, zero stale
  chunks, and an explicit still-valid pilot gate, resume at the first missing
  chunk. Do not repeat source audit, chunk preparation, or semantic pilot work.
- Treat complete current-manifest chunk coverage as immutable generation work.
  A resume must skip source audit, pilot review, and writer launch and continue
  directly at deterministic finalization.
- Record a deterministic export/audit/cover failure as
  `finalization_blocked`, with the finalizer log and concise failure evidence;
  do not downgrade it to an incomplete translation.
- Do not repeat an identical failed finalizer several times in one queue pass.
  Make one evidenced attempt, advance the queue when configured to continue on
  blockers, and retry finalization after the underlying code or asset is fixed.
- Reconcile a valid finalizer `success.json` plus current color and black-white
  maximum-language exports back into queue state. This is required after a
  manual repair so a completed book cannot remain falsely blocked.
- A finalizer waits for the writer, stall-repair, and autorepair tmux sessions.
  It may stop those project-owned producer sessions only after current-manifest
  coverage is complete with zero stale chunks.
- Generate ordinary-layout `source.tex` with `--tex-only` before canonical
  large-font export. Compile ordinary-size PDFs only when
  `KEEP_STANDARD_PREVIEWS=1`; otherwise avoid four redundant XeLaTeX passes.

## Completion Checklist

- Manifest coverage is complete with no stale chunk mismatch.
- Both directions and all requested variants compile.
- TOC is present and chapter starts begin cleanly.
- Ruby/pinyin align to their own tokens.
- Grammar colors use normalized roles and remain readable.
- Spot-checked pages show line-based alignment without truncation or overflow.
- Generated PDFs are synced to the requested destination.
- Cloud export filenames are server-safe and not rejected by the Nutstore client.
- Source code, prompts, schemas, and durable JSON are committed; large original sources stay ignored unless explicitly requested.
