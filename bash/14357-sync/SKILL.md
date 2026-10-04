---
name: sync
description: Multi-machine .xm/ state sync — server start/stop, push, pull, setup, status
model: sonnet
---

<Purpose>
Sync .xm/ project state (traces, plans, build data) across multiple machines via a lightweight Bun HTTP server backed by SQLite.
</Purpose>

<Use_When>
- User says "sync", "push", "pull", "sync server", "동기화"
- User wants to share .xm/ state between machines
- User wants to start/stop the sync server
</Use_When>

<Do_Not_Use_When>
- Git push/pull (use git directly)
- File sync unrelated to .xm/ state (use rsync, etc.)
</Do_Not_Use_When>

# x-sync — Multi-Machine .xm/ Sync

Syncs .xm/ project state across machines. Server stores data in SQLite; clients push/pull via HTTP.

Pull is incremental by a monotonic server **cursor** (id), so same-millisecond pushes never get skipped. Push sends a **full snapshot**, so the server propagates local deletions as tombstones — clients then remove only the machine-namespaced copies they pulled earlier (never your local working files).

## Model Routing

| Subcommand | Model | Reason |
|------------|-------|--------|
| `status`, `server status` | **haiku** (Agent tool) | Read-only check |
| `push`, `pull`, `push-all`, `pull-all` | **haiku** (Agent tool) | Script execution, no reasoning |
| `server start`, `server stop` | **haiku** (Agent tool) | Simple process management |
| `setup` (interactive) | **sonnet** | Requires AskUserQuestion |

## CLI Invocation

> **⚠ Call `xm sync <command>` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xms()`) defined in one call do NOT persist to the next, causing `command not found: xms`. Never define a helper across calls; always use the dispatcher.**
>
> The `xm sync <sub>` dispatcher routes to `lib/x-sync/sync-<sub>.mjs` (and `server` → `sync-server.mjs`), resolving the bundled lib path internally. You never have to compute paths.
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XMS_LIB=$(ls -d ~/.claude/plugins/cache/xm/{x-sync,xm}/*/lib/x-sync 2>/dev/null | sort -V | tail -1)
> node "$XMS_LIB/sync-status.mjs"
> ```
>
> **Forbidden:** `XMS="node ..."; $XMS status` — zsh treats the quoted string as a single command and fails.

## Arguments

User provided: `$ARGUMENTS`

## AskUserQuestion Dark-Theme Rule

**CRITICAL:** The `question` field in AskUserQuestion is invisible on dark terminals.

**Visibility map:**
| Element | Visible | Use for |
|---------|---------|---------|
| `header` | ✅ YES | Short context tag (e.g., "x-sync setup") |
| `question` | ❌ NO | Keep minimal — user cannot see this text |
| option `label` | ✅ YES | Primary info — must be self-explanatory |
| option `description` | ✅ YES | Supplementary detail |

**Always follow this pattern:**
1. Output ALL context (descriptions, status, analysis) as **regular markdown text** BEFORE calling AskUserQuestion
2. `header`: put the key context here (visible, max 12 chars)
3. `question`: keep short, duplicate of header is fine (invisible to user)
4. Option `label` + `description`: carry all decision-relevant information

**WRONG:** Putting context in `question` field → user sees blank space above options
**RIGHT:** Print context as markdown first, use `header` for tag, options for detail

## Routing

- Empty or `status` → [Mode: status]
- `setup` → [Mode: setup]
- `server start` → [Mode: server-start]
- `server stop` → [Mode: server-stop]
- `server status` → [Mode: server-status]
- `push` → [Mode: push]
- `pull` → [Mode: pull]
- `push-all` or `push all` → [Mode: push-all]
- `pull-all` or `pull all` → [Mode: pull-all]

---

## Mode: setup

Interactive wizard to configure sync credentials.

**Step 1: Show current config**

```bash
xm sync setup --show
```

**Step 2: Collect server URL and API key**

