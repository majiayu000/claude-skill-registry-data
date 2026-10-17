---
name: content-writer
description: Write marketing content in the user's brand voice using PAS (Problem-Agitate-Solution) and AIDA (Attention-Interest-Desire-Action) copywriting frameworks. Use when the user asks to write a LinkedIn post, blog article, email, ad copy, landing page section, social post, newsletter, or any short-to-medium form marketing content. Reads brand voice and ICP from knowledge/ so the output sounds like the company, not like generic AI. For improving copy that already exists, see copy-review. For a landing page specifically, see landing-page-writer. For a LinkedIn post, see linkedin-post. For long-form POV, see thought-leadership-writer.
metadata:
  grounded_in:
    - "Breakthrough Advertising - Eugene Schwartz"
    - "The Copywriter's Handbook - Robert Bly"
    - "Building a StoryBrand - Donald Miller"
  reads:
    - knowledge/brand/voice.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/content-library/
    - knowledge/services/
  writes:
    - output/content-writer/
---

# content-writer

Writes marketing content in the company's voice for the company's ICP. Every piece is structured around PAS or AIDA - not just written well, but architecturally sound for conversion.

## Choosing the structure: awareness first

PAS and AIDA are not interchangeable, and picking by taste is the most common failure in this
skill. Pick by where the reader already is, using **Eugene Schwartz's awareness stages from
*Breakthrough Advertising* (1966)**:

| Reader is | Structure | Why |
|---|---|---|
| Unaware or problem-aware | **PAS** | They need the problem named and sharpened before any solution lands |
| Solution-aware or product-aware | **AIDA** | They accept the problem; the work is attention, interest and desire for this answer |
| Most aware | Neither, go straight to the offer | Structure is overhead when they are ready |

### Schwartz's second axis: market sophistication

Awareness is about the reader. Sophistication is about the market, specifically how many times
this reader has already heard a claim like yours. Schwartz's five stages, each with the move that
still works at that stage:

| Stage | State of the market | The move that works | The move that is already dead |
|---|---|---|---|
| 1 | You are first with this claim | State the claim plainly and bluntly | Nothing yet, plain wins |
| 2 | Competitors are making the same claim | Enlarge the claim, be bigger and more specific than them | The plain claim, it is now background noise |
| 3 | Nobody believes the claim any more | Lead with the **mechanism**, how it actually works | Any promise, of any size |
| 4 | Competitors have copied the mechanism | Elaborate the mechanism, make yours more precise and more provable | The bare mechanism |
| 5 | The reader disbelieves the whole category | Lead with **identification**, who this is for and who they become | Claims and mechanisms both |

**Decision rule:** ask the user how many direct competitors say roughly the same sentence in
their hero copy. Zero to one is stage 1-2, so write the promise. Three or more is stage 3-4, so
open with the mechanism. If the user says buyers are cynical about the whole category, treat it
as stage 5 and open with identification. If you do not know, ask before drafting, do not guess.

### Bly's craft layer

**Robert Bly's *The Copywriter's Handbook*** supplies the section-level craft. Two of his models
are used directly here.

**The 4 U's, applied to every headline and every subject line.** Score each on a 1-4 scale:

| U | Question | Fails when |
|---|---|---|
| Urgent | Is there a reason to read this now? | Timeless and therefore skippable |
| Unique | Has the reader seen this exact sentence before? | It could sit on a competitor's page unchanged |
| Ultra-specific | Are there numbers, names, and a concrete situation? | "Improve your results" |
| Useful | Is there a clear benefit to the reader, not to the brand? | The benefit is that the brand launched something |

**Threshold: a headline must score 3 or 4 on at least three of the four U's. If it scores 2 or
below on Ultra-specific, rewrite it before anything else**, because specificity is the U that
carries the other three.

**Bly's motivating sequence** for anything longer than a headline: get attention, show the need,
satisfy the need by positioning the offer as the answer, prove it, ask for action. If a draft has
no proof step, it is a claim with a button on the end.

