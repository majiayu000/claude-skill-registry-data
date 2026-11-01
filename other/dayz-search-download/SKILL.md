---
name: dayz-search-download
description: "Downloads the prebuilt DayZ RAG search index from the repo's GitHub releases, verifies its SHA-256 and installs it for the dayz-rag MCP server. Use when setting up a fresh machine instead of building the index locally with /dayz-search-index."
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-search-download

Pull the prebuilt vanilla-source vector index from the repo's GitHub releases instead of building it locally with `/dayz-search-index`, skipping the local build and its Voyage API embedding cost.

Follow `skills/_shared/dayz-conventions.md`.

## When to use this vs. `/dayz-search-index`

| Scenario | Use |
|---|---|
| Fresh clone, just want DayZ agents to work | `/dayz-search-download` |
| You re-extracted vanilla data after a DayZ update | `/dayz-search-index --full` (rebuild against your local data) |
| You changed embed model in `.env` | `/dayz-search-index --full` |

The downloaded index is built against vanilla DayZ at the release-tagged version. If your local DayZ install is on a newer patch and you need precise recall against your installed source, rebuild locally.

## Where it lands

`~/.claude/dayz-search-index/`, the same path `/dayz-search-index` writes to. Per-user, outside the repo, survives clones.

Releases have published the index under two asset names, `dayz-rag-index-v0.1.0.tar.gz` (most releases) and `dayz-search-index-<version>.tar.gz` (1.2.0 and 1.2.1). The skill accepts either, and either top-level folder name inside the archive (`dayz-rag-index/` or `dayz-search-index/`), and always installs to `~/.claude/dayz-search-index/`. Release 1.2.2 shipped with neither asset. Without `--tag`, a latest release like that is skipped: the skill prints a `[WARN]` line naming the latest tag and installs from the newest published (non-draft, non-prerelease) release that has an index asset. With `--tag` naming such a release it exits non-zero with a `[FAIL]` line.

After download the folder holds what `/dayz-search-index` writes (`lancedb/`, `manifest.json`, `config.json`), plus `release-tag.txt`, the release tag that was installed (written by this skill). If the old folder held `usage.log` (the token ledger `/dayz-search-index` uses for its free-tier check) or `embed-checkpoint.bin` (vectors from an unfinished local build), they are copied into the new index, so tokens you already spent still count. The release index was built before oversize class blocks were split into windows, so very long classes are only partly searchable; run `/dayz-search-index --full` if you need full coverage.

## How to run

Latest release that has an index asset (default):
```cmd
python "<skill-dir>\download.py"
```

Specific version:
```cmd
python "<skill-dir>\download.py" --tag 1.2.1
```

Overwrite an existing index without the prompt (this also reinstalls when the installed tag already matches):
```cmd
python "<skill-dir>\download.py" --force
```

Install an asset that has no published SHA-256 digest (every current release asset has one, so this is only for an asset uploaded without it):
```cmd
python "<skill-dir>\download.py" --allow-unverified
```

## Output

Each line is a `[LEVEL]` tag (`INFO`, `OK`, `WARN`, or `FAIL` for the error that ends a failed run), a tab, then the message:

```
DayZ RAG index downloader

[INFO]	Repo: DayZ-n-Chill/Agentic-Z
[INFO]	Resolving latest release...
[OK]	Release: <tag>
[INFO]	Asset: dayz-rag-index-v0.1.0.tar.gz (<size> MB)
[INFO]	Target: C:\Users\you\.claude\dayz-search-index
[INFO]	Downloading... <size>/<size> MB (100%)
[OK]	Downloaded <size> MB
[OK]	SHA-256 verified.
[INFO]	Extracting...
[OK]	Indexed source chunks: <count>
[OK]	Embed model: voyage-code-3
[OK]	Done. Restart Claude Code to reconnect the dayz-rag MCP server.
```

## Idempotency

