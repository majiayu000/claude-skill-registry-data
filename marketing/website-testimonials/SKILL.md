---
name: website-testimonials
description: >
  Encode customer / attendee testimonials as proper schema.org `Review` JSON-LD
  AND render the "What people say" UI from ONE typed source of truth
  (`src/data/testimonials.ts`). Individual Review nodes only — author + 5/5
  reviewRating + reviewBody + inLanguage + itemReviewed pointing at the SPECIFIC
  thing reviewed (Event / Product / Service), never a fabricated org-wide
  AggregateRating. Use when adding quotes, testimonials, social proof, ratings,
  or star reviews to a site built with the new-website kit (pipeline step 5,
  alongside `website-seo-geo`). Delegates other schema types to `schema-markup`.
  Trigger phrases: "add testimonials", "customer quotes", "attendee feedback",
  "review schema", "star ratings", "social proof section", "encode the quotes",
  "schema.org Review", "what people say section".
---

# Website Testimonials & Review Schema

Turn real quotes into (1) a UI section and (2) valid `Review` structured data,
both from **one typed data file** so the visible card and the JSON-LD can never
drift. This skill owns the testimonial pattern; it hands generic schema work
(Product, FAQ, Breadcrumb, Article…) to `schema-markup`.

## Read this first — what schema can and can't buy you

- **Google does NOT show ⭐ rich-results for self-hosted reviews about your own
  `Organization` / `LocalBusiness`.** It treats them as *self-serving* and may
  ignore — or, for a fabricated `AggregateRating`, penalise — them. So the value
  here is **truthful semantic markup + GEO** (LLMs / AI answer engines citing
  your social proof), not blue-link stars. Set expectations honestly (Rule 12).
- **`itemReviewed` is the specific thing the person reviewed** — the `Event`
  (talk/workshop), `Product`, `Service`, `Course` — not a blanket org rating.
  This keeps the markup accurate and is what review-snippet-eligible types want.
- **Individual `Review` nodes only by default. No `AggregateRating`** unless the
  reviewed item is a genuinely rich-results-eligible type (e.g. `Product`) AND
  the rating reflects *all* real ratings. Few hand-picked 5-stars + an aggregate
  reads as spam.

## Accuracy rules (non-negotiable)

- **Quotes are verbatim.** Never invent, embellish, or "tidy" a quote or a name.
- **Keep the original language.** A quote written in another language stays in
  that language (e.g. a German quote on an English page) — translating a
  testimonial misrepresents it. Set `lang` on the element AND `inLanguage` on the
  Review so screen readers + parsers get it right.
- **Real ratings only.** `ratingValue` is what the person actually gave.

## Sourcing quotes (where they come from)

Testimonials come from wherever real feedback lives: post-purchase emails,
post-event surveys, support tickets, sales calls, or review sites (G2,
Trustpilot, app stores). Most sources are **private to you, with no public feed
or API** to pull from, so the workflow is **manual curation** — which is also
better editorially, since you pick the strongest, on-message quotes:

1. Open the source and copy the best **verbatim** quote + the rating + the
   person's name/affiliation.
2. Add one entry to `src/data/testimonials.ts` (set `lang`; map `itemName`/`itemUrl`
   to the specific item reviewed — the product, service, or event). No sync script
   is possible for most sources — don't build one.
3. **Get consent for named quotes before they go live** — see *Consent &
   shipping* below.

> Example (event sites): **Luma** keeps ratings organizer-private in *Manage
> Event → Insights*, exportable only as CSV; its per-response "share card" is a
> one-off image, not a live source — so you transcribe by hand. Expect the same
> of most platforms.

## Consent & shipping named quotes

A person left feedback for one purpose, not blanket permission to be quoted **by
name on your marketing site**. Treat consent as a publish gate, applied per person:

1. **Ask before production.** "OK to feature this quote, with your name and
   affiliation, on our site?" Anonymous/handle-only quotes are lower-risk — but
   still ask if the wording itself is identifying. Keeps you clean on GDPR/consent.
