---
name: pihole
description: >
  Pi-hole DNS server in Kubernetes: cluster.home wildcard DNS, Cilium LB-IPAM
  LoadBalancer for port 53, local-path PVC storage, and split-DNS for
  workstations (Fedora Silverblue / macOS).
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, pihole, dns, networking, homelab, cilium]
---

# Pi-hole Skill

## Cluster Context

Pi-hole runs inside the K3s cluster as the LAN DNS server.
Its only job: resolve `*.cluster.home → 192.168.178.200` (Cilium Gateway IP).
Everything else is forwarded upstream (8.8.8.8 / 8.8.4.4).

Helm release: `pihole` in namespace `pihole`
Chart: `mojo2600/pihole`
Chart version pinned in: `roles/install-pihole/defaults/main.yml`

Chart version: 2.30.0
Pi-hole app version: 2025.04.0
Cilium LB-IPAM IP: `192.168.178.203` (port 53 UDP+TCP)
Web UI: `https://pihole.cluster.home/admin` (via HTTPRoute on shared Gateway)
Storage: `PersistentVolumeClaim` via `local-path` StorageClass, 2Gi

---

## Architecture

```
Workstation (DNS: 192.168.178.203)
         │
         ▼
   Pi-hole (.203, port 53)
         │
         ├── *.cluster.home → 192.168.178.200  (local override via dnsmasq)
         │
         └── everything else → 8.8.8.8 (upstream)
                                      │
                              Cilium Gateway (.200)
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                  ▼
           argocd.cluster.home  pihole.cluster.home  app.cluster.home
```

---

## Pi-hole vs cert-manager — No Relationship

Pi-hole and cert-manager are **completely independent**. They do not communicate.

- Pi-hole resolves DNS names to IPs
- cert-manager issues TLS certificates
- The Gateway uses both: Pi-hole for name resolution (client-side), cert-manager for TLS

---

## Key Helm Values

```yaml
# roles/install-pihole/defaults/main.yml
pihole_chart_version: "2.30.0"
pihole_namespace: pihole
pihole_dns_ip: "192.168.178.203"   # Cilium LB-IPAM IP for DNS
pihole_storage_size: "2Gi"
pihole_storage_class: "local-path"
```

```yaml
# Helm values (roles/install-pihole/tasks/main.yml)

# DNS: two separate LoadBalancer services (UDP + TCP), sharing same Cilium LB-IPAM IP
# lbipam sharing-key ensures both services get the same IP
# externalTrafficPolicy must be Cluster — L2 Announcements incompatible with Local
serviceDns:
  type: LoadBalancer
  annotations:
    lbipam.cilium.io/ips: "192.168.178.203"
    lbipam.cilium.io/sharing-key: "pihole-dns"
  externalTrafficPolicy: Cluster

serviceDnsTCP:
  type: LoadBalancer
  annotations:
    lbipam.cilium.io/ips: "192.168.178.203"
    lbipam.cilium.io/sharing-key: "pihole-dns"
  externalTrafficPolicy: Cluster

# Web UI: ClusterIP — exposed via HTTPRoute on the shared Gateway
serviceWeb:
  type: ClusterIP
  http:
    enabled: true
    port: 80

persistentVolumeClaim:
  enabled: true
  storageClass: local-path
  size: 2Gi

dnsmasq:
  # Wildcard: *.cluster.home and cluster.home itself → shared Gateway IP
  customDnsEntries:
    - address=/cluster.home/192.168.178.200

# Pi-hole 6.x: set listening mode to ALL so FTL binds port 53 on all interfaces
# listeningMode=LOCAL (default) maps to dnsmasq local-service; setting it via
# customSettings causes a duplicate keyword CRIT crash.
extraEnvVars:
  - name: FTLCONF_dns_listeningMode
    value: "ALL"

# Pi-hole 6.x FTL needs >110s on first boot (loading gravity blocklists)
probes:
  liveness:
    initialDelaySeconds: 120
    failureThreshold: 15
  readiness:
    initialDelaySeconds: 120
    failureThreshold: 15
```

