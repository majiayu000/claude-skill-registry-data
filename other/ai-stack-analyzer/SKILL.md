---
name: ai-stack-analyzer
description: Diagnostic tool for analyzing the AI Agent Stack (Hermes, OpenClaw, LiteLLM, Honcho). Invoke this skill whenever there are routing issues, 403/429 errors, or bots not responding.
---

# AI Stack Analyzer (Hermes, OpenClaw, LiteLLM)

Use this skill whenever the user reports an issue with the AI stack (e.g., "Hermes is stuck", "OpenClaw isn't responding", "LiteLLM rate limits").

## 1. Check LiteLLM Proxy Status and Logs
First, verify if the AI traffic router (LiteLLM) is healthy and check for API errors (403, 429).
```bash
kubectl get pods -n ai -l app=litellm-proxy
kubectl logs -n ai deploy/litellm-proxy --tail 100
```
- Look for `403 Key limit exceeded` or `429 Too Many Requests`.
- Ensure models don't have the `:free` suffix if the OpenRouter provider is saturated.

## 2. Check Hermes Agent
Check if Hermes is processing messages or retrying due to timeouts.
```bash
kubectl get pods -n ai -l app=hermes-agent-mcp
kubectl logs -n ai deploy/hermes-agent-mcp -c hermes-agent --tail 100
```

## 3. Check OpenClaw Gateway
Check if OpenClaw is running and connected to its Telegram provider.
```bash
kubectl get pods -n openclaw -l app=openclaw
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway --tail 100
```
- Look for `[bridge] :18790 ready` to ensure the MCP deadlock bypass is active.
- Check for `[telegram] isolated polling ingress started`.
- **CRITICAL**: Verify that OpenClaw and Hermes are **NOT** using the same Telegram Bot token. If both are polling the same token, one will silently drop messages or throw 409 conflicts.

## 4. Check Honcho (Memory)
If memory operations fail, check the Honcho persistence layer.
```bash
kubectl get pods -n honcho
kubectl logs -n honcho deploy/honcho-api --tail 50
```

## Troubleshooting Cheatsheet
- **Hermes/OpenClaw stuck with no logs**: Check LiteLLM for 429 errors.
- **LiteLLM 403 errors**: The API key in `secrets.yml` ran out of funds.
- **OpenClaw not answering but Hermes does**: They are likely sharing the same Telegram Bot token. Create a new bot in BotFather for OpenClaw.
- **OpenClaw MCP Bridge stuck**: Apply the `paired.json` bypass script documented in `AGENTS.md`.
