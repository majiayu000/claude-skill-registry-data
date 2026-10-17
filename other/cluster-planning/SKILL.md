---
name: cluster-planning
description: >
  Cluster planning guide: hardware profiles, deployment tiers, and roadmaps.
  Use cluster-advisor MCP to analyze survey data and generate a phased plan.
  Covers what each tier unlocks, how to assign nodes, and what to buy next.
license: MIT
compatibility:
  - opencode
metadata:
  tags: [k8s, k3s, planning, hardware, tiers, roadmap, homelab]
---

# Cluster Planning Guide

## Philosophy

A K8s homelab is not a destination — it's a learning progression.
Start small, validate, add complexity. Each phase teaches something new.

**Core principle:** maximize what you can deploy NOW, then identify what
hardware delta unlocks the NEXT tier. Never over-provision before you know
what you actually need.

---

## Hardware Profiles

These profiles classify what a cluster CAN be, not what it IS.
The cluster-advisor MCP reads survey data and assigns a profile automatically.

| Profile | Nodes | RAM/node | Storage | Unlocks |
|---------|-------|----------|---------|---------|
| `nano`     | 1    | 1–2 GB  | any     | Basic K8s, learning |
| `micro`    | 1–2  | 4 GB    | eMMC/SD | Full single-node: ingress + DNS + GitOps |
| `small`    | 3–5  | 4–8 GB  | NVMe    | HA control-plane + observability |
| `medium`   | 5–8  | 8–16 GB | NVMe    | Full stack: observability + security + AI |
| `large`    | 8+   | 16–32 GB| NVMe    | Everything: HA + AI + NPU inference |
| `gpu`      | any  | 16+ GB  | any     | Local AI inference (NPU/GPU required) |

---

## Deployment Tiers

Each tier adds capabilities. Run phases in order — each builds on the previous.

### Tier 1 — K8s Foundations
**Minimum:** 1 node, 2GB RAM, cgroups v2

What you deploy:
- K3s + kubeconfig
- Cilium CNI + LB-IPAM

What you learn:
- kubectl basics, pod scheduling, namespaces
- ClusterIP services, CNI networking

Make command: `make core`

---

### Tier 2 — Real Services
**Minimum:** 1 node, 4GB RAM, eBPF

What you deploy (adds to Tier 1):
- cert-manager (internal CA + wildcard TLS)
- Gateway API (shared HTTPRoute ingress)
- Pi-hole (wildcard DNS, local-path storage)
- ArgoCD (GitOps)
- Helm Dashboard (release UI)

What you learn:
- HTTPRoute pattern (ClusterIP + HTTPRoute — never LoadBalancer for HTTP)
- TLS termination, cert rotation
- GitOps workflow: push → sync
- Service-to-service DNS

Make command: `make services`

---

### Tier 3 — Observability
**Minimum:** 2+ nodes, 12GB total cluster RAM

What you deploy (adds to Tier 2):
- kube-prometheus-stack (Prometheus + Grafana + AlertManager)
- Grafana Tempo (distributed tracing)
- Grafana Loki (log aggregation)
- Alloy (telemetry collector)

What you learn:
- PromQL queries, dashboards, alerts
- Log correlation with Loki
- Trace-based debugging with Tempo
- The four golden signals (latency, traffic, errors, saturation)

Make command: `make observability`

---

### Tier 4 — AI Stack
**Minimum:** 24GB total cluster RAM, 4GB server RAM, OpenRouter API key

What you deploy (adds to Tier 2+):
- Docker registry (ARM64 image storage)
- LiteLLM proxy (OpenRouter router, free→free2→cheap fallback)
- Hermes Agent (AI assistant, Telegram + web)
- HolmesGPT + Holmes UI (SRE assistant)
- kagent (multi-tenant AI agent platform + MCP servers)

