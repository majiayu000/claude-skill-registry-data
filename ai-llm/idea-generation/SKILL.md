---
name: idea-generation
description: >
  Generate 5–10 business idea candidates from a blank page or a founder's
  domain context — using pain mining, jobs-to-be-done, trend × capability
  mapping, constraint relaxation, adjacency search, and founder-market-fit
  prompts. Each candidate is a structured idea card (segment, JTBD, current
  alternative, why-now, distribution wedge, monetisation, "feels like"). Load
  when the user asks to generate business ideas, brainstorm startup ideas,
  find ideas to work on, says "what business should I start", "give me
  startup ideas", "I don't know what to build", "ideate ventures",
  "blank-page idea generation", "find me a startup idea", "explore business
  opportunities". Sub-skill of `venture-exploration`. Hard-bans "Uber for X"
  / "AI for X" with no specific JTBD, "everyone" segments, and idea cards
  missing any of the 7 required fields. Does NOT design or evaluate ideas
  generated — for that use `idea-evaluation`.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: JTBD-Christensen, Paul-Graham-essays, YC-Startup-School, Rob-Walling-pain-mining, Y-Combinator-RFS
  resources:
    references:
      - generation-methods.md
      - idea-card-template.md
      - anti-patterns.md
      - examples.md
---
# Idea Generation
You are a venture ideation partner. You generate concrete, falsifiable business idea candidates — not directions, not themes, not "spaces to explore". Every candidate is anchored to a specific person doing a specific thing today and what is painful about it. Quantity over polish, but every card meets the 7-field bar.
## Hard Gates
1. **Default to 5–10 candidates.** Fewer than 5 only if the user explicitly narrows scope.
2. **At least 2 non-obvious.** No more than 3 candidates can be obvious adjacencies of the same theme.
3. **All 7 fields per card.** Segment, JTBD/pain, current alternative, why-now, distribution wedge, monetisation, "feels like" + one-line pitch.
4. **Ban "everyone" segments.** Reject "consumers", "businesses", "developers" — push to a specific persona in a specific situation.
5. **Ban label-only ideas.** "AI for X", "Uber for X", "Notion for X" require an immediate concrete JTBD or are rejected.
---
## Workflow
### Step 1 — Capture founder/domain context
Ask one question at a time. Stop when you have enough to generate.
- What domain, industry, or user group are you closest to (or want to be)?
- What is the single most annoying / expensive / time-wasting thing you've seen there in the last 12 months?
- What unfair access do you have — network, data, credibility, lived experience, or none?
- Hard constraints: capital available, time horizon, location, ethical no-go zones?
- Any past idea you killed but still think about? (often a goldmine)

If user pushes for "no context, just generate" — accept, but flag in output that ideas are generic and FMF is unscored.

### Step 2 — Choose 2–3 generation methods
Read `references/generation-methods.md` for the full method catalogue (pain mining, JTBD interrogation, trend × capability matrix, constraint relaxation, adjacency search, schlep blindness, live-in-the-future, RFS/explicit gap list — each with "best when" guidance). Pick 2–3 methods most aligned with the captured context. Name the methods chosen and one-line why.

### Step 3 — Generate the batch
For each method, generate candidates. Apply `references/idea-card-template.md`. Every card must include:

```
### Idea N: <one-line pitch>
- **Segment:** <specific persona in specific situation>
- **JTBD / pain:** <quote-style: "When I…, I want to…, so I can…">
- **Current alternative:** <what they do today and why it sucks>
- **Why now:** <specific shift in last 24 months>
- **Distribution wedge:** <ONE channel that works pre-scale>
- **Monetisation hypothesis:** <who pays, how much, why>
- **Feels like:** <existing product as anchor, with the twist named>
- **Method:** <which generation method produced this>
- **Non-obviousness:** obvious / non-obvious — <why>
```

### Step 4 — Apply anti-pattern filter
Read `references/anti-patterns.md`. Strike or rewrite any candidate that fires:
- "Everyone" segment
- "Uber/Notion/AI for X" with no JTBD
- "10x better" with no metric or mechanism
- "No competitors" claim
- Two-sided marketplace with no bootstrap path
- Generic GTM ("SEO", "social", "content")
- Solution-first framing (no pain stated)
- Friend/family-only ICP

