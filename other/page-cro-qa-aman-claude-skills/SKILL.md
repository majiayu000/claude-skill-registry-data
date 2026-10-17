---
name: page-cro
description: Diagnose why a landing page, homepage, pricing page, or signup form is not converting, and produce a ranked fix list with a test plan. Runs a structured audit across motivation, value clarity, friction, anxiety, and CTA hierarchy rather than giving generic design opinions. Use when the user says "why isn't this page converting", "improve our conversion rate", "CRO", "conversion audit", "this page isn't working", "high traffic low signups", "people bounce", "review our landing page", or shares a URL and asks what is wrong with it. For rewriting the words only, see copy-review. For writing a new page from scratch, see landing-page-writer. For the statistics of running the test afterwards, see growth-experiment.
metadata:
  grounded_in:
    - "Don't Make Me Think - Steve Krug"
    - "Influence - Robert Cialdini"
    - "Tiny Habits - BJ Fogg"
    - "MECLABS conversion sequence heuristic"
  reads:
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/kpis.md
    - knowledge/learnings.md
  writes:
    - output/page-cro/
---

# page-cro

Diagnoses a page that is not converting. Produces a ranked list of fixes with an expected direction and a test plan, not a list of design preferences.

The discipline this skill enforces: **every finding names which of the five conversion factors it damages, and no fix is recommended without saying how it would be measured.**

## Framework

Conversion is not one property. It is five factors, and a page usually fails on one or two. Naming which one keeps the audit from becoming a redesign.

| Factor | Question | Grounded in |
|---|---|---|
| **Motivation** | Does the visitor already want this, and did the page meet them where their intent was? | MECLABS conversion sequence heuristic |
| **Value clarity** | Within five seconds, can they say what this is, who it is for, and what it does for them? | Krug, *Don't Make Me Think* |
| **Friction** | How much effort does the next step cost, in fields, clicks, thinking, and time? | Fogg Behavior Model: behaviour needs motivation, ability, prompt |
| **Anxiety** | What are they afraid of at the moment of clicking? | Cialdini on trust and social proof |
| **Prompt** | Is there one obvious next action, visible without hunting? | Fogg, and CTA hierarchy practice |

Motivation is mostly bought upstream, in the channel and the audience. If motivation is the failure, no button colour fixes it, and the skill must say so rather than offering cosmetic fixes.

## Process

1. **Get the page.** A URL (use WebFetch), pasted HTML or copy, or a screenshot. If a URL is given, fetch it. If fetching fails, ask for pasted content rather than guessing from the domain name.

2. **Get the numbers, or mark their absence.** Ask for: current conversion rate, traffic volume, primary traffic source, and the conversion event. If the user does not have them, continue but stamp the output `DIAGNOSIS UNVALIDATED - no baseline`. A CRO audit without a baseline is a design opinion, and it should be labelled as one.

3. **Load context.** Read `knowledge/icp/personas.md` for who this is aimed at, `knowledge/markets/positioning.md` for what it should be claiming, and `knowledge/learnings.md` for anything already tested.

4. **Run the five-second test first, before reading the page properly.** From the first screen only, write down what you think this is, who it is for, and what it costs. Then read the rest and compare. Any gap between the two is a value-clarity finding, and it is usually the most valuable output of the whole audit.

5. **Audit each factor** using the checklists below.

6. **Rank findings** by expected impact multiplied by confidence, not by how easy they are to fix.

7. **Build the test plan** for the top three.

8. **Save and offer next steps.**

## Factor checklists

### Motivation
- Where does traffic come from, and does the page match the promise that brought them? A paid ad promising a price and a page that hides pricing is a motivation mismatch, not a copy problem.
- Does the page address the persona's trigger event from `knowledge/icp/personas.md`?
- Is the visitor problem-aware, solution-aware, or product-aware? A product-aware page shown to problem-aware traffic fails regardless of quality.

### Value clarity
- Headline: does it state an outcome, or a category? "Marketing automation platform" is a category.
- Is the audience named, explicitly or unmistakably?
- Is there a visual or demonstration of the product in the first screen?
- Could a competitor use this headline unchanged? If yes, it is not positioning.
- Reading level of the first screen: plain and scannable, or dense?

