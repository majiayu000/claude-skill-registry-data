---
name: website-story
description: >
  OPTIONAL story layer: narrate the home page as the customer's story — the
  visitor as hero, their problem as the villain, the brand as the guide with a
  three-step plan — captured in STORY.md and mapped onto a seven-section home
  page. Inspired by Donald Miller's StoryBrand framework, in this suite's own
  words. POSITIONING.md still decides WHAT is claimed; STORY.md decides only how
  the home page tells it and loses every conflict. Never runs unasked: offered
  once after website-positioning, or run later on an existing site when asked.
  Ships an opt-in tests/story.spec.ts. Trigger phrases: "tell it as a story",
  "customer as the hero", "story layer", "StoryBrand", "one-liner", "grunt
  test", "homepage reads like a feature list", "lead magnet", "what do they
  lose if they do nothing". Not for positioning itself, voice, or a quick check.
---

# Website story

A narrative layer on top of positioning. Positioning (`website-positioning`,
`POSITIONING.md`) decides **what** the site claims, for whom, in which category.
This skill decides **how the home page tells it**: as the visitor's own story, with
the brand as the guide, not the hero. Optional, never part of the default build.

The vocabulary and the seven-section map below are this suite's own; the ideas are
inspired by Donald Miller's StoryBrand framework (*Building a StoryBrand*).

**The governing rule: `POSITIONING.md` is the source of truth for what is claimed.
`STORY.md` only decides how the home page narrates it. On any conflict, positioning
wins and `STORY.md` is corrected.**

## The offer (what the orchestrator says to the owner)

The owner has usually never heard of this. Explain it before asking, in the
language the owner writes in (per `new-website` §1), roughly like this:

> Positioning is done: we know what you offer, for whom, and against which
> alternative. Optional next step: build the home page as your customer's story.
> The idea comes from Donald Miller's book *Building a StoryBrand*: the visitor is
> the hero, you are the guide. The page opens with a one-liner (who you help, the
> problem, your plan, the result), shows what is at stake if nothing changes, gives
> a simple three-step plan, shows life after, and repeats one clear call to action.
> Most home pages talk about the company; this one talks about the customer. It
> does not change your positioning, only how the home page tells it. Want me to do
> this? (yes / no; you can ask for it any time later)

This text lives here, once. `new-website` §2a reads it from here; do not restate it.

## 0. When it runs

- **Offered once** by `new-website` §2a, right after `POSITIONING.md` is filled and
  before the content guide. "No" or no answer means the standard home page; say
  nothing more about it.
- **Later, on any site**, when the owner asks ("build the home page as a story",
  "what do we do in one sentence", "the home page reads like a feature list").
- **Prerequisite:** a filled `POSITIONING.md`. If it is missing or half-filled, run
  `website-positioning` first. Never derive story elements from guesswork. An
  existing site often has the facts without the file (a wording guide, a pinned
  definition, comparison pages, a brand doc): then the positioning step is to draft
  `POSITIONING.md` from those sources, citing the file each line comes from and
  marking gaps as unverified, and to let the owner confirm it before the story is
  derived. The story never becomes the place where positioning is decided.
- **Scope:** the home page. Other pages only when asked, and then one at a time.

## 1. Outputs

- **`STORY.md`** (from this skill's `templates/story.md`; the bundled copy of the skill
  on a handed-off repo has it too, as `.claude/skills/website-story/templates/story.md`):
  the story elements, the one-liner, and the seven-section home page map. It goes next
  to `POSITIONING.md`: the repo root on a new site, or `docs/` on a site that keeps its
  strategy documents there. Look in both places before concluding either file is missing.
- Optional **`tests/story.spec.ts`** (from `templates/story.spec.ts`), see §6.

Explicitly **not** touched: `POSITIONING.md`, `tests/positioning.spec.ts`,
`SITE.tagline` in `src/config.ts`, and the "Brand in one line" in `BRAND.md`. Those
are positioning surfaces and stay with `website-positioning`, except `SITE.tagline`,
which belongs to `website-tagline`.

## 2. Derive the story from the positioning

Every line in `STORY.md` must be traceable to a line in `POSITIONING.md`:

| Story element | Comes from `POSITIONING.md` | Rule |
|---|---|---|
| Character: who + one want | §4 Target customer + "why they care most" | same segment, in their own words; one want, not a list |
| Problem: villain, external, internal, philosophical | §1 Competitive alternatives + §4 "why they care most" | the villain is the status quo or the situation, never a competitor by name |
| Guide: empathy + authority | §2 Unique attributes + §3 Proof | authority reuses existing proof only; nothing new is asserted here |
| Plan: three steps | how the attributes are delivered / how to start | verb-first; each step ends in what the visitor gets |
| Success: life after | §3 Value | concrete and visual, about the customer |
| Stakes: cost of doing nothing | staying with §1 | proportionate; the truth of the alternative, not fear |
| Market category | §5 | unchanged; still appears in the header |
| One-liner + controlling idea | the positioning statement | narrows the core positioning term, never replaces it |

