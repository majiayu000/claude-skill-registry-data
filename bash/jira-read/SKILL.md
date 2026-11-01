---
name: jira-read
version: "3.2.0"
user-invocable: true
description: Read Jira issue data from local cache or API, and download attachments via script (never into context). Triggers when user says "jira-read [JIRA-ID]", 「读取 Jira」「查看 Jira」「下载 Jira」「下载附件」 (read/view/download Jira / download attachments), or needs to fetch Jira issue data. Requires $JIRA_CACHE_DIR (e.g. ~/.cache/jira).
---

# Jira Read — Execution Rules

> Quickly read downloaded Jira data from local cache — no network access required.

## Configuration

Set the cache directory environment variable before use (recommend adding to `.zshrc` / `.bashrc`):

```bash
export JIRA_CACHE_DIR="$HOME/.cache/jira"
```

Defaults to `~/.cache/jira/` if not set.

## Triggers & Parameters

**Primary trigger**: `jira-read [JIRA-ID]` — case-insensitive (auto-converted to uppercase)

| Usage | Behavior | Output Mode |
|-------|----------|-------------|
| `jira-read {ID}` | Read local cache; auto-fetch from API if missing | Summary |
| `jira-read {ID} --live` | Skip cache, fetch from API and update cache | Summary |
| `jira-read {ID} --force` | Force API fetch, overwrite local cache | Summary |
| `jira-read {ID} --no-download` | Local only; prompt if missing | Summary |
| `jira-read {ID} --full` | Same as default, output full content including all comments | Full |
| `jira-read {ID} --meta` | Same as default, output YAML front matter only | Metadata |
| `jira-read ID1 ID2 ID3` | Batch read from local cache | Summary |
| `jira-read --live ID1 ID2 ID3` | Batch fetch from API and cache | Summary |
| `jira-read --force ID1 ID2 ID3` | Batch force re-fetch (overwrite local cache) | Summary |
| `jira-read --list` / `-l` | List all local cache entries | List |

---

## Storage Paths

- **Main file**: `$JIRA_CACHE_DIR/{JIRA-ID}.md`
- **Field mapping cache**: `$JIRA_CACHE_DIR/.field-mapping.json`

On first use, automatically calls `jira_search_fields` to build field ID mapping; subsequent reads use the cache directly. `--force` refreshes the mapping.

---

## Execution Flow

### Step 1: Parse Jira ID

Extract (regex: `([A-Za-z]+-\d+)`) and convert to uppercase, build the local file path.

### Step 2: Check File Existence

**File exists**: continue to step 3

**File does not exist**:
- Resolve the PAT via the credential chain (below) before any API call
- **Default**: call `jira_get_issue(issue_key="{JIRA-ID}", fields="*all", comment_limit=50)` → on success, format and save, then continue; on failure, classify per Error Handling
- **--no-download**: prompt only, don't auto-download
- **--live**: skip local check, fetch from API and update cache
- **--force**: fetch from API and overwrite local cache

### Step 3: Read, Parse, Output

Read Markdown → parse YAML front matter and body → output as structured Markdown.

**Parsed fields**: `jira_id`, `title`, `priority`, `status`, `reporter`, `assignee`, `created_at`, `updated_at`, `downloaded_at`, `source_url`; body contains issue description, reproduction steps, expected/actual results, comment history.

**Attachment handling**: Never read attachment content into the Agent context. If the issue has attachments (logs, screenshots), note them at the end of the output. When the user needs the actual attachment (logs), follow the "Attachment Download" section below.

> Output format examples for each scenario: see [`reference.md`](reference.md)

---

## Credential resolution (before any live fetch)

Run this chain **before** MCP/`jira_get_issue`, `--live`/`--force`, and attachment download. mcp-atlassian is an optional way to populate step 1; it is not required.

1. Env `JIRA_PERSONAL_TOKEN` (canonical)
2. Else env `JIRA_PAT` (alias; copy into `JIRA_PERSONAL_TOKEN` for the rest of the session)
3. Else file `~/.config/jira-certs/jira-pat.txt` (Windows: `%USERPROFILE%\.config\jira-certs\jira-pat.txt`) — first line, trimmed, single-line secret
4. Else ask the user **once** for a PAT and **ask whether to write it** to that file. Do not live-fetch until a token exists.

