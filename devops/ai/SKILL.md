---
name: ai
description: >
  AI Agent stack: Hermes Agent (self-improving AI assistant) routed through
  in-cluster LiteLLM proxy with OpenRouter fallback chains (free→free2→cheap).
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
| Hermes Agent | `registry.registry:5000/ai/hermes-agent` | 0.7.0 | ai | Gateway mode + Telegram polling + MCP sidecar |
| kubernetes-mcp-server | `registry.registry:5000/ai/kubernetes-mcp-server` | v0.0.60 | ai (sidecar) | K8s read-only MCP server sidecar in Hermes pod |
| HolmesGPT | `robusta/holmes` (Helm) | 0.24.0 | ai | SRE assistant — K8s + logs + Prometheus toolsets |
| Holmes UI | `nginx:alpine` | — | ai | Chat UI at `holmes-ui.cluster.home` (no kaniko, ConfigMap) |
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

Hermes does NOT call OpenRouter directly. It calls the in-cluster LiteLLM proxy:

```
OPENAI_API_BASE=http://litellm-proxy.ai.svc.cluster.local:4000
OPENAI_API_KEY=sk-hermes-internal  (LiteLLM master key)
HERMES_MODEL=free
```

LiteLLM config (`roles/install-litellm-proxy/tasks/main.yml`):

| Virtual model | Real model | Provider | Notes |
|--------------|-----------|---------|-------|
| `rk1-npu-local` | `llama-3.1-8b-instruct` | 4× RK1 NPU (load-balanced) | NPU only — no token limit workaround, `max_input_tokens: 4096` |
| `hermes-qwen` | `llama-3.1-8b-instruct` | 4× RK1 NPU | NPU directo — **NO usar como modelo principal de agentes** (4096 token limit traba sesiones largas) |
| `holmes-llama` | `llama-3.1-8b-instruct` | 4× RK1 NPU | Holmes alias |
| `qwen3.6-free` | `openrouter/qwen/qwen3-coder:free` | OpenRouter | **Hermes Agent primary** (desde 2026-05-28) |
| `free` | `openrouter/qwen/qwen3-coder:free` | OpenRouter | Cloud primary alias |
| `free2` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Cloud fallback #1 |
| `deepseek4v-free` | `openrouter/deepseek/deepseek-v4-flash:free` | OpenRouter | Cloud fallback #2 |
| `nemotron` | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | Nemotron alias — **NO soporta `tool_choice: any`** |
| `kimi-free` | `openrouter/moonshotai/kimi-k2.6:free` | OpenRouter | **Honcho reasoning primary** — 262K ctx, soporta tool_choice any/required (2026-06-01) |
| `gemma4-free` | `openrouter/google/gemma-4-31b-it:free` | OpenRouter | Free fallback extra |
| `deepseek-pro` | `openrouter/deepseek/deepseek-v4-pro` | OpenRouter | Paid strong fallback (last resort) |

**Routing policy (2026-05-28→2026-06-01):** NPU modelos (`hermes-qwen`, `rk1-npu-local`) son accesibles por nombre directo pero NO se usan como primario de ningún servicio. Todos los servicios (Hermes, Holmes, OpenClaw, kagent) usan OpenRouter free tier como primary.

**Por qué se sacó NPU de los servicios:** context limit 4096 tokens. En sesiones con historial largo (>20 mensajes + tool descriptions) el NPU se traba con APITimeoutError. OpenRouter no tiene ese límite.

**Default fallback chain (2026-06-01):** `default → kimi-free → gemma4-free → deepseek4v-free → deepseek-pro`

**`deepseek-free` was removed** from all chains — persistently 429 rate-limited on OpenRouter.

**`local-fast` removed from `context_window_fallbacks`** — it has the same 4096 NPU token limit as the primary, so it never helped with context overflow errors; it just delayed the real fallback.