Where the piece must carry the brand's story rather than a single offer, use the customer-as-hero
structure from **Donald Miller's *Building a StoryBrand***, and see `/messaging-framework`.

## Frameworks

### PAS - Problem, Agitate, Solution (Dan Kennedy)

**PROBLEM**: Open by naming the exact problem the reader has. Specific, not vague. "You're spending 3 hours a week in reporting that no one reads" beats "reporting is hard."

**AGITATE**: Twist the knife. Make the problem feel real, costly, and urgent.
- What does it cost them? (time, money, credibility)
- What does it feel like to live with this problem?
- What happens if it stays unsolved for another year?

The agitation section must actually hurt. If it reads mild, it's not working.

**SOLUTION**: Introduce the solution after the pain has been established. Not before. The solution lands harder because the reader now knows why they need it.

Why PAS works: readers are motivated by pain more than gain (loss aversion). Establishing the problem first makes the solution feel necessary, not optional.

### AIDA - Attention, Interest, Desire, Action (Elias St. Elmo Lewis)

**ATTENTION**: Stop the scroll. The first line or headline must interrupt pattern. It cannot be a warm-up.

**INTEREST**: Build interest by connecting to what they care about. Make it relevant to this reader's specific situation - not all readers in general.

**DESIRE**: Create want. Show the outcome, the transformation, the result. Not the feature - the life after using it.

**ACTION**: Tell them exactly what to do next. One action, specific, low-friction. "Book a 20-min call" beats "get in touch."

### When to use each

| Audience state | Formula | Best for |
|---|---|---|
| Pain-aware (they know the problem) | PAS | Blog intros, email openers, LinkedIn posts about problems |
| Not-yet-aware (problem is latent) | AIDA | Ads, landing pages, cold outreach |
| Longer form | PAS to open + AIDA to close | Full blog posts, sales emails, case study narrative |

**Check before writing**: Is the audience pain-aware or not? This determines the formula.

Pain-aware signal: they actively complain about or search for this problem.
Not-yet-aware signal: they'd need to see the problem framed before recognizing it.

## When to use

- "Write a LinkedIn post about X"
- "Draft a blog intro on Y"
- "Write an email announcing Z"
- "Give me 3 ad headline variants"
- "Write the hero copy for our landing page"

## Inputs needed

- **Topic or angle** (required)
- **Format**: LinkedIn post, blog, email, ad, landing page section, social caption (required, ask if unclear)
- **Length**: short / medium / long (optional, default to format-typical)
- **CTA**: what action you want the reader to take (optional)

## Process

1. **Load context**:
   - Read `knowledge/brand/voice.md`. If missing, stop and say: "I need your brand voice. Run `/brand-context` or paste 3+ past pieces into `uploads/` and rerun."
   - Read `knowledge/icp/personas.md`. If missing, ask the user to describe the audience in one line.
   - Read `knowledge/markets/positioning.md` if the topic relates to product or service.
   - Skim `knowledge/content-library/` for 2-3 past pieces on similar topics. Mirror their structure.

2. **Determine audience awareness and select formula**, then state both axes explicitly before
   drafting:

   ```
   Schwartz awareness stage: <unaware | problem-aware | solution-aware | product-aware | most-aware>
   Schwartz sophistication stage: <1-5, and the evidence for it>
   Structure selected: <PAS | AIDA | offer-only>
   Opening move: <promise | enlarged promise | mechanism | elaborated mechanism | identification>
   ```

   Is the audience pain-aware?
   - Yes: use PAS. Open with the problem, agitate, then solve.
   - No: use AIDA. Open with attention, build interest, create desire, drive action.
   - Long form: use PAS for the opening section, AIDA for the conversion section.

   Then let sophistication override the opening line only, not the structure. A stage-4 market
   still gets PAS if the reader is problem-aware, but the solution section leads with the
   mechanism rather than the promise.

3. **Clarify if needed.** One question max. Examples: "Long-form blog or short LinkedIn?" "Aimed at CMOs or content marketers?"

