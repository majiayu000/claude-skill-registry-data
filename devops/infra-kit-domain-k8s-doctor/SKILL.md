---
name: infra-kit.domain.k8s-doctor
description: Debug Kubernetes workload, networking, routing, and rollout issues using read-only kubectl flows across pods, services, endpoints, HTTPRoute, ingress, and gateway resources.
---

# Kubernetes Debug

Use this skill when the user is troubleshooting Kubernetes runtime behavior such as failing Pods, broken Service routing, missing endpoints, HTTPRoute or Ingress issues, rollout failures, or namespace-scoped application reachability problems.

This skill is read-only by default. Prefer `kubectl get`, `kubectl describe`, `kubectl logs`, and `kubectl events` style inspection first.

This skill does not perform write actions. It is limited to read-only troubleshooting.

Never run mutating commands from this skill, including:

- `kubectl delete`
- `kubectl patch`
- `kubectl scale`
- `kubectl rollout restart`
- `kubectl apply`
- changing context or namespace defaults

For interactive troubleshooting commands that may still be useful during investigation, ask for approval step by step before each individual command:

- `kubectl exec`
- `kubectl debug`
- `kubectl cp`
- `kubectl port-forward`

When checking namespaced resources, prefer explicit namespace scoping on every command:

```bash
kubectl get pod -n <namespace>
kubectl describe svc -n <namespace> <name>
kubectl logs -n <namespace> <pod>
```

Do not rely on the current namespace implicitly when debugging user workloads.

## Outcomes

- Isolate whether the failure is in the workload, Service wiring, or traffic layer above it
- Explain the concrete broken hop in the request path
- Keep investigation safe by default through read-only inspection
- Leave the user with the exact evidence, command trail, and likely next fix

## Where This Fits In The Flow

- Use during intake/triage when the ticket is “something is broken in k8s” and you need a read-only diagnosis.
- Feed the findings back into `infra-kit.workflow` artifacts (`spec.md`/`plan.md`/`tasks.md`) before making changes.

## Workflow

1. Confirm the namespace, workload name, traffic entrypoint, and observed symptom before digging deeper.
2. Start at the backend and work outward, bottom to top:
   - Pod
   - controller (`Deployment`, `StatefulSet`, `DaemonSet`, `Job`)
   - Service
   - EndpointSlice
   - HTTPRoute or Ingress
   - Gateway or ingress controller exposure when relevant
3. Inspect Pods first:
   - readiness and liveness failures
   - restart counts
   - image pull issues
   - scheduling failures
   - recent logs
   - namespace events
   - if the Pod is in `Error`, `CrashLoopBackOff`, `ImagePullBackOff`, or another unhealthy state, capture both `describe pod` output and error logs into text files for later analysis
4. Check the owning controller next for rollout health, replica mismatch, and selector correctness.
5. Check the Service:
   - selector matches Pod labels
   - target port maps to a real container port
   - type and annotations fit the intended exposure model
6. Check `EndpointSlice` objects, not just Service existence. A healthy Service with zero or wrong endpoints is a common break point.
7. If Gateway API is used, inspect:
   - `HTTPRoute`
   - parent refs
   - backend refs
   - route status conditions
   - Gateway listener attachment
8. If Ingress is used, inspect:
   - rules and path matching
   - backend Service and port references
   - ingress class
   - controller events/status
9. Check namespace guardrails that commonly block healthy workloads:
   - `NetworkPolicy` for denied east-west or ingress-controller traffic
   - `ResourceQuota` for failed scheduling or rejected creates
   - `LimitRange` for implicit resource defaults or invalid workload sizing
10. Only after the path is mapped should you suggest interactive checks such as `exec` or `port-forward`.
11. Do not run those commands automatically. Present the exact next command, explain why it is needed, and wait for explicit user approval before each step.
12. If a likely fix requires patching, deleting, restarting, scaling, or applying resources, stop at the diagnosis and tell the user what change is recommended rather than performing it.

## Hallucination Guardrails

- Only report health or routing conclusions that are backed by concrete `kubectl` output; cite the exact command (and captured file when applicable) so the user can trace every statement to evidence.
- If a resource, namespace, or controller cannot be found, say so explicitly instead of assuming its state; ask the user for corrected names when needed.
- When permissions, kubeconfig access, or tooling limitations block a command, document the blocker and keep the analysis scoped to the data that was actually retrievable.
- Separate read-only evidence from recommended write actions clearly so users understand no mutation occurred and can decide whether to run the fix themselves.

## Command Pattern

Prefer a read-only sequence like:

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod -n <namespace> <pod>
kubectl logs -n <namespace> <pod> --container <container> --tail=200
kubectl get deploy -n <namespace>
kubectl describe deploy -n <namespace> <deploy>
kubectl get svc -n <namespace>
kubectl describe svc -n <namespace> <service>
kubectl get endpointslice -n <namespace>
kubectl describe endpointslice -n <namespace> <slice>
kubectl get networkpolicy -n <namespace>
kubectl describe networkpolicy -n <namespace> <policy>
kubectl get resourcequota -n <namespace>
kubectl describe resourcequota -n <namespace>
kubectl get limitrange -n <namespace>
kubectl describe limitrange -n <namespace>
kubectl get httproute -n <namespace>
kubectl describe httproute -n <namespace> <route>
kubectl get ingress -n <namespace>
kubectl describe ingress -n <namespace> <ingress>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

When the Pod is unhealthy, prefer capturing artifacts as files:

```bash
kubectl describe pod -n <namespace> <pod> > describe_pod.txt
kubectl logs -n <namespace> <pod> --container <container> --previous --tail=200 > log_error.txt
```

If `--previous` is not applicable, capture the current container logs instead.

If the issue is cross-namespace or controller-level, widen scope deliberately and say why.

## Review Priorities

When debugging Kubernetes, check in this order:

1. Pod health and recent events
2. Controller rollout status and selector consistency
3. Service selector and port wiring
4. EndpointSlice population and backend IP/port correctness
5. NetworkPolicy, ResourceQuota, and LimitRange side effects
6. HTTPRoute or Ingress routing rules and status conditions
7. Gateway, ingress controller, or external exposure layer

## Read-Only Rules

- Default to inspection commands only.
- Never treat `exec`, `debug`, `cp`, or `port-forward` as implicitly allowed.
- Ask before entering containers or creating debug containers.
- Ask before port-forwarding, even if it seems harmless.
- Do not perform write, restart, scaling, delete, patch, or apply actions from this skill.
- Make the exact command explicit before requesting approval for each non-read-only step.
- Approval is per step, not blanket approval for a whole debugging session.

Bundled helper:

```bash
bash scripts/collect_pod_debug.sh <namespace> <pod> [container]
```

## Delivery Standard

Always leave the user with:

- the exact hop where traffic or workload health breaks
- the commands used to prove it
- the key evidence from Pods, Services, endpoints, routes, and namespace guardrails
- the least invasive recommended fix, clearly separated from read-only findings
