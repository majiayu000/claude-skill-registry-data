---
name: setup-business
description: Use when the user wants to set up Solo Stack, create or update their business context, or when another Solo Stack skill can't find .solo/business.md. Interviews the user and writes the shared business.md that every other skill reads.
---

# Setup Business Context

You are creating the single source of truth about the user's business. Every other Solo Stack skill reads `.solo/business.md` first, so the quality of this file determines the quality of everything else.

## Where the file lives
1. Check `./.solo/business.md` (project-level).
2. If missing, check `~/.solo/business.md` (global).
3. If neither exists, you will create `./.solo/business.md` unless the user asks for global.

If a file exists, read it and offer to update rather than overwrite.

## How to run the interview
Ask in **small batches of 2–3 questions**, not a wall of questions. Skip anything the user has already told you in the conversation or that exists in the current file. Accept rough answers — "about $80/h" is fine. Never invent details; leave a field blank rather than guess.

Batch 1 — the basics
- What do you do, in one sentence, and what's the business called (if anything)?
- Who's the ideal client, and what problem do they usually come to you with?

Batch 2 — money
- How do you charge (hourly, day rate, packages)? Rough numbers and currency?
- Payment terms you actually use (deposit? net 14/30? late fees?).

Batch 3 — voice and proof
- How should things you send sound? (Give an example: "friendly but direct, no buzzwords.") Any spelling preference (US/UK)?
- Two or three proof points: results you've delivered, years in the field, notable clients.

Batch 4 — current state
- Any active clients or projects right now? (Name, project, status.)
- Tools you use for invoicing, calendar, email, project tracking.

## Write the file
Use the template structure below. Fill only what you learned. Keep the user's own wording for positioning and tone — do not "improve" it into marketing speak.

```markdown
# Business context

## Who I am
- **Name:**
- **Business name:**
- **What I do (one sentence):**
- **Location / timezone:**
- **Website:**

## Services & packages
- <name — what's included — price>

## Rates
- **Hourly:** / **Day rate:** / **Minimum engagement:** / **Currency:**

## Ideal clients
- **Who:** / **Their typical problem:** / **Not a fit:**

## Positioning
- **Why clients pick me over alternatives:**
- **Proof points:**

## Tone of voice
- <as the user described it>

## Payment & terms
- **Payment terms:** / **Late fee policy:** / **Payment methods:** / **Tax/VAT notes:**

## Active clients
- <name — project — status — key contact — notes>

## Tools I use
- 
```

## After writing
Show the user the path you wrote to and a 3-line summary. Then say which skills are now ready to use, for example: "Try `/proposal-writer` with your last discovery call notes, or `/invoice-generator` for an outstanding invoice."

## Do not
- Do not ask all questions at once.
- Do not fabricate rates, clients, or proof points.
- Do not rewrite the user's tone description into something generic.
- Do not store secrets (bank details, API keys) in this file — point them to their invoicing tool instead.
