---
name: gpt-usage
description: 顯示 ChatGPT/Codex (openai-codex) 訂閱的用量與剩餘額度——短窗(5小時)與長窗(週)的 used_percent、視窗長度、重置時間，以及額外 credits。直接讀 pi 在 ~/.pi/agent/auth.json 的 OAuth token 去打 Codex endpoint、抓 X-Codex-* rate-limit headers（拿到 header 就中止請求，幾乎不花額度；額度爆掉時的 429 完全不花）。當使用者問 GPT/Codex/OpenAI 用量、額度、剩多少、rate limit、「還有多少額度」、「額度差多少」、「GPT usage」、或 pi 用 gpt-5.x 拿到 empty response（很可能就是額度爆了）時使用。
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [gpt, codex, usage, quota, rate-limits, openai, chatgpt-subscription]
---

# GPT Usage / Codex Quota Checker

Use when the user asks about ChatGPT/Codex/OpenAI subscription usage, quota, remaining
credits, rate limits（「剩餘使用量」「還有多少額度」「GPT usage」），**or** when pi returns an
empty response from a `gpt-5.x` (`openai-codex`) model — that is almost always the Codex
backend returning HTTP 429 `usage_limit_reached`, which pi swallows as blank.

## How it works

The ChatGPT-subscription Codex endpoint returns rate-limit state in response headers on
every call. This skill:

1. Reads the `openai-codex` OAuth token pi stored in `~/.pi/agent/auth.json`
   (auto-refreshes it via the OAuth token endpoint if it's expired).
2. Sends one minimal request to `https://chatgpt.com/backend-api/codex/responses` and
   **aborts as soon as the response headers arrive** — so it spends ~no quota (and when
   you're already rate-limited, the 429 returns the headers at zero cost).
3. Parses the `X-Codex-*` headers and prints used/remaining %, window length, reset time
   (Taiwan time, UTC+8), and any extra credits.

No dependency on the standalone `codex` CLI or `~/.codex/sessions` logs.

## Run it

```bash
/home/chihmin/.hermes/skills/gpt-usage/bin/gpt-usage.sh          # pretty Chinese output
/home/chihmin/.hermes/skills/gpt-usage/bin/gpt-usage.sh --json   # machine-readable JSON
# or call node directly:
node /home/chihmin/.hermes/skills/gpt-usage/bin/gpt-usage.mjs [--json] [--model gpt-5.5]
```

## The X-Codex-* headers it reads

- `x-codex-plan-type` (plus / pro …), `x-codex-active-limit`
- `x-codex-primary-used-percent`, `x-codex-primary-window-minutes` (300 = 5-hour rolling), `x-codex-primary-reset-at` / `-reset-after-seconds`
- `x-codex-secondary-used-percent`, `x-codex-secondary-window-minutes` (10080 = weekly), `x-codex-secondary-reset-at` / `-reset-after-seconds`
- `x-codex-credits-balance` / `-has-credits` / `-unlimited`

Remaining = `100 - used_percent` for each window. The **primary (5-hour)** window is the one
that usually trips first.

## Response style

Reply concisely in Traditional Chinese: 方案、短窗(已用/剩餘 % + 重置台灣時間)、長窗(同)、credits。
If the primary window is at 100%, tell the user roughly when it resets and suggest using a
lighter model (gpt-5.4-mini) or the local qwen in the meantime.

## Gotchas

- Requires pi to be logged into ChatGPT (`pi` → `/login` → ChatGPT Plus/Pro (Codex)); if
  `auth.json` has no `openai-codex` entry the skill exits with that hint.
- A 400 `model is not supported` / `Unsupported parameter` means the request didn't reach the
  rate-limit check — the script uses a body shape that does (no `max_output_tokens`).
- The token auto-refresh rewrites `~/.pi/agent/auth.json`; harmless, pi reads it fresh.
- The whole point: heavy gpt-5.x use burns the subscription's 5-hour window fast (each pi call
  also ships a big system prompt) — see the pi/piscord setup notes.
