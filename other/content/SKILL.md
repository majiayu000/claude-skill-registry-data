---
name: content
description: 'Run the Markster OS content playbook. CHECK prerequisites (ICP, messaging guide, platform, time), DO theme definition + 30-day calendar + writing + distribution, VERIFY output before declaring done. Routes through ScaleOS G2 Warm.'
---

# Content Operator

---

## CHECK

Do not proceed past any failed check.

**1. F1 complete?**

Read `company-context/audience.md`.

Required before this skill runs:
- ICP defined with company type and specific pain
- Decision-maker title named
- Buying trigger identified

If missing: "Content without ICP produces generic output that your buyer does not recognize themselves in. Open `methodology/foundation/F1-positioning.md` and complete it first."

**2. Messaging guide complete?**

Read `company-context/messaging.md` and `methodology/foundation/messaging-guide.md`.

Required:
- Problem statement in the buyer's words (not category descriptions)
- Mechanism (why this problem exists or has gotten worse now)
- At least one specific proof point with company type, result, and timeframe

If missing: "The messaging guide defines the language the content must use. Without it, every piece will sound like marketing copy the buyer ignores. Complete `methodology/foundation/messaging-guide.md` first."

**3. Platform and time commitment**

Ask the user:
- What platform do they primarily publish on? (LinkedIn, website, newsletter, X?)
- How much time per week can they dedicate to content? (30 min / 1 hour / 2+ hours)

This determines calendar density and format mix. Do not generate a calendar without knowing the platform.

**4. Your archetype**

Before writing content, confirm the business type. Route to the correct segment file.

| Your type | Read this first |
|-----------|----------------|
| B2B SaaS, devtools, marketplace | `playbooks/segments/startup-archetypes/` |
| Agency, consulting, IT/MSP, advisory | `playbooks/segments/service-firms/` |
| Residential or commercial services | `playbooks/segments/trade-businesses/` |

The archetype determines which GOD Engine bricks matter most and what the G2 Warm motion looks like for your category.

---

## DO

Run these four steps in order. Do not skip a step unless the user confirms it is already done.

### Step 1: Define core theme

Help them define their theme as a one-sentence statement:

> "I write about [specific intersection of ICP problem + your unique perspective]."

Push back if the theme is too broad. Use these as failure examples:
- "AI and marketing" -- not a theme
- "Business growth tips" -- not a theme
- "Why B2B service firms under 20 people should treat content as a sales warmer, not a brand play" -- this is a theme

The theme must:
- Be specific enough that their ICP recognizes themselves in it
- Have a point of view that goes beyond category average
- Be something they have evidence for (data, client results, direct experience)

If they cannot produce a theme that passes these three tests, do not move to Step 2. The calendar will be useless without it.

### Step 2: Build a 30-day calendar

Generate 30 days of specific content ideas scaled to their time commitment:

| Time per week | Mix |
|---------------|-----|
| 30 min | 8-10 short posts (under 150 words) |
| 1 hour | 4-6 LinkedIn posts + 4-6 short hooks |
| 2+ hours | 2 long-form + 6-8 LinkedIn posts + 6-8 short hooks |

For each calendar item, define:
- Specific topic (not "content marketing tips" -- something concrete and named)
- Core insight (one sentence -- what is the non-obvious thing?)
- Connection to ICP's situation (why does this matter to them right now?)
- Format (long-form / LinkedIn post / short hook)

### Step 3: Write

**For long-form content:** Use `playbooks/warm/content/long-form/templates/article.md`

**For short-form content:** Use `playbooks/warm/content/short-form/templates/linkedin-post.md`

Apply these rules to every piece:
- First line must earn the scroll -- do not warm up, do not start with "I want to talk about"
- Problem-first framing -- ICP's situation before your solution
- Use buyer verbatims from the messaging guide -- their language, not yours
- No em dashes
- Short paragraphs (3-4 sentences max)
- One CTA per piece
- No category claims ("AI-powered," "data-driven," "full-service")

### Step 4: Distribute

Remind them: publishing is not distribution.

Distribution plan for every piece published:
1. Post natively on primary platform
2. Send to email list (even if under 100 subscribers)
3. Share in 1-2 relevant communities where ICP is active
4. Repurpose each long-form piece into 3-5 short-form posts
5. Reference in cold outreach as proof of expertise and point of view

---

## VERIFY

Before this session ends:

**1. Theme passes the specificity test?**

Read the theme out loud. Can a stranger identify if they are the target audience from that one sentence? If not, rewrite.

**2. 30-day calendar exists?**

Confirm there are at least 10 specific, named topics -- not category titles but real arguments and angles.

**3. First piece written?**

Do not leave the session with only a calendar. Write at least the first piece before closing. Momentum beats planning.

**4. Distribution plan set?**

Confirm they know exactly what happens the day they publish. Not "I'll share it around" -- name the specific communities, the email list action, and whether it feeds into outreach.

**5. Metrics baseline set?**

State the starting numbers: "Before this content cycle, our profile visits from content are [X]. Success this month = at least [Y] inbound inquiries sourced from content."

Monthly metrics to track:
- Impressions per post
- Comments per post
- Profile visits from content
- Inbound inquiries sourced from content

---

## Reference files

- Full playbook: `playbooks/warm/content/README.md`
- Long-form guide: `playbooks/warm/content/long-form/README.md`
- Short-form guide: `playbooks/warm/content/short-form/README.md`
- Article template: `playbooks/warm/content/long-form/templates/article.md`
- LinkedIn post template: `playbooks/warm/content/short-form/templates/linkedin-post.md`
- Messaging guide: `methodology/foundation/messaging-guide.md`
