---
name: open-codex-ui
description: Install, update, secure, daemonize, expose through Cloudflare Tunnel, and enable speech input for the open-source Open Codex UI application. Use when a user asks to install or enable Open Codex UI, configure its login daemon, set its access password, install or manage the sherpa-onnx bilingual speech model, troubleshoot microphone access, or expose local port 13140 through a Cloudflare Quick Tunnel or managed tunnel. Never use the company-only etcd/vc.cheftin.cn mapping workflow in this skill.
---

# Open Codex UI

Use the installed `open-codex-ui` CLI for application lifecycle, speech, and Cloudflare Tunnel
operations. Do not use the company-only etcd or `vc.cheftin.cn` route mapper.

## Install or Update

1. Check `open-codex-ui --version`.
2. If unavailable, install through the official package runner:
   - Prefer `uvx open-codex-ui daemon install` on macOS, Linux, WSL, and Windows.
   - Use `npx open-codex-ui daemon install` only when `uvx` is unavailable.
3. Use `open-codex-ui update` to update an existing persistent installation.

Do not clone or build the repository for a normal installation. The published wheel contains the
compiled frontend and requires Python 3.12+ through `uvx`.

## Enable the Daemon

Install the native login service for local-only use:

```bash
open-codex-ui daemon install
```

Check and operate it with:

```bash
open-codex-ui daemon status
open-codex-ui daemon start
open-codex-ui daemon stop
```

The service uses LaunchAgent on macOS, a user systemd service on Linux/WSL, and current-user Task
Scheduler on Windows. Runtime state and logs are under `~/.yier/web/`.

## Enable Speech Input

Install and verify the standard bilingual Chinese-English streaming Zipformer model:

```bash
open-codex-ui speech install
open-codex-ui speech status
```

Store models under `~/.yier/models` by default; activate the standard model at
`~/.yier/models/sherpa-onnx`. A valid model directory contains `tokens.txt`, `encoder*.onnx`,
`decoder*.onnx`, and `joiner*.onnx`. The installer resumes interrupted downloads, verifies the
archive, extracts safely, and activates atomically.

Use `HTTPS_PROXY` or `ALL_PROXY` when required:

```bash
HTTPS_PROXY=http://127.0.0.1:7890 open-codex-ui speech install
```

On Windows PowerShell:

```powershell
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
open-codex-ui speech install
Remove-Item Env:HTTPS_PROXY
```

Replace or remove the standard model only when the user asks:

```bash
open-codex-ui speech install --force
open-codex-ui speech remove
```

Use `open-codex-ui speech --models-dir <path> install|status|remove` for a custom storage root.
Configure advanced runtime behavior with:

- `YIER_SHERPA_ONNX_MODEL_DIR`: streaming transducer model directory.
- `YIER_SHERPA_ONNX_PROVIDER`: execution provider; default `cpu`.
- `YIER_SHERPA_ONNX_NUM_THREADS`: decoder threads; default `2`.

Re-run `open-codex-ui daemon install` after setting these `YIER_*` variables so the daemon captures
them. Remote and mobile browsers require HTTPS for microphone capture; localhost is also a secure
context. The Cloudflare Tunnel HTTPS URL satisfies the remote-browser requirement.

## Password Configuration

Require authentication before any public tunnel. Authentication is disabled unless
`YIER_AUTH_PASSWORD` or `YIER_AUTH_PASSWORD_HASH` is configured. Prefer a hash for persistent
storage. On POSIX, the user can set a password interactively and reinstall the daemon:

```bash
read -r -s YIER_AUTH_PASSWORD
export YIER_AUTH_PASSWORD
open-codex-ui daemon install
unset YIER_AUTH_PASSWORD
```

Generate `YIER_AUTH_PASSWORD_HASH` with the package's `yier_web.auth.hash_password` helper when
requested. Do not print either password form or inspect the stored value. `daemon install` captures
current `YIER_*` variables into its user-only environment file. `YIER_AUTH_SECRET` and
`YIER_AUTH_SESSION_TTL_HOURS` are optional hardening settings.

## Cloudflare Public Exposure

Treat public exposure as a gated operation:

1. Verify `http://127.0.0.1:13140/api/auth/session` reports `enabled: true`. Do not start a tunnel
   when authentication is disabled or the origin cannot be reached.
2. Require `cloudflared` in `PATH`. If missing, direct the user to Cloudflare's official
   cloudflared downloads page.
3. Use Quick Tunnel when the user wants a temporary URL and has no Cloudflare hostname:

```bash
open-codex-ui tunnel start
open-codex-ui tunnel status
```

Quick mode proxies `http://127.0.0.1:13140` by default and prints a temporary
`https://<random>.trycloudflare.com` URL. Use `--origin` only when the local address differs. Do not
claim the Quick Tunnel hostname is stable.

4. Use managed-remote only when the user supplies the relevant Cloudflare tunnel configuration:

```bash
open-codex-ui tunnel start --mode managed-remote --name <tunnel-name> --hostname <hostname>
```

Managed-remote accepts `CF_TOKEN`, `CF_ACCOUNT_ID`, `--api-token-file`, `--account-id`, and
`--token-file`. Never print API or connector tokens. Use an existing local cloudflared config with:

```bash
open-codex-ui tunnel start --mode managed-local --config ~/.cloudflared/config.yml
```

5. Report the tunnel mode, public URL/hostname, local origin, PID/log path, and authentication
   status.

Stop the tunnel only when the user asks:

```bash
open-codex-ui tunnel stop
open-codex-ui tunnel status
```

Never use `expose.py`, etcd keys, `vc.cheftin.cn` subdomains, or company route replacement in this
skill.

## Safety and Reporting

- Never expose a public tunnel before verifying authentication is enabled.
- Do not expose passwords, daemon environment contents, Cloudflare tokens, or config secrets.
- Report daemon status, speech status when requested, authentication state, tunnel mode, origin,
  log path, and public URL after success.
- Do not claim a Windows-specific operation was tested unless it actually ran on Windows.
