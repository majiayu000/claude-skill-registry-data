---
name: gateway
description: >
  Cilium Gateway API shared gateway: single entry point for all cluster.home
  HTTP/HTTPS traffic, HTTPRoute and GRPCRoute management, TLS termination,
  ReferenceGrant for cross-namespace routing, and new service onboarding.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, gateway-api, cilium, httproute, tls, ingress, homelab, lb-ipam]
---

# Gateway Skill

## Cluster Context

A single shared `Gateway` resource handles all HTTP/HTTPS ingress for the cluster.
All services use `HTTPRoute` (or `GRPCRoute`) pointing to this Gateway.
TLS is terminated at the Gateway; backends receive plain HTTP internally.

Role: `roles/install-gateway` (raw manifests, no Helm chart)
Gateway namespace: `gateway`
Gateway IP: `192.168.178.200` (fixed via Cilium LB-IPAM annotation)
GatewayClass: `cilium` (managed by Cilium operator)
Domain: `cluster.home`
TLS cert: `cluster-home-wildcard-tls` (wildcard `*.cluster.home`, issued by cert-manager internal CA)

---

## Architecture

```
LAN / Tailscale
      │
      ▼
Cilium Gateway (192.168.178.200)
  port 80  → HTTP  listener (all hostnames)
  port 443 → HTTPS listener (*.cluster.home, TLS terminated here)
      │
      ├── argocd.cluster.home  → HTTPRoute → argocd-server:80   (ns: argocd)
      ├── pihole.cluster.home  → HTTPRoute → pihole-web:80       (ns: pihole)
      └── <svc>.cluster.home  → HTTPRoute → <svc>:<port>        (ns: <ns>)

Pi-hole DNS (.203): wildcard *.cluster.home → .200  (covers all services automatically)
```

One IP. One TLS cert. All HTTP/HTTPS services behind one Gateway.
**Only non-HTTP services** (e.g. Pi-hole DNS port 53) get their own LoadBalancer IP.

### Why `.203` is separate from `.200`

`.200` is the shared Gateway VIP for HTTP/HTTPS. `.203` is Pi-hole's DNS VIP.
DNS must be reachable first so clients can learn `.200`; the Gateway is never used for port 53.
If `dig @192.168.178.203` times out, fix Pi-hole L2 announcement or host ARP first.

---

## Traffic Flow: real examples

### `https://argocd.cluster.home`

```
  Browser
    │
    │  1. DNS query: argocd.cluster.home
    ▼
  Pi-hole (192.168.178.203:53)
  [LoadBalancer — Cilium LB-IPAM: lbipam.cilium.io/ips=.203]
  [Cilium L2 Announce: ARP .203 → node MAC]
    │
    │  responds: 192.168.178.200
    │
    ▼
  192.168.178.200:443
    │
    │  Cilium L2 Announce: ARP .200 → node MAC
    │  Cilium BPF (kube-proxy replacement): DNAT → Envoy
    ▼
  ┌──────────────────────────────────────────────────────┐
  │  Gateway: cluster-gateway  (ns: gateway)             │
  │  Listener: https :443 / *.cluster.home               │
  │  TLS Terminate: Secret cluster-home-wildcard-tls     │
  └─────────────────────┬────────────────────────────────┘
                        │  plain HTTP — Host: argocd.cluster.home
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  HTTPRoute: argocd  (ns: argocd)                     │
  │  parentRef: cluster-gateway                          │
  │  hostname:  argocd.cluster.home                      │
  │  backendRef: argocd-server :80                       │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Service: argocd-server  (ns: argocd)                │
  │  type: ClusterIP                                     │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Pod: argocd-server  (ns: argocd)                    │
  │  server.insecure: true  →  plain HTTP :80            │
  │  (TLS already terminated at Gateway)                 │
  └──────────────────────────────────────────────────────┘
```

### `https://pihole.cluster.home`

