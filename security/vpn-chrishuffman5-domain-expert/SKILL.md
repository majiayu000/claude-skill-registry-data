---
name: vpn
description: "Cross-platform comparison and architecture guidance for all VPN technologies: IPsec/IKEv2, WireGuard, SSL VPN, remote access VPN, site-to-site VPN, crypto algorithm selection, and VPN architecture design. Use for \"VPN comparison\", \"VPN architecture\", \"site-to-site VPN\", \"remote access VPN\", \"IPsec vs SSL\", \"VPN selection\", \"crypto algorithms\", \"VPN tunnel\", \"VPN troubleshooting\". Do NOT use for ipsec-, wireguard-, or cisco-secure-client-specific configuration -- use that technology's own skill."
license: MIT
---

# VPN

This skill covers all VPN technologies, providing cross-platform expertise in IPsec/IKEv2, WireGuard, SSL/TLS VPN, remote access architectures, site-to-site design, and cryptographic algorithm selection. Sibling technology skills provide deep implementation details.

## When to Use This Skill vs. a Technology Skill

**Use this skill when the question is cross-platform or architectural:**
- "Which VPN technology should I use for our remote workforce?"
- "Compare IPsec vs WireGuard for site-to-site"
- "Design a VPN architecture for 50 branch offices"
- "What crypto algorithms should I use in 2026?"
- "IPsec vs SSL VPN -- trade-offs?"

**Route to a technology skill when the question is implementation-specific:**
- "Configure IKEv2 tunnel between FortiGate and ASA" --> the `ipsec` skill
- "WireGuard AllowedIPs routing" --> the `wireguard` skill
- "Cisco Secure Client SAML authentication" --> the `cisco-secure-client` skill

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture / Design** -- Load `references/concepts.md` for protocol fundamentals
   - **Technology selection** -- Compare options in the platform comparison below
   - **Algorithm selection** -- Apply CNSA guidance below
   - **Troubleshooting** -- Identify the VPN technology and consult the specific technology skill
   - **Migration** -- Map current to target technology, identify feature gaps

2. **Gather context** -- Use case (site-to-site vs remote access), scale, existing infrastructure, compliance requirements, team expertise, client platform support

3. **Analyze** -- Consider security, performance, operational complexity, and interoperability

4. **Recommend** -- Provide specific guidance with trade-offs

## VPN Technology Comparison

### IPsec / IKEv2

**Strengths:**
- Industry standard with widest interoperability (every enterprise firewall supports it)
- Hardware acceleration on most platforms (FortiASIC, PAN-OS SP, Cisco ASIC)
- Strong crypto flexibility (AES-GCM, SHA-384, ECP-384, PQC transition path)
- Mature protocol suite with RFC standards (RFC 7296, 4303, 3948)
- Route-based VPN (VTI) supports dynamic routing protocols over tunnels

**Considerations:**
- Complex configuration with many knobs (proposals, transforms, DH groups, traffic selectors)
- Interoperability issues between vendors (proposal mismatch is the most common failure)
- Requires UDP/500 and UDP/4500 (or ESP protocol 50) -- can be blocked by restrictive firewalls

**Best for:** Site-to-site VPN between enterprise firewalls, hub-and-spoke with dynamic routing, DMVPN/ADVPN, compliance-driven environments requiring CNSA-grade cryptography.

### WireGuard

**Strengths:**
- Simplest configuration of any VPN technology (~4,000 lines of kernel code)
- Highest performance (kernel-space, ChaCha20-Poly1305, near-wire-speed)
- 1-RTT handshake (<100ms connection establishment)
- Fixed cryptography (no negotiation = no downgrade attacks)
- Built into Linux kernel 5.6+; cross-platform support

**Considerations:**
- No built-in user authentication (key-based only; needs external layer for SSO)
- No built-in key distribution (manual or external orchestration required)
- UDP only (can be blocked; no native TCP fallback)
- No dynamic IP updates without external tooling
- No enterprise management features natively (no centralized management, no logging)

**Best for:** Linux-to-Linux site-to-site, developer/IT team VPNs, container networking (Calico/Flannel), mesh VPN (Tailscale/Headscale/Netmaker), simple road warrior setups.

### Cisco Secure Client (AnyConnect)

**Strengths:**
- Full enterprise remote access platform with VPN + posture + NAC + ZTNA
- DTLS for optimal performance (avoids TCP-over-TCP)
- Deep integration with Cisco ecosystem (ISE, FMC, Umbrella, XDR)
- SAML authentication with system browser (SSO, biometric, hardware tokens)
- DAP (Dynamic Access Policies) for granular per-session access control
- Always-On VPN, split tunneling, per-app VPN (mobile), TND

