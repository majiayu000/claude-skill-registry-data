---
name: gpu-infrastructure-security
description: Review GPU infrastructure for shared tenancy risks — VRAM residue between workloads, GPU memory not cleared between jobs, CUDA context isolation failures, side-channel attacks via GPU timing, and credential exposure in GPU compute environments.
last_reviewed: 2026-04-29
---

# GPU Infrastructure Security

## First Principle

**A GPU is shared memory. When one workload finishes and another begins on the same GPU, the VRAM from the previous workload is not automatically zeroed. Any workload that runs after you may be able to read data you left behind — including model weights, intermediate activations, and input tokens.**

GPU security is routinely overlooked because GPU programming abstractions hide the underlying memory model. CUDA does not zero VRAM between kernel invocations by default. In a multi-tenant GPU cluster — cloud instances, Kubernetes GPU nodes, shared research clusters — the boundaries between workloads depend on the orchestration layer correctly isolating VRAM allocations. Those boundaries have failed in documented attacks.

## Attack Mental Model

1. **VRAM residue leakage** — after a workload completes and releases GPU memory, the next workload allocated to the same GPU can read uninitialized VRAM containing data from the previous workload.
2. **GPU timing side-channel** — CUDA kernel execution times vary based on input data. An attacker sharing a GPU can measure timing to infer properties of a victim workload's computation — including token counts, attention patterns, or model architecture details.
3. **Credential exposure in compute environments** — GPU training jobs often run in environments where cloud credentials are injected via environment variables or instance metadata. A workload with code execution capability can exfiltrate these credentials.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | GPU memory is explicitly cleared (zeroed) before release. Workloads explicitly initialize VRAM allocations rather than relying on implicit zero-initialization. |
| **Scope** | Sensitive inference workloads run on dedicated GPU instances — not shared with other tenants or workloads of different trust levels. |
| **Isolate** | GPU credentials (IAM roles, API keys, cloud metadata) are scoped to the minimum permissions required for the inference or training task — not inherited from a high-privilege node role. |
| **Enforce** | GPU node access is limited to authorized workloads. Node-level shell access for debugging is audited and time-limited. |

## GIS.1 VRAM Isolation and Memory Clearing

**The core vulnerability:** CUDA's `cudaMalloc` does not guarantee zero-initialized memory. Memory released by one process may be immediately reallocated to another process on the same GPU in a shared environment. The new process can read the contents of the previous allocation using standard CUDA memory reads.

### Check

- Are GPU workloads running on dedicated instances (one tenant per physical GPU) — or in a shared multi-tenant environment where VRAM is multiplexed between jobs?
- If running in a shared environment, is GPU memory explicitly zeroed before release in all workloads that handle sensitive data?
- Are GPU drivers and firmware versions current — including any patches that address VRAM isolation vulnerabilities?

### Action

- **Prefer dedicated GPU instances for sensitive workloads.** In AWS, use instances where GPU isolation is guaranteed at the hardware level (each EC2 instance gets dedicated GPU hardware, not a virtualized slice). In Kubernetes, schedule sensitive workloads with node affinity rules that prevent co-location with untrusted workloads.
- **Explicitly zero sensitive VRAM allocations before freeing.** When handling sensitive data (inference inputs containing PII, model weights for proprietary models), zero the allocation before calling `cudaFree`:

```python
import torch
import ctypes

def secure_free(tensor: torch.Tensor):
    # zero the tensor data before releasing
    tensor.zero_()
    # explicitly synchronize to ensure the zero operation completes
    if tensor.is_cuda:
        torch.cuda.synchronize()
    del tensor
```

- **Keep GPU drivers current.** GPU driver vulnerabilities that allow cross-process VRAM access have been disclosed (CVE-2018-6260, related side-channel work). Maintain a patching cadence for GPU nodes — treat GPU driver updates as security-critical.

### Failure Modes

- A Kubernetes GPU node runs inference pods from multiple tenants using time-slicing (MIG or GPU sharing). A malicious pod allocates and reads uninitialized VRAM containing activations from the previous tenant's inference request.
- A PyTorch training job allocates a large tensor for intermediate computation. The job exits without explicitly zeroing the tensor. The next job on the GPU inherits the allocation with the previous job's gradient data.

## GIS.2 Credential Isolation in GPU Compute Environments

**The core vulnerability:** GPU training and inference jobs typically run in containers or VMs that inherit cloud credentials from the node's instance metadata service (IMDS). If a workload achieves code execution (via prompt injection → tool use → arbitrary command), it can query IMDS to obtain IAM credentials with whatever permissions the node role has — often far broader than the workload needs.

### Check

- Does the GPU node's IAM role have permissions beyond what is required for GPU workloads — such as write access to production S3 buckets, ECR, or other services?
- Is instance metadata service (IMDS) access blocked for containers that do not require cloud credentials — using `--metadata-service-num-hops 0` in Docker or equivalent Kubernetes network policy?
- Are GPU node access logs (SSH connections, kubectl exec sessions) audited and retained?

### Action

- **Apply IMDSv2 and hop limit restriction.** Configure the GPU node's IMDS to require IMDSv2 (token-based access) and limit the hop count to 1, preventing containers from accessing instance credentials:

```bash
# When launching an EC2 instance
aws ec2 run-instances \
  --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=1"
```

In Kubernetes, block IMDS access at the network policy level for pods that do not require cloud credentials:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: block-imds
spec:
  podSelector: {}
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except: ["169.254.169.254/32"]  # block IMDS
```

- **Scope GPU node IAM roles to minimum required permissions.** The node role should allow only: reading from the training data bucket, writing to the staging artifact bucket, and pulling from the container registry. No production write access. No IAM mutation permissions.
- **Audit kubectl exec and SSH access.** Every interactive session on a GPU node is a security event. Log session start/end times, the user, and the commands executed. Alert on sessions longer than 30 minutes.

### Minimum Deliverable Per Review

- [ ] Tenancy model: dedicated vs. shared GPU instances and justification
- [ ] VRAM clearing: explicit zero-before-free for sensitive data allocations
- [ ] Driver patch status: current driver version and last patching date
- [ ] IMDS configuration: IMDSv2 required, hop limit set to 1
- [ ] Network policy: IMDS blocked for containers without cloud credential requirements
- [ ] Node IAM role: scoped to staging storage only, no production write access

## Quick Win

**Set `HttpPutResponseHopLimit=1` on all GPU EC2 instances.** This single metadata option prevents containers running inside the instance from reaching the IMDS endpoint to obtain IAM credentials — without affecting the host's access to its own credentials. It takes one AWS CLI command and requires no workload changes.

## References

- Container security for AI workloads → [container-ai-workload-security/SKILL.md](../container-ai-workload-security/SKILL.md)
- System and runtime security → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Secrets management → [secrets-in-prompts-detection/SKILL.md](../secrets-in-prompts-detection/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