Print the prompts as markdown text, then use AskUserQuestion (`header: "x-sync setup"`) to collect:
- Server URL (e.g. `http://my-server:19842`)
- API key (must match the server's `XM_SYNC_API_KEY`)

**Step 3: Write config + test connection**

```bash
xm sync setup --server-url "$SERVER_URL" --api-key "$API_KEY"
```

`sync-setup.mjs` writes `~/.xm/sync.json` (chmod 600), then probes `/dashboard/health` and prints `✅ 서버 연결 확인` or `❌ 서버 연결 실패 (...)`. Substitute the user-provided values for `$SERVER_URL` / `$API_KEY`.

---

## Mode: server-start

Start the sync server as a managed background process. `sync-server.mjs` reads the API key from `~/.xm/sync.json`, prefers `bun` over `node`, writes the PID, and tails the log if startup crashes.

```bash
xm sync server start
```

Optional: `xm sync server start --port 19842` (default: 19842).

If no API key is configured, the server warns that it is running **open** (push/pull and dashboard reachable without auth). Surface that warning to the user.

---

## Mode: server-stop

```bash
xm sync server stop
```

Kills the tracked PID; falls back to killing whatever holds the port. Reports a stale PID file if found.

---

## Mode: server-status

```bash
xm sync server status
```

Reports the running PID and a `/dashboard/health` probe, or `Server not running`.

---

## Mode: push

Push local .xm/ state (full snapshot) to the sync server.

Canonical handoff files (`build/SESSION-STATE.json` and `build/HANDOFF.md`) are
included. Machine-local mem-mesh mirror bookkeeping and legacy namespaced
handoff copies are excluded.

```bash
xm sync push
```

Optional: `xm sync push --project PROJECT_ID` to override the auto-detected project name.

Output example:
```
[x-sync push] 42 files from my-project (macbook-a1b2)
[x-sync push] accepted: 12, skipped: 30, 1 deleted
```

`deleted` = paths tombstoned because they no longer exist locally. If sync is not configured:
```
❌ x-sync 설정이 필요합니다. `xm sync setup`을 먼저 실행하세요.
```

---

## Mode: pull

Pull remote .xm/ state from the sync server (incremental by cursor).

```bash
xm sync pull
```

Optional flags:
- `--project PROJECT_ID` — override project name
- `--since TIMESTAMP` — legacy timestamp pull (epoch ms); normally omit and let the cursor drive it

Output example:
```
[x-sync pull] project=my-project cursor=128
[x-sync pull] 8 files written, 1 namespaced, 2 removed (3 skipped — own machine)
```

`removed` = machine-namespaced copies deleted because their source was tombstoned. Your own local files at non-namespaced paths are never touched.

Handoff files use a separate rule from ordinary `.xm` files: pull selects one
newest valid `SESSION-STATE.json`, writes it to the canonical path (never a
machine-namespaced filename), and brings along `HANDOFF.md` from the same
machine. `handoff_generation` wins when all candidates provide it; `saved_at`
is the compatibility fallback for older clients. Remote tombstones never
delete a locally restorable handoff.

---

## Mode: push-all

Push all .xm/ projects under a root directory.

```bash
xm sync push-all
```

Optional flags:
- `--root <dir>` — root directory to scan (default: `~/work`)
- `--dry-run` — preview only, no files pushed

---

## Mode: pull-all

Pull .xm/ data for all local projects from the sync server.

```bash
xm sync pull-all
```

Optional flags:
- `--root <dir>` — root directory to scan (default: `~/work`)
- `--dry-run` — preview only, no files pulled

---

## Mode: status

Show sync configuration and last sync state.

```bash
xm sync status
```

`sync-status.mjs` prints config (API key masked), the resolved `.xm/` path and project id, last pull/push details, and a remote health check. Output format:
```
x-sync Status

  Config:        ~/.xm/sync.json
  Server URL:    http://my-server:19842
  Machine ID:    macbook-a1b2
  API Key:       ****configured****

  Last Pull:     2026-04-06T10:30:00Z
  Last Push:     2026-04-06T10:25:00Z
  Server:        ✅ Remote healthy

  Quick commands:
    xm sync setup          Configure sync credentials
    xm sync server start   Start local server
    xm sync push           Push .xm/ to server
    xm sync pull           Pull from server
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "My local is newest, I'll just push" | "Newest" is a claim, not evidence. Pull first to verify — the cost of a conflicting overwrite is higher than a round-trip. |
| "The conflict is trivial, I'll pick mine" | Trivial conflicts are the ones where the wrong resolution looks right. Read both sides before picking. |
| "I'll pull and deal with conflicts later" | Later is now. Unresolved sync state compounds silently across machines — the longer you wait, the more places it can be wrong. |
| "Small changes don't need sync" | Small changes across machines are exactly when drift starts. Sync is cheap; unwinding drift is expensive. |
| "Setup is a one-time thing, I'll skip verifying" | Setup drift across machines is the most common sync failure. Verify setup before you trust pull/push — five seconds up front, hours saved later. |
| "I'll start the server without an API key, it's just my LAN" | An open server accepts pushes (and arbitrary writes) from anyone who can reach the port. Set `XM_SYNC_API_KEY` before binding to anything but localhost. |