What you learn:
- LLM routing and fallbacks
- MCP (Model Context Protocol) servers
- AI agent patterns (tool-use loops, memory, multi-agent)
- Building K8s-native AI workloads

Make command: `make ai && make ai-holmes && make kagent`

Note: No GPU needed. Uses OpenRouter API (free tier available).
Costs: ~$0–$5/month depending on model usage.

---

### Tier 5 — Security
**Minimum:** 4GB server RAM, 8GB total RAM

What you deploy (adds to Tier 2+):
- NeuVector (container runtime security, vulnerability scanning)

What you learn:
- Container runtime security policies
- Network policy enforcement
- Vulnerability assessment in K8s
- Zero-trust networking

Make command: `make security`

Note: NeuVector uses a dedicated LoadBalancer (not HTTPRoute) — HTTPS backend.

---

### Tier 6 — HA Control-Plane
**Minimum:** 3 nodes with <10ms write latency, cgroups v2, eBPF

What you deploy:
- K3s embedded etcd across 3 server nodes
- All Tier 2–5 components across the HA cluster

What you learn:
- etcd consensus, split-brain prevention
- Leader election, node failure scenarios
- Rolling upgrades without downtime
- Production-grade cluster operations

Make command: `make services` (with 3 server nodes in inventory)

Note: etcd requires <10ms disk write latency per node.
NVMe: typically 0.1–3ms. eMMC: 2–10ms. USB/SD: 10–100ms+.

---

### Tier 7 — Local AI Inference (Future)
**Minimum:** 1+ node with NPU (/dev/rknpu0) or GPU, 16GB RAM

What you deploy (not yet implemented):
- Ollama or similar local inference engine
- RKNN runtime (Rockchip NPU)
- Local model serving

What you learn:
- Local LLM inference, model quantization
- NPU/GPU scheduling in K8s
- Air-gapped AI operations

Make command: `# Future: make ai-local`

Note: Rockchip RK3588S NPU (/dev/rknpu0) detected on RK1 nodes.
RKNN runtime needs to be packaged as a K8s role first.

---

## Node Role Assignment Rules

### Control-plane (etcd) nodes — pick the FASTEST writes

Priority (highest to lowest):
1. NVMe + <1ms write latency (ideal: western digital, samsung)
2. NVMe + 1–5ms write latency (acceptable)
3. eMMC + 2–5ms write latency (borderline — monitor etcd health)
4. eMMC + >5ms (not recommended for etcd — use as worker instead)

**Never use a node with >10ms write latency as etcd.**

### AI worker nodes — pick the MOST RAM

AI workloads (kagent, Hermes, Holmes) are memory-bound, not compute-bound.
- RK1 nodes (31GB) — ideal for AI workloads
- super6c (8GB) — acceptable for lightweight agent pods

NPU availability (rknpu0) is a bonus for future local inference.

### General workers — fill with remaining nodes

Any node with cgroups v2 and 2GB+ RAM can be a K3s agent.

---

## What to Buy Next

Recommendations by gap:

| Missing | Buy | Cost | Unlocks |
|---------|-----|------|---------|
| HA CP (need 3 nodes) | Raspberry Pi 5 (8GB) × 2 | ~$200 | Tier 6 |
| More AI RAM | Turing RK1 32GB module | ~$150 | Bigger models |
| Faster storage | 512GB NVMe M.2 | ~$50 | Better etcd, faster builds |
| Local inference | Rockchip RK3588 board | ~$200 | Tier 7 |
| More workers | Any ARM64 SBC with 4GB+ | ~$50–$100 | More pods |

---

## cluster-advisor MCP Tools

