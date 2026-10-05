---
name: staticflow-cli-publisher
description: >-
  Publish and verify StaticFlow content in LanceDB via `sf-cli`: write
  articles/images, sync notes, infer missing metadata, and run local API
  checks. This skill is not a live-table repair or corruption-recovery playbook.
---

# StaticFlow CLI Publisher

Use this skill to publish Markdown/blog notes into LanceDB and verify results.
It is a publish/verify skill, not a table-repair skill.

## When To Use
1. Publish one Markdown article (`write-article`).
2. Batch import images (`write-images`) or sync a notes directory (`sync-notes`).
3. Query/update/upsert data in `articles`, `images`, and `taxonomies`.
4. Update bilingual fields from files (`db update-article-bilingual`).
5. Backfill article vectors (`db backfill-article-vectors`).
6. Run backend-equivalent local API queries for verification/debug.
7. Do routine post-batch index coverage only after successful writes on healthy tables.
8. Manually complete a music wish (`complete-wish`).

## Execution Policy (Mandatory)
- Context-first: read article and metadata from current context/local files first.
- LLM-native generation: generate missing metadata and summary directly in-session.
- Do not call external model APIs, proxy scripts, or sub-agent model commands.
- Use CLI only for fetch fallback, write/sync, and verification.
- Keep intermediate artifacts under `/tmp/`, not in the project root directory.
- Never run destructive operations unless explicitly requested.
- Treat duplicate-key, merge-ambiguity, and scalar-index errors as storage-integrity incidents,
  not routine publish failures.
- On a live production DB with a running backend, do not improvise repair by chaining
  `delete-rows`, `drop-index`, `ensure-indexes`, `optimize --all --prune-now`,
  `cleanup-orphans`, or `rebuild-table-stable`.
- If storage maintenance or table repair is the main task, switch to
  `lancedb-optimize` or an explicit repair workflow instead of continuing this skill.

## Load Extra Context
- Required: `references/publish-checklist.md`
- If summary generation is needed: `../article-summary-architect/SKILL.md`
- Optional docs: `README.md`, `docs/cli-user-guide.zh.md`

## Preconditions
1. Resolve CLI in this order:
   - `./target/release/sf-cli`
   - `./target/debug/sf-cli`
   - `../target/release/sf-cli`
   - `sf-cli` from `PATH`
2. Verify CLI works: `<cli> --help`
   - Build if needed: `cargo build -p sf-cli --release`
3. If the checkout is newer than the chosen binary, rebuild before use.
4. Do not prefer legacy `./bin/sf-cli` snapshots for storage-format-sensitive writes.
5. Verify DB path exists.
6. Verify DB tables:
   - `<cli> db --db-path <db_path> list-tables`
   - required: `articles`, `images`, `taxonomies`
   - current content DB may also include runtime tables such as `article_views`,
     `api_behavior_events`, `article_requests*`, and `interactive_*`
7. If DB is uninitialized, ask user before:
   - `<cli> init --db-path <db_path>`

## Hard Stop Conditions (Mandatory)
Stop the normal publish workflow immediately if any of these appear:
1. `Ambiguous merge inserts`
2. `RowAddrTreeMap::from_sorted_iter called with non-sorted input`
3. Duplicate taxonomy/article key errors that persist after input-side dedupe
4. Full-list reads succeed but filtered single-row reads fail on a long-running backend
5. Any sign that the target table/index layout is already unhealthy

Required response:
1. Stop retries and stop mutating the affected tables.
2. Capture diagnostics first:
   - `<cli> db --db-path <db_path> audit-storage --table <table>`
   - `<cli> db --db-path <db_path> list-indexes <table> --with-stats`
   - targeted `query-rows` / `count-rows`
3. Preserve rollback state before repair.
4. Escalate to a stable-row-id rebuild / temp-DB rewrite workflow.
5. If a table directory is rebuilt or swapped while backend is still running, assume the old
   backend may keep a stale manifest/index view; validate with a fresh process and plan
   blue-green restart before switching traffic.

## Publication Workflow

### A) Single Article (`write-article`)
1. Read Markdown body/frontmatter.
2. Ensure required metadata in final payload:
   - `summary`
   - `tags`
   - `category`
   - `category_description`
   - when bilingual publish is requested: `content_en` and `detailed_summary.zh/en`
3. Metadata priority:
   - frontmatter
   - explicit user CLI args
   - skill inference from content + existing taxonomy records
4. Preserve source date:
   - use `--date` when user provides it
   - else keep frontmatter `date`
   - else derive from file birth time/mtime (`YYYY-MM-DD`) and pass `--date`
5. Summary gate (before publish):
   - regenerate `detailed_summary.zh/en` when missing/stale/unstructured
   - follow `article-summary-architect` quality contract
