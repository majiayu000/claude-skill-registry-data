---
name: routerbase-api-integration
description: Use when integrating applications with an OpenAI-compatible model gateway, migrating SDK calls, or documenting safe API key handling for RouterBase.
---

# RouterBase API Integration

## Overview

Integrate applications with [routerbase](https://routerbase.com/) as an OpenAI-compatible model gateway. This skill covers SDK migration, base URL configuration, streaming, tool calling, JSON mode, vision inputs, request validation, error handling, and safe credential handling.

## When to Use

Use this skill when the user asks for:
- Migrating OpenAI-compatible SDK calls to RouterBase
- Setting `base_url` or `baseURL` to `https://routerbase.com/v1`
- Configuring RouterBase API keys without exposing secrets
- Implementing chat completions, streaming, tool calling, JSON mode, or vision inputs
- Writing concise RouterBase integration examples for Python, JavaScript, curl, LangChain, LlamaIndex, Vercel AI SDK, Cursor, Continue, or similar clients

## Do not use

Do not use this skill for:
- Publishing, logging, or storing real API keys
- Guessing provider-specific behavior that is not documented by the user or upstream docs
- Rewriting a working provider integration when the user only needs model selection guidance

## Instructions

1. Identify the user's current client, language, model ID, and deployment environment.
2. Keep the existing OpenAI-compatible SDK when possible; change only the base URL, model, and local secret configuration.
3. Use placeholders such as `<ROUTERBASE_API_KEY>` in examples.
4. Keep credentials server-side and out of git.
5. Prefer a small test request before suggesting broad application changes.
6. Include a verification checklist with expected status code, response shape, timeout handling, and redaction requirements.
