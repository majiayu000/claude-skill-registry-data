---
name: ab-copy-writer
description: Generate A/B copy variants grounded in Eugene Schwartz's awareness and market-sophistication stages and John Caples' tested-headline discipline. Every variant declares its angle, the awareness stage it targets, and a falsifiable hypothesis, and the skill recommends which pair to test first and what delta counts as signal. Use when the user says "A/B test this", "write variants", "give me options", "test different angles", "copy variants", "ab copy", "test this headline", "multiple versions", "which version is better", or wants to test copy before publishing. For reviewing copy that already exists, see copy-review. For sample size and stopping rules, see growth-experiment. For diagnosing a page rather than its words, see page-cro. For full paid ad sets by platform, see ad-campaign-writer.
metadata:
  grounded_in:
    - "Tested Advertising Methods - Caples"
    - "Breakthrough Advertising - Schwartz"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/learnings.md
  writes:
    - output/ab-copy/
---

# ab-copy-writer

Produces testable copy variants and argues for a specific test. Most variant generators produce five versions of the same idea and leave the choice to taste. This one selects angles from the reader's awareness stage, prioritises the element with the most leverage, and states what result would prove it wrong.

## The two frameworks

### 1. Awareness and sophistication (Eugene Schwartz, *Breakthrough Advertising*, 1966)

Schwartz's argument is that copy does not have a quality score in the abstract. It has a fit with where the reader already is. Two axes:

**Awareness: how much the reader already knows.**

| Stage | The reader | Copy must |
|---|---|---|
| Unaware | Does not know they have the problem | Name the problem before selling anything |
| Problem-aware | Feels the pain, does not know solutions exist | Articulate the pain better than they can |
| Solution-aware | Knows solutions exist, not that yours does | Show the mechanism and why it is faster or surer |
| Product-aware | Knows your product, not convinced | Prove it, with specifics and social proof |
| Most aware | Ready, needs a reason to act now | State the offer and the deadline |

The common failure is writing product-aware copy for problem-aware traffic. It reads as a good ad that nobody responds to.

**Sophistication: how tired the market is of this claim.**

| Stage | Market state | What still works |
|---|---|---|
| 1 | First to market | State the claim plainly. Nothing else needed |
| 2 | Competitors making the same claim | Make the claim bigger or more specific |
| 3 | Claims no longer believed | Lead with the mechanism, how it works |
| 4 | Mechanisms competing | Make your mechanism easier, faster, or surer |
| 5 | Everything sounds the same | Stop claiming. Identify with the reader's experience |

Sophistication is why a contrarian angle is mandatory in a crowded category and wasteful in a new one. Ask for it, or infer it from `knowledge/markets/competitors.md`.

### 2. Tested headline discipline (John Caples, *Tested Advertising Methods*, 1932)

Caples ran split-run tests at BBDO to measure actual response rather than opinion, and the book is the origin of the discipline this skill supports. Three findings that change how we test:

1. **The headline carries most of the leverage.** Changing the headline moves response far more than changing body copy. So test the headline first, and never burn a test cycle on body copy while the headline is untested.
2. **Headline types are not equal.** Caples grouped them as news, self-interest or benefit, and curiosity, and found curiosity weakest **on its own**. A curiosity angle that carries no benefit is the most common way a clever variant loses.
3. **Specific beats general.** A concrete number or detail consistently outperforms the same claim stated broadly.

## Element priority (Caples)

Test in this order. Do not test element 3 while element 1 is unresolved.

| Priority | Element | Why |
|---|---|---|
| 1 | Headline, subject line, LinkedIn hook, ad headline | Highest leverage by a wide margin |
| 2 | Offer and CTA wording | Changes what is being asked, not just how |
| 3 | Opening line, sub-headline | Decides whether the headline's promise is kept |
| 4 | Body copy, length, formatting | Real but small. Test last |

If the user asks for body-copy variants while the headline has never been tested, say so and offer to test the headline first.

## The angle table

Each angle is mapped to the awareness stage where it can work, the sophistication level it suits, and its Caples type. Never use the same angle twice in one set, and never pick an angle whose stage does not match the traffic.

| Angle | Works at awareness | Suits sophistication | Caples type |
|---|---|---|---|
| **Pain-led** | Problem-aware | 1-2 | Self-interest |
| **Outcome-led** | Solution / product-aware | 1-2 | Self-interest |
| **Specificity** | Solution / product-aware | 2-3 | Self-interest + news |
| **Mechanism-led** | Solution-aware | 3-4 | News |
| **Speed-led** | Solution-aware | 2-4 | Self-interest |
| **Social proof** | Product-aware | 3-4 | News |
| **Contrarian** | Unaware / problem-aware | 4-5 | Curiosity + self-interest |
| **Curiosity gap** | Unaware / problem-aware | 4-5 | Curiosity (never alone) |
| **How-to** | Problem / solution-aware | 2-3 | Self-interest |
| **Identification** | Any, strongest at 5 | 5 | Self-interest |
| **FOMO / deadline** | Most aware | any | News |
| **Founder voice** | Any | 4-5 | Identification |

**Hard rule from Caples:** a curiosity or contrarian variant must also carry a benefit. Curiosity that pays off in nothing is the most reliable loser in the set, and it is usually the variant that reads cleverest in the document.

## Process

