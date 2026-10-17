---
name: brand-namer
description: >-
  Generate, score, and shortlist brand names through a guided interview. Use when the
  user says "name my brand", "help me name", "come up with a name", "naming ideas",
  "what should I call this", "brand name", "product name", "company name", "rename",
  "rebrand", or is stuck choosing between names. Self-contained and brand-agnostic: it
  does not read knowledge/, so it works for naming a brand-new venture, product,
  service, feature, or rebrand from scratch, before any brand context exists. Runs on
  Alexandra Watkins' SMILE and SCRATCH tests to generate and filter, Marty Neumeier's
  7 criteria to score, and the Lexicon Branding method for sound symbolism and
  strategy. Asks the user questions before generating. For the positioning the name
  has to carry, see positioning-doc. For the message architecture built on top of it,
  see messaging-framework.
metadata:
  grounded_in:
    - "Hello, My Name Is Awesome - Alexandra Watkins"
    - "The Brand Gap / Zag - Marty Neumeier"
    - "The Lexicon Branding method - David Placek"
  reads: []
  writes:
    - output/brand-namer/
---

# brand-namer

Turn a brand brief into a ranked, scored shortlist of names plus one recommended pick. Self-contained: every input comes from the interview, nothing from `knowledge/`.

## When to use

- "Help me name my company / product / service / app / feature"
- "I need naming ideas for X"
- "What should I call this?"
- "I'm rebranding, give me name options"
- "I'm stuck choosing between these names" (jump to scoring)

## The frameworks this skill runs on

These are the load-bearing ideas. Apply them, don't just cite them.

**SMILE - what makes a name great** (Alexandra Watkins, *Hello, My Name Is Awesome*). Aim every candidate at these:
- **S**uggestive - evokes something about the brand experience, not literal description
- **M**emorable - sticks after one exposure
- **I**magery - triggers a mental picture (aids recall)
- **L**egs - stretches into a theme, tagline, and story
- **E**motional - makes people feel something

**SCRATCH - instant rejects** (same book). Kill any candidate that trips one of these:
- **S**pelling-challenged - looks like a typo
- **C**opycat - echoes a competitor's name
- **R**estrictive - boxes the brand in (geography, one product) and blocks growth
- **A**nnoying - tries too hard, feels gimmicky
- **T**ame - flat, literal, forgettable
- **C**urse of knowledge - only makes sense to insiders
- **H**ard to pronounce or spell out loud

**Neumeier's 7 criteria - the scoring rubric** (Marty Neumeier, *The Brand Gap* / *Zag*). Score each shortlisted name 1-5 on each:
- Distinctiveness, Brevity, Appropriateness, Easy spelling/pronunciation, Likability, Extendability, Protectability (can it be owned/trademarked/domained)

**The Lexicon method - sound and strategy** (David Placek, Lexicon Branding). The deepest layer. Where SMILE shapes intent and Neumeier scores, Lexicon engineers the actual *sound* of a name and its strategic job. Its core ideas: sound symbolism (letters carry meaning independent of definition), "don't describe, evoke", "relevant but unexpected", invent when the category is crowded, and distinctiveness requires discomfort. **Before you generate (Step 3) and before you score (Step 5), read `references/lexicon-method.md`** - it holds the sound-symbolism table, the strategy questions, the generation tricks, the competitor test, and six case principles. Do not name from memory of Lexicon; use the reference.

## Step 1: Let the user pick the flow

Before asking anything else, present both flows and let the user choose:

> **Flow A - Structured (recommended if you want it fast and predictable):** I ask 7 set questions, then generate.
> **Flow B - Adaptive:** I ask 3 core questions, then follow up based on your answers. More tailored, less predictable.
>
> Which flow do you want, A or B?

Wait for the choice. Ask one question at a time in both flows - do not dump the whole list at once. Naming answers are short; a wall of questions makes people give lazy input, and lazy input makes weak names.

## Step 2: Interview

### Flow A - the 7 questions (ask in order, one per message)

1. **What does the brand do?** One or two sentences, plain language.
2. **Who is it for?** The customer or audience.
3. **Personality - give me 3 adjectives.** (e.g. bold, warm, precise)
4. **What feeling should the name evoke** when someone hears it?
5. **Names you love** (in any industry) and why. This reveals taste faster than any abstract question.
6. **Names you hate or want to avoid,** and any competitor names to steer clear of.
7. **Preferred style:** descriptive (says what it does), suggestive/evocative (hints at a feeling), invented/coined (made-up word), or abstract (unrelated word)? "No preference" is a valid answer.

