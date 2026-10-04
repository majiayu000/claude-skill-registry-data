---
name: ml-stack-compute
description: Route ML workloads when a user asks about local CPU or GPU, HF Jobs, Sandbox, Spaces, Kaggle, Modal, SSH, Slurm, quotas, cost, logs, retries, cancellation, artifacts, or resume; plan provider-neutral execution with explicit approvals.
---

# Compute routing

Require workload specification, hardware/memory, data locality, network and secret policy, quota, latency, cost ceiling, persistence, and cleanup approval.

## Workflow

1. Preflight local or remote hardware, driver/framework compatibility, quota, expected duration, cost, and failure modes.
2. Select local CPU/GPU, HF Jobs/Sandbox/Spaces, Kaggle, Modal, SSH, or Slurm by constraints; record why alternatives were rejected.
3. Stage immutable code, data, model, environment, and secrets-by-reference. Define submit, status, logs, inspect, cancel, artifact, cleanup, heartbeat, retry, and resume actions.
4. Require explicit approval before paid, remote, secret-bearing, destructive, or publication actions.
5. Emit a bounded provider plan or executable job handoff to `ml-stack-training` and diagnostics to `ml-stack-tracking`; never claim submission when no registry operation exists.

## Outputs and recovery

Return provider, resource profile, commands or API intent, estimated cost, approval state, run identity, artifact paths, heartbeat and orphan recovery policy. Abstain when quota, cost, data access, or resume point is unknown. Next owner: `ml-stack-training` for job content, `ml-stack-tracking` for runtime diagnostics, and `ml-stack-audit` for evidence reconciliation.

See [provider routing](references/provider-routing.md), [sandbox and jobs](references/sandbox-and-jobs.md), [resource profiles](references/resource-profiles.md), [resume and orphans](references/resume-and-orphans.md), and [cost controls](references/cost-controls.md).