**`modify_params: true`** — Added to `litellm_settings` (2026-06-01). LiteLLM auto-drops or translates provider-specific params (e.g. `tool_choice: "any"` → drops when unsupported). Required for Honcho's deriver/dialectic to work with any OpenRouter model.

### LiteLLM smoke tester

`scripts/test-litellm-models.py` — tests all model groups, reports which work/fail:

```bash
# Test all models against in-cluster LiteLLM
kubectl port-forward -n ai svc/litellm-proxy 4000:4000 &
python3 scripts/test-litellm-models.py --url http://localhost:4000 --key sk-hermes-internal

# Options
--timeout 30       # per-model timeout (default: 30s)
--prompt "hi"      # test prompt
--models free,free2,nemotron  # test specific models only
```

**Known broken (2026-05-28):** `qwen-turbo` (404 on OpenRouter), `gemini-flash-1.5` (404), any paid model if OpenRouter credits exhausted.

### Hermes MCP lessons learned

- Kubernetes MCP works reliably when exposed as HTTP and configured with `url: http://127.0.0.1:8080/mcp`.
- `type: sse` was not enough in practice; the HTTP endpoint had to be explicit.
- Removing the terminal block did not force MCP usage by itself.
- Adding a strong system prompt helped, but Hermes can still prefer shell fallbacks unless the MCP transport is correct.
- `kubectl`/`oc` inside the Hermes container were not required for MCP to work once the client connected correctly.
- The working static manifest uses a sidecar pattern: Hermes agent + `kubernetes-mcp-server` sidecar + `/opt/data` + `serviceAccountName` + `mcp_servers.kubernetes.url=/mcp`.
- For cluster metrics, Hermes still needs either `metrics-server` or a custom bridge; Prometheus alone is not enough for `pods_top` / `nodes_top`.
- Telegram privacy is enforced with `TELEGRAM_ALLOWED_USERS` and the gateway platform `allowed_users` list. Keep those aligned to a single user ID when you want a private bot.

Fallback chain: `free → free2 → cheap` (automatic, transparent to Hermes).
Use `cheap` or `strong` directly when you want to skip free tiers.

### LiteLLM Metrics & Grafana Dashboard

LiteLLM exposes AI traffic and billing metrics to Prometheus when `success_callback: ["prometheus"]` is set.

The `install-litellm-proxy` role automates observability:
1. **ServiceMonitor**: Deploys a `ServiceMonitor` looking for labels `app: litellm-proxy` (the LiteLLM service must have these labels in its metadata or Prometheus will silently ignore it).
2. **Grafana Dashboard**: Injects a custom JSON dashboard via ConfigMap labeled `grafana_dashboard: "1"` into the `monitoring` namespace. The Grafana sidecar automatically provisions it.

**Key Metrics Tracked:**
- `litellm_requests_metric_total`: Total successful and failed API requests.
- `litellm_request_total_latency_seconds_bucket`: Request latency histograms.
- `litellm_tokens_metric_total`: Prompt and completion tokens processed.
- `litellm_spend_metric_total`: Estimated USD cost of the inference based on model pricing.
- `litellm_deployment_successful_fallbacks_total`: Counter for when fallback chains trigger successfully.

---

## Installation

### Step 1: Install registry (fast)

```bash
make ai-registry
```

### Step 2: Build ARM64 images (60 min + 1 min)

```bash
make ai-hermes-build        # hermes-agent (~60 min on CM4)
make ai-kubernetes-mcp-build  # kubernetes-mcp-server sidecar (~1 min)
# Monitor with:
kubectl get jobs -n kaniko
kubectl logs -n kaniko job/build-hermes-arm64 -f | grep -v "npm WARN"
kubectl logs -n kaniko job/build-kubernetes-mcp-server-arm64 -f
```

Both images are required before Hermes deploy — `hermes-agent-mcp` pod has 2 containers.

### Step 3: Deploy LiteLLM proxy + Hermes (2 min)

```bash
make ai-hermes-deploy
```

