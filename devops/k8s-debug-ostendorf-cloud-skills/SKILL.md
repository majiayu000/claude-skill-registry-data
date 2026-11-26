---
name: k8s-debug
description: "Diagnoses a failing workload in Kubernetes read only first, from events and logs down to scheduling, storage, network and ingress, then proposes a fix before touching live state. Use when a pod, deployment, job or release in the cluster is not working."
---

# Kubernetes debugging

Find out what is wrong before changing anything in a live cluster.

## When to use

- A pod is crash looping, pending, or not ready.
- A Helm release failed or is stuck.
- A service, route or ingress is unreachable.

## Steps

1. Confirm the context first: which cluster, which namespace. Never debug against the wrong
   context, and say which one is in use.
2. Read only phase, in this order:
   - `kubectl get` the object and its owner, then its events.
   - `kubectl describe` for scheduling, image pull, probe and volume detail.
   - current and previous container logs.
   - the rendered configuration (`helm get values`, `helm get manifest`) against what the
     repository says it should be.
   - storage: PVC status, bound volume, storage class events.
   - network: Service, Endpoints, NetworkPolicy, ingress or gateway route.
3. Classify the failure before acting: image or registry, configuration, secret or RBAC,
   scheduling and resources, storage, network and DNS, probe tuning, application defect, upstream
   regression.
4. Build a short table of findings: object, symptom, evidence, suspected cause.
5. Do not restart, delete or scale anything to make the symptom disappear. A restart destroys the
   evidence. If a restart or a scale change is the actual fix, say so and ask first. Never scale a
   workload to zero without confirmation.
6. Propose the fix as a change in the repository, not as a live edit. A live change is drift and is
   lost on the next apply. If an emergency live change is unavoidable, confirm it first and write
   the matching repository change right after.
7. Report: the cause with its evidence, the proposed change, and what could not be determined.

## Guardrails

- Never restart, delete or scale a workload without confirmation.
- Never scale a workload to zero without confirmation.
- Never treat a live edit as the fix. The repository change is the fix, the live edit is a bridge.
- Never skip the read only phase to save time.

## References

- `kubernetes-conventions` for how the workload should be installed and configured.
- `tofu-plan` when the fix is an infrastructure change.
