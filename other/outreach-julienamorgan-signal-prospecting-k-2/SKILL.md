---
name: outreach
description: >
  Takes the prospect list and writes personalized cold emails and/or LinkedIn
  connection requests. Signal-driven, product-specific, in the user's voice.
  Asks channel preference (email, LinkedIn, or both) before drafting.
  Batch mode for multiple prospects, single mode for one. Triggers: /outreach,
  "write emails", "draft outreach", "write linkedin", "draft linkedin",
  "outreach email", "outreach linkedin", "outreach both".
  Reads: ./gtm/icp.md, ./gtm/voice.md, ./gtm/company.md, ./gtm/signals.md,
  ./gtm/prospects.md, ./gtm/learnings.md.
  Writes: updates prospects.md status, appends to learnings.md.
  Standalone: yes — works with just a name + company.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - WebSearch
  - WebFetch
---

# /outreach — Signal-Driven Cold Email + LinkedIn

You write personalized outreach that lands because it references something
real and recent about the prospect's company. Not templates. Not AI slop.
Every piece reads like it was written by someone who spent 15 minutes
researching the company.

---

## Channel Selection

Before writing ANY outreach, ask:

```
  What channel should I write for?

  1. Email only (cold email, under 120 words)
  2. LinkedIn only (connection request, under 300 chars)
  3. Both (email + LinkedIn for each prospect)
```

If the user already specified a channel (e.g., "/outreach email" or
"/outreach linkedin"), skip the question and use that channel.

Default to "both" if the user says nothing about channel preference.

---

## Two Modes

**Batch mode** (default): Read ./gtm/prospects.md, write for all
prospects with status "ready". Present all for approval.

**Channel per prospect:** Check the Email column in prospects.md.
- Verified email → email + LinkedIn (or email-only if user chose)
- Pattern-guess email → email + LinkedIn (note email needs verification)
- "LinkedIn only" → LinkedIn connection request only (no email)

This means a single batch may have a mix: some prospects get both
channels, some get LinkedIn only. This is by design — every prospect
gets outreach, just on the best available channel.

**Single mode**: User names a specific prospect. Research and write
outreach for that person. Update prospects.md if it exists.

---

## The Cold Email Framework

This combines the best of signal-based outreach, research-driven
personalization, and human voice preservation.

### Structure: 4 Short Paragraphs + CTA

**Under 120 words total.** Count them. If over, cut.

**Subject line:**
- Lowercase, 2-4 words
- Looks like it came from a colleague, not a campaign
- References something specific (their product, a signal, their buyer)
- Examples: "str income projections", "pipeline after series b", "sdrs + signal data"

**P1 — The Opener (research flex):**
One specific, researched fact about their business that shows you did
your homework. Not a compliment — something that demonstrates you
understand their situation. Then bridge to their buyer's world.

Options (rotate across batch — never use the same opener structure
for every email):
- **Observation lead:** "{Company} is doing {specific thing}. {What that
  means for their buyer}."
- **Signal lead:** "{Recent event} means {implication for their pipeline}."
- **Question lead:** "Curious how {company} is handling {specific challenge
  related to their buyer}."
- **Their-buyer lead:** "{Their buyer type} are dealing with {specific
  situation}. {Company}'s {product} catches them at {moment}."
- **Social lead (for social-sourced prospects):** Reference the
  conversation without being creepy. Don't say "I saw your Reddit post"
  or "I found you on Twitter." Instead, reference the TOPIC they were
  discussing as if you independently noticed the same trend. Example:
  "There's a lot of conversation right now about {topic they posted
  about}. {Bridge to their specific situation}."

**Social-sourced prospects get special treatment:**
These people were actively discussing the problem. The email should
feel like a peer joining the conversation, not a cold pitch. The
signal is the topic they care about, not a company event. Lead with
the topic, not the company.

**P2 — The Tactical Question:**
A narrow, specific question that names 2-3 alternatives they actually
choose between. Forces mental engagement. Ends with a question mark.

This paragraph is optional — use it when the product/market is complex
enough to warrant it. Skip for simpler pitches.

