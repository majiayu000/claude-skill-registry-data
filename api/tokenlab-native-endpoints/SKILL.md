---
name: tokenlab-native-endpoints
description: Use TokenLab native endpoint families such as Responses, Anthropic Messages, Gemini generateContent, System One decisions, media, audio, embeddings, and translations when OpenAI-compatible chat is not the right contract.
license: MIT
metadata:
  category: coding
---

# TokenLab Native Endpoints

Use this skill when a user needs provider-native behavior, non-chat APIs, or migration guidance beyond OpenAI-compatible `/v1/chat/completions`.

## What this skill should deliver

- A clear endpoint choice and why it fits the request.
- A minimal request example with the correct base URL and auth header.
- A note on when OpenAI-compatible chat remains the simpler path.
- A fail-closed contract check for non-chat or provider-native request shapes.
- A recovery path when TokenLab returns a native endpoint hint or contract error.

## Endpoint families

- OpenAI-compatible chat: `POST https://api.tokenlab.sh/v1/chat/completions`
- OpenAI Responses: `POST https://api.tokenlab.sh/v1/responses`
- Anthropic Messages: `POST https://api.tokenlab.sh/v1/messages`
- Gemini native generate content: `POST https://api.tokenlab.sh/v1beta/models/{model}:generateContent`
- System One decisions: `POST https://api.tokenlab.sh/v1/systemone` (synchronous `state` + `questions`)
- Model catalog: `GET https://api.tokenlab.sh/v1/models`
- Task-specific model shortlist: `GET https://api.tokenlab.sh/v1/models?recommended_for=<scene>`
- Model contract: `GET https://api.tokenlab.sh/v1/models/:model`

## Preferred approach

1. Start with OpenAI-compatible chat unless the user needs a native contract, non-chat API, or provider-specific behavior.
2. If a previous response includes `X-TokenLab-Hint` or `X-TokenLab-Native-Endpoint`, treat it as routing evidence and prefer the exact native route in the header.
3. For Anthropic-style requests, use `/v1/messages` and preserve Anthropic request semantics instead of converting blindly.
4. For Gemini-style requests, preserve Gemini content parts, roles, tools, and generation config when the user explicitly needs Gemini-native behavior.
5. For decision/media/audio/embedding/rerank/translation requests, inspect `GET /v1/models/:model` before changing request parameters.

## Output format

- One sentence naming the chosen endpoint.
- One runnable code block or cURL block.
- One short explanation of why this endpoint fits.
- One recovery note naming the catalog or contract endpoint to check if the call fails.

## Avoid

- Do not flatten native Anthropic or Gemini request semantics into generic OpenAI chat unless the user explicitly accepts that tradeoff.
- Do not remove unsupported fields just to make validation pass when doing so would change output, safety, billing, or response guarantees.
- Do not hardcode media request shapes without inspecting the model contract.
- Do not expose private TokenLab routing, channel, or physical provider internals.

## Edge Cases

- If the model supports both OpenAI-compatible and native routes, pick the simpler path unless the user needs native behavior.
- If the endpoint hint conflicts with the user's explicit requirement, explain the tradeoff and ask for confirmation before changing semantics.
- If a request fails with a contract error, use supported operations and recommended request fields to repair it.

## Decision models

Discover `category=decision` and verify the exact model contract. System One uses `model`, `state`, and named `questions` with `noul`, `choice`, or `score` types. It returns typed answers, not generated chat text. Keep probabilities, optional confidence, and usage intact. Use the native HTTP endpoint or the published MCP `evaluate_decisions` tool. Do not bind a decision model as a chat-provider model, add streaming or Batch fields, or treat a decision as permission to execute an action.