```
  Browser
    │
    │  1. DNS query: pihole.cluster.home
    ▼
  Pi-hole (192.168.178.203:53)
  [wildcard: address=/cluster.home/192.168.178.200]
    │
    │  responds: 192.168.178.200
    │
    ▼
  192.168.178.200:443
    │
    │  Cilium BPF: DNAT → Envoy (same path as ArgoCD above)
    ▼
  ┌──────────────────────────────────────────────────────┐
  │  Gateway: cluster-gateway  (ns: gateway)             │
  │  TLS Terminate: Secret cluster-home-wildcard-tls     │
  └─────────────────────┬────────────────────────────────┘
                        │  plain HTTP — Host: pihole.cluster.home
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  HTTPRoute: pihole  (ns: pihole)                     │
  │  backendRef: pihole-web :80                          │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Service: pihole-web  (ns: pihole)                   │
  │  type: ClusterIP                                     │
  └─────────────────────┬────────────────────────────────┘
                        ▼
  ┌──────────────────────────────────────────────────────┐
  │  Pod: pihole  (ns: pihole)                           │
  │  Pi-hole FTL + lighttpd :80                          │
  │  PVC: /etc/pihole  (local-path-provisioner)          │
  │                                                      │
  │  NOTE: same pod also handles DNS on .203:53          │
  │  via separate LoadBalancer services (pihole-dns-tcp  │
  │  and pihole-dns-udp) — completely separate path      │
  └──────────────────────────────────────────────────────┘
```

### Key difference between the two

| | ArgoCD | Pi-hole web UI |
|---|---|---|
| Service | `argocd-server` ClusterIP | `pihole-web` ClusterIP |
| HTTPRoute ns | `argocd` | `pihole` |
| Backend config | `server.insecure: true` | plain lighttpd HTTP |
| Extra LB | none | yes — `pihole-dns-tcp/udp` at `.203:53` (separate, non-HTTP) |

The Gateway is the single entry point for both. Only the HTTPRoute differs.

---

## IP Assignment Strategy

| IP | Service | Protocol | LB type |
|----|---------|----------|---------|
| `.200` | Cilium shared Gateway | HTTP/HTTPS | LoadBalancer — `lbipam.cilium.io/ips=.200` |
| `.203` | Pi-hole DNS port 53 | DNS UDP+TCP | LoadBalancer — `lbipam.cilium.io/ips=.203` + `sharing-key` |
| `.204+` | Future non-HTTP services | varies | LoadBalancer as needed |

**Rule: HTTP/HTTPS services → HTTPRoute via Gateway at `.200`.**
Only non-HTTP protocols (DNS, MQTT, custom TCP, etc.) get their own LoadBalancer IP.
Every new HTTP service costs zero new IPs — just an HTTPRoute.

---

## Gateway Resource

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: cluster-gateway
  namespace: gateway
  annotations:
    lbipam.cilium.io/ips: "192.168.178.200"   # Cilium LB-IPAM pins this IP
spec:
  gatewayClassName: cilium
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
    - name: https
      protocol: HTTPS
      port: 443
      hostname: "*.cluster.home"
      tls:
        mode: Terminate
        certificateRefs:
          - name: cluster-home-wildcard-tls
            namespace: gateway
      allowedRoutes:
        namespaces:
          from: All
```

`allowedRoutes.namespaces.from: All` — HTTPRoutes from any namespace attach to this Gateway.
This is correct for a shared cluster gateway. No `ReferenceGrant` needed for this direction.

---

## Adding a New Service — Step by Step

No changes to Pi-hole, cert-manager, or the Gateway are needed.
The wildcard DNS and wildcard TLS cert cover all `*.cluster.home` subdomains automatically.

### 1. Deploy the service with ClusterIP

```yaml
service:
  type: ClusterIP   # never LoadBalancer for HTTP/HTTPS services
  port: 80
```

### 2. Create an HTTPRoute in the service's namespace

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-service
  namespace: my-service-ns
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
  hostnames:
    - "my-service.cluster.home"
  rules:
    - backendRefs:
        - name: my-service
          port: 80
```

### 3. That's it

- Pi-hole wildcard already resolves `my-service.cluster.home → .200`
- cert-manager wildcard cert already covers `*.cluster.home`
- Gateway routes by `Host` header to the correct HTTPRoute

---

## Non-HTTP services: own LoadBalancer

For services that cannot go through the HTTP Gateway (port 53, MQTT, raw TCP, etc.):

```yaml
# Pin a specific IP from the Cilium LB-IPAM pool:
metadata:
  annotations:
    lbipam.cilium.io/ips: "192.168.178.203"

# Share one IP between TCP and UDP services (same port):
metadata:
  annotations:
    lbipam.cilium.io/ips: "192.168.178.203"
    lbipam.cilium.io/sharing-key: "my-service-dns"

# Always Cluster, never Local (L2 Announcements requirement):
spec:
  externalTrafficPolicy: Cluster
```

---

## TLS — how it works end to end