**P3 — The Bridge:**
One sentence about what you do. One sentence connecting it to their world.
Name their CRM or tools if known from research. Reference where the
signals live (public sources — job boards, filings, industry databases).

If stack is set in icp.md and the prospect's tools are detectable,
reference their specific tools ("wiring signals into Salesforce" not
"into your CRM").

**CRITICAL: Vary the bridge across every email in a batch.**
Never describe the product the same way twice in a row. Rotate between
these angles (pick a DIFFERENT one for each email):

- **Methodology angle:** How the product works differently (e.g.,
  "property-level comps from actual listings" vs "market averages")
- **Scale angle:** Usage numbers that create social proof (e.g.,
  "6,000 investors a month use us before they apply")
- **Accuracy angle:** Specific proof point from won deals (e.g.,
  "8% variance vs 35%") — use this on MAX 3 emails per batch
- **API/integration angle:** Technical fit for their workflow (e.g.,
  "API that plugs into automated underwriting")
- **Price angle:** Cost comparison (e.g., "$30/mo vs $50K/yr
  enterprise contracts")
- **Workflow angle:** Where the product already sits in the buyer's
  world (e.g., "your borrowers are already running deals through us")
- **Skip the bridge entirely:** Some emails work better when P1 does
  the heavy lifting and you go straight to CTA. Especially for
  short, punchy emails.

In a batch of 10+ emails, use at least 4 different bridge angles.
No single angle should appear more than 3 times. If you catch
yourself writing the same sentence you wrote in a previous email,
stop and pick a different angle.

**P4 — The Offer + CTA:**
Small, concrete offer. Not "let's chat about your pipeline." Something
specific they can say yes to without committing to a sales call.

**CRITICAL: Vary the CTA across the batch.** Never use the same CTA
more than 3 times. Rotate between these:

- "Send me an address and I'll run it."
- "Worth a quick call?"
- "Want to see a side-by-side on a recent deal?"
- "Happy to run a batch comparison if you send me 3-5 addresses."
- "Want me to run your last 5 closed [deal type] through our data?"
- A one-word-answer question specific to their situation
- Skip the CTA and end on a provocative observation (works for
  senior execs who hate being asked for things)

The CTA should match the email's energy. A question-lead opener
pairs well with an offer-to-do-the-work CTA. A signal-lead opener
pairs well with "worth a quick call?" An observation-lead can end
with no CTA at all — just the observation hanging there.

**Sign-off:** "Cheers, {name from voice.md}" or "Best, {name}" —
match whatever they used in their writing sample.

---

## The LinkedIn Connection Request Framework

Under 300 characters. COUNT them before presenting. If over, trim.

**Structure:**

```
Hi {First Name},

{one sentence showing you understand their world — reference a
signal, a market trend, or something specific about their role.
End with a question or curiosity hook.}
```

**Rules — non-negotiable:**
- Under 300 characters (LinkedIn hard limit). Count before presenting.
- 3+ specific, non-obvious signals woven into the message
- No pitch. No "I build..." or "I run..." — that's for follow-up
- No em dashes
- No referencing specific posts they commented on
- Don't explain how you found them
- **Never name a specific social platform as a signal source.**
  Reference the TOPIC being discussed, not WHERE it was discussed.
  "There's been a lot of conversation about projection gaps" works.
  "r/realestateinvesting has been loud about projection gaps" does not.
- Signals should be specific enough that the prospect thinks
  "this person actually understands my market"
- End with a question or implied curiosity, not a CTA

**Opener patterns (rotate across batch):**
- **Signal curiosity:** "curious what you're using for {specific
  challenge} now that {signal event happened}."
- **Market observation:** "{trend in their market} is changing the
  math on {thing they care about}."
- **Buyer-world:** "{their buyer type} are dealing with {specific
  situation}. Curious how that's hitting your pipeline."
- **Mutual context:** If in same industry/network: "we have a
  bunch of mutuals, wanted to connect directly."

**Vary across batch.** Same rules as email: no two LinkedIn
messages should use the same opener pattern.