6. Publish command:
   - frontmatter complete:
     - `<cli> write-article --db-path <db_path> --file <post.md>`
   - frontmatter incomplete:
     - `<cli> write-article --db-path <db_path> --file <post.md> --summary "..." --tags "a,b" --category "..." --category-description "..."`
   - with custom id:
     - `--id <custom_id>` (defaults to markdown file stem)
   - with explicit date:
     - `--date YYYY-MM-DD`
   - explicit bilingual files (preferred for non-frontmatter workflow):
     - `<cli> write-article --db-path <db_path> --file <post.md> --summary "..." --tags "a,b" --category "..." --category-description "..." --content-en-file <content_en.md> --summary-zh-file <summary_zh.md> --summary-en-file <summary_en.md>`
   - with pre-computed vectors:
     - `--vector <json_array>` / `--vector-en <json_array>` / `--vector-zh <json_array>`
   - with auto-embedding language hint:
     - `--language en|zh`
   - disable auto-optimize after write:
     - `--no-auto-optimize`
   - `--no-auto-optimize` is only for healthy-table publish batching; it is not a repair switch
7. Local image import (optional):
   - `--import-local-images`
   - optional `--media-root <path>` (repeatable)
   - optional `--generate-thumbnail --thumbnail-size <n>`
   - supports `![](path)`, `![[path]]`, `![[path|alias]]`
8. Verify publication:
   - article row exists
   - taxonomy rows updated
   - images imported when expected
   - `sf-cli api get-article <id>` returns the updated row on a fresh CLI connection
   - if any verification step throws merge/index integrity errors, stop instead of attempting
     ad-hoc maintenance
9. Report:
   - article id
   - inferred metadata (if any)
   - summary generated/reused
   - bilingual fields generated/reused (`content_en`, `detailed_summary.zh/en`)
   - image import count and warnings

### B) Image Batch (`write-images`)
`<cli> write-images --db-path <db_path> --dir <image_dir> [--recursive] [--generate-thumbnail] [--thumbnail-size <n>] [--no-auto-optimize]`

Storage note:
- `images.data` is blob v2 in current production layout
- `images.thumbnail` remains regular `Binary`
- prefer verifying image readability through `<cli> api get-image ...` instead of assuming raw Arrow `Binary`

### C) Notes Sync (`sync-notes`)
`<cli> sync-notes --db-path <db_path> --dir <notes_dir> [--recursive] [--generate-thumbnail] [--thumbnail-size <n>] [--language <en|zh>] [--default-category <name>] [--default-author <name>] [--no-auto-optimize]`

## DB and API Quick Map
- Safe publish/debug ops: `<cli> db --db-path <db_path> <subcommand>`
  - table info: `list-tables`, `describe-table <table>`, `count-rows <table> [--where ...]`
  - targeted data checks: `query-rows`, `update-rows`, `list-indexes <table> [--with-stats]`
  - upsert: `upsert-article --json <json>`, `upsert-image --json <json>`
  - bilingual: `update-article-bilingual --id <id> [--content-en-file ...] [--summary-zh-file ...] [--summary-en-file ...]`
  - vectors: `backfill-article-vectors [--limit N] [--dry-run]`
  - special: `reembed-svg-images [--limit N] [--dry-run]`
  - schema: `create-table <table>`
- Escalation-only repair/maintenance ops:
  - `delete-rows`
  - `ensure-indexes`, `drop-index <name>`
  - `optimize`, `cleanup-orphans [--table <table>]`
  - `rebuild-table-stable <table>`, `migrate-images-blob-v2`, `drop-table <table> --yes`
  - only use these when the user explicitly asked for DB repair/maintenance and you have a
    rollback and verification plan
- API-equivalent ops: `<cli> api --db-path <db_path> <subcommand>`
  - articles: `list-articles [--tag ...] [--category ...]`, `get-article <id>`, `related-articles <id>`
  - search: `search --q "..."`, `semantic-search --q "..."`
  - taxonomy: `list-tags`, `list-categories`
  - images: `list-images`, `get-image <id-or-filename>`, `search-images --id <id>`, `search-images-text --q "..."`
- Legacy query shortcut: `<cli> query --table <table> [--where ...] [--columns ...] [--limit N] [--offset N] [--format table|vertical]`

## Healthy-Table Post-Batch Maintenance
Only after the writes have already succeeded and the affected tables are healthy:
- If you intentionally used `--no-auto-optimize` for batching, finish with:
  - `<cli> db --db-path <db_path> optimize articles`
  - `<cli> db --db-path <db_path> optimize images`
- Use `cleanup-orphans` / `optimize --all --prune-now` only as explicit storage maintenance,
  not as write-failure recovery.
- If compaction/prune is the main task, use the `lancedb-optimize` skill.

## Error Handling
- Missing metadata: infer and continue, but report inferred fields explicitly.
- Image resolution warnings: rerun with `--media-root`.
- Partial success: rerun only failed steps, then verify again.
- Integrity symptoms (`Ambiguous merge inserts`, `non-sorted input`, repeated duplicate keys,
  stale-backend manifest mismatch) are stop conditions, not retry conditions.
- Never use `delete-rows`, `drop-index`, `ensure-indexes`, `optimize`, `cleanup-orphans`, or
  `rebuild-table-stable` as an ad-hoc response to a failed write on a live production DB.
- Never run `drop-table` or `delete-rows --all` unless user explicitly requests it.
