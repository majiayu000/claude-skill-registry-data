---
name: "openclaw"
description: "OpenClaw Personal AI Gateway: Telegram bot, Modular RBAC, LiteLLM proxy integration, and webhook management"
---

# OpenClaw — Personal AI Gateway

OpenClaw is a personal AI assistant and gateway that integrates directly into the Kubernetes cluster. It listens for commands via Telegram and executes tasks locally in the homelab environment.

## Overview
- **Deployment**: `ghcr.io/openclaw/openclaw` (Multi-arch/ARM64)
- **Namespace**: `openclaw`
- **Domain**: `openclaw.cluster.home`
- **Configuration**: Managed entirely via Ansible (`roles/install-openclaw`)

## Integrations

### 1. Webhooks & CI/CD Automation
OpenClaw can function as an autonomous agent processing webhooks.
- **Endpoint**: `https://openclaw.cluster.home/hooks/agent` (for complex analysis) o `/hooks/wake` (for simple ping).
- **GitHub Actions Integration (Smee.io)**: Dado que `openclaw.cluster.home` es un DNS privado, OpenClaw utiliza un Webhook Relay a través de Smee.io (`https://smee.io/NibMMS9tqGdtxzN1`).
  - Un pod `smee-client` corre junto a OpenClaw, intercepta las peticiones enviadas a Smee desde GitHub Actions y las reenvía a `http://openclaw:18789/hooks/wake`.
  - **Requisito en GitHub**: El repositorio debe tener el secret `OPENCLAW_GATEWAY_TOKEN` configurado para autenticar las peticiones.
- **Allowed Ingress**: Traffic is permitted from `gateway` (for external sources) and internal namespaces like `argocd`, `monitoring` (AlertManager), and `kaniko`.
- **Behavior**:
  - Automatically parses payloads (e.g. `alertname`, `status`, `repo`).
  - If a job/workflow is successful (`severity=info`, `sync-success`), it notifies Telegram directly without polling Kubernetes.
  - If a job fails, it leverages the `kubernetes-mcp` sidecar to fetch logs/events for context before alerting.

### 2. Honcho Memory (Dialectic Reasoning)
OpenClaw uses **Honcho** to provide persistent, AI-native memory across sessions.
- **Provider**: `@honcho-ai/openclaw-honcho` plugin (auto-installed on pod startup via `init-plugins`).
- **Configuration**: 
  - `HONCHO_WORKSPACE=openclaw`
  - `HONCHO_API_KEY` (secret)
- **How it works**: The "Dreaming Agent" continuously infers facts and user preferences asynchronously in the background. OpenClaw injects this derived context into the prompt, giving it a persistent personality and deep context about the user's homelab.

### 3. LiteLLM Proxy
All model requests flow through the in-cluster LiteLLM Proxy (`http://litellm-proxy.ai.svc.cluster.local:4000`), ensuring usage is tracked in Prometheus.
- **Primary Model**: `litellm/gpt-4o` (which LiteLLM routes according to its own fallback chains, typically `openai/gpt-oss-120b:free` via OpenRouter).

### 4. Kubernetes MCP Sidecar
OpenClaw includes a `kubernetes-mcp-server` sidecar container running on `localhost:8080`.
- Used for fast, read-only inspection of the cluster (listing pods, checking node resources, reading logs).
- Controlled by `openclaw_rbac_level` (default: `readonly`, can be escalated to `operator` or `cluster-admin`).

## Debugging

**View gateway logs:**
```bash
kubectl logs -n openclaw deploy/openclaw -c openclaw-gateway -f
```

**Check Honcho plugin installation:**
```bash
kubectl logs -n openclaw deploy/openclaw -c init-plugins
```

**Trigger a test webhook:**
```bash
curl -X POST https://openclaw.cluster.home/hooks/wake \
  -H "Authorization: Bearer <OPENCLAW_GATEWAY_TOKEN>" \
  -d '{"event": "test_ping", "status": "success"}'
```

## Troubleshooting & Bootstrap Deadlock Bypass

### The MCP Bridge Deadlock
In OpenClaw versions v2026.x+, the `openclaw-mcp-bridge` sidecar container requires a scope upgrade (`operator.read, operator.write, operator.approvals, operator.pairing`) to register and route A2A bridge tools. 

Because the gateway suspends unauthorized scope upgrades, the bridge client connection gets blocked in a pending state (`scope upgrade pending approval`). However, trying to run the approval CLI command (`openclaw devices approve`) inside the gateway container itself initiates a WebSocket connection that triggers a nested scope upgrade, leading to a **chicken-and-egg bootstrap deadlock**.

### Direct PVC Approval Bypass
To resolve this deadlock and authorize the bridge:
1. Run a Node.js one-liner directly inside the gateway container to edit the device list on the PVC and pre-approve all required scopes:
   ```bash
   kubectl exec -n openclaw deployment/openclaw -c openclaw-gateway -- node -e '
   const fs = require("fs");
   const file = "/home/node/.openclaw/devices/paired.json";
   const data = JSON.parse(fs.readFileSync(file, "utf8"));
   const key = "c7eb17c905d9c3b9fad7d2623ce4f58ab3fe7499a1a2b13a7efb81ae679b8fb8";
   if (data[key]) {
     const targetScopes = ["operator.read", "operator.write", "operator.approvals", "operator.pairing"];
     data[key].scopes = targetScopes;
     data[key].approvedScopes = targetScopes;
     if (data[key].tokens && data[key].tokens.operator) {
       data[key].tokens.operator.scopes = targetScopes;
     }
     fs.writeFileSync(file, JSON.stringify(data, null, 2), "utf8");
     console.log("SUCCESS: paired.json successfully updated.");
   }
   '
   ```
2. Remove any stale queue requests:
   ```bash
   kubectl exec -n openclaw deployment/openclaw -c openclaw-gateway -- rm -f /home/node/.openclaw/devices/pending.json
   ```
3. Restart the OpenClaw deployment to force the gateway to reload `paired.json` and let the bridge connect:
   ```bash
   kubectl rollout restart -n openclaw deployment/openclaw
   ```

*Note: Since supergateway only supports one active client session per stdio process, do not run concurrent manual curls to `supergateway` port 18790, as it will crash the container.*

## Security Best Practices
> [!IMPORTANT]
> **NPM and CVE Prevention**: Whenever installing packages with `npm` or running tools via `npx` inside initContainers, GitHub Actions, or local scripts, always ensure you are using the latest stable packages (e.g. `npx @latest` or specifying exact pinned versions known to be secure). Periodically run `npm audit` on Node.js projects to prevent vulnerabilities and CVEs from being introduced into the cluster.