### All at once

```bash
make ai  # registry + hermes-build + kubernetes-mcp-build + hermes-deploy (~70 min total)
```

---

## Configuration

### API key (required)

Create `roles/install-litellm-proxy/defaults/secrets.yml` (gitignored):

```yaml
hermes_openrouter_api_key: "sk-or-v1-..."
hermes_telegram_token: ""   # optional
hermes_discord_token: ""    # optional
```

LiteLLM proxy loads this same file automatically.

### Change default model tier

Edit `roles/install-hermes-agent/defaults/main.yml`:

```yaml
hermes_model: "qwen3.6-free"   # default (2026-05-28) — OpenRouter qwen/qwen3-coder:free
hermes_model: "free2"          # alternativa: nvidia/nemotron-120b:free (más capaz, misma key)
hermes_model: "hermes-qwen"    # NPU directo — EVITAR, 4096 token limit traba sesiones largas
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
kubectl describe node srv-rk1-nvme-01 | grep -E "DiskPressure|MemoryPressure|Taints"
kubectl get events -n kaniko --sort-by=.lastTimestamp
# Look for: "ephemeral-storage" eviction or DiskPressure taint
```

**Root cause (fixed 2026-06-01):** `local-path` StorageClass writes PVC data to node's root disk.
RK1 nodes have ~29 GB root disks. A 40 GB `kaniko_workspace_storage_size` PVC + ephemeral writes
triggers DiskPressure, which evicts ALL pods on the node (including Hermes, LiteLLM, etc.).

**Fix:** all kaniko roles use `longhorn-nvme` (NVMe replicated storage, not local disk).
Argo Workflow also has `ttlStrategy` and `ephemeral-storage` limits set.

**If DiskPressure still appears after fix:** check for leftover PVCs from failed builds:
```bash
kubectl get pvc -n kaniko          # delete stale PVCs
kubectl get workflows -n kaniko    # delete stuck workflows
```

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

### Hermes pod ImagePullBackOff (2 containers — both must exist)

```bash
kubectl describe pod -n ai -l app=hermes-agent-mcp | grep -A5 Events
```

The pod `hermes-agent-mcp` has 2 containers:
- `hermes-agent` → `registry.registry:5000/ai/hermes-agent:0.7.0` (build: `make ai-hermes-build`)
- `kubernetes-mcp-server` → `registry.registry:5000/ai/kubernetes-mcp-server:v0.0.60` (build: `make ai-kubernetes-mcp-build`)

Both builds must complete before the pod can start. If the sidecar image is missing, pod shows
`1/2` or `ImagePullBackOff` on the second container. Fix: run the missing build, then
`kubectl rollout restart deployment/hermes-agent-mcp -n ai`.

- `registries.yaml` not configured → run `make ai-registry`

### LiteLLM proxy CrashLoopBackOff

```bash
kubectl logs -n ai -l app=litellm-proxy --tail=50
```

- Missing `litellm-secrets` → run `make ai-hermes-deploy`
- Bad API key → check `roles/install-litellm-proxy/defaults/secrets.yml`

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

## Storage Dependency

All AI build/deploy roles use `smb-nas` StorageClass by default.
The storage backend (`install-cifs-nas`) is **auto-installed** as the first task — no need to run `make storage` separately.

| Role | Storage var | StorageClass |
|------|-------------|-------------|
| `install-registry` | `registry_storage_class` | `smb-nas` |
| `install-hermes-agent` | `hermes_storage_class` | `smb-nas` |
| `install-hermes-agent-image` | `kaniko_storage_class` | `longhorn-nvme` |
| `install-kubernetes-mcp-server-image` | `kubernetes_mcp_storage_class` | `smb-nas` |