| Tool | What it does |
|------|-------------|
| `list_nodes()` | Table of all surveyed nodes with key metrics |
| `node_profile(hostname)` | Deep-dive: hardware, K8s readiness, role recommendation |
| `analyze_cluster()` | Achievable flavors + node assignments + make commands |
| `cluster_power_score()` | 5-dimension score: Compute / Memory / Storage / Network / AI |
| `cluster_roadmap()` | Phased deployment plan: what to run now vs later + what to buy |
| `cluster_stacks()` | RAM budget per behavioral stack + storage tiers + recipes |
| `learning_roadmap(profile)` | Curriculum for beginner/devops/ai-builder/security/full-stack |
| `hardware_catalog()` | Browse boards to buy with prices, K8s readiness, vendors |
| `what_to_buy(goal)` | Targeted recommendations: ha/npu/budget/inference/full-cluster |
| `stack_projects(stack)` | CNCF status + license + stars + maintenance health per stack |
| `get_skill(name)` | Read skill docs (cilium, ai, kagent, monitoring, etc.) |
| `list_skills()` | List all available skills |

```bash
# Start MCP (add to .mcp.json for Claude Code / opencode.json for OpenCode)
python3 mcp/cluster-advisor/server.py

# Run survey first to populate data
make survey

# Then ask Claude / OpenCode:
# "Analyze my cluster and tell me what I can deploy"
# "What hardware do I need to run the full AI stack?"
# "Give me a step-by-step deployment roadmap"
# "What's the CNCF status of the observability stack projects?"
# "I want to learn DevOps — what should I deploy and in what order?"
# "What boards should I buy to add local AI inference?"
```

---

## Knowledge Graph

The cluster-advisor connects 5 data sources:

```
survey/*.json           → live hardware facts (make survey → populates)
stacks.yaml             → 29 modular stacks (17 live, 12 planned)
learners.yaml           → 5 learning profiles with curricula
hardware-catalog.yaml   → 12 boards with prices/vendors
projects.yaml           → 44 projects: CNCF status, license, maintenance health
```

**Extending the knowledge graph** (YAML-only, no code changes):
- New stack: add to `stacks.yaml` with `status: planned` until roles are written
- New board: add to `hardware-catalog.yaml`
- New project: add to `projects.yaml` with all maintenance fields
- New learning profile: add to `learners.yaml`

---

## Planned Stacks (not yet implemented — add roles to activate)

| Stack | Adds |
|-------|------|
| `gitops-alternatives` | Flux, Helmfile, Kustomize, SOPS secrets |
| `data-engineering` | Kafka/Strimzi, Spark, Airflow KubernetesExecutor |
| `databases` | CloudNativePG, KubeDB, Vitess |
| `ml-platform` | Kubeflow, MLflow, KServe, Ray |
| `networking-advanced` | Cilium mesh, Istio, Linkerd, Flagger canary, BGP |
| `observability-advanced` | OTel Operator, Flagger, Pyrra SLOs, Chaos Mesh |
| `wasm` | WasmEdge, SpinKube, runwasi shim |
| `virtualization` | KubeVirt ARM64, CDI, live migration |
| `cost-modeling` | OpenCost, Kepler power, homelab vs cloud ROI |
| `sustainability` | Carbon-aware scheduler, power efficiency dashboard |
| `gpu-sharing` | HAMi, Rockchip NPU device plugin, RKNN |
| `storage-distributed` | Longhorn or OpenEBS Mayastor |

---

## Common Questions → MCP Tool

| Question | Tool to call |
|----------|-------------|
| "What hardware do I have?" | `list_nodes()` |
| "Can I run HA?" | `analyze_cluster()` |
| "How powerful is my cluster?" | `cluster_power_score()` |
| "What should I deploy first?" | `cluster_roadmap()` |
| "What do I need to buy?" | `what_to_buy('ha')` or `what_to_buy('local inference')` |
| "Which nodes for control-plane?" | `analyze_cluster()` (see Node Assignments) |
| "I want to learn K8s from scratch" | `learning_roadmap('beginner')` |
| "What's in the AI stack?" | `stack_projects('ai')` |
| "Is this project production-ready?" | `stack_projects('security')` |
| "How does cilium work?" | `get_skill('cilium')` |
