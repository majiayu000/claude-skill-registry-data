---
name: k8s-debug
description: >
  Kubernetes debugging skill: systematic approach to diagnosing pod failures,
  network issues, resource contention, and cluster-level problems.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, debugging, troubleshooting, k8s]
---

# Kubernetes Debugging Skill

When diagnosing Kubernetes issues, follow this systematic approach:

## Pod not starting
1. `kubectl get pod <name> -o wide` — check node, status, restarts
2. `kubectl describe pod <name>` — read Events section first
3. `kubectl logs <name> --previous` — if CrashLoopBackOff
4. Check resource limits: OOMKilled → increase memory limit
5. Check image pull: ImagePullBackOff → verify registry auth / image tag

## Service not reachable
1. `kubectl get endpoints <svc>` — verify pod IPs are listed (selector match?)
2. `kubectl run -it --rm debug --image=nicolaka/netshoot -- bash` — test from inside cluster
3. Check NetworkPolicy: `kubectl get netpol -A`
4. Verify port names match between Service and Pod spec

## Node pressure
1. `kubectl describe node <name>` — check Conditions and Allocated resources
2. `kubectl top nodes` / `kubectl top pods -A --sort-by=memory`
3. Identify DaemonSets consuming resources on every node

## Persistent volume issues
1. `kubectl get pvc -A` — check Bound/Pending status
2. `kubectl describe pvc <name>` — look for provisioner errors
3. Verify StorageClass exists: `kubectl get sc`

## General tools
- `k9s` — interactive real-time view
- `kubectl events --for pod/<name>` (k8s 1.26+)
- `stern <pod-prefix>` — multi-pod log tailing
- `kubectl exec -it <pod> -- /bin/sh` — shell into container

## Hermes MCP troubleshooting

- Working Hermes MCP setup used an in-pod HTTP sidecar exposing `http://127.0.0.1:8080/mcp`.
- `url` was required in Hermes config; `type: sse` alone did not solve client selection.
- Keep the `kubernetes-mcp-server` container in the same pod as Hermes.
- Mount `/opt/data`, `/opt/data/.hermes`, `config.yaml`, `.env`, and `gateway.json`.
- Use `serviceAccountName` on the pod and let Kubernetes mount the API token/CA automatically.
- If Hermes falls back to terminal and tries `kubectl`, remove or disable the terminal block while testing MCP.
- The static manifest that worked used `hermes-agent-mcp` + `kubernetes-mcp-server:v0.0.60` + `hermes-config-mcp-test` + `mcp_servers.kubernetes.url: http://127.0.0.1:8080/mcp`.
- For Telegram-only access, enforce the bot allowlist with `TELEGRAM_ALLOWED_USERS` and the gateway `allowed_users` field; if either is broad, anyone can talk to the bot.

## Common quick fixes
- Stuck namespace terminating: patch finalizers to `[]`
- ConfigMap/Secret not updating in pod: rolling restart `kubectl rollout restart deploy/<name>`
- Certificate expired: check cert-manager `kubectl get certificate -A`

## Observability stack debugging

The cluster runs Prometheus + Grafana + Tempo + Loki + Alloy in `monitoring` namespace.

### Grafana datasource not connected
1. Check datasource config: `kubectl get configmap kube-prometheus-stack-grafana-datasource -n monitoring -o yaml`
2. Verify target service is running: `kubectl get pods -n monitoring`
3. Test connectivity from Grafana pod: `kubectl exec -it <grafana-pod> -n monitoring -- curl http://loki-gateway.monitoring:80/loki/api/v1/label`
4. For Loki: ensure `X-Scope-OrgId: fake` header is set in datasource config

