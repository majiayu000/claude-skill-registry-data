---
name: web-research-corpus
description: >
  Web research methodology adapted for static document corpus retrieval.
  Covers iterative search loop with corpus search and full-document fetch,
  strict completion criteria, information redundancy principle, and
  automatic source quality scoring.
---

# Corpus Research Skill

## Mission

Search the document corpus thoroughly to gather reliable, factual, and
verifiable information that directly addresses the question. Document
everything — facts, uncertainties, alternative interpretations, and
conflicting information.

# Corpus Research Guidance

For research questions that require finding information in the document corpus,
search thoroughly and cross-verify from multiple sources.

- Use `web_search` to find relevant text chunks from the corpus.
- Use `web_fetch` with a descriptive query to retrieve the full document text
  when you need more context than search snippets provide. The query should
  describe what you want to read — it is NOT URL-based.
- Start with broad queries, then narrow down based on initial results.
- Cross-check key facts across at least 2 independent document chunks.
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
1. Use comprehensive `web_search` queries to find relevant text chunks
   from the document corpus.
2. Use `web_fetch` with a descriptive query to retrieve the full document
   text when you need more context than the search snippets provide.
   The query should describe what you want to read — it searches the
   document corpus independently (it is NOT URL-based).

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
- Search for alternative document chunks to cross-verify previous findings.
- Resolve any contradictions between sources.
- Find ALL plausible answers — don't stop at the first answer.

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

When you call `web_search`, the system may or may not **automatically score**
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
  in the corpus — **cross-verify** when appropriate.
- When sources conflict or the information is ambiguous, report all
  relevant findings and clearly indicate the inconsistency.
- Favor quoting or excerpting the **original source text** rather than
  paraphrasing or interpreting it.

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

When initial searches return poor results or fail to find the answer,
**systematically broaden your search angles**:

1. **Vary terminology** — Try synonyms, alternative spellings, and
   related terms for the same concept.
2. **Try partial queries** — Break a complex question into smaller,
   more focused queries targeting individual facts.
3. **Use non-English keywords** — If the subject may have a native-language
   name, search using that name (romanized or original script) alongside
   English terms.
4. **Use web_fetch for deeper reads** — When search snippets are
   insufficient, use `web_fetch` with a targeted query to retrieve the
   full document text for deeper investigation.
