---
name: publishing-optimized-content
version: "1.0.1"
description: >
  Runs SEO optimization at two stages of FlashFusion content production: before writing (brief + keyword targeting) and before publishing (on-page audit + metadata + schema). Chains searchfit-seo plugin skills at the right moments so SEO happens during content creation, not as an afterthought or separate pass.

  Activate when the user mentions: ready to publish, SEO check this, finishing this piece, optimize this before publishing, write a content brief, I'm about to write a post about X, pre-publish check, meta description, title tag, on-page SEO, add schema, internal links, content brief for, or any content piece transitioning from planning to writing, or writing to publishing.
---

# Content SEO Publisher

Ensures SEO happens at the right moments — not as a separate task you remember three days after publishing.

**Two modes:**
- **PRE-WRITE** — runs before drafting. Sets keyword target, structure, and gaps to cover.
- **PRE-PUBLISH** — runs on a finished draft. Audits all on-page elements before going live.

Load `references/ff-seo-context.md` before either mode.

---

## DEPENDENCY_DECLARATION

| Dependency | Type | Required for |
|---|---|---|
| `searchfit-seo:content-brief` | Chained plugin skill | PRE-WRITE Step 2 |
| `searchfit-seo:on-page-seo` | Chained plugin skill | PRE-PUBLISH Step 1 |
| `searchfit-seo:schema-markup` | Chained plugin skill | PRE-PUBLISH Step 2 |
| `references/ff-seo-context.md` | Reference file | Both modes |

**FAIL_IF:** `searchfit-seo:content-brief` is not loaded → do not call the plugin. Instead, run the content brief steps manually using the PRE-WRITE section below as a checklist. Output the brief as a structured document covering: recommended H1, recommended H2 structure, 4–6 semantic keywords, word count target, and angle recommendation. Note in the output: `[Manual brief — searchfit-seo:content-brief not available]`.

---

## Mode Detection

| Signal | Mode |
|---|---|
| "I'm about to write about X" / "write a brief for" / "what should this post cover" / "starting a new post" | PRE-WRITE |
| "ready to publish" / "SEO check this" / "finished draft" / "optimize this" / "pre-publish" | PRE-PUBLISH |
| Unclear | Ask one question: "Is this before writing or before publishing?" |

---

## PRE-WRITE Mode

### Step 1: Confirm keyword target

Check if the topic has an assigned keyword from the quarterly content plan (`researching-content-opportunities` output stored in `FlashFusion/Content/SEO/`).

- Assigned keyword found → use it
- No assignment → identify the best primary keyword: highest-volume, sub-KD-40 term that matches informational or commercial-investigation intent for this topic

### Step 2: Run content brief

Call `searchfit-seo:content-brief` with:
- Target keyword
- FlashFusion context (audience, tone, content pillar — from `references/ff-seo-context.md`)
- 2–3 top-ranking competitor URLs for this keyword (pull from Ahrefs SERP)

Output includes: recommended H1, recommended H2 structure, 4–6 semantic keywords to weave in, word count target, and a one-sentence angle recommendation that differentiates from what's already ranking.

### Step 3: Internal link planning

Before writing, identify 2–3 existing FlashFusion pages that should link to or from this piece. Note them in the brief now — retrofitting internal links after publishing is consistently skipped.

### Deliver

Present the brief as a single structured document ready to write from. Do not start the draft — that's the user's job.

---

## PRE-PUBLISH Mode

### Step 1: On-page audit

Run `searchfit-seo:on-page-seo` on the draft. Verify each element:

| Element | Requirement |
|---|---|
| Title tag | 50–60 characters · primary keyword near the front |
| Meta description | 150–160 characters · includes keyword · has a reason to click |
| H1 | Present · matches or closely mirrors title tag · contains keyword |
| H2s | At least 2 · include semantic keywords from the brief |
| URL slug | Short · keyword included · no stop words (the, a, in, for, with) |
| First 100 words | Primary keyword appears naturally in the opening |
| Image alt text | All images have descriptive alt text · keyword where natural |
| Internal links | Minimum 2 links to other FlashFusion pages |
| External links | At least 1 link to a credible external source · opens in new tab |
| Word count | Meets target from content brief · not padded |

Flag each failing element: `[FIX BEFORE PUBLISH — element name]`

Do not present a publish-ready summary until all flags are resolved.

### Step 2: Schema markup

Run `searchfit-seo:schema-markup` for the appropriate type:

| Content type | Schema |
|---|---|
| Blog post, tutorial, opinion | `Article` |
| How-to guide with steps | `HowTo` |
| Tool or product comparison | `Article` + `ItemList` |
| FAQ section present | `FAQPage` (for FAQ section only) |
| Workshop or event | `Event` |

Output the JSON-LD block. It goes in the `<head>` of the published page, not inline in the body.

### Step 3: Pre-publish checklist

- [ ] All on-page elements pass (Step 1)
- [ ] Schema block generated (Step 2)
- [ ] Canonical URL set (no duplicate indexing risk)
- [ ] Open Graph title, description, and image set
- [ ] Publishing to `flashfusion.co/blog` (not Substack as primary) and URL submitted to Google Search Console

---

## FlashFusion Context Block

Inject this into every `searchfit-seo:*` call:

```
Brand: FlashFusion — AI consulting and workflow automation
Audience: AI practitioners, consultants, IT professionals
Tone: Direct, specific, no filler. Technical when appropriate. First-person where natural.
Content pillars: AI agents, workflow automation, AI enablement, tool consolidation, consulting operations
Domain: flashfusion.co
Primary content hub: flashfusion.co/blog
Newsletter: Substack (syndication only, not primary SEO surface)
Keyword difficulty target: under 40
```

---

## Anti-Patterns

- **Don't skip PRE-WRITE mode.** Writing without a brief and then trying to optimize the resulting post is consistently worse than brief-first. Structure matters before the first sentence.
- **Don't publish on Substack as the primary surface.** Google indexes Substack poorly relative to a self-hosted blog. Publish on `flashfusion.co/blog` first, then syndicate.
- **Don't treat keyword density as a ceiling.** The checklist sets a floor (keyword appears in opening, H1, at least one H2). Going beyond that to stuff keywords degrades the content.
- **Don't skip schema.** It's a five-minute step with compounding value. Rich results in Google Search come from schema. Always generate it.
- **Don't publish without the internal links.** They're the most skipped step and also among the highest-ROI. Two minimum, planned during PRE-WRITE.
