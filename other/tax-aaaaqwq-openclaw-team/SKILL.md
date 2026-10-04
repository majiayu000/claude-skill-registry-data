---
name: tax
description: Local-first year-round tax memory system for individuals, freelancers, and small businesses. Use when users mention tax documents, receipts, expenses, tax notices, filing preparation, missing forms, accountant meetings, or year-end organization. Captures tax-relevant facts as they happen, tracks what may be missing, and prepares CPA-ready handoff summaries. NEVER provides tax advice, legal interpretations, filing positions, or final tax calculations.
---

# Tax

A local-first, year-round tax memory system.

Tax is designed to help users capture tax-relevant facts throughout the year, prevent missing documents, and prepare organized handoff packages for CPAs, EAs, accountants, or tax software.

This skill is not a tax advisor.  
It is a tax fact capture, organization, and handoff system.

## Core Product Principle

Tax problems are usually not calculation problems first.  
They are information fragmentation problems first.

By the time filing season arrives, users often already have the necessary information — but it is scattered across email, paper mail, receipts, payment platforms, brokerages, bank accounts, and memory.

This skill exists to:
- capture tax-relevant facts early
- preserve them in structured local records
- track what may be missing
- prepare clean outputs for professional review

## What This Skill Does

This skill can:
- Capture tax-relevant events from natural language
- Log tax documents as they are received
- Track expenses and receipts that may matter during filing
- Record tax authority notices
- Maintain questions for a CPA or tax professional
- Compare current-year records with prior-year patterns
- Surface potentially missing forms or incomplete records
- Generate structured year-end and pre-filing handoff summaries
- Store everything locally

This skill cannot:
- Provide tax advice
- Interpret tax law
- Recommend filing positions
- Determine whether a specific item is deductible
- Calculate final tax liability
- Replace a CPA, EA, attorney, or licensed tax professional

## Safety Boundary: Facts vs. Judgments

This skill records facts.  
It does not make legal or tax judgments.

Examples of facts:
- "Received a 1099-NEC from Client A"
- "Spent $120 on a client meal today"
- "Received an IRS notice"
- "Need to ask CPA about contractor payment treatment"

Examples of judgments this skill does NOT make:
- whether a payment is deductible
- what percentage may be deductible
- whether a filing position is appropriate
- how a tax authority will interpret a record

When users ask judgment questions, this skill should:
1. Record the fact or question
2. Mark it for professional review
3. Encourage confirmation with a licensed professional

## Privacy & Storage

All data is stored locally only.

Base path:  
`~/.openclaw/workspace/memory/tax/`

No cloud storage is required.  
No tax authority systems are accessed.  
No external APIs are required for storage.  
No documents are uploaded unless the user independently chooses to do so outside this skill.

## Tax Memory Model

This skill organizes data into six local layers:

### 1. Event Capture Layer
`ledger_events.json`

Raw tax-relevant facts captured from natural language:
- expenses
- documents received
- notices
- questions for CPA
- reminders
- unknown tax-relevant events

### 2. Document Inventory
`documents.json`

Formal forms and document records:
- W-2
- 1099 series
- K-1
- mortgage interest statements
- property tax statements
- donation receipts
- brokerage tax forms
- other filing-year forms

### 3. Expected Documents
`expected_documents.json`

Predicted or expected forms based on:
- prior-year history
- recurring issuers
- user-declared accounts or entities
- manually added expectations

### 4. Expense & Receipt Records
`expenses.json`

Structured expense or receipt facts that may need professional review later.

### 5. Notices & Questions
`notices.json`  
`questions_for_cpa.json`

Tracks:
- tax authority notices
- unresolved follow-up items
- questions the user wants to ask a CPA

### 6. Year State
`year_state.json`

Tracks annual status:
- capturing
- reconciling
- pre_filing
- filed
- archived
- notice_followup

## Product Behaviors

### Frictionless Capture
Users should be able to speak naturally.

Example:  
"Today I spent 120 dollars taking a client to lunch."

The skill should convert that into structured local records with minimal follow-up, preserving raw text even when some fields remain uncertain.

Capture first.  
Refine later.

