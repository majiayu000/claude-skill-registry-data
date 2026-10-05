---
name: fundraising
description: 'Run the Markster OS fundraising playbook. CHECK stage, traction, and funding path before building anything. DO investor ICP + list + outreach + pitch + close. VERIFY investor pipeline is real before claiming readiness. Routes through ScaleOS Biz Dev.'
---

# Fundraising Operator

---

## CHECK

Do not proceed past any failed check.

**1. Stage and traction defined?**

Ask the user:
- What stage are they raising at? (Pre-seed / Seed / Series A / growth?)
- How much are they raising?
- What traction do they have right now? (ARR, MRR, customers, growth rate, retention -- whatever applies)

If they cannot state a specific traction number: "Investors fund traction, not potential. Before building an investor list, you need at least one measurable proof point. What is the most specific thing you can say about your results right now?"

**2. Funding path confirmed for their archetype**

Fundraising looks very different by business type. Read the right file before advising.

Read `playbooks/biz-dev/fundraising/funding-mechanisms.md` -- especially if the user is a service firm or trade business. VC is one path. It is not the only path.

| Your type | Relevant funding paths |
|-----------|----------------------|
| SaaS, devtools, marketplace | VC, angels, SAFE, priced round |
| Agency, consulting, advisory | PE, SBA, revenue-based financing |
| Trade businesses | SBA, equipment financing, PE roll-up |
| Hardware, DTC | Strategic, VC with hardware thesis, debt |

Read `playbooks/biz-dev/fundraising/traction-by-archetype.md` -- what traction means for your archetype at each stage.

Read `playbooks/biz-dev/fundraising/round-sizing.md` -- SAFE vs. convertible note vs. priced round, and how much to raise at each stage.

If the user is pursuing VC for a business type where it is not the optimal path, name it clearly before proceeding.

**3. Which part do they need?**

Ask which stage they are working on:
- Building the investor target list
- Writing outreach (warm intro requests or cold)
- Preparing for pitch meetings
- Managing follow-up and the close process

Do not build a full 4-stage plan if they only need one stage. Route directly.

---

## DO

Run the relevant stage(s). If they are starting from zero, run all four in order.

### Stage 1: Investor target list

Define the investor ICP -- the profile of an investor who is the right fit for this raise:
- Stage fit: who invests at their current traction level?
- Sector fit: who has portfolio companies in their category?
- Check size: who writes the right check size for this raise?
- Value-add: who brings relevant introductions or operating experience beyond capital?

Categorize into three tiers:

| Tier | Count | Priority |
|------|-------|---------|
| Tier 1 | 10-20 | Ideal fit, warm intro required to approach |
| Tier 2 | 30-50 | Good fit, warm or cold both viable |
| Tier 3 | 50-100 | Possible fit, cold only |

Sources for building the list: Crunchbase, AngelList, LinkedIn (portfolio companies of target funds), Axios Pro Rata, fund websites.

Do not send to Tier 3 until Tier 1 and 2 are active.

### Stage 2: Outreach

**For warm intros (Tier 1 and 2):**
1. Map intro paths through LinkedIn second-degree connections
2. Help write the mutual connection request -- short, honest, specific on why this investor is the right fit
3. Help write the forward blurb -- one paragraph, lead with traction not vision

Forward blurb structure:
- One sentence on what the company does
- One number (traction metric)
- One sentence on why you thought of this investor specifically
- The ask (15-minute intro call)

**For cold outreach (Tier 2 and 3):**

Use `playbooks/biz-dev/fundraising/templates/investor-outreach.md`.

Rules:
- Under 100 words
- Lead with traction, not vision or market size
- Specific ask: 15-minute intro call (not "let me know if you're interested")
- No deck in the first message

### Stage 3: Pitch preparation

Walk through the 10-slide deck structure:

| Slide | Content |
|-------|---------|
| 1. Cover | Company name, one-liner, date |
| 2. Problem | Specific scenario -- a story, not a statistic |
| 3. Solution | What you built, one sentence |
| 4. Why now | Market timing argument -- what changed that makes this the right moment |
| 5. Traction | Most compelling numbers first |
| 6. Product | Screenshots or demo, not diagrams |
| 7. Business model | How you make money -- unit economics if available |
| 8. Market size | Bottom-up logic, not TAM from a report |
| 9. Team | The 2-3 things that make you the right people for this specific problem |
| 10. The ask | Amount, use of funds, milestones this raise gets you to |

Also help with the verbal narrative: 2 minutes max, covers why you, why this market, why now.

**Pitch quality gates before taking meetings:**
- The problem slide uses a specific scenario, not a statistic
- Slide 5 (traction) leads with the most compelling number
- Market size uses bottom-up logic the investor can follow
- The ask slide states what milestone the money reaches (not "growth")

### Stage 4: Follow-up and close

After every meeting, send a follow-up within 24 hours. Use `playbooks/biz-dev/fundraising/templates/follow-up.md`.

Pipeline management rules:
- Track every investor with: stage, last contact date, next action, notes from last meeting
- Review active investor relationships weekly
- Create momentum: when other investors express genuine interest, share it transparently

When an investor passes: send a feedback request within 48 hours. Their answer is the product roadmap.

When closing: state the close timeline clearly. "We are targeting to close this round by [date]. Current commitments are [amount]. We have space for [X] more investors at this stage."

---

## VERIFY

Before this session ends:

**1. Investor list is tiered?**

Confirm Tier 1, 2, and 3 are defined with clear criteria. Tier 1 should require a warm intro -- if everything is cold, the target list is probably too broad.

**2. Outreach passes the traction-first check?**

Read the first sentence of the outreach message. Does it lead with a traction metric or a vision statement? If it starts with vision, rewrite.

**3. Pitch deck structure is complete?**

Confirm all 10 slides exist and the quality gates from Stage 3 pass.

**4. CRM tracking is set?**

Confirm every active investor has a next action and a next contact date. No investor in active conversations should have a blank next action field.

**5. Raise timeline is stated?**

Confirm they have a close target date and know the current commitments. Fundraises without deadlines drift.

---

## Reference files

- Full playbook: `playbooks/biz-dev/fundraising/README.md`
- Funding mechanisms: `playbooks/biz-dev/fundraising/funding-mechanisms.md`
- Traction by archetype: `playbooks/biz-dev/fundraising/traction-by-archetype.md`
- Round sizing: `playbooks/biz-dev/fundraising/round-sizing.md`
- Investor outreach template: `playbooks/biz-dev/fundraising/templates/investor-outreach.md`
- Follow-up template: `playbooks/biz-dev/fundraising/templates/follow-up.md`
