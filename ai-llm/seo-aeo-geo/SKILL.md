---
name: "seo-aeo-geo"
description: "Optimize content and site structure for AI-driven search experiences including AI overviews, large language model citations, generative answer engines, and AI assistants. Use this skill whenever the user wants to optimize for AI search, get cited by language models, appear in AI overviews, build llms.txt, structure content for AI extraction, or future-proof their SEO for the shift from blue links to AI answers. Triggers on AEO, GEO, AI search, AI SEO, AI overview, generative search, LLM optimization, llms.txt, AI citation, ChatGPT search, Perplexity, Gemini, Claude search, AI assistant optimization, answer engine. Also triggers when the user expresses concern about AI eating their organic traffic or wants to understand how to remain visible as search shifts."
---

# AEO and GEO

Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO). Make content discoverable, extractable, and citable by AI search experiences.

This skill encodes principles. AI search products evolve fast. The principles age slower than the products.

---

## When to use

- Optimizing content for AI overviews and generative answer engines
- Building or updating llms.txt
- Structuring content so AI assistants can extract and cite it correctly
- Future-proofing a site as search shifts from blue links to AI answers
- Auditing whether existing content is AI-friendly
- Adding signals that help AI assistants identify the site as a trustworthy source

## When NOT to use

- Traditional on-page or technical SEO (use `seo-onpage` or `seo-technical`)
- Keyword research (use `seo-keyword`)
- Off-page authority and link building (use `seo-offpage`)

This skill stacks on top of those. Strong AEO/GEO requires strong fundamental SEO underneath.

---

## Required inputs

- The site or page to optimize
- The topic area or query types AI should cite the site for
- Access to inspect rendered HTML and structured data

---

## The framework: 5 layers

AI search visibility comes from five stacked layers. Each layer compounds.

### 1. Extractable content structure

AI systems extract facts and pull citations from content. Make extraction easy.

- **Direct answers.** Open major sections with a definitive 1 to 3 sentence answer to the question that section addresses. This improves reader clarity; extraction behavior varies by product and must not be assumed.
- **Question-headers.** Use H2s and H3s phrased as questions when natural. Mirrors how people prompt AI.
- **Atomic facts.** When stating a fact, state it once, clearly, with the supporting context next to it. AI struggles when claims are spread across paragraphs.
- **Tables and lists.** AI parses these reliably. Use them for comparisons, specs, steps, and data.
- **Definitions early.** When introducing a concept, define it inline. Do not assume the reader (or AI) saw a definition three pages ago.
- **Numbered steps.** For procedural content, number every step. Avoid prose disguised as instructions.

### 2. Citation worthiness

AI cites sources it considers authoritative. Earn that consideration.

- **Original data.** Surveys, studies, proprietary research, internal benchmarks. Primary sources make claims independently verifiable; provider citation preferences must be measured rather than assumed.
- **Specific numbers.** "Roughly 40 percent" beats "many." Specific stats with sources beat round-number generalizations.
- **Named experts.** Author bios with credentials, links to professional profiles, schema-marked-up Person entities.
- **Date stamps.** Publication date AND last-updated date, both visible AND in schema. Use honest dates to communicate freshness; do not invent a universal ranking weight.
- **Methodology disclosure.** When stating a finding, briefly note how it was reached. This lets readers and reviewers assess the evidence.
- **Citations of other sources.** Linking to authoritative sources you used builds reciprocal credibility.

### 3. Structured data depth

Structured data describes the page in a machine-readable form. Support and use vary by consumer; apply documented types that match visible content.

- **Schema.org types** appropriate to content (Article, FAQPage, HowTo, Recipe, Product, Organization, Person, LocalBusiness, etc.)
- **Required AND recommended properties** filled in (most sites only fill required, leaving signal on the table)
- **Person schema** for authors, with `sameAs` links to verifiable profiles
- **Organization schema** on the homepage with logo, contact, social links
- **FAQPage schema** for content with genuine question-answer pairs
- **HowTo schema** for procedural content
- **BreadcrumbList schema** site-wide
- Validates in Schema.org Validator AND Rich Results Test (some properties differ)

