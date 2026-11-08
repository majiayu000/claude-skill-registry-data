---
name: openai
description: OpenAI integration for AI agents via ClawLink — browser login, no API key setup. Connect openai through ClawLink's hosted setup. Use this skill when the user wants to work with OpenAI (AI & ML) — connect OpenAI, read or update OpenAI data, or take actions in OpenAI from chat instead of saying you cannot access it.
---

# OpenAI

Use **OpenAI** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect OpenAI once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect openai   # opens browser → authorize OpenAI
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using OpenAI

```bash
npx @useclawlink/cli actions openai "<what you want to do>"   # find an action
npx @useclawlink/cli describe openai <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run openai <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `openai_add_upload_part` | Tool to add a part (chunk of bytes) to an Upload object. Use when uploading large files in chunks, with each part up to 64 MB. |
| `openai_cancel_batch` | Tool to cancel an in-progress batch. Use when you need to stop a batch that is currently processing. The batch will be in status 'cancelling' for up to 10 minutes before changing to 'cancelled', where partial results (if any) will be available. |
| `openai_cancel_eval_run` | Tool to cancel an ongoing evaluation run. Use when you need to stop an evaluation run that is currently in progress. |
| `openai_cancel_response` | Tool to cancel a background model response by its ID. Use when you need to stop a response that was created with the 'background' parameter set to true. Only background responses can be cancelled; attempting to cancel a non-background response will fail. |
| `openai_cancel_run` | Tool to cancel a run that is currently in progress. Use when you need to stop an assistant run that is taking too long or is no longer needed. The run's status will transition to 'cancelling' and then 'cancelled'. |
| `openai_cancel_upload` | Tool to cancel an upload. Use when you need to stop an upload that is in progress. No parts may be added after cancellation. |
| `openai_compact_response` | Tool to compact a conversation or response to reduce token usage. Use when you need to reduce the size of long conversations while preserving important context. Either provide an array of input messages or reference a previous response ID to compact. |
| `openai_create_audio_transcription` | Tool to transcribe audio files to text via OpenAI Audio Transcriptions API. Use when you need to convert speech in audio files to written text, optionally with timestamps or speaker diarization. |
| `openai_create_audio_translation` | Tool to translate audio files to English text via OpenAI Audio Translations API. Use when you need to convert speech in audio files (any language) to English text. |
| `openai_create_batch` | Tool to create and execute a batch from an uploaded file of requests. Use after uploading a JSONL file with purpose 'batch' to process multiple API requests in a single batch operation. |
| `openai_create_chat_completion` | Tool to create a chat completion response from OpenAI models. Use for conversational AI, text generation, function calling, multimodal tasks with vision/audio, and structured JSON outputs. Supports advanced features like reasoning models, tool use, and streaming responses. |
| `openai_create_completion` | Tool to generate text completions using OpenAI's legacy Completions API. Use for single-turn text generation with models like gpt-3.5-turbo-instruct. Note: This endpoint is legacy; prefer Chat Completions for newer models. |

## Notes

- **No API key for OpenAI itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect openai`.
- The action list above is a snapshot; `npx @useclawlink/cli actions openai` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
