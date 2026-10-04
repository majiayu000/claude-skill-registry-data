---
name: tms
version: "1.0.6"
description: Manage downloads via Telegram Media Server (TMS) REST API — add by URL (video/magnet/torrent), list, delete, search torrents.
metadata:
  {"openclaw":{"requires":{"env":[]},"primaryEnv":"TMS_API_URL"}}
---

# TMS (Telegram Media Server) API skill

Use this skill when the user wants to add downloads, check download status, stop a download, or search for torrents via the TMS backend. All requests go to the TMS REST API.

**How to use:** This skill does not add a "tms" command. The agent must make HTTP requests (GET/POST/DELETE) to the TMS endpoints. The **full API contract** (paths, request/response schemas, examples) is included in this document below — no need to fetch any URL to get the API spec. Use the OpenAPI spec (inline) section to build and invoke API calls.

## Base URL and authentication

- **Base URL:** Use env `TMS_API_URL` if set; otherwise, when TMS and OpenClaw run on the **same host**, use **`http://127.0.0.1:8080`** (TMS default API listen). Do not add a trailing slash. All endpoint paths in the spec use the prefix `/api/v1` — e.g. `GET /health` means **`GET {BaseURL}/api/v1/health`**.
- **Authentication:** Optional. When TMS and OpenClaw run on the same host, TMS accepts requests from localhost without a key — `TMS_API_KEY` can be omitted. When OpenClaw runs on another host (or you want auth), set `TMS_API_KEY` and send every API request with either `Authorization: Bearer <TMS_API_KEY>` or header `X-API-Key: <TMS_API_KEY>`.

## Operations (summary)

1. **Health check** — `GET {BaseURL}/api/v1/health` — returns `{"status":"ok"}` if the API is up.
2. **List downloads** — `GET {BaseURL}/api/v1/downloads` — returns a JSON array of downloads with `id`, `title`, `status` (queued, downloading, converting, completed, failed, stopped), `progress`, `conversion_progress`, `error` (if failed), `position_in_queue` (if queued). Snapshot is best-effort.
3. **Add download** — `POST {BaseURL}/api/v1/downloads` with JSON body `{"url": "<url>", "title": "<optional>"}`. URL can be: video URL (yt-dlp), magnet link (`magnet:...`), .torrent file URL, or (when Prowlarr is configured on TMS) Prowlarr proxy download URL. Prefer **magnet** from search results when adding a torrent. Optional `title` overrides the display name. Response: `201` with `{"id": <number>, "title": "<string>"}`. Use `id` for delete or status.
4. **Delete download** — `DELETE {BaseURL}/api/v1/downloads/{id}` — stops and removes the download. Response: `204` no body. `id` is the numeric id from the add response or list.
5. **Search torrents** — `GET {BaseURL}/api/v1/search?q=<query>&limit=20&quality=1080` — requires Prowlarr configured on TMS. `q` is required; `limit` (1–100, default 20) and `quality` (optional filter) may be used. Returns array of `{title, size, magnet, torrent_url, indexer_name, peers}`. When adding from search, use the **magnet** field in POST /downloads (or torrent_url); you may pass `title` from the result.

Detailed request/response schemas and status codes are in the **OpenAPI spec (inline)** below.

## OpenAPI spec (inline)

The following YAML is the full TMS API contract. Paths are relative to base path `/api/v1`; full URL = `{BaseURL}` + path (e.g. `{BaseURL}/api/v1/health`). Inline spec is copied from `internal/api/openapi/openapi-llm.yaml`; keep in sync when API changes.