**Kaniko workspace MUST be `longhorn-nvme`** (fixed 2026-06-01). Using `local-path` writes 40 GB workspace to
the node's root disk (`/var/lib/rancher/k3s/storage/`). RK1 nodes have ~29 GB root — accumulated failed builds
triggered DiskPressure and evicted all pods on that node. Also: Argo Workflow now has `ttlStrategy`
(5 min cleanup on success / 1 h on failure) and `ephemeral-storage` requests/limits so kubelet evicts the
build job before pressuring the node.

See `skills/storage/SKILL.md` for the full pattern documentation.

---

## HolmesGPT + Holmes UI

HolmesGPT (Helm `robusta/holmes` v0.24.0) is deployed in the `ai` namespace alongside Hermes.

- API: `https://holmes.cluster.home` → `POST /api/chat` `{"ask": "question"}` → `{"analysis": "markdown"}`
- Chat UI: `https://holmes-ui.cluster.home` — nginx:alpine + ConfigMap, no kaniko needed
- Latency: 60–90s (multiple LLM tool-use calls per query)
- Node: `srv-rk1-nvme-01` (`holmes_node_hostname` in `roles/install-holmes/defaults/main.yml`)
- Memory: 3Gi limit (1Gi → OOMKill, exit 137)

### Model routing map — every UI surface

| Surface | Effective model | GPU | Where configured |
|---|---|---|---|
| Holmes UI (`holmes-ui.cluster.home`) | `llama3.1:8b` via `gpt-5.4` | t7910 P4 :11434 | `roles/install-litellm-proxy/tasks/main.yml` "Legacy Aliases" |
| Headlamp ai-assistant → Holmes provider | `llama3.1:8b` via `gpt-5.4` | t7910 P4 :11434 | same LiteLLM alias above |
| Headlamp ai-assistant → Local Models | user-configured in browser localStorage | t7910 :11434 or :4000 | no code in repo |
| headlamp-holmes (inline pod diagnosis) | `qwen2.5-coder:7b` (`local-fast`) | t7910 P4 :11434 | hardcoded in `src/index.tsx` LITELLM_URL/LITELLM_MODEL |

**None use OpenRouter.** All use t7910 local GPU.

⚠️ `local-fast` alias works at t7910 LiteLLM `:4000` but NOT at Ollama `:11434` directly.
⚠️ `qwen2.5-coder:7b` embeds tool calls as JSON in `content` — don't use for Holmes (use `llama3.1:8b`).

### gpt-5.4 alias — routes to LOCAL GPU (no OpenRouter key needed)

Holmes v0.24.0 internally uses `gpt-5.4` as its default model name. The in-cluster
LiteLLM proxy **must** have this alias or Holmes fails with `BadRequestError`.

Current routing — **direct Ollama** (no t7910 LiteLLM hop):
```yaml
- model_name: gpt-5.4         # Holmes default call
  litellm_params:
    model: openai/llama3.1:8b
    api_base: http://192.168.178.90:11434/v1  # direct Ollama
    api_key: "dummy"

- model_name: openai/gpt-5.4  # same, prefixed variant
  litellm_params:
    model: openai/llama3.1:8b
    api_base: http://192.168.178.90:11434/v1
    api_key: "dummy"
```

Chain: Holmes → in-cluster LiteLLM (`gpt-5.4`) → **Ollama directly** :11434

**Why direct Ollama:** The double-hop (in-cluster LiteLLM → t7910 LiteLLM → Ollama) silently
breaks tool calling. `llama3.1:8b` generates inline JSON blobs instead of proper `tool_calls`
API objects. Calling Ollama's OpenAI-compatible `/v1` endpoint directly fixes this.

When OpenRouter key is available in `secrets.yml`, change to `openrouter/nvidia/nemotron-3-super-120b-a12b:free`.

### Local GPU routes (DIRECT to Ollama — bypass t7910 LiteLLM)

All `local-*` models route **directly to Ollama** ports, bypassing t7910 LiteLLM.
**Why:** Double-hop (in-cluster LiteLLM → t7910 LiteLLM → Ollama) breaks tool_calls.
Fixed 2026-05-22. t7910 LiteLLM still runs on :4000 for workstation/other devices.