2. **Ship to PREVIEW first, not prod.** Put the section on a preview deploy (a
   branch build, off the production branch) so the team can review wording and
   layout while consent is pending. Keep testimonials **off production** until approved.
3. **Promote per person — ship only the approved subset.** If two of three
   consent, the live `TESTIMONIALS` array carries those two; the third stays out.
4. **Withhold, don't delete.** Keep an unconsented quote out of the array but
   leave a `// NOTE:` comment (the verbatim text also survives in git history), so
   re-adding on approval is a one-line edit.

Caveat: a static preview is usually **not auto-noindexed**, and a `*.pages.dev`
URL is public — so a named, unconsented quote sitting on a preview is still
exposure. Keep previews unlinked and short-lived (or add a branch-only `noindex`);
the real guarantee is keeping it **off production** until consent lands.

## The data model — one source of truth

`src/data/testimonials.ts` exports the typed list **and** the schema builder, so
a page imports both and nothing is duplicated:

```ts
import { SITE } from '../config';

export interface Testimonial {
  author: string;        // name or handle, verbatim
  org?: string;          // affiliation, shown after the name
  rating: number;        // 1–5, as actually given
  quote: string;         // verbatim
  lang: string;          // BCP-47 tag, e.g. 'en' / 'de' → `lang` attr + inLanguage
  itemName: string;      // the thing reviewed → itemReviewed.name
  itemUrl: string;       // canonical URL of that item (absolute)
  itemType?: string;     // schema.org type of the reviewed thing; default 'Event'
}

// Only consent-approved entries ship here; withhold the rest with a // NOTE.
export const TESTIMONIALS: Testimonial[] = [ /* … */ ];

// Individual Review nodes — no self-serving AggregateRating.
export function reviewSchemas(): Record<string, unknown>[] {
  return TESTIMONIALS.map((t) => ({
    '@context': 'https://schema.org',
    '@type': 'Review',
    author: { '@type': 'Person', name: t.author },
    reviewRating: { '@type': 'Rating', ratingValue: t.rating, bestRating: 5, worstRating: 1 },
    reviewBody: t.quote,
    inLanguage: t.lang,
    itemReviewed: { '@type': t.itemType ?? 'Event', name: t.itemName, url: t.itemUrl },
  }));
}
```

## Wiring it in (Astro / new-website kit)

1. **Schema** — pass the builder to `Base`'s `schemas` prop; the Base layout
   already serialises each entry to `<script type="application/ld+json">`:
   ```astro
   ---
   import { TESTIMONIALS, reviewSchemas } from '../data/testimonials';
   ---
   <Base titleExact="…" description="…" schemas={reviewSchemas()}>
   ```
   (Do NOT hand-write JSON-LD in the page — go through `schemas` so it stays in
   sync with the data file and Base's other schema nodes.)
2. **UI** — render cards from the same `TESTIMONIALS` array. Stars are decorative
   (`aria-label="Rated 5 out of 5"`, the glyphs themselves hidden from the name);
   foreign-language quotes get `lang={t.lang}` so AT pronounces them correctly.
3. **Theme** — reuse the site's tokens (`--dark-card`, `--text`, `--text-muted`,
   `--primary-light`); a gold star (`#F5A623`) clears AA on the dark card.

## Done means

- `npm test` green — `a11y.spec.ts` (star contrast + lang attrs), `tone`, `seo`.
- JSON-LD parses and passes the schema.org validator / Google Rich Results Test
  with **no errors**; each `Review` has `author`, `reviewRating` (with
  `bestRating`/`worstRating`), `reviewBody`, `inLanguage`, and an `itemReviewed`
  with a real `name` + absolute `url`.
- The rendered card text equals the `reviewBody` (same source — verify one).
- No `AggregateRating` unless justified per the rules above.
- Every NAMED quote on **production** has consent; un-approved ones are withheld
  (with a `// NOTE:`), and anything pending consent shipped to **preview only**.
