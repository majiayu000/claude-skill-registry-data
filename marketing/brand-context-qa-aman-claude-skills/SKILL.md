---
name: brand-context
description: Create and maintain the shared knowledge/ context files that every other marketing skill reads - brand voice, ICP personas, positioning, KPIs, and the learnings log. Run this once per company or client before using any other marketing skill. Use when the user says "set up brand context", "onboard my brand", "set up the marketing knowledge base", "the skills don't know my brand", "update our positioning", "our voice has changed", "add a new persona", or when any marketing skill reports that a knowledge/ file is missing. Also use when output sounds generic or off-brand. For writing a positioning statement as a standalone document, see positioning-doc. For deep persona research from raw sources, see customer-research.
metadata:
  grounded_in:
    - "Obviously Awesome - April Dunford"
    - "Lean Analytics - Croll & Yoskovitz"
    - "Competing Against Luck - Clayton Christensen"
    - "Nielsen Norman Group tone-of-voice model"
  reads:
    - knowledge/
  writes:
    - knowledge/brand/voice.md
    - knowledge/brand/visual.md
    - knowledge/icp/personas.md
    - knowledge/markets/positioning.md
    - knowledge/markets/competitors.md
    - knowledge/kpis.md
    - knowledge/learnings.md
---

# brand-context

Builds the `knowledge/` folder that the rest of the marketing skills read before they write anything. Without it, every skill produces competent generic output. With it, output carries the company's actual voice, audience, positioning and targets.

Run once per company or client. Re-run any single section when something changes.

## Why this exists

21 of the 25 marketing skills declare a read on `knowledge/`. If those files are absent, some skills stop and the rest quietly guess. This skill is the only writer of that folder.

## The files it owns

| File | What it holds | Read by |
|---|---|---|
| `knowledge/brand/voice.md` | Tone dimensions, vocabulary, banned words, sentence rhythm, worked examples | Nearly every writing skill |
| `knowledge/brand/visual.md` | Colours, fonts, logo rules, template path | ppt-maker, ad-campaign-writer |
| `knowledge/icp/personas.md` | One block per persona: job, trigger, pains, alternatives, objections | Most planning and writing skills |
| `knowledge/markets/positioning.md` | Category, competitive alternatives, unique attributes, value, best-fit segment | positioning-doc, landing-page-writer, ad-campaign-writer |
| `knowledge/markets/competitors.md` | Named competitors, their claims, where we win and lose | competitor-analyst, content-writer |
| `knowledge/kpis.md` | The one metric that matters now, supporting metrics, current baselines | campaign-brief, kpi-review, social-calendar |
| `knowledge/learnings.md` | Append-only log of what worked and what did not | retro writes it, six skills read it |
| `knowledge/company.md` | What the company does, model, stage, verified proof points, claim constraints | case-study-writer, press-release-writer |
| `knowledge/services/` | One file per product or offering, with what is and is not included | landing-page-writer, ad-campaign-writer, campaign-brief |
| `knowledge/content-library/` | Past published content, so skills do not repeat topics | content-repurposer, social-calendar, newsletter-writer |

## Modes

Ask which mode, or infer from what the user gives you.

1. **Interview** (default). Ten to fifteen minutes of questions. Use when there is no existing material.
2. **Draft from sources.** The user supplies a website URL, a deck, a pitch, existing copy, or a folder. Read those with WebFetch or Read, draft every file, then present each for correction. Always faster and always needs the correction pass.
3. **Update one section.** The user names what changed. Touch only that file and bump its `updated` date.

## Process

1. **Check what already exists.** List `knowledge/`. If files are present, read them and report what is covered and what is missing. Never overwrite a populated file without showing the user the current content and getting explicit confirmation.

   If `knowledge/` does not exist at all, copy the blank templates that ship with this skill before starting: `cp -r ${CLAUDE_SKILL_DIR}/assets/knowledge ./knowledge`. Every other skill then reads a template with visible `[TEMPLATE]` markers instead of hitting a missing file, which degrades far more gracefully.

2. **Pick the mode** and gather source material if mode 2.

3. **Work through the sections below in order.** Positioning depends on personas, and KPIs depend on positioning, so the order matters.

