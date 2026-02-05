---
name: new-proposal
description: Outline the lightweight process for turning discovery inputs into a first-draft Sentient proposal.
version: 0.2.0
author: Sentient GTM Enablement Team
updated: 2025-05-19
keywords: proposal, sales enablement, sentient.io
---

# New Proposal Drafting (Lightweight)

## Overview
The **new-proposal** skill is now a streamlined playbook. It explains how to assemble a first-draft Sentient proposal using
existing skills and source folders in this repository—no custom scripts or bundled assets required. Follow these instructions to
move quickly from discovery to a shareable document while keeping messaging aligned with Sentient's positioning.

## Quick Start
1. Run the latest **customer-brief** skill to capture discovery findings for the account.
2. Open the relevant product narrative in `product-white-paper/` and flag the sections that map to the customer's needs.
3. Reference the tone and messaging guidance in **sentient-brand-guideline** to keep language on-brand.
4. Combine the above into a proposal outline using your preferred editor (Docs, Notion, Markdown). The sample outline in
   `presentation-outline/` is a good starting point when you need structure.

## Recommended Workflow
1. **Validate inputs**: Confirm you have the newest intake form, customer brief, and stakeholder list from the account team.
2. **Draft the executive summary**: Highlight customer objectives, Sentient's solution fit, and expected outcomes in 2–3
   paragraphs.
3. **Detail the solution**: Use content from `product-white-paper/` to explain architecture, differentiators, and implementation
   plan.
4. **Showcase proof**: Pull relevant success metrics from `smartchat-service-costs/` or other collateral to reinforce value.
5. **Outline next steps**: Define timeline, owners, and required follow-up actions. Link to the **work-day** skill if the deliverable
   should live in the shared Workday folder.

## Success Criteria
- Proposal mirrors Sentient's structure (executive summary → solution overview → roadmap → next steps).
- Messaging stays aligned with the brand guidelines and references approved differentiators.
- Source documents are cited or linked so reviewers can verify claims quickly.
- Output is saved using the `<YYYYMMDD>-<CustomerName>-Proposal-R<Revision>` naming convention.

## Limitations & Notes
- This lightweight skill intentionally omits automation scripts, bundled samples, and tests. It is documentation-only.
- Teams that need repeatable generation or validation should add back scripts in a dedicated branch and update this guide.
- Keep sensitive customer data out of the repository; store working drafts in approved collaboration tools.

## Related Skills & Artifacts
- **customer-brief** – Use to gather and refresh account discovery notes before drafting.
- **product-white-paper** – Provides canonical product positioning and technical capabilities.
- **sentient-brand-guideline** – Supplies tone, terminology, and styling cues for all outbound materials.
- **work-day** – Automates saving final drafts to the shared Workday folder once ready for review.

## Extending Later
If you decide to reintroduce automation:
1. Stand up generator scripts in `scripts/` or a new `automation/` folder.
2. Document new usage patterns here so others know how to run them.
3. Add tests under `tests/` to cover the automated workflow.
