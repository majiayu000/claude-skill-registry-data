---
name: omniroute-free-llm-routing
description: Configure and troubleshoot OmniRoute, Ollama, free-tier hosted LLMs, model fallback and token-conscious routing for Claude Code and OpenAI Codex CLI. Use when users request free/local models, provider routing, quota-aware fallback, or one gateway for coding agents.
---

# OmniRoute, Ollama and Free LLM Routing

## Goal

Use a user-controlled local gateway to route compatible coding clients to local Ollama models and eligible hosted providers. Prefer local inference when privacy or recurring cost matters; use hosted free tiers only within provider terms.

## Before changing configuration

1. Inspect the installed OmniRoute version and its official documentation: https://github.com/akoeraste/omniroute
2. Check `omniroute doctor`, the local dashboard, and `omniroute models list` where supported by the installed version.
3. Preserve existing Claude Code, Codex, MCP and provider configuration. Back up files before any change.
4. Never print, commit, log or place API keys in shell history. Use the gateway's credential UI or documented secret environment variables.
5. Never assume a free provider is available in the user's region or account.

## Recommended setup

```bash
npm install -g omniroute
omniroute
```

Open `http://localhost:20128`, connect providers through the gateway's Providers UI, and copy the gateway API key from Dashboard → Endpoints. Verify the API with the gateway's documented `/v1/models` endpoint before configuring clients.

For Claude Code and Codex CLI, prefer OmniRoute's own CLI integration so it can set the correct environment and model mapping:

```bash
omniroute run claude --model auto/coding
omniroute run codex --model auto/coding
omniroute configure claude
omniroute configure codex
```

Confirm the exact supported commands with `omniroute --help` for the installed version. Do not assume every provider/model supports every coding-agent feature such as tool calling, long context, vision or structured output.

## Ollama local models

1. Install Ollama from https://ollama.com and start the local service.
2. Pull a model compatible with the machine's RAM/VRAM, e.g. `ollama pull qwen2.5-coder:7b` (model availability and tags can change).
3. Add the local Ollama provider in OmniRoute's provider settings and confirm it appears in the model list.
4. Test a short request before selecting it for a large coding task.

Local inference has no hosted provider token quota, but is bounded by hardware, speed, power and model license. Local use is not literally unlimited compute.

## Free hosted providers

Examples to check in OmniRoute's current provider catalog:
- Google Gemini API free tier
- Groq developer free tier
- Cerebras developer tier
- Cloudflare Workers AI free allocation
- NVIDIA NIM developer access
- Hugging Face Inference free allowances
- OpenRouter models marked `:free`

Availability, limits, model names, rate limits, regions and terms change. Use the current dashboard/catalog and each provider's official terms instead of hard-coded quota claims. Some free tiers require API keys, phone verification, payment details, or regional eligibility.

## Routing policy

- Use a local Ollama model for low-risk, private, repetitive tasks.
- Use a hosted free-tier model for tasks it can handle, while respecting limits.
- Prefer a stronger configured model for difficult debugging, security-sensitive review or final verification.
- Use fallback only across providers the user has explicitly connected and is allowed to use.
- Avoid repeated retries after quota/authentication failures; respect Retry-After and provider cooldowns.
- Never rotate accounts, forge identities, bypass rate limits, scrape credentials, or evade usage restrictions.
- Never claim a task is complete based solely on model output; run tests and inspect results.

## Token and context optimization

- Load the smallest relevant skill and project context.
- Summarize repository state once, then update the summary when facts change.
- Keep system instructions concise and reuse stable prefixes where provider prompt caching is supported.
- Avoid sending secrets, binaries, generated bundles or irrelevant repository files.
- Compression can reduce input tokens but may remove important details; preserve code, commands, paths, URLs, JSON and exact error messages.
- Do not promise a fixed savings percentage or zero tokens. Measure usage using the provider/gateway usage view.

## Claude.ai and ChatGPT web

The browser-based Claude.ai and ChatGPT interfaces do not automatically route their own model inference through a local OmniRoute gateway. Reuse this skill as project instructions, or use a supported API client, custom action/connector or coding CLI. Do not tell users that adding a repository skill changes the provider's hosted chat backend.

## Troubleshooting

- Gateway unavailable: verify process, port 20128, local firewall and dashboard.
- Empty model list: connect a provider and check its credentials, region and eligibility.
- Model rejected: refresh the provider catalog and select a model actually listed by the gateway.
- Quota errors: honor cooldowns, switch only to another configured eligible provider, or use Ollama.
- Tool calls fail: select a model/provider with tool-calling support and test a minimal tool call.
- Claude/Codex config conflicts: stop, back up the current config and use OmniRoute's guided configure/run command rather than hand-editing blindly.