The `address=/cluster.home/192.168.178.200` dnsmasq syntax matches ALL subdomains
of `cluster.home` (wildcard), not just the apex.

---

## Pi-hole 6.x Gotchas

### FTLCONF_dns_listeningMode=ALL (required)

Pi-hole 6.x FTL defaults to `listeningMode=LOCAL`, which maps to dnsmasq's `local-service`
option. If you also set `local-service` in `customSettings`, dnsmasq crashes with:

```
CRIT: Duplicate keyword 'local-service' in configuration file
```

**Fix**: Do NOT add `local-service` to `customSettings`. Instead, override the listening
mode entirely via the env var `FTLCONF_dns_listeningMode=ALL`. This makes FTL bind port 53
on all interfaces and accept queries from external networks (e.g. workstation at .178.x).

### Liveness probe: FTL slow start on first boot

Pi-hole 6.x FTL loads the gravity blocklist database on first boot. On ARM64 with a large
blocklist, this can take >110 seconds before port 80 is ready.

Chart default probes: `initialDelaySeconds: 60` + `failureThreshold: 10` × `periodSeconds: 5`
= 110 seconds max → pod gets killed before ready.

**Fix** (applied in role):
```yaml
probes:
  liveness:
    initialDelaySeconds: 120
    failureThreshold: 15
  readiness:
    initialDelaySeconds: 120
    failureThreshold: 15
```

---

## Workstation DNS

### Fedora Silverblue (primary workstation)

Split-DNS via **systemd-resolved** drop-in. Run on HOST (not toolbox — sudo inside toolbox
writes to container fs, not host).

```bash
# From infra repo on HOST:
bash scripts/setup-dns-split.sh
```

Drop-in created: `/etc/systemd/resolved.conf.d/cluster-home.conf`
```ini
[Resolve]
DNS=192.168.178.203
Domains=~cluster.home
```

This routes only `*.cluster.home` queries to Pi-hole. All other queries use the default resolver.

### Why `.203` works and `.200` does not

`192.168.178.203` is the DNS listener. `192.168.178.200` is only the shared HTTP/HTTPS Gateway.
That means:

- `dig @192.168.178.203 <name>` should answer immediately
- `curl https://<name>.cluster.home` goes to `.200` after DNS resolves
- `arp -n 192.168.178.200` can stay empty if the Gateway has not been announced yet

If DNS times out on `.203`, the issue is L2/LAN reachability for the DNS VIP, not the wildcard record itself.

### macOS

```bash
# Set Pi-hole as DNS for active WiFi interface
networksetup -setdnsservers Wi-Fi 192.168.178.203

# Verify
networksetup -getdnsservers Wi-Fi

# Test
dig argocd.cluster.home @192.168.178.203   # → 192.168.178.200
```

---

## Adding a New Service (Zero Pi-hole Changes Needed)

Because Pi-hole has a **wildcard entry** (`address=/cluster.home/192.168.178.200`),
any new `<service>.cluster.home` hostname resolves automatically without touching Pi-hole.

New service checklist:
1. Deploy service with `ClusterIP` (no LoadBalancer)
2. Create `HTTPRoute` pointing to Gateway `.200` with hostname `<service>.cluster.home`
3. cert-manager issues cert automatically (wildcard `*.cluster.home` covers it)
4. Done — DNS, TLS, and routing all work without manual steps

---

## Upgrade Procedure

1. Update `pihole_chart_version` in `roles/install-pihole/defaults/main.yml`
2. Check release notes: https://github.com/MoJo2600/pihole-kubernetes/releases
3. Re-run:
   ```bash
   ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
     --start-at-task "Add Pi-hole Helm repository"
   ```

---

## Health Checks

```bash
# Pi-hole pods (expect 1/1 Running, RESTARTS=0 or <2 from first boot)
kubectl get pods -n pihole

# DNS services and assigned Cilium LB-IPAM IP
kubectl get svc -n pihole

# Test DNS resolution via Pi-hole
dig argocd.cluster.home @192.168.178.203

# Test wildcard
dig anything.cluster.home @192.168.178.203
# Both should return 192.168.178.200

# Pi-hole query logs (last 20)
kubectl logs -n pihole -l app=pihole --tail=20
```