```
cert-manager
  └── SelfSigned ClusterIssuer
        └── root CA Certificate  (cluster.home Root CA)
              └── CA ClusterIssuer
                    └── Certificate *.cluster.home
                          └── Secret: cluster-home-wildcard-tls  (ns: gateway)
                                └── Gateway listener: https  (references the secret)
                                      └── TLS terminated here — backends get plain HTTP
```

The CA cert is exported to `/tmp/cluster-home-ca.crt` by the `install-cert-manager` role.
Import it into macOS Keychain once to trust all `*.cluster.home` certs in the browser:

```bash
security add-trusted-cert -d -r trustRoot \
  -k ~/Library/Keychains/login.keychain-db /tmp/cluster-home-ca.crt
```

---

## ArgoCD specifics

ArgoCD server must run in insecure mode — the Gateway terminates TLS:

```yaml
# Helm values:
configs:
  params:
    server.insecure: "true"

server:
  service:
    type: ClusterIP
```

`BackendTLSPolicy` (mTLS between Gateway and ArgoCD) is **not supported by Cilium**.
Do not enable it. `server.insecure: true` + Gateway TLS termination is correct.

---

## Health Checks

```bash
# Gateway status — both listeners should be Programmed: True
kubectl get gateway -n gateway cluster-gateway
kubectl get gateway -n gateway cluster-gateway -o yaml | grep -A5 "conditions:"

# All HTTPRoutes and their parent attachment status
kubectl get httproute -A

# GatewayClass (should be Accepted: True)
kubectl get gatewayclass cilium

# Verify IP assigned by LB-IPAM
kubectl get svc -n gateway

# Test HTTPS (requires CA in macOS Keychain)
curl -v https://argocd.cluster.home
curl -v https://pihole.cluster.home/admin

# Test HTTP (should work too — no redirect configured by default)
curl -v http://argocd.cluster.home

# Verify TLS cert is correct
echo | openssl s_client -connect argocd.cluster.home:443 -servername argocd.cluster.home \
  2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

---

## Troubleshooting

### Gateway stuck `Programmed: False`
```bash
kubectl describe gateway cluster-gateway -n gateway
kubectl logs -n kube-system -l io.cilium/app=operator --tail=50
```

### HTTPRoute not routing (404 or wrong backend)
```bash
kubectl describe httproute <name> -n <namespace>
# Check: parentRef name/namespace matches, sectionName if set, backend service/port exist

kubectl get svc <backend-svc> -n <namespace>
```

### Gateway has no EXTERNAL-IP (stuck pending)
```bash
# Check LB-IPAM pool exists and has free IPs
kubectl get ciliumloadbalancerippools

# Check lbipam annotation on the Gateway's generated Service
kubectl get svc -n gateway
kubectl describe svc -n gateway

# Check L2 Announcement lease (node holding ARP for .200)
kubectl -n kube-system get lease | grep cilium-l2announce
```

### ARP not resolving for .200
```bash
arp -n 192.168.178.200
# If "(incomplete)": check L2 announcement lease and Cilium L2 policy
kubectl get ciliuml2announcementpolicy
kubectl logs -n kube-system -l k8s-app=cilium --tail=50 | grep -i l2
```

### TLS cert warning in browser
```bash
# Check Certificate is Ready
kubectl get certificate -n gateway

# Check Secret exists
kubectl get secret cluster-home-wildcard-tls -n gateway

# Check CA is trusted on Mac
security find-certificate -c "cluster.home Root CA"

# Verify cert SAN
echo | openssl s_client -connect argocd.cluster.home:443 2>/dev/null \
  | openssl x509 -noout -text | grep -A1 "Subject Alternative"
```

---

## Useful Commands

```bash
# Full Gateway spec + status
kubectl get gateway -n gateway cluster-gateway -o yaml

# All routes with parent attachment status
kubectl get httproute,grpcroute -A -o wide

# Cilium Gateway/Envoy controller logs
kubectl logs -n kube-system -l io.cilium/app=operator -f

# Test a specific route bypassing DNS
curl -H "Host: argocd.cluster.home" https://192.168.178.200 -k

