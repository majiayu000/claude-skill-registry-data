---
name: dayz-search-index
description: "Builds the semantic-search index over vanilla DayZ source on P:\\ (scripts, configs, layouts, rvmats, XML, JSON) with Voyage AI embeddings in LanceDB for the dayz-rag MCP server. Use when setting up a new machine, after a DayZ update or re-extraction, or when search_dayz_source reports no index."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-search-index

Builds the vector index behind the `dayz-rag` MCP server's `search_dayz_source` tool. Follow `skills/_shared/dayz-conventions.md`.

If you only need the index and don't want to spend Voyage tokens, `/dayz-search-download` installs a prebuilt one.

## Before you run

1. The indexer runs `/dayz-preflight` first and stops if it fails (`P:\` not mounted). Preflight warnings (Tools, Workshop) don't block it. `--status` skips the gate, and so does the refusal to overwrite an existing index (below), which is checked before anything else.
2. Install the dependencies once: `python -m pip install -r "<skill-dir>\requirements.txt"` (`lancedb`, `tqdm`, `voyageai`, `python-dotenv`). The indexer exits with that command if any are missing.
3. Put a Voyage key in `.env` at the repo root (gitignored): `VOYAGE_API_KEY=pa-...`. Get one at [dash.voyageai.com](https://dash.voyageai.com). The key is found the same way the `dayz-rag` MCP server finds it (both use `.claude/mcp/dayz-rag/voyage_common.py`): a variable already set in the environment wins, then the nearest `.env` at or above the working directory, then the one at the repo (or plugin) root.

## How to run

```cmd
python "<skill-dir>\index.py" --full
```

Builds (or rebuilds) the whole index. Without `--full` it refuses, with one `[FAIL]` line and exit 1, when an index already exists (a `manifest.json` or a `lancedb/chunks.lance` table).

```cmd
python "<skill-dir>\index.py" --status
```

Prints `manifest.json` and exits; exits 1 if there is no index. It creates nothing on disk.

Other flags: `--ignore-tier-warning` skips the free-tier prompt (needed in non-interactive shells), `--force` overrides the 150,000-chunk ceiling (`CHUNK_CEILING`). Both are explained in [references/cost-and-free-tier.md](references/cost-and-free-tier.md).

After a build, restart Claude Code so the MCP server opens the new index.

## What it indexes

The indexer walks `P:\scripts`, `P:\gui`, `P:\dz`, `P:\core`, `P:\graphics` and `P:\languagecore` and picks up `.c .cpp .hpp .h .cfg .layout .rvmat .xml .json .csv`. Run `--status` to see the current chunk, file and token counts (a full build of vanilla came to 61,757 chunks when counted on 2026-10-22, with XML, JSON and CSV windowed too).

How each file type is chunked, and what an index built by an older version is missing, is in [references/chunking.md](references/chunking.md).

## Where the index lives

`~/.claude/dayz-search-index/`, per user and outside the repo:

- `lancedb/` holds the `chunks` table (1024-dim vectors).
- `manifest.json` records model, per-folder counts, rvmat duplicates skipped, total chunks, the tokens this run used, chunks reused from a checkpoint, and estimated cost.
- `file_hashes.json` records the sha256 of every indexed file, so the MCP server flags a hit stale only when the file's content changed.
- `config.json` tells the MCP server which model to embed queries with.
- `usage.log` is the local token ledger used by the free-tier check. A build appends its tokens as soon as the embed returns, before the table and manifest are written, so tokens already billed are logged even if a later step fails.
- `embed-checkpoint.bin` holds every batch embedded so far while a build runs. If the build fails or is stopped, the next `--full` reuses those vectors and embeds (and pays for) only the rest. A successful build deletes it.

## Output

```
DayZ RAG indexer

DayZ preflight

[OK]    P:\ is mounted
...     (rest of the /dayz-preflight report)

Preflight complete.

[OK]    Vanilla data: P:\dz
[OK]    VOYAGE_API_KEY loaded (ending ...wxyz)
[INFO]  Index: C:\Users\you\.claude\dayz-search-index
[INFO]  Embedding model: voyage-code-3 (1024D, via Voyage cloud)
[INFO]  Estimate rate: $0.18 per 1M tokens (Voyage pricing page is authoritative)

Walking vanilla folders: scripts, gui, dz, core, graphics, languagecore
Indexed extensions: .c, .cfg, .cpp, .csv, .h, .hpp, .json, .layout, .rvmat, .xml

  scripts/  c=<chunks>c/<files>f
  ...
  rvmat dedup:    <n> duplicates (<pct>%)

[INFO]  Resuming: <n> of <total> chunks were embedded by an earlier run (embed-checkpoint.bin)   (only after a failed run)

Embedding <n> chunks via Voyage (voyage-code-3, document mode)...
  embedding: 100%|...| <n>/<n> [<time>] <tokens> tok / ~$<cost>

[OK]    Index built: <n> chunks at C:\Users\you\.claude\dayz-search-index
[INFO]  Tokens used: <tokens>  |  Estimated cost: $<cost>
[INFO]  Embed time: <seconds>s
[INFO]  Restart Claude Code so the dayz-rag MCP server picks up the new index.
```

## Failure modes

- Missing dependency, missing `VOYAGE_API_KEY`, `P:\` not mounted, a `VOYAGE_FREE_TIER_TOKENS` that is not a positive whole number, or no chunks produced: exits 1 before any tokens are spent.
- The free-tier prompt is refused (answered no, or the shell is not interactive): one `[FAIL]` line on stderr says which, the non-interactive one names `--ignore-tier-warning`, and it exits 1 with no tokens spent.
- The startup line names the key by its last 4 characters only, so transcripts never hold a usable part of it.
- Ctrl+C during the embed prints one `[FAIL]` line, logs the tokens already spent to `usage.log` and exits 1. Ctrl+C while the index is being written rolls the files back where it can and says the index may be inconsistent; re-run with `--full`.
- Every returned vector must have 1024 values (`EMBED_DIM`). A `VOYAGE_MODEL` with other output stops at its first batch with one `[FAIL]` line naming the dimension, before anything is saved or written; the few tokens spent are logged.
- Transient Voyage errors (the SDK's `RateLimitError`, `Timeout`, `APIConnectionError`, `TryAgain`, `ServiceUnavailableError` and `ServerError`) are retried with exponential backoff, 5 attempts per batch. Any other embed failure (a bad or revoked key, for example), or a transient one still failing after the last attempt, prints one `[FAIL]` line naming the error and exits 1 before LanceDB is touched. Tokens already spent on the batches that succeeded are appended to `usage.log` first, so the next free-tier check still counts them, and those batches stay in `embed-checkpoint.bin`, so a re-run with `--full` does not pay for them again.
- The write after the embed is all or nothing. `file_hashes.json`, `config.json` and `manifest.json` are first written to `.tmp` files; the new rows go to a `chunks_staging` table and are then swapped into `chunks`; then the `.tmp` files replace the real ones, manifest last. If any step fails (a full disk, a locked file, a LanceDB error), `chunks` is left at or rolled back to its previous version and the files already replaced get their old contents back, so a new table never sits next to an old `config.json` (after a `VOYAGE_MODEL` change that would embed queries with the wrong model). The build prints one `[FAIL]` line naming the error and saying the previous index is unchanged, and exits 1. The tokens are already in `usage.log` and the vectors in `embed-checkpoint.bin`; re-run with `--full`, which then spends no tokens on them. If the rollback itself fails, the `[FAIL]` line names both errors and says the index may be inconsistent; re-run with `--full` before searching.
- A successful build deletes `release-tag.txt` (written by `/dayz-search-download`), so the download skill no longer treats the local build as an installed release; if the file cannot be deleted the build prints a `[WARN]` line and still succeeds. A failed build leaves it in place.

## Do not

- Don't index per clone. The index reflects this machine's DayZ install, not the project.
- Don't commit `.env`.
- Don't change `VOYAGE_MODEL` without a `--full` rebuild; query and document vectors must come from the same model.
