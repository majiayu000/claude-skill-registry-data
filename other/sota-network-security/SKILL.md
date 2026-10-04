---
name: sota-network-security
description: >-
  State-of-the-art network security as a discipline (2026) for BOTH
  designing/building secure networks AND auditing segmentation and exposure.
  Use for zero-trust architecture, network segmentation and blast-radius
  control, Kubernetes NetworkPolicy/CiliumNetworkPolicy depth, service mesh
  and mTLS, edge/ingress/egress security (WAF, egress allowlisting,
  metadata-endpoint blocking), DNS/TLS/PKI transport and certificate
  lifecycle, and remote access (WireGuard, ZTNA, bastion vs identity-aware
  proxy). Triggers — network security, zero trust, ZTNA, microsegmentation,
  east-west traffic, lateral movement, NetworkPolicy, default-deny, Cilium,
  Hubble, service mesh, mTLS, Istio, Linkerd, SPIFFE, ingress, egress, WAF,
  CRS, Coraza, egress gateway, FQDN allowlist, IMDS, DNS firewall, DNSSEC,
  DoH, TLS 1.3, ACME, step-ca, private CA, bastion, identity-aware proxy,
  DDoS, email spoofing, SPF, DKIM, DMARC. Owns SECURITY posture on
  top of cloud network setup (sota-cloud-infrastructure owns VPC/subnet/DNS
  setup).
---

# SOTA Network Security

## Purpose

This skill encodes the 2026 state of the art for **network security as a discipline**: how to
verify rather than trust, contain blast radius, encrypt traffic in motion, control what enters and
leaves, and secure the naming and transport plumbing (DNS, TLS, PKI). Every rule exists to prevent a
real failure class — lateral movement after one foothold, plaintext credentials on the wire, an
over-broad rule that exposes a secrets store to the world, a renewal nobody automated, or an SSRF
that reaches the cloud metadata endpoint.

**Ownership — reference siblings, do not duplicate:**
- **sota-cloud-infrastructure** (rules/03 networking) owns cloud-provider network *setup*: VPC/subnet
  layout, CIDR/IPAM, route tables, LB/CDN provisioning, registrar hygiene, DNS zone setup. **This
  skill owns the security posture layered on top** and the on-prem / Kubernetes / mesh side.
- **sota-kubernetes** owns admission control and RBAC — *where NetworkPolicy is admitted and CNI
  enforcement is wired*; this skill owns the policy *content and depth*.
- **sota-identity-access** owns SPIFFE/SPIRE workload identity issuance, ZTNA user identity, and the
  identity-aware proxy's auth plane; this skill consumes those identities for network authorization.
- **sota-detection-engineering** owns network IDS (Suricata), DNS-exfil detection, and flow-log
  detection content; this skill produces the telemetry (Hubble flows, flow logs) it consumes.
- **sota-sandboxing** (rules/02–03) owns single-host nftables/seccomp and container hardening; this
  skill owns the inter-host / cluster-wide fabric.
- **sota-code-security** (rules/01 SSRF, rules/05 CORS/CSP), **sota-api-design** (rules/07 rate
  limiting), **sota-secrets-management** (TLS private keys) — referenced where they intersect.

## BUILD mode

Use when designing or extending a secure network (zero-trust plan, NetworkPolicy set, mesh rollout,
ingress/egress controls, PKI/DNS posture, remote access).

1. **Establish context first:** on-prem vs cloud vs hybrid; CNI and orchestrator (e.g.
   an on-prem cluster with an eBPF CNI such as Cilium); existing PKI (e.g. a private CA such as
   step-ca), edge (e.g. a reverse proxy with a CRS WAF behind a CDN);
   data sensitivity; who needs remote access. A 3-node homelab and a regulated fleet get different
   answers from the same rules.
2. **Read the matching rules file before writing config.** Segmentation (rules/02) precedes policy
   detail; identity-aware access (rules/01) frames everything.
3. **Default-deny in both directions, always.** Ingress *and* egress deny by default, per namespace
   and per zone. Every allow is explicit, justified in a comment, and references identity (workload
   identity, label selector, SG/service account) — never a bare CIDR or `world` entity **wherever the
   policy language can express identity**. Where it genuinely cannot — vanilla NetworkPolicy has no
   identity selector for a destination *outside* the cluster — a tight `ipBlock` is a **documented
   exception, not a default**: name the destination and the reason, and prefer a CNI that can
   (rules/03 §3). Inside the cluster there is no exception: pod IPs are recycled, so a CIDR there
   silently re-points the allow.
