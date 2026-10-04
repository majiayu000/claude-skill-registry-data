---
name: proposal-writer
description: Write a client proposal or quote from your own service tiers, saved once in a pricing config. Produces a structured proposal with a current-situation read, scoped line items, an investment table, process phases, and terms. Drafts only, a human reviews before anything reaches a client. Use when the user says "write a proposal", "quote for this client", "proposal for this project", or "turn this brief into a proposal".
---

# Proposal Writer

You write proposals that read like a busy specialist wrote them: specific about the client's situation, clear about scope, and unapologetic about price. This skill produces drafts for human review. It never sends anything.

## Step 0: Load the pricing config (never guess prices)

Look for a `proposal-pricing.config.md` file in the project root. If it does not exist, ask the user for the values below, then offer to save them for next time.

```
SENDER          Name and positioning title for the header
SERVICES        The services offered, each with a one-line description
TIERS           Price ranges per service or package, with currency
TERMS           Payment split, revision rounds, validity window
PROCESS         The phases a project moves through, with rough durations
PROOF_POINTS    Optional real numbers for credibility, e.g. "300+ projects"
```

Never invent prices, discounts, or proof points. If a requested scope has no tier, say so and propose a custom line item for the user to price.

## Step 1: Read the client's situation

Gather whatever exists: a brief, meeting notes, their website, or a description from the user. The proposal opens with a short read of where the client is now, and that section only works if it is specific. If you know nothing about the client, ask for two sentences about them rather than writing filler.

## Step 2: Write the proposal

Default output is a markdown file named `Proposal_<Client>.md` in the folder the user indicates (or the current project). Structure:

```markdown
# Proposal: <Client>

**Prepared by:** <SENDER>
**Date:** <today>
**Valid until:** <today + validity window from TERMS>

## Where you are now
Two or three sentences on their current situation. Specific observations, not flattery.

## What I propose
Each scope item with one line on the outcome it buys the client.

## Investment
| Item | Deliverables | Price |
|---|---|---|

## Process
The phases from PROCESS with rough timeline.

## Terms
Payment split, revisions, validity from TERMS.

## Next step
One low-friction closing line.
```

Rules for the body:

- Price from TIERS. Round numbers. State the currency once.
- Every scope item maps to a deliverable the client can point at.
- The "Where you are now" section must contain at least one observation the client would recognize as true about their business. If it could open any proposal, rewrite it.
- Keep the whole proposal under one page of reading. Longer proposals hide weak scoping.

## Step 3: Report

Show the Investment table and the "Where you are now" section in chat, with the file path. The user reviews and adjusts before the client ever sees it.

## Rules

- Drafts only. Never email or deliver the proposal anywhere.
- Never invent prices, deadlines, availability, or credentials. Everything comes from the config or the user.
- No em dashes in any output. Use commas, colons, full stops, or brackets.
- If the user asks for a price you consider off-config, flag it once and then follow their instruction. It is their business.

## Output

One proposal markdown (or HTML on request) file plus a chat summary of investment and positioning for quick review.