4. **Drafting and writing are different acts. Always draft. Gate only the write.**

   The gates in this skill protect the `knowledge/` folder from unreviewed content. They are not
   a reason to withhold work. Refusing to produce a draft is a failure of this skill, not caution.

   | Act | Gate |
   |---|---|
   | **Draft** the content and show it in full in your response | None. Always do this |
   | **Write** it to `knowledge/` for the first time | Show it, then write. Say what you wrote |
   | **Overwrite** a populated file | Show current content, show the change, wait for an explicit yes |

   In mode 2, draft every file from the sources, present each one complete, and mark anything you
   inferred rather than found with `[NEEDS INPUT]` or `[UNVERIFIED]`. Do not stop at "I need more
   information": produce the draft from what the sources give you and name the gaps inside it.

   In mode 3, perform the update. Read the current section, produce the revised version in full,
   show the difference, and write on confirmation. Do not refuse an update because the request was
   short.

   Write each file as you complete it rather than at the end, so a user who runs out of time keeps
   what is done.

5. **Run the completeness gate** and report the score.

6. **Tell the user what to run next.**

## Section 1: brand voice

Framework: the four tone dimensions from the Nielsen Norman Group tone-of-voice model.

Ask the user to place the brand on each axis, then make them justify one of the four with an example:

| Dimension | Ask |
|---|---|
| Funny to serious | Would a joke in a product email feel right or wrong? |
| Formal to casual | Do you write "cannot" or "can't"? Do you use first names? |
| Respectful to irreverent | Do you ever name a competitor, or push back on your own industry? |
| Enthusiastic to matter-of-fact | Is a launch "huge news" or "now available"? |

Then capture the mechanics, because tone words alone do not constrain a writer:

1. **Words we use.** Ten to twenty terms specific to this business, including how the product and the customer are named.
2. **Words we never use.** Jargon, hype, competitor terms, anything legal has banned.
3. **Sentence rhythm.** Short and punchy, or considered and flowing. Give a target sentence length if the user has a view.
4. **Punctuation rules.** Em dashes, exclamation marks, emoji, Oxford comma. Ask explicitly, these are the details that make output feel foreign.
5. **Two worked examples.** One paragraph the user considers on-brand and one they consider off-brand, with a sentence on why. This is the single most useful part of the file, so do not let it be skipped.

Write to `knowledge/brand/voice.md`:

```markdown
---
updated: DD-MM-YYYY
source: interview | drafted from [url or file]
---
# Brand voice

## Tone
| Dimension | Position | Evidence |
|---|---|---|
| Funny - serious | [position] | [why] |
| Formal - casual | [position] | [why] |
| Respectful - irreverent | [position] | [why] |
| Enthusiastic - matter-of-fact | [position] | [why] |

## Vocabulary
**We say:** [terms]
**We never say:** [terms]
**We call the product:** [name and any rules]
**We call the customer:** [term]

## Mechanics
[rhythm, sentence length, punctuation rules]

## On-brand example
> [paragraph]

Why: [reason]

## Off-brand example
> [paragraph]

Why: [reason]
```

## Section 2: ICP personas

Framework: Jobs to be Done (Clayton Christensen) for the trigger, April Dunford for the alternatives.

One block per persona. Cap at three. A fourth persona is usually a segment nobody has actually sold to, so challenge it: "Have you closed at least three of these? If not, I will mark it provisional."

For each, capture: role and seniority, the job they hire this product to do, the trigger event that starts the search, top three pains in their own words, what they use today including doing nothing, their top three objections, and where they get information.

Two rules:
1. **Pains must be quoted, not paraphrased.** If the user has no real quote, mark the line `[NEEDS INPUT: real customer language]` rather than inventing one.
2. **"Doing nothing" is always a listed alternative.** It is the most common competitor and skills that forget it write copy that argues against the wrong thing.

Write to `knowledge/icp/personas.md`, one `## Persona: [name]` block each, with a `confidence: high | provisional` field per persona.

## Section 3: positioning

Framework: April Dunford's *Obviously Awesome* sequence, run in order.

