---
name: competitive-research
description: Produce a sourced competitive matrix for a focused research question
argument-hint: "[research topic or path to a research-prompt file]"
---

# Competitive Research

You help produce a sourced competitive matrix for a focused research question. The output is a markdown table plus sourced observations, landed in `research/`.

## Input

The user provides via `$ARGUMENTS`:
- A short research topic (e.g., "how competitors handle first-time user onboarding"), OR
- A path to a research-prompt file (e.g., `samples/sample-competitor-prompt.md`)

## Workflow

### 1. Read the prompt

If `$ARGUMENTS` is a file path, read it. Otherwise use the prompt directly.

**Extract (or ask in one round)**:
- **Research topic** - the question.
- **Scope** - which competitors (direct / adjacent / aspirational), any exclusions.
- **Questions** - 3-7 specific things you want answered.
- **Deliverable format** - matrix (rows = products, columns = questions) by default.
- **Timeline and non-goals**.

If any of these are missing, ask the user in ONE `AskUserQuestion` round. Skip any that are clear.

### 2. Pick the competitor set

If the user provided competitors, use them. Otherwise suggest a set and confirm:

- **Direct**: 2-3 products in the same pricing tier and feature surface as your own (list your company's known competitors from `CLAUDE.md` or ask).
- **Adjacent / aspirational**: 1-2 products in related spaces known for excellent practice in the research topic.
- **Exclude**: tools clearly out of scope.

Confirm the list with the user before proceeding.

### 3. Gather observations (sourced)

For each product, for each research question, gather observations. Use available tools:

- **WebFetch / WebSearch** for public product docs, blog posts, marketing pages, changelog posts, and product-hunt-style coverage.
- **Any documentation MCP** your environment has configured (check the `MCP Servers Available` section of `CLAUDE.md`).
- **Internal research notes** in `Loose Notes/Work/` that mention the competitor by name.

**Rules for observations**:
- **Sourced**: every observation has a URL or an internal note reference. No "I think they probably...".
- **Observed vs. inferred**: mark each cell as `observed:` (you can point to a specific page/screenshot) or `inferred:` (your reasoning based on other evidence).
- **Date-stamped**: competitive landscapes move fast. Note the date of the source when it's older than 6 months.

### 4. Build the matrix

Produce a markdown table:

| Product | Q1 | Q2 | Q3 | ... |
|---------|----|----|----|-----|
| Competitor A | observed: [fact] - [link] | inferred: [reasoning] | ... | ... |
| Competitor B | ... | ... | ... | ... |

Cells can be long. Keep them scannable but informative.

### 5. Summarize the landscape

Below the matrix, write a 3-5 paragraph synthesis:

- **Common patterns**: what do all / most of the competitors do similarly?
- **Divergences**: where do they differ meaningfully, and why?
- **Outliers**: any surprising approaches worth investigating further.
- **Implications for us**: how this should inform our decision (without prescribing a specific solution yet).

### 6. Note methodology and limits

A short section at the end:

- **Sources consulted**: docs, blog posts, pricing pages, external analyses.
- **Gaps**: what you couldn't find out (and would need a customer conversation or a demo account to verify).
- **Confidence**: where you're confident in observations vs. where you're inferring.

### 7. File location and naming

- **Folder**: `research/`. Create if it doesn't exist.
- **Filename**: `YYYY-MM-DD - Competitive - [Topic slug].md`. Example: `2026-04-20 - Competitive - Onboarding UX.md`.
- **Frontmatter**: `tags: Research, Competitive`, `created: YYYY-MM-DD`.

### 8. Link the research

- **Daily journal**: under `## Notes`.
- **Related epic** (if any): add a link in that epic's `## Breakdown > Explore` section.

### 9. Output summary

```
✅ Research: [[YYYY-MM-DD - Competitive - Topic]]
✅ Linked in today's journal

Products compared: [N]
Questions answered: [N]
Sources cited: [N]
Gaps flagged: [N]

💡 Key pattern: [One-line top insight]

Next step: run `/opportunity-solution-tree` to convert insights into opportunities.
```

## Notes

- **Sourced over speculative.** If you can't find evidence, say so.
- **A matrix is a structure, not a verdict.** Don't prescribe "we should do X because Competitor Y does it."
- **Competitive research ages fast.** Add the source date for anything older than 6 months. A year-old blog post about a product's onboarding is probably wrong now.
- **The Extended Opportunity Solution Tree framework** pairs well with this - use `/opportunity-solution-tree` next to turn patterns into opportunity hypotheses.
