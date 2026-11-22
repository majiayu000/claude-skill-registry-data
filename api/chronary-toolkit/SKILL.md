---
name: chronary-toolkit
description: Chronary Toolkit — 50 pre-built tools with framework adapters for Vercel AI SDK, OpenAI, LangChain, Mastra, and MCP.
---

# Chronary Toolkit

The `@chronary/toolkit` package provides 50 pre-built tools for AI agent frameworks. Each tool maps to Chronary API operations with typed parameters, descriptions, and MCP annotations.

```bash
npm install @chronary/toolkit
```

## Available Tools

### Calendars (5 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `list_calendars` | List calendars, optionally filtered by agent. Returns paginated results. | Yes | No |
| `get_calendar` | Get a calendar by its ID, including its name, timezone, and iCal feed URL. | Yes | No |
| `create_calendar` | Create a new calendar. Specify a name and IANA timezone. Optionally scope it to an agent. | No | Yes |
| `update_calendar` | Update a calendar's name, timezone, or metadata. | No | Yes |
| `delete_calendar` | Permanently delete a calendar and all its events. | No | Yes |

### Events (7 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `list_events` | List events on a calendar or for an agent. Supports date range and status filters. Provide calendar_id or agent_id. | Yes | No |
| `get_event` | Get a specific event by its calendar ID and event ID. | Yes | No |
| `create_event` | Create a new event on a calendar. The event blocks the agent's availability during the specified time window and appears in availability queries. | No | Yes |
| `update_event` | Update an existing event's title, times, status, or other properties. | No | Yes |
| `cancel_event` | Delete or cancel an event from a calendar. The event is marked cancelled and excluded from future availability calculations. | No | Yes |
| `confirm_event` | Promote a held event to a confirmed booking. The event must currently have status="hold" and its hold_expires_at must not have passed. | No | Yes |
| `release_event` | Manually release a held event before its hold_expires_at. The event must currently have status="hold". Frees the slot for other agents to book. | No | Yes |

### Agents (5 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `create_agent` | Register your agent (AI assistant, human participant, or resource) with Chronary so it can own calendars, events, and webhooks. | No | Yes |
| `list_agents` | List all agents in your organization. Returns paginated results. | Yes | No |
| `get_agent` | Fetch a single agent by ID. An agent represents an AI assistant, human, or shared resource (e.g. a meeting room). | Yes | No |
| `update_agent` | Update an agent's name, description, metadata, or status (active/paused). Requires an org-level API key. | No | Yes |
| `delete_agent` | Decommission an agent. This marks the agent as decommissioned and revokes all of its scoped API keys. Requires an org-level API key. | No | Yes |

### Availability (2 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `get_availability` | Check when a single agent is free within a time range. Returns available time slots and optionally busy blocks. | Yes | No |
| `find_meeting_time` | Find time slots when multiple agents are all free simultaneously. All agents must be free during the returned slots. | Yes | No |

### Calendar Context (1 tool)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `get_calendar_context` | Get a calendar's temporal context in a single call: the current event, the next upcoming event, recent past events, a short upcoming window, and the owning agent's status. | Yes | No |

### Scheduling Proposals (6 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `create_proposal` | Create a scheduling proposal — send candidate time slots to one or more participant agents so they can accept, decline, or counter-propose. Requires an org-level API key and a Developer or Pro plan. | No | Yes |
| `list_proposals` | List scheduling proposals for the org. Filter by status or organizer_agent_id. Requires an org-level API key. | Yes | No |
| `get_proposal` | Get a scheduling proposal by id, including its slots and per-participant responses. Requires an org-level API key. | Yes | No |
| `respond_to_proposal` | Submit a response (accept / decline / counter) on behalf of one participant agent to an open proposal. Requires an org-level API key and a Developer or Pro plan. | No | Yes |
| `resolve_proposal` | Force-resolve an open proposal using responses collected so far. Picks the highest-scoring slot and creates a confirmed calendar event. Requires an org-level API key and a Developer or Pro plan. | No | Yes |
| `cancel_proposal` | Cancel an open proposal. Fires a proposal.cancelled webhook with reason="organizer_cancelled". Requires an org-level API key. Works on every plan. | No | Yes |

### Availability Rules (3 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `set_availability_rules` | Set or replace the availability rules on a calendar — buffer times before/after events and optional per-day working hours. Upsert: overwrites any existing rules. | No | Yes |
| `get_availability_rules` | Read the buffer times and working-hours rules configured on a calendar. Returns the rules row, or an error if none are set. | Yes | No |
| `clear_availability_rules` | Remove the availability rules from a calendar, reverting to the default (no buffers, no working-hours mask). | No | Yes |

### Webhooks (6 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `list_webhooks` | List all webhook subscriptions for the organization. | Yes | No |
| `get_webhook` | Get a webhook subscription by its ID. | Yes | No |
| `create_webhook` | Create a webhook subscription to receive event notifications at a URL. Payloads are signed with HMAC-SHA256. | No | Yes |
| `update_webhook` | Update a webhook's URL, subscribed events, or active status. | No | Yes |
| `delete_webhook` | Delete a webhook subscription. No further events will be delivered to this URL. | No | Yes |
| `list_webhook_deliveries` | List delivery attempts for a webhook subscription, with per-status counts (pending/delivered/failed). Use this to debug failing deliveries. Requires an org-level API key. | Yes | No |

