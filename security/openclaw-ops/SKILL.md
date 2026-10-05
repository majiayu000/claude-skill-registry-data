---
name: openclaw-ops
description: >
  OpenClaw and NemoClaw operations — sandbox management, inference provider config,
  policy configuration, Tailscale integration, security hardening, skill vetting.
  Trigger on: "OpenClaw", "NemoClaw", "OpenShell", "sandbox", "openclaw tui",
  "agent assistant", "ClawHub", "gateway token", or any task involving
  personal AI assistant deployment and operations.
---

# OpenClaw/NemoClaw Operations

## Deployment on Primary Host

| Component | Status | Port | Access |
|---|---|---|---|
| OpenClaw | v2026.3.13 | <service-port> (loopback) | Tailscale Serve → HTTPS |
| NemoClaw | v0.1.0 (alpha) | <gateway-port> (OpenShell gateway) | Internal |
| Sandbox | `my-assistant` | — | `nemoclaw my-assistant connect` |
| Tailscale | Connected | <tailscale-ip> | `https://<primary-host>.tail<tailnet>.ts.net/` |

## Security Posture

- All messaging channels **disabled** (WhatsApp, Telegram, Discord, Slack, Signal, Matrix, IRC)
- DM policy: **disabled** on all channels
- Gateway auth: **token-based**
- Gateway bind: **loopback only** (127.0.0.1:<service-port>)
- UFW: gateway port **denied** from LAN, **allowed** via Tailscale interface
- NemoClaw sandbox: OpenShell with Landlock + seccomp + network namespace isolation
- Inference binding and service ports configured for internal access only

## Interaction

**Recommended: CLI/TUI via Tailscale SSH (most secure)**
```bash
# From any device on your tailnet
ssh admin_user@<primary-host>    # via Tailscale
openclaw tui         # interactive chat

# Or inside the sandbox
nemoclaw my-assistant connect
openclaw tui
```

**Web dashboard:** `https://<primary-host>.tail<tailnet>.ts.net/` (tailnet only)

## Inference

**Primary:** Local Ollama on GPU host (<gpu-host-ip>:<ollama-port>)
- Available models: qwen3:8b/14b, llama3.3:70b, deepseek-r1:70b, mistral-nemo:12b, gemma2:9b
- Requires GPU host to be online

**Fallback:** Anthropic Claude API (if configured)
- Known Ollama bugs: cold-start timeouts (#43946), API key after reconfig (#28927)

## Key Commands

```bash
# Gateway
openclaw gateway status
openclaw gateway restart
systemctl --user status openclaw-gateway

# Sandbox
nemoclaw list
nemoclaw my-assistant status
nemoclaw my-assistant connect
nemoclaw my-assistant logs --follow
nemoclaw my-assistant destroy         # nuclear option

# Config
openclaw config set <key> <value>
openclaw doctor                       # health check
openclaw security audit --deep        # policy drift check

# Tailscale
sudo tailscale serve status
sudo tailscale serve --bg 18789       # re-enable serve
sudo tailscale serve --https=443 off  # disable serve
```

## Security Warnings

1. **CVE-2026-25253** (CVSS 8.8) — patched in >= 2026.1.29. We run 2026.3.13.
2. **29 pages of GitHub Security Advisories** — large attack surface from messaging integrations (all disabled).
3. **ClawHub skills** — no mandatory vetting. Treat all as untrusted. Audit before installing.
4. **NemoClaw is alpha** — expect instability. The sandbox is the security-critical layer.
5. **API keys** — never paste in chat. Use env vars or config files with 600 permissions.

## Rules

- Never enable messaging channels without explicit approval
- Never install ClawHub skills without security review
- Never expose OpenClaw ports to LAN (Tailscale only)
- Always verify sandbox is active before trusting isolation
- Rotate gateway token if compromised
- Keep OpenClaw updated (check: `openclaw --version`)