### Friction
- Count the form fields. Every field beyond the minimum needs a reason.
- Count clicks from landing to conversion.
- Is anything demanded before value is shown, such as a signup wall on a pricing page?
- Cognitive friction: how many decisions must the visitor make? Plan choice, term choice, seat count, add-ons all compound.
- Mobile: does the primary action fit on the first screen at phone width?

### Anxiety
- What is the visitor risking: money, time, data, their credibility internally?
- Is there proof near the action, not just at the bottom? Proof at the top of the page and a button at the bottom is proof in the wrong place.
- Are the specific objections from `knowledge/icp/personas.md` answered anywhere?
- Trust signals present: named customers with real logos, specific testimonials rather than adjectives, security or compliance marks, a visible refund, cancellation or exit path.
- Is pricing findable? Hidden pricing is an anxiety cost that most pages underestimate.

### Prompt
- Count distinct CTAs. More than two competing actions means no primary action.
- Is the primary CTA visually dominant, and repeated after each major section?
- Does the button text state the outcome ("Get the template") rather than the mechanic ("Submit")?
- Is there a low-commitment secondary path for visitors not ready to buy?

## Output format

```markdown
# Page CRO audit: [page name]

**URL:** [url]
**Conversion event:** [what counts as a conversion]
**Baseline:** [rate, traffic, source] | or: DIAGNOSIS UNVALIDATED - no baseline
**Audited:** DD-MM-YYYY

## Five-second test
**What I understood from the first screen alone:**
- What it is: [answer]
- Who it is for: [answer]
- What it costs: [answer]

**What the page actually offers:** [after full read]
**Gap:** [the difference, or "none - the first screen is clear"]

## Factor scores
| Factor | Score | One-line reason |
|---|---|---|
| Motivation | N/5 | |
| Value clarity | N/5 | |
| Friction | N/5 | |
| Anxiety | N/5 | |
| Prompt | N/5 | |

**Primary failure:** [the lowest-scoring factor, named plainly]

## Findings, ranked

### 1. [Finding] - [FACTOR] - impact [H/M/L], confidence [H/M/L]
**What I see:** [specific element, quoted or described by location]
**Why it costs conversions:** [mechanism, one or two sentences]
**Fix:** [specific change]
**How we would know:** [the metric that should move, and in which direction]

[repeat]

## Test plan for the top three
| # | Change | Hypothesis | Metric | Minimum runtime |
|---|---|---|---|---|
| 1 | [change] | If [change] then [metric] improves because [reason] | [metric] | [time or sample] |

**Do not call any of these tests early.** Run `/growth-experiment` to set the sample size and stopping rule before launching.

## What I could not assess
[anything needing analytics, session recordings, or user testing that a page read cannot answer]
```

## Self-check before saving

- The five-second test was written before reading the full page, not reconstructed after
- Every finding names exactly one primary factor
- Every finding says how it would be measured
- No finding is a personal design preference. If it cannot be tied to a factor and a metric, cut it
- If motivation is the primary failure, the output says plainly that on-page fixes will not solve it
- Findings are ranked by impact times confidence, and the ranking is not just the order they were found
- If no baseline was supplied, the `DIAGNOSIS UNVALIDATED` stamp is present at the top

## Rules

- **Never predict a specific percentage lift.** "This should increase conversions by 30%" is fabrication. Say the expected direction and the confidence, and let the test produce the number.
- Never recommend more than five changes at once. A page with fifteen simultaneous changes cannot be learned from.
- Do not invent benchmark conversion rates. If the user asks whether their rate is good, say what it depends on and ask for their own historical baseline, which is the only comparison that is reliably valid.
- If the page is genuinely good, say so and point upstream at traffic quality or offer. Manufacturing findings on a solid page wastes a test cycle.
- Save to `output/page-cro/<DD-MM-YYYY>-<page-slug>.md`.

## Related skills

- `/copy-review` for the words once the structural problems are named
- `/landing-page-writer` if the verdict is that the page needs rebuilding rather than fixing
- `/ab-copy-writer` to generate variants for the top finding
- `/growth-experiment` to set sample size and stopping rules before running the test
- `/brand-context` if `knowledge/icp/personas.md` is missing, since the anxiety pass depends on real objections

## What this skill cannot know

- How the page behaves on real devices and at real speeds
- What users actually do on it, absent session recordings or analytics
- Whether traffic quality, rather than the page, is the constraint
- Whether a fix that helped another page will help this one, since audiences differ
