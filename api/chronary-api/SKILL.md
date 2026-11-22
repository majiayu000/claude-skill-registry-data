---
name: chronary-api
description: |
  Chronary calendar API for AI agents — REST + MCP server, agent self-signup
  flow, calendar/event/proposal/availability model, webhook HMAC verification,
  iCal subscriptions, error envelopes, and rate-limit/quota semantics.

  TRIGGER when the user asks about any of: creating an agent or calendar
  programmatically, scheduling an event from an agent, querying free/busy or
  availability, multi-agent meeting coordination, temporal holds before
  booking, subscribing to a Google/Outlook/iCal feed, verifying webhook
  payloads, calling `chronary.ai` / `api.chronary.ai` / `chr_sk_` / `chr_ak_`
  / `agt_` / `cal_` / `evt_` IDs, the MCP server at `api.chronary.ai/mcp`,
  the `@chronary/sdk` / `chronary` Python / `@chronary/mcp` packages, the
  agent-self-signup endpoints (`POST /v1/agent/sign-up`, `/v1/agent/verify`),
  or anything that pairs the words "calendar" and "agent".

  SKIP when the user is asking about generic calendar libraries (`ical.js`,
  `node-ical`, RFC 5545 parsing without the Chronary API), Google Calendar
  API directly, or the Chronary CLI binary install (use `chronary.ai/install.sh`
  reference, not this skill).
---

# Chronary Calendar API

Chronary is a calendar-as-a-service API for AI agents. It lets agents own calendars, create events, query availability, subscribe to external iCal feeds, and receive webhook notifications.

Base URL: `https://api.chronary.ai`
OpenAPI spec: `https://api.chronary.ai/openapi.json`
Docs: `https://docs.chronary.ai`

## Data Model

```
Organization
  └── Agent (agt_)          — AI, human, or resource agent
        ├── Calendar (cal_) — timezone-aware calendar
        │     └── Event (evt_) — scheduled event with start/end time
        ├── Webhook (whk_)  — event notification subscription
        └── iCal Subscription (ics_) — external calendar import
```

Every resource belongs to an organization, scoped by API key.

## Authentication

All API requests require a Bearer token:

```
Authorization: Bearer chr_sk_...
```

