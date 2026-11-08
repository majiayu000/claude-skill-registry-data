---
name: postiz
description: Postiz integration for AI agents via ClawLink — browser login, no API key setup. Connect Postiz through ClawLink's hosted setup to list social channels, get posting schemas, schedule and publish posts, and generate images or videos for your posts. Use this skill when the user wants to work with Postiz (Social Media) — connect Postiz, read or update Postiz data, or take actions in Postiz from chat instead of saying you cannot access it.
---

# Postiz

Use **Postiz** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Postiz once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect postiz   # opens browser → authorize Postiz
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Postiz

```bash
npx @useclawlink/cli actions postiz "<what you want to do>"   # find an action
npx @useclawlink/cli describe postiz <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run postiz <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `postiz_mcp_integrationlist` | List connected social media integrations in Postiz |
| `postiz_mcp_integrationschema` | Get the posting schema for a social media platform |
| `postiz_mcp_integrationscheduleposttool` | Schedule or publish a post to a social media platform |
| `postiz_mcp_ask_postiz` | Ask the Postiz agent a question about managing or scheduling posts |
| `postiz_mcp_generateimagetool` | Generate an image to use in a social media post |
| `postiz_mcp_generatevideotool` | Generate a video to use in a social media post |
| `postiz_mcp_generatevideooptions` | Get available options for video generation |
| `postiz_mcp_triggertool` | Fetch additional details needed for scheduling posts |
| `postiz_mcp_videofunctiontool` | Get extra video generation info like available voice IDs |

## Notes

- **No API key for Postiz itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect postiz`.
- The action list above is a snapshot; `npx @useclawlink/cli actions postiz` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
