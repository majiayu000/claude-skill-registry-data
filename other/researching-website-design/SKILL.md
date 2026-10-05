---
name: researching-website-design
description: Analyzes industry websites for design patterns, layout, typography, and content strategies using first-principles thinking. Use when researching website design, UI patterns, or competitive design analysis.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [industry-or-topic]
  stability: stable
  content-hash: sha256:4829bf30cb564e0e86956a55ee9423aa335eb7f774ca12b1d1ffca9b364b415b
  last-verified-cc-version: 1.0.34
---

# Website Design Research

**Target**: $ARGUMENTS

Analyzes industry websites for design patterns through first-principles
thinking. Focus on layout, typography, color, and content presentation.
Pair with `auditing-website-accessibility` and `auditing-website-usability`
for implementation.

## Core Question

"How would users naturally expect this information organized if they had
never seen a website?"

## Workflow

1. **Find websites** - Search "[industry] companies/platforms", target 6-8 sites
2. **Extract design elements** - Colors (hex), typography, layout hierarchy, CTAs
3. **Track sources** - URL, authority level (H/M/L), cited research, cross-references
4. **Identify anomalies** - Who breaks conventions with better UX results?
5. **Synthesize findings** - Breakthroughs, patterns, contrarian insights, quick wins

## Output Format

### Source Index

```text
1. [Company] - [URL] - Authority: [H/M/L]
   Cites: [Studies/sources referenced]
   Cross-refs: [Shared sources with other sites]
```

### Design Breakthroughs (Max 3)

```text
BREAKTHROUGH #N (Impact: N/100)
Pattern: [Specific design element]
Principle: [Why it works for users]
Opportunity: [How to apply]
Sources: [URLs and cited research]
```

### Visual and Content Patterns

```text
COLORS: Primary #HEX [effect], Accent #HEX [effect]
TYPOGRAPHY: Headers [font/weight], Body [font/size]
HEADLINES: "[Pattern]" - [User psychology]
CTAS: "[Button text]" - [Action driver]
```

### Contrarian Insights

```text
Everyone: [Common practice]
Reality: [What creates better UX]
Evidence: [Sources]
```

### Quick Wins

```text
ELIMINATE: [Element hurting UX]
SIMPLIFY: [Over-complex pattern]
ADOPT: [Underused effective pattern]
```

## Rules

- Focus exclusively on visual design, layout, typography, and content
- Question every design assumption with first-principles thinking
- Extract exact values: hex codes, font names, button text
- Track cross-references between sites to identify authoritative sources
- Keep insights concise and actionable for design implementation

## Further Reading

- [Awwwards — Website Design Trends](https://www.awwwards.com/)
- [Google Fonts](https://fonts.google.com/)
- [Dribbble — Design Inspiration](https://dribbble.com/)
- [Smashing Magazine — Web Design](https://www.smashingmagazine.com/category/design/)
