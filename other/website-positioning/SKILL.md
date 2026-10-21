---
name: website-positioning
description: >
  Work out a new site's POSITIONING before any SEO or content — what you offer,
  for whom, and the market category it sits in — using April Dunford's
  five-component framework, captured in POSITIONING.md and threaded through every
  page's title, description, H1 and schema. Owns the positioning spine; enforced
  by tests/positioning.spec.ts (a hermetic per-page string test, sibling to the
  tone test). Use FIRST on a new site (step 2 of the new-website pipeline), before
  website-content-guide, before page copy, and whenever the offer or audience
  shifts. Trigger phrases: "positioning", "value proposition", "what are we
  offering", "who is this for", "market category", "positioning statement",
  "Dunford", "frame the offer", "how do we describe ourselves".
---

# Website positioning

Owns the **what you offer, for whom, and in what category** layer — the spine the
whole site hangs off. It is worked out **first**, before SEO keywords and before a
word of page copy: positioning decides what the copy is even trying to say.
`website-content-guide` (voice + EEAT) and everything downstream **read** this; they
do not redefine it.

The five-component framework is **domain-agnostic** — it positions any kind of site (a
SaaS product, a local service business, a consultancy, a personal portfolio, a nonprofit,
an event, a community). Only the answers change, never the components; the tech-comparison
example below is just the clearest case for the per-surface map form, not the expected
subject matter.

## Outputs

