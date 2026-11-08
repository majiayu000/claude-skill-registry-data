---
name: miro
description: Miro integration for AI agents via ClawLink — browser login, no API key setup. Connect miro through ClawLink's hosted setup. Use this skill when the user wants to work with Miro (Productivity) — connect Miro, read or update Miro data, or take actions in Miro from chat instead of saying you cannot access it.
---

# Miro

Use **Miro** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Miro once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect miro   # opens browser → authorize Miro
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Miro

```bash
npx @useclawlink/cli actions miro "<what you want to do>"   # find an action
npx @useclawlink/cli describe miro <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run miro <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `miro_attach_tag_to_item` | Tool to attach an existing tag to a specific item on a Miro board. Use when you need to associate a tag with an item after confirming the board, item, and tag IDs. Note that card and sticky note items can have up to 8 tags. |
| `miro_create_app_card_item` | Tool to add an app card item to a board. Use when you need to push a rich preview card with custom fields into a Miro board. Returns the created card; the card ID is nested under data.id in the response, not at the top level. Burst writes may trigger HTTP 429; honor the Retry-After header before retrying. |
| `miro_create_board` | Tool to create a new board. Use when you need to set up a board with a specific name, description, and policies. Example: 'Create a new board named Project Plan'. If workspace board quota is reached, returns HTTP 400; use MIRO_GET_BOARDS to reuse an existing board instead. |
| `miro_create_card_item` | Tool to create a card item on a Miro board. Use when you need to add task cards with titles, descriptions, due dates, and assignees. |
| `miro_create_connector` | Tool to create a connector (edge/arrow) that links two existing board items. Use after creating or locating the two endpoint items (shapes/cards/stickies) to establish visual relationships in flowcharts and diagrams. Both start and end items must be specified; connectors cannot be created with loose endpoints. |
| `miro_create_document_item` | Tool to create a document item on a Miro board by providing a URL to the document. Use when you need to attach a document (PDF, DOC, etc.) to a board from a publicly accessible URL. |
| `miro_create_document_item_using_file_from_device` | Tool to create a document item on a Miro board using a URL to the document. Use when you need to add a document (PDF, DOC, etc.) to a board from a publicly accessible URL. |
| `miro_create_embed_item` | Tool to create an embed item on a Miro board by providing a URL to embed content (YouTube videos, websites, etc.). Use when you need to add embedded content from external sources to a board. |
| `miro_create_frame_item` | Tool to add a frame item to a Miro board. Use frames to group and organize diagram regions (e.g., swimlanes, sections, slides). |
| `miro_create_group` | Tool to create a group on a Miro board by grouping multiple items together. Use when you need to organize related board items (shapes, sticky notes, cards, etc.) into a single logical group. |
| `miro_create_image_item_using_local_file` | Tool to create an image item on a Miro board by uploading a local image file. Use when you need to add an image from the user's device to a board, rather than referencing an external URL. |
| `miro_create_items_in_bulk` | Tool to create multiple items on a Miro board in a single request. Use when you need to add 1-20 items (text, sticky notes, shapes, cards, frames, etc.) efficiently. Items are created atomically in one API call. |

## Notes

- **No API key for Miro itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect miro`.
- The action list above is a snapshot; `npx @useclawlink/cli actions miro` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
