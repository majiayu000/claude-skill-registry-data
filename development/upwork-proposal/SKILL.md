---
name: upwork-proposal
version: 1.0.0
description: |
  Win Upwork proposals. Given a job description (and optionally the client's first
  reply message), produce a 120-180 word proposal that mirrors the JD, anchors price,
  weaves real proof, asks 2-3 sharp questions, and closes with a presumptive CTA.
  Also flags red flags, recommends Connects/boost decision, and suggests Loom or
  speculative micro-deliverable when ROI fits. Tuned for SkynetLabs:
  WordPress, n8n, AI integrations, AEO/SEO, Shopify, WhatsApp bots, healthcare,
  wellness funnels.
  Trigger when user says: "write upwork proposal", "upwork bid", "/upwork-proposal",
  pastes an Upwork JD, or asks to draft a proposal/cover letter for a freelance brief.
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebFetch
  - AskUserQuestion
---

# Upwork Proposal Skill — SkynetLabs Edition

Goal: produce proposal client wants to reply to. Not CV-dump. Not generic. Not "I hope this finds you well."

## Inputs

User provides ONE or BOTH of:

1. **Upwork JD** (full job post text)
2. **Client message** (their first DM/reply after invite)

If only JD given → write proposal.
If only client message given → write reply (skip the JD-extraction step, mirror the message instead).
If both → write proposal that anticipates the reply concerns.

If user gives neither, ask: "Paste the JD (or invite message). Anything you already know about the client/budget?"

## Workflow

### Step 1 — Red-flag scan (skip-or-bid decision)

Before writing, check JD for:

- Payment method **not verified** → skip if job <$1K
- "Send a sample first" / "do a test task" → free-work scam, skip
- Budget <20% of stated scope ($50 for "build me Uber") → skip
- "Communicate on Telegram/WhatsApp first" → TOS violation + scam pattern, skip
- 0 hires + posted >2 weeks → ghost client, deprioritize
- Spelling/grammar inconsistencies → AI-generated scam, skip
- "NDA before any conversation" → skip
- "Urgent — need today" + no budget listed → panic client, churn risk
- Hire rate <30% with 50+ jobs posted → shopper not buyer
- Vague ("build me an app like Uber") → unscope-able, skip

**Output a 1-line verdict before the proposal:**
`Verdict: BID / BID-WITH-CAUTION / SKIP — reason.`

If SKIP, stop. Do not draft.

### Step 2 — Extract from JD

Pull these 8 signals (mentally, not in output):

1. **Stated problem** — what they typed
2. **Hidden problem** — underneath (e.g., "need fast site" = previous dev ghosted)
3. **Tech stack constraints** — named tools = non-negotiable
4. **Decision-maker tells** — "we / my team / founder / agency"
5. **Budget signal** — range, "open", or absent
6. **Timeline urgency** — "ASAP", "no rush", date-anchored
7. **Past-pain phrases** — "last freelancer", "tried before", "didn't work"
8. **Success metric** — revenue / speed / launch / compliance

Reflect **2 of these** in the opener. Never all 8 (parrot territory).

### Step 3 — Pick the proof point (Profile→Proposal bridge)

From your real builds, weave ONE per plan-bullet. Rotate from this bank:

| Niche            | Proof point                                                                | Live URL / receipt                   |
| ---------------- | -------------------------------------------------------------------------- | ------------------------------------ |
| WordPress        | A custom companion plugin, HMAC+replay auth, kills ZIP uploads             | your-personal-site.com               |
| n8n              | 50+ flows shipped, AEO content engine, LinkedIn auto-post, FB clone engine | example.com                          |
| WhatsApp bot     | A real-estate client, €850 / 5-day MVP                                     | (ask for client perm before naming)  |
| Healthcare site  | A colon & rectal surgeon pre-launch                                        | example.vercel.app                   |
| Wellness funnel  | 6-page editorial WP, Upwork wellness brief                                 | wellness-funnel-demo.vercel.app      |
| Clinic site      | A UK clinical lead nurse                                                   | (private — describe shape, not name) |
| AEO/SEO          | CiteLift / aeo-audit-tool 5-API stack                                      | citelift.app (in build)              |
| Local-services   | A home-services NYC quote-funnel                                           | (private — case study OK)            |
| Demo-first habit | Builds free demo before pitch                                              | shows in pattern, not bullet         |

