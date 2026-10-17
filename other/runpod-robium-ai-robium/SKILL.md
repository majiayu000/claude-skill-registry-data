---
name: runpod
description: Provision, diagnose, and clean up paid RunPod compute for robotics workloads.
---

# RunPod

Treat the allocated Pod, not the submitted request, as the resource contract.

## Before allocating

- Define the workload acceptance test, minimum compute, immutable image,
  storage, placement, ports, budget, deadline, and cleanup responsibility.
- Inspect balance, existing Pods, volumes, live inventory, prices, and volume
  locality without creating anything.
- Verify current CLI or API fields against
  [official RunPod documentation](https://docs.runpod.io/); provider interfaces,
  stock, and prices change.
- Present one exact candidate and obtain explicit approval for that paid
  resource and lifetime. Failed or mismatched creation does not authorize a
  series of retries.
- Read [provisioning.md](references/provisioning.md) when selecting an
  interface, attaching a network volume, or creating a Pod.

## Verify what was created

- Re-read safe fields for the image digest, GPU ID and count, cloud tier,
  datacenter, volume ID and mount, ports, registry identity, operating mode,
  price, and termination control.
- Never print full environment maps or authenticated resource objects; they may
  contain credentials.
- Delete a mismatched Pod after preserving safe evidence. Do not diagnose it as
  though its requested contract were realized.

Robium observed `runpodctl` 2.8 accepting volume flags while the resulting Pod
had no network volume, and REST rejecting a live inventory GPU identifier, on
2026-08-24. GraphQL expressed the required contract in that run. This is a
reason to verify provider state, not a universal preference for GraphQL.

For a public service with a shared daily cap, reserve a conservative maximum
session cost in an external atomic ledger before Pod creation. Use
generation-conditional writes, fail closed on conflicts, and reconcile only
controller-owned Pod IDs against final billing. A process-local counter or
unconditional object overwrite cannot enforce a multi-instance budget.

## Diagnose without guessing

- Combine control-plane state, system logs, container logs, storage identity,
  durable progress markers, health endpoints, and artifact timestamps.
- A missing runtime, silent container, or repeated start event does not alone
  distinguish a cold pull, restart loop, provider lag, or application failure.
- Use at most one explicitly approved, time-bounded interactive Pod to isolate
  application defects. A clean rerun from the rebuilt image digest is the
  deployment proof; an overlay is not.
- Read
  [diagnostics-and-lifecycle.md](references/diagnostics-and-lifecycle.md) for
  startup classification, proxy validation, evidence, billing, and cleanup.

## Finish the allocation

- Validate localhost before the provider proxy, then test authentication and
  scope boundaries through the public route.
- Download and independently check the evidence before termination.
- Record cost as provider billing, a price-by-lifetime bound, or an observed
  balance delta; do not blur those measures.
- Delete temporary Pods and verify the authoritative Pod list. Preserve a
  network volume unless its deletion was explicitly authorized; storage cost
  continues independently.
- Production enablement is a separate decision from feasibility or cleanup.
