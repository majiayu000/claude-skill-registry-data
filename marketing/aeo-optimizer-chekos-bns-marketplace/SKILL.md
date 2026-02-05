---
name: aeo-optimizer
description: |
  Optimize content for AI search engines (ChatGPT, Perplexity, Google AI Overviews).
  Use when: (1) Auditing content for AI citability, (2) Writing content designed to be
  cited by AI assistants, (3) Analyzing why content isn't being cited, (4) Adapting
  existing SEO content for answer engines. Spanish-language technical content focus.
---

# AEO Optimizer

Optimize tacosdedatos content to be cited by AI search engines.

**Context**: `/agents/shared/tacosdedatos-growth-playbook.md` has current traffic data (ChatGPT: 7 visits, Perplexity: 3 visits — early but growing).

## Key Insight

AI assistants cite content that:
1. **Answers questions directly** in the first 2-3 sentences
2. **Uses structured formats** (numbered lists, tables, clear headers)
3. **Is recent** (93% of Perplexity citations are 2024-2025)
4. **Has topical authority** (multiple related articles on the same subject)

## Quick Audit Checklist

For any piece of content, check:

```
□ First paragraph directly answers the main question
□ Has numbered lists or bullet points for key information
□ Uses H2/H3 headers as natural questions
□ Includes a clear definition early ("X is...")
□ Has specific numbers, steps, or examples
□ Updated within last 12 months
□ Part of a topic cluster (linked related content)
```

## AEO-Optimized Structure

```markdown
# [Question as H1]

[Direct 2-3 sentence answer with key facts]

## [Supporting question as H2]

[Numbered list or table with specifics]

## [Another angle as H2]

[More detail, examples, code]
```

## Platform Differences

See `references/platform-behaviors.md` for how each AI handles citations differently:
- **ChatGPT**: Prefers authoritative, comprehensive sources
- **Perplexity**: Cites inline, loves recent listicles
- **Google AI Overviews**: Pulls from top 10 organic results

## Spanish Content Opportunity

Most AI assistants lack quality Spanish sources for technical topics. Being the definitive Spanish resource on a topic significantly increases citation likelihood.

High-opportunity topics for tacosdedatos:
- AI tool tutorials in Spanish
- Python/pandas guides in Spanish
- Data visualization techniques in Spanish
