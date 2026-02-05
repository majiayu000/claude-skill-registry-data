---
name: k8s-troubleshoot
description: Debug Kubernetes pods, services, and cluster issues. Use when the user says "pod not starting", "CrashLoopBackOff", "service not reachable", "kubectl debug", "pod stuck pending", or asks about Kubernetes problems.
allowed-tools: Bash, Read, Grep
---

# Kubernetes Troubleshoot

Debug pods, services, deployments, and networking issues in Kubernetes.

## Instructions

1. Identify the affected resource (pod, service, deployment)
2. Get current state with `kubectl get` and `kubectl describe`
3. Check logs if applicable
4. Diagnose based on status/events
5. Provide specific remediation steps

## Diagnostic commands

```bash
# Pod debugging
kubectl get pods -o wide
kubectl describe pod <pod>
kubectl logs <pod> [--previous] [-c container]
kubectl get events --sort-by=.lastTimestamp

# Service/networking
kubectl get svc,endpoints
kubectl describe svc <service>
kubectl get ingress

# Resource issues
kubectl top pods
kubectl describe node <node> | grep -A5 "Allocated resources"

# Debug pod (ephemeral container)
kubectl debug -it <pod> --image=busybox --target=<container>
```

## Common issues

| Status                     | Cause                | Solution                               |
| -------------------------- | -------------------- | -------------------------------------- |
| Pending                    | No resources         | Check node capacity, resource requests |
| Pending                    | No matching node     | Check nodeSelector, taints/tolerations |
| ImagePullBackOff           | Bad image/auth       | Verify image name, imagePullSecrets    |
| CrashLoopBackOff           | App crashing         | Check logs, entrypoint, health probes  |
| CreateContainerConfigError | Bad configmap/secret | Verify referenced configs exist        |
| Evicted                    | Node pressure        | Check node conditions, resource limits |

## Service not reachable checklist

1. Pod running? `kubectl get pods -l app=<app>`
2. Pod ready? Check readiness probe
3. Endpoints exist? `kubectl get endpoints <svc>`
4. Service selector matches pod labels?
5. Port/targetPort correct?
6. NetworkPolicy blocking traffic?

## Rules

- MUST check events with `kubectl describe` before diagnosing
- MUST check logs for CrashLoopBackOff
- Never delete pods/resources without user approval
- Never apply changes without showing the diff first
- Always specify namespace if not default: `-n <namespace>`