# Check what IP Cilium assigned to the Gateway Service
kubectl get svc -n gateway -o wide
```

---

## Workstation DNS Setup (Fedora Silverblue / Sericea)

> **Platform-specific**: Fedora Silverblue uses `systemd-resolved` as DNS resolver
> (NM default, no `dns=` override in NetworkManager.conf). Split-DNS is configured
> via a `systemd-resolved` drop-in — survives reboots and rpm-ostree upgrades.
>
> **Important**: commands must be run on the **host OS**, not inside a toolbox container.
> `sudo` inside toolbox writes to the container filesystem, not the host.

### How cluster.home DNS works end-to-end

```
Workstation (host)
  │  *.cluster.home → systemd-resolved (split-DNS routing domain)
  │
  ▼
Pi-hole @ 192.168.178.203       ← wildcard: *.cluster.home → 192.168.178.200
  │
  ▼
Cilium Gateway @ 192.168.178.200  ← L2 announced, single LoadBalancer IP
  │
  ▼
Cilium Envoy (Gateway API)       ← routes by Host header via HTTPRoutes
  │
  ▼
ClusterIP services (argocd, grafana, pihole-ui, …)
```

Key points:
- Pi-hole answers `*.cluster.home` with `192.168.178.200` (the shared Gateway IP).
- The Gateway uses the `Host:` header to route to the correct backend.
- cert-manager issues a wildcard TLS cert for `*.cluster.home` — browsers trust it if
  you import the internal CA (see TLS section above).
- **No entries needed in `/etc/hosts`** — Pi-hole covers everything via wildcard.

### Verify your DNS stack first (host terminal)

```bash
# Confirm systemd-resolved is active (expected on Fedora Silverblue)
systemctl is-active systemd-resolved           # → active

# Confirm NM is NOT overriding DNS (should return empty)
grep dns /etc/NetworkManager/NetworkManager.conf
```

If `dns=systemd-resolved` or empty → use the drop-in approach below.
If `dns=dnsmasq` → use NM dnsmasq approach instead (different setup).

### Configure split-DNS via systemd-resolved drop-in (run on HOST)

```bash
sudo mkdir -p /etc/systemd/resolved.conf.d
sudo tee /etc/systemd/resolved.conf.d/cluster-home.conf <<'EOF'
[Resolve]
DNS=192.168.178.203
Domains=~cluster.home
EOF
sudo systemctl restart systemd-resolved
```

`~cluster.home` is a **routing domain**: only `*.cluster.home` queries go to Pi-hole,
all other DNS traffic uses your normal upstream DNS.

### Verify

```bash
# Check the routing domain is registered
resolvectl status | grep -A5 "cluster.home"

# Should resolve to 192.168.178.200
dig +short grafana.cluster.home
dig +short argocd.cluster.home

# Internet must still work
dig +short google.com
```

### Trust the internal CA (optional but recommended)

Importing the CA lets your browser treat `https://*.cluster.home` as fully trusted.

```bash
# Copy the CA cert from the cluster (run inside toolbox or with kubectl in PATH)
kubectl get secret -n cert-manager cluster-home-ca \
  -o jsonpath='{.data.tls\.crt}' | base64 -d > /tmp/cluster-home-ca.crt

# Import into the system NSS trust store (Silverblue / Fedora)
sudo cp /tmp/cluster-home-ca.crt /etc/pki/ca-trust/source/anchors/cluster-home-ca.crt
sudo update-ca-trust

# Restart Firefox after update-ca-trust (it reads from system store on Fedora)
```

### Toolbox note

Commands above must run on the **host** (outside toolbox). Inside a toolbox:
- `sudo` writes to the container filesystem — changes don't affect the host
- DNS resolution inherits from the host via `/run/host/etc/resolv.conf` symlink
- Once split-DNS is configured on the host, it works inside toolbox automatically

```bash
# Toolbox shares host network — once host DNS is set, this works inside toolbox too
dig +short grafana.cluster.home   # resolves after host config is done
```

### Script (recommended)

```bash
# Run from the infra repo on the HOST (not inside toolbox)
bash ~/Nextcloud/Repos/infra-ai/infra/scripts/setup-dns-split.sh
```

The script guards against running inside toolbox, restarts systemd-resolved,
and verifies resolution automatically.

### Recommendation

**Always configure split-DNS on the host before accessing `*.cluster.home`.**
The one-time setup above is persistent across reboots and rpm-ostree upgrades.

### Important L2 note

If `cluster.home` resolves but HTTPS returns `No route to host`, check the
Cilium L2 announcement selector. New nodes may expose `end1` or other `en*`
interface names instead of `eth*`, and the Gateway VIP is only announced on
interfaces matched by `CiliumL2AnnouncementPolicy`.