### iCal Subscriptions (8 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `list_ical_subscriptions` | List external calendar imports (iCal subscriptions) for an agent. | Yes | No |
| `get_ical_subscription` | Get an iCal subscription by its ID, including sync status and last error. | Yes | No |
| `subscribe_ical` | Link an external iCal feed (e.g. a human's Google Calendar) to an agent's calendar so external events appear in availability calculations. Events are synced every 30 minutes. | No | Yes |
| `update_ical_subscription` | Update an iCal subscription's label or feed URL. | No | Yes |
| `delete_ical_subscription` | Remove an external calendar import. Previously synced events remain on the calendar. | No | Yes |
| `sync_ical_subscription` | Start an immediate fetch of an iCal subscription instead of waiting for the next scheduled poll. Paused feeds must be resumed first; one manual sync per feed per minute. | No | Yes |
| `pause_ical_subscription` | Pause an iCal subscription: polls skip it until it is resumed. | No | Yes |
| `resume_ical_subscription` | Resume a paused or failing iCal subscription and clear its last error. | No | Yes |

### Scoped Keys (3 tools)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `create_scoped_key` | Create an agent-scoped API key (chr_ak_*) that can only act on behalf of a single agent. The plaintext key is returned exactly once. Requires an org-level API key. | No | Yes |
| `list_scoped_keys` | List all live (non-revoked) agent-scoped API keys for this org. Returns key metadata only — never the plaintext secret. Requires an org-level API key. | Yes | No |
| `revoke_scoped_key` | Revoke an agent-scoped API key by ID. Revocation is permanent (cannot be un-revoked); the key stops authenticating within about a minute. Requires an org-level API key. | No | Yes |

### Audit Log (1 tool)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `get_audit_log` | List audit-log entries for the calling org — mutating operations and auth-lifecycle events, newest first. Results are clamped to the plan's retention window. Requires an org-level API key. | Yes | No |

### Terms (1 tool)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `accept_terms` | Re-accept the current Chronary terms of service on behalf of the calling org. Use this when responses carry the Chronary-Terms-Upgrade-Required header. Requires an org-level API key. | No | Yes |

### Usage (1 tool)

| Tool | Description | Read-only | Requires confirmation |
|------|-------------|-----------|-----------------------|
| `get_usage` | Get quota and usage statistics for the current billing period. | Yes | No |
| `get_usage_history` | Get monthly usage totals for the last 1-12 UTC months. | Yes | No |

## Framework Adapters

### Vercel AI SDK

```typescript
import { ChronaryToolkit } from '@chronary/toolkit/ai-sdk';

const toolkit = new ChronaryToolkit({ apiKey: process.env.CHRONARY_API_KEY });
const tools = toolkit.getTools();

// Use with generateText or streamText
import { generateText } from 'ai';
const result = await generateText({
  model: yourModel,
  tools,
  prompt: 'Schedule a meeting tomorrow at 2pm on my work calendar',
});
```

### OpenAI Function Calling

```typescript
import { ChronaryToolkit } from '@chronary/toolkit/openai';

const toolkit = new ChronaryToolkit({ apiKey: process.env.CHRONARY_API_KEY });
const tools = toolkit.getTools();

// Returns OpenAI-formatted function definitions
// Use with openai.chat.completions.create({ tools })
```

### LangChain

```typescript
import { ChronaryToolkit } from '@chronary/toolkit/langchain';

const toolkit = new ChronaryToolkit({ apiKey: process.env.CHRONARY_API_KEY });
const tools = toolkit.getTools();

// Returns LangChain StructuredTool instances
// Use with AgentExecutor or tool-calling chains
```

### Mastra

```typescript
import { ChronaryToolkit } from '@chronary/toolkit/mastra';

const toolkit = new ChronaryToolkit({ apiKey: process.env.CHRONARY_API_KEY });
const tools = toolkit.getTools();

// Returns Mastra-compatible tool definitions
```

### MCP (Model Context Protocol)

```typescript
import { ChronaryToolkit } from '@chronary/toolkit/mcp';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

const server = new McpServer({ name: 'chronary', version: '1.0.0' });
const toolkit = new ChronaryToolkit({ apiKey: process.env.CHRONARY_API_KEY });
toolkit.registerAll(server);
```

## Selective Tool Loading

Load only the tools you need:

```typescript
const toolkit = new ChronaryToolkit({
  apiKey: process.env.CHRONARY_API_KEY,
  tools: ['list_calendars', 'create_event', 'find_meeting_time'],
});
```

## Error Handling

All tools return a structured result:

```typescript
// Success
{ result: { id: 'cal_...', name: 'Work', ... }, isError: false }

// Error
{ result: { error: { type: 'not_found', message: '...' } }, isError: true }
```

Tools never throw — they return `isError: true` with details. This is safe for agent loops.