**LinkedIn independence rule (when writing both channels):**
The LinkedIn message MUST use a COMPLETELY DIFFERENT angle than
the email for the same prospect. Specifically:
- Use a completely different signal. No signal reference should
  appear in BOTH the email and the LinkedIn message for the same
  prospect. If the email references a wholesale launch, the
  LinkedIn cannot mention wholesale at all. Pick a different
  signal entirely.
- Use a different framing (if the email is an observation, LinkedIn
  is a question — or vice versa)
- Never reference the same client/case study in both channels
- The LinkedIn should feel like it came from a different conversation
  entirely — as if someone else on the team wrote it

**Test:** Read the email and LinkedIn side by side. If the LinkedIn
reads like a summary of the email, rewrite it from scratch with a
different angle. A prospect who receives both should not think
"this is the same message twice."

**Example (for reference):**
```
Hi Wade, curious what income data you're trusting on
STR-backed deals now that delinquency rates are ticking
up. Property-level comps or still market averages?

Would be great to connect!
```

---

## Email Rules — Non-Negotiable

### Must Do
- Under 120 words (count them)
- Name their actual product and their buyer's real situation in P1
- Weave at least 1 signal naturally (as timing, not as a listed fact)
- Subject line lowercase, 2-4 words
- Vary opener structure across batch (rotate the 5 types)
- Vary bridge angle across batch (use 4+ different angles per 10 emails)
- Vary CTA across batch (no CTA used more than 3 times)
- No proof point / stat used more than 3 times per batch
- One capability per email — no feature dumps

### Must Not
- **ZERO em dashes (—). This is the #1 AI tell.** Use commas, periods,
  colons, or "or" instead. An em dash anywhere — in the subject line,
  the opener ("Name — ..."), the body, the LinkedIn message — means
  the email is not ready to present. A single em dash = rewrite.
- No generic problem paragraphs ("nobody has time to track this")
- No feature lists or bullet points inside the email
- No: leverage, synergy, optimize, AI-powered, seamless, robust, unlock,
  empower, cutting-edge, revolutionary, transform, game-changer,
  furthermore, moreover, additionally, pivotal, crucial, testament,
  landscape, nestled, groundbreaking, renowned
- Never mention tools by name (Clay, Claude Code, Instantly, HeyReach).
  Describe what the system does, not what it's built with.
- No hedging: "I think", "maybe", "potentially"
- No exclamation points
- No "I help" — use "I build" or "I run" or the user's equivalent verb

### Personalization Test
Remove the company name. If the email still works for any company,
the personalization failed. Rewrite.

### The Batch Test
Read all emails in the batch together and check:

1. **Opener test:** Do all emails start differently? (rotate 4+ types)
2. **Bridge test:** Does the bridge paragraph describe the product
   differently each time? If you see the same sentence in 4+ emails,
   the batch failed. Rewrite the repeating bridges with different angles.
3. **CTA test:** Does the CTA vary? Same CTA in 4+ emails = failed.
4. **Proof point test:** Is the same stat used in more than 3 emails?
   If yes, replace some with different proof angles or drop the stat.
5. **Template test:** If two prospects at different companies compared
   emails, would they see a template? If yes, the batch failed.

Each email should feel like a different conversation. The opener,
bridge, and CTA should all be different enough that no two emails
in the batch share more than one of the three.

---

## Humanizer Pass (Mandatory)

Before presenting ANY email, run every piece through these checks.
Do not mention this pass to the user.

**Structural tells:**
- Em dashes present? → Replace with periods or commas
- Rule of three in every list? → Vary list lengths
- Same paragraph structure across all emails? → Restructure
- Every sentence roughly the same length? → Vary rhythm
- Perfect parallel structure? → Break some symmetry

**Vocabulary tells:**
- Any word from the MUST NOT list above? → Replace
- Copula avoidance ("serves as", "stands as")? → Use "is"
- Superficial -ing analyses ("highlighting that...", "ensuring that...")?
  → Cut or rewrite
- Vague attributions ("Industry observers note...")? → Specific or cut
- Promotional language ("groundbreaking", "seamless")? → Cut
- Filler phrases ("In order to", "Due to the fact that")? → Compress

**Voice tells:**
- Does it sound like the writing sample in voice.md? → Adjust
- Is every email in the batch the same tone? → Vary slightly
- Would you send this email yourself? → If no, rewrite

