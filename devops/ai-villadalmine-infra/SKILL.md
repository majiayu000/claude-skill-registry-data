---
name: ai
description: >
  AI Agent stack: Hermes Agent (self-improving AI assistant), HolmesGPT (SRE),
  and OpenClaw (personal AI gateway) routed through in-cluster LiteLLM proxy.
  Holmes uses GPU-local Ollama primary with OpenRouter cloud fallbacks.
  OpenRouter fallback chains for all services (free→free2→cheap→paid).
  Built for ARM64 (Raspberry Pi CM4) using in-cluster kaniko build.
  Includes Docker registry:2 for storing custom ARM64 images.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, ai, hermes, openrouter, litellm, llm, kaniko, arm64, registry]
---

# AI Agent Skill

## Stack Overview

| Component | Image | Version | Namespace | Notes |
|-----------|-------|---------|-----------|-------|
| Docker registry | `registry:2` | 2 | registry | ARM64-compatible image storage (5Gi PVC) |
| LiteLLM proxy | `ghcr.io/berriai/litellm` | main-latest | ai | In-cluster OpenRouter router with fallbacks |
| Hermes Agent | `NousResearch/hermes-agent` | 0.7.0 | ai | Self-improving AI assistant |
| Kaniko | `gcr.io/kaniko-project/executor` | latest | kaniko | In-cluster ARM64 image builder |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Namespace: ai                          │
│                                                             │
│  ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │  Hermes Agent   │───▶│  LiteLLM Proxy               │   │
│  │  model=free     │    │  port 4000                   │   │
│  │  OPENAI_API_BASE│    │  fallback: free→free2→cheap  │   │
│  └─────────────────┘    └─────────────┬────────────────┘   │
│                                       │ HTTPS:443           │
│                                       ▼                     │
│                               OpenRouter API                │
│                               (external)                    │
│  PVC: hermes-data (/opt/data)                               │
│  Secret: litellm-secrets (OPENROUTER_API_KEY)               │
│  Secret: hermes-secrets (OPENROUTER_API_KEY + bot tokens)   │
└─────────────────────────────────────────────────────────────┘

Namespace: registry
  registry:2 pod ← kaniko pushes here ← Kaniko job (namespace: kaniko)
  registries.yaml on K3s nodes → mirror registry.registry:5000 → ClusterIP
```

---

## Why Custom Build?

Hermes Agent official Docker image (`nousresearch/hermes-agent`) is **amd64-only**.
For ARM64 clusters (Raspberry Pi CM4), we build in-cluster using kaniko.

**Build process:**
1. Kaniko job clones `https://github.com/NousResearch/hermes-agent`
2. Builds ARM64 image using custom Dockerfile (`--snapshot-mode=redo` for low memory)
3. Pushes to local registry: `registry.registry:5000/ai/hermes-agent:0.7.0`
4. Hermes deployment uses the local image

**Build time:** ~60 min on Raspberry Pi CM4 (heavy: debian + nodejs + pip deps + ffmpeg)

**Kaniko gotchas:**
- `--snapshot-mode=redo` — uses mtime for change detection (much less memory than default)
- Node affinity → control-plane node (more disk space than agent)
- `backoffLimit: 3` — OOM on agent node caused earlier failures
- Wait timeout: `3600s`

---

## LiteLLM Proxy — Model Routing

Services do NOT call OpenRouter directly. They call the in-cluster LiteLLM proxy:

```
OPENAI_API_BASE=http://litellm-proxy.ai.svc.cluster.local:4000
OPENAI_API_KEY=sk-hermes-internal  (LiteLLM master key)
HERMES_MODEL=hermes-qwen
```

LiteLLM config (`roles/install-litellm-proxy/tasks/main.yml`):

### Hermes routing

| Virtual model | Real model | Provider | Notes |
|--------------|-----------|---------|-------|
| `hermes-qwen` | `openrouter/qwen/qwen3-coder:free` | OpenRouter | Primary Hermes |
| `free` | `openrouter/qwen/qwen3-coder:free` | OpenRouter | Legacy alias |
| `free2` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Fallback tier 1 |
| `cheap` | `openrouter/qwen/qwen-turbo` | OpenRouter | Fallback tier 2 |
| `qwen-pro` | `openrouter/qwen/qwen3.6-plus` | OpenRouter | Paid last resort |

### Free Models & Aliases (Headlamp / Holmes)