**Considerations:**
- Requires Cisco headend (ASA or FTD)
- Client software required on endpoints
- Complex licensing model (Advantage, Premier, Secure Access tiers)
- Primarily remote access (not site-to-site)

**Best for:** Enterprise remote access with full endpoint compliance, organizations deep in the Cisco ecosystem, environments requiring per-session dynamic access control.

## Site-to-Site vs Remote Access

| Aspect | Site-to-Site | Remote Access |
|---|---|---|
| Endpoints | Firewall-to-firewall | Client device-to-firewall |
| Protocol | IPsec IKEv2, WireGuard | SSL/DTLS, IPsec IKEv2, WireGuard |
| Routing | Static or dynamic (BGP/OSPF over tunnel) | Full tunnel or split tunnel |
| Authentication | PSK or certificates (device-level) | User credentials + MFA + posture |
| Scale | Hundreds of tunnels per hub | Thousands of concurrent users |
| Topology | Point-to-point, hub-spoke, mesh | Hub-spoke (client to gateway) |

## Crypto Algorithm Selection (2025/2026)

### Current Recommended (CNSA 1.0)
| Component | Algorithm | Notes |
|---|---|---|
| IKE Encryption | AES-256-GCM or AES-256-CBC | GCM preferred (AEAD) |
| IKE Integrity | SHA-384 | With GCM, use explicit PRF instead |
| PRF | PRF_HMAC_SHA2_384 | Required with AEAD encryption |
| DH Group | Group 20 (ECP-384/P-384) | Group 19 (P-256) minimum |
| IPsec Encryption | AES-256-GCM-16 | AEAD, no separate integrity needed |
| IPsec Integrity | SHA-256 or SHA-384 (with CBC) | Not used with GCM |
| PFS | Group 20 (ECP-384) | Always enable PFS on Child SAs |

### Post-Quantum Transition (CNSA 2.0, by 2033)
| Component | Algorithm | Notes |
|---|---|---|
| Key Exchange | ML-KEM-1024 (FIPS 203) | Hybrid: ML-KEM-1024 + ECP-384 during transition |
| Digital Signatures | ML-DSA-87 (FIPS 204) | For certificate authentication |
| Hash/PRF | SHA-384 | Still compliant |

### Avoid
- DH Groups 1, 2, 5, 22, 23, 24 (all weak/broken)
- MD5 or SHA-1 for integrity/PRF
- DES or 3DES encryption
- IKEv1 (disable where possible)

## VPN Architecture Patterns

### Point-to-Point (Site-to-Site)
Two gateways with fixed peer IPs. Route-based (VTI) preferred over policy-based (crypto map).

### Hub-and-Spoke
Central hub with multiple spokes. Spoke-to-spoke traffic traverses hub unless shortcuts configured (DMVPN Phase 3, ADVPN).

### Dynamic Mesh (DMVPN / ADVPN)
- **DMVPN (Cisco)**: mGRE + IPsec + NHRP + dynamic routing. Scales to thousands of spokes.
- **ADVPN (Fortinet)**: IKEv2 extensions for automatic spoke-to-spoke shortcuts.
- Both allow direct spoke-to-spoke tunnels on demand while hub facilitates initial contact.

### Full Mesh
Every site connected to every other site. Scales as O(n^2). Only practical for <10 sites.

## Common Pitfalls

1. **Proposal mismatch**: The most common IPsec failure. Both sides must have at least one overlapping set of encryption, integrity, DH group, and PRF algorithms.
2. **PFS mismatch**: One side requires PFS with specific DH group; other has PFS disabled. Fails silently or with TS_UNACCEPTABLE.
3. **Traffic selector mismatch**: Initiator proposes 10.1.0.0/24 but responder expects 10.0.0.0/8. Check both sides.
4. **NAT-T not enabled**: IPsec fails when NAT device is between peers. Enable NAT-T (UDP/4500) on all configurations.
5. **Clock skew with certificates**: Certificate validation fails if time differs >5 minutes. NTP is critical.
6. **WireGuard key management at scale**: Without orchestration (Tailscale, Netmaker, Ansible), manual key distribution becomes unmanageable beyond ~20 peers.

## Technology Routing

| Request Pattern | Route To |
|---|---|
| IPsec, IKEv2, site-to-site, crypto proposals, DMVPN, VTI | the `ipsec` skill |
| WireGuard, wg-quick, AllowedIPs, Tailscale, Netmaker | the `wireguard` skill |
| Cisco Secure Client, AnyConnect, DTLS, DAP, TND, posture | the `cisco-secure-client` skill |

## Reference Files

- `references/concepts.md` -- IPsec protocol suite, IKEv2 exchange mechanics, ESP, tunnel vs transport mode, crypto algorithms, PFS, DPD, NAT-T. Read for protocol fundamentals.