---

## Troubleshooting

### Pi-hole pod CrashLoopBackOff (first boot)
```bash
kubectl describe pod -n pihole -l app=pihole | grep -E 'initialDelay|failureThreshold|Events'
```
→ If `initialDelaySeconds` is 60 and pod keeps restarting, the probe config is missing.
→ Fix: ensure probes block is in the Helm values (added in role since Pi-hole 6.x).

### Pi-hole not responding on port 53
```bash
# Check services and Cilium LB-IPAM IP assignment
kubectl get svc pihole-dns-tcp pihole-dns-udp -n pihole

# Check Cilium L2 announcement
kubectl get l2announcement -A
kubectl get svc pihole-dns-tcp pihole-dns-udp -n pihole -o wide

# Test from node directly
ssh dalmine@192.168.178.133 'dig argocd.cluster.home @192.168.178.203'
```

If the pod answers queries inside the cluster but the workstation times out, focus on
`arp -n 192.168.178.203`, the `cilium-l2announce-pihole-pihole-dns` lease, and the
host-side neighbor cache, not on Pi-hole's DNS records.

### DNS not resolving from workstation
```bash
# Fedora Silverblue: check resolved config
resolvectl status
# Should show Pi-hole for cluster.home domain

# macOS: check WiFi DNS
networksetup -getdnsservers Wi-Fi

# Test directly (bypass system DNS)
dig cluster.home @192.168.178.203
```

### Host can reach cluster but not Pi-hole VIP
```bash
ip neigh show 192.168.178.203
arp -n 192.168.178.203
sudo ip neigh flush to 192.168.178.203
dig +short argocd.cluster.home @192.168.178.203
```

If Pi-hole works from inside the cluster but the laptop times out, check:
1. The VIP is announced on the right interface family (`en*`, `wl*`, `end*`, `eno*`, `ens*`, `enp*`, `enx*`)
2. The laptop has a stale ARP/neighbor cache entry
3. `systemd-resolved` or NetworkManager is still using another DNS path

### Pi-hole answers inside cluster but laptop times out
```bash
# Check LAN reachability and neighbor cache first
ip neigh show 192.168.178.203
arp -n 192.168.178.203

# Clear stale ARP if needed
sudo ip neigh flush to 192.168.178.203

# Test raw DNS over UDP to the VIP
dig +short argocd.cluster.home @192.168.178.203
```

If the service answers from inside the cluster but the laptop times out, the
usual causes are:
- the Pi-hole VIP is not being announced on the correct host interface
- the host has a stale neighbor entry for `192.168.178.203`
- the workstation DNS path is pointed elsewhere, even if Pi-hole itself is healthy

Troubleshoot in this order:
1. `ip neigh show 192.168.178.203`
2. `arp -n 192.168.178.203`
3. `dig @192.168.178.203 argocd.cluster.home`
4. `kubectl -n kube-system get lease | grep cilium-l2announce`
5. `kubectl get svc pihole-dns-tcp pihole-dns-udp -n pihole -o wide`

### PVC not binding (Pending)
```bash
kubectl get pvc -n pihole
kubectl describe pvc -n pihole
kubectl get storageclass   # must show local-path
```

### Custom DNS entries not working after Pi-hole restart
- Pi-hole persists custom DNS in its SQLite DB via PVC — should survive restarts
- If entries are lost: PVC data was corrupted or PVC was deleted
- Re-run `install-pihole` role to reapply `customDnsEntries` via Helm values

---

## Useful Commands

```bash
# All Pi-hole resources
kubectl get all -n pihole

# Helm values
helm get values pihole -n pihole

# Enter Pi-hole container (for pihole-FTL commands)
kubectl exec -it -n pihole deploy/pihole -- pihole status
kubectl exec -it -n pihole deploy/pihole -- pihole -q argocd.cluster.home

# Check dnsmasq custom config
kubectl exec -it -n pihole deploy/pihole -- cat /etc/dnsmasq.d/02-custom.conf
```