| Virtual model | Real model | Provider | Notes |
|--------------|-----------|---------|-------|
| `nemotron` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Dedicated free Nemotron model |
| `qwen3.6-free` | `openrouter/qwen/qwen3-coder:free` | OpenRouter | Dedicated free Qwen3.6 coder model |
| `deepseek4v-free` | `openrouter/deepseek/deepseek-v4-flash:free` | OpenRouter | Dedicated free DeepSeek-v4 model |

### Holmes routing (GPU primary → cloud fallback)

| Virtual model | Real model | Provider | Notes |
|--------------|-----------|---------|-------|
| `holmes-llama` | `openai/llama3.1:8b` | GPU Ollama :11434 | Primary |
| `gpt-5.4` | `openai/llama3.1:8b` | GPU Ollama :11434 | Holmes default model name |
| `local-reason` | `openai/deepseek-r1:8b` | GPU Ollama :11434 | Headlamp AG-UI default |
| `holmes-free2` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Cloud fallback tier 1 |
| `holmes-cheap` | `openrouter/qwen/qwen-turbo` | OpenRouter | Cloud fallback tier 2 |

### OpenClaw routing

| Virtual model | Real model | Provider | Notes |
|--------------|-----------|---------|-------|
| `openclaw-gemini` | `openai/gpt-oss-120b:free` | OpenRouter | Primary |
| `gemini-free2` | `openai/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Fallback tier 1 |
| `openclaw-cheap` | `openai/qwen/qwen-turbo` | OpenRouter | Fallback tier 2 |
| `gpt-4o` / `openai/gpt-4o` | `openai/gpt-oss-120b:free` | OpenRouter | OpenClaw compatibility alias |

### Fallback chains

```
Hermes:   rk1-npu-local (NPU) → hermes-qwen → qwen-pro → free2 → cheap
Holmes:   rk1-npu-local (NPU) → holmes-llama (Ollama) → holmes-free2 (cloud) → holmes-cheap (cloud) → qwen-pro (paid)
OpenClaw: rk1-npu-local (NPU) → openclaw-gemini → gemini-free2 → openclaw-cheap → deepseek-pro → deepseek-free
Local GPU (all): rk1-npu-local (NPU) → GPU → free tier → cheap → qwen-pro (paid last resort)
```

> **Note on NPU Integration:** The NPU Pool (`rk1-npu-local`) is intended to be the default primary base for all consumers. Due to its context window limit (`max_input_tokens: 4096`), LiteLLM will automatically trigger a `context_window_fallback` to the cloud/GPU chains defined above if a prompt exceeds the limit. If an NPU model fails or is offline, it will similarly fall back to the "real" models.

### Modifying LiteLLM Configuration (Strict Rule)

**CRITICAL:** NEVER use `sed` or regex-based python script text replacement to inject aliases into `install-litellm-proxy/tasks/main.yml`. Because `model_list` is a YAML list, appending a model with a duplicate `model_name` elsewhere in the file creates a duplicated list item that can unintentionally hijack other model routes and break traffic. 

If you must update the LiteLLM config:
1. Manually edit `roles/install-litellm-proxy/tasks/main.yml` using precise replacement.
2. Ensure you modify the existing YAML block scalar directly.
3. Validate that you are not defining duplicate `- model_name: <alias>` items unintentionally.
4. Redeploy cleanly using `make ai-litellm-proxy-deploy` (or `ansible-playbook ... --tags ai-litellm-proxy`).

### Hermes MCP lessons learned

- Kubernetes MCP works reliably when exposed as HTTP and configured with `url: http://127.0.0.1:8080/mcp`.
- `type: sse` was not enough in practice; the HTTP endpoint had to be explicit.
- Removing the terminal block did not force MCP usage by itself.
- Adding a strong system prompt helped, but Hermes can still prefer shell fallbacks unless the MCP transport is correct.
- `kubectl`/`oc` inside the Hermes container were not required for MCP to work once the client connected correctly.
- The working static manifest uses a sidecar pattern: Hermes agent + `kubernetes-mcp-server` sidecar + `/opt/data` + `serviceAccountName` + `mcp_servers.kubernetes.url=/mcp`.
- For cluster metrics, Hermes still needs either `metrics-server` or a custom bridge; Prometheus alone is not enough for `pods_top` / `nodes_top`.
- Telegram privacy is enforced with `TELEGRAM_ALLOWED_USERS` and the gateway platform `allowed_users` list. Keep those aligned to a single user ID when you want a private bot.

---

## Installation

### Step 1: Install registry (fast)

```bash
make ai-registry
```

### Step 2: Build ARM64 image (60 min)

```bash
make ai-hermes-build
# Monitor with:
kubectl get jobs -n kaniko
kubectl logs -n kaniko job/build-hermes-arm64 -f | grep -v "npm WARN"
```