Key prefixes:
- `chr_sk_` — org-level keys (full account access)
- `chr_ak_` — agent-scoped keys (limited to one agent's calendars / events)
- Legacy `chr_sk_live_*` / `chr_ak_live_*` keys issued before the test-mode removal still authenticate.

## Entity ID Prefixes

| Prefix | Entity |
|--------|--------|
| `agt_` | Agent |
| `cal_` | Calendar |
| `evt_` | Event |
| `whk_` | Webhook |
| `ics_` | iCal Subscription |
| `org_` | Organization |
| `spr_` | Scheduling Proposal |
| `slt_` | Proposal Slot |
| `rsp_` | Proposal Response |

## Endpoints

### Agents

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/agents` | Create an agent |
| GET | `/v1/agents` | List agents (filterable by type, status) |
| GET | `/v1/agents/{id}` | Get agent by ID |
| PATCH | `/v1/agents/{id}` | Update agent name, description, status, metadata |
| DELETE | `/v1/agents/{id}` | Soft-delete an agent |

Agent types: `ai`, `human`, `resource`
Agent statuses: `active`, `paused`, `decommissioned`

### Calendars

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/calendars` | Create a standalone calendar |
| POST | `/v1/agents/{agent_id}/calendars` | Create a calendar scoped to an agent |
| GET | `/v1/calendars` | List all calendars |
| GET | `/v1/agents/{agent_id}/calendars` | List calendars for an agent |
| GET | `/v1/calendars/{id}` | Get calendar by ID |
| PATCH | `/v1/calendars/{id}` | Update calendar name, timezone, metadata |
| DELETE | `/v1/calendars/{id}` | Soft-delete a calendar |

Calendars require an IANA timezone (e.g., `America/New_York`). Each calendar has an iCal feed URL for consumption by Google Calendar, Outlook, etc.

### Events

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/calendars/{cal_id}/events` | Create an event on a calendar |
| GET | `/v1/calendars/{cal_id}/events` | List events on a calendar |
| GET | `/v1/agents/{agent_id}/events` | List events across all agent's calendars |
| GET | `/v1/events/{id}` | Get event by ID |
| PATCH | `/v1/events/{id}` | Update event title, times, status, metadata |
| DELETE | `/v1/events/{id}` | Soft-delete an event |

Event statuses: `confirmed`, `tentative`, `cancelled`
Event sources: `internal` (created via API), `external_ical` (synced from iCal feed)
Filterable by: `start_after`, `start_before`, `status`, `source`

### Availability

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/agents/{id}/availability` | Free/busy slots for a single agent |
| GET | `/v1/calendars/{id}/availability` | Free/busy slots for a single calendar |
| GET | `/v1/availability` | Cross-agent intersection (multiple agents) |
| GET | `/v1/calendars/{id}/availability-rules` | Get scheduling rules (working hours, buffer time) |
| PUT | `/v1/calendars/{id}/availability-rules` | Set scheduling rules |
| DELETE | `/v1/calendars/{id}/availability-rules` | Remove scheduling rules |

Query parameters: `start` (ISO 8601), `end` (ISO 8601), `slot_duration` (`15m`, `30m`, `45m`, `1h`, `2h`), `include_busy` (boolean).

Cross-agent query also accepts: `agents` (comma-separated agent IDs), `calendars` (comma-separated calendar IDs).

Response returns `{ slots: [{ start, end }] }` — each slot is an available time window. With `include_busy=true`, also returns `per_agent_busy` with conflict details.

### Webhooks

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/webhooks` | Create a webhook subscription (returns signing secret) |
| GET | `/v1/webhooks` | List webhook subscriptions |
| GET | `/v1/webhooks/{id}` | Get webhook by ID |
| PATCH | `/v1/webhooks/{id}` | Update URL, events, or active status |
| DELETE | `/v1/webhooks/{id}` | Delete a webhook subscription |

Payloads are signed with HMAC-SHA256. Verify using the `X-Signature` and `X-Timestamp` headers.

### iCal Subscriptions

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/agents/{agent_id}/ical-subscriptions` | Subscribe to an external iCal feed |
| GET | `/v1/agents/{agent_id}/ical-subscriptions` | List subscriptions for an agent |
| GET | `/v1/ical-subscriptions/{id}` | Get subscription by ID |
| PATCH | `/v1/ical-subscriptions/{id}` | Update label or feed URL |
| DELETE | `/v1/ical-subscriptions/{id}` | Remove subscription |

External feeds are polled every 15 minutes. Trigger an immediate sync with `POST /v1/ical-subscriptions/{id}/sync`.

### iCal Feed (Public)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ical/{ical_token}` | Public iCal feed for a calendar (no auth required) |

### Usage

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/usage` | Current month's usage counters and plan limits |

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (no auth required) |

## Webhook Event Types

```
agent.created          — New agent created
agent.updated          — Agent properties changed
event.created          — New event created on a calendar
event.updated          — Event properties changed
event.deleted          — Event soft-deleted
event.started          — Event start time reached
event.ended            — Event end time reached
proposal.created       — Scheduling proposal created
proposal.responded     — Agent responded to a proposal
proposal.confirmed     — Proposal accepted and event created
proposal.expired       — Proposal expired without resolution
proposal.cancelled     — Proposal cancelled
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Validation error — check request body against schema |
| 401 | Invalid or missing API key |
| 404 | Resource not found (check ID and org scope) |
| 422 | Unprocessable — valid format but business rule violation |
| 429 | Rate limited (per API key: Free 10, Developer 25, Pro 50 req/sec) or monthly quota exceeded |
| 500 | Server error — retry with backoff |

Error response format:
```json
{
  "error": {
    "type": "validation_error",
    "message": "Human-readable description",
    "request_id": "req_..."
  }
}
```

## Pagination

List endpoints return paginated results:

```json
{
  "data": [...],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

Use `limit` (max 200) and `offset` query parameters to paginate.

## Rate Limits

- Per API key: 10 requests/second on Free, 25 on Developer, 50 on Pro
- Monthly quotas vary by plan (check `GET /v1/usage`)
- HTTP 429 responses include a `Retry-After` header
