---
name: dlp
description: "Expert routing agent for Data Loss Prevention. Classifies DLP requests across endpoint, network, and cloud enforcement layers, then delegates to the appropriate technology agent. WHEN: \"DLP\", \"data loss prevention\", \"data exfiltration\", \"sensitive data leak\", \"data classification\", \"content inspection\", \"USB block\", \"email DLP\", \"cloud DLP\", \"CASB\", \"data discovery\". Do NOT use for vendor-specific questions -- use the `purview-dlp`, `symantec-dlp`, `forcepoint`, `digital-guardian`, or `cyberhaven` skill."
license: MIT
---

# Data Loss Prevention (DLP)

This skill covers Data Loss Prevention: DLP concepts, architecture, and the major DLP platforms. It helps prevent unauthorized exfiltration or exposure of sensitive data across endpoint, network, and cloud channels.

## How to Approach Tasks

When you receive a DLP request:

1. **Identify the technology** — Determine which DLP platform is in use (Purview, Forcepoint, Symantec, Digital Guardian, Cyberhaven, or technology-agnostic).

2. **Classify the request type:**
   - **Architecture/Design** — Load `references/concepts.md` for DLP fundamentals
   - **Policy configuration** — Read the technology-specific sibling skill
   - **Detection tuning** — Understand data types, then read the sibling skill
   - **Incident response** — Understand enforcement channel, then read the sibling skill
   - **Data discovery** — Identify scope (endpoint, network, cloud), then read the sibling skill

3. **Load context** — Read `references/concepts.md` for general DLP concepts, or read a sibling skill for platform-specific work.

4. **Cross-reference** — Read the appropriate sibling skill using the decision tree below.

5. **Recommend** — Provide actionable guidance with specific policy examples.

## Technology Routing

### Microsoft Purview DLP
**Read `purview-dlp` when:**
- Microsoft 365 environment (Exchange, SharePoint, OneDrive, Teams)
- Purview compliance portal or Unified labeling
- Endpoint DLP on Windows or macOS (M365-managed)
- Sensitivity labels, MIP, AIP
- Copilot/AI Hub data leak prevention
- Adaptive Protection or Insider Risk Management integration
- Keywords: "Purview", "M365 DLP", "MIP", "sensitivity labels", "endpoint DLP", "compliance portal", "EDM", "exact data match", "trainable classifier", "Activity Explorer", "Content Explorer"

### Forcepoint DLP
**Read `forcepoint` when:**
- Forcepoint ONE or Forcepoint DLP platform
- Behavioral analytics / risk-adaptive protection
- Dynamic data protection based on user risk scores
- Forcepoint Web Security or Email Security DLP integration
- Keywords: "Forcepoint", "dynamic data protection", "risk-adaptive", "Forcepoint ONE", "behavioral analytics DLP"

### Symantec DLP (Broadcom)
**Read `symantec-dlp` when:**
- Symantec DLP / Broadcom DLP environment
- Network Monitor, Network Prevent (email/web)
- Endpoint Discover, Endpoint Prevent
- Indexed Document Matching (IDM) or Exact Data Matching (EDM)
- Vector Machine Learning (VML)
- Keywords: "Symantec DLP", "Broadcom DLP", "Vontu", "Network Monitor", "Endpoint Prevent", "IDM", "VML", "Detection Server"

### Digital Guardian (Fortra)
**Read `digital-guardian` when:**
- Digital Guardian agent (kernel-level)
- Fortra Digital Guardian platform
- ARC (Analytics & Reporting Cloud)
- Agent-based data visibility across all data movement
- Keywords: "Digital Guardian", "Fortra DLP", "DG agent", "ARC", "kernel-level DLP"

### Cyberhaven
**Read `cyberhaven` when:**
- Cyberhaven platform
- Data lineage tracking
- Behavioral data flow analysis
- Generative AI data protection (ChatGPT, Copilot leakage)
- Keywords: "Cyberhaven", "data lineage", "data flow tracking", "behavioral DLP"

## DLP Concepts Reference

Load `references/concepts.md` for general DLP architecture questions, vendor-neutral policy design, detection method selection, and data classification framework design.

## Core DLP Knowledge

### What DLP Protects Against

Data Loss Prevention prevents three primary scenarios:

- **Exfiltration** — Intentional theft by malicious insider or compromised account
- **Negligent exposure** — Accidental sharing, misconfigured permissions, wrong recipient
- **Inadvertent leak** — Auto-sync to personal cloud, copy to unmanaged USB, AI prompt injection

### Data Classification Tiers

| Tier | Label | Examples | Default Treatment |
|---|---|---|---|
| 1 — Public | Public | Press releases, public docs | No restrictions |
| 2 — Internal | Internal | General business data | Internal sharing only |
| 3 — Confidential | Confidential | Client data, contracts, strategy | Need-to-know, no external sharing without approval |
| 4 — Restricted | Highly Confidential | PII, PHI, PCI data, trade secrets | Strict controls, encryption required, audit all access |

### Detection Methods

**Regex / Pattern Matching**
- Fastest, lowest compute
- Best for structured data (SSN: `\d{3}-\d{2}-\d{4}`, credit card patterns, passport numbers)
- High false positive rate without context
- Use with keyword boosters (near "social security", near "card number")