### Step 3: Deploy AI stack (fast)

```bash
make ai  # registry + litellm + hermes deploy (skips kaniko build)
```

### All at once (including build)

```bash
make ai-build && make ai
```

---

## Configuration

### API key (required)

Create `roles/install-hermes-agent/defaults/secrets.yml` (gitignored):

```yaml
hermes_openrouter_api_key: "sk-or-v1-..."
hermes_telegram_token: ""   # optional
hermes_discord_token: ""    # optional
```

LiteLLM proxy loads this same file automatically.

### Change default model tier

Edit `roles/install-hermes-agent/defaults/main.yml`:

```yaml
hermes_model: "free"    # default — uses LiteLLM fallback chain
hermes_model: "cheap"   # skip free tiers entirely
```

### Resources (CM4-friendly defaults)

| Component | CPU req | CPU limit | Mem req | Mem limit |
|-----------|---------|-----------|---------|-----------|
| LiteLLM proxy | 100m | 500m | 128Mi | 512Mi |
| Hermes Agent | 100m | 500m | 128Mi | 512Mi |

---

## Access

```bash
# Hermes web UI (requires ingress stack)
https://hermes.cluster.home

# Port-forward (no ingress required)
kubectl port-forward -n ai svc/hermes-agent 8080:8080
# → http://localhost:8080

# Hermes CLI
kubectl exec -it -n ai deployment/hermes-agent -- hermes

# LiteLLM proxy health
kubectl port-forward -n ai svc/litellm-proxy 4000:4000
curl http://localhost:4000/health
```

---

## Troubleshooting

### Kaniko build fails with OOM / disk pressure

```bash
kubectl describe node cm4-unknow  # check disk/memory
kubectl get events -n kaniko --sort-by=.lastTimestamp
```

Fix: build always runs on control-plane node (`node-role.kubernetes.io/control-plane`).
Job has `backoffLimit: 3` — it will retry up to 3 times.

### Kaniko build push fails (registry unreachable)

```bash
# Check registries.yaml on server node
ssh srv-rk1-01 "cat /etc/rancher/k3s/registries.yaml"
# Should show:
# mirrors:
#   "registry.registry:5000":
#     endpoint:
#       - "http://<ClusterIP>:5000"
```

Reapply: `make ai-registry`

### Hermes pod ImagePullBackOff

```bash
kubectl describe pod -n ai -l app=hermes-agent | grep -A5 Events
```

- Build not done → run `make ai-hermes-build` and wait
- `registries.yaml` not configured → run `make ai-registry`

### LiteLLM proxy CrashLoopBackOff

```bash
kubectl logs -n ai -l app=litellm-proxy --tail=50
```

- Missing `litellm-secrets` → run `make ai-hermes-deploy`
- Bad API key → check `roles/install-hermes-agent/defaults/secrets.yml`

### Hermes calling wrong model / 429 errors

LiteLLM handles 429s automatically via fallback chain.
Debug routing:
```bash
kubectl port-forward -n ai svc/litellm-proxy 4000:4000
curl http://localhost:4000/v1/models
```

---

## Useful Commands

```bash
# Build status
kubectl get job -n kaniko build-hermes-arm64
kubectl logs -n kaniko job/build-hermes-arm64 --tail=30 | grep -v "npm WARN"

# Registry images
kubectl port-forward -n registry svc/registry 5000:5000 &
curl http://localhost:5000/v2/_catalog

# AI stack health
kubectl get pods -n ai
kubectl logs -n ai -l app=litellm-proxy --tail=20
kubectl logs -n ai -l app=hermes-agent --tail=20

# LiteLLM models
kubectl port-forward -n ai svc/litellm-proxy 4000:4000 &
curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-hermes-internal"
```

---

## Repo Paths

- Roles: `roles/install-registry/`, `roles/install-litellm-proxy/`, `roles/install-hermes-agent-image/`, `roles/install-hermes-agent/`
- Playbook tags: `ai`, `ai-registry`, `ai-hermes-build`, `ai-hermes-deploy`
- Makefile: `make ai`, `make ai-registry`, `make ai-hermes-build`, `make ai-hermes-deploy`
- Secrets: `roles/install-hermes-agent/defaults/secrets.yml` (gitignored, shared with litellm-proxy)

### Operational notes

- Keep the Hermes MCP test manifest separate from the stable no-sidecar manifest.
- The sidecar image must exist in `registry.registry:5000` before Hermes pod rollout.
- Use `/mcp` for the Kubernetes MCP HTTP endpoint in Hermes configs.
