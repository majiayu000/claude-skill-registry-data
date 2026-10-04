---
name: pki
description: "Routing agent for PKI and Certificate Lifecycle Management. Delegates to Let's Encrypt, Venafi, DigiCert, cert-manager, EJBCA, and smallstep specialists. Handles PKI design, CA hierarchy, X.509 concepts, ACME protocol, and certificate automation strategy. WHEN: \"PKI\", \"certificate authority\", \"CA hierarchy\", \"TLS certificate\", \"certificate lifecycle\", \"ACME\", \"X.509\", \"certificate rotation\", \"certificate renewal\", \"CLM\", \"machine identity\". Do NOT use for vendor-specific questions -- use the `lets-encrypt`, `venafi`, `digicert`, `cert-manager`, `ejbca`, or `smallstep` skill."
license: MIT
---

# PKI & Certificate Lifecycle Management

This skill covers PKI and Certificate Management. It classifies requests, points to technology-specific sibling skills, and answers cross-cutting questions about certificate strategy, CA design, and lifecycle management.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Tool-specific** — Read the matching sibling skill
   - **CA hierarchy design** — Answer here with `references/concepts.md`
   - **Certificate strategy** — Answer here (public vs. private CA, short-lived vs. long-lived)
   - **ACME protocol** — Load `references/concepts.md`
   - **Compliance/regulatory** — Answer here with CA requirements by framework
   - **Migration** — Identify source and target, read both sibling skills

2. **Load context** — For foundational questions, read `references/concepts.md`

3. **Identify technology** — See routing table below

## Technology Routing Table

| If the request involves... | Delegate to |
|---|---|
| Let's Encrypt, ACME automation, certbot, acme.sh | `lets-encrypt` |
| Venafi, TLS Protect, CodeSign Protect, CyberArk Machine Identity | `venafi` |
| DigiCert, CertCentral, Trust Lifecycle Manager, DigiCert ONE | `digicert` |
| cert-manager, Kubernetes certificates, Issuers, ClusterIssuers | `cert-manager` |
| EJBCA, Keyfactor, enterprise CA, ACME/EST/SCEP/CMP protocols | `ejbca` |
| smallstep, step-ca, step CLI, internal PKI, SSH certificates | `smallstep` |

## Certificate Strategy

### When to Use a Public CA

