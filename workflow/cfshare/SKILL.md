---
name: cfshare
description: Use the cfshare CLI to expose local ports/files as temporary Cloudflare Quick Tunnel URLs. Trigger when a user needs a temporary public URL for a local service, needs to share files/directories from terminal, or needs to inspect/export cfshare audit and policy state.
metadata: { "cfshare": { "emoji": "☁️", "requires": { "bins": ["cfshare", "cloudflared"] }, "author": "ystemsrx" } }
---

# CFShare CLI Skill

`cfshare` wraps Cloudflare Quick Tunnel and outputs structured JSON.

## Install when version checks fail

If either command fails, install missing binaries before running any `cfshare` tool.

```bash
cfshare --version
cloudflared --version
```

1. If `cfshare --version` fails, install `cfshare` (requires Node.js and npm):

```bash
npm install -g @ystemsrx/cfshare
```

2. If `cloudflared --version` fails, install `cloudflared` by platform:

macOS:

```bash
brew install cloudflare/cloudflare/cloudflared
```

Debian/Ubuntu:

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install -y cloudflared
```

Windows (PowerShell):

```powershell
winget install --id Cloudflare.cloudflared
```

WSL/Linux generic binary install:

```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

3. Re-run both version checks. If still failing, stop and report exact stderr output to user.

## CLI contract

```bash
cfshare <tool> [params-json] [options]
```

Supported tools:

- `env_check`
- `expose_port`
- `expose_files`
- `exposure_list`
- `exposure_get`
- `exposure_stop`
- `exposure_logs`
- `maintenance`
- `audit_query`
- `audit_export`

Global options:

- `--params '<json>'` or `--params-file <path>`
- `--config '<json>'` or `--config-file <path>`
- `--workspace-dir <dir>` (only used by `expose_files`)
- `--keep-alive` (for `expose_*`, keep foreground process alive)
- `--no-keep-alive` (default for `expose_*`, print result then exit)
- `--compact`

Command names accept `_` and `-` (for example `expose-port` == `expose_port`).

## Standard workflow for agents

1. Run `env_check` first.
2. Create exposure with `expose_port` or `expose_files`.
3. Return `public_url` and `expires_at` to user immediately.
4. By default, `expose_*` prints result and exits.
5. Use `--keep-alive` only when foreground lifecycle control is needed; stop with `Ctrl+C` when done.

Recommended for stable automation:

- Prefer `--params`/`--params-file` over positional raw JSON to reduce quoting errors.
- Prefer `access: "token"` for sensitive content.
- Treat `access: "none"` as publicly readable by anyone with link.

## Tool usage

### 1) env_check

```bash
cfshare env_check
```

Returns:

- `cloudflared.ok/path/version`
- `defaults` (effective policy + runtime paths)
- `warnings`

### 2) expose_port

```bash
cfshare expose_port --params '{"port":3000,"opts":{"access":"token","ttl_seconds":3600}}'
```

Params:

- `port`: `1..65535`
- `opts.ttl_seconds`
- `opts.access`: `token | basic | none`
- `opts.protect_origin`: default `access != "none"`
- `opts.allowlist_paths`: path prefix allowlist for reverse proxy

Returns:

- `id`
- `public_url` (token mode auto-appends `?token=...`)
- `local_url`
- `expires_at`
- `access_info` (secrets are masked)

### 3) expose_files

```bash
cfshare expose_files --params '{"paths":["./dist"],"opts":{"mode":"normal","presentation":"preview","access":"none"}}'
```

Params:

- `paths`: files/directories to copy into temp workspace
- `opts.mode`: `normal | zip` (default `normal`)
- `opts.presentation`: `download | preview | raw` (default `download`)
- `opts.ttl_seconds`
- `opts.access`: `token | basic | none`
- `opts.max_downloads`: auto-stop after threshold

File Serving Behavior:

Mode: normal

- Single file → served directly at the root URL.
- Multiple files or a directory → displayed in an intuitive file explorer interface.

Mode: zip

- All files are packaged into a ZIP archive.

Presentation:

- Default behaviors: download | preview | raw
- Behavior can be overridden via query parameters.
  - download → forces browser file save.
  - preview → renders inline (images, PDF, Markdown, audio/video, HTML, text, etc.).
  - raw → serves original content without any wrapper.
- If a file type is not previewable, preview automatically falls back to raw, then to download.

Returns:

- `id`, `public_url`, `expires_at`, `mode`, `presentation`
- `manifest`, `manifest_mode`, `manifest_meta`

### 4) exposure_list

```bash
cfshare exposure_list
```

Lists tracked sessions with `id/type/status/public_url/local_url/expires_at`.

### 5) exposure_get

```bash
cfshare exposure_get --params '{"id":"port_xxx","opts":{"probe_public":true}}'
cfshare exposure_get --params '{"filter":{"status":"running"},"fields":["id","status","public_url"]}'
```

Supports selector by `id`, `ids`, or `filter`.
Can probe public reachability via `opts.probe_public`.

### 6) exposure_stop

```bash
cfshare exposure_stop --params '{"id":"all"}'
```

Stops tunnel/proxy/origin and removes temporary workspace.
Returns `{stopped, failed, cleaned}`.

### 7) exposure_logs

```bash
cfshare exposure_logs --params '{"id":"files_xxx","opts":{"component":"all","lines":200}}'
```

`component`: `tunnel | origin | all`.

### 8) maintenance

```bash
cfshare maintenance --params '{"action":"run_gc"}'
cfshare maintenance --params '{"action":"set_policy","opts":{"policy":{"maxTtlSeconds":7200},"ignore_patterns":["*.pem",".env*"]}}'
```

Actions:

- `start_guard`
- `run_gc`
- `set_policy` (requires `opts.policy` or `opts.ignore_patterns`)

### 9) audit_query

```bash
cfshare audit_query --params '{"filters":{"event":"exposure_started","limit":100}}'
```

### 10) audit_export

```bash
cfshare audit_export --params '{"range":{"from_ts":"2026-01-01T00:00:00Z","output_path":"./audit.jsonl"}}'
```

## Runtime files (CLI mode)

Default CLI state directory is `~/.cfshare`:

- `policy.json`
- `policy.ignore`
- `audit.jsonl`
- `sessions.json`
- `workspaces/`
- `exports/`

## Important limitations in CLI mode

- `expose_port` and `expose_files` exit by default after printing result; use `--keep-alive` to hold foreground.
- Current session registry is in-process memory; separate `cfshare` invocations do not restore full live session state.
- `basic` mode credentials are masked in outputs, so `token` is usually the practical authenticated mode for agent-delivered links.

## Troubleshooting

- `cloudflared binary not found`: install `cloudflared` or set `--config '{"cloudflaredPath":"..."}'`
- `local service is not reachable on 127.0.0.1:<port>`: start service first
- `path blocked by ignore policy`: adjust `policy.ignore` or `maintenance set_policy`
- `port blocked by policy`: update `blockedPorts` in policy if intentional

Use `CFSHARE_LOG_LEVEL=info` or `CFSHARE_LOG_LEVEL=debug` for more stderr logs.
