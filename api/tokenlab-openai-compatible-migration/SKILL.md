---
name: tokenlab-openai-compatible-migration
description: Migrate OpenAI-compatible apps, SDKs, examples, and environment variables to TokenLab while preserving request semantics and adding live model discovery.
license: MIT
metadata:
  category: coding
---

# TokenLab OpenAI-Compatible Migration

Use this skill when a user wants to move an existing OpenAI-compatible integration, OpenRouter setup, LiteLLM config, LangChain/LlamaIndex app, or custom SDK wrapper to TokenLab.

## What this skill should deliver

- A minimal diff or config change that preserves the existing user path.
- The correct TokenLab base URL and API key environment variable.
- A model migration note with live discovery commands.
- A native endpoint note when the old code actually needs Responses, Anthropic Messages, Gemini, media, audio, embeddings, rerank, or translation behavior.
- A rollback note that restores the previous provider config.

## Default migration rules

- OpenAI-compatible SDKs:
  - base URL: `https://api.tokenlab.sh/v1`
  - auth: `Authorization: Bearer $TOKENLAB_API_KEY`
  - chat path: `/v1/chat/completions`
- Anthropic-native clients:
  - base URL: `https://api.tokenlab.sh`
  - messages path: `/v1/messages`
- Gemini-native clients:
  - base URL: `https://api.tokenlab.sh`
  - generateContent path: `/v1beta/models/{model}:generateContent`
- Live discovery:
  - `GET https://api.tokenlab.sh/v1/models`
  - `GET https://api.tokenlab.sh/v1/models?recommended_for=<scene>`
  - `GET https://api.tokenlab.sh/v1/models/:model`

## Preferred approach

1. Locate the current provider config, environment variables, and model IDs.
2. Make the smallest possible change first:
   - replace base URL
   - replace API key variable
   - keep SDK/client shape intact
3. Add model discovery only where the app currently hardcodes provider-specific models.
4. Keep native semantics when the source integration uses Responses, Anthropic Messages, Gemini content parts, tools, media, audio, embeddings, rerank, or translation.
5. Provide a smoke test command for the migrated path.

## Output format

- One short explanation of the migration surface.
- A focused diff, config block, or runnable replacement snippet.
- One smoke test command.
- One model discovery command.
- One rollback line naming the previous base URL/env vars.

## Avoid

- Do not rewrite the user's SDK architecture if a base URL change is enough.
- Do not flatten native Anthropic or Gemini payloads into generic chat unless the user explicitly accepts that behavior change.
- Do not silently change models when the user's existing model has no obvious TokenLab equivalent.
- Do not embed API keys in source files or prompts.
- Do not claim feature parity without checking the model details endpoint.

## Edge Cases

- If an app has separate base URLs for chat, embeddings, and media, migrate one family at a time.
- If the existing app uses OpenRouter model slugs, map to TokenLab public model IDs only after catalog lookup.
- If the user's previous provider had provider-specific headers, keep only headers that TokenLab documents or that the user's app still needs.