1. **Load context.** Read `knowledge/brand/voice.md` for tone and banned words, `knowledge/icp/personas.md` for the language this audience uses, and `knowledge/markets/positioning.md` for the claim the copy must carry. If voice is missing, continue and mark the output generic rather than stopping.

2. **Check `knowledge/learnings.md`** for past test results. If a prior test settled an angle for this ICP, say so and weight accordingly rather than re-running a decided question.

3. **Establish the two stages before writing anything.** Ask, or infer and state the inference:
   - **Awareness:** where is this traffic coming from, and what do they already know? Cold LinkedIn feed is problem-aware at best. A pricing page is product-aware. A retargeting ad is most aware.
   - **Sophistication:** how many competitors make this same claim already? Check `knowledge/markets/competitors.md`.

   Both go in the output header. A variant set without a declared stage is a set of guesses, and every hypothesis below it is unfalsifiable.

4. **Confirm the element and its priority.** If the requested element is priority 3 or 4 and priority 1 is untested, flag it once.

5. **Select angles.** Filter the table to the declared awareness stage, then prefer angles matching the sophistication level. Default 3 variants, maximum 5. If the user supplied existing copy, include one variant that keeps their angle and sharpens the execution, so there is a baseline.

6. **Write each variant:**

```
## Variant [A-E]: [angle]

**Copy:**
[complete, ready to paste]

**Angle:** [from the table]
**Awareness stage:** [stage this is written for]
**Caples type:** [news | self-interest | curiosity + benefit]
**Hypothesis:** [why this should outperform for THIS ICP, referencing the stage]
**Would be proven wrong if:** [the observation that would kill it]
**Watch:** [the one metric that reads it]
```

7. **Recommend the test.** Pair by stage, not by contrast:

```
## Recommended test

**Test:** Variant [X] vs Variant [Y]
**Why this pair:** [the one assumption they isolate]
**Element:** [name] (priority [N] of 4)
**Declared stages:** awareness [stage], sophistication [level]
**Primary metric:** [one]
**Signal threshold:** [what delta is worth acting on for this volume]
**Before launching:** run `/growth-experiment` to set sample size and the stopping rule.
```

8. **Save** to `output/ab-copy/<DD-MM-YYYY>-<element-slug>.md` with frontmatter carrying `element`, `channel`, `awareness-stage`, `sophistication-level`, `angles`, `variants`, `created`.

9. **Offer follow-ups:** run `/retro` after the test so the winning angle lands in `knowledge/learnings.md`, or `/content-writer` to build the winner out.

## Pairing logic

Testing the two most different variants is a weak default, because a loss tells you nothing about which of the several differences caused it.

1. **Isolate one variable.** Two variants at the same awareness stage with different angles test the angle. Two variants of the same angle at different stages test the stage. Pick which question is being asked and hold everything else steady.
2. **When the stage itself is uncertain**, that is the more valuable test. Run problem-aware against product-aware copy first. The answer redirects every future piece for this channel.
3. **Never test three or more simultaneously** on low volume. Two variants need enough traffic already.

## Copy length by channel

| Channel | Element | Length |
|---|---|---|
| LinkedIn | Hook (first 2 lines) | 15-25 words |
| LinkedIn | Full post | 80-220 words |
| Email | Subject line | 6-10 words |
| Email | Preview text | 8-12 words |
| Landing page | H1 | 5-10 words |
| Landing page | Sub-headline | 15-25 words |
| Google ad | Headline | 30 characters |
| Google ad | Description | 90 characters |
| LinkedIn ad | Intro text | 150 characters |
| Webinar | Title | 8-12 words |
| CTA button | Text | 2-5 words |

Verify current platform limits before shipping paid copy. These change.

## Self-check

- Awareness and sophistication are declared in the header, not implied
- Every angle is valid for the declared awareness stage
- No two variants share an angle
- Every curiosity or contrarian variant also carries a benefit
- Every hypothesis names the ICP and the stage, not "this will perform well"
- Every variant has a "would be proven wrong if" line
- The recommended pair isolates exactly one variable, and the output says which
- The element's priority is stated, and a priority 3-4 request with an untested headline was flagged
- Variants differ in approach, not in word choice
- Voice rules from `knowledge/brand/voice.md` are respected, or their absence is declared

## Rules

- **Never produce cosmetic variants.** Swapping a word is not an angle.
- **Never invent a statistic** to make a specificity variant concrete. Tag `[NEEDS INPUT: real figure]`. A fabricated number in a winning variant ships to the whole audience.
- **Never predict a percentage lift.** Give direction and confidence, and let the test produce the number.
- If `knowledge/learnings.md` shows an angle already lost for this ICP, do not silently include it. Flag it or leave it out.
- If the copy's problem is the offer rather than the words, say so and point at `/positioning-doc`. Testing headlines on a weak offer optimises the wrong thing.

## Related skills

- `/ad-campaign-writer` applies the same Schwartz stages to full paid ad sets by platform
- `/growth-experiment` sets sample size and stopping rules before the test runs
- `/copy-review` improves a single piece rather than generating alternatives
- `/page-cro` when the page underperforms for reasons beyond its words
- `/retro` records which angle won, so `knowledge/learnings.md` improves the next set
- `/brand-context` creates the voice, persona and competitor files this reads

## What this skill cannot know

- Whether the traffic actually arriving at this copy matches the awareness stage you declared
- Current platform character limits, which change without notice
- Whether a variant that won last quarter still wins, since audiences fatigue
- The sample size this test needs. Run `/growth-experiment` before launching
