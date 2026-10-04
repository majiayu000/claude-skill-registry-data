---
name: contractor
description: >-
  Generate professional .docx reservation agreements for vacation rental properties.
  Collects client data interactively, calculates totals and deposit automatically,
  and produces a ready-to-send Word document with logo, bank details, signature,
  and legal clauses. Use when user says "contractor", "contrat de réservation",
  "accord de réservation", "nouvelle résa", "contrat gîte", or asks to generate
  a rental contract. Not for invoicing, payment tracking, email sending, lease
  agreements (bail), or properties other than Au Jardin d'Éole.
---

# Contractor — Vacation Rental Agreement Generator

## Overview

Generates professional "Accord de Réservation" `.docx` documents for Au Jardin d'Éole vacation rentals in Guadeloupe. Collects reservation data through an interactive workflow, auto-calculates totals and security deposit, and produces a ready-to-send contract with integrated logo, bank details (RIB), owner signature, and all legal clauses.

## Quick Start

```
User: "contractor"
→ Claude collects reservation data (client, dates, accommodations, pricing)
→ Claude displays summary with auto-calculated amounts
→ User validates
→ Claude generates .docx file
```

## Workflow

### Step 1: Data Collection

Collect data interactively. Group questions logically (2-3 per message max).

**Round 1 — Client & Stay:**
- Client name (family), reference name (first + last), email, phone (optional)
- Which accommodation(s)? → Kaz Alizé / Ti Briz / Souf Van
- Arrival date, departure date, number of guests

**Round 2 — Pricing:**
- Nightly rate per accommodation
- Cleaning fee (frais ménage)
- Tourist tax amount (taxe de séjour — manually provided by owner)
- Any surcharges? (label + amount)
- Any discounts? (label + amount)

**Round 3 — Payment & Schedule:**
- Payment schedule: default 30% / 30% / 40% or custom
- Payment deadline dates
- Check-in/check-out times (default: 15h00 / 10h00)
- Security deposit override? (default: auto-calculated)

→ See [fixed-data.md](references/fixed-data.md) for owner details, bank info, accommodation specs.

### Step 2: Summary & Validation

Display a formatted summary:

```
📋 RÉCAPITULATIF — AJDE-{YEAR}-{CLIENT_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Client      : {name} — {email}
Séjour      : {arrival} → {departure} ({nights} nuitées, {guests} pers.)
Logements   : {list with rates}

Total brut  : {amount} €
Remises     : - {amount} €
TOTAL NET   : {amount} €

Garantie    : {amount} € (auto: 30% du total net)
Échéancier  : {schedule}

✅ Valider et générer le contrat ?
```

Wait for explicit user validation before generating.

### Step 3: Document Generation

1. Read [document-structure.md](references/document-structure.md) for the 11-section structure
2. Read [legal-clauses.md](references/legal-clauses.md) for clause wording
3. Read [guarantee-rules.md](references/guarantee-rules.md) for deposit calculation
4. Load the generation script from `scripts/generate_contract.js`
5. Adapt the contract data object in the script with collected values
6. Run: `node generate_contract.js`
7. Validate: `python scripts/office/validate.py {output}.docx`
8. Present file to user

**Output filename**: `Accord_Reservation_{CLIENT}_{YEAR}.docx`

## Calculation Rules

### Totals
```
sub_total = rate_per_night × nights (per accommodation)
gross_total = sum(sub_totals) + sum(extras)
net_total = gross_total - sum(discounts)
```

### Security Deposit (auto)
```
deposit = net_total × 30%
deposit = ceil_to_50(deposit)    // round up to nearest 50€
deposit = clamp(300, deposit, 1500)  // floor 300€, cap 1500€
```

Override: user can force a specific amount with `--override-garantie {amount}`.

### Contract Reference
```
AJDE-{STAY_YEAR}-{CLIENT_LAST_NAME_UPPER}
```

## Commands

| Command | Effect |
|---------|--------|
| `contractor` | Start interactive workflow |
| `contractor --recap` | Show summary only, don't generate |
| `contractor --override-garantie 500` | Force deposit amount |

## Critical Rules

1. **Always read references** before generating — fixed data, clauses, and structure
2. **Always validate** the generated `.docx` with the validation script
3. **Never skip** the summary step — wait for user approval
4. **Assets path**: `assets/Logo.png` and `assets/Signature_Edouard.jpg` must be copied to working directory before generation
5. **Nuitées calculation**: auto from dates if not provided
6. **Payment schedule amounts**: adjust final payment so sum equals net_total exactly
7. **Output language**: French for the document, conversation in user's language

## Skill Bridges

After generating the contract:
- → `corrector` to draft the email sending the contract to the client
- → `notion-task-enricher` to create a payment tracking task

## Limitations

This skill does NOT:
- Send emails
- Track payments or send reminders
- Handle invoicing or accounting
- Support properties other than Au Jardin d'Éole
- Provide electronic signature
- Calculate tourist tax (manually provided by owner)

## Dependencies

- `npm install -g docx` (docx-js v9+)
- Python validation scripts from the `docx` skill
- Assets: `Logo.png`, `Signature_Edouard.jpg`

## Knowledge Base

- [Fixed Data](references/fixed-data.md) — Owner info, bank details, accommodation specs
- [Document Structure](references/document-structure.md) — 11-section contract layout and design
- [Legal Clauses](references/legal-clauses.md) — Clause wording for all sections
- [Guarantee Rules](references/guarantee-rules.md) — Deposit calculation logic and rationale

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-27 | Initial release — full contract generation with interactive workflow |

## Current: v1.0.0

## Owner

- **Author**: Édouard PHELIP
- **Contact**: Via Claude.ai
