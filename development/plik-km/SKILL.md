---
name: plik_KM
description: How to send Kosta files via the Plik MCP — when, how, where credentials live, and how to verify the backend is healthy. Read this once per session before the first upload.
targets: [hermes-default, hermes-gpt, claude-hermes]
machines: [mac-studio]
---
# Plik file sharing

Plik (root-gg/plik 1.4.2) is the self-hosted "send Kosta a file via short link" backend. It runs in Docker on the Mac Studio, exposed via Tailscale Funnel. The official Plik CLI ships an MCP server (`plik --mcp`) that is wired into every Hermes profile and the Claude Hermes hybrid.

## When to use it

Use **native Telegram attach** (the platform reply tool with `files=[…]`) for:
- Images under 10MB (PNG/JPG/WebP — render as inline photos).
- Audio under 10MB (OGG — sends as voice bubble).
- Short videos under 10MB (MP4 — plays inline).
- Small PDFs and Office files Kosta opens in the moment.

Use **`plik upload_file` / `upload_files` / `upload_text`** for:
- Any file > 10MB (Telegram's document cap is 50MB and gets unreliable above ~10MB).
- Formats Telegram won't preview (zip, sqlite, log dumps, build artifacts).
- Anything Kosta should be able to reopen from another device or after the chat scrolls away.
- Code/log dumps the model would otherwise paste as a giant wall of text — use `upload_text` with a meaningful filename.

If both are viable, prefer native attach so Kosta gets the inline render.

## TTL policy

Plik's default TTL is **24h**. Choose explicitly per upload:

| Situation | `ttl` | Notes |
| --- | --- | --- |
| One-off oversized artifact, ephemeral | `0` (server default = 24h) | Also include the source path or regeneration command in the reply. |
| Week-scope working artifact | `604800` (7 days) | Logs being investigated, screenshots from an ongoing thread. |
| "For the record" / archived deliverable | `2592000` (30 days) | The server max — anything longer requires a config change. |
| Sensitive payload | combine TTL with `password` and `one_shot: true` | Encrypts at rest, deletes after first download. |

Avoid quietly shipping a 24h link when Kosta said "stable" or "I'll need this later". State the TTL in the reply so he knows.

## Credentials and auditability

| Field | Value |
| --- | --- |
| 1Password vault | `CLI` |
| 1Password item | `Plik (Mac Studio)` |
| Backend URL | `https://macstudio.tailf7342a.ts.net/plik` |
| Plik account | `ildunari` (admin) |
| API token field | `credential` (used by `plik --mcp`, hand-off via `~/.plikrc`) |
| Web/Telegram-mini-app login field | `password` |
| CLI config | `~/.plikrc` — `URL` + `Token` |

The token is loaded by the MCP server from `~/.plikrc` at process start. Hermes profiles and the Claude hybrid all spawn `plik --mcp` under the kosta UID, so they share the same `~/.plikrc` and the same `ildunari` token.

### Verify before relying on it

```bash
op read "op://CLI/Plik (Mac Studio)/credential" >/dev/null && \
  curl -sS -o /dev/null -w 'plik health: HTTP %{http_code}\n' https://macstudio.tailf7342a.ts.net/plik/version
```

Both should succeed (1Password item readable, plik /version returns 200) before trusting the upload path. If either fails, fall back to native attach (for small files) or tell Kosta the plik backend is unreachable — do not retry blindly.

If the token has rotated (1P updated, but a stale `~/.plikrc` is still cached on the gateway process), the upload will return `403 Forbidden : invalid token`. Re-pull via:

```bash
TOKEN=$(op read "op://CLI/Plik (Mac Studio)/credential")
printf 'URL = "https://macstudio.tailf7342a.ts.net/plik"\nToken = "%s"\n' "$TOKEN" > ~/.plikrc
```

Then restart the calling gateway so the MCP child reloads `~/.plikrc`.

## MCP tools

`plik --mcp` exposes these tools:

- `upload_text(content, filename, ttl?, one_shot?, password?, comments?)` — inline text → named file.
- `upload_file(path, ttl?, one_shot?, password?, comments?, stream?)` — single file by absolute path.
- `upload_files(paths, ttl?, one_shot?, password?, comments?)` — multiple files in one upload.
- `server_info()` — version, feature flags, what's allowed.
- `list_profiles()` — Plik CLI profiles defined in `~/.plikrc` (currently just the default).

All upload tools return `{"url": "https://macstudio.tailf7342a.ts.net/plik/#/?id=…", "id": "…", "expires_at": "…"}` shape. The URL points at the bundled Plik UI; rewrite to the custom UI (see "Two UI surfaces" below) only when sharing the link with a human who will load it interactively. For machine-to-machine and quick chat shares, the bundled URL is fine.

## Two UI surfaces

There are two web UIs on top of the same Plik backend:

| Route | What it is | When |
| --- | --- | --- |
| `/plik/` | Plik's bundled Angular SPA (1.4.2 stock) | Fallback / admin. Stays untouched as a recovery path. Also the default for share links returned by the MCP tools. |
| `/plik/ui/` | Custom UI built for Hermes (dark editorial theme, harmonized with the Hermes mini-app dock) | What humans actually use — Hermes mini-app dock Plik tab and Claude hybrid Plik tab both route here. |

The custom UI's HTML/CSS/JS lives at `/Users/Kosta/plik-ui/` and is served by an nginx Docker container (`plik-ui`, port 9080) bound there read-only. Tailscale Funnel forwards `/plik/ui/...` to that nginx; everything else under `/plik` continues to go to the Plik backend at port 8080. Sub-paths:

- `/plik/ui/` — upload composer (drag-drop + all toggles + real QR + share URL).
- `/plik/ui/inbox.html` — list/filter/revoke your uploads.
- `/plik/ui/d.html?id=…` — public download page for a share (handles password-protected uploads via HTTP Basic auth modal, renders comments as markdown).
- `/plik/ui/m/` and `/plik/ui/m/inbox.html` — compact Telegram-mini-app variants of the same pages.
- `/plik/ui/login.html` — local-login form. After login, sessions auto-redirect.

Auth model in the custom UI: standard Plik cookie + `X-XSRFToken` (cookie has Path=/plik so it's readable from /plik/ui/*). API token auth via `X-PlikToken` is also supported by the server but the UI uses cookies for simplicity.

To swap the public share-URL shape over to the custom UI, edit `shareUrl()` in `/Users/Kosta/plik-ui/assets/api.js` — it already builds `/plik/ui/d.html?id=…`. If MCP tools should return the custom URL shape too, that's a server-side rewrite (Plik's `PlikDomain` only controls the host, not the path).

## Edge cases

- **Plik backend down**: MCP call returns an error. Surface "plik backend is unreachable, falling back to inline attach for small files" — never silently drop the artifact.
- **Disk full on Studio**: `~/plik-data/` lives on the boot disk; periodically `du -sh ~/plik-data` and prune expired uploads with `plik` list/revoke.
- **Token leaked into logs**: rotate via `curl -b cookies -X DELETE …/me/token/<id>`, generate new one, update 1P + `~/.plikrc`, restart gateways. Never echo `TOKEN` in shell output.
- **Source-tagging**: `plik` does not record which agent uploaded which file. If you need to disambiguate, set `comments` to something like `"from: hermes-gpt"` and the comment shows on the share page.
- **Streaming uploads**: for ephemeral relays (forward a file someone sent you to Kosta without storing it on disk), set `stream: true`. The file is not persisted server-side; the download has to be ready when Kosta clicks the link.
- **Password-protected uploads**: when sharing secrets, pass `password`. The recipient gets HTTP basic auth before download.
- **`one_shot: true`**: deletes after first download. Good for tokens/secrets sent in chat that Kosta will read once.

## Operator

### Plik backend (the API)

- Container: `docker ps --filter name=plik`
- Config file: `~/plik-config/plikd.cfg` (host-mounted into container)
- Data + sqlite DB: `~/plik-data/` (host-mounted)
- Restart: `docker restart plik` (no Hermes-gateway impact)
- Public path: `https://macstudio.tailf7342a.ts.net/plik` (Tailscale Funnel → `127.0.0.1:8080/plik`)
- `Path = "/plik"` is set in `plikd.cfg` so the server handles the prefix
- `FeatureAuthentication = "forced"` — no anonymous uploads, ever
- `PlikDomain = "https://macstudio.tailf7342a.ts.net"` — Plik generates links matching the public origin

### Custom UI (the browser frontend)

- Container: `docker ps --filter name=plik-ui` (nginx:alpine, port 9080)
- Static root: `/Users/Kosta/plik-ui/` (bind-mounted read-only)
- Nginx config: `/Users/Kosta/plik-ui-conf/nginx.conf`
- Public path: `https://macstudio.tailf7342a.ts.net/plik/ui` (Tailscale Funnel `/plik/ui` → `127.0.0.1:9080`)
- Restart: `docker restart plik-ui` (no Hermes-gateway impact)
- Cache: currently `Cache-Control: no-store` while iterating; can flip back to a short cache once the layout stabilises

To edit the UI: change files under `/Users/Kosta/plik-ui/`, refresh the browser. No build step. Note that `m/index.html` and `m/inbox.html` are byte copies of `index.html` and `inbox.html` with `<body class="tg">` swapped in — patch the parents and re-copy.

### Tailscale Funnel routes (state-changing — be careful)

The funnel is shared across many services. To list the live routing without touching it:

```bash
tailscale serve status
```

Funnel routes touching Plik:
- `/plik` → `http://127.0.0.1:8080/plik` (Plik backend)
- `/plik/ui` → `http://127.0.0.1:9080` (nginx serving the custom UI)
- `/plik-ui` → `http://127.0.0.1:9080` (alias — kept while older bot/mini-app links still reference it)

Tailscale uses longest-prefix-match, so `/plik/ui/...` correctly hits nginx while `/plik/...` (anything else) hits Plik. Don't add a `/` route to the same hostname — it shadows everything.

If `tailscale serve --bg --set-path=X ...` accidentally turns off funnel, restore with `tailscale serve --bg --https=443 --set-path=X ...` (note `--https=443` — that's what flags the route as funnel-exposed instead of tailnet-only).

If you change anything operational (config flags, auth model, retention, the mounted-paths, the funnel layout, the UI layout), update this skill in canonical Skillshare source, sync, commit, push.
