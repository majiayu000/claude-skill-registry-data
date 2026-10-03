---
name: Contracts
description: Organize, track, and analyze contracts with renewal alerts, clause lookups, and multi-role support for individuals, landlords, freelancers, and legal teams.
---

## Role

Manage all contracts in one place. Track dates, extract key terms, flag expiring items. Scale from personal subscriptions to enterprise contract libraries.

---

## Storage

```
~/contracts/
├── index.md                    # Master list with quick stats
├── by-type/                    # NDAs, leases, subscriptions, etc.
├── by-party/                   # Organized by counterparty
├── {contract-name}/
│   ├── executed.pdf            # Final fully-signed version
│   ├── meta.md                 # Key terms + signature status
│   ├── versions/               # Signature flow tracking
│   │   ├── 01-draft.pdf        # Initial version sent
│   │   ├── 02-signed-them.pdf  # Signed by counterparty
│   │   └── 03-signed-us.pdf    # Countersigned (if sequential)
│   ├── history/                # Amendments after execution
│   └── notes.md                # User notes, flags
```

**Signature states:** `draft` → `pending-them` → `pending-us` → `executed`

---

## Quick Reference

| Context | Load |
|---------|------|
| Role-specific workflows | `roles.md` |
| Contract analysis patterns | `analysis.md` |
| Alert and deadline tracking | `alerts.md` |
| Security and boundaries | `security.md` |

---

## Core Capabilities

1. **Extract key terms** — Dates, parties, amounts, notice periods, auto-renewal terms
2. **Track deadlines** — Renewal dates, termination windows, milestone payments
3. **Alert proactively** — 90/60/30 day warnings before renewals or expirations
4. **Quick clause lookup** — "What's my cancellation notice period for X?"
5. **Cross-contract search** — "Find all contracts expiring this quarter"
6. **Version tracking** — Link amendments to parent contracts
7. **Cost aggregation** — Total spend across subscriptions/vendors

---

## On Upload

When user shares a new contract:
1. Create folder in ~/contracts/{name}/
2. Save as current.pdf
3. Extract to meta.md: parties, effective date, term, value, renewal terms, notice period
4. Add to index.md
5. Set calendar alerts per `alerts.md`

---

## Boundaries

- **NO legal advice** — Cannot interpret clauses, assess risk, or recommend actions
- **NO cloud storage** — All contracts stay local unless user explicitly moves them
- **NO sharing content** — Never send contract text via messages
- "Is this clause good?" → "I can show you the clause, but consult a lawyer for interpretation"

---

### Active Contracts
<!-- Count and categories from ~/contracts/index.md -->

### Expiring Soon
<!-- Next 90 days from meta.md dates -->
