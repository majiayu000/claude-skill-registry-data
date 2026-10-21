---
name: website-content-guide
description: >
  Create and maintain a new site's CONTENT_GUIDE.md and BRAND.md — Tone of Voice
  and EEAT (Experience/Expertise/Authoritativeness/Trust) signals — so every page
  hangs off one source of truth for HOW it says it. Reads positioning from
  POSITIONING.md (owned by website-positioning, which runs first); it does not
  redefine positioning. Use at the start of a new site (step 3 of the new-website
  pipeline, after website-positioning), before writing page copy, and whenever
  reviewing/editing copy for voice. Pairs with the tone test (tests/tone.spec.ts)
  which hard-enforces the voice rules. Trigger phrases: "content guide", "tone of
  voice", "brand voice", "is this on brand", "EEAT", "E-E-A-T", "write the content
  guide", "set up the brand doc", "review the copy", "does this sound like AI".
---

# Website content guide & voice

Owns the **how it says it** layer of a new site: tone of voice and EEAT signals,
captured in the per-site docs that everything downstream reads. **Positioning**
(what you offer, for whom, the market category) is owned by `website-positioning`
and worked out first; this guide reads it from `POSITIONING.md` and must stay
consistent with it — it does not redefine it. A quick "does this still read
clearly to a stranger" check on an already-built site is `website-positioning-check`,
not this guide — it's a read-only diagnostic, not a voice/EEAT audit.

## Outputs

- **`CONTENT_GUIDE.md`** (from the `new-website` skill's `templates/content-guide.md`)
  — ToV rules, EEAT checklist, page inventory with target titles, per-page-type
  copy templates, new-page checklist. Reads positioning/audience from `POSITIONING.md`.
- **`POSITIONING.md`** is owned by `website-positioning`; this guide consumes it
  and must not restate the positioning (single source of truth).
- **`BRAND.md`** is owned by `website-design-system`, but its positioning line
  comes from `POSITIONING.md` — keep them consistent. Each of its two parts, the palette and
  the logo, has its own source: what the owner brought or chose at `new-website` §2b
  (her own colours or logo, or the ones the optional `website-brand-kit` helped her to)
  stands, and is not changed here. A part she neither brought nor wanted help with
  keeps the starter's default until `website-design-system` fills it.
- **`STORY.md`** (optional, owned by `website-story`): when present, the home page's
  section order in the per-page-type copy template comes from its seven-section map.
  The voice rules here apply unchanged.

## How to use

1. Positioning comes first: `website-positioning` has already produced
   `POSITIONING.md` (what you offer, for whom, the market category). Read it and
   build the voice on top of it. Then pull insights: run `customer-research` for
   ICP + voice-of-customer, and `content-strategy` if topic planning is needed.
   Feed the findings in.
2. Copy the template to `CONTENT_GUIDE.md` and fill every `[BRACKET]`.
3. For actual page copy, hand off wording to `copywriting`, then apply the voice
   rules below and run the tone test.

## Tone of voice — the hard rules (enforced by the tone test)

These mirror the tone guards proven on earlier production sites. The test is the source of
truth; the guide explains the *why*.

- **No em dashes (—).** Comma, period, or colon instead.
- Active voice; proof over claims.
- **Exempt:** genuinely quoted customer/human voice — wrap in `<blockquote>`,
  `<q>`, or add `data-tov-exempt`. Do not use this to smuggle brand copy past the
  rules.

The rules below are lexical (specific words/mechanisms to avoid) and differ by
language — apply the subsection that matches the site's content language.

### English content
- **No contractions.** Long form: "cannot", "it is", "you are", "we are".
- **No buzzwords:** supercharge, world-class, leverage, unlock, seamless, robust,
  cutting-edge, empower, holistic, revolutionary, synergy, next-level (trim/extend
  per brand).
- Speak to the reader as "you".

### German content
English's "no contractions" rule has no German equivalent — German doesn't
contract "cannot" into "can't" the way English does, so there's no parallel
mechanism to enforce. The real formality lever in German is **register:
informal "du" vs. formal "Sie"** — and, more important than which one you
pick, staying **consistent** with that choice for the entire page. Mixing
"du" and "Sie" mid-page doesn't read as a stylistic choice; it reads as a
translation error.

- **Pick du or Sie per brand, then hold it for the whole page.** This is a
  per-brand decision, not a universal rule — record the choice explicitly in
  `BRAND.md`/`CONTENT_GUIDE.md` so every page follows the same one. A
  community/consumer brand aiming for approachable and informal typically
  picks "du" throughout; a B2B/enterprise or public-sector brand more often
  picks "Sie" — either is fine as long as it's consistent.
- This *is* the German answer to "speak to the reader as 'you'" — the du/Sie
  choice above settles it; don't treat "you" as a separate, unresolved
  question for German copy. tone.spec.ts machine-checks the unambiguous
  mixing cases (lowercase du-family vs. capitalized "Kontaktieren Sie ..."
  imperatives on one page); subtler shifts still need a human read.
- **No buzzwords:** ganzheitlich, nahtlos, Synergie(n), Synergieeffekt(e/en),
  bahnbrechend, revolutionär, wegweisend, erstklassig, hochmodern,
  maßgeschneidert (Swiss spelling "massgeschneidert" is caught too — the
  enforced test doesn't fold ß↔ss, so both spellings are listed explicitly),
  zukunftsweisend, transformativ, unschlagbar, entfesseln/entfesselt,
  Spitzenreiter (trim/extend per brand).
- **AI-tell phrases to avoid:**
  - "In der heutigen ... Welt" (the enforced test tolerates up to two
    modifiers and compound Welt-nouns like "Geschäftswelt")
  - "Es ist wichtig zu betonen/beachten/erwähnen, dass..."
  - "Zusammenfassend lässt sich sagen,..."
  - "Lassen Sie uns / Lass uns / Lasst uns eintauchen / einen Blick werfen"

## EEAT — build it in from the start

Search and AI answer engines reward Experience, Expertise, Authoritativeness,
Trust. Ship the signals, not just claims:
- **Experience/Expertise:** named authors with a real bio and a stable schema
  `@id`; first-hand specifics and dates; inline citations on claim-heavy copy.
- **Authoritativeness:** `sameAs` profiles that actually resolve (LinkedIn,
  GitHub, public register); Organization schema; corroborating external mentions.
- **Trust:** imprint/legal entity page, clear contact, privacy page, last-updated
  timestamps, HTTPS, zero broken links.

The author/Organization/`sameAs` plumbing lives in `website-seo-geo` (schema) and
`config.ts`/`SAME_AS`; this skill decides *what* those signals should be.

## Done means

`CONTENT_GUIDE.md` filled, voice consistent with `POSITIONING.md` and `BRAND.md`,
and the tone test green after any copy change (`npm test` runs `tone.spec.ts`).
