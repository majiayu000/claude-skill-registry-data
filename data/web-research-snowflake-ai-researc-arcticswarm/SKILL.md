---
name: web-research
description: >
  Web research methodology with iterative search loop, strict completion
  criteria, information redundancy principle, and automatic source quality
  scoring. Covers search strategy, source evaluation, cross-verification,
  and handling conflicting information.
---

# Web Research Skill

## Mission

Search the web thoroughly to gather reliable, factual, and verifiable
information that directly addresses the question. Document everything —
facts, uncertainties, alternative interpretations, and conflicting
information.

# Web Research Guidance

For research questions that require external information, search the web
thoroughly and cross-verify from multiple sources.

- Use `web_search` to find relevant URLs, then `web_fetch` to read full page content.
- Use `pdf_read` for academic papers, reports, and other PDF documents.
- Start with broad queries, then narrow down based on initial results.
- Prefer primary sources (official sites, papers, databases) over secondary summaries.
- Cross-check key facts across at least 2 independent sources.
- Include source URLs for every factual claim.
- If sources conflict, note the discrepancy and explain which you trust more and why.

## Core Principles

- **Comprehensive Coverage**: All aspects of the question must be addressed
  from multiple perspectives (mainstream + alternative viewpoints).
- **Depth Over Breadth**: Reject superficial data; require detailed data
  points and multi-source verification.
- **Information Redundancy**: Pursue information redundancy — avoid
  "minimum sufficient" data. When accuracy matters, more data is always
  better than less. **Default to continuing research when in doubt.**

## Iterative Research Workflow

Execute research in **iterative rounds**. Each round follows:
Search → Assess → Decide (continue or stop).

### Round 1: Broad Discovery
1. Use comprehensive `web_search` queries to understand the landscape.
2. Use `web_fetch` to read full content from the most relevant URLs.
   Do not rely solely on search snippets.
3. Use `pdf_read` for academic papers, reports, or PDF documents.

### After Each Round: Self-Assessment
Pause and explicitly evaluate what you have:
- What specific data points have I found?
- What dimensions of the question remain unanswered?
- Are my sources reliable and up-to-date?
- Do I have multiple sources confirming the same facts?
- Are there contradictions or gaps I need to resolve?

Apply the **Completion Criteria** below to decide whether to continue.

### Round 2+: Targeted Gap-Filling
- Use specific, targeted queries to fill gaps identified in the assessment.
- Search for alternative sources to cross-verify previous findings.
- Resolve any contradictions between sources.
- Find ALL plausible answers — don't stop at the first answer.
- If results are only from mainstream/Western sources, apply **Search
  Diversity** strategies below (niche platforms, non-English terms, forums).

## Completion Criteria (Strict)

### STOP searching — requires ALL conditions met:
- You have covered every dimension of the question.
- Sources are reliable and up-to-date.
- Zero information gaps or unresolved contradictions.
- You have 3+ independent sources providing consistent information.
- **80% certainty still requires continuation — default to keep searching
  when in doubt.**

### CONTINUE searching (default state) — if ANY condition is true:
- Any dimension of the question remains unanswered.
- Sources are outdated or questionable.
- Missing critical data points.
- Lack of cross-verification from independent sources.
- Any unresolved contradiction between sources.

## Source Quality Scores (Optional)

When you call `web_search` or `web_fetch`, the system may or may not **automatically score**
each result for relevance, answerability, authority, and data_density (each 0-10).
You may see a `[Source Quality: ...]` annotation on results. If provided:

- **High composite (25+/40)**: Reliable primary evidence. Cite these.
- **Medium composite (15-24/40)**: Supporting evidence. Cross-reference.
- **Low composite (<15/40)**: Weak source. Search for better alternatives.

## Source Evaluation

Critically evaluate the trustworthiness of every piece of information
you retrieve:
- If a source's reliability is uncertain, explicitly flag it.
- Do **not** assume information is credible merely because it appears
  online — **cross-verify** when appropriate.
- When sources conflict or the information is ambiguous, report all
  relevant findings and clearly indicate the inconsistency.
- Favor quoting or excerpting the **original source text** rather than
  paraphrasing or interpreting it, and include the URL.

## Calculator Usage

- **NEVER calculate mentally** — use the `calculator` tool for ALL numeric
  operations including arithmetic, percentages, counting, rounding, and
  unit conversions.
- For counting items: list items explicitly with numbering, then use
  `calculator` to verify the total.
- For rounding: use `ceil()` for "round up", `floor()` for "round down",
  `round()` for standard rounding.

## Research Rigor

1. **Cross-verify claims** — compare statements from multiple sources to
   identify commonalities and deviations. Highlight any discrepancies.
2. **For lists/enumeration** — if the question asks "all X that meet Y",
   search multiple sources and explicitly verify completeness.
3. **For superlatives** ("oldest", "newest", "first", "last") — verify
   with multiple different search queries. Don't accept first result as
   definitive.
4. **Terminology precision** — use the MOST COMMON EVERYDAY term. Copy
   names and terms EXACTLY from sources with all qualifiers.
5. **Be decisive** — present findings confidently if sources are credible.
   Only say "unable to determine" after exhaustive search finds nothing.
6. **Resist fame bias** — questions are designed so that the
   obvious/famous answer is usually WRONG. If your initial research points
   to a very well-known entity, invest extra effort searching for obscure
   alternatives that match ALL constraints. The correct answer is typically
   someone/something that requires deep searching to find.

## Search Diversity

When initial searches return only mainstream/Western results, or fail to
find the answer, **systematically broaden your search angles**:

1. **Vary cultural and regional context** — If the topic could involve
   non-Western entities, add region-specific terms (e.g. "K-drama",
   "Bollywood", "J-pop", country names, city names). Don't assume the
   answer is from the US/UK/Europe.
2. **Try niche platforms by name** — Search for the topic on specific
   platforms: "reddit.com", "quora.com", "Bandcamp", "SoundCloud",
   "Discogs", "RateYourMusic", "MusicBrainz", or domain-specific databases.
3. **Use non-English keywords** — If the subject may have a native-language
   name, search using that name (romanized or original script) alongside
   English terms.
4. **Search social media bios** — Combine the entity name with keywords like
   "bio", "about", "profile", "interview", "born in", "hometown" to surface
   personal details from social platforms.
5. **Try forum and community sources** — Reddit threads, fan wikis, Fandom
   pages, and niche community forums often have information that mainstream
   sources miss.
6. **Expand beyond the obvious category** — If searching for a musician, don't
   only search music databases — try general biographical sources, news
   archives, university alumni pages, and local press.