If writing the story exposes a positioning error (the want does not match the
segment, the proof does not support the authority), **stop**: fix `POSITIONING.md`
via `website-positioning`, then return and correct `STORY.md`. Do not paper over it
in the story.

## 3. Fill STORY.md

Copy the template as `STORY.md` next to `POSITIONING.md` (repo root or `docs/`, see §1)
and fill every `[BRACKET]`:

- **Character.** Who they are and the one thing they want, in their words (pull
  phrasing from `customer-research` voice-of-customer where it exists).
- **Problem, three layers.** External: the practical thing in the way. Internal:
  how it makes them feel. Philosophical: why it is simply wrong that they have to
  put up with it. Name the villain: the situation, the status quo, the way things
  are usually done.
- **Guide.** One empathy sentence ("we know what it is like to…") and one authority
  sentence backed by proof already in `POSITIONING.md` §3. Empathy restates the
  customer's situation from §4 in warmer words; it adds no new fact about it.
  Empathy without proof is a claim; proof without empathy is a brochure.
- **Plan.** Three steps, each starting with a verb and ending in what the visitor
  gets. Give it a title. Four is the maximum; five is a process page, not a plan.
- **Direct call to action.** One label ("Get a quote", "Book a call"), used verbatim
  everywhere it appears. Active, specific, never "Learn more".
- **Transitional call to action.** A lead generator with a specific title (a
  checklist, a short guide, a sample), in exchange for an email. If the site has
  none, leave the slot blank. Do not invent one.
