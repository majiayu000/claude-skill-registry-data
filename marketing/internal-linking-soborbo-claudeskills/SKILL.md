---
name: internal-linking
description: Plans internal link structure using content silos. Outputs link map with SEO priority. Does not create links.
---

# Internal Linking Skill

## Purpose

Outputs internal link structure using content silo architecture. SEO-focused link equity distribution.

## Primary Objective

**Push link equity to money pages (silo tops) through structured silos.**

Not "pretty web" — strategic authority building.

## Skill Output

```yaml
silos: [...]           # Defined content clusters
link_map: [...]        # Per-page outbound links
link_requirements: [...] # Inbound requirements
orphan_check: [...]    # Pages with <minimum inbound
```

## Input

```yaml
site_structure:
  silos:
    - name: "house-removals"
      top: "/services/house-removals"      # Money page
      areas: ["/areas/bath", "/areas/bristol"]
      articles: ["/blog/moving-costs", "/blog/packing-tips"]
      
    - name: "office-removals"
      top: "/services/office-removals"
      areas: ["/areas/bath-office"]
      articles: ["/blog/office-moving-guide"]
      
  standalone:
    - { url: "/calculator", type: "tool", priority: 1 }
    - { url: "/contact", type: "conversion" }
    - { url: "/about", type: "info" }
```

## Content Silo Rules

### Silo Structure

```
Homepage
    │
    ├── SILO: House Removals
    │   ├── /services/house-removals  ← SILO TOP (money page)
    │   ├── /areas/bath               ← links UP to silo top
    │   ├── /areas/bristol            ← links UP to silo top
    │   └── /blog/moving-costs        ← links UP to silo top
    │
    └── SILO: Office Removals
        ├── /services/office-removals ← SILO TOP (money page)
        └── /blog/office-guide        ← links UP to silo top
```

### Silo Linking Rules

| Rule | Requirement |
|------|-------------|
| Intra-silo | Encouraged — link freely within silo |
| Cross-silo | Limited — max 1-2 per page |
| Silo top receives | Links from ALL pages in silo |
| Areas/Blog | ALWAYS link to parent silo top |
| Homepage | Links to ALL silo tops |

### Cross-Silo Linking (Restricted)

| From | To | Allowed |
|------|-----|---------|
| Service → Service | Different silo | Max 1 "related service" |
| Area → Area | Different silo | NO (only nearby same-silo) |
| Blog → Blog | Different silo | Max 1 if highly relevant |
| Blog → Service | Different silo | NO |

## Link Budget Per Page

| Page Type | Max Outbound | Intra-silo | Cross-silo |
|-----------|--------------|------------|------------|
| Homepage | 25 | N/A | All silo tops |
| Service (silo top) | 15 | Unlimited | 2 max |
| Area page | 10 | 5+ | 1 max |
| Article | 12 | 3+ required | 1 max |
| Calculator | 5 | N/A | 2 (results only) |

## Inbound Requirements

### Minimum Inbound Links

| Page Type | Minimum | Priority Sources |
|-----------|---------|------------------|
| Silo top (service) | 5 | Homepage, all silo areas, all silo articles |
| Area page | 3 | Silo top, nearby areas, 1 article |
| Article | 2 | Silo top, related articles |
| Calculator | 4 | Homepage, ALL silo tops |
| Homepage | 1+ | Nav/logo from all pages |

### Inbound Priority Order

For silo tops (money pages), inbound links should come from:

1. **Homepage** (highest value)
2. **Same-silo areas** (relevance)
3. **Same-silo articles** (content support)
4. **Other silo tops** (1 max, related service)

## Anchor Text Rules

### Limits

| Anchor Type | Per Page | Per Target (total inbound) |
|-------------|----------|---------------------------|
| Exact match keyword | 1 max | 3 max site-wide |
| Service name | Unlimited | Unlimited |
| Branded | Unlimited | Unlimited |
| Generic | 0 in body | Nav/footer only |

### Anchor Patterns

| Target Type | Use |
|-------------|-----|
| Silo top | Service name, "our {service}" |
| Area | "{service} in {area}", "{area} removals" |
| Article | Topic phrase, question |
| Calculator | "get quote", "instant price", "calculate" |
| Homepage | Brand name, "home" |

### Forbidden Anchors

- ❌ "click here" in body content
- ❌ "read more" in body content  
- ❌ "learn more" in body content
- ❌ Same exact-match anchor 4+ times to one target

## Blog as Link Pump

**Blog's primary job: push equity to silo tops.**

| Rule | Requirement |
|------|-------------|
| Every article | MUST link to parent silo top |
| Link placement | Within first 3 paragraphs |
| Anchor | Service-focused, not generic |
| Cross-silo | Max 1 link, only if highly relevant |
| Blog → Blog | Max 2 "related posts" |

```yaml
# Good blog linking
article: "/blog/moving-costs"
silo: "house-removals"
required_outbound:
  - target: "/services/house-removals"  # Parent silo top
    anchor: "house removals service"
    placement: "body, paragraph 2"
optional_outbound:
  - target: "/blog/packing-tips"  # Same silo
    anchor: "packing guide"
```

## Calculator Page (Special)

**High-priority inbound, minimal outbound.**

| Direction | Rule |
|-----------|------|
| Inbound | From homepage + ALL silo tops |
| Outbound | Max 5: logo home + 2 in results |
| No nav | Minimal header, no full nav |

## Link Map Output

```yaml
link_map:
  - page: "/services/house-removals"
    silo: "house-removals"
    role: "silo_top"
    outbound:
      - { to: "/", anchor: "Home", section: "breadcrumb" }
      - { to: "/calculator", anchor: "Get your quote", section: "cta" }
      - { to: "/services/packing", anchor: "packing service", section: "related", cross_silo: true }
      - { to: "/areas/bath", anchor: "removals in Bath", section: "areas" }
    inbound_required:
      - { from: "/", min: 1 }
      - { from: "/areas/*", min: 2 }
      - { from: "/blog/*", min: 1 }
    inbound_actual: 4
    status: "healthy"
```

## Orphan Prevention

| Check | Rule |
|-------|------|
| Orphan | 0 inbound links → BLOCKER |
| Weak | Below minimum → WARNING |
| Healthy | At/above minimum → OK |

```yaml
orphan_check:
  orphan_pages: []      # Must be empty
  weak_pages: 
    - { url: "/areas/gloucester", inbound: 1, minimum: 3 }
  healthy_pages: 10
```

## Blocking Conditions (STOP)

| Condition | Result |
|-----------|--------|
| Orphan page exists | STOP — fix before deploy |
| Silo top has <3 inbound | STOP — add links |
| No silo definition | STOP — define silos first |
| Cross-silo >3 on any page | STOP — reduce |

## Non-goals

- Does NOT create actual links
- Does NOT handle external links
- Does NOT track performance
- Does NOT analyze competitors
- Does NOT audit existing sites

## Forbidden

- ❌ Orphan pages
- ❌ Generic anchors in body
- ❌ Exact match anchor >3 times to one target
- ❌ Blog not linking to silo top
- ❌ Cross-silo >3 per page
- ❌ Area linking to different-silo area

## References

- [silo-examples.md](references/silo-examples.md) — Full silo structures
- [anchor-patterns.md](references/anchor-patterns.md) — Anchor text by type

## Definition of Done

- [ ] All silos defined with tops
- [ ] Every page has silo assignment
- [ ] Every silo top has 5+ inbound
- [ ] Every article links to silo top
- [ ] Zero orphan pages
- [ ] Zero weak pages (below minimum)
- [ ] Cross-silo max 2 per page
- [ ] Calculator has 4+ inbound
