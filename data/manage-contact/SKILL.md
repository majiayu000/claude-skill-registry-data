---
name: manage-contact
description: Manage contacts in Sinch Conversation API. Use when the user wants to create a contact, update contact information, list contacts, find a contact, get contact details, add channels to a contact, or manage contact channels. Handles contact creation, updates, and channel associations.
---

# Contact Management

Manage contacts and their channel associations in Sinch Conversation API using the Conversation API specification. Note: MCP tools do not provide contact management tools, so this skill always uses the Conversation API endpoints. Contacts represent end-users and can span multiple messaging channels.

## Instructions

1. **Identify the operation from user request:**
   - **Create contact**: New contact with channel identity
   - **Update contact**: Modify contact information or add channels
   - **List contacts**: Retrieve contacts with optional filtering
   - **Get contact**: Retrieve specific contact details
   - **Find contact**: Search for contact by phone number, email, or ID

2. **Extract contact information:**
   - Contact identifier: phone number, email, contact ID, or name
   - Channel identities: WhatsApp, SMS, or other channels with identities
   - Display name: Contact's display name
   - Email: Contact's email address
   - Language: Preferred language code (e.g., EN_US)

3. **Use Conversation API endpoints to perform operations:**
   - **Note**: MCP Sinch does not provide contact management tools, so this skill always uses the Conversation API endpoints
   - **Create contact**: `POST /v1/projects/{project_id}/contacts` (Operation ID: `Contact_CreateContact`)
   - **Update contact**: `PATCH /v1/projects/{project_id}/contacts/{contact_id}` (Operation ID: `Contact_UpdateContact`)
   - **Get contact**: `GET /v1/projects/{project_id}/contacts/{contact_id}` (Operation ID: `Contact_GetContact`)
   - **List contacts**: `GET /v1/projects/{project_id}/contacts` (Operation ID: `Contact_ListContacts`)
   - Authentication: Use Basic Auth or OAuth2 with credentials from environment variables
   - Region: Use CONVERSATION_REGION environment variable (us, eu, or br)
   - Base URL: `https://{region}.conversation.api.sinch.com`

4. **Response handling:**
   - Confirm successful operations with contact ID
   - Display contact information clearly
   - Show associated channels for contacts
   - Report errors with actionable guidance

## Examples

**Natural language prompts that trigger this Skill:**
- "Create a contact for John with WhatsApp number +1234567890"
- "Add SMS channel to contact abc123"
- "Show me contact details for +1234567890"
- "List all contacts"
- "Find contact by phone number +1234567890"
- "Update contact abc123 with email john@example.com"
- "What channels does contact xyz789 have?"

**Conversation API Usage (Required - no MCP alternative):**
1. **Note**: MCP Sinch does not provide contact management tools, so this skill always uses the Conversation API
2. Use the Conversation API endpoints for contact operations (see endpoints above)
3. Authentication: Use Basic Auth with CONVERSATION_KEY_ID and CONVERSATION_KEY_SECRET, or OAuth2
4. Include required headers: `Authorization`, `Content-Type: application/json`
5. For list contacts, use query parameters: `page_size`, `page_token`, `external_id`, `channel`, `identity`
6. For create/update, include request body with `channel_identities`, `display_name`, `email`, `language`, `metadata`

## Contact Operations

### Create Contact
- Create with single channel identity
- Create with multiple channel identities
- Set display name, email, and language preferences

### Update Contact
- Add new channel identities
- Update display name or email
- Modify language preferences
- Update metadata

### Retrieve Contact
- Get contact by ID
- Get contact by channel identity (phone number, etc.)
- List contacts with pagination
- Filter contacts by criteria

## Channel Identity Format

Channel identities are channel-specific:
- **WHATSAPP**: Phone number with country code (e.g., +1234567890)
- **SMS**: Phone number with country code (e.g., +1234567890)
- **MESSENGER**: Facebook Page Scoped ID (PSID)
- **VIBERBM**: Viber user ID
- **INSTAGRAM**: Instagram user ID
- **TELEGRAM**: Telegram user ID
- **LINE**: LINE user ID
- **WECHAT**: WeChat OpenID
- **KAKAOTALK**: KakaoTalk user ID
- **APPLEBC**: Apple user identifier

## Notes

- **MCP Note**: MCP Sinch does not provide contact management tools, so this skill always uses the Conversation API endpoints
- Contacts can have multiple channel identities
- Channel identities must be unique per channel
- Use the Conversation API endpoints directly - reference the OpenAPI spec for exact parameter names and types
- Contact creation is automatic when sending messages to new recipients
- Contacts are scoped to apps
- List contacts supports filtering by `channel` and `identity` query parameters
- Maximum page_size for list contacts is 20 (default is 10)