**Rule:** ONE proof per bullet, woven, not stacked. Live URL > screenshot > claim. Never list >2 URLs in proposal — clients click 1.

### Step 4 — Decide: Loom and/or speculative micro-deliverable

**Loom worth it when:** job ≥$1K, scope is concrete, client has ≥1 prior hire. 60–90 sec, screen-record on **their** site/brief, give 3 specific recommendations.

**Speculative demo worth it when:**

- job ≥$500
- scope concrete (a site, a flow, a funnel)
- client payment-verified
- you can ship demo in <2 hrs

**Neither when:** vague JD, $50 budgets, "send samples first" requests (free-work scam), 0-hire ghost clients.

If recommended, say so in **Meta** block (after proposal). Don't actually build the demo until user confirms.

### Step 5 — Draft proposal (120–180 words)

Skeleton:

1. **Hook** (2 lines, ≤25 words line 1) — mirrors job, never starts with "I"
2. **3-bullet plan** — each bullet = action + "Done = ..." outcome + woven proof
3. **1 proof artifact** — inline link, not "see portfolio at end"
4. **2-3 sharp questions** — micro-demo of expertise (see Q-bank below)
5. **Price anchor** — concrete number + scope + timeline
6. **Presumptive CTA** — choice-based ("two ways to start: A or B"), signed first name only

### Hook templates (pick the fit)

- **Mirror + claim:** "[Specific JD pain] is almost always [diagnosis] — fixable in [timeline]."
- **Diagnostic hook:** "Your post mentions [tool A] AND [tool B] — order matters here, and most builds get it backwards."
- **Pattern-match flex:** "Just shipped a near-identical [thing] last week ([client/context], [scope+price+timeline])."
- **Specific compliment:** "Your brief is already 80% spec'd — rare. Only gap I see is [X]."

**Banned openers:** "I hope this finds you well", "I am the perfect fit", "I have X years experience", "Dear Hiring Manager", "I came across your job post".

### Question bank (pick 2-3, never lazy)

**Lazy (banned):** "What's your budget?" "When do you need this?" "What's the goal?"

**Sharp:**

- "Is the [WhatsApp bot / chat flow] routing to a human after qualification, or fully autonomous?"
- "n8n self-hosted or cloud? (Changes credentials approach.)"
- "Existing GA4 + Search Console access, or do we set up tracking from zero?"
- "Shopify theme — Dawn-based or custom/legacy? (Affects upgrade path.)"
- "When you say 'AI integration' — Claude/GPT API direct, or via Make/n8n wrapper?"
- "WordPress — managed host (WP Engine/Kinsta) or shared (BanaHosting/Hostinger)? Affects deploy method."
- "Is the success metric leads, bookings, or revenue? Build sequencing changes."

### Pricing language (anchor, never apologize)

- **Anchor:** "$2,500 fixed for the scope you described — [scope items], [revisions], [timeline]. Done = [observable artifact]."
- **Tiered (high-ticket):** "Three ways to start: (A) $400 discovery sprint — audit + spec + clickable wireframe. (B) $1,800 build — implements A. (C) $3,500 build + 30 days post-launch support."
- **"What's your budget?" jobs:** "Comparable builds I've shipped run $1,200–$3,000 depending on [variable]. Happy to scope to either end once I know [Q1, Q2]."
- **Hourly defense:** "$65/hr, capped at 25 hrs for this milestone — over is on me."
- **Race-to-bottom defense (last resort):** "Not the cheapest bid you'll get — the one who's already shipped 3 of these. If lowest price is the brief, no hard feelings."

