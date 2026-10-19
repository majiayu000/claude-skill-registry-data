---
name: threat-modeling
description: >
  Identify architectural security risks, map trust boundaries, and evaluate attack
  paths using STRIDE and risk assessment frameworks. Use when designing new system
  architectures, conducting security design reviews, identifying attacker entry
  points, analyzing threat vectors, or prioritizing defensive mitigations.
compatibility: >
  Agent Skills-compatible coding agents analyzing software architectures and security designs.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "threat-modeling, stride, security, risk-assessment, architecture, attack-trees"
  topics: "security, software-development, architecture"
---

# Architectural Threat Modeling (STRIDE)

Threat modeling is an engineering practice that identifies potential security vulnerabilities and attack paths early in the design phase. By systematically analyzing architecture diagrams, data flows, and trust boundaries against the **STRIDE** framework, teams eliminate architectural flaws before writing code.

## Core Rules

1. **Model what you build, not an abstract ideal**: Base threat models on real architectural components (data stores, processes, networks, third-party APIs).
2. **Identify Trust Boundaries explicitly**: Mark everywhere data crosses between networks (public internet vs private VPC), processes (root vs unprivileged daemon), or tenants.
3. **Assume attacker capabilities realistically**: Consider both external unauthenticated attackers and compromised internal accounts/tenants.
4. **Use STRIDE for exhaustive coverage**: Evaluate every component against all six threat categories.
5. **Prioritize mitigations by risk**: Focus engineering effort on high-impact, easily exploitable threats first.

---

## 1. The STRIDE Threat Classification

| Threat | Security Property Violated | Definition | Example Risk | Typical Mitigations |
| :--- | :--- | :--- | :--- | :--- |
| **S**poofing | Authenticity | Impersonating another user, service, or system | Forged JWT token, forged webhook signature | Mutual TLS, asymmetric HMAC signatures, MFA |
| **T**ampering | Integrity | Malicious modification of data in transit or at rest | Modifying database balances, altering payload in transit | TLS 1.3, cryptographic checksums, immutable audit logs |
| **R**epudiation | Non-Repudiation | Denying having performed an action | User denies submitting transfer; no audit trail exists | Append-only audit logs, cryptographically signed receipts |
| **I**nformation Disclosure | Confidentiality | Exposing sensitive data to unauthorized actors | PII leak in logs, database dump exposed via S3 | Encryption at rest (AES-256), PII masking, strict IAM |
| **D**enial of Service | Availability | Disrupting legitimate access through resource exhaustion | ReDoS regex crash, API request flooding, memory exhaustion | Rate limiting, timeouts, resource quotas (cgroups), CDNs |
| **E**levation of Privilege | Authorization | Gaining higher permissions than intended | IDOR to admin, container breakout to host root | Least privilege, dropped capabilities, non-root users |

---

## 2. Threat Modeling Process

```
Step 1: Deconstruct the System
  ├── Identify Assets: User passwords, financial records, API keys.
  ├── Map Data Flow Diagrams (DFD): External client -> Gateway -> Service -> DB.
  └── Draw Trust Boundaries: Public Internet | DMZ | Private VPC | Database.
         │
         ▼
Step 2: Apply STRIDE to Each Element
  ├── What happens if an attacker spoofs the Gateway?
  ├── Can messages between Service and DB be tampered with?
  └── Can an attacker flood the Service with unauthenticated payloads?
         │
         ▼
Step 3: Score and Prioritize Risks (DREAD or Severity)
  ├── Damage Potential (High / Med / Low)
  ├── Reproducibility (High / Med / Low)
  └── Exploitability (High / Med / Low)
         │
         ▼
Step 4: Formulate Concrete Mitigations
  └── Create actionable tickets (e.g. "Implement HMAC-SHA256 signature on webhooks").
```

---

## 3. Threat Model Specification Example

```markdown
### Component: Payment Webhook Receiver (`POST /webhooks/stripe`)

#### 1. Trust Boundary
Internet (Stripe servers) -> Ingress Reverse Proxy -> Internal Webhook Worker.

#### 2. Identified Threats (STRIDE)
- **[Spoofing] [HIGH]**: An attacker crafts fake HTTP POST requests pretending to be Stripe, claiming an order was paid.
  - *Mitigation*: Validate the `Stripe-Signature` header using the shared webhook secret with constant-time HMAC comparison before processing payload.
- **[Denial of Service] [MEDIUM]**: An attacker floods the webhook endpoint with 100MB JSON payloads to exhaust worker RAM.
  - *Mitigation*: Restrict max request body size to 64KB at reverse proxy; reject payloads without valid signature immediately.
- **[Repudiation] [LOW]**: Disputed charge event.
  - *Mitigation*: Persist raw webhook payload and event ID in append-only `webhook_events` table with unique constraint on `stripe_event_id` to prevent replay attacks.
```

---

## 4. Verification Checklist

- [ ] All components, data stores, and external entities cataloged in a DFD.
- [ ] Trust boundaries clearly marked where privilege levels change.
- [ ] Each data flow evaluated against all six STRIDE categories.
- [ ] Every identified threat has an assigned risk score and a concrete technical mitigation.
