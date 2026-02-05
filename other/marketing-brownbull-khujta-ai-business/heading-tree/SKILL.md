---
name: heading-tree
description: Generates H1-H4 heading structure for a page. SEO-optimized hierarchy. Stateless, deterministic.
---

# Heading Tree Skill

## Purpose

Outputs H1-H4 heading hierarchy for a page. Structure only, no body copy.

## Skill Output

Single deterministic heading tree. No alternatives, no variants.

```yaml
headings:
  - level: h1
    section: hero
    text: "House Removals Bristol - Stress-Free Moving"
  - level: h2
    section: benefits
    text: "Why Families Choose Our Moving Service"
    children:
      - level: h3
        text: "Fully Insured & Protected"
```

**Output contains `text` only.** Patterns/examples are documentation only.

## Input

```yaml
page_type: landing | service | service-area | article
primary_keyword: "house removals bristol"  # Required
secondary_keywords: ["moving company"]      # Optional
location: "Bristol"                         # Required for local
sections: [hero, benefits, faq, final-cta]  # From allowed list
faq_questions: ["How much..."]              # Optional
```

## Blocking Conditions (STOP)

| Condition | Result |
|-----------|--------|
| Missing `primary_keyword` | STOP - no output |
| Missing `page_type` | STOP - no output |
| Unknown section in list | IGNORE section |
| Empty sections list | STOP - no output |

## Allowed Sections

| Section | H2 | H3s |
|---------|-----|-----|
| `hero` | No (H1 only) | No |
| `trust-strip` | No | No |
| `problem` | Yes | No |
| `solution` | Yes | No |
| `benefits` | Yes | 3 typical |
| `how-it-works` | Yes | 3 (steps) |
| `social-proof` | Yes | No |
| `pricing` | Yes | 2-3 (tiers) |
| `faq` | Yes | 6 (questions) |
| `final-cta` | Yes | No |
| `gallery` | Yes | No |
| `coverage` | Yes | Optional |

**Unknown section → ignored, no error.**

## Heading Rules

### H1 Rules

| Rule | Requirement |
|------|-------------|
| Count | Exactly 1 per page |
| Keyword | Primary keyword at START |
| Location | Include if local business |
| Length | Max 60 characters |
| Section | Always `hero` |

### H2 Rules

| Rule | Requirement |
|------|-------------|
| Count | 1 per section (except hero, trust-strip) |
| Order | Follow sections order |
| Primary keyword | In 1-2 H2s max |
| Location | In 2-3 H2s for local |

### H3 Rules

| Rule | Requirement |
|------|-------------|
| Parent | Always under H2 (never orphaned) |
| Count | 3-6 per parent H2 |
| Keyword | Rarely, natural only |

### H4 Rules

| Rule | Requirement |
|------|-------------|
| Page type | Article ONLY |
| Count | Max 5 per page |
| Forbidden | Landing, service, service-area pages |

## FAQ Questions

| Scenario | Behavior |
|----------|----------|
| `faq_questions` provided | Use provided questions as H3s |
| `faq_questions` empty | Use generic templates |
| No FAQ section | Skip |

Generic FAQ templates:
- "How much does {service} cost?"
- "What areas do you cover?"
- "How do I book?"
- "Are you fully insured?"
- "How far in advance should I book?"
- "Do you provide {related_service}?"

## Location Mentions

For local business pages:

| Level | Location Required |
|-------|-------------------|
| H1 | Always |
| H2 | 2-3 headings |
| H3 | Rarely |

## Keyword Density (Annotation)

```yaml
keyword_density: primary | secondary | location | none
```

This is annotation only — helps downstream skills, not a rule.

| Density | Max Count |
|---------|-----------|
| primary | 3 total (H1 + 1-2 H2s) |
| secondary | No limit |
| location | H1 + 2-3 H2s |

## Example Output

```yaml
page_type: landing
primary_keyword: "house removals bristol"

headings:
  - level: h1
    section: hero
    text: "House Removals Bristol - Stress-Free Moving From £299"
    
  - level: h2
    section: benefits
    text: "Why Families Choose Our Moving Service"
    children:
      - { level: h3, text: "Fully Insured & Protected" }
      - { level: h3, text: "Fixed Price, No Hidden Fees" }
      - { level: h3, text: "Professional Packing Service" }
      
  - level: h2
    section: faq
    text: "House Removals FAQs"
    children:
      - { level: h3, text: "How much do Bristol removals cost?" }
      - { level: h3, text: "What areas around Bristol do you cover?" }
      
  - level: h2
    section: final-cta
    text: "Ready for a Stress-Free Move?"
```

## Non-goals

- Does NOT write body copy
- Does NOT suggest alternatives
- Does NOT optimize existing headings
- Does NOT do keyword research
- Does NOT analyze competitors

## Forbidden

- ❌ Multiple H1s
- ❌ H4 on non-article pages
- ❌ Orphaned H3 (no parent H2)
- ❌ Keyword stuffing (>3 primary mentions)
- ❌ Providing alternative heading options
- ❌ Writing body content

## References

- [patterns-landing.md](references/patterns-landing.md) — Landing page patterns
- [patterns-service.md](references/patterns-service.md) — Service page patterns
- [patterns-article.md](references/patterns-article.md) — Article patterns

## Definition of Done

- [ ] Exactly 1 H1
- [ ] H2s match sections list
- [ ] H3s have parent H2
- [ ] No H4 (unless article)
- [ ] Primary keyword in H1
- [ ] Primary keyword in 1-2 H2s
- [ ] Location in H1 + 2-3 H2s (if local)
