---
name: gcp-gke-platform-operator
description: Operate GKE clusters (Standard and Autopilot), manage node pools, configure Workload Identity, enforce Binary Authorization, plan node pool upgrades, and review cluster security posture.
allowed-tools: Read Grep Glob Bash(gcloud container:*) Bash(kubectl apply:*)
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.2.0"
  updated: "2026-05-09"
  category: platform
---

# GCP GKE Platform Operator

## Purpose

Act as a rigorous GKE platform operator. Keep GKE clusters secure, upgraded, and operating with zero-trust pod identity and image provenance enforcement.

## Reference Directory

Load the relevant reference based on the request. Prefer the most specific match.

| Scenario | Trigger Keywords | Reference |
|---|---|---|
| Golden Path & Defaults | golden path, Day-0, production defaults, cluster creation | [Golden path and Day-0 checklist](#golden-path-configuration) |
| Networking | private cluster, VPC, subnet, Gateway API, DNS, ingress, datapath | [Networking section](#networking) |
| Security & IAM | Workload Identity, Secret Manager, RBAC, Binary Auth, hardening | [Security section](#security) |
| Scaling | HPA, VPA, autoscaler, NAP, scale pods, scale nodes | [Scaling section](#scaling) |
| Cost | Spot VMs, rightsizing, CUD, budget, OPTIMIZE_UTILIZATION | [Cost section](#cost) |
| AI/ML Inference | LLM serving, GPU, TPU, vLLM, GIQ, model deployment | [AI/ML Inference section](#aiml-inference) |
| Upgrades | maintenance window, release channel, patching, version | [Upgrades section](#upgrades) |
| Observability | monitoring, Prometheus, Grafana, metrics, alerts | [Observability section](#observability) |
| Multi-tenancy | namespace isolation, team access, RBAC planning | [Multi-tenancy section](#multi-tenancy) |
| Batch & HPC | batch jobs, high performance, MPI, parallel workloads | [Batch & HPC section](#batch--hpc) |
| Backup & DR | backup, restore, disaster recovery, CMEK | [Backup & DR section](#backup--dr) |
| Storage | PVC, persistent volume, StorageClass, Filestore, GCS FUSE | [Storage section](#storage) |

## Day-0 vs Day-1 Decisions

**Day-0 decisions** are made at cluster creation and are hard or impossible to change afterwards. Always surface and confirm these before generating any cluster config:

| Decision | Why It's Hard to Change |
|---|---|
| Autopilot vs Standard | Cannot convert after creation |
| Private nodes (`enablePrivateNodes`) | Requires cluster recreation to change |
| VPC and subnet | Network range cannot be shrunk post-creation |
| IP allocation policy (pod/svc CIDRs) | Cannot be modified after creation |
| Private endpoint enforcement | Changing opens public control plane |
| Workload Identity pool | Requires workload reconfiguration |
| Release channel | Changing channel may trigger immediate upgrade |

**Day-1 decisions** can be changed after cluster creation (some require node pool recreation or short downtime):
- Secret Manager integration
- Monitoring/logging component list
- Binary Authorization policy
- RBAC bindings
- Node pool machine type (via new pool + drain)
- Maintenance exclusion windows

## When to use

Use this skill for:

- GKE cluster type selection (Standard vs. Autopilot) and initial setup
- Node pool design, sizing, and upgrade planning
- Workload Identity configuration and audit
- Binary Authorization policy setup and enforcement path
- Release channel selection and upgrade strategy
- Cluster security posture review (network policies, Pod Security Standards, RBAC)

## Key GKE specifics

- GKE Autopilot: Google manages nodes, you manage pods. Billing is per Pod CPU/memory. Cannot run privileged containers or DaemonSets. Best for most workloads.
- GKE Standard: you manage nodes. More flexibility but more operational burden.
- Workload Identity: maps Kubernetes ServiceAccounts to GCP Service Accounts via annotation — eliminates SA key files from pods. Always prefer over mounted key files.
- Binary Authorization: enforces image signatures at admission. Must be set to WARN mode before ENFORCE mode — enforce mode will break deployments if images are unsigned.
- Node pool upgrades: cluster must be on a release channel (Rapid/Regular/Stable) for automated upgrades. Manual upgrades for custom versioning.
- Release channels: Rapid > Regular > Stable in terms of how quickly new Kubernetes versions arrive. Use Regular for production.

## Lean operating rules

- Prefer official GCP documentation and live evidence over memory or inference.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- Challenge missing Workload Identity, Binary Authorization in permissive mode, skipped node pool upgrades, and overbroad RBAC.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review or formatting the final answer.
- [Official sources](references/official-sources.md) — use when grounding GKE behavior or checking the detailed source list.

## AI/ML Inference

GKE supports GPU/TPU workloads for LLM inference via the GKE Inference Quickstart (GIQ) — a `gcloud` workflow that generates optimized Kubernetes manifests for specific model + accelerator + serving framework combinations.

### Discovery and manifest generation

```bash
# List all supported models
gcloud container ai profiles models list

# Find valid accelerator + server combinations for a model
gcloud container ai profiles list --model=gemma-2-9b-it

# Generate an optimized manifest
gcloud container ai profiles manifests create \
  --model=gemma-2-9b-it \
  --model-server=vllm \
  --accelerator-type=nvidia-l4 \
  --target-ntpot-milliseconds=50 > inference.yaml

# Deploy
kubectl apply -f inference.yaml
```

Supported model-server values: `vllm`, `tgi`, `triton`, `tensorrt-llm`
Common accelerator types: `nvidia-l4`, `nvidia-tesla-a100`, `nvidia-h100-80gb`, `nvidia-tesla-t4`

### Key rules for inference workloads
- GKE Autopilot supports GPU workloads via ComputeClasses and Node Auto-Provisioning — no manual node pool needed
- Use GIQ manifests as the starting point; they embed best-practice resource requests, tolerations, and readiness probes
- Some models (Llama, Mistral) require Hugging Face tokens — create a Kubernetes Secret and reference it in the manifest
- Monitor inference latency via `--target-ntpot-milliseconds` (Normalized Time Per Output Token) — this controls the accelerator selection trade-off
- For multi-tenant inference, use separate namespaces with ResourceQuotas per team

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main risks or control gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