**Exact Data Matching (EDM / Fingerprinting)**
- Hash fingerprints of actual sensitive records (employee database, customer PII list)
- Near-zero false positives — only triggers on actual data values
- Requires periodic re-fingerprinting as data changes
- Best for: protecting known PII datasets, customer lists, source code files

**Document Fingerprinting**
- Creates fingerprint of a template document
- Detects filled-out versions of that template (W-9s, NDAs, contracts)
- Useful for: HR forms, financial templates, legal agreements

**ML / Trainable Classifiers**
- Trained on labeled document corpora
- Classifies document type by content semantics, not just patterns
- Built-in classifiers: financial statements, HR resumes, source code, medical records
- Lower precision than EDM but catches novel sensitive content
- Best for: unstructured data where exact patterns are unknown

**OCR (Image/Screenshot DLP)**
- Extracts text from images, screenshots, PDFs
- Applies pattern/classifier detection to extracted text
- Significant compute cost — apply selectively
- Best for: detecting screenshots of confidential data, image-based document exfil

### Enforcement Channels

```
Endpoint DLP
├── Clipboard monitoring (copy/paste to unauthorized app)
├── USB/removable media blocking or auditing
├── Print / print to PDF blocking
├── Screen capture restrictions
├── Cloud sync client monitoring (OneDrive personal, Dropbox, Google Drive)
└── Browser upload blocking

Network DLP
├── Email (SMTP) — inspect outbound email attachments and body
├── Web (HTTP/HTTPS) — inspect web uploads (requires SSL inspection)
├── File transfer protocols (FTP, SFTP)
└── Instant messaging / collaboration tools

Cloud DLP (CASB)
├── Shadow IT discovery (unsanctioned SaaS usage)
├── API-based inspection of cloud storage (Box, Dropbox, Google Drive)
├── Inline proxy or reverse proxy for SaaS
└── Cloud-to-cloud data movement monitoring
```

### DLP Policy Design Workflow

```
1. Identify data assets
   └── What sensitive data exists? Where does it live?
       └── Run data discovery scan (endpoint, file shares, cloud)

2. Classify sensitivity
   └── Apply classification labels (manual, automatic, or recommended)
   └── Define what makes each tier sensitive (regulatory requirements, business value)

3. Define policies
   └── For each data tier: Who can access? What can they do? What is blocked?
   └── Map to enforcement channels: endpoint + network + cloud

4. Start in audit/monitor mode
   └── Collect baseline — understand normal data flows before blocking
   └── Tune false positives before enabling enforcement

5. Enforce with graduated response
   └── Low risk: log only
   └── Medium risk: alert + user notification ("this looks sensitive")
   └── High risk: block + require justification
   └── Critical: block + alert security team + trigger incident

6. Review and iterate
   └── Activity Explorer / SIEM review
   └── Tune policies based on false positives/negatives
   └── Update fingerprint/EDM databases as data changes
```

### Regulatory Drivers for DLP

| Regulation | Key Data Type | DLP Requirement |
|---|---|---|
| HIPAA | PHI (patient health info) | Prevent unauthorized disclosure; audit all access |
| PCI DSS | Cardholder data (PAN, CVV) | Restrict to CDE; detect and block exfiltration |
| GDPR | EU personal data | Data minimization; detect unauthorized transfers outside EU |
| CCPA | California resident PI | Know where data is; prevent unauthorized sale/disclosure |
| SOX | Financial records | Integrity controls; audit financial data access |
| ITAR/EAR | Technical data, export-controlled | Prevent transfer to unauthorized persons/countries |

### Common DLP Anti-Patterns

**Starting with block mode** — Always begin in audit/monitor mode. Blocking before understanding normal data flows causes business disruption and loss of user trust.

**Over-broad regex without context** — A SSN regex alone matches phone numbers, ZIP codes, invoice numbers. Add keyword context, minimum occurrence thresholds, and confidence scoring.

**Ignoring endpoint DLP** — Network DLP misses encrypted traffic, VPN users, and remote workers who are off-network. Endpoint DLP is essential for comprehensive coverage.

**Fingerprinting stale data** — EDM databases become outdated as records change. Stale fingerprints miss new sensitive records or generate stale matches. Automate re-fingerprinting on a schedule.

**No user education** — DLP without user awareness increases shadow IT as users route around controls. Pair enforcement with clear user-facing messages explaining the policy and how to get exceptions.

**Single-channel focus** — Organizations often deploy email DLP and consider themselves protected. Attackers and careless users use cloud sync, USB, and web uploads. Enforce across all channels.

## Technology Agents

Read these sibling skills for platform-specific work:

- `purview-dlp` — Microsoft Purview DLP (M365, endpoint, Copilot)
- `forcepoint` — Forcepoint DLP (risk-adaptive, behavioral analytics)
- `symantec-dlp` — Symantec/Broadcom DLP (IDM, EDM, VML, Network Monitor)
- `digital-guardian` — Digital Guardian/Fortra (kernel-level endpoint DLP)
- `cyberhaven` — Cyberhaven (data lineage, behavioral DLP, AI protection)

## Reference Files

- `references/concepts.md` — DLP fundamentals: classification tiers, detection methods, policy design patterns, regulatory mapping, CASB integration