### Loki not receiving logs
1. Check Loki status: `kubectl get pods -n monitoring -l app.kubernetes.io/name=loki`
2. Verify MinIO is running: `kubectl get pods -n monitoring -l app.kubernetes.io/name=minio`
3. Test push: `kubectl port-forward -n monitoring svc/loki-gateway 3100:80` then `curl -XPOST http://localhost:3100/loki/api/v1/push -H "Content-Type: application/json" -H "X-Scope-OrgId:fake" -d '{"streams":[{"stream":{"job":"test"},"values":[["'$(date +%s)000000000'","test log"]]}]}'`
4. Check Alloy config for Loki output: `kubectl get configmap -n monitoring -l app.kubernetes.io/name=alloy`
5. `loki-chunks-cache-0` Pending is normal — optional cache, not required for operation

### Tempo not receiving traces
1. Check Tempo status: `kubectl get pods -n monitoring -l app.kubernetes.io/name=tempo`
2. Verify Alloy is sending traces: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy | grep tempo`
3. Test query: `kubectl port-forward -n monitoring svc/tempo 3200:3200` then `curl http://localhost:3200/api/search`

### Alloy not forwarding data
1. Check Alloy pods: `kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy`
2. Check Alloy logs: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy`
3. Verify Alloy config: `kubectl get configmap -n monitoring -l app.kubernetes.io/name=alloy -o yaml`

### ArgoCD repo-server CrashLoopBackOff (ARM64 CM4)
1. Check pod events: `kubectl describe pod -n argocd -l app.kubernetes.io/name=argocd-repo-server`
2. Check logs: `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server --tail=50`
3. If liveness probe fails with "context deadline exceeded": probe timeout too low for CM4
4. Fix: set `repoServer.livenessProbe.timeoutSeconds: 5`, `initialDelaySeconds: 30`

## Observability stack debugging

The cluster runs Prometheus + Grafana + Tempo + Loki + Alloy in `monitoring` namespace.

### Grafana datasource not connected
1. Check datasource config: `kubectl get configmap kube-prometheus-stack-grafana-datasource -n monitoring -o yaml`
2. Verify target service is running: `kubectl get pods -n monitoring`
3. Test connectivity from Grafana pod: `kubectl exec -it <grafana-pod> -n monitoring -- curl http://loki-gateway.monitoring:80/loki/api/v1/label`
4. For Loki: ensure `X-Scope-OrgId: fake` header is set in datasource config

### Loki not receiving logs
1. Check Loki status: `kubectl get pods -n monitoring -l app.kubernetes.io/name=loki`
2. Verify MinIO is running: `kubectl get pods -n monitoring -l app.kubernetes.io/name=minio`
3. Test push: `kubectl port-forward -n monitoring svc/loki-gateway 3100:80` then `curl -XPOST http://localhost:3100/loki/api/v1/push -H "Content-Type: application/json" -H "X-Scope-OrgId:fake" -d '{"streams":[{"stream":{"job":"test"},"values":[["'$(date +%s)000000000'","test log"]]}]}'`
4. Check Alloy config for Loki output: `kubectl get configmap -n monitoring -l app.kubernetes.io/name=alloy`
5. `loki-chunks-cache-0` Pending is normal — optional cache, not required for operation

### Tempo not receiving traces
1. Check Tempo status: `kubectl get pods -n monitoring -l app.kubernetes.io/name=tempo`
2. Verify Alloy is sending traces: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy | grep tempo`
3. Test query: `kubectl port-forward -n monitoring svc/tempo 3200:3200` then `curl http://localhost:3200/api/search`

### Alloy not forwarding data
1. Check Alloy pods: `kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy`
2. Check Alloy logs: `kubectl logs -n monitoring -l app.kubernetes.io/name=alloy`
3. Verify Alloy config: `kubectl get configmap -n monitoring -l app.kubernetes.io/name=alloy -o yaml`

### ArgoCD repo-server CrashLoopBackOff (ARM64 CM4)
1. Check pod events: `kubectl describe pod -n argocd -l app.kubernetes.io/name=argocd-repo-server`
2. Check logs: `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server --tail=50`
3. If liveness probe fails with "context deadline exceeded": probe timeout too low for CM4
4. Fix: set `repoServer.livenessProbe.timeoutSeconds: 5`, `initialDelaySeconds: 30`
