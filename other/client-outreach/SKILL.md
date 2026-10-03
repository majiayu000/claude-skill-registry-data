---
name: client-outreach
description: Draft and refine outbound outreach workflows for agency prospecting, follow-up, and contact sequencing. Use when the user needs prospecting messages, follow-up structure, outreach personalization logic, or repeatable outbound playbooks.
---

# client-outreach

## Purpose

- Create structured outreach assets for prospecting and follow-up.
- Keep outbound messaging consistent, concise, and easy to personalize.

## Triggers

- The user wants cold outreach sequences.
- The user wants personalized outreach copy for a lead list.
- The user wants a repeatable outbound playbook for an agency offer.

## Inputs

### Required

- target audience or lead segment
- offer or desired call to action

### Optional

- brand voice notes
- proof points, case studies, or social proof
- channel constraints such as email, LinkedIn, or DM

## Outputs

- outreach sequence outline
- draft messages by step or channel
- personalization fields or instructions

## Guardrails

- Do not invent proof, metrics, or client results.
- Keep claims supportable from provided inputs.
- Escalate when compliance, deliverability, or legal review is needed.

## Failure Modes

- offer is too vague to write credible outreach
- tone does not match the brand or market
- sequence is generic and not segment-aware
- requested channel constraints are missing

## QA Steps

1. Confirm the target audience and CTA are explicit.
2. Check every claim against provided proof.
3. Check the sequence has a clear progression and no duplicated step.
4. Check personalization tokens are obvious and usable.
