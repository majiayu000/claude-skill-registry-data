---
name: whatsapp
description: WhatsApp Business integration for AI agents via ClawLink — browser login, no API key setup. Connect whatsapp through ClawLink's hosted setup. Use this skill when the user wants to work with WhatsApp Business (Communication) — connect WhatsApp Business, read or update WhatsApp Business data, or take actions in WhatsApp Business from chat instead of saying you cannot access it.
---

# WhatsApp Business

Use **WhatsApp Business** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect WhatsApp Business once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect whatsapp   # opens browser → authorize WhatsApp Business
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using WhatsApp Business

```bash
npx @useclawlink/cli actions whatsapp "<what you want to do>"   # find an action
npx @useclawlink/cli describe whatsapp <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run whatsapp <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `whatsapp_create_message_template` | Create a new message template for the WhatsApp Business Account. Templates must be approved by WhatsApp before they can be used. Templates are required for marketing messages and messages sent outside the 24-hour window. |
| `whatsapp_delete_message_template` | Delete a message template from the WhatsApp Business Account by name. This permanently removes the template and it cannot be recovered. When you delete a template by name, all templates with that name across all languages will be deleted. Names of deleted templates cannot be reused for 30 days. Important: Only delete templates that are no longer needed, as this operation is irreversible. |
| `whatsapp_get_business_profile` | Get the business profile information for a WhatsApp Business phone number. This includes business details like description, address, website, and contact info. |
| `whatsapp_get_media_info` | Get metadata and download URL for uploaded WhatsApp media. Returns media ID, download URL (valid for 5 minutes), MIME type, SHA256 hash, and file size. The download URL can be used to retrieve the actual media file. |
| `whatsapp_get_message_templates` | Get all message templates for the WhatsApp Business Account. Templates are required for sending messages outside the 24-hour window and for marketing/utility messages. |
| `whatsapp_get_phone_number` | Retrieve detailed information about a specific WhatsApp Business phone number. Returns phone number details including verification status, quality rating, display number, verified business name, throughput limits, and webhook configuration. Use this to check phone number status, settings, and capabilities. To get available phone number IDs, first call WHATSAPP_GET_PHONE_NUMBERS. |
| `whatsapp_get_phone_numbers` | Retrieve all phone numbers registered to your WhatsApp Business Account. Returns phone number IDs, display numbers, verification status, quality ratings, and messaging throughput limits. Use the phone number ID from the response to send WhatsApp messages via other API actions. |
| `whatsapp_get_template_status` | Get the status and details of a specific message template. This is useful for checking if a template has been approved, rejected, or is still pending review. |
| `whatsapp_send_contacts` | Send contacts WhatsApp number. Note: The message will be delivered to the recipient only if they have initiated a conversation first. |
| `whatsapp_send_interactive_buttons` | Send an interactive button message with up to 3 reply buttons to a WhatsApp user. Interactive button messages allow recipients to quickly respond by tapping predefined buttons. Perfect for yes/no questions, multiple choice selections, quick actions, or call-to-action scenarios. IMPORTANT REQUIREMENTS: - The recipient must be a registered WhatsApp user - The recipient must have messaged your business first within the last 24 hours (WhatsApp's customer service window) - You can include 1-3 buttons per message - Each button can have a title (max 20 chars) and unique ID (max 256 chars) Use cases: Customer service menus, appointment confirmations, feedback collection, product selections. |
| `whatsapp_send_interactive_list` | Send an interactive list message to a WhatsApp number. List messages display a menu of options organized into sections. Users tap a button to view the list and select one option. Perfect for product catalogs, service menus, or guided workflows. Supports up to 10 sections with up to 10 items per section (100 total options). Note: Recipients must have messaged you first within the last 24 hours to receive this message. |
| `whatsapp_send_location` | Send a location message with coordinates, name, and address to a WhatsApp user. This action allows you to share location information through WhatsApp Business API. The location message includes latitude/longitude coordinates, a location name, and address. Important: The recipient must have an active WhatsApp account. Additionally, you can only send free-form messages (like location messages) within the 24-hour customer service window after the recipient has initiated contact with your business. Outside this window, you must use approved message templates. Common error codes: - 133010: Recipient's phone number doesn't have a WhatsApp account - 131026: Message undeliverable (recipient may have blocked your business number) - 131047: Re-engagement message (outside 24-hour window, need to use template) |

## Notes

- **No API key for WhatsApp Business itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect whatsapp`.
- The action list above is a snapshot; `npx @useclawlink/cli actions whatsapp` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
