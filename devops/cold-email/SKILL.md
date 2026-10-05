---
name: cold-email
description: 'Run the Markster OS cold email playbook. CHECK prerequisites, DO the sequence build, VERIFY before sending. Routes through ScaleOS G3 Book with context from F1/F2.'
---

# Cold Email Operator

---

## CHECK

Do not proceed past any failed check.

**1. F1 complete?**

Read `company-context/audience.md`.

Required before this skill runs:
- ICP defined with company type, headcount range, and buying trigger
- Decision-maker title named
- Specific pain in the buyer's words (not your description of their pain)

If missing: "F1 is not complete. Cold email will not perform without a defined ICP and buying trigger. Open `methodology/foundation/F1-positioning.md` and complete it first."

**2. F2 complete?**

Read `company-context/offer.md`.

Required:
- Outcome statement (what the client achieves, not what you deliver)
- Proof point (specific result with company type, number, and timeframe)
- Risk reversal or guarantee exists

If missing: "F2 needs an outcome statement and at least one proof point before this sequence will convert. Gut check: can you complete this sentence with a real number? 'We help [ICP] achieve [outcome] in [timeframe]. [Company] did this.' If not, fix F2 first."

**3. Offer passes the Stranger Test?**

Ask: "Read your offer to me in one sentence. Why is it obviously better than doing nothing?"

If you cannot explain it without jargon in under 15 seconds, the offer needs work before the sequence does. Route to `playbooks/offer/README.md`.

**4. List exists or can be built?**

Ask: "Do you have a prospect list? How many contacts, and have they been verified?"

- No list: go to `playbooks/find/README.md` + `playbooks/find/templates/icp-worksheet.md` first
- Unverified list (bounce rate unknown): run verification before sending (target: under 3% bounce rate)
- List ready: proceed

**5. Sending infrastructure ready?**

Ask: "Are you sending from a separate domain? Is SPF/DKIM/DMARC configured? Is a warmup tool running?"

If no to any of these: stop here. Sending from a cold or misconfigured domain will destroy your deliverability. Fix infrastructure before sequence.

**6. Your archetype**

Before writing the sequence, confirm the business type. Route to the correct segment file.

| Your type | Read this first |
|-----------|----------------|
| B2B SaaS, devtools, marketplace | `playbooks/segments/startup-archetypes/` |
| Agency, consulting, IT/MSP, advisory | `playbooks/segments/service-firms/` |
| Residential or commercial services | `playbooks/segments/trade-businesses/` |

Cold email is not always the right G3 motion. Trade businesses and advisory firms often convert better on referrals and warm outreach first. Your segment file will say if cold email should come later.

---

## DO

Run these six steps in order. Do not skip a step unless the user confirms it is already done.

### Step 1: Research

Ask: "Have you run the buyer JTBD and competitive intelligence research prompts?"

- If no: direct to `research/prompts/buyer-jobs-to-be-done-prompt.md` and `research/prompts/competitive-intelligence-prompt.md`
- If yes: ask them to share the buyer verbatims -- the exact words their buyers use to describe the problem

**Use the verbatims in the sequence.** Not your language. Their language.

### Step 2: Segment

Define the list-building filter from F1:

```
Industry: [specific, not "B2B"]
Revenue range: [floor and ceiling]
Headcount: [range]
Geography: [if relevant]
Decision-maker title: [exact title, not "manager"]
Buying trigger: [the event that makes them a buyer right now]
```

Source options: Apollo, LinkedIn Sales Navigator, Hunter.io, industry directories.

Target list size: 200-500 contacts per cohort.

Verification: run through an email validator before importing. Bounce rate must be under 3%.

### Step 3: Write

Using buyer verbatims from Step 1 and the outcome statement from F2, write the 3-touch sequence:

**Email 1 -- Cold intro**
- Under 100 words
- One CTA (a question, not a link)
- Structure: [Specific trigger] + [Problem in their words] + [One proof point] + [Soft ask]
- Subject: "[Company] -- [traction number or outcome] -- [category]"
- No deck, no calendar link in first email

**Follow-up 1 -- Different angle, same offer**
- Under 60 words
- New angle: different pain, different proof point, or different framing
- Reply to the original thread

**Follow-up 2 -- Pattern interrupt or breakup**
- Under 40 words
- Options: honest breakup frame ("Should I close your file?") or humor if the brand voice allows it
- Reply to same thread

Reference template: `playbooks/book/cold-email/templates/sequence-b2b.md`

Writing rules:
- No em-dashes
- Sentences under 20 words
- One idea per sentence
- First person, plain language
- No buzzwords ("leverage," "solutions," "synergy," "space")

### Step 4: Send

Confirm:
- From: separate domain (not primary)
- SPF/DKIM/DMARC: configured
- Warmup: running for at least 2 weeks before first send
- Daily send limit: start at 20/day, scale up slowly
- Sending tool: (Clay, Instantly, Smartlead, Reply.io -- confirm which they use)

Send schedule:
- Tuesday through Thursday, 8am-10am local time for the recipient
- Batch 1: 20-50 contacts as a test cohort
- Wait 72 hours before evaluating results

### Step 5: Reply handling

Review how they will handle each reply type. Reference `playbooks/book/reply-triage.md` for exact scripts.

| Reply type | Action |
|-----------|--------|
| Positive / interested | Respond within 4 hours. Book the meeting immediately. |
| Soft no / not now | Add to quarterly follow-up sequence. No longer than 3 lines. |
| Referral | Ask for intro. Thank them. Log the contact. |
| Unsubscribe | Remove. Do not follow up. |
| Objection | Use objection scripts from `playbooks/biz-dev/sales/templates/objections.md` |
| No reply | Follow-up 1 at day 3, Follow-up 2 at day 7. Then stop. |

### Step 6: Iterate

After 100 sends, review:

| Metric | Target | Action if below target |
|--------|--------|----------------------|
| Open rate | 30%+ | Investigate deliverability. Check spam filters. |
| Reply rate | 1%+ | Message problem if open rate is good. Rewrite Email 1. |
| Meeting rate | 0.25%+ | Check CTA clarity. Is the ask too big? |

Change one variable at a time. Do not rewrite the entire sequence at once.

**Volume rule:** More volume beats better copy at the same conversion rate. Fix volume before copy unless open rate is already above 30%.

---

## VERIFY

Before this session ends:

**1. Sequence written?**

Confirm all three emails are written, use buyer verbatims, and pass the Stranger Test when read aloud.

**2. Infrastructure confirmed?**

Confirm separate domain, SPF/DKIM/DMARC, and warmup are all checked.

**3. List ready?**

Confirm list exists, is filtered to ICP match, and is verified.

**4. Reply triage plan set?**

Confirm what happens when positive replies come in. Who responds? How fast? What's the booking link?

**5. Metric baseline set?**

State the starting numbers: "Before this send, our reply rate is [X]. Success this week = at least [Y]."

---

## Add-ons

If `AOE_GRADER_KEY` is set: the AOE Grader can score AI visibility as part of the research step.

If `LEAD_PACKS_KEY` is set: pre-built, verified contact lists by vertical and geography are available instead of building from scratch.

---

## Reference files

- Full playbook: `playbooks/book/cold-email/README.md`
- Sequence template: `playbooks/book/cold-email/templates/sequence-b2b.md`
- Follow-up templates: `playbooks/book/cold-email/templates/follow-up.md`
- Reply triage: `playbooks/book/reply-triage.md`
- Warm outreach (run before cold): `playbooks/book/warm-outreach.md`
- Objection scripts: `playbooks/biz-dev/sales/templates/objections.md`