Use a publicly-trusted CA (Let's Encrypt, DigiCert, etc.) for:
- Any certificate that must be trusted by browsers, mobile devices, or external clients
- Customer-facing APIs and web applications
- External integrations where you cannot control the trust store

### When to Use a Private/Internal CA

Use a private CA (Vault PKI, EJBCA, smallstep, internal AD CS) for:
- Internal service-to-service TLS
- mTLS client certificates
- Developer/staging environments
- Short-lived certificates for CI/CD
- SSH host certificates and user certificates

### Short-Lived vs. Long-Lived Certificates

| Dimension | Long-Lived (1 year) | Short-Lived (≤24h) |
|---|---|---|
| Revocation needed? | Yes (CRL/OCSP required) | No (expiry is revocation) |
| Automation required? | Recommended | Mandatory |
| Risk on key compromise | High (valid until expiry) | Low (expires soon anyway) |
| Operational complexity | Lower (less frequent renewal) | Higher (constant renewal) |
| Emerging industry direction | Declining (Let's Encrypt moving to 6-day) | Growing |

The industry is moving toward short-lived certificates. Let's Encrypt launched 6-day certificates in March 2025 as an opt-in, with 45-day certificates as an opt-in from May 2026.

### CA Hierarchy Design

#### Public-Facing Services

```
External Root CA (DigiCert, Let's Encrypt, etc.)
  └── Their Intermediate CA (managed by CA)
        └── Your TLS certificates (90 days, automated)
```

Use ACME for automation. No intermediate CA management needed.

#### Internal Services

```
Offline Root CA (self-generated, air-gapped)
  └── Online Intermediate CA (Vault PKI, EJBCA, step-ca)
        ├── TLS server certificates (24-72h for mTLS, 30-90d for internal TLS)
        ├── mTLS client certificates (short-lived)
        └── SSH host/user certificates (short-lived)
```

Keep the Root CA offline. If the online intermediate is compromised, revoke the intermediate cert from the root (offline), re-issue a new intermediate.

#### Enterprise / Regulated

```
Internal Root CA (HSM-backed, air-gapped)
  ├── Issuing CA for Infrastructure (Vault PKI / EJBCA / AD CS)
  │     ├── Server TLS
  │     └── mTLS client certs
  ├── Issuing CA for Code Signing (air-gapped)
  │     └── Code signing certificates
  └── Issuing CA for Email (S/MIME)
        └── User email certificates
```

## Certificate Automation Approaches

### ACME (Automated Certificate Management Environment)

ACME (RFC 8555) is the standard for automated certificate issuance and renewal. Supported by:
- Let's Encrypt (free, public)
- ZeroSSL (free, public)
- Google Trust Services (free, public)
- Vault PKI engine (internal)
- EJBCA (internal)
- step-ca (internal)
- DigiCert, Sectigo (paid, ACME support)

ACME clients:
- **certbot** — The reference implementation, widely supported
- **acme.sh** — Bash-based, lightweight, broad DNS provider support
- **cert-manager** — Kubernetes-native, integrates with ACME
- **Caddy** — Built-in ACME, automatic HTTPS
- **Traefik** — Built-in ACME
- **step CLI** — CLI with built-in ACME client

### cert-manager (Kubernetes)

The standard for certificate management in Kubernetes. Supports multiple issuers:
- ACME (Let's Encrypt, ZeroSSL)
- Vault PKI
- Venafi
- AWS Private CA
- Self-signed
- Custom CA

See `cert-manager` for complete guidance.

### Venafi / DigiCert TLM (Enterprise CLM)

For large enterprises requiring:
- Visibility across all certificates (discovery)
- Policy enforcement (no weak keys, expiry limits)
- Workflow approvals
- Multi-CA support
- Compliance reporting

## Certificate Discovery and Inventory

Before automating, discover your existing certificate estate:

**Methods**:
- **CT log scanning**: `crt.sh`, Censys, Shodan for internet-facing certs
- **Network scanning**: Nmap/Masscan with TLS negotiation, Qualys SSL Labs
- **Active Directory**: AD CS enrollment records
- **Venafi/DigiCert TLM**: Continuous discovery agents

**Why it matters**: Organizations typically have 2-5x more certificates than they track. Undiscovered expiring certs cause outages.

## Compliance Requirements

### PCI-DSS

- Minimum TLS 1.2 for cardholder data transmission
- 2048-bit RSA or 256-bit EC minimum
- Certificate expiry monitoring required
- No expired or self-signed certs for external services

### FIPS 140-3

- RSA 2048/3072/4096 with SHA-2
- ECDSA P-256/P-384/P-521
- No MD5, SHA-1, or RSA-1024

### CA/Browser Forum (Public CAs)

- Maximum 398 days for publicly-trusted TLS certificates (enforced since 2020)
- SAN required (CN deprecated for hostname)
- CAA DNS records checked at issuance
- CT log submission required
- OCSP stapling recommended
- Moving toward 90-day maximum (2024 ballot), and Apple/Google pushing shorter

### US Federal / FedRAMP

- FIPS 140-3 Level 1+ for software, Level 3 for HSM
- Common Access Card (CAC) / PIV compliance for user certs
- Certificate Policy (CP) and Certification Practice Statement (CPS) required
- Federal PKI bridge cross-certification for some use cases

## Reference Files

- `references/concepts.md` — PKI fundamentals: X.509 certificate structure, certificate chains, CRL/OCSP, CT logs, ACME protocol detail, challenge types, rate limits. Load for foundational questions.