- After each install the skill writes `release-tag.txt` into the index folder. If that file names the same release tag, the skill skips the download and exits 0, unless `--force` is passed, which downloads and reinstalls the same tag (useful to repair a damaged index).
- Otherwise, if an index already exists, it asks before overwriting (after the checksum-availability check below, so an unverifiable asset is refused without a prompt). `--force` skips the prompt. A declined prompt, or a run with no interactive input (an agent's shell has none), exits 1 on `[FAIL]	Existing index (<installed tag or "unknown origin">) not replaced with <tag>. Rerun with --force to replace it.`

## Upgrading an existing index (agents)

An agent's shell cannot answer the overwrite prompt. When the run ends on the `Existing index ... not replaced` `[FAIL]` line, ask the user whether to replace the installed index with the named tag. If they agree, rerun the same command with `--force` added; if not, stop and leave the index as it is.
- The download lands in a temp folder. The existing index is replaced only after the checksum passes and the archive extracts cleanly, and it is restored if the final swap fails.

## Integrity checks

- **Checksum:** GitHub publishes a SHA-256 `digest` for release assets it stores. The download must match it, or the skill exits non-zero and leaves the existing index untouched. This catches corrupted or truncated downloads only: the digest comes from the same GitHub release as the file, so it does not prove who published the asset. An asset with no digest is refused before downloading unless you pass `--allow-unverified`, which installs it with a warning.
- **Safe extraction:** archive entries that would land outside the extract folder (absolute paths, `..` traversal, links pointing outside) are refused. On Python 3.12+ this uses the `tarfile` `data` filter.
- **Network errors** (offline, DNS, proxy, HTTP errors, and timeouts or dropped connections partway through the download) exit non-zero with the URL and the reason, leaving the existing index untouched.
- **GitHub API rate limit:** without a token GitHub allows 60 API requests an hour per IP address. When that runs out (HTTP 403 or 429 with `X-RateLimit-Remaining: 0`), the skill says so and prints the reset time instead of blaming your connection. Set `GITHUB_TOKEN` in your environment to send it with the release lookup and raise the limit to 5,000 an hour.
- **Index in use:** on Windows a running dayz-rag MCP server keeps the LanceDB files open, so the old index cannot be moved aside. The skill then exits non-zero with "Close Claude Code (or disconnect dayz-rag with /mcp) and rerun", leaving the existing index untouched.
- **Short download:** the bytes received must equal the size GitHub lists for the asset. A connection closed early exits non-zero with "is incomplete: got X of Y bytes", which matters most under `--allow-unverified`, where no checksum would catch it.
- **Corrupt archive:** an archive that fails to decompress or extract exits non-zero with "Archive ... is corrupt or truncated", leaving the existing index untouched.
- **Failed swap:** if the new index cannot be moved into place, the old one is put back and the run exits non-zero. If putting it back also fails, the `[FAIL]` line names `~/.claude/dayz-search-index.old`, where the old index still is.
- **Leftover `.old` folder:** an interrupted install can leave the previous index at `~/.claude/dayz-search-index.old`. It is never deleted. When `dayz-search-index/` is missing, the next run restores it from there with a `[WARN]` line; when both exist, the run exits non-zero naming both paths so you can keep one and remove the other. A leftover `dayz-search-index.new/` is only an unfinished copy and is replaced.
- **Index path is a file:** if `~/.claude/dayz-search-index` exists as a file rather than a folder, the run exits non-zero asking you to move or delete it.

## After downloading

The dayz-rag MCP server reads the index when it starts. Restart Claude Code (or reconnect with `/mcp`) to pick up the new index. Downloading needs no `VOYAGE_API_KEY`, but the server embeds each search query with Voyage, so add the key to `.env` before searching.

## Dependencies

- Python 3.8+ (stdlib only: `urllib`, `tarfile`, `zlib`, `hashlib`, `json`)
- No `gh` CLI required; uses GitHub's public REST API for release metadata (optional `GITHUB_TOKEN` for a higher rate limit)

## Do not

- Don't run this if you've already built a local index against your specific DayZ install: the release index is built against the maintainer's snapshot and may drift from your installed version.
- Don't commit the downloaded index. It lives at `~/.claude/dayz-search-index/` (outside the repo) by design.