After env or the file has a token: do **not** paste the PAT into chat, argv, or command previews; do **not** echo it in replies or logs; do **not** `cat` the file into the conversation. Scripts read env or the file themselves.

Do **not** teach a manual `curl` that interpolates the PAT (no “equivalent curl from the Authentication table”). That fallback is forbidden (supersedes the older attachment-download delta if it is still open).

## Attachment Download

Always download attachments to local disk via the skill scripts — never read attachment content into the Agent context. To inspect log contents, extract only the relevant lines with `grep`/`head`/`tail`.

### Authentication (Internal Jira)

| Element | Source | Notes |
|---|---|---|
| PAT (Bearer) | Credential chain above | Canonical env `JIRA_PERSONAL_TOKEN`; alias `JIRA_PAT`; file `jira-pat.txt` |
| mTLS client cert | `JIRA_CLIENT_CERT` / `JIRA_CLIENT_KEY` | Default `~/.config/jira-certs/client.crt` + `client.key` |
| SSL | `JIRA_SSL_VERIFY=false` | Internal self-signed cert → curl `-k` / node `rejectUnauthorized: false` |

**Credentials (recipe field):** store the PAT as one line in `~/.config/jira-certs/jira-pat.txt` (same directory as the mTLS pair; not in any git repo). Format: single-line secret, no quotes. Rotation: replace the file contents and any exported env, then retry. mcp-atlassian may inject `JIRA_PERSONAL_TOKEN` instead of the file.

### Attachment URL

Take it directly from `attachment[].url` returned by `jira_get_issue`, e.g.:
`https://jira.example.com/secure/attachment/{attachmentId}/{filename}`

### Download Script

Probe `curl -V` first. If the output contains `Schannel` (typical Windows) or PEM `--cert`/`--key` is unavailable, **MUST** use the node sidecar. Otherwise the bash script is allowed.

```bash
# Node (Windows / Schannel curl)
node scripts/download_jira_attachments.mjs 100001 app-log-1700000000000.zip /tmp/logs/PROJ-1234.zip

# Bash + OpenSSL curl (PEM --cert/--key)
scripts/download_jira_attachments.sh 100001 app-log-1700000000000.zip /tmp/logs/PROJ-1234.zip
```

Both resolve the PAT from the credential chain (Bearer, Basic fallback). Override cert paths with `JIRA_CLIENT_CERT` / `JIRA_CLIENT_KEY`. Set `JIRA_URL` (e.g. `https://jira.example.com`). Never put the PAT on the command line.

### Download & Archive Flow

1. Resolve credentials (chain above), then call `jira_get_issue(issue_key=..., fields="summary,description,attachment,status,priority")` for `attachment[].id` / `filename` / `url`
2. Download to a temp dir via the selected script — download 1 first to verify auth, then batch
3. `unzip -l` to preview the zip structure; confirm it is flat before extracting
4. Archive into the project at `issues/{type}/jira-bug/{JIRA-ID}-app-log/`, writing `{JIRA-ID}.md` to record the ticket info + attachment list

> Download result report format: see [`reference.md`](reference.md) § 7

---

## Cache Freshness Prompts

| Cache Age | Prompt |
|-----------|--------|
| < 1 hour | None |
| 1–24 hours | "Cached X hours ago" |
| 1–7 days | "Cached X days ago, recommend updating" |
| > 7 days | "Cache expired (X days ago), strongly recommend updating" |

---

## Error Handling

| Error Scenario | Handling |
|----------------|----------|
| Invalid Jira ID format | Prompt correct format |
| File not found | Auto-fetch from API (prompt only with `--no-download`) |
| Credential chain empty (env + alias + file) | Ask-and-persist (do not treat as 401) |
| mcp-atlassian unavailable | Optional injector missing: still use the credential chain; if issue JSON is needed, try cache / `jira-read --live` after resolving PAT; do not abort only because MCP is missing |
| HTTP 401 / 403 with a resolved token | Token invalid or revoked — rotate it and update `jira-pat.txt` (and env if set) |
| TLS handshake / client cert | Check `client.crt` / `client.key` and TLS 1.3; on Windows do not use Schannel curl for PEM mTLS — use the node sidecar |
| Issue not found | Prompt that Jira ID may be incorrect |
| File parse failure | Output raw file content |
