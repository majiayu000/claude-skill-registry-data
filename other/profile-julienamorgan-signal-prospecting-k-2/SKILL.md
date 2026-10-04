---
name: profile
description: >
  Researches the user's market, competitors, and competitive positioning to
  build a complete ICP profile. Shows findings for user approval before
  proceeding. Triggers: /profile, "research my market", "who are my
  competitors". Reads: ./gtm/company.md, ./gtm/icp.md. Writes: updates
  ./gtm/icp.md with competitive positioning. Standalone: yes (asks for
  domain if company.md missing).
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - WebSearch
  - WebFetch
---

# /profile — Market Research + Competitive Positioning

You research the user's market, find their competitors, map competitive
positioning, and build a complete picture of who they should target and why.
This is the foundation that makes every downstream skill smarter.

---

## Process

### Step 1: Load Context

Read `./gtm/company.md` and `./gtm/icp.md`.

If company.md doesn't exist, ask for their domain and do the research
inline (same as /start Step 3). Don't make them go back.

Show what you loaded:

```
  Loaded: {company name} ({domain}), selling to
  {buyer type}. Researching your market now.
```

### Step 2: Competitive Research

Use WebSearch to find:

**Direct competitors** (same product, same buyer):
- Search: `"{product category}" competitors alternatives`
- Search: `"{company name}" vs OR alternative OR competitor`
- Search: site:g2.com OR site:capterra.com "{product category}"
- **REQUIRED: Find 5-8 direct competitors.** Fewer than 5 = search
  harder or the category isn't understood yet.

**Adjacent competitors** (different product, same buyer) — REQUIRED,
not optional:
- What else does this buyer evaluate or buy from their quarterly budget?
- Who else is selling to the same title/company profile with a
  different pitch?
- What tools does the buyer already own that solve adjacent problems?
- Search: `"{buyer title}" stack OR "tech stack" OR "tools we use"`
- Search: `"{buyer title}" "bought" OR "evaluated" 2026`
- **REQUIRED: Find 3-5 adjacent competitors.** This block must
  appear in the output. If you cannot find 3, your research isn't
  done — keep searching. Do not skip the Adjacent Competitors
  section even if direct competitors are more obvious.

For each competitor, capture:
- Company name and domain
- Their positioning (headline from their site)
- Who they say they serve
- Key claims/differentiators
- Pricing if publicly available

### Step 3: Map the Competitive Landscape

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  COMPETITIVE LANDSCAPE: {category}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  DIRECT COMPETITORS
  ─────────────────────────────────────────────

  {Competitor 1} — {domain}
    Positioning: {their headline}
    Sells to: {their buyer}
    Key claim: {their main differentiator}

  {Competitor 2} — {domain}
    Positioning: {their headline}
    Sells to: {their buyer}
    Key claim: {their main differentiator}

  ...

  ADJACENT COMPETITORS
  ─────────────────────────────────────────────

  {Adjacent 1} — {domain}
    Different product, same buyer: {what they sell}

  ...

  YOUR WHITE SPACE
  ─────────────────────────────────────────────

  What you do that nobody else claims:
  {specific differentiators from company.md vs
  competitor positioning}

  Saturated claims (3+ competitors say this):
  {claims that are crowded}

  ──────────────────────────────────────────────
```

### Step 4: Refine the ICP

Based on competitive research, propose updates to icp.md:

```
  PROPOSED ICP REFINEMENTS
  ─────────────────────────────────────────────

  Buyer's Situation (updated):
  {more specific pain points now that we understand
  the competitive landscape}

  Why They'd Pick You Over {Top Competitor}:
  {specific positioning angle based on white space}

  Disqualifiers (who NOT to target):
  {companies that are a better fit for a competitor,
  or that don't have the pain you solve}

  ──────────────────────────────────────────────

  Does this look right? I can adjust before
  we lock it in and move to signal research.
```

### ✋ APPROVAL GATE

Wait for user confirmation before updating icp.md. They may:
- Confirm as-is → update and route to /signal-scout
- Correct something → re-research the corrected area via WebSearch,
  then re-present the full landscape with corrections highlighted.
  Don't just delete bad data — replace with better research.
- Add context you missed → incorporate and update
- Ask a question → answer it, then re-present for approval

Once approved, update `./gtm/icp.md` with:
- Competitive positioning section
- Refined buyer's situation
- Disqualifiers
- White space positioning

### Step 5: Route

```
  ──────────────────────────────────────────────

  ICP locked. Moving on to signal discovery.
```

**After the user approves and ICP is updated, automatically proceed
to run the /signal-scout process.** Do not wait for the user to type
"/signal-scout". Keep the momentum going — the user already said yes.

---

## Handling Questions and Tangents

If the user asks a question mid-flow ("what's a disqualifier?",
"why did you include X as a competitor?", "should I target SMB
or enterprise?"), answer clearly, then resume: "Good question.
[answer]. Here's the updated landscape — does this look right?"

If they want to explore something ("can you research company Y?",
"what about the European market?"), do the research and fold it
into the competitive analysis. Then re-present for approval.

The flow is a guide, not a cage. Answer questions, explore tangents,
and always bring it back to the approval gate.

---

## What Makes a Good Profile

- **Specific competitors, not categories.** "Gong.io charges $100/user/month
  and positions as revenue intelligence" not "there are several conversation
  intelligence tools."
- **White space from evidence.** Your differentiator should be something no
  competitor claims on their site, not something you assume.
- **Disqualifiers save time.** Knowing who NOT to target is as valuable as
  knowing who to target. If a competitor owns a segment, don't fight for it.
- **Buyer's situation, not buyer's demographics.** "VP Sales at a company
  that just hired 5 SDRs and needs to fill pipeline fast" not "VP Sales at
  a mid-market SaaS company."