| In-cluster alias | Ollama model | Port | Notes |
|---|---|---|---|
| `local-fast` | `qwen2.5-coder:7b` | `:11434` P4 | Chat/debug |
| `local-llama` | `llama3.1:8b` | `:11434` P4 | Tool calling ✅ |
| `local-reason` | `deepseek-r1:8b` | `:11434` P4 | Reasoning (no tool calls) |
| `local-coder-7b` | `qwen2.5-coder:7b-instruct-q8_0` | `:11436` M4000 | Code |
| `local-codestral` | `codestral:latest` | `:11436` M4000 | Large code |
| `local-deepseek` | `deepseek-coder-v2:16b` | `:11436` M4000 | — |

**Note**: `local-fast` (qwen2.5-coder:7b) embeds tool calls as JSON in `content`, not `tool_calls`.
Use `local-llama` (llama3.1:8b) for tool-calling tasks.

### LiteLLM secret — always created (even without OpenRouter key)

The `litellm-secrets` Secret is now always created (unconditionally). Previously the secret
was only created when `hermes_openrouter_api_key` was non-empty, causing `CreateContainerConfigError`
on fresh deploys without secrets.yml. Fixed in `roles/install-litellm-proxy/tasks/main.yml`.

### Holmes model fix — no `openai/` prefix in Helm values

Holmes Helm values use `model: "{{ holmes_model_name }}"` (without `openai/` prefix).
Using `openai/local-fast` caused Holmes to fall back to `gpt-5.4` because the
in-cluster LiteLLM had no `openai/local-fast` entry in model_list.

### Robusta Helm repo — must be added explicitly

The `install-holmes` role adds the repo:
```yaml
- name: Add Robusta Helm repository
  kubernetes.core.helm_repository:
    name: robusta
    repo_url: https://robusta-charts.storage.googleapis.com
```
Without this, `helm install robusta/holmes` fails with "repo not found".

### LiteLLM Metrics & Grafana Dashboard

LiteLLM exposes AI traffic and billing metrics to Prometheus when `success_callback: ["prometheus"]` is set.

The `install-litellm-proxy` role automates observability:
1. **ServiceMonitor**: Deploys a `ServiceMonitor` looking for labels `app: litellm-proxy` (the LiteLLM service must have these labels in its metadata or Prometheus will silently ignore it).
2. **Grafana Dashboard**: Injects a custom JSON dashboard via ConfigMap labeled `grafana_dashboard: "1"` into the `monitoring` namespace. The Grafana sidecar automatically provisions it.

**Key Metrics Tracked:**
- `litellm_requests_metric_total`: Total successful and failed API requests.
- `litellm_request_total_latency_seconds_bucket`: Request latency histograms.
- `litellm_tokens_metric_total`: Prompt and completion tokens processed.
- `litellm_spend_metric_total`: Estimated USD cost of the inference based on model pricing.
- `litellm_deployment_successful_fallbacks_total`: Counter for when fallback chains trigger successfully.

### Holmes AG-UI — Headlamp `ai-assistant` plugin integration

The Headlamp `ai-assistant` plugin (v0.2.0-alpha) can use Holmes as its AI backend
via the AG-UI streaming protocol. This requires several pieces:

#### 1. Combined server.py (ConfigMap mount)

Holmes 0.24.0 only exposes `/api/chat`. The Headlamp plugin needs `/api/agui/chat`.
Solution: mount a custom `server.py` over `/app/server.py` via ConfigMap subPath.

The combined server in `roles/install-holmes/files/holmes-combined-server.py` adds:
- `POST /api/agui/chat` — AG-UI streaming endpoint (SSE)
- `GET  /api/agui/chat/health` — health check

It uses `create_toolcalling_llm` (server toolsets) NOT `create_agui_toolcalling_llm`
(CLI toolsets) — the CLI version lacks K8s tools and causes tool-not-found failures.

