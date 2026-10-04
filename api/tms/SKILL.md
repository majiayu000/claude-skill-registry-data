---
name: tms
version: "1.0.5"
description: Manage downloads via Telegram Media Server (TMS) REST API — add by URL (video/magnet/torrent), list, delete, search torrents.
metadata:
  {"openclaw":{"requires":{"env":[]},"primaryEnv":"TMS_API_URL"}}
---

# TMS (Telegram Media Server) API skill

Use this skill when the user wants to add downloads, check download status, stop a download, or search for torrents via the TMS backend. All requests go to the TMS REST API.

**How to use:** This skill does not add a "tms" command. The agent must make HTTP requests (GET/POST/DELETE) to the endpoints below. **Base URL:** use env `TMS_API_URL` if set; otherwise when TMS and OpenClaw run on the **same host**, use default **`http://127.0.0.1:8080`** (TMS default API listen). Do not add a trailing slash. To get the full API contract, fetch **`{base_url}/api/v1/openapi-llm.yaml`** (e.g. `http://127.0.0.1:8080/api/v1/openapi-llm.yaml`).

## Configuration

- **Base URL:** optional. From env `TMS_API_URL` (e.g. `http://tms-host:8080`). When not set and agent runs on the same host as TMS, use **`http://127.0.0.1:8080`** (TMS default).
- **Authentication:** optional. When TMS and OpenClaw run on the **same host**, TMS accepts requests from localhost without a key — `TMS_API_KEY` can be omitted. When OpenClaw runs on another host (or you want auth), set `TMS_API_KEY` and send every API request with either `Authorization: Bearer <TMS_API_KEY>` or header `X-API-Key: <TMS_API_KEY>`.

## Operations

1. **Health check** — `GET {TMS_API_URL}/api/v1/health` — returns `{"status":"ok"}` if the API is up.

2. **List downloads** — `GET {TMS_API_URL}/api/v1/downloads` — returns a JSON array of downloads with `id`, `title`, `status` (queued, downloading, converting, completed, failed, stopped), `progress`, `conversion_progress`, `error` (if failed), `position_in_queue` (if queued). Snapshot is best-effort.

3. **Add download** — `POST {TMS_API_URL}/api/v1/downloads` with JSON body `{"url": "<url>", "title": "<optional>"}`. URL can be: video URL (yt-dlp), magnet link (`magnet:...`), .torrent file URL, or (when Prowlarr is configured on TMS) Prowlarr proxy download URL. Prefer **magnet** from search results when adding a torrent. Optional `title` overrides the display name (e.g. from search result). For magnets without a display name in the link, the default title is "Magnet download"; size may show 0 until metadata is received; the status circle is yellow until resolved. Response: `201` with `{"id": <number>, "title": "<string>"}`. Use `id` for delete or status.

4. **Delete download** — `DELETE {TMS_API_URL}/api/v1/downloads/{id}` — stops and removes the download. Response: `204` no body. `id` is the numeric id from the add response or list.

5. **Search torrents** — `GET {TMS_API_URL}/api/v1/search?q=<query>&limit=20&quality=1080` — requires Prowlarr configured on TMS. `q` is required; `limit` (1–100, default 20) and `quality` (optional filter) may be used. Returns array of `{title, size, magnet, torrent_url, indexer_name, peers}`. When adding a download from search, use the **magnet** field in POST /downloads (or torrent_url if it is a direct .torrent link). You may pass `title` from the result for a clearer name in the list.

## Full API spec for tools

**Exact URL:** `{base_url}/api/v1/openapi-llm.yaml` where base_url is `TMS_API_URL` if set, else `http://127.0.0.1:8080` for same-host. Example: `http://127.0.0.1:8080/api/v1/openapi-llm.yaml`. Use this to get the full contract (parameters, schemas, examples) when building or invoking API calls.

## Webhook (optional)

If TMS is configured with `TMS_WEBHOOK_URL` pointing to an endpoint OpenClaw can receive, TMS will POST to that URL when a download completes, fails, or is stopped. Body: `id`, `title`, `status` (completed|failed|stopped), `error` (if failed), `event_id` (UUID). When `TMS_WEBHOOK_TOKEN` is set in TMS config, TMS sends `Authorization: Bearer <TMS_WEBHOOK_TOKEN>` (required for OpenClaw gateway hooks). Delivery is best-effort (no guaranteed delivery). Use this to notify the user in chat when a download finishes.