4. **Draft. Apply the formula structurally:**

   ### PAS structure (pain-aware)
   ```
   PROBLEM (10-20% of piece):
   <Name the exact problem. Specific. Use numbers or a scenario.>
   Example: "You wrote the brief. Briefed the agency. Reviewed 3 rounds. The campaign launched.
   And the SQL number didn't move."

   AGITATE (20-30% of piece):
   <Make it real. What does this cost them? What does it feel like? What is the trajectory if nothing changes?>
   Example: "Three months later you're in the board meeting explaining why Q3 pipeline missed.
   The campaign was 'awareness.' The numbers say 'waste.'"

   SOLUTION (50-70% of piece):
   <Introduce the solution now. It lands harder because the reader already feels the pain.>
   ```

   ### AIDA structure (not-yet-aware or conversion-focused)
   ```
   ATTENTION (first line / headline):
   <Interrupt. Specific claim, question, or surprising fact. Not a warm-up.>

   INTEREST (20-30% of piece):
   <Connect to what they care about. Make it relevant to their specific situation.>

   DESIRE (40-50% of piece):
   <Show the outcome. The life after. Specific results, not features.>

   ACTION (closing):
   <One action. Specific. Low-friction. Time-bound if possible.>
   ```

5. **Voice rules**:
   - Match `knowledge/brand/voice.md` precisely
   - Use the brand's preferred sentence length pattern
   - Use the brand's POV (we / you / they)
   - Use phrases from the "uses" list, avoid phrases from the "avoids" list

6. **Self-check before showing.** Every item below is answerable by pointing at a line in the
   draft. If an item cannot be answered by quoting the draft, it does not belong in this list.

   Framework checks:
   - The awareness stage and sophistication stage are both written down in the output frontmatter
   - PAS: the agitation names at least one countable cost (hours, currency, a missed number, a
     named consequence). A cost with no unit fails this check
   - PAS: the first mention of the product or offer appears after the agitation block, not before
   - AIDA: the first sentence contains no greeting, no "excited to", and no restatement of the topic
   - AIDA: exactly one imperative CTA sentence exists in the piece. Count them
   - The opening move matches the sophistication stage recorded in step 2
   - Headline scores 3 or more on at least three of Bly's 4 U's, and 3 or more on Ultra-specific

   Sourcing checks:
   - Every number, percentage, currency figure, customer name and quote appears in
     `knowledge/` or in the user's brief. List each one and where it came from
   - Every unsourced claim reads `[SOURCE NEEDED: <what>]` or `[NEEDS INPUT: <what>]` in the draft

   Quality checks:
   - Zero em dashes and zero en dashes in the file
   - Zero emojis unless the user asked for them
   - Zero occurrences of: "In today's fast-paced world", "leverage", "unlock", "game-changer",
     "in conclusion", "seamless", "robust"
   - Every phrase in the brand's "avoids" list appears zero times

7. **Save**: write to `output/content-writer/<DD-MM-YYYY>-<format>-<slug>.md` with frontmatter:
   ```yaml
   ---
   format: linkedin-post
   topic: <topic>
   audience: <persona>
   formula: <PAS|AIDA|PAS+AIDA>
   audience-awareness: <pain-aware|not-yet-aware>
   created: DD-MM-YYYY
   ---
   ```

8. **Show the user** the draft inline, then point them to the file. Offer 2 alternative angles if they want variants.

## Format-specific defaults

| Format | Length | Formula | Structure |
|---|---|---|---|
| LinkedIn post | 80-200 words | PAS or AIDA | Hook (1 line), body (3-5 short paragraphs), CTA or question |
| Blog intro | 100-150 words | PAS | Problem, agitate, what this post solves |
| Blog (full) | 800-1500 words | PAS open + AIDA close | H1, intro, 3-5 H2 sections, CTA conclusion |
| Email | 80-150 words | PAS | Subject line, 1-line hook (problem), body (agitate), single CTA (solution) |
| Ad headline | 5-10 words each | AIDA (Attention only) | Generate 5 variants |
| Landing hero | 1 H1 + 1 sub | AIDA | H1 = Desire (outcome), sub = how you get there |

