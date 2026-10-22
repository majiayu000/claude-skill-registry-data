---
name: zlog
description: Compresses stale AI agent session logs (Claude Code, Cursor, Gemini, Codex, Ollama, Windsurf, LM Studio, Aider) to save disk space. Reclaims space from .log/.out/.trace files while protecting transcripts, configs, and live databases. Never touches conversation history, SQLite stores, or files being written. Use when the user asks to clean, compress, preview, restore, or scan for AI logs at session wrap-up.
license: MIT
compatibility: Linux, WSL, macOS, Windows 11 (Bash, Zsh, Git Bash, PowerShell)
allowed-tools: Bash(scripts/zlog.sh:*) Read Write
metadata:
  version: "2.0.0"
  last_verified: "2026-09-21"
  registry: skills.sh
---

# zlog — AI agent log storage optimizer

## Purpose

Reclaim disk space from stale AI agent session logs. The skill decides
*what* may be touched; `scripts/zlog.sh` (POSIX) and `scripts/zlog.ps1`
(Windows) implement *how*. Never paste shell from memory — always run
the bundled scripts so preview and cleanup share one candidate engine.

## Use When

- "clean up my AI logs", "free disk space from Cursor logs"
- "compress old Claude/Codex/Gemini logs", "zlog", "pack logs"
- "preview what zlog would change" (read-only first when ambiguous)
- "restore my compressed log"
- "scan for AI logs" / "find new AI agents" (deep modes)
- Session wrap-up cleanup

## Don't Use When

- "delete my chat history" → refuse (transcripts are Class B protected)
- "clean node_modules / caches" → refuse unless the user explicitly asks
  for cache cleanup (out of scope for this skill)
- "vacuum my Codex database" → refuse automatic handling; SQLite/WAL
  stores are live databases (report as intentionally untouched)
- Broad home-directory cleanup without explicit deep-scan intent
- Any file currently being written (locked or fresh)

## Workflow

1. Determine intent: preview, clean, restore, or scan.
2. Determine OS/shell: Linux/macOS/WSL/Git Bash → `scripts/zlog.sh`;
   Windows PowerShell → `scripts/zlog.ps1`.
3. Identify roots from `references/agent-paths.md` (scripts embed them).
4. Read-only candidate scan first: run `preview` (or `deep-preview`).
5. Exclude protected data (see Protected Data).
6. Check age + active writers (scripts enforce 60s default, lock checks).
7. If intent is ambiguous, show the preview and ask before cleaning.
8. Run `clean` (or `deep` only on explicit deep-scan intent).
9. Scripts validate each archive before deleting its source.
10. Report exact measured results (never estimates).

## Safety Rules

Full rationale: `references/safety.md`. Non-negotiable invariants:

- Never follow symlinks out of a scan root (POSIX `-P` default).
- Never touch Class B protected data (transcripts, configs, SQLite/WAL).
- Never descend into Class C junk locations.
- Never compress a locked or fresh file; never clean caches unprompted.
- Never delete a source unless its archive passed integrity test AND is
  smaller than the source AND the destination was absent AND the source
  identity is unchanged since it was scanned — POSIX: inode/size/mtime;
  Windows: length/timestamps/full-content SHA-256
  (transactional: temp → test → size check → dest-absent check →
  source-unchanged check → publish-without-overwrite → delete).
- Restore never overwrites: unknown formats refused, existing
  destinations kept, `.tar.gz` members must exactly match the intended
  basename (extracted to a temp dir first).
- Unknown (Class D) files and directories are ignored by default.

## Scan Scope

- **Standard** (`preview`/`clean`): known agent roots only
  (see `references/agent-paths.md`).
- **Deep** (`deep-preview`/`deep`): known agent locations recursively
  (depth-capped, pruned). Read-only `deep-preview` first; `deep` only on
  explicit user intent. It does not discover unknown agents.
- One candidate engine serves preview and clean, so the preview can
  never disagree with cleanup.

## Compression Rules

- Candidates: `*.log`, `*.out`, `*.trace` over 10KiB, older than the age
  window (default 60s; `--older-than DAYS` for retention policies like
  "compress logs older than 7 days").
- Order: `zstd -15` → `xz -9` → `gzip -9` (POSIX); single-entry
  `.tar.gz` via `tar.exe` (Windows).
- Empty (0-byte) logs are purged through the same predicate (pruned
  location + age + lock check), never bare deletion.

## Protected Data

Class B is always excluded: `*.jsonl`, `transcript.*`,
`conversation.*`, `history.*`, `*.sqlite*`, `*.db`, `*.wal`, `*.shm`,
configs, `SKILL.md`, `README*`, `LICENSE*`, archives, temp files.
`*.txt` is excluded by default (docs/data live beside logs).

## Dry Run

`preview` / `deep-preview` change nothing and report raw candidate
sizes only. Compression estimates are unavailable without test
compression — never quote a ratio; run `clean` for measured savings.

## Deep Scan

Known-location deep walk (not new-agent discovery). Always
`deep-preview` before `deep`. Pruned-dir count is reported.
On Windows, standard roots already recurse fully, so `deep-preview`
and `deep` are explicitly the same operation as `preview` and `clean`
(the scripts say so in their output) — not a separate wider scan.

## Failure Handling

Per-file status, never silent: `COMPRESSED`, `SKIPPED` (locked/fresh),
`FAILED` (exit-code/integrity failure or source changed mid-run, source
preserved), `NOT_BENEFICIAL` (archive not smaller, source preserved),
`UNSAFE-SKIP` (unknown format, destination exists, multi-entry or
member-mismatch tar).
Surface failures to the user with the reason and "original preserved".

## Reporting

Report the script's measured lines verbatim, e.g.
`mode=clean roots=8 candidates=14 compressed=11 …` plus
`raw=… compressed=… saved=…`, including skipped/failed counts and why
(locked, protected, not beneficial). No estimates, no marketing ratios.

## Examples

- "preview what zlog would change" → run `preview`, show candidates.
- "compress yesterday's logs" → `clean --older-than 1` (POSIX) / `clean -OlderThanDays 1` (PowerShell).
- "keep last 30 days, compress the rest" → `clean --older-than 30` (POSIX) / `-OlderThanDays 30` (PowerShell).
- "compress this file" (user names it) → that exact file only, still
  with lock/age/integrity checks.
- "restore session.log.zst" → `restore` mode (refuses if destination
  exists; archive preserved).

## Edge Cases

- Filenames with spaces/newlines: handled (NUL-delimited engine).
- Hardlinked files compress independently (valid, reported normally).
- High-entropy files that grow when compressed: kept, reported
  `NOT_BENEFICIAL`.
- Missing tools (`zstd`, `fuser`): graceful fallback chain; age buffer
  is the last line of defense — prefer idle periods.
- Multi-entry `.tar.gz` on restore: refused.