### Flow B - adaptive

Start with the 3 core questions: **what it does**, **who it's for**, and **the feeling to evoke**. Then branch:
- If they gave a strong style signal, probe that style ("you said 'like Stripe' - do you want a real word repurposed, or something invented?").
- If personality is vague, ask for 3 adjectives.
- If they named competitors, ask what to avoid.
Stop interviewing once you can clearly picture the target. Don't over-interview - 5-6 questions total is plenty.

## Step 3: Generate ~25-30 candidates

**Read `references/lexicon-method.md` first.** Then, before generating, name the single feeling or expectation the name must plant (Lexicon's "what do we need to say?"). Everything below serves that one idea.

Generate across all 5 name types so the user sees a real range, not 30 variations of one idea. Label each group.

1. **Real-word** - existing words repurposed (Apple, Dove, Slack)
2. **Compound / blend** - two words fused (Facebook, Snapchat, Netflix)
3. **Invented / coined** - built from sound and morphemes (Kodak, Verizon, Spotify)
4. **Metaphor / evocative** - borrows meaning from something else (Nike, Amazon, Oracle)
5. **Altered spelling** - a real word twisted (Lyft, Flickr, Tumblr) - use sparingly, it flirts with SCRATCH's spelling trap

Push every candidate toward SMILE, and engineer its **sound** to match the feeling (see the sound-symbolism table in the reference): plosives and front vowels for fast/sharp brands, sonorants and fuller vowels for calm/premium brands. Suggestive and imagery-rich beats literal, and evoke rather than describe - a merely descriptive name is Tame.

Two Lexicon generation moves to apply:
- **Don't self-censor early.** Push past the first 10 obvious names. The surprise winner hides after you have exhausted the obvious, so generate wide before you judge.
- **Use the unrelated-category trick.** Generate a few names as if the brand were in a totally different category, then see which cross over. It breaks the pull of what every competitor already sounds like.

If the user picked a style, weight that type heavier but still show a few from each group - the surprise winner often comes from a type they didn't ask for.

## Step 4: Apply the SCRATCH filter

Run all candidates through SCRATCH. Cut the failures, but show the cut briefly so the user trusts the process:

> **Filtered out:** *Namey* (Tame), *Qzynx* (Hard to pronounce, Spelling-challenged), *EuroWidgetCo* (Restrictive)

Keep this to one or two lines. The point is transparency, not a lecture.

## Step 5: Score and rank the survivors

Take the strongest survivors and score each on Neumeier's 7 criteria (1-5 each, 35 max). Rank by total, but use judgment - a name that scores 33 but is unpronounceable is worse than a 30 that sings. Note that Protectability is a directional guess, not a legal opinion.

Then apply two Lexicon lenses before you finalize the ranking (details in the reference):
- **Sound check.** For each finalist, does its sound actually match the desired feeling? Note it. A calming brand with harsh plosives, or a fast brand with heavy back vowels, is fighting itself.
- **The competitor test and the discomfort signal.** Judge each name by "if a competitor launched with this, what's my reaction?" - fear or envy means power, a shrug means Tame. And if a candidate makes you slightly uneasy but you cannot fault it on SCRATCH or strategy, that discomfort is often a sign of strength, not weakness. Do not let comfort alone crown a safe, forgettable winner.

## Step 6: Output

Write the full run to `output/brand-namer/<DD-MM-YYYY>-<slug>.md` and present the shortlist in chat. Use this structure:

```markdown
# Brand names for <what the brand does> - <DD-MM-YYYY>

## Brief (from your answers)
- Does: ...
- For: ...
- Personality: ...
- Feeling: ...
- Style preference: ...

## Shortlist (ranked)

### 1. <Name>  (score: 32/35)
- **Why it works:** one or two sentences
- **SMILE angle:** which SMILE levers it pulls
- **Sound:** the sound-symbolism read - which sounds it uses and why they fit the feeling
- **Say it out loud:** pronunciation note + a one-line tagline showing its "legs"
- **Score:** Distinctiveness 5 / Brevity 4 / Appropriateness 5 / Spelling 4 / Likability 5 / Extendability 5 / Protectability 4

### 2. <Name> (score: .../35)
...

(6-8 names total)

## My pick: <Name>
One clear paragraph on why this is the one. You can overrule me - the score is a guide, not a verdict.

## Full candidate list
All ~25-30 generated names, grouped by type, so you can mine for more.

## Next steps (do these before you commit)
- [ ] Domain check: search the .com and your target TLDs
- [ ] Trademark search: USPTO (or your local registry) for conflicts in your class
- [ ] Social handles: check the name is free on the platforms you'll use
- [ ] Cross-language screening: check the name carries no awkward, rude, or comic meaning in the languages of your market (for an Indian brand, Hindi plus the local regional language)
- [ ] Say it in a sentence, out loud, to someone who's never heard it
```

Run the cross-language screening yourself as far as you can, and flag any collision you already spot. Lexicon kills ~90% of candidates at linguistic and legal screening - a great-sounding name that means something absurd in the buyer's language is a dead name.

## Anti-patterns

1. **Generating before interviewing.** A name produced from a one-line prompt is a guess. Every candidate here has to trace back to the feeling named in Step 3, and that feeling comes from the user's answers, not from the category.
2. **Thirty variations of one idea.** If the list is all compounds, or all `-ify` coinages, the range is fake. Generate across all five name types even when the user has stated a preference.
3. **Describing instead of evoking.** A name that spells out what the product does scores Tame on SCRATCH and cannot be owned. It is the single most common weak output of this skill.
4. **Claiming a name is available.** You cannot confirm a domain, a handle, or a trademark. Present availability as the user's checklist, never as a completed check, and never write "the .com is free".
5. **Crowning the comfortable name.** The candidate everyone likes on first hearing is often the one nobody remembers on the second. A name is only disqualified by a real SCRATCH failure or a strategy miss, not by discomfort.
6. **Skipping `references/lexicon-method.md`.** Naming the sounds from memory produces generic sound-symbolism claims. Read the reference before Step 3 and again before Step 5.
7. **Hiding the cuts.** Showing one line of what SCRATCH removed, and why, is what makes the shortlist trustworthy. A shortlist with no visible filter reads as an arbitrary list.
8. **Skipping cross-language screening.** Roughly 90% of candidates die at linguistic and legal screening. A name that is comic or rude in the buyer's language is dead, however well it scores.

## Quality checklist

Before presenting the shortlist, confirm every line:

1. The single feeling the name must plant is written down, and every shortlisted name serves it.
2. `references/lexicon-method.md` was read before generating and before scoring.
3. Candidates span all five name types, each group labelled.
4. Every candidate ran through SCRATCH, and the cuts are shown in one or two lines with the reason.
5. Each shortlisted name carries all 7 Neumeier scores, not a bare total.
6. Each shortlisted name has a sound read that says which sounds it uses and why they match the feeling.
7. Each shortlisted name is shown doing its job: said out loud, in a tagline, or on a sign.
8. Cross-language screening is run as far as you can, and any collision you spotted is flagged.
9. Availability is presented as an unchecked user checklist, with no claim about what is free.
10. There is exactly one recommended pick, with the reasoning stated, and the decision handed back to the user.
11. The full candidate list is in the output file so the user can mine it later.
12. Dates and filenames use DD-MM-YYYY. No em dashes, no emojis.

## What this skill cannot know

Write these into the output as open items rather than letting the reader assume they were handled.

1. **Whether the name is legally available.** Trademark conflicts turn on class, jurisdiction and existing marks. Nothing here searches a registry, and Protectability in the score is a directional guess, not a legal opinion.
2. **Whether the domain or the handles are free.** These change daily and cannot be checked from here.
3. **How the name lands in every language of the market.** You can screen the obvious languages; you cannot replicate the linguist network that kills most candidates in professional naming.
4. **Whether the audience will react as predicted.** Sound symbolism is a directional heuristic that is category-dependent, not a law. The real test is saying the name to someone who has never heard it.
5. **Whether the strategy behind the brief is right.** The name will faithfully carry whatever positioning the user described. If that positioning is wrong, a great name makes the wrong promise louder.

## Context and output

**Before you start.** Nothing to load from `knowledge/`. This skill is deliberately self-contained, because naming usually happens before a brand has any context written down. Everything comes from the interview.

**When you finish.** Save to `output/brand-namer/<DD-MM-YYYY>-<slug>.md` using the structure in Step 6, then present the shortlist in chat. The output file carries the brief, the ranked shortlist, the pick, the full candidate list, and the pre-commit checklist.

## Related skills

- `/positioning-doc` for the positioning the name has to carry, and the place to go first if the brief in Step 2 keeps coming back vague
- `/messaging-framework` for the message hierarchy and brand script built on top of the chosen name
- `/brand-context` for writing the chosen name and its story into the shared `knowledge/` files every other marketing skill reads
- `/competitor-analyst` for the competitor set to steer clear of in Step 2, question 6
- `/press-release-writer` for announcing the name once it is chosen and cleared
