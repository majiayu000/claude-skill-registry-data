---
name: canva
description: Canva integration for AI agents via ClawLink — browser login, no API key setup. Connect Canva through ClawLink's hosted setup to create designs, import assets, export content, manage comments, and resize designs. Use this skill when the user wants to work with Canva (Design) — connect Canva, read or update Canva data, or take actions in Canva from chat instead of saying you cannot access it.
---

# Canva

Use **Canva** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Canva once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect canva   # opens browser → authorize Canva
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Canva

```bash
npx @useclawlink/cli actions canva "<what you want to do>"   # find an action
npx @useclawlink/cli describe canva <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run canva <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `canva_create_asset_upload_job` | Upload an asset file to the Canva content library |
| `canva_create_url_asset_upload_job` | Import an asset into Canva from a public URL |
| `canva_fetch_asset_upload_job_status` | Poll for asset upload job completion status |
| `canva_create_design_import_job` | Import an external file as a new Canva design |
| `canva_create_design_resize_job` | Create a resized copy of an existing design |
| `canva_fetch_design_metadata_and_access_information` | Get metadata for a Canva design |
| `canva_get_design_export_job_result` | Poll for design export job completion status |
| `canva_get_designs_designid_export_formats` | List available export formats for a design |
| `canva_fetch_current_user_details` | Get the current Canva user details |

## Notes

- **No API key for Canva itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect canva`.
- The action list above is a snapshot; `npx @useclawlink/cli actions canva` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