### Closing CTA — presumptive close

**Banned:** "Looking forward to hearing from you", "Let me know if interested", "Hope to chat soon", "Best regards / SkynetLabs Team."

**Alive:**

- "Two ways to start: 15-min call this week, or I send a 2-slide plan tomorrow — your pick. — [Your Name]"
- "Want the demo URL? Reply 'yes' and it's in your inbox in an hour."
- "If [Q1] is yes, discovery doc to you tomorrow. — [Your Name]"
- "Worth a 10-min call Thursday? I'll come with the wireframe pre-built."

### Step 6 — Output format

Always output in this structure:

```
═══════════════════════════════════════
VERDICT: <BID / BID-WITH-CAUTION / SKIP>
Reason: <one line>
═══════════════════════════════════════

PROPOSAL (paste-ready):
---
<the proposal — 120-180 words>
---

META:
- Word count: <n>
- Connects: <est cost> | Boost: <YES if 9/10 fit + verified + ≥$1K else NO>
- Loom: <YES + what to show / NO>
- Speculative demo: <YES + what to ship / NO>
- Red flags found: <list or "none">
- Anticipated client objections: <2-3>
- If they reply "what's your timeline / when can you start": <prepared answer>
═══════════════════════════════════════
```

## Reply mode (client already messaged back)

If user pastes a client reply, switch to **reply mode**:

- Mirror their last message in line 1 (quote a phrase or restate their concern)
- Answer ONE concern fully, not all of them (avoid wall-of-text)
- Always end with ONE forward-motion question
- Length: 60–120 words, plain text, no bullets unless they used bullets
- Match their formality level (formal client → formal you; casual → casual)

## Hard rules

- Never start a proposal with "I"
- Never write more than 200 words
- Never list more than 2 URLs
- Never use "Looking forward to hearing from you"
- Never quote a price as a range without the upper-bound logic ("$X–$Y depending on Z")
- Never offer free trial week / first task free / money-back guarantee
- Never lie about a build (no fake metrics, no invented clients) — see [feedback-no-fake-claims](../../projects/C--Users-info/memory/feedback-no-fake-claims.md)
- If naming a real client — only first names or shape ("a real-estate developer", "a UK clinical nurse"), never full client identifiers without permission

## Quality checklist (run before delivering)

- [ ] Opener doesn't start with "I"
- [ ] Opener mirrors ≥1 specific JD detail (not just rephrases JD)
- [ ] 3 plan bullets, each with "Done = ..." or proof link
- [ ] Concrete price stated
- [ ] 2-3 sharp questions, no lazy ones
- [ ] CTA is presumptive, not "looking forward"
- [ ] Word count 120-180
- [ ] Signed "— [Your Name]" not "Best, SkynetLabs Team"
- [ ] No fake claims / invented metrics
- [ ] Loom + spec-demo decisions stated

## Connects economics (for Boost decision)

- $0.15/Connect. Standard bid = 6C ($0.90). Competitive = 10–16C.
- Plus plan: $19.99/mo, 100 Connects. Worth past ~50 bids/mo.
- **Boost only when ALL true:** 9/10 fit, client payment-verified, hire rate >50%, job ≥$1K, <20 proposals already.
- Healthy reply rate: 20–35%. Below 15% = hook or targeting wrong, not volume.

## When to invoke

User says any of:

- "write upwork proposal" / "upwork bid" / "draft a proposal for this Upwork job"
- "/upwork-proposal"
- pastes an Upwork JD
- "client just messaged back, what do I say"
- "help me reply to this Upwork client"

## When NOT to invoke

- Generic cover letter requests (LinkedIn, email outreach, RFP) — different game
- Existing client comms inside an active Upwork contract — that's not a proposal
- Fiverr gig descriptions — different platform mechanics

---

**Reference:** Full research synthesis in `playbook.md` (loaded only if user asks "why" or wants deeper teardown).
