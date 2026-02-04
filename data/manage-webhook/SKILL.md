---
name: manage-webhook
description: Manage webhooks in Sinch Conversation API. Use when the user wants to create a webhook, update webhook settings, list webhooks, delete a webhook, get webhook details, configure webhook triggers, or manage webhook callbacks. Handles webhook lifecycle management including creation, updates, deletion, and trigger configuration.
---

# Webhook Management

Manage webhooks in Sinch Conversation API using the Conversation API specification. Note: MCP tools do not provide webhook management tools, so this skill always uses the Conversation API endpoints. Webhooks receive callbacks for various events like message delivery, inbound messages, contact updates, and conversation events.

## Instructions

1. **Identify the operation from user request:**
   - **Create webhook**: New webhook with target URL and triggers
   - **Update webhook**: Modify webhook target, triggers, or secret
   - **List webhooks**: Retrieve webhooks for an app or project
   - **Get webhook**: Retrieve specific webhook details
   - **Delete webhook**: Remove a webhook

2. **Extract webhook information:**
   - Webhook ID: Unique identifier for existing webhooks
   - Target URL: The callback URL where webhooks will be sent
   - App ID: The app this webhook belongs to (required for creation)
   - Triggers: Array of webhook triggers (MESSAGE_DELIVERY, MESSAGE_INBOUND, CONTACT_CREATE, etc.)
   - Secret: Optional secret for signing webhook payloads
   - Target type: HTTP (default) or DISMISS

3. **Use Conversation API endpoints to perform operations:**
   - **Note**: MCP Sinch does not provide webhook management tools, so this skill always uses the Conversation API endpoints
   - **Create webhook**: `POST /v1/projects/{project_id}/webhooks` (Operation ID: `Webhooks_CreateWebhook`)
   - **Update webhook**: `PATCH /v1/projects/{project_id}/webhooks/{webhook_id}` (Operation ID: `Webhooks_UpdateWebhook`)
   - **Get webhook**: `GET /v1/projects/{project_id}/webhooks/{webhook_id}` (Operation ID: `Webhooks_GetWebhook`)
   - **List webhooks**: `GET /v1/projects/{project_id}/apps/{app_id}/webhooks` (Operation ID: `Webhooks_ListWebhooks`)
   - **Delete webhook**: `DELETE /v1/projects/{project_id}/webhooks/{webhook_id}` (Operation ID: `Webhooks_DeleteWebhook`)
   - Authentication: Use Basic Auth or OAuth2 with credentials from environment variables
   - Region: Use CONVERSATION_REGION environment variable (us, eu, or br)
   - Base URL: `https://{region}.conversation.api.sinch.com`

4. **Response handling:**
   - Confirm successful operations with webhook ID
   - Display webhook information clearly (target URL, triggers, app ID)
   - Show webhook configuration details
   - Report errors with actionable guidance

## Examples

**Natural language prompts that trigger this Skill:**
- "Create a webhook for https://example.com/webhook with MESSAGE_DELIVERY trigger"
- "List all webhooks for app abc123"
- "Update webhook xyz789 to add MESSAGE_INBOUND trigger"
- "Delete webhook with ID webhook-123"
- "Show me webhook details for webhook-456"
- "Add CONTACT_CREATE trigger to my webhook"
- "What webhooks are configured for this app?"

**Conversation API Usage (Required - no MCP alternative):**
1. **Note**: MCP Sinch does not provide webhook management tools, so this skill always uses the Conversation API
2. Use the Conversation API endpoints for webhook operations (see endpoints above)
3. Authentication: Use Basic Auth with CONVERSATION_KEY_ID and CONVERSATION_KEY_SECRET, or OAuth2
4. Include required headers: `Authorization`, `Content-Type: application/json`
5. For create webhook, include request body with `app_id` (required), `target`, `target_type` (HTTP or DISMISS), `triggers` array, and optional `secret`
6. For update webhook, use PATCH with `update_mask` parameter to specify which fields to update
7. Maximum 5 webhooks per app

## Webhook Triggers

Available webhook triggers:
- **MESSAGE_DELIVERY**: Delivery receipts for sent messages
- **EVENT_DELIVERY**: Delivery receipts for sent events
- **MESSAGE_INBOUND**: Inbound messages from end users
- **EVENT_INBOUND**: Inbound events from end users
- **CONVERSATION_START**: New conversation started
- **CONVERSATION_STOP**: Active conversation stopped
- **CONVERSATION_DELETE**: Conversation deleted
- **CONTACT_CREATE**: New contact created
- **CONTACT_UPDATE**: Contact updated
- **CONTACT_DELETE**: Contact deleted
- **CONTACT_MERGE**: Contacts merged
- **OPT_IN**: Opt-in events
- **OPT_OUT**: Opt-out events
- **CAPABILITY**: Capability query results
- **CHANNEL_EVENT**: Channel-specific events
- **SMART_CONVERSATION**: Smart conversation analysis
- **MESSAGE_INBOUND_SMART_CONVERSATION_REDACTION**: Smart conversation redaction
- **CONTACT_IDENTITIES_DUPLICATION**: Contact identity duplication detected
- **RECORD_NOTIFICATION**: Record notifications
- **MESSAGE_SUBMIT**: Message submission events

## Webhook Operations

### Create Webhook
- Requires `app_id` in request body
- Specify `target` URL (must be HTTPS for production)
- Set `target_type` (HTTP or DISMISS)
- Configure `triggers` array with one or more trigger types
- Optional `secret` for signing webhook payloads
- Maximum 5 webhooks per app

### Update Webhook
- Use PATCH method with `update_mask` parameter
- Can update `target`, `triggers`, `secret`, `target_type`
- Include only fields to update in request body

### List Webhooks
- List webhooks for a specific app: `GET /v1/projects/{project_id}/apps/{app_id}/webhooks`
- Returns array of webhooks with their configuration

### Get Webhook
- Retrieve specific webhook by ID
- Returns full webhook configuration including triggers and target

### Delete Webhook
- Remove webhook by ID
- Webhook will stop receiving callbacks immediately

## Notes

- **MCP Note**: MCP Sinch does not provide webhook management tools, so this skill always uses the Conversation API endpoints
- Maximum 5 webhooks per app
- Webhook target URLs should use HTTPS in production
- Webhook secret is optional but recommended for verifying webhook authenticity
- Triggers can be combined - a webhook can subscribe to multiple trigger types
- Webhooks are scoped to apps - each webhook belongs to a specific app
- Use the Conversation API endpoints directly - reference the OpenAPI spec for exact parameter names and types
- Webhook callbacks are sent as HTTP POST requests to the target URL
- For testing, you can use HTTP URLs, but production webhooks should use HTTPS