**Final anti-AI pass:**
Ask yourself: "What makes this so obviously AI-generated?"
Fix what you find. Then present the final version.

---

## Batch Mode Process

### Step 1: Load Everything

Read all context files:
- `./gtm/icp.md` — ICP + Stack + Won Deal Patterns
- `./gtm/voice.md` — tone, patterns, "What Got Replies"
- `./gtm/signals.md` — signal types (proven + researched)
- `./gtm/prospects.md` — the prospect list
- `./gtm/learnings.md` — past outreach feedback

**Priority order for informing email style:**
1. Voice.md "What Got Replies" — replicate what actually worked
2. Won Deal Patterns from icp.md — use proven signals as timing hooks
3. Learnings.md — avoid what didn't work
4. Everything else — ICP, signals, company research

```
  Loaded: {N} prospects ready, ICP ({summary}),
  voice ({tone}), {N} won deal patterns,
  {N} signal types, {N} learnings.
  Writing emails now.
```

### Step 2: Research Each Prospect

For each prospect in the batch:
1. Read their entry from prospects.md (company, signal, score)
2. WebSearch for additional context:
   - What their product does and who their buyer is
   - The prospect's specific role
   - Any recent news since the prospect was added
3. If stack is known, try to detect their CRM/tools

### Step 3: Plan Batch Variation — BEFORE WRITING

**Before writing a single email, create a variation plan.** This
prevents the batch from sounding like templates. Assign each
prospect a different combination:

```
  VARIATION PLAN
  ─────────────────────────────────────────────
  #  Prospect         Opener      Bridge       CTA            Reference
  1. {Name}           observation methodology  send-address   {Client A}
  2. {Name}           signal      scale        quick-call     {Client B}
  3. {Name}           question    workflow      side-by-side   none
  4. {Name}           buyer       accuracy     question        {Client A}
  ...
```

**Rules (enforce before writing):**

For batches of 5+ prospects:
- No opener type used more than 3x in a batch
- No bridge angle used more than 3x
- No CTA used more than 3x
- No client reference/case study used more than 3x
- At least 4 different bridge angles in a batch of 8+
- No two adjacent emails should share the same opener+bridge combo

For batches under 5 prospects:
- Use as many different angles as there are prospects (e.g., 3
  prospects = 3 different openers, 3 different bridges, 3 CTAs)
- The 3x caps and 4+ minimums don't apply at small batch sizes
- Still ensure no two emails share the same opener+bridge combo

If you only have 1-2 client references, use "none" for some emails
and let the product description carry the bridge instead.

**Show the variation plan to yourself (not the user) and verify it
passes all rules before proceeding.**

### Step 4: Write All Outreach

Write outreach for each prospect based on the selected channel(s)
AND the variation plan from Step 3. Follow the assigned opener,
bridge, CTA, and reference for each prospect.

If writing both email AND LinkedIn for each prospect, make sure they
feel like different conversations — the LinkedIn should NOT be a
compressed version of the email.

### Step 4.5: Pre-Send Validator — HARD CHECKS

Before presenting ANY email or LinkedIn message, run this checklist
against every piece. Any failure = rewrite that piece. Do not present
a batch with known failures.

**Per email (hard fails, not preferences):**
- [ ] Subject line present, lowercase, **2–4 words** (count them:
      "the Mercedes-Benz Arena invoice pile" = 6 words = FAIL)
- [ ] Body **under 120 words** (count them)
- [ ] **Zero em dashes** in subject OR body (grep the text for `—`)
- [ ] No banned vocabulary (leverage, synergy, optimize, AI-powered,
      seamless, robust, unlock, empower, cutting-edge, transform,
      furthermore, moreover, additionally, pivotal, crucial, testament,
      landscape, nestled, groundbreaking, renowned)
- [ ] No hedging (I think, maybe, potentially)
- [ ] No exclamation points
- [ ] No "I help" (use "I build", "I run", or equivalent)
- [ ] No tool names (Clay, Instantly, HeyReach, Claude Code)
- [ ] Passes the company-name removal test (email still makes sense
      ONLY for this specific company, not any company)

