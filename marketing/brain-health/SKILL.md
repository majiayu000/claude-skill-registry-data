---
name: brain-health
version: 1.0.0
description: "Check which brain files are complete, incomplete, or empty, and get recommendations for what to fill next. Trigger with /brain-health or when the user mentions 'brain status,' 'brain health,' 'what's missing in my brain,' 'brain completeness,' 'which brain files,' or 'brain check.' Also runs automatically at the end of /setup."
---

# Brain Health Check

Scan all brain files, report completeness, and tell the user exactly which skill to run next to fill gaps.

---

## Workflow

### Step 1: Scan brain files

Read every file in `brain/` and count `[FILL IN]` and `[VERIFY]` placeholders in each. Also check for files that exist in the expected set but are missing from the directory.

**Expected brain files:**

| File | Category |
|------|----------|
| `truth.md` | Core |
| `positioning-and-messaging.md` | Core |
| `personas.md` | Core |
| `competitive.md` | Core |
| `capabilities.md` | Core |
| `use-cases.md` | Core |
| `voice-and-tone.md` | Brand |
| `voice-samples.md` | Brand |
| `brand-guide/brand-guide.md` | Brand |
| `audience-language.md` | Supporting |
| `customer-journey.md` | Supporting |
| `market-signals.md` | Supporting |
| `qualifying-questions.md` | Supporting |
| `tactical-assets.md` | Supporting |

### Step 2: Calculate completeness

For each file, determine status:

- **Complete** — zero `[FILL IN]` and `[VERIFY]` placeholders remaining
- **Partial** — some placeholders filled, some remaining. Show the count of remaining placeholders.
- **Empty** — all or nearly all fields are still `[FILL IN]` (untouched template). Treat a file as Empty if it has no substantive content beyond the template boilerplate.
- **Missing** — file doesn't exist in `brain/`

### Step 3: Present the dashboard

Display a health report. Use a simple text-based progress bar for each file.

```
Brain Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Files
  truth.md                     ██████████  Complete
  positioning-and-messaging.md ████░░░░░░  18 fields remaining
  competitive.md               ██████░░░░  6 fields remaining
  personas.md                  ████░░░░░░  9 fields remaining
  capabilities.md              ░░░░░░░░░░  Empty
  use-cases.md                 ░░░░░░░░░░  Empty

Brand
  voice-and-tone.md            ░░░░░░░░░░  Empty — run /tone-mapping
  voice-samples.md             ░░░░░░░░░░  Empty — run /tone-mapping
  brand-guide.md               ████████░░  3 fields remaining

Supporting Files
  audience-language.md         ░░░░░░░░░░  Empty
  customer-journey.md          ░░░░░░░░░░  Empty
  market-signals.md            ░░░░░░░░░░  Empty
  qualifying-questions.md      ░░░░░░░░░░  Empty
  tactical-assets.md           ░░░░░░░░░░  Empty

Overall: 1 of 14 files complete
```

### Step 4: Recommend next actions

After the dashboard, recommend the top 3 files to fill next, in priority order. Use this priority logic:

1. **Core files first, supporting files later.** Core files feed every skill; supporting files feed specialized skills.
2. **Within core, prioritize by downstream impact:**
   - `truth.md` (everything depends on this)
   - `positioning-and-messaging.md` (messaging pillars feed capabilities, use-cases, content)
   - `competitive.md` (feeds competitor pages, battlecards)
   - `personas.md` (feeds content targeting)
   - `capabilities.md` (feeds feature pages, datasheets)
   - `use-cases.md` (feeds case studies, landing pages)
3. **Brand files when core is >60% done.**
4. **Supporting files when core is >80% done.**

For each recommendation, specify the skill to run:

| Brain File | Skill to Run | What to Prepare |
|-----------|-------------|-----------------|
| `truth.md` | Manual entry or `/setup` | Company facts, product details, customer list |
| `positioning-and-messaging.md` | `/product-marketing` | Knowledge of market problem, competitors, differentiation |
| `competitive.md` | `/product-marketing` | Competitor names, why you win/lose against each |
| `personas.md` | `/product-marketing` | Buyer titles, their problems, what they care about |
| `capabilities.md` | `/product-marketing` | Product features organized by messaging pillar |
| `use-cases.md` | `/product-marketing` | Customer scenarios, triggers, outcomes |
| `voice-and-tone.md` | `/tone-mapping` | 3-5 real writing samples (LinkedIn posts, blog posts, emails) |
| `voice-samples.md` | `/tone-mapping` (Step 6, after the profile) | 5+ real writing samples — more samples, better calibration |
| `brand-guide.md` | `/design-extract` | Your website URL, or brand colors/fonts manually |
| `audience-language.md` | `/product-marketing` | Sales call transcripts or customer conversations |
| `customer-journey.md` | `/product-marketing` | Sales process knowledge, common objections, deal patterns |
| `market-signals.md` | `/product-marketing` | Industry trends, analyst reports, news |
| `qualifying-questions.md` | `/product-marketing` | Discovery call experience, qualification criteria |
| `tactical-assets.md` | `/product-marketing` | Company bios, speaker bios, social profiles |

Present the recommendations:

```
Recommended next steps (in order):

1. capabilities.md — Run /product-marketing and ask to build out capabilities
   Have ready: your product's features organized by messaging pillar

2. voice-and-tone.md — Run /tone-mapping with 3-5 writing samples
   Have ready: LinkedIn posts, blog posts, or emails you wrote yourself

3. use-cases.md — Run /product-marketing and ask to define use cases
   Have ready: customer scenarios and the triggers that bring them to you
```

### Step 5: Offer to start

Ask:

> Want to start filling one of these now? Pick a number, or tell me which file you'd like to work on.

If they pick one, route to the appropriate skill.

---

## Rules

- Read files as-is. Don't modify any brain files during a health check.
- Count `[FILL IN]` and `[VERIFY]` literally (case-insensitive match on `[fill in]` and `[verify]`).
- If a file has custom content mixed with some remaining placeholders, it's partial, not empty.
- Don't judge quality of filled-in content. The health check measures completeness, not correctness.
- If running at the end of `/setup`, skip Step 5 (the offer to start) since setup is wrapping up. Just show the dashboard and recommendations.
