---
name: regen-landing-copy
description: >
  Build conversion-focused landing page copy and structure for ReGen Civics:
  hero blocks, value-prop ladders, social proof placements, FAQ blocks, CTA
  patterns, and A/B variant generation. Distinct from regen-fundraising-copy
  by focusing on page architecture and conversion flow rather than persuasive
  narrative. Triggers on: "landing page", "hero block", "above the fold",
  "value prop", "value proposition", "page structure", "CTA copy", "call to
  action", "above-the-fold", "A/B test variants", "conversion copy", "headline
  options", "subheadline", "page architecture", or any request to design or
  rewrite the structure of a marketing page.
---

# ReGen Civics Landing Copy

## What this skill does

Build the structural skeleton of any landing page on ReGen Civics, plus
the copy that goes in each block. Cover the seven canonical sections,
the three audience versions of each section, and the A/B variant patterns
we use to test claims.

If the request is "write the narrative" (one-pager, pitch deck, donor
email), use `regen-fundraising-copy` instead. This skill is for the
architectural layer: what blocks, in what order, with what copy, with
what CTAs.

## The seven canonical sections

Every ReGen Civics landing page follows this skeleton. Skip a section
only with reason; don't reorder.

1. **Hero.** Headline + subheadline + primary CTA + supporting visual
2. **Proof of why-now.** A specific, current piece of context that
   anchors the page in real time
3. **The promise (value-prop ladder).** What you get / what you
   become / what changes in the world
4. **The mechanism.** How it works in plain language. 3-5 steps max
5. **Social proof.** Real names, real quotes, real numbers
6. **The ask (CTA section).** One primary action, one secondary
7. **FAQ.** 5-9 honest questions answered honestly

Optional eighth: **The honest tension.** A "things to know before you
say yes" section that names what's hard. Builds trust.

## Section 1: Hero

The hero is one job: make the right person say "wait, this is for me"
in under 5 seconds.

### Headline patterns that work for us

- **Inviting + concrete.** "Help land projects regenerate their bioregions
  through real participation, real tools, and real games."
- **Tools-and-game framing.** "Tools and an in-real-life game for the
  Regenerative Renaissance."
- **Direct address.** "You can play a part in healing the earth. Here's
  one way to start."
- **Stakes-naming.** "Building the financial and governance systems land
  projects need to thrive."

### Headline patterns that don't work

