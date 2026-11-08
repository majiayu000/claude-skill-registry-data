---
name: lmnt
description: LMNT integration for AI agents via ClawLink — browser login, no API key setup. Connect lmnt through ClawLink's hosted setup. Use this skill when the user wants to work with LMNT (AI & ML) — connect LMNT, read or update LMNT data, or take actions in LMNT from chat instead of saying you cannot access it.
---

# LMNT

Use **LMNT** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect LMNT once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect lmnt   # opens browser → authorize LMNT
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using LMNT

```bash
npx @useclawlink/cli actions lmnt "<what you want to do>"   # find an action
npx @useclawlink/cli describe lmnt <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run lmnt <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `lmnt_create_voice` | Creates a custom voice in LMNT by training on uploaded audio samples. The voice can then be used for text-to-speech synthesis. Returns the voice ID and metadata upon successful creation. The voice may be in 'training' state initially before becoming 'ready'. |
| `lmnt_delete_voice_info` | Deletes a voice from your LMNT account. This operation permanently removes the voice and cancels any pending operations on it. This action cannot be undone. Only voices owned by you (owner='me') can be deleted; system voices cannot be deleted. Use case: Remove custom voices that are no longer needed to manage your voice library. |
| `lmnt_generate_speech_with_metadata` | Generates speech from text and returns JSON with base64-encoded audio and optional word-level timing metadata. Use when you need the synthesis seed or word timestamps for subtitle synchronization. For lower latency without metadata, use the Synthesize Speech action instead. |
| `lmnt_get_account` | Retrieves account information including subscription plan details and current usage statistics. |
| `lmnt_get_voice_info` | Gets metadata for a specific LMNT voice, including active status, supported languages, and plan availability. Useful for validating a voice ID before using it in synthesis requests. |
| `lmnt_get_voices_list` | Retrieves a list of available voices from LMNT. Returns both system-provided preset voices and any custom voices you have created. Use filters to narrow results by ownership (system vs custom) or starred status. Each voice includes details like ID, name, description, gender, state, and preview URL. |
| `lmnt_synthesize_speech` | Synthesizes speech from text using LMNT's AI voices. Converts text (up to 5000 characters) into natural-sounding speech audio using a specified voice. Returns base64-encoded audio at `data.response_data.audio` — decode before saving or passing to other tools. Supports multiple audio formats and quality settings for different use cases. |
| `lmnt_update_voice` | Updates information about a specific voice in LMNT. You can update the name, description, gender, starred status, and unfreeze state of a voice. Note: Only user-owned voices (owner='me') can have their name, description, and gender updated. System voices can only be starred/unstarred. |

## Notes

- **No API key for LMNT itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect lmnt`.
- The action list above is a snapshot; `npx @useclawlink/cli actions lmnt` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
