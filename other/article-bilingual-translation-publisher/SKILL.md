---
name: article-bilingual-translation-publisher
description: >-
  Translate one Chinese article into high-quality English Markdown,
  regenerate bilingual detailed summaries, and write back only
  `articles.content_en` + `articles.detailed_summary` to LanceDB.
  Default workflow is context-first and LLM-native generation.
---

# Single-Article Bilingual Translation and LanceDB Write-back

## When To Use
Use this skill when the user asks to:
1. Translate one Chinese article into high-quality English (`content_en`).
2. Regenerate bilingual detailed summaries (`detailed_summary.zh/en`).
3. Fix broken Markdown structure in translated content/summaries (especially tables).
4. Overwrite and write the result back to LanceDB.

## Required Context
1. Required: `../article-summary-architect/SKILL.md`
2. Recommended: `../staticflow-cli-publisher/SKILL.md`

Notes:
- Summary generation must follow `article-summary-architect` thinking order
  (classify type first, then produce structured compression).
- Summaries must not paste raw table markdown into bullets.

## Default Mode (Mandatory): LLM-native Direct Generation
Use this mode unless the user explicitly asks for another approach.

1. Read source article from current context first.
2. Generate final `content_en`, `detailed_summary_zh`, and `detailed_summary_en` directly in one pass.
3. Run lightweight structure checks.
4. Write back via `sf-cli`.

Hard rule:
- Do not call external model APIs, proxy model scripts, or sub-agent model commands for generation.
- Do not split translation into mechanical line-by-line scripts unless recovery is required.
- Tool/CLI usage is limited to source fetch, write-back, and essential validation.

## Inputs
At least one is required:
1. Article `id` (`articles.id` in LanceDB), or
2. Markdown file path.

If only `id` is provided, read source markdown from LanceDB `articles.content`.

## Resolve CLI and Query Source Article
Reuse the same query path as `staticflow-cli-publisher` only when source is not already in context.

1. Resolve CLI binary in this order:
   - `./target/release/sf-cli`
   - `./target/debug/sf-cli`
   - `sf-cli` from `PATH`
2. If the checkout is newer than the chosen binary, rebuild before use.
3. Do not prefer legacy `./bin/sf-cli` snapshots for storage-format-sensitive writes.
4. Verify CLI availability:
   - `<cli> --help`
5. Preferred query path (API-style):
   - `<cli> api --db-path <db_path> get-article <article_id>`
6. Fallback query path (DB-style projection):
   - `<cli> db --db-path <db_path> query-rows articles --where "id='<article_id>'" --columns id,title,date,content,content_en,detailed_summary --limit 1 --format vertical`
7. Source-of-truth field for translation input:
   - `articles.content`

## Hard Constraints
### English body (`content_en`)
1. Translate the full article as a coherent whole (not fragmented line-by-line output).
2. Preserve render-safe Markdown structure:
   - heading hierarchy
   - list nesting
   - code fence boundaries
   - inline code syntax
   - links/images syntax
   - table syntax (row/column structure)
3. Do not change executable code logic.
4. It is allowed (and recommended) to translate comments inside code blocks into English.
5. Do not change link/image target URLs.
6. Keep headings, list levels, tables, and fenced blocks structurally equivalent to the source.
7. Keep formulas and technical symbols intact.

### Bilingual summary (`detailed_summary`)
1. Produce `zh/en` via `article-summary-architect` reasoning.
2. Each language must contain:
   - one natural opening sentence
   - 3-5 `###` sections
   - 2-4 concise bullets per section
3. Do not paste raw table markdown into summary bullets.
4. `zh/en` must be semantically aligned and evidence-grounded (no fabricated claims).
5. Keep summaries scannable and content-specific; avoid empty template phrases.

## Recommended Workflow (Single Article)
### Step 1. Prepare minimal workspace
- Resolve target article id/file.
- Create `tmp/article_translate/<article_id>/`.
- Back up current row and key fields before overwrite.

### Step 2. Generate content directly
- Produce in one coherent pass:
  - `content_en`
  - `detailed_summary_zh`
  - `detailed_summary_en`
- Prefer article-level translation, not sentence-by-sentence conversion.

### Step 3. Lightweight structure checks
- Source vs translation:
  - same fenced-code block count
  - same Mermaid block count (if present)
  - same table block count and compatible column shape
  - same link/image target URLs
- Summary checks:
  - both languages include opening sentence + `###` sections + bullets
  - no table-markdown pollution in bullets

### Step 4. Write back to LanceDB
- Update only:
  - `articles.content_en`
  - `articles.detailed_summary` (JSON with `zh` and `en`)
- Never mutate unrelated fields (`title`, `content`, `tags`, `category`, `date`, etc.).

### Step 5. Verify after write-back
- Re-read the target article.
- Confirm:
  - `content_en` is non-empty and render-safe
  - `detailed_summary.zh/en` exists and is valid JSON structure

## LanceDB Write-back Example (`sf-cli`)
Use the built-in CLI command to update one article from files:

```bash
<cli> db --db-path <db_path> update-article-bilingual \
  --id <article_id> \
  --content-en-file tmp/content_en.md \
  --summary-zh-file tmp/detailed_summary_zh.md \
  --summary-en-file tmp/detailed_summary_en.md
```

You can also update only one side:

```bash
# only content_en
<cli> db --db-path <db_path> update-article-bilingual \
  --id <article_id> \
  --content-en-file tmp/content_en.md

# only detailed_summary.zh/en
<cli> db --db-path <db_path> update-article-bilingual \
  --id <article_id> \
  --summary-zh-file tmp/detailed_summary_zh.md \
  --summary-en-file tmp/detailed_summary_en.md
```

## Suggested tmp Layout
Use `tmp/article_translate/<article_id>/` and keep artifacts local:
- `row_backup.json`
- `source_zh.md`
- `old_content_en.md`
- `old_detailed_summary_raw.txt`
- `content_en.md`
- `detailed_summary_zh.md`
- `detailed_summary_en.md`
- `after_update.json`

## Output Report Requirements
Always report:
1. Target article id.
2. Whether `content_en` was regenerated.
3. Whether `detailed_summary.zh/en` was regenerated.
4. Structure validation result (tables/code fences/links).
5. Write-back status and version (if available).
6. Backup artifact paths under `tmp/`.
7. Whether generation followed LLM-native direct mode.

## Failure and Rollback
1. If structure checks fail: do not write back; fix first.
2. If write-back fails: keep `tmp` artifacts and output reproducible commands.
3. If post-write quality is unsatisfactory: restore from backups via the same workflow.
4. If source content is missing from context and DB lookup fails, stop and request a resolvable article id/path.
