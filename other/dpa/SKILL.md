---
name: "dpa"
version: "1.0.0"
description: "Data Processing Agreement reference — GDPR Article 28, processor obligations, sub-processor management, and cross-border transfers. Use when drafting or reviewing DPAs with vendors."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [dpa, gdpr, data-processing, privacy, processor, legal, compliance]
category: "legal"
---

# DPA — Data Processing Agreement Reference

Quick-reference skill for Data Processing Agreements, GDPR Article 28 compliance, and processor obligations.

## When to Use

- Drafting a DPA with a new vendor or service provider
- Reviewing a vendor's DPA for GDPR compliance
- Understanding controller vs processor obligations
- Managing sub-processor chains
- Handling cross-border data transfers in DPAs

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of DPAs — what they are, when required, legal basis.

### `article28`

```bash
scripts/script.sh article28
```

GDPR Article 28 requirements — mandatory DPA clauses.

### `roles`

```bash
scripts/script.sh roles
```

Controller vs Processor vs Sub-processor — roles and responsibilities.

### `clauses`

```bash
scripts/script.sh clauses
```

Essential DPA clauses — scope, obligations, security, and termination.

### `subprocessors`

```bash
scripts/script.sh subprocessors
```

Sub-processor management — authorization, notification, and liability.

### `transfers`

```bash
scripts/script.sh transfers
```

Cross-border data transfers — SCCs, adequacy decisions, and safeguards.

### `breaches`

```bash
scripts/script.sh breaches
```

Data breach handling in DPAs — notification, cooperation, and remediation.

### `checklist`

```bash
scripts/script.sh checklist
```

DPA review checklist for compliance verification.

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Configuration

| Variable | Description |
|----------|-------------|
| `DPA_DIR` | Data directory (default: ~/.dpa/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