### 4. AI-readable accessibility

Beyond traditional SEO, AI tools need access patterns of their own.

- **Optional llms.txt for consumers that document support, not a universal search requirement.** A markdown file at `/llms.txt` describing the site's content, key URLs, and what topics the site covers. See [`references/llms-txt-guide.md`](references/llms-txt-guide.md).
- **llms-full.txt** (optional) - a content bundle for supporting consumers, only when publication is authorized; it is not a training permission or access-control mechanism.
- **Separate search and training controls.** Read [provider controls](references/search-provider-controls.md). Decide policy per provider and purpose from current official documentation; search visibility does not imply permission for training crawlers.
- **Clean HTML semantics.** Semantic tags (`article`, `section`, `nav`, `main`) help AI parse structure.
- **Avoid client-side-only rendering for critical content.** Many AI crawlers render less reliably than Googlebot.

### 5. Real-world entity signals

AI builds knowledge graphs and prefers entities with multiple consistent signals.

- **Wikipedia entry** if the brand or person qualifies for notability (do not force this; it requires genuine notability)
- **Wikidata entry** for the entity, with consistent properties
- **Consistent NAP** (Name, Address, Phone) across all citations
- **Brand mentions across multiple authoritative sources.** AI cross-references entity claims across the open web.
- **Social profile schema** linking owned profiles via `sameAs` properties
- **Reviews and reputation signals.** Aggregate ratings on Google Business, Trustpilot, industry-specific review sites where applicable

---

## Workflow

1. **Audit current state.** Run the 5-layer framework against the existing site. Score each.
2. **Identify the priority queries.** What questions should AI cite this site for? List 10 to 20.
3. **Test current AI visibility.** Query each of the major AI products (those relevant to the audience) with the priority questions. Note which sources they cite, or state the gap per the data-availability rule.
4. **Identify gaps.** Is the site cited? On which queries? Why does it lose to the cited sources?
5. **Layer-by-layer plan.**
   - Fix extractable structure on top 20 priority pages
   - Add citation-worthy signals (original data, expert authorship, methodology)
   - Deepen schema implementation
   - Build/update llms.txt only for a documented consumer or an explicit user request
   - Strengthen entity signals
6. **Implement and re-test.** AI products update frequently. Re-test priority queries quarterly.

---

## Failure patterns

- **Treating AEO/GEO as separate from SEO.** Strong fundamental SEO is a prerequisite. AI cites pages, not magic.
- **Stuffing FAQ schema on pages that have no genuine FAQs.** Do not manufacture FAQ content or imply undocumented penalties; follow each consumer’s current eligibility and content rules.
- **Hiding key content behind heavy JavaScript.** AI crawlers render less reliably. Server-render or pre-render critical content.
- **Optimizing for one AI product only.** Different products use different ranking and citation logic. Optimize for the principles, not for one product's quirks.
- **Ignoring entity strength.** Content alone, with no real-world entity signals, will not get cited reliably for branded or expertise-related queries.
- **Treating llms.txt as a magic bullet.** Its utility depends on the consumer; do not describe it as a universal ranking or citation signal.
- **Static optimization.** AI products evolve faster than search algorithms historically did. Re-audit at least quarterly.

---

## Output format

Default output is a markdown plan at `aeo-geo-strategy.md`. Structure:

1. Current AI visibility audit (which queries cite the site, which do not)
2. 5-layer scorecard
3. Priority queries (the 10 to 20 the site should be cited for)
4. Layer-by-layer remediation plan
5. Implementation roadmap
6. Re-test schedule (quarterly)

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/llms-txt-guide.md`](references/llms-txt-guide.md) - How to write a useful llms.txt, with examples.
- [`references/extraction-friendly-patterns.md`](references/extraction-friendly-patterns.md) - Content patterns that AI extracts cleanly, with before/after examples.