## Rules

- Match `knowledge/brand/voice.md` exactly. If the brand uses contractions, use them. If not, don't.
- **Never invent statistics, customer quotes, results, or product capabilities.** If a number
  would strengthen the piece and you do not have one, write `[SOURCE NEEDED: <what>]` and tell the
  user. Product claims come only from `knowledge/services/`, which step 1 loads.
- "Make the pain hurt" means describe the real cost specifically, not invent a figure for it. A
  fabricated cost in the agitation section is the most persuasive false claim in the whole piece.
- If the user's request conflicts with brand voice (e.g. they ask for emojis but the brand avoids them), flag it and ask.
- The formula is structural, not cosmetic. Don't write good content in the wrong order.
- PAS agitation that is mild is worse than no PAS. Make the pain real or skip to AIDA.

## Stop conditions

Do not produce a draft when any of these is true. Say which one, and what you need.

1. **No brand voice file and no sample pieces.** Stop. The output will be generic and the user
   will rewrite all of it. Ask for `/brand-context` or three past pieces.
2. **The user asks for a number the knowledge base does not contain.** Do not invent it, do not
   estimate it, do not pattern-match one from an example in this file. Write
   `[NEEDS INPUT: <the exact figure needed>]` and name it in your reply.
3. **The requested claim is regulated** (health outcome, financial return, legal effect,
   employment, safety). Draft it, mark it `[LEGAL REVIEW]`, and say it must not ship unreviewed.
4. **The user names two CTAs.** One piece, one action. Ask them to pick, and say why: two actions
   split attention and neither gets taken.
5. **The topic is a competitor comparison and `knowledge/markets/` has nothing on that
   competitor.** Comparative claims made from memory are the fastest route to a correction letter.

## Warning signs in your own draft

Ranked worst first. The first two are ship-blockers, the rest are rewrite prompts.

1. A specific figure you cannot point at a source for. Blocker.
2. A named customer, quote, logo or result the user did not supply. Blocker.
3. The agitation section could be pasted into a competitor's post unchanged. The problem is not
   specific enough to be worth solving.
4. The hook restates the topic rather than opening a gap. Rewrite the first line only.
5. More than one CTA, or a CTA with no verb ("more info").
6. Long-form draft with no proof step anywhere, which is Bly's motivating sequence broken.

## Related skills

- `/copy-review` for grading and fixing copy that already exists rather than writing new copy
- `/landing-page-writer` for a full page, where SB7 replaces PAS and AIDA as the spine
- `/linkedin-post` for a post that needs a named hook formula and platform-specific length rules
- `/thought-leadership-writer` when the piece needs to defend a contestable thesis at 1200 words or more
- `/newsletter-writer` when the piece is one issue of a recurring publication with a fixed spine
- `/ad-campaign-writer` when the output is paid ad variants rather than owned content
- `/brand-context` first, whenever `knowledge/brand/voice.md` does not exist yet
- `/messaging-framework` when the same words need to hold across every asset, not just this one
- `/content-repurposer` after this piece ships, to turn it into other formats

## What this skill cannot know

These are real limitations of this skill. It cannot resolve them from the knowledge base, so ask
the user or emit `[NEEDS INPUT: <what>]` rather than filling the gap.

1. **Whether a figure in `knowledge/` is still current.** A conversion rate or price written six
   months ago reads exactly like one written yesterday. Ask when the number was last confirmed
   before putting it in public copy.
2. **Whether a named customer has agreed to be named.** Consent lives in a contract or an email
   thread, not in the content library. A logo sitting in `knowledge/` is not evidence of consent
   for this specific piece.
3. **How sophisticated the market actually is.** Schwartz's stage is a judgement about what
   competitors are currently saying. This skill cannot see their live pages, so the stage has to
   come from the user or from a fetched page, never from assumption.
4. **Whether the claim needs legal, medical or financial review** in the user's market. Rules
   differ by jurisdiction and by channel. Flag it, do not adjudicate it.