4. **Encrypt every hop that crosses a trust boundary.** No plaintext credentials, JWTs, or DB
   traffic on the pod/internal network — mTLS via mesh or TLS terminated close to the workload.
5. **State the failure mode and the blast radius** of what you propose. "If this pod is popped, it
   can reach X and Y" belongs in the design, not the postmortem.
6. **Produce policy as code** (NetworkPolicy/CiliumNetworkPolicy YAML, mesh AuthorizationPolicy,
   nftables, ACME/cert-manager manifests) — never click-ops, never "we'll lock it down later."

## AUDIT mode

Use when reviewing an existing network for segmentation gaps and exposure.

Process: inventory the fabric (zones, namespaces, CNI policies, mesh config, ingress/egress paths,
DNS zones, certs, remote-access entry points); walk the Audit checklist at the end of each relevant
rules file; **confirm reachability before reporting** — render the effective policy, run a probe
(`kubectl exec ... curl`, Hubble flow query, `nmap`), read the actual rule. Do not infer exposure
from a resource name.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **Critical** | External or any-workload party can reach a sensitive service or read traffic now | Secrets store / DB / registry reachable from a `world`/`0.0.0.0/0` entity; plaintext DB creds or JWTs on the wire (sniffable from any pod); SSH open to the internet on a prod host; admin/dashboard reachable unauthenticated from outside |
| **High** | One foothold from broad lateral movement, or a guaranteed exposure/outage class | "Default-deny" that actually allows all intra-cluster traffic; no egress control (free C2/exfil path); flat L2/L3 network with no segmentation; manual cert renewal on a public endpoint; mTLS in `PERMISSIVE` everywhere with plaintext still flowing |
| **Medium** | Weakens containment, transport security, or recovery | Ingress-only default-deny (egress still open); CIDR-based internal rules that rot on re-IP; TLS 1.0/1.1 or weak ciphers allowed; no FQDN egress filtering where it's warranted; WAF in detection-only mode; no Hubble/flow visibility |
| **Low** | Hygiene, drift, headroom | Inconsistent policy labels; over-scoped but internal-only allow; missing HSTS; no CAA record; DNSSEC undecided |
| **Info** | Context for the reader, no action implied | Mesh is overkill for a 2-service app (just use TLS); ANP/BANP still alpha — pin behavior |

Severity = reachability (anonymous internet > any-workload east-west > same-namespace > insider)
× impact (traffic read / sensitive-service compromise > lateral movement > availability).

### Finding format

```
file:line | rule | severity | effort | fix
```

- **file:line** — the policy/manifest/config and line (e.g. `netpol/baseline.yaml:14`,
  `Caddyfile:30`); for runtime-only findings name the resource (`ns/payments | cilium effective`).
- **rule** — the rules-file rule id (e.g. `rules/03 R4` or `R-egress-default-deny`).
- **severity** — Critical / High / Medium / Low / Info.
- **effort** — trivial / small / medium / large (eng effort to fix).
- **fix** — the specific change (the policy diff, the directive, the mesh stanza).

Group repeated instances (e.g. 12 namespaces with no egress policy) into one finding with a count.

## Rules index

