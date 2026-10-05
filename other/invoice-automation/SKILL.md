---
name: invoice-automation
displayName: Invoice Automation
tagline: Automate invoice creation, sending, and payment tracking for faster cash collection.
description: |
  Automates the invoice lifecycle from creation to payment collection.
  Generates invoices from contract data or time entries, sends them
  via email, tracks payment status, and follows up on overdue invoices.
  Integrates with accounting software and payment processors.
department:
  - Finance
  - Accounting
use_cases:
  - Invoicing
  - Accounts Receivable
  - Payment Collection
tools_required:
  - QuickBooks MCP
  - Stripe MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Generate and send invoices for all completed projects this month.
  Follow up on invoices overdue by more than 15 days.
exampleOutput: |
  Invoice Automation — May 2026

  GENERATED
  New Invoices:     8 created ($124,500 total)
  Sent:             8 via email
  Payment Links:    Stripe checkout links attached

  OVERDUE FOLLOW-UP
  INV-2024-041:  Acme Corp — $18,000 — 22 days overdue — 2nd reminder sent
  INV-2024-038:  TechStart — $7,500 — 18 days overdue — 1st reminder sent
  INV-2024-035:  DataFlow  — $12,000 — 16 days overdue — 1st reminder sent

  COLLECTIONS SUMMARY
  Collected This Month:   $89,200
  Outstanding:            $37,500
  Avg Days to Pay:        12 days (target: 14)
---

# Invoice Automation

Automate invoice creation, sending, and payment tracking for faster cash collection.

**Integrations:** QuickBooks, Stripe

## When to Use

- The user needs to generate and send invoices
- Overdue invoices require follow-up
- The user mentions "invoicing", "accounts receivable", or "payment tracking"

## Steps

### Step 1: Generate Invoices

Create invoices from project data, time entries, or contracts.

### Step 2: Send and Track

Send invoices via email with payment links and track delivery.

### Step 3: Follow Up on Overdue

Send automated reminders for overdue invoices with escalation.

## Output

Deliver:
- Generated invoices with payment links
- Overdue follow-up report
- Collections summary and aging report