- **Stakes.** One to three things that stay wrong or get worse if nothing changes.
  Loss language is what makes people act, but keep it proportionate, and mind the
  register: state what the visitor keeps missing ("meet before the conference, and she
  may introduce you to the people you need"), not what will go wrong for them. In
  formal-register markets and most B2B copy, one such line is enough; agitation reads
  as pressure there and costs trust.
- **Success.** One to three lines of life after, about the customer, concrete.
- **One-liner.** Character + problem + plan + success, at most 30 words, usually two
  or three short sentences. Open on the visitor's own moment, in the second person
  and the present tense ("When you travel, you keep missing people worth seeing
  again."), then the mechanism, then the outcome. A moment the visitor recognises
  lands harder than a statistic about people like them ("Most travelers…"). It must
  pass a stranger test: does someone who has never heard of you understand what you do
  and for whom? No em dashes, so it survives the tone test when pasted into copy.
- **Controlling idea.** The single thought the whole page reinforces, at most ten
  words. It must agree with the core positioning term in `POSITIONING.md`.

**Non-English builds:** write the one-liner and the controlling idea as native
sentences; do not fill an English frame with translated words (same rule as
`POSITIONING.md`).

**Worked example** (this suite's own story, from a real site it built; the evals use a
different business on purpose, so reuse the shape, not the words):

- Input, from `POSITIONING.md`: target = organizers, founders and small businesses who
  need a site that ranks within a week and will not pay a monthly fee; alternatives = a
  subscription site builder, WordPress, an agency; unique attributes = open-source
  skills an AI assistant runs end to end, static output on free hosting, a shipped test
  suite; proof = genai-wednesday.de live in one week, PageSpeed 98/100/100/100, no
  monthly fee; value = a site that ranks and reads well.
- Feature-list one-liner (fails the stranger test, the product is the subject): "An
  open-source suite of Claude Code skills that scaffolds Astro sites with SEO, tests
  and Cloudflare deployment."
- Story one-liner (28 words, the visitor's own moment first): "You need a site people
  find, and every option costs months or a monthly fee. With the builder, your AI
  assistant ships a tested site in a week."
- Controlling idea: "A site that ranks, live in a week."
- Plan, titled "Live in a week": 1. Say what you offer and for whom → the positioning.
  2. Let the assistant build and test → every page checked. 3. Publish on free hosting
  → your domain, your code.
- Direct CTA: "Build your first site", used in the header, after the plan, and at the end.

Every line above traces to one positioning section; nothing was added to it.

## 4. The seven-section home page map

Fill the map in `STORY.md`; `copywriting` writes the page from it in this order:

| # | Section | Job |
|---|---|---|
| 1 | **Header** | Pass the grunt test in five seconds: what you do, how it makes life better, how to get it. `<h1>` plus the one-liner as the first paragraph. Direct CTA button. Up to three short outcomes, one per success line in `STORY.md` §7 (fewer is fine; never invent one). An image of the customer succeeding, not of the company. |
| 2 | **Stakes** | The stakes from `STORY.md` §6, one to three lines in the "what you keep missing" register (one line in formal-register and most B2B copy), then a one-line pivot to the guide. No extra pains beyond §6. |
| 3 | **Plan** | The titled three-step plan as an `<ol>`. Direct CTA again. |
| 4 | **Value stack** | The success lines from `STORY.md` §7, each a headline plus one sentence, describing life after. As many as §7 has, up to three. |
| 5 | **Explanatory paragraph** | The guide: empathy, then authority. Answer the top objections, using only facts already in `POSITIONING.md`; an objection the positioning cannot answer is listed for the owner, not answered with an invented promise. Give the visitor room for due diligence with a "read more" to the about or offer page. |
| 6 | **Lead generator** | The transitional CTA with its specific title. Omit the section if the slot is blank. |
| 7 | **Junk drawer** | FAQ, careers, everything else. Final direct CTA. |

Hard notes:
- The `<h1>` or the intro paragraph still carries the page's positioning term, and
  the body still contains the market category: `positioning.spec.ts` is unchanged
  and must stay green.
- The direct CTA appears at least in the header and once more (after the plan or
  at the end). Same label, same target.
- Every headline has the customer as its subject. The company appears as the
  guide in section 5, and nowhere as the hero.
- Positive and negative language both belong: success (4) and stakes (2) are two
  halves of one story.

## 5. Hand-off

- **Copy:** `copywriting` writes the page from the map; the tone rules in
  `CONTENT_GUIDE.md` apply unchanged and `tone.spec.ts` still gates.
- **Record the choice** in the project README next to the decision-interview
  answers ("home page: story-led, see STORY.md").
- **Review:** `website-review` checks `STORY.md` agrees with `POSITIONING.md`;
  `website-positioning-check` judges the header by the grunt test.

## 6. `story.spec.ts`: the opt-in guard

Copy this skill's `templates/story.spec.ts` into the site's `tests/` and fill its
`CONFIG` block from the values `STORY.md` lists at its end (`planStep` is `li` for a
real list; a numbered card grid names its card class instead). It lives here rather than
in the `new-website` Astro overlay because a fresh scaffold has no story to assert.

| assertion | the bug it catches |
|---|---|
| The direct CTA appears at least twice as a visible link or button with exactly that label, and (with `directCtaHref`) always the same target | the repeat being cut, the label drifting ("Get a quote" / "Request quote") until fewer than `directCtaMin` copies still match (a third, drifted copy beside two exact ones is not caught), or one copy pointing to another page or site |
| The one-liner or controlling idea is in the body text | the one line the page exists to say being edited away |
| The plan is one container of three or four non-empty steps (a list, or a card grid via `planStep`) | the plan growing into a process, or being restyled into prose |

Hermetic string checks, sibling to `positioning.spec.ts`: no network, no extraction
library, not a density check. Every test skips with a stated reason while `CONFIG`
is empty, so an unconfigured copy reports "not applicable" rather than failing like
a product bug. An unconfigured copy left in a repo is a smell, not a pass. The
suite's `template-tests.yml` runs only the Astro overlay, so this template is not
exercised by the suite's CI: verify it against the real site once, then keep it in
the site's `npm test`.

## 7. Gotchas

- The villain is a situation, never a named competitor.
- If the problem reads like a missed nicety rather than a pain, do not inflate it.
  Narrow the character instead: find the visitor for whom it is a loss (the founder
  whose next investor is someone they already know), and tell their story. A vitamin
  for everyone is a painkiller for someone.
- Stakes that are overdone read as a threat and lose the reader; one true cost
  beats three invented ones.
- The one-liner is not the `<title>` and not the tagline. The `<title>` stays with
  positioning and SEO limits; the tagline belongs to `website-tagline`.
- Do not restate the positioning inside `STORY.md`; link to it. Two sources of
  truth drift.
- No lead magnet is better than a fabricated one.
- A plan with five or more steps is a process page, not a plan.
- Answer the question that was asked. "Which villain?" wants a decision and its
  reason, not a whole `STORY.md`; the draft comes when the owner asks for the build.

## Boundaries (do not duplicate)

- **Positioning, the spine** → `website-positioning`.
- **The tagline (the short line under the logo)** → `website-tagline` (optional).
- **Tone of voice, EEAT** → `website-content-guide`.
- **Quick fresh-eyes check of an existing site** → `website-positioning-check`.
- **Writing the actual copy** → `copywriting` (reads `STORY.md` for the home page).

## Done means

`STORY.md` filled with every element traceable to `POSITIONING.md`, the home page
built in the seven-section order, the direct CTA repeated, `positioning.spec.ts` and
`tone.spec.ts` green, and `story.spec.ts` configured and green if the site adopted it.
