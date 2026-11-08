---
name: tinypng
description: TinyPNG integration for AI agents via ClawLink — browser login, no API key setup. Connect tinypng through ClawLink's hosted setup. Use this skill when the user wants to work with TinyPNG (Developer Tools) — connect TinyPNG, read or update TinyPNG data, or take actions in TinyPNG from chat instead of saying you cannot access it.
---

# TinyPNG

Use **TinyPNG** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect TinyPNG once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect tinypng   # opens browser → authorize TinyPNG
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using TinyPNG

```bash
npx @useclawlink/cli actions tinypng "<what you want to do>"   # find an action
npx @useclawlink/cli describe tinypng <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run tinypng <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `tinypng_get_compression_count` | Tool to retrieve the number of compressions made this month. Use when you need to monitor your TinyPNG API usage. |
| `tinypng_shrink_and_get_image_id` | Tool to shrink an image and return its TinyPNG image ID. Use when you need only the compressed image identifier from the API response Location header. |
| `tinypng_tinify_compress_and_store_in_azure` | Compress an image using the Tinify API and upload the optimized result directly to Azure Blob Storage in a single operation. The image is first compressed by Tinify, then uploaded to the specified Azure Blob URL using the provided SAS token. Use this when you need to optimize images and store them in Azure without intermediate steps. Supports JPEG, PNG, and WebP image formats. |
| `tinypng_tinify_output` | Tool to retrieve a compressed image by its image ID. Use after compressing an image to download the result. |
| `tinypng_transform_image` | Tool to transform a compressed image by resizing, converting format, preserving metadata, or storing to cloud storage. Use when you have an image ID from a previous compression and need to apply transformations. |

## Notes

- **No API key for TinyPNG itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect tinypng`.
- The action list above is a snapshot; `npx @useclawlink/cli actions tinypng` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
