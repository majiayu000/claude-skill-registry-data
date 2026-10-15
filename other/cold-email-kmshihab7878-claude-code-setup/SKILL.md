---
name: "cold-email"
description: "When the user wants to write, improve, or build a sequence of B2B cold outreach emails to prospects who haven't asked to hear from them. Use when the user mentions 'cold email,' 'cold outreach,' 'prospecting emails,' 'SDR emails,' 'sales emails,' 'first touch email,' 'follow-up sequence,' or 'email prospecting.' Also use when they share an email draft that sounds too sales-y and needs to be humanized. Distinct from email-sequence (lifecycle/nurture to opted-in subscribers) — this is unsolicited outreach to new prospects. NOT for lifecycle emails, newsletters, or drip campaigns (use email-sequence)."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# Cold Email Outreach

Use this skill for B2B cold outreach to prospects who have not opted in. Write, critique, or iterate emails so they sound like a thoughtful human, not a sales machine.

Do not use this skill for lifecycle emails, newsletters, onboarding, re-engagement, or opted-in drip campaigns.

## Required Input Contract

Check for `marketing-context.md` first. If it exists, read it before asking questions.

Gather or infer:

- Sender: role, seniority, offer, buyer, proof points, individual vs company voice.
- Prospect: title, company segment, likely problem, trigger or reason to reach out now.
- Personalization scope: named prospects, segment template, or account-specific signals.
- Ask: reply, referral, short call, demo, or another single next step.
- Operating constraints: send volume, timeline, market, compliance needs, and data confidence.

## Core Modes

1. **First email:** clarify ICP, problem, trigger, proof, and ask; draft subject, opener, body, CTA, and 2-3 subject variants.
2. **Follow-up sequence:** build a 5-6 touch sequence with send gaps, distinct angles, standalone follow-ups, and a professional breakup email.
3. **Performance iteration:** diagnose opens, replies, CTA quality, and wrong-fit responses; rewrite the failing element and recommend one test.

## Core Writing Rules

- Lead with the prospect's world, not the sender's product.
- Write like a peer. Remove vendor language, marketing claims, and inflated phrasing.
- Every sentence must create curiosity, establish relevance, build credibility, or drive the ask.
- Personalization must connect to the problem or trigger.
- Use one ask per email.
- Keep first emails short: usually 3-7 sentences and under 150 words.
- Prefer plain text.

See [writing-principles.md](references/writing-principles.md) for audience calibration, subject line patterns, and anti-patterns.

## Follow-Up Rules

- Use increasing gaps, typically Day 1, 4, 9, 16, 25, and 35.
- Each follow-up needs a new angle: proof, a different pain point, a relevant insight, a direct question, or a referral ask.
- Do not send "just checking in" or "circling back" emails.
- Make each follow-up understandable without reading previous emails.
- Close the loop professionally in the final message.

See [follow-up-playbook.md](references/follow-up-playbook.md) for the cadence table, angle rotation, and breakup template.

## Safety, Compliance, and Deliverability

- Do not fabricate customer proof, prospect research, performance metrics, affiliations, referrals, or outcomes.
- Do not use deceptive `Re:`/`Fwd:` subject lines.
- Do not include secrets, credentials, private context, scraped personal data, or local paths.
- Include opt-out language where legally or operationally required.
- Flag deliverability risks: missing SPF/DKIM/DMARC, cold sending from the primary domain, new domain with no warmup, high bounce risk, heavy HTML, or excessive daily volume.
- Use public-safe placeholders for missing company, prospect, or metric details.

See [deliverability-guide.md](references/deliverability-guide.md) for setup checks, warmup notes, and spam-risk patterns.

## Validation and Review

Before returning copy, check:

- The opener is about the prospect, not the sender.
- The email has one clear ask.
- Any proof point is real or explicitly marked as a placeholder.
- The message is concise enough for the buyer's seniority.
- Follow-ups add new value instead of repeating the same ask.
- Compliance and opt-out needs are addressed when relevant.
- Output is plain text unless the user explicitly asks otherwise.

## Output Expectations

- **Write a cold email:** first-touch email, 2-3 subject variants, and a short rationale.
- **Build a sequence:** 5-6 emails with send gaps, subject lines, and the role of each touch.
- **Critique a draft:** line-level assessment, rewrite, and reason for each major change.
- **Write follow-ups:** emails 2-6 with distinct angles and a breakup email.
- **Analyze performance:** diagnosis by open rate, reply rate, CTA, and fit; rewritten element plus one test.

Use bottom-line-first communication, explain what changed and why, and tag assumptions when source context is incomplete.

## Minimal Examples

```text
Write a first-touch email to CFOs at Series B SaaS companies about reducing billing errors.
Build a five-email outbound sequence for VP Sales prospects using a hiring-trigger angle.
Rewrite this draft so it sounds less sales-y and has one clear ask.
```

## Reference Map

- Detailed writing principles, voice calibration, subject lines, and avoid list: [writing-principles.md](references/writing-principles.md)
- Follow-up cadence, angle rotation, and breakup email pattern: [follow-up-playbook.md](references/follow-up-playbook.md)
- Deliverability basics, compliance cues, and proactive review triggers: [deliverability-guide.md](references/deliverability-guide.md)
- Expanded examples and output patterns: [examples.md](references/examples.md)
