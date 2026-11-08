---
name: retellai
description: Retell AI integration for AI agents via ClawLink — browser login, no API key setup. Connect retellai through ClawLink's hosted setup. Use this skill when the user wants to work with Retell AI (AI & ML) — connect Retell AI, read or update Retell AI data, or take actions in Retell AI from chat instead of saying you cannot access it.
---

# Retell AI

Use **Retell AI** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Retell AI once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect retellai   # opens browser → authorize Retell AI
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Retell AI

```bash
npx @useclawlink/cli actions retellai "<what you want to do>"   # find an action
npx @useclawlink/cli describe retellai <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run retellai <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `retellai_add_community_voice` | Add a community voice from ElevenLabs to your Retell voice library. Use when you need to import a shared community voice for use in your agents. |
| `retellai_add_knowledge_base_sources` | Tool to add sources (documents, URLs, text) to an existing knowledge base in Retell AI. Use when you need to add additional content to a knowledge base. At least one of knowledge_base_texts, knowledge_base_files, or knowledge_base_urls should be provided. |
| `retellai_buy_a_new_phone_number_bind_agents` | This endpoint allows purchasing a new phone number with a specified area code and binding it to designated agents for inbound and outbound calls. It requires JSON with agent IDs and area code. Responses indicate the creation status or errors. A purchased phone number is a prerequisite for initiating outbound calls; an empty phone number inventory will prevent outbound calls from being made. |
| `retellai_create_a_new_outbound_phone_call` | Initiate an outbound call by POST to '/v2/create-phone-call'. Requires 'from_number' and 'to_number' in E.164 format. Optional overrides and metadata supported. On success, returns call details including type, status, and IDs. |
| `retellai_create_a_new_web_call` | The /v2/create-web-call endpoint creates a web call with a unique agent ID, returning call details like type, token, call ID, and status in JSON format, with a 201 response. Optional metadata and variables can be included. |
| `retellai_create_agent` | Create a new voice AI agent with specified configuration. Use when you need to set up a voice-based AI agent with custom response engine, voice settings, and behavior configuration. |
| `retellai_create_batch_test` | Tool to create a batch test job that runs multiple test cases against an agent. Use when you need to evaluate agent performance across multiple test scenarios simultaneously. |
| `retellai_create_chat` | Tool to create a new chat session with a chat agent. Use when you need to initiate a new chat conversation with a RetellAI chat agent. |
| `retellai_create_chat_agent` | Create a new chat agent with specified configuration. Use when you need to set up a chat-based AI agent with custom response engine and behavior settings. |
| `retellai_create_chat_completion` | Tool to create a chat completion for an existing chat session, generating the agent's response to a user message. Use when you need the agent to respond to user input in an ongoing chat conversation. |
| `retellai_create_conversation_flow` | Create a new Conversation Flow that can be attached to an agent for response generation. Requires start_speaker, model_choice, and nodes. Returns conversation_flow_id and full configuration. |
| `retellai_create_conversation_flow_component` | Creates a new shared conversation flow component at POST '/create-conversation-flow-component'. Requires 'name' and 'nodes' array. Optional: tools, mcps, start_node_id, begin_tag_display_position. Returns component ID, timestamp, and the full component definition. |

## Notes

- **No API key for Retell AI itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect retellai`.
- The action list above is a snapshot; `npx @useclawlink/cli actions retellai` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
