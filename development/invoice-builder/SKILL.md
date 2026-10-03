---
skill_id: invoice-builder
name: Invoice Builder — itemized invoice from one line of plain text
description: "Build a client invoice — \"make an invoice for\", \"create an invoice\", \"bill this client for\". Parses plain text into line items, computes subtotal, tax and total with the math sanity-checked."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
everyday_skill: true
triggers:
  - "make an invoice for"
  - "create an invoice"
  - "bill this client for"
collaborates_with:
  - planner
  - financial-modeler    # tax/total math sanity
references:
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Invoice Builder

> **Does:** generates a clean, itemized invoice from a line of plain text.
> **Solves:** fumbling with invoice formatting every billing cycle.
> **Triggers on:** *"make an invoice for [work, amount]"*

## How Maxim does this

Parses the plain-text description into line items (description · qty · rate · amount), computes subtotal / tax / total (math sanity-checked via `financial-modeler`), and emits a professional invoice (Markdown table by default; structured fields on request for a template). Pulls your business identity from the brand foundation if available; otherwise asks for the missing header fields once.

## Hard guardrail (governance)

**This skill generates an invoice document only. It never sends money, processes payments, or initiates transfers** — those require the operator to act in their own payment tool. Stated explicitly per Maxim's financial-action boundary.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Cognitive Ease** (unambiguous line items, one clear total) · **Goal-Gradient** (prominent "Amount Due" + due date drives faster payment).
- **No-fabrication:** every number traces to the input; nothing is invented. Missing tax rate / terms → it asks rather than assuming.
- **Confidence tag (ADR-010).**

## Output

An itemized invoice: header (from/to) · line items · subtotal/tax/total · invoice # + dates + payment terms.
