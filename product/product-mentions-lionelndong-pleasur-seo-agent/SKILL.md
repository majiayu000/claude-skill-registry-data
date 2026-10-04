---
name: product-mentions
description: Annotate the outline with where to mention specific brand products. Designed-in at outline time so product callouts feel natural in the draft, not bolted on.
allowed-tools: Read, Write, Edit
---

# Product Mentions Skill

The brand writes content because the brand has a product to demonstrate. This skill plans where each product fits **before drafting** — bolting product mentions on during drafting reliably produces awkward results.

## Input

For slug `{slug}`:
- `content-pipeline/3-outlines/{slug}.md` (the outline to annotate)
- `brand-config.md` (the product list with use cases)
- `content-pipeline/2-reference/{slug}.md` (existing product use cases)

## Process

0. **Constraint reconciliation pass (run BEFORE annotating).** The outline can contradict itself — a section can include a `coming-soon` product mention while a structural-concerns note at the bottom of the same outline restricts that product to a different section. Catch this before the draft sees it.

   1. Read the outline end-to-end.
   2. For each `coming-soon` or `roadmap` product mentioned in `brand-config.md`, search the outline for every reference.
   3. Cross-check those references against:
      - The outline's own structural-concerns notes (typically near the end of the file)
      - `brand-config.md`'s rule that coming-soon products only appear in roadmap / preview / "where the category goes" sections
      - The article context in `0-context/{slug}.md` (if it explicitly authorizes a launch post)
   4. If a reference sits outside the permitted slot, **delete that reference from the outline** before the rest of this skill runs. The outline file you save in step 7 is the corrected version.
   5. Log every deletion at the top of the saved annotated file in a `## Pre-flight reconciliation` block:
      ```
      ## Pre-flight reconciliation

      The original outline had {N} contradictions about coming-soon products. They were resolved before annotation:
      - H2 #X line Y: removed mention of "{product}" because the outline's own constraints (line Z) restrict it to H2 #N. Reason: {brand-config.md L36 forbids coming-soon products in evergreen sections / outline structural-concerns line N}.
      ```
   6. If no contradictions, write `## Pre-flight reconciliation\n\nNo contradictions found.` and continue.

   This pass exists because the previous pipeline run shipped a draft that violated coming-soon rules; the gate caught it but only after a full /draft run. Catching it here costs one careful read and saves an iteration loop.

1. **Read the brand product catalog** from `brand-config.md`. For each product, note its top use cases AND its `status` field.
   - **Only `live` products are eligible for normal article mentions.** Coming-soon and roadmap products must NOT be inserted into evergreen content (they'll mislead readers and require article updates the moment the roadmap shifts).
   - Exception: if `0-context/{slug}.md` explicitly says the article is a launch / preview / roadmap post for a coming-soon product, then mentions of that specific product are permitted.
2. **Read the outline** carefully — you're looking for natural fits, not opportunities to shoehorn.
3. **For each H2 in the outline, ask:**
   - Is there a product that genuinely solves or demonstrates what this section discusses?
   - Would a competent reader, reading the brand's article on this topic, expect to see the brand's tool used here?
   - If yes → annotate. If forced → leave alone.
4. **Annotate naturally — three flavors:**
   - **Walkthrough** — "Use ProductA to do X. Show 1–2 screenshots." Visuals here should be `{type: screenshot, target: <product-slug>, what: <UI element>}` per `templates/visual-types.md`.
   - **Inline mention** — "Mention ProductA when explaining concept Y."
   - **Tip box** — "Pro tip: ProductA's feature Z saves you from doing this manually."

When a walkthrough adds visuals, **upgrade the section's `Visual:` field** to typed form (e.g. swap a generic `screenshot` to `{type: screenshot, target: create, what: voice profile selector with audition button}`). Don't add new Visual entries — refine the existing one, since a section should have at most one anchor visual.
5. **Cross-reference brand-reference** — if the brand has existing product walkthroughs for related concepts, link them so the new article doesn't re-explain product workflows the existing article already covers.
6. **Don't over-annotate.** Aim for product mentions in 3–5 sections of a 6-section article — not every section.
7. **Save annotated outline** to `content-pipeline/4-outlines-annotated/{slug}.md`. Preserve the original outline structure; add a `**Product mentions:**` line after each affected section's other fields.

## Output

`content-pipeline/4-outlines-annotated/{slug}.md`

The original outline plus product-mention annotations. Same structure, more content.

## Quality checklist

- [ ] No section forced to mention a product that doesn't naturally fit
- [ ] At least 3 sections have meaningful product annotations (if the brand has products)
- [ ] Annotations specify HOW to mention (walkthrough / inline / tip box) — not just "mention ProductA"
- [ ] Existing product walkthroughs from `2-reference/` are linked, not re-explained
- [ ] Product names match exactly what `brand-config.md` says (no paraphrasing)
- [ ] **No `coming-soon` or `roadmap` products mentioned** unless the article context explicitly authorizes a launch / preview post

## When NOT to add a product mention

- The section is foundational ("What is X") — keep it product-free; reader hasn't earned the pitch yet
- The product solves a different problem than the section discusses
- A product mention would interrupt the argument
- The mention would force a CTA where prose is more useful

A good test: imagine a competent reader who's never heard of the brand. Would they read the section and think "they're just trying to sell me something"? If yes, drop the mention.

## Example annotation

For a section on "How to find keyword cannibalization on your site":

```
## How to find keyword cannibalization on your site

- **BLUF:** A `site:` search and a quick rank-checker tell you which pages are competing for the same query.
- **Key points:** site: operator method; rank-tracker method; manual SERP inspection
- **Evidence:** screenshot of overlapping rankings
- **Visual:** {type: screenshot, target: cannibalization-report, what: filled report showing overlapping rankings, annotate: highlight the overlap row}
- **Product mentions:** Walkthrough — Use ProductA's "Cannibalization Report" to surface overlapping rankings in one view. Link to the existing ProductA tutorial from `2-reference/` rather than re-explaining setup.
```