#### 2. Namespace patch on ai-assistant plugin

The plugin hardcodes `fB="default"` (namespace). Holmes runs in `ai`. Patch after every install:
```bash
sed -i 's/"holmesgpt-holmes",dB=80,fB="default"/"holmesgpt-holmes",dB=80,fB="ai"/' \
  /tmp/headlamp-plugins/ai-assistant/main.js
```

#### 3. Proxy chain

```
Headlamp browser → localhost:4466 → k8s API proxy
  → /api/v1/namespaces/ai/services/holmesgpt-holmes:80/proxy/api/agui/chat
  → Holmes pod:5050 → in-cluster LiteLLM → Ollama (direct)
```

#### 4. Event generator — JSON extraction fix

`llama3.1:8b` sometimes wraps answers in TodoWrite-style JSON:
`{"id":"1","content":"The answer","status":"pending"}`.
The event generator in `holmes-combined-server.py` extracts the `"content"` field
rather than discarding the blob. See `_stream_agui_text_message_event` and the
`ANSWER_END` handler with `json.loads` fallback.

#### 5. Model requirements for Holmes

- ✅ `llama3.1:8b` — tool calling works when called via direct Ollama `/v1`
- ❌ `deepseek-r1:8b` — returns empty `content` (reasoning-only model, needs different handling)
- ❌ Double-hop via t7910 LiteLLM — silently breaks tool_calls format

#### 6. Memory limit + node placement

Holmes requires `memory_limit: 3Gi` — 1Gi causes OOMKill under load (exit code 137).
Node: `srv-rk1-nvme-01` (RK1 node, set via `holmes_node_hostname` in defaults).

After updating in-cluster LiteLLM ConfigMap, **restart Holmes pod**:
```bash
kubectl rollout restart deployment/holmesgpt-holmes -n ai
```
SubPath ConfigMap mounts don't auto-update in running pods.

### Holmes UI pattern — nginx:alpine + ConfigMap (no kaniko)

For simple static UIs (HTML/JS), skip kaniko entirely:
- HTML + nginx.conf live in a ConfigMap (`holmes-ui-config`)
- nginx:alpine deployment mounts them via `subPath`
- nginx proxies `/api/` → Holmes with `proxy_read_timeout 300s`

```bash
make ai-holmes      # deploy Holmes + Holmes UI
make holmes-ui      # deploy Holmes UI only
```

---

---

## Headlamp + ai-assistant plugin (observability UI with Holmes)

Headlamp is the K8s web UI. The official `ai-assistant` plugin connects it to Holmes.

### Deploy order (single-node minimum)

```bash
make core          # K3s + kubeconfig
make networking    # Cilium + Gateway API
make ingress       # cert-manager + gateway (HTTPRoutes need this)
make dns-metrics   # Pi-hole — wildcard *.cluster.home DNS

# LiteLLM proxy + Holmes (skip hermes — no ARM64 build needed)
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
  --tags ai-hermes-deploy,ai-holmes \
  --skip-tags ai-hermes-agent
```

Resource budget on single CM4 node (7.6 GB RAM):
- cert-manager (3 pods): ~150 Mi
- Gateway (Cilium): ~64 Mi
- LiteLLM proxy: 512 Mi request / 3 Gi limit
- Holmes: 512 Mi request / 1 Gi limit
- Pi-hole: 100 Mi
- **Total requests: ~1.4 GB — fits comfortably on 7.6 GB**

### Run Headlamp locally (workstation)