- **`POSITIONING.md`** (from the `new-website` skill's `templates/positioning.md`)
  — the five Dunford components, a one-paragraph positioning statement, reusable
  boilerplate, and the **per-page positioning spine** (one term per page). It lives
  in the repo root on a new site; an existing site may keep it in `docs/` with its
  other strategy documents. Look in both before concluding it is missing.
- The **`POSITIONING` map** in `tests/positioning.spec.ts` — the same spine, in
  code, that hard-enforces each page carries its term.

## How to use

0. **Explain it to the owner first.** Most owners have never worked through
   positioning and will otherwise be asked about "competitive alternatives" and
   "market categories" cold. Before the first question, say in the language the
   owner writes in (per `new-website` §1), roughly:

   > Before any text or design we work out your positioning: what you offer, for
   > whom, and what they would use instead. The method is April Dunford's, from her
   > book *Obviously Awesome*. It has five parts: the alternatives your customer has
   > today, what you have that they do not, the value that creates and the proof for
   > it, who cares most about that value, and the market category that makes the
   > value obvious. The answers become the one sentence every page hangs off. It
   > takes a few questions; there are no wrong answers.

   This is an explanation, not an offer: positioning is required. Keep it to those
   few sentences and move on to the questions.
1. **Pull insights first.** Run `customer-research` for the real ICP, jobs-to-be-done
   and voice-of-customer, and `competitor-alternatives` (or a quick scan) for what
   customers use today. Positioning is grounded in those facts, not invented.
2. **Fill the five components** in `POSITIONING.md` (the Dunford framework):
   1. **Competitive alternatives** — what the customer would use if you did not
      exist (often the status quo, a spreadsheet, an in-house team, doing nothing —
      not just direct rivals).
   2. **Unique attributes** — what you have that those alternatives do not.
      Capabilities and assets, stated as facts, not adjectives.
   3. **Value + proof** — the benefit each attribute makes possible that the
      customer actually cares about, with evidence (a metric, a mechanism, a reference).
   4. **Target customer** — who cares *a lot* about that value; the best-fit
      segment described by traits you can identify, not "everyone".
   5. **Market category** — the context you place the offer in so the value is
      obvious. Pick the category where your unique value wins. Search each
      candidate before choosing (a trap test): if the results are a different
      concept, the category will mis-file the site. When the only safe category is
      also bland ("an app for business travelers"), keep it, and use the frame the
      customer already holds as the **unlike** in the statement ("not another
      itinerary app"), never as a title, slug or schema value. The familiar frame
      does the explaining; the bland category keeps the site correctly filed.
3. **Write the positioning statement** (one paragraph) and the boilerplate from
   the components. Derive the **core positioning term** — the short, plain phrase
   you will thread through the home page. Optionally add a **human version** of the
   statement: the same claim in the owner's own voice, for pitches and the About
   page. The Dunford paragraph stays the reference; the human version may not add
   a claim it lacks.
4. **Set the per-page spine.** One positioning term per page in the
   `POSITIONING.md` table, then mirror it into the `POSITIONING` map in
   `tests/positioning.spec.ts`. The home page also declares `body` phrases (its
   **market category** + the core positioning phrase), checked in the page body.
5. **Thread it, then enforce it.** As each page is built it must carry its term
   verbatim in `<title>`, `<meta description>` and `<h1>` (the test drives this red
   → green, same loop as adding a route to `PAGES`). Feed the 50-word boilerplate
   into the schema `description` via `website-seo-geo`.

## The positioning spine — the hard rule (enforced by the test)

`tests/positioning.spec.ts` asserts, for every page in the `POSITIONING` map:

- the page's **`<title>`** contains its positioning term,
- the page's **`<meta description>`** contains it,
- the page's **`<h1>` or the intro paragraph** (the sentence right under it) contains it —
  so the H1 can stay human while the term is still threaded,
- and any phrases in the page's **`body`** array (typically the market category and the
  core positioning phrase on the home page) appear in the visible body text.

Two map forms, so each page is checked fairly — do not punish a good page for the wrong rule:
- **`{ term, body? }`** — the term must appear in `<title>`, `<meta description>`, and the
  `<h1>` or intro. Use for a page that owns ONE brand/category phrase.
- **`{ title?, desc?, h1?, body? }`** — explicit per-surface clauses, for a page whose
  surfaces legitimately differ (a search-intent page may carry a comparison `<title>` but a
  category-naming `<h1>`). Each surface is a list of clauses that **all** must match (AND); a
  clause is either a **phrase** (required) or an **array of phrases** (any-one — an OR-group of
  acceptable alternatives). So
  `title: ['mobile app technology', ['React Native vs Flutter vs Native', 'RN vs Flutter']]`
  requires "mobile app technology" AND one of the two phrasings. `h1` clauses match the `<h1>`
  OR the intro paragraph; omitted surfaces are not checked.

The match is plain, case-insensitive **string containment** — deterministic,
offline, no new npm dependency. It protects the strategic spine; it is **not** a
keyword-density check. Do **not** add `keyword-extractor`, `seord`, or a density
target: density tests reward stuffing, fight tone and GEO readability, and produce
vague failures. A failure here reads cleanly — *"`/services` is missing its
positioning term «X» in `<title>`"* — and the fix is to say the thing, once, where
it belongs. Use the same term across the three surfaces; do not pad with synonyms.

The map starts **empty**, so the suite is green from commit 1. You populate it as
the positioning is worked out and pages are built.

**Coverage flag (warn-only).** The spec also *warns, without failing*, when a `PAGES`
route has no `POSITIONING` entry and isn't in `POSITIONING_EXEMPT` (the legal/utility
pages — privacy, imprint, 404 — that own no term). It is not an error: positioning is
opt-in and the suite stays green. But an un-positioned **content** page ships with no term
it owns — a lost opportunity — so the warning surfaces it (in the test output and the HTML
report) instead of letting it pass silently. Clear it by giving the page a term, or, for a
genuinely term-free page, add it to `POSITIONING_EXEMPT`.

## Boundaries (do not duplicate)

- **Quick fresh-eyes check of an existing site** → `website-positioning-check`
  (read-only diagnostic; come back here to rework the spine if it finds a problem).
- **The home page told as the customer's story** (one-liner, three-step plan, seven-section
  home page map) → `website-story` (optional; `new-website` offers it once after this
  skill; it reads this file and never edits it, and loses every conflict with it).
- **The tagline (the short line under the logo)** → `website-tagline` (optional; it reads
  this file, never edits it, and adds no claim this file lacks).
- **Tone of voice, EEAT, page copy** → `website-content-guide` (reads this file).
- **Keyword / SERP research** → `seo-audit`. Positioning leads; keywords follow and
  must not bend the spine into stuffing.
- **AI / answer-engine phrasing (GEO)** → `ai-seo`.
- **Schema, head metadata, boilerplate placement** → `website-seo-geo` (+ `schema-markup`).
- **Information architecture / URLs** → `site-architecture`.

## Done means

`POSITIONING.md` filled (all five components, a statement, boilerplate, the per-page
table), the `POSITIONING` map mirrored into `tests/positioning.spec.ts`, and the
positioning test green after every page is built (`npm test` runs
`positioning.spec.ts`).
