---
name: data-room
description: Structures a virtual data room with a full folder taxonomy and staged access tiers, use it when you must organize diligence materials for buyers.
---

# Data Room Agent

## When to use
Use this when preparing a sell-side process and you must organize diligence materials so multiple buyers can review them in a controlled way. A disorganized data room slows diligence, invites repetitive questions, and leaks sensitive information too early. This agent gives you a clean taxonomy and a staged-access plan before documents go live.

## What it does
It produces a data room index and an access-tiering plan: a complete folder structure for diligence materials plus a mapping of which documents are exposed in round one, round two, and confirmatory diligence, with watermarking and Q&A discipline built in.

## Method
1. Build the top-level folder taxonomy.
   - Standard folders: corporate, financial, commercial, legal, tax, HR, IT and technology, and material contracts.
   - Add industry-specific folders only where the sector demands them, for example regulatory or environmental.

2. Populate each folder with standard subfolders.
   - Corporate: org chart, cap table, board minutes, constitutional documents. Financial: audited statements, management accounts, budget and forecast, working capital.
   - Commercial: customer and revenue analysis, pipeline. Legal: litigation, IP, permits. Tax: returns and structure. HR: org, comp, key contracts. IT: systems and security. Contracts: top customer and supplier agreements.

3. Assign each document a sensitivity level.
   - Levels: open, sensitive, and clean-team only.
   - Clean-team items include customer-level pricing, named-customer margins, and detailed forward pipeline that a competitor could weaponize.

4. Define staged access tiers.
   - Round one: overview and non-sensitive materials to all qualified bidders. Round two: detailed financials, key contracts (redacted where needed), and management-access materials to shortlisted parties. Confirmatory: remaining and clean-team materials to the preferred bidder.
   - Good looks like: exposure escalating strictly with buyer commitment, never ahead of it.

5. Map every document to the earliest round in which it is released.
   - Honor its sensitivity level so a clean-team item cannot surface in round one even if it lives in an early folder.

6. Set watermarking rules.
   - Apply dynamic watermarks carrying viewer identity and timestamp on all sensitive and clean-team documents.
   - Disable download or restrict to view-only where the item is highly sensitive.

7. Establish Q&A discipline.
   - Route all questions through a single logged channel, tagged by workstream, with a tracked status and a standard turnaround.
   - Common pitfall: side-channel answers by phone that never get logged; prohibit them so every response is captured and consistent across bidders.

8. Define permission and audit hygiene.
   - Use named user groups per tier, review the access log regularly, and set a downgrade or takedown path if a party drops out mid-process.

## Inputs
- The list of diligence documents available, or the categories you can supply
- Which items are competitively sensitive or clean-team only
- The number of process rounds and the gating between them
- Buyer groups and how many parties are expected per round
- Watermarking and download restrictions you require
- Any redaction rules for third-party contracts
- The Q&A turnaround target and the workstream owners

## Output format
- Data room index: the folder taxonomy with subfolders and the documents mapped into them, each tagged with its sensitivity level (open, sensitive, clean-team only).
- Access-tiering plan: for each round (round one, round two, confirmatory), the buyer group, the folders and documents exposed, and the watermarking rules applied.
- Q&A rules: channel, routing by workstream, turnaround, and the no-side-channel discipline.
- Audit rules: user groups per tier and the access-log review cadence.
- Describe all mappings as structured text, never a rendered markdown table.

## Example
Meridian Foods sell-side. Index excerpt, Financial folder: audited statements (open), management accounts (sensitive), customer-level margin bridge (clean-team only). Access plan: round one exposes corporate overview, audited statements, and market materials to all six qualified bidders, view-only with dynamic watermarks. Round two adds management accounts and redacted top-20 customer contracts to the three shortlisted parties, with download disabled on the contracts. Confirmatory opens the customer-level margin bridge to the preferred bidder under a clean-team agreement, viewable only by named advisers. Q&A runs through one logged channel with a two-business-day turnaround, routed by workstream, and phone answers are prohibited so all bidders see the same record.
