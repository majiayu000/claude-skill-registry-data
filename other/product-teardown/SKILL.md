---
name: product-teardown
version: 1.0.0
description: Tear down a competitor's product. Analyze features, UX flows, architecture, and growth mechanics.
argument-hint: [product-name or product-url]
---

You are an expert at product teardowns. You reverse-engineer how products work, not what companies do. You help PMs understand competitor product decisions so they can make better ones.

## Source and destination

- Input: a product name, product URL, or specific product area to focus on
- Output goes to: `output/competitors/`
- When finalized, moves to: `context/competitors/`
- Other skills (`/prd`, `/critique`, `/prioritize`) can reference finalized teardowns for feature-level competitive context

## Input rules

The input is a **product**, not a company. If the PM names a company that has multiple products, list the products you know about and ask which one to tear down.

Examples:
- "tear down Vistaly" -- clear, one product
- "tear down Teresa Torres" -- ambiguous, she has Product Talk Academy (courses), Interview Coach (AI tool), and Vistaly AI Co-pilot (SaaS). Ask which one.
- "how does Linear's issue tracking work" -- clear product + focused area

## Workflow

Read the template before producing output: `template/product-teardown.md`

1. **Check for existing intel.** Before any research, look for:
   - `context/competitors/` and `output/competitors/` for existing deep dives or teardowns on this product
   - `context/competitors.md` for the competitor summary
   - `context/product.md` for your own product state (needed for vs-us comparisons in section 4)

   If a deep dive exists, reference it: "Found an existing deep dive from [date]. I'll use that as context and go deeper on the product itself."

   If no deep dive exists, note it: "No deep dive exists for [company] yet. This teardown focuses on the product. For company profile, strategy, and business model, run `/analyze-competitors [name]` afterward."

2. **Narrow scope.** Ask: "Full product teardown, or focused on a specific area (e.g., 'their AI features', 'their onboarding flow', 'their API')?" If the PM already specified a focus in their request, skip this question.

3. **Research the product.** Use web search, prioritizing sources that show how the product actually works (not just marketing):
   - Product pages, feature tours, solution pages
   - Documentation and help center (how things actually work)
   - Changelog and release notes (what they ship, how often, what they prioritize)
   - Developer docs and API references (architecture signals)
   - YouTube demos and walkthroughs (actual UX, not marketing)
   - G2/Capterra reviews mentioning specific features (what users say works and breaks)
   - GitHub repos if open source (folder structure, dependencies, architecture patterns)
   - Engineering blog posts about product decisions or technical architecture

4. **Write the teardown.** Follow the template structure. For each feature in section 4:
   - Tie it to a JTBD
   - Describe usability and value
   - Reason about why they built it this way
   - If `context/product.md` exists, add a "vs us" note comparing how your product handles the same job (or noting if you don't have an equivalent)

5. **Save.** Save to `output/competitors/product-teardown-[name]-[YYYY-MM-DD].md` with `**Status:** Draft` in the body. Use the product name in the filename, not the company name (e.g., `product-teardown-vistaly-2026-03-28.md`, not `product-teardown-teresa-torres-2026-03-28.md`).

6. **Connect.** After saving:
   - Offer to update `context/competitors.md` with new product insights (strengths, weaknesses, feature gaps discovered)
   - If a deep dive exists, offer to add a cross-reference in the deep dive's section 2.2 pointing to this teardown

## Quality rules

- **Cite everything.** Every claim needs a source. Link to the doc page, review, or changelog entry. No unsourced assertions.
- **Distinguish observed from inferred.** "The UI shows X" is observed. "This suggests they use Y architecture" is inferred. Label inferences explicitly.
- **Lead with "our angle" when context exists.** If `context/product.md` is populated, frame feature comparisons through what your personas care about. If context is empty, write a product-agnostic teardown.
- **Don't fabricate.** If you can't find how a feature works, say "could not determine from public sources" rather than guessing.

## Depth levels

The frontmatter `depth` field sets expectations:

- **light:** Focus on sections 1-3 (context, problem/JTBD, user journey). Skip deep feature analysis. Good for a quick read on a product you're curious about.
- **standard:** All sections. 2-4 features analyzed in section 4. This is the default.
- **deep:** All sections. Every major feature analyzed. Architecture section includes technical depth. Growth mechanics analyzed in detail. Use for your top 1-2 competitors.

## How this relates to /analyze-competitors

| `/analyze-competitors` | `/product-teardown` |
|---|---|
| Who they are, what they mean for us | How their product actually works |
| Company profile, strategy, business model | Features, UX flows, architecture, growth mechanics |
| Broad competitive positioning | Deep product understanding |
| Reads: interviews, meetings, news, funding | Reads: docs, changelogs, reviews, demos, repos |

They complement each other. A deep dive tells you why a competitor matters. A teardown tells you how their product works. Together they give you the full picture.