```yaml
openapi: 3.1.0
info:
  title: TMS REST API
  description: |
    Telegram Media Server API. Use to add downloads by URL (video/magnet/torrent), list downloads with status,
    delete a download, or search torrents. All endpoints require Authorization Bearer or X-API-Key.
  version: 1.0.0

servers:
  - url: /api/v1
    description: Base path (prepend your TMS base URL, e.g. from TMS_API_URL)

tags:
  - name: health
  - name: downloads
  - name: search

security:
  - BearerAuth: []
  - ApiKeyHeader: []

paths:
  /health:
    get:
      tags: [health]
      summary: Check API availability
      description: Call to verify TMS API is reachable. Returns 200 and {"status":"ok"}. No auth required for this endpoint in some setups; if 401, send Bearer or X-API-Key.
      operationId: getHealth
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/HealthResponse' }

  /downloads:
    get:
      tags: [downloads]
      summary: List downloads
      description: |
        Call to get current downloads (queued, active, completed). Returns array of items with id, title, status (queued|downloading|converting|completed|failed|stopped), progress (0-100), conversion_progress, error (if failed), position_in_queue (if queued). Snapshot is best-effort.
      operationId: listDownloads
      responses:
        '200':
          description: Array of download items
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/DownloadItem' }
    post:
      tags: [downloads]
      summary: Create a download
      description: |
        Call to add a download. Body: JSON with "url" (required) and optional "title" (display name, e.g. from search). URL can be: video URL (yt-dlp), magnet link (magnet:...), .torrent file URL, or Prowlarr proxy download URL when Prowlarr is configured. Prefer magnet from search results. Response gives id (number) and title (string). Use this id for DELETE /downloads/{id}.
      operationId: addDownload
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/AddDownloadRequest' }
            example: { url: "magnet:?xt=urn:btih:abc123" }
      responses:
        '201':
          description: Download created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/AddDownloadResponse' }
        '400':
          description: Missing url or invalid URL
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '500':
          description: Server error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

  /downloads/{id}:
    delete:
      tags: [downloads]
      summary: Stop and remove a download
      description: Call to stop the download with given id and remove it. id is the numeric id returned by POST /downloads. Returns 204 with no body on success.
      operationId: deleteDownload
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: integer, minimum: 1 }
      responses:
        '204':
          description: Download stopped
        '400':
          description: Invalid id (not a number)
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '500':
          description: Server error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

  /search:
    get:
      tags: [search]
      summary: Search torrents
      description: |
        Call to search torrents (requires Prowlarr configured). Query param "q" (required): search string. "limit" (optional, 1-100, default 20): max results. "quality" (optional): filter by substring in release title (e.g. 1080). Returns array of objects with title, size, magnet, torrent_url, indexer_name, peers. When adding a download, prefer the magnet field in POST /downloads; you may also pass title from the result.
      operationId: searchTorrents
      parameters:
        - name: q
          in: query
          required: true
          schema: { type: string }
        - name: limit
          in: query
          schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
        - name: quality
          in: query
          schema: { type: string }
      responses:
        '200':
          description: Array of search results
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/SearchResultItem' }
        '400':
          description: Missing q
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '503':
          description: Search not configured or Prowlarr error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API Key
    ApiKeyHeader:
      type: apiKey
      in: header
      name: X-API-Key

  schemas:
    HealthResponse:
      type: object
      required: [status]
      properties:
        status: { type: string, example: "ok" }

    DownloadItem:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }
        status: { type: string, enum: [queued, downloading, converting, completed, failed, stopped] }
        progress: { type: integer, minimum: 0, maximum: 100 }
        conversion_progress: { type: integer, minimum: 0, maximum: 100 }
        error: { type: string }
        position_in_queue: { type: integer }

    AddDownloadRequest:
      type: object
      required: [url]
      properties:
        url: { type: string }
        title: { type: string, description: Optional display name e.g. from search result }

    AddDownloadResponse:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }

    SearchResultItem:
      type: object
      properties:
        title: { type: string }
        size: { type: integer }
        magnet: { type: string }
        torrent_url: { type: string }
        indexer_name: { type: string }
        peers: { type: integer }

    ErrorResponse:
      type: object
      required: [error]
      properties:
        error: { type: string }
```

## Webhook (optional)

If TMS is configured with `TMS_WEBHOOK_URL` pointing to an endpoint OpenClaw can receive, TMS will POST to that URL when a download completes, fails, or is stopped. Body: `id`, `title`, `status` (completed|failed|stopped), `error` (if failed), `event_id` (UUID). When `TMS_WEBHOOK_TOKEN` is set in TMS config, TMS sends `Authorization: Bearer <TMS_WEBHOOK_TOKEN>` (required for OpenClaw gateway hooks). Delivery is best-effort (no guaranteed delivery). Use this to notify the user in chat when a download finishes.