### Cross-Year Memory
Prior-year records help predict current-year missing items.

Example:  
"If Robinhood issued a 1099-B last year but none has been logged this year, surface that as a possible missing document."

This is a reminder system, not a legal conclusion.

### CPA Handoff
The final output of the skill is not tax advice.  
It is a clean handoff package for professional review.

A handoff package may include:
- filing snapshot
- income document inventory
- expense summary by category
- outstanding notices
- missing items
- questions for CPA

## Recommended Usage

### During the Year
Use this skill when:
- a form arrives
- a receipt or expense happens
- a tax notice is received
- a tax-related question comes up
- the user wants to avoid losing track of details

### Before Filing
Use this skill to:
- compare expected vs received forms
- surface missing items
- summarize expense categories
- prepare a CPA handoff package
- collect unresolved questions

### After Filing
Use this skill to:
- archive the year
- mark unresolved notices
- carry forward expected recurring documents

## Core Workflows

### 1. Capture a tax-relevant event
Example user messages:
- "Today I paid $49 for Adobe"
- "I received a 1099 from Stripe"
- "IRS sent me a letter"
- "Remind me to ask my CPA about this contractor payment"

Internal action:
- classify event
- save raw text
- extract structured fields where possible
- store locally
- mark uncertain items for follow-up

### 2. Log a document
Use when a formal tax form or relevant supporting document is received.

### 3. Record an expense or receipt
Use when the user mentions a business, rental, freelance, or otherwise tax-relevant payment or receipt.

Important:  
The skill records the fact and category.  
It does not determine tax treatment.

### 4. Record a notice
Use when the user mentions receiving communication from a tax authority.

### 5. Check missing items
Use prior-year memory and current-year records to surface items that may still be missing.

### 6. Prepare CPA handoff package
Generate a structured Markdown handoff summary for professional review.

### 7. Generate annual summary
Generate Markdown and CSV annual summary outputs for review, recordkeeping, or handoff support.
## Files

- `ledger_events.json` — captured raw tax-relevant events
- `documents.json` — formal document inventory
- `expected_documents.json` — expected or predicted forms
- `expenses.json` — structured expense records
- `notices.json` — authority notices
- `questions_for_cpa.json` — open professional review questions
- `year_state.json` — annual workflow state
- `summaries/` — generated Markdown and CSV handoff outputs

## Scripts

| Script | Purpose |
|--------|---------|
| `capture_event.py` | Main entrypoint for tax-relevant natural language capture |
| `add_document.py` | Log a formal tax document |
| `track_expense.py` | Record an expense or receipt fact |
| `log_notice.py` | Record a tax authority notice |
| `add_cpa_question.py` | Save a question for professional review |
| `check_missing.py` | Compare prior-year and current-year document history to surface possible missing documents |
| `prep_meeting.py` | Generate CPA-ready handoff package |
| `generate_summary.py` | Produce Markdown and CSV annual summary outputs |
| `archive_year.py` | Archive a filing year and roll forward expected items |
| `set_year_state.py` | Update annual tax workflow status |

## Response Style Rules

When using this skill:
- Prefer operational clarity over explanation
- Capture facts first, even if incomplete
- Preserve raw user wording when helpful
- Clearly distinguish recorded facts from unresolved judgments
- Use phrases like:
  - "recorded"
  - "captured"
  - "flagged for professional review"
  - "possible missing item"
- Avoid phrases like:
  - "deductible"
  - "allowed deduction"
  - "you should file"
  - "you owe"
  - "safe harbor"
  - "final liability"

## Standard Boundary Response

If a user asks:
- "Can I deduct this?"
- "How much tax do I owe?"
- "Should I file this as X or Y?"
- "Will the IRS accept this?"

The skill should respond in this pattern:
1. Record the underlying fact
2. Offer to log it as a CPA review item
3. Explain that final tax treatment requires a licensed professional

## Disclaimer

This skill is for organization, recordkeeping, and professional handoff only.

Tax outcomes depend on jurisdiction, dates, filing status, entity structure, elections, and documentation quality.  
Always confirm tax treatment, filing positions, and calculations with a licensed CPA, EA, attorney, or other qualified tax professional.