- "Reimagining [X]." (Vague, AI tell.)
- "The future of regen is here." (Empty, vibes-based.)
- "We're building the world's most [adjective] [thing]." (Performance
  marketing voice, doesn't match the site.)
- "Join us in our journey." (Banned by project Writing Rules.)
- Anything with an em-dash. (Banned project-wide.)

### Subheadline rules

The subheadline does the work the headline can't. Make it concrete and
load-bearing:

- Names the audience directly ("for land stewards, contributors, and
  movement builders")
- Names the next action ("apply for the next incubator season" or "join
  the Welcome Aboard Quests")
- Names the proof anchor ("13 stewardship roles. One network. Many games.")

### Hero CTA

One primary CTA, full button. One secondary, text link or ghost button.

Primary CTA verbs that fit our voice: **Apply, Join the game, Send
gratitude, Read the Field Guide, Become a citizen.**

Avoid: **Get started, Learn more, Sign up now, Click here, Discover.**

## Section 2: Proof of why-now

This is where the page earns trust quickly. Pick one real, current,
specific anchor:

- A live deadline: "Season 2 applications close on [date]"
- A live event: "Earth Day 2026 Convergence is in 4 days"
- A live shift: "Season 2's shared crowdpool launches at the December
  solstice"
- A live number, only once Rye has marked it public in the admin metrics
  table. Public pages show no counts of players, members, land projects,
  partners, hectares or dollars until then (ruling 2026-09-27).

Anchor the page in time. Generic always-on copy reads as ad copy.

## Section 3: The promise (value-prop ladder)

Every audience cares about three things in this order:

1. **What you get.** The concrete thing in your hands
2. **What you become.** The identity shift the thing enables
3. **What changes in the world.** The collective outcome you're part of

For ReGen Civics, the ladder by audience:

| Audience          | What you get                   | What you become                     | What changes                        |
| ----------------- | ------------------------------ | ----------------------------------- | ----------------------------------- |
| Player            | Quests, badges, $ReGen tokens  | A Citizen with a Field Guide        | A bioregional movement networks    |
| Land project      | Tools, season cohort, a crowdpool | A project with peers and a plan  | Bioregional regeneration scales    |
| Contributor       | A way to bring time, things, skills, land and money to a project | Part of a project's crew | Land projects get what they need |
| Future member     | An invitation into the cooperative's design conversations | A co-designer of the cooperative | Say only what `COOP` says (it is in design) |
| Movement partner  | Coordination, joint quests     | A node in a wider field             | The movement holds together        |

Render as three short paragraphs or a 3-column grid. Don't render as a
9-bullet list.

## Section 4: The mechanism

Plain-language. Three to five steps. Each step is one sentence.

Bad: "Through our innovative regenerative governance and tokenized
incentive layer..."

Good:

> 1. Apply to a season as a player or a land project.
> 2. Earn $ReGen by completing quests and contributing.
> 3. Vote on Game proposals using RGVoice.
> 4. Watch the bioregional results land in real soil.

## Section 5: Social proof

Real names. Real quotes. Real numbers. No stock photos. No fake
testimonials.

If we don't have enough real testimonials yet for a specific page, use
program facts instead: "13 land projects per season cohort. 13 stewardship
roles." Program design facts and the Season One (2022) record in
`shared/regenYear.ts` may appear. Counts of players, members, land
projects, partners, hectares or dollars may not, until Rye marks them public
in the admin metrics table.

If we don't have either, skip the section. An empty social-proof block
is worse than no social-proof block.

### Pull quote patterns

| Pattern                             | When to use                                    |
| ----------------------------------- | ---------------------------------------------- |
| Land steward quote                  | Project / incubator pages                     |
| Player quote                        | Game / quest / community pages                 |
| Contributor or future member quote  | Crowdpooling and cooperative pages (/fund, /opportunity, /loi) |
| Movement partner quote              | Comparison / alongside pages                   |

A quote on a cooperative page never mentions money coming back, what a
membership is worth, or anything the cooperative will pay out.

Each quote: 15-40 words. Name + role + bioregion or organization.

## Section 6: The ask (CTA section)

One primary action. One secondary.

Common pairings:

| Page type           | Primary CTA                         | Secondary CTA                      |
| ------------------- | ----------------------------------- | ---------------------------------- |
| Cooperative         | Tell us you're interested (/loi)    | Read about the cooperative (/fund) |
| Land project        | Apply to next season                | Read the Field Guide               |
| Player              | Start the Welcome Aboard Quests     | Browse all quests                  |
| Movement partner    | Schedule a 30-minute conversation   | Read the alongside page            |

Primary CTA gets a real verb and the noun it acts on. Secondary CTA can
be a text link with an arrow.

## Section 7: FAQ

5-9 questions. Honest. Real questions actual people have asked.

Format:

```
**[Question phrased exactly as a real person would ask it]**

[3-5 sentence answer. Plain language. Names the thing the person is
worried about, then resolves it. If the answer is "we don't know yet,"
say so.]
```

FAQ patterns we should always include:

- **Money:** "Where does the funding come from? Where does it go?"
- **Risk:** "What happens if [thing fails / I drop out / the season
  ends]?"
- **Trust:** "Who's behind this? What's their track record?"
- **Differentiation:** "How is this different from [SEEDS / Hypha /
  other regen projects]?" (link to comparison page)
- **Practicality:** "How much time / money does this require from me?"

Skip "is this for me?". That's a vibe a good page communicates without
asking.

## Section 8 (optional): The honest tension

A trust-builder section. Pattern:

> ### Things to know before you say yes
>
> - This is early. We're running our first incubator seasons; not every
>   piece is polished.
> - The Game's tokens add cognitive load. We explain each one where it
>   appears, and none of them makes a claim about financial value.
> - The cooperative is in design. It is not yet a legal entity, it accepts
>   no money, and its terms will be set with counsel and the founding
>   members.
> - You're committing to participation: quests, forum, seasons. Membership
>   is for the land projects and people who use the cooperative.

If you're doing it right, this section grows the conversion rate by
filtering for the right people earlier.

## A/B variant generation patterns

When asked to "give me 3-5 variant headlines for this hero," vary along
these axes:

- **Direct address vs. third person.** "You can plant a food forest..."
  vs. "Land projects need..."
- **Program fact vs. principle.** "13 land projects per cohort, 13 roles"
  vs. "Tools a land project keeps."
- **Two-part framing vs. single framing.** "Tools and a game" vs. "A game
  that grows regeneration."
- **Stakes vs. invitation.** "The Regenerative Renaissance needs..." vs.
  "Come help us..."

For each variant, write the matching subheadline. The pair has to land
together.

## A/B testing infrastructure (if it exists)

Check `client/src/lib/ab.ts` (or similar) before assuming experiments
exist. If they don't, recommend Rye add a thin variant flag in the URL
or via a feature toggle, run for 2 weeks, look at conversion. Don't
invent A/B infrastructure as part of a copy task; that's its own
project.

## Voice rules (binding)

These ride on top of the project Writing Rules. Specific to landing copy:

- **No em-dashes.** Use commas, periods, or rewrite.
- **No "not X, but Y."** Lead with the affirmative.
- **No "delve, leverage, foster, navigate, unleash, transformative,
  groundbreaking."** AI tells.
- **No "join us on this journey."** Vague filler.
- **Specific numbers beat vague intensifiers.** "13 roles" beats
  "comprehensive cohort."
- **Concrete actions beat abstract aspirations.** "Plant a food forest
  on 5 acres" beats "regenerate landscapes."

### Money, the cooperative and tokens (plan v1.2, Gate G5)

- **The cooperative:** describe it only with the fields of `COOP` in
  `shared/fund.ts`, verbatim (`COOP.statement`, `COOP.designPrinciples`
  introduced by `COOP.designPrinciplesNote`, `COOP.interestPromise`), and
  render `COOP.notAnOffer` once on any page that describes it. It is in
  design and accepts no money. Never use the present tense about its
  members, land, votes or terms.
- **Never promise or price upside.** A purchasing cooperative keeps its
  "bought for use" footing only while nothing in the funnel promises a
  return. `node scripts/check-fund-claims.mjs` fails the build on:
<!-- fund-claims-allow: this line names the G5-banned phrases so agents can avoid them -->
  returns of any kind, IRR, ROI, yield, appreciation, distributions or dividends, exchange listings, token prices, "index fund", portfolio, "invest in land projects", direct investment, accredited investors, minimums, carry, LPs, and any fund terms.
- **Crowdpooling** uses the binding wording: "Crowdpooling coordinates and
  accounts for what people bring to land projects: time, things, skills,
  land and money. Money goes through outside partners each project holds,
  never through ReGen Civics. The campaigns shown today are examples; real
  campaigns open when Season 2 starts crowdpooling."
- **Tokens:** $ReGen and RGVoice are the Game's tokens. `COOP.tokensNote`
  is the general line; $RCivics and RCVoice appear only as
  `COOP.coopTokens` says.
- **Nine forms of capital,** never eight (`shared/capitals.ts`).
- **"Invest"** survives only in the everyday sense with no money nearby
  ("invest your time in the quest"). When in doubt, cut the sentence.

## Cross-references

- `regen-fundraising-copy` for the narrative voice that fills these
  blocks
- `regen-comparison-pages` for the "alongside" page structure
- `regen-form-design` for any form embedded in a CTA section
- `regen-seo-audit` for the meta tags and OG image of the page
- `CONTEXT_THE_TWO_GAMES.md` for the two-sided framing (where it describes
  the Fund side, the cooperative replaces it, in `COOP`'s words)
- `shared/fund.ts` (`COOP`) for every sentence about the cooperative
- `docs/planning/SOCIAL_SHARING_SPEC.md` for share preview optimization