```bash
mkdir -p /tmp/headlamp-work /tmp/headlamp-plugins
cd /tmp/headlamp-work
curl -sL https://github.com/headlamp-k8s/headlamp/releases/download/v0.42.0/Headlamp-0.42.0-linux-x64.tar.gz \
  -o headlamp.tar.gz && tar -xzf headlamp.tar.gz

# Install ai-assistant plugin (pre-built)
curl -sL https://github.com/headlamp-k8s/plugins/releases/download/ai-assistant-0.2.0-alpha/headlamp-k8s-ai-assistant-0.2.0-alpha.tar.gz \
  -o /tmp/ai-assistant.tar.gz
tar -xzf /tmp/ai-assistant.tar.gz -C /tmp/headlamp-plugins/

# Start Headlamp
/tmp/headlamp-work/Headlamp-0.42.0-linux-x64/resources/headlamp-server \
  -kubeconfig ~/.kube/config \
  -html-static-dir /tmp/headlamp-work/Headlamp-0.42.0-linux-x64/resources/frontend \
  -plugins-dir /tmp/headlamp-plugins \
  -dev -port 4466
```

### Configure ai-assistant to use Holmes

In Headlamp → ✨ (top right) → **Settings** → **Add configuration**:

| Field | Value |
|---|---|
| Provider | `Holmes` |
| URL | `http://holmes.cluster.home` |

Holmes then answers with real cluster data — it calls kubectl, reads logs, queries Prometheus.
Latency: 20-60s per query (multiple tool calls).

### Plugin compatibility fix

Headlamp checks `package.json` alongside `main.js`. Without it, plugin shows "incompatible".
Both files must exist in `/tmp/headlamp-plugins/<plugin-name>/`.

### headlamp-holmes (custom lightweight plugin)

Alternative to ai-assistant: adds an inline "AI Diagnosis" section to every Pod/Deployment detail.
Source: `/tmp/headlamp-holmes/src/index.tsx`, built with:
```bash
cd /tmp/headlamp-holmes && node_modules/.bin/headlamp-plugin build
cp dist/main.js package.json /tmp/headlamp-plugins/headlamp-holmes/
```
Calls LiteLLM directly (not Holmes) — no cluster access, just static JSON analysis.
Auto-triggers on CrashLoopBackOff/Pending/restartCount>3.

Full setup guide: `docs/headlamp-setup.md`

---

## Repo Paths

- Roles: `roles/install-registry/`, `roles/install-litellm-proxy/`, `roles/install-hermes-agent-image/`, `roles/install-hermes-agent/`, `roles/install-holmes/`, `roles/install-holmes-ui/`
- Playbook tags: `ai`, `ai-registry`, `ai-hermes-build`, `ai-hermes-deploy`, `ai-holmes`, `ai-holmes-ui`
- Makefile: `make ai`, `make ai-registry`, `make ai-hermes-build`, `make ai-hermes-deploy`, `make ai-holmes`, `make holmes-ui`
- Secrets: `roles/install-hermes-agent/defaults/secrets.yml` (Hermes bot tokens) & `roles/install-litellm-proxy/defaults/secrets.yml` (OpenRouter keys)

### Hermes secrets — `include_vars` required

`roles/install-hermes-agent/defaults/secrets.yml` is NOT auto-loaded by Ansible
(only `defaults/main.yml` is auto-loaded). The role explicitly calls `include_vars`
at the start to load secrets. If `secrets.yml` is missing, the role continues with
empty vars (`failed_when: false`) — resulting in empty OPENROUTER_API_KEY.



### Operational notes

- Deployment name is `hermes-agent-mcp` (not `hermes-agent`) — sidecar pattern since 2026-04.
- The sidecar `kubernetes-mcp-server` exposes port 8080 → Hermes connects via `http://127.0.0.1:8080/mcp`.
- `hermes-secrets` Secret and `hermes-gateway-config` ConfigMap are created by the Ansible template on every deploy.
- Use `/mcp` for the Kubernetes MCP HTTP endpoint in Hermes configs.

---

## OpenCode CLI — uso desde línea de comandos

OpenCode v1.4.0. Config leída en este orden (la primera que exista gana):
1. `~/.config/opencode/opencode.json` o `~/.config/opencode/opencode.jsonc` (global)
2. `./opencode.json` o `./opencode.jsonc` (proyecto — este repo)

