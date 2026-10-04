---
name: seo-glossary
description: This skill should be used when the user asks to "write an SEO article", "create a glossary post", "write a comparison guide", "write X vs Y article", "create educational content for SEO", "write a complete guide to X", or needs to create search-optimized educational content that balances SEO requirements with opinionated, engaging writing.
version: 1.0.0
---

# SEO Glossary Article Specialist

Create SEO-optimized educational content that ranks well while maintaining an opinionated, engaging voice. This style combines the structure needed for search visibility with the "Thoughts on Trends" pattern for developer audiences.

## 1. Core Philosophy

**Not neutral explainers—opinionated educators.**

Standard SEO glossary articles are dry, definition-focused, and interchangeable. This style differentiates by:

- **Reframing the question:** Don't just answer "What is X vs Y?" Answer "Why does this distinction matter, and when should you care?"
- **Taking a stance:** Provide a framework or mental model, not just facts
- **Acknowledging trade-offs:** Every choice has costs; help readers understand both directions of failure

## 2. Article Structure

### Opening (Hook)

- **Challenge conventional wisdom:** "Most explanations of X get stuck in definitions—technically accurate, practically useless."
- **State the uncomfortable truth:** Reframe the topic as a business/practical decision, not just a technical one
- **Preview the framework:** Tell readers what lens you'll use to analyze the topic

### Body Sections

Follow this pattern for each major section:

**H2 → Transition → H3 structure:**
- After each H2 heading, write 1-2 sentences framing the section's purpose
- Example: "The technical capabilities matter, but timing matters more. Most companies start with X alone—and that's correct. The question is recognizing when your business stage demands adding Y."

**H3 → Introduction → List structure:**
- Before bullet points, write a sentence explaining the core characteristic
- Example: "OLTP is the foundation of every data architecture. It handles the writes that power your application—every user action, every state change."

### Comparison Format

For Feishu/Notion compatibility, use bullet-based comparisons instead of markdown tables:

```markdown
**Dimension Name**
- Option A: Description
- Option B: Description
- Option C: Description
```

### Conclusion

- **Condense to essentials:** 50% shorter than typical conclusions
- **Three truths format:** Memorable, quotable takeaways
- **Reframe the question:** "Stop asking 'X or Y?' Ask: 'What stage is my business?'"

## 3. Voice & Tone

### Phrases to Use

- "Here's the uncomfortable truth..."
- "The reality is..."
- "Most companies get this wrong..."
- "The question isn't X—it's Y"
- "This isn't failure—it's maturity"

### Phrases to Avoid

- "In my experience..." (too soft)
- "You might consider..." (too hedging)
- "It depends..." without following up with a framework
- Generic definitions without business context

### Tone Characteristics

- **Confident, not arrogant:** Assert opinions but acknowledge complexity
- **Challenging, not condescending:** Push readers to think differently
- **Practical, not academic:** Focus on decisions, not theory
- **Balanced acknowledgment:** "This depends on X expertise and Y patterns"

## 4. SEO Requirements

### Metadata

```yaml
---
title: "Primary Keyword: Descriptive Subtitle (50-60 chars)"
description: "Compelling summary with primary keyword. Focus on the reframe, not just definitions. (150-160 chars)"
slug: primary-keyword-descriptive-slug
keywords: primary keyword, secondary keyword 1, secondary keyword 2
---
```

### Keyword Integration

- Primary keyword in H1, first paragraph, and 2-3 H2 headings
- Secondary keywords in H3 headings and body text
- Natural usage—never force keywords at the cost of readability

### Featured Snippet Optimization

- Use clear H2/H3 hierarchy for "What is X" queries
- Bullet-based comparisons for "X vs Y" queries
- Numbered lists for "How to" or "When to use" queries

## 5. Technical Content Balance

### Include

- **Code examples:** Show typical queries/usage for each option
- **Architecture diagrams:** ASCII art for compatibility
- **Quantified claims:** "10-50x reduction in I/O" not "significant improvement"

### Avoid

- Over-explaining basics the audience already knows
- Technical details that don't serve the decision framework
- Jargon without immediate clarification

## 6. Product Mentions (Non-markety Style)

When mentioning products (e.g., Apache Doris, ClickHouse):

- **Education first:** Explain the capability, then mention the product
- **Compare honestly:** Acknowledge where alternatives excel
- **Avoid superlatives:** "Ideal choice for X use case" not "the best database"
- **Remove if too promotional:** If a sentence sounds like marketing, cut it

## 7. Workflow

### Phase 1: Framework Design

1. Identify the conventional framing (what everyone says)
2. Define your reframe (the uncomfortable truth)
3. Create a decision framework (stages, symptoms, trade-offs)

### Phase 2: Structure

1. Outline H2 sections with transition sentences
2. Plan H3 subsections with introduction sentences
3. Identify where comparisons, code examples, and diagrams go

### Phase 3: Draft & Polish

1. Write with the opinionated voice throughout
2. Add SEO metadata
3. Condense conclusion to essentials
4. Convert tables to bullet format for platform compatibility

## 8. Example Article Structure

```
# X vs Y: A Complete Guide to [Decision Framework]

[Hook: Challenge conventional wisdom]
[Uncomfortable truth: Reframe as business decision]
[Preview: What this guide covers]

## What Is X?
[Transition sentence]
[Core explanation with code examples]

## What Is Y?
[Transition sentence]
[Core explanation with code examples]

## Key Differences Between X and Y
[Transition: Why these differences matter]
[Bullet-based comparison by dimension]
[Trade-off summary]

## X vs Y: When to Use Each
[Transition: Timing matters more than features]

### When to Use X
[Introduction sentence]
[Patterns that demand X]

### When to Use Y
[Introduction sentence]
[Patterns that demand Y]

## Common Use Cases
[Transition: Making differences concrete]

### X in Practice
[Introduction sentence]
[Real-world examples]

### Y in Practice
[Introduction sentence]
[Real-world examples]

## Can X and Y Work Together?
[Transition: Evolution, not competition]
[Integration patterns]

## Which Is Right for You?
[Reframe: Wrong question]
[Stage-based framework]
[Decision criteria]

## Conclusion
[Three truths]
[Reframed question]

## References
[Categorized links]
```

## 9. Reference Materials

For the original article demonstrating this style:
- **`references/oltp-vs-olap-example.md`** — Full example of SEO glossary style with all techniques applied
- **Published version:** [OLTP vs OLAP: A Complete Guide to Database Architecture](https://www.velodb.io/glossary/olap-vs-oltp)
