---
name: figma
description: Figma integration for AI agents via ClawLink — browser login, no API key setup. Connect Figma through ClawLink's hosted setup to read files, manage comments, extract design tokens, download images, and create webhooks from your Figma account. Use this skill when the user wants to work with Figma (Design) — connect Figma, read or update Figma data, or take actions in Figma from chat instead of saying you cannot access it.
---

# Figma

Use **Figma** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Figma once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect figma   # opens browser → authorize Figma
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Figma

```bash
npx @useclawlink/cli actions figma "<what you want to do>"   # find an action
npx @useclawlink/cli describe figma <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run figma <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `figma_download_figma_images` | Download images from Figma file nodes |
| `figma_extract_design_tokens` | Extract design tokens from Figma files |
| `figma_add_a_comment_to_a_file` | Post a comment to a Figma file or branch |
| `figma_create_a_webhook` | Create a Figma webhook |
| `figma_create_dev_resources` | Attach development resources to Figma nodes |
| `figma_design_tokens_to_tailwind` | Convert design tokens to Tailwind CSS config |

## Notes

- **No API key for Figma itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect figma`.
- The action list above is a snapshot; `npx @useclawlink/cli actions figma` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