> **`opencode.local.json` NO existe** en v1.4.0 — solo `.json` y `.jsonc`.

### Modos de uso

```bash
# Modo interactivo (TUI) — desde el directorio del repo
opencode

# Non-interactive: prompt único, resultado por stdout, sale al terminar
opencode run "¿Cuántos pods hay en el namespace ai?"

# Con modelo específico (--model provider/alias)
opencode run --model litellm/kimi-free "Responde en una línea: qué modelo eres"

# Modo interactivo forzando un modelo distinto al default del config
opencode --model litellm/claude-sonnet
```

### Formato `--model`

Siempre `provider/alias`. El provider es la clave en `opencode.json → provider`:

```
litellm/default          # Claude Sonnet vía OpenRouter (default del repo)
litellm/kimi-free        # Kimi K2.6 — MEJOR free (18-57s, tool calling nativo)
litellm/gpt-oss-free     # GPT-OSS 20B (free, ~o3-mini calidad)
litellm/nemotron         # Nemotron Super 120B (free)
litellm/nemotron-ultra   # Nemotron Ultra 550B (free, 1M ctx — latencia alta en free tier)
litellm/llama70b-free    # Llama 3.3 70B (free, 131K ctx)
litellm/rk1-npu-local    # Llama 3.1 8B NPU — 4× RK1 in-cluster, 0 costo, ctx 4K
litellm/claude-sonnet    # Claude Sonnet 4.5 (de pago, vía OpenRouter)
litellm/claude-opus      # Claude Opus 4 (de pago)
litellm/gemini-flash     # Gemini Flash (vía OpenRouter)
litellm/cheap            # Qwen Turbo (más barato)
litellm/free             # qwen3-coder:free con fallback chain
```

### LiteLLM local vs in-cluster

`opencode.json` apunta a `http://localhost:4000/v1`. Dos formas de tenerlo activo:

**Opción A — Local (workstation):**
```bash
# En una terminal separada:
mise run litellm          # o: make litellm
# LiteLLM escucha en :4000, usa setup/litellm/config.yaml
```

**Opción B — In-cluster (sin correr LiteLLM local):**
```bash
# Port-forward al servicio del cluster (mantener abierto en background):
kubectl port-forward -n ai svc/litellm-proxy 4000:4000 &

# Luego opencode usa el LiteLLM del cluster transparentemente
opencode run --model litellm/kimi-free "tu prompt aquí"
```

> API key unificada: `sk-hermes-internal` (en `opencode.json`, `setup/litellm/config.yaml`,
> y `~/.config/opencode/opencode.jsonc`).

### MCP servers activos en el repo

`opencode.json` activa dos MCP:
- **kubernetes** (`npx kubernetes-mcp-server@latest`) — pods, logs, events, namespace list
- **cluster-advisor** (`python mcp/cluster-advisor/server.py`) — knowledge graph del cluster

El MCP de kubernetes requiere `~/.kube/config` válido (creado por `make core`).

### Gotchas conocidos

| Problema | Causa | Fix |
|---|---|---|
| `No connected db.` al hacer streaming | LiteLLM ≥1.82 sin PostgreSQL | `allow_requests_on_db_unavailable: true` (ya en el role) |
| API key `sk-infra-local` no funciona | LiteLLM espera `sk-hermes-internal` como master key | Actualizar en todos los configs (ya hecho) |
| Context7 MCP demora 23-30s en arrancar | npm download timeout | Desactivar en `~/.config/opencode/opencode.jsonc` → `"enabled": false` |
| Multiple `opencode run` bloqueados | SQLite lock en `~/.local/share/opencode/opencode.db` | `kill -9 $(pgrep -f ".opencode")` antes de correr nuevo proceso |
| `ProviderModelNotFoundError` | Provider desconocido o alias no en config | Verificar que el alias esté en `opencode.json → provider.litellm.models` |