1. **Competitive alternatives.** What would this customer do if this product did not exist? Behaviours, not brand names. Spreadsheets, an agency, an intern, nothing.
2. **Unique attributes.** What do we have that the alternatives do not? Features and capabilities, stated plainly.
3. **Value.** What does each attribute let the customer do that they could not before? Attribute to value, one line each.
4. **Who cares most.** The segment for whom that value is urgent rather than nice.
5. **Market category.** The frame that makes the value obvious to that segment.

The test before writing the file: if a competitor could claim the same statement without changing their product, it is not positioning. Say so and rerun step 2.

Write to `knowledge/markets/positioning.md` with the five sections plus a one-paragraph statement at the top.

## Section 4: competitors

Only if the user names competitors. Three to five, each with: what they claim, who they win with, where we genuinely lose to them.

**"Where we lose" must not be empty.** A competitor file with no losses is a marketing document, not a working file, and downstream skills will write copy that ignores real objections. If the user resists, ask which deals they lost last quarter and to whom.

Write to `knowledge/markets/competitors.md`.

## Section 5: KPIs

Framework: the One Metric That Matters (Croll and Yoskovitz, *Lean Analytics*).

1. **The OMTM for this quarter.** One metric. If the user names three, ask which one they would keep if they could only see one number.
2. **Current baseline** for that metric, with the date measured. A target without a baseline is a wish.
3. **Target and by when.**
4. **Three supporting metrics** with baselines.
5. **What we deliberately are not optimising** this quarter.

Mark any number the user is unsure of as `[UNVERIFIED]`. Downstream skills, especially `kpi-review` and `campaign-brief`, treat unverified baselines differently from measured ones.

Write to `knowledge/kpis.md`.

## Section 6: the learnings log

Create `knowledge/learnings.md` as an empty structured file. This skill never writes entries, `retro` does.

```markdown
---
updated: DD-MM-YYYY
---
# Learnings

Append-only. Written by `/retro` after a campaign. Read by campaign-brief,
social-calendar, content-writer, email-nurture, ad-campaign-writer, kpi-review.

Each entry: date, campaign, what happened, why (Five Whys terminal cause),
scope (this-campaign-only | all-future-campaigns). Only all-future entries
change how later skills behave.

<!-- No entries yet. Run /retro after your first campaign. -->
```

## Completeness gate

Score before finishing and report it. Do not claim the setup is done below 7.

| Check | Points |
|---|---|
| Voice file has both worked examples filled in | 2 |
| At least one persona at `confidence: high` | 2 |
| Every persona lists "doing nothing" as an alternative | 1 |
| Positioning survives the competitor-could-claim-this test | 2 |
| OMTM has a dated baseline, not just a target | 2 |
| Competitors file has a non-empty "where we lose" (or no competitors named) | 1 |
| Every unverified number is tagged `[UNVERIFIED]` | 1 |
| Every missing customer quote is tagged `[NEEDS INPUT]` | 1 |

Report as `Context completeness: N/12` plus the specific gaps. Then say which skills are safe to run now and which will still guess.

## Rules

- **Never invent a customer quote, a competitor claim, or a metric baseline.** Tag it and move on. An invented persona pain propagates into every downstream artifact and is very hard to trace back.
- **Never overwrite a populated file silently.** Show the current content, propose the change, wait.
- **Never refuse to draft.** The gates above cover writing to disk, not producing work. If inputs
  are thin, draft what they support, tag the rest, and say what would improve it. A response that
  contains no drafted content has not done this skill's job.
- Keep every file under 200 lines. These are read by other skills on every run and long files cost context on every invocation.
- Date every file `DD-MM-YYYY` in frontmatter and update it on any edit.
- If the user only has ten minutes, do voice and one persona. Those two unblock the most skills.

## Related skills

- `/positioning-doc` turns section 3 into a full standalone positioning document
- `/customer-research` sources real persona material when the user has none
- `/competitor-analyst` does the deep ERRC and strategy-canvas work that section 4 only summarises
- `/retro` is the only other writer of `knowledge/`, and it writes `learnings.md`

## What this skill cannot know

- Whether the voice captured here is how customers actually perceive the brand, as opposed to how the team wants to be perceived
- Whether a persona describes real buyers or the team's hopes, until `/customer-research` sources evidence
- Whether a stated KPI baseline was measured or estimated, beyond what the user tells you
- Whether the positioning survives contact with a competitor's next release
