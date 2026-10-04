---
name: question-interpretation
description: >
  Workflow for analyzing ambiguous data questions. Covers decomposing
  questions, identifying implicit assumptions and edge cases, verifying
  interpretations with SQL evidence, and guiding the team toward the
  correct interpretation.
---

# Question Interpretation Skill

## Mission

Analyze the user's question for ambiguity, implicit assumptions, and edge
cases. Use SQL to verify your interpretations against the actual data.
Produce an explicit, evidence-backed interpretation and flag when multiple
valid interpretations exist.

## Workflow

1. **Decompose the question** — identify:
   - The **metric** being asked about (revenue, count, rate, etc.)
   - The **time range** (explicit or implied by "current", "last month", etc.)
   - The **entity** (specific company, product, account, or "all")
   - The **filters** (explicit conditions and implicit assumptions)
   - The **comparison** (if any — MoM, YoY, vs. benchmark)
2. **Study the semantic model** — check if the metric maps to a known
   dimension/measure. Check `sample_values` to verify entity names and filter
   values actually exist in the data.
3. **Identify ambiguities** — common sources:
   - "Revenue" — gross or net? Booked or recognized?
   - "Last quarter" — calendar quarter or fiscal quarter?
   - "Active users" — by what definition? What activity counts?
   - Entity names — exact spelling? Case sensitivity? Partial matches?
   - Missing filters — should deleted/inactive records be excluded?
   - Entity identification — when a question names a specific entity,
     verify how it maps to the data. It could be an ID, a name pattern,
     a boolean flag, or a combination — do not assume without checking.
   - Aggregation granularity — what level should the query group by?
     The same question can yield different answers depending on whether
     you aggregate per entity, per entity-per-account, or globally.
   - Time window semantics — does "weekly" or "monthly" refer to fixed
     calendar periods or rolling/trailing windows? These require
     different SQL patterns.
   - Data volume assumptions — does the question assume a large
     population? The actual count may change the appropriate analysis
     approach entirely.
4. **Verify with SQL** — use `execute_sql` to resolve ambiguities with data:
   - Check what date ranges are available (MIN/MAX of date columns).
   - Check what values exist in key filter columns (e.g., DISTINCT values).
   - Check which table is appropriate when multiple candidates exist
     (compare row counts, column coverage).
   - Run a quick sanity query to estimate the expected answer magnitude.
   This evidence makes your interpretations defensible in discussion.
5. **Record your interpretation** — when ambiguity exists, include your
   recommended interpretation and the SQL evidence that supports it in
   your findings summary so the consumer of your work can audit your
   reasoning.
6. **Submit your findings** with your interpretation using the completion
   mechanism provided by your runtime.

## Interpretation Tips

- **Back claims with data.** When you recommend an interpretation, include
  the SQL evidence that supports it. Data-backed interpretations carry more
  weight than opinions.
- **Be concrete.** Don't just say "this is ambiguous" — state the specific
  interpretations, recommend one, and show the SQL evidence supporting it.
- **Verify with your own queries.** If you encounter a conflicting result
  or a suspect interpretation elsewhere, re-run the relevant query yourself
  instead of deferring. Your SQL evidence is what makes an interpretation
  defensible.
- **Treat custom_instructions as defaults, not rules.** The semantic model's
  `custom_instructions` describe typical usage. If the question requires a
  different grain or filter, override the default and document why.

## Findings Summary Format

Always include:
- **Question Interpretation** — your plain-language restatement of what the user is asking.
- **Key Entities and Filters** — the exact values to filter on.

Include when relevant:
- **Ambiguities Identified** — each ambiguity, possible interpretations, and
  recommended resolution with SQL evidence.
- **Verification Queries** — SQL you ran and results.
- **Edge Cases** — potential pitfalls (missing data, definitional issues).
- **Your Answer (optional)** — your best answer if you have one.
