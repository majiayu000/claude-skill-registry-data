---
name: keyword-research
description: Keyword research for UK local service businesses. Generates silo-compatible keyword map. Binding input for heading-tree and internal-linking skills.
---

# Keyword Research Skill

## Purpose

Generates keyword map organized by silos. One canonical keyword per page.

## Primary Objective

**Maximize transactional intent coverage for service (silo top) and area pages.**

Not "more keywords" — focused targeting.

## Skill Output Contract

Output is **binding input** for:
- `heading-tree` skill (H1 from canonical keyword)
- `internal-linking` skill (silo structure)
- `lead-gen-copy` skill (page copy)

This is not a suggestion list.

## Input

```yaml
business:
  service: "house removals"       # Core service
  location: "Bristol"             # Primary location
  service_areas: ["Bath", "Weston-super-Mare"]
  services: ["house removals", "office removals", "packing"]
```

## Output

```yaml
silos:
  - name: "house-removals"
    keywords:
      silo_top:
        canonical: "house removals bristol"
        supporting: ["removal company bristol", "movers bristol"]
      areas:
        - page: "/areas/bath"
          canonical: "removals bath"
          supporting: ["house movers bath"]
      articles:
        - page: "/blog/moving-costs"
          canonical: "how much do removals cost"
          
questions: [...]
near_me: [...]
```

## Keyword Budget Per Page

| Page Type | Canonical | Supporting | Long-tail | Total Max |
|-----------|-----------|------------|-----------|-----------|
| Homepage | 1 | 2 | 2 | 5 |
| Service (silo top) | 1 | 2 | 3 | 6 |
| Area page | 1 | 1 | 2 | 4 |
| Article | 1 | 1 | 0 | 2 |

**Canonical keyword** = THE one keyword for H1. Only one per page.

## Silo Structure

Keywords organized by content silos:

```yaml
silo:
  name: "house-removals"
  
  silo_top:                        # Service page = money page
    page: "/services/house-removals"
    canonical: "house removals bristol"
    supporting:
      - "removal company bristol"
      - "movers bristol"
    long_tail:
      - "cheap removals bristol"
      - "best removal company bristol"
      
  areas:                           # Feed up to silo top
    - page: "/areas/bath"
      canonical: "removals bath"
      supporting: ["house movers bath"]
      
    - page: "/areas/weston"
      canonical: "removals weston-super-mare"
      
  articles:                        # Support silo top
    - page: "/blog/moving-costs"
      canonical: "how much do removals cost"
```

## Keyword Types

### Canonical Keywords

**ONE per page.** Used in:
- H1 heading (required)
- Meta title (required)
- URL slug (if possible)

| Page Type | Pattern |
|-----------|---------|
| Homepage | `{service} {location}` |
| Service | `{service} {location}` |
| Area | `{service} {area}` or `removals {area}` |
| Article | Question or topic phrase |

### Supporting Keywords

2-3 per page. Used in:
- H2 headings (1-2)
- Meta description
- Body content

### Long-tail Keywords

Modifiers + core keyword. Used in:
- Body content
- FAQ answers
- NOT in H1/H2

| Modifier Type | Examples |
|---------------|----------|
| Price | cheap, affordable, budget |
| Quality | best, top rated, professional |
| Urgency | same day, emergency, last minute |
| Size | small, single item, full house |

## Synonym Rules

**ONE dominant synonym per page.**

```yaml
synonyms:
  house_removals:
    dominant: "house removals"      # Use in H1
    supporting: ["movers", "moving company", "relocation"]
    
# Page uses ONE dominant, others in body only
page: "/services/house-removals"
h1: "House Removals Bristol"        # Dominant
body: "...our moving company..."    # Supporting
```

## "Near Me" Keywords

**Special handling — NOT in headings.**

| Allowed | Forbidden |
|---------|-----------|
| Schema LocalBusiness | H1 |
| Google Business Profile | H2 |
| FAQ answer | Meta title |
| CTA text | URL |

```yaml
near_me_keywords:
  - "removals near me"
  - "moving company near me"
  
usage:
  schema: true
  gbp: true
  faq: "Looking for removals near me? We cover..."
  heading: false  # NEVER
```

## Question Keywords

Allocated to FAQ or articles:

```yaml
questions:
  faq:                    # Short answers on service pages
    - "how much do removals cost"
    - "how long does moving take"
    - "are you insured"
    
  articles:               # Long-form content
    - "how much does it cost to move a 3 bed house"
    - "removal company vs man and van"
    - "how to pack for a house move"
```

| Question Type | Destination | Answer Length |
|---------------|-------------|---------------|
| Cost | FAQ or Article | 1 para or full guide |
| Process | FAQ | 1-2 sentences |
| Comparison | Article | Full guide |
| How-to | Article | Full guide |

## Complete Output Example

```yaml
keyword_research:
  business:
    service: "house removals"
    location: "Bristol"
    
  silos:
    - name: "house-removals"
      silo_top:
        page: "/"
        canonical: "house removals bristol"
        supporting: ["removal company bristol"]
        long_tail: ["cheap removals bristol"]
        
      areas:
        - page: "/areas/bath"
          canonical: "removals bath"
          
    - name: "office-removals"
      silo_top:
        page: "/services/office-removals"
        canonical: "office removals bristol"
        
  questions:
    faq: ["how much do removals cost"]
    articles: ["how to pack fragile items"]
    
  near_me: ["removals near me"]
  
  summary:
    total_pages: 8
    total_keywords: 24
    silos: 2
```

## Blocking Conditions (STOP)

| Condition | Result |
|-----------|--------|
| No canonical for page | STOP |
| >1 canonical per page | STOP |
| Near-me in heading | STOP |
| Budget exceeded | STOP |

## Non-goals

- Does NOT provide search volumes
- Does NOT analyze competition
- Does NOT track rankings
- Does NOT prioritize by traffic

## Forbidden

- ❌ Multiple canonical keywords per page
- ❌ "Near me" in H1/H2
- ❌ Exceeding keyword budget
- ❌ Same canonical on two pages
- ❌ Keywords without silo assignment

## References

- [patterns.md](references/patterns.md) — Keyword patterns by type
- [synonyms.md](references/synonyms.md) — Service synonym mapping
- [modifiers.md](references/modifiers.md) — Long-tail modifiers

## Definition of Done

- [ ] Every page has ONE canonical keyword
- [ ] Keyword budget respected
- [ ] All keywords assigned to silo
- [ ] No "near me" in headings
- [ ] Synonyms: one dominant per page
- [ ] Questions allocated to FAQ/article
- [ ] Output ready for heading-tree skill