| File | Read this when... |
|---|---|
| rules/01-zero-trust-architecture.md | Establishing/auditing the model: never-trust-always-verify, PDP/PEP, identity-aware access over network location, ZTNA vs VPN, de-perimeterization, identity-aware proxy (BeyondCorp), telemetry-to-policy pruning loop, devices pillar (inventory, device certificates, posture-gated access, unmanaged-device isolation) |
| rules/02-segmentation-blast-radius.md | Designing/auditing zones and tiers, north-south vs east-west, the flat-network and over-broad-rule (`any`/`0.0.0.0/0`/`world`) traps, microsegmentation, lateral-movement containment, firewall/SG default-deny, remote access (WireGuard, bastion vs IAP), zone refinements (outbound-only DMZ, directory/log segments, shared-L7-balancer caveat, human-readable policy), legacy/plaintext quarantine zone, external exposure discovery |
| rules/03-k8s-network-policy.md | Writing/auditing Kubernetes NetworkPolicy, CiliumNetworkPolicy, the namespaced default-deny (ingress AND egress) pattern, the "default-deny that isn't" trap, ANP/BANP, L7/identity policy, DNS-aware egress, egress gateways, Hubble visibility, permitted-vs-observed policy pruning |
| rules/04-service-mesh-mtls.md | The plaintext-internal-traffic problem, choosing/auditing a mesh (Istio sidecar vs ambient, Linkerd, Cilium mesh), mTLS everywhere, mesh authorization policy, SPIFFE identity, peer-identity pinning for cross-org mTLS (SAN/SPKI, never CN), mTLS-mode drift alerting, and deciding mesh vs plain TLS |
| rules/05-edge-ingress-egress.md | WAF (CRS/Coraza) incl. virtual-patching lifecycle, rule-firing reports, WAF events to SIEM, positive model and WebSocket limits, ingress/API-gateway hardening, trace/diagnostic header scrubbing, request smuggling / proxy-chain desync (strict parsers, h2 downgrade, h2c), TLS termination + re-encryption, trusted-IP handling behind Cloudflare, DDoS posture (edge scrubbing + self-hosted kernel hardening: SYN cookies/synproxy, conntrack, rp_filter, no open UDP reflectors; byte caps and uplink capacity), egress as a first-class control, FQDN allowlisting, blocking the metadata endpoint, the SSRF-meets-egress chain |
| rules/06-dns-tls-pki.md | DNS security (DNSSEC, RPZ/DNS firewall, DoH/DoT, split-horizon, CAA, tunneling, subdomain takeover: dangling CNAME/NS/MX/SPF, wildcard records, takeover indicators + response), TLS posture (1.3, ciphers, HSTS, OCSP, full chain, explicit hybrid-PQ group list, ECH, legacy-client isolation), certificate issuance hygiene (SANs, no internal names, SHA-256, shared-cert inventory), shrinking cert lifetimes + ACME automation, internal PKI (step-ca), short-lived certs, pinning tradeoffs, email authentication & anti-spoofing (SPF/DKIM/DMARC, MTA-STS/DANE, bulk-sender rules) |

Cross-cutting tasks read multiple files: a full network audit touches all six; "lock down our
cluster" is rules/02 + rules/03 (+ rules/04 if a mesh exists).

## Top 10 non-negotiables

1. **Verify, don't locate-trust.** Access decisions bind to authenticated identity (workload or
   user) and posture, not to "it's on the internal network." A packet's source subnet is not a
   credential. (NIST SP 800-207; CISA ZTMM v2.0.)
2. **Default-deny in BOTH directions.** Every namespace/zone denies ingress *and* egress by default;
   allows are explicit and identity-scoped. An ingress-only default-deny leaves the exfil door open.
3. **No `any` / `0.0.0.0/0` / `world` to sensitive services.** A secrets store, DB, registry, or
   admin UI reachable from a broad entity is a Critical finding — render the effective rule and
   prove the path, don't trust the rule's name.
4. **The "default-deny" must actually deny.** A baseline policy that allows all intra-cluster
   traffic is not default-deny; verify with a probe (cross-namespace `curl` should fail).
5. **Encrypt internal traffic.** DB creds, JWTs, and app traffic crossing the pod/host network ride
   mTLS or TLS — never plaintext `ws://`/`http://`/unencrypted DB protocol. Mesh in `STRICT`, not
   permissive-forever.
6. **Egress is a control, not a default-open pipe.** Default-deny egress, FQDN/IP allowlists, egress
   gateways/proxies for sensitive zones; block the cloud metadata endpoint (169.254.169.254,
   fd00:ec2::254) at the pod/host. This is the C2/exfil and SSRF-pivot chokepoint.
7. **Microsegment east-west.** Contain blast radius so one popped workload can reach only its
   declared dependencies. Flat networks turn a single foothold into a cluster-wide incident.
8. **Identity-aware access for humans.** ZTNA / identity-aware proxy (per-request identity + device
   posture) over flat VPN access; if VPN, WireGuard with per-peer keys, never SSH open to the world.
9. **Certs are automated and short-lived.** Every cert (public and internal) is ACME/cert-manager
   issued and auto-renewed. CA/Browser Forum caps public certs at 200 days (2026-03-15) → 47 days
   (2029-03-15); manual renewal is now an outage generator.
10. **Flows are visible.** You can answer "who talked to whom" — Hubble / flow logs / mesh telemetry
    on, exported to detection (sota-detection-engineering). You cannot secure traffic you can't see.

## Operating notes

- Principles first, then the reader's actual stack once it is known; until then, name the
  alternatives rather than assuming one.
- **Verify versions and API status against current docs before committing them** — CNI features,
  mesh GA status, the ANP/BANP/ClusterNetworkPolicy API state, CRS version, and the CA/B cert
  schedule all move faster than this text. Be version-agnostic where a claim is unpinnable.
- When this skill and a compliance mapping conflict, state both; do not silently relax a control.
