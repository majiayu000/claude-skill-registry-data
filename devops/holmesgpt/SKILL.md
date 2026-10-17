---
name: holmesgpt
description: >
  HolmesGPT in Kubernetes: OpenAI-compatible backend via LiteLLM, Kubernetes
  and log/metrics toolsets, Gateway API exposure, and in-cluster troubleshooting.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, holmesgpt, ai, litellm, openai-compatible, gateway-api, observability]
---

# HolmesGPT Skill

## Cluster Context

HolmesGPT runs in the `ai` namespace and uses the in-cluster LiteLLM proxy as
an OpenAI-compatible backend.

### Backend wiring

- `OPENAI_API_BASE=http://litellm-proxy.ai.svc.cluster.local:4000/v1`
- `OPENAI_API_KEY=sk-hermes-internal` (LiteLLM master key)
- Models must support function calling / tool calling

### First smoke test

```bash
kubectl port-forward -n ai svc/holmesgpt-holmes 8080:80
curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"ask":"list pods in namespace ai?","model":"holmes-litellm"}'
```

Or use the local wrapper from `infra`:

```bash
./scripts/holmes-chat "Using Prometheus, how many pods are using more than 500 MiB of RAM right now?"
./scripts/holmes-chat "Using Prometheus, show the top 5 pods by CPU in namespace monitoring over the last 15m."
```

### Prometheus questions

Ask Holmes in plain English and mention Prometheus explicitly:

```bash
curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"ask":"Using Prometheus, show the top 5 pods by CPU in namespace monitoring over the last 15m.","model":"holmes-litellm"}'

curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"ask":"Using Prometheus, check whether Grafana latency or error rate spiked in the last 30m.","model":"holmes-litellm"}'

curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"ask":"Using Prometheus, how many pods are using more than 500 MiB of RAM right now? List the namespace, pod name, and memory usage.","model":"holmes-litellm"}'

curl -X POST http://localhost:8080/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"ask":"Using Prometheus, show the top 10 pods by memory usage in namespace monitoring over the last 15m.","model":"holmes-litellm"}'
```

### Telegram prompts

In Telegram, send plain text. Do not prefix with `/ask`.

Examples:

```text
che como está mi cluster
cuantos pods hay en monitoring
mostrame los pods que usan más de 500 MiB de RAM
revisá si argocd está healthy
```

### Expected toolsets

- Kubernetes core
- Kubernetes logs
- Live metrics
- Prometheus stack
- Bash (extended allowlist)

### MCP follow-up

HolmesGPT can also use MCP servers later (for example GitHub or custom K8s
helpers). Not wired yet in this cluster; add it after the base Helm install is
stable.

### Troubleshooting

1. Check the Holmes deployment and service:
   ```bash
   kubectl get deploy,svc,httproute -n ai | grep holmes
   ```
2. Check pod logs:
   ```bash
   kubectl logs -n ai -l app.kubernetes.io/name=holmes --tail=100
   ```
3. Verify LiteLLM access from the pod:
   ```bash
   kubectl exec -it -n ai deploy/holmesgpt-holmes -- sh -lc 'curl -sf -H "Authorization: Bearer sk-hermes-internal" http://litellm-proxy.ai.svc.cluster.local:4000/v1/models'
   ```
4. If tool calling fails, pick a different OpenRouter model in LiteLLM.