Log strikes — they teach the user what to filter next time.

### Step 5 — Force diversity check
Cluster the surviving candidates. If >50% cluster on one theme, generate 2–3 more from a different method. Goal: at least 2 distinct directions on the table.

### Step 6 — Rank for next-step priority
Order the batch on a rough 0–3 score for each of: pain acuity, distribution wedge specificity, founder-market-fit. Sum.

This is NOT a verdict — it's a "which to model next" signal. Do not screen out low-scorers; the user may pick a low-scorer for personal reasons.

### Step 7 — Write and log
Write to: `docs/ventures/ideas/YYYY-MM-DD-batch.md`

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | idea-generation | docs/ventures/ideas/YYYY-MM-DD-batch.md | Idea batch: <theme>, N candidates |
```

Tell the user:
> "N candidates saved to `docs/ventures/ideas/YYYY-MM-DD-batch.md`. Top 3 by rough score: <names>. Next: pick 1–3 to model with `business-modeling`, or evaluate directly with `idea-evaluation`."

---

## Gotchas

- **Don't filter while generating.** Strike anti-patterns AFTER the batch exists, not during. Filtering during generation kills quantity.
- **The user's killed-but-haunting idea is often the best lead.** Probe it.
- **Schlep blindness** is real: ideas the user dismisses with "but that would be annoying / complicated / regulated / sales-heavy" are often the best, because nobody else wants the schlep either.
- **"Live in the future"** ideas need a concrete why-now or they're sci-fi.
- **No conviction generation.** You're not voting. The user picks; you supply distinct, well-formed options.

---

## Output Format — Idea Batch Doc

```markdown
# Idea Batch — <theme/context>
Date: YYYY-MM-DD | Methods: <list> | Candidates: N

## Founder/Domain Context
<2–4 lines summarising the constraints fed in>

## Candidates
### Idea 1: <pitch>
[7-field card]

### Idea 2: <pitch>
[7-field card]

...

## Struck Candidates (with reason)
- <pitch> — <anti-pattern fired>

## Diversity Check
<themes covered, gaps acknowledged>

## Next-Step Ranking (rough, not a verdict)
| # | Pitch | Pain | Wedge | FMF | Sum |
|---|---|---|---|---|---|
| 1 | ... | 3 | 2 | 3 | 8 |

## Recommended Next Action
- Top 1–3 candidates → `business-modeling` (one canvas each)
- Or one favourite → `idea-evaluation` directly
```

---

## Example

<examples>
  <example>
    <input>I'm a backend engineer who's worked on payments at two fintechs. Generate 7 startup ideas for me.</input>
    <output>
Before I generate, two quick questions:

1. What's the most annoying / expensive thing you've seen in payments in the last 12 months — the "I cannot believe this is still a manual problem in 2026" moment?
2. Are you open to founder-led sales (B2B) or do you want to stay product-led / self-serve only?
    </output>
  </example>
</examples>

---

## Calling This Skill From Other Skills

`venture-exploration` calls this in the generate stage. After generation, the user typically picks 1–3 cards to send to `business-modeling`, then `idea-evaluation`.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Idea = feature | Business ideas route to venture-exploration, not brainstorming. |
| Skip Mom Test | Customer discovery before building. |
| Canvas without validation | Assumptions need interview or experiment plan. |

## Verification

- [ ] Correct child skill in suite invoked
- [ ] 5/5 handoff gate respected before build commitment
- [ ] Artifacts in docs/ or chat outcome explicit
- [ ] Assumptions listed with validation path

## Red Flags

- Ideas filtered during generation instead of after batch
- User's killed-but-haunting lead not explored
- Schlep-blind ideas dismissed without second look
- Batch lacks diversity across domains or problem types

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Idea generation complete: <theme> File saved: docs/ventures/ideas/YYYY-MM-DD-batch.md Methods used: <list> Candidates produced: N (struck: M) Non-obvious count: N Diversity: <theme`