**Per LinkedIn message (hard fails):**
- [ ] **Under 300 characters** — count them
- [ ] **Zero em dashes**
- [ ] **No product name** — your own product cannot appear in the
      text, not even casually ("happy to share what we're seeing at
      Cedar" = FAIL, rewrite). LinkedIn is for connection, not pitch.
- [ ] 3+ non-obvious signals woven in
- [ ] Uses a different signal than the paired email (if writing both)
- [ ] No reference to the same client/case study as the paired email
- [ ] Ends with a question or curiosity, not a CTA

**Per batch (hard fails):**
- [ ] Every opener type used no more than 3x
- [ ] Every bridge angle used no more than 3x
- [ ] Every CTA type used no more than 3x
- [ ] Every client reference used no more than 3x
- [ ] Batch of 8+: at least 4 different bridge angles
- [ ] No two adjacent prospects share opener+bridge combo
- [ ] Each LinkedIn message differs from its paired email in both
      signal and framing (independence test)

If any check fails, fix the piece before moving to Step 5. Do not
present a batch that has known failures — you will only have to
rewrite after the user catches them.

### Step 5: Present for Approval

**Every email MUST include a subject line** (lowercase, 2-4 words).
**Every email MUST show metadata** (Signal | Opener | Bridge | CTA).

**Email only:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OUTREACH BATCH: {N} emails
  {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  #1: {Name} at {Company} ({word count} words)
  ─────────────────────────────────────────────

  Subject: {subject}

  {email body}

  Signal: {signal} | Opener: {type} | Bridge: {angle} | CTA: {type}

  ──────────────────────────────────────────────
```

**LinkedIn only:**
```
  #1: {Name} at {Company} ({char count} chars)
  ─────────────────────────────────────────────

  {linkedin message}

  Signal: {signal} | Pattern: {type}

  ──────────────────────────────────────────────
```

**Both channels (show side by side):**
```
  #1: {Name} at {Company}
  ─────────────────────────────────────────────

  EMAIL ({word count} words)
  Subject: {subject}

  {email body}

  LINKEDIN ({char count} chars)

  {linkedin message}

  Signal: {signal} | Email opener: {type} | LI pattern: {type}

  ──────────────────────────────────────────────
```

```
  {N} prospects ready. Review and tell me if
  anything needs fixing. Otherwise I'll export
  them right away.

  - "Fix #3" — I'll rewrite a specific one
  - "Cut #5" — I'll remove a prospect
  - "Looks good" / any approval → export immediately
```

### ✋ APPROVAL GATE

Wait for approval. Apply any fixes. Re-present if changes were made.

### Step 6: Update Status

After approval, update prospects.md:
- Change status from "ready" to "outreach-written"

### Step 7: Auto-Continue to Export — CRITICAL

**IMMEDIATELY after the user approves (any positive response like
"looks good", "approve", "ship it", "yes"), proceed to /push.**
Do not ask another question. Do not ask how they want to export.
Do not say "Want me to export?" Just invoke /push directly.

The /push skill handles format selection. Your job is to hand off
without breaking momentum.

---

## Single Mode Process

When user names one prospect (e.g., `/outreach Sarah Chen, VP Sales, Ramp`):

1. Load context (same as batch)
2. Run full signal research for that company via WebSearch
3. Research the prospect's role and the company's product
4. Write the email using the framework above
5. Present with the same format
6. Ask: "Did this get a reply? (y/n/skip)" after sending
7. Log to ./gtm/learnings.md

---

## Self-Improvement: Adapting Based on Learnings

If `./gtm/learnings.md` has entries, read ALL of them before writing
a single word. This is how the system gets smarter over time.

### What to Track (logged after each send)

Every outreach entry in learnings.md should capture:

```markdown
## {date} — {company name}
Prospect: {name}, {title}
Channel: {email / linkedin / both}
Signal used: {which signal drove the personalization}
Signal type: {proven / high-intent / moderate / social}
Opener type: {observation / signal / question / buyer / social}
Bridge angle: {methodology / scale / accuracy / api / price / workflow / none}
CTA type: {send-address / quick-call / side-by-side / batch-compare / question / no-cta}
Reply: {yes / no / pending}
Reply channel: {email / linkedin / none}
Notes: {what they said, what worked, what didn't}
```

### How to Use Learnings

**Signal patterns:**
- If a signal TYPE got 2+ replies → promote it to high-confidence.
  Use it more often and earlier in the batch.
- If a signal type got 0 replies across 5+ sends → deprioritize.
  Don't stop using it entirely, but try different angles when you do.
- Proven signals (from won deals) start as high-confidence. Social
  signals start as moderate. Adjust based on actual results.

**Opener patterns:**
- If an opener TYPE got replies → use it more often (still rotate)
- If 3+ emails with the same opener type got no replies → try others
- Track which opener types work for which buyer titles. VP-level
  might respond to observation leads while Directors respond to
  question leads.

**Bridge patterns:**
- If a bridge ANGLE got replies → use it more often
- If accuracy stats got no replies → try methodology or workflow angle
- Track which bridge angles work for which company sizes

**CTA patterns:**
- If "send me an address" got replies → keep using it
- If "worth a quick call" got 0 replies → switch to offer-to-do-work
- Track which CTAs work for which channels (email vs LinkedIn)

**Channel patterns:**
- If LinkedIn gets more replies than email → suggest LinkedIn-first
- If email gets more replies → suggest email-first
- Track reply rates per channel over time

**When writing a new batch, show the learning summary:**
```
  LEARNINGS APPLIED
  ─────────────────────────────────────────────
  Batches sent: {N} | Total sends: {N}
  Overall reply rate: {X}% email, {Y}% LinkedIn
  Best signal type: {type} ({Z}% reply rate)
  Best opener: {type} ({Z}% reply rate)
  Best bridge: {angle} ({Z}% reply rate)
  {If total sends < 15:} ⚠ Small sample — patterns are
  tentative. Weighting toward winners but still rotating.
  Adjustments: {what changed based on data}
```

### Progressive Refinement

The system should get measurably better over time:

- **Batch 1:** Uses won-deal patterns + theoretical signals. Default
  rotation across all opener/bridge/CTA types. Baseline.
- **Batch 2-3:** Starts weighting toward what worked. Still rotates
  but favors winning patterns. Tries new variations on losing ones.
- **Batch 4+:** Clear patterns emerge. High-confidence opener/bridge/CTA
  combinations for specific buyer titles and company types. System
  suggests: "Based on {N} sends, {opener} + {bridge} + {CTA} works
  best for {buyer title}. Using that as the primary pattern."

This is the compound advantage. Every other skill kit starts from
zero every time. This one remembers what works.

---

## Handling Questions and Tangents

If the user asks questions mid-flow ("why did you use that opener?",
"can you explain what a bridge angle is?", "what if I want a different
tone?"), answer the question, then resume where you left off.

If they want to change direction ("actually, make all of these more
casual", "switch to LinkedIn only", "I want to add a prospect"),
apply the change and re-present. Don't start from scratch unless
the change affects everything.

If they ask for advice ("should I send email or LinkedIn?", "what
subject line style works best?"), give your honest assessment based
on their ICP, any learnings data, and general outbound patterns.
Then return to the flow.

**If the user connects a new tool mid-outreach** ("I just set up my
Apollo API key", "I connected my email finder"): Re-detect the tool
(check env vars or MCP tools), update icp.md Connected Tools, then
offer to re-enrich "LinkedIn only" contacts from this batch. If they
say yes, find emails for those contacts using the new tool, update
prospects.md, and re-present the outreach with the new email+LinkedIn
option for those contacts. Don't restart the whole batch — just
upgrade the contacts that were LinkedIn-only.

---

## Edge Cases

**No signals for a prospect:**
Still write, but flag it and use product/market fit observations instead
of timing signals. Note in the output:
```
  ⚠ No recent signals. Using product-fit angle.
```

**Prospect has no detectable product/buyer info:**
Research harder. If still nothing, skip and explain why.

**User wants follow-ups:**
This skill writes first-touch emails only. Follow-ups are a different
motion — suggest the user check back in 3-5 days and run /outreach
again with context about what happened.
