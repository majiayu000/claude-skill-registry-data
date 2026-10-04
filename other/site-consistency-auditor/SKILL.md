---
name: site-consistency-auditor
description: Audit website content for internal factual contradictions and inconsistent claims. Use when checking site consistency, finding conflicting facts across pages, verifying claims match, auditing content accuracy, or when user mentions contradictions, inconsistencies, fact-checking, or content audits. Works with HTML files, markdown content, route files, or any site content.
---

# Site Consistency Auditor

Identify factual claims that contradict each other across different pages of a website.

## Workflow

1. **Gather inputs** — Confirm content source (files, URLs, sitemap) and any truth baseline docs (brand guidelines, service documentation)
2. **Extract claims** — Harvest every discrete factual assertion from each page (see Claim Categories below)
3. **Group by type** — Cluster same-category claims across pages into comparison sets
4. **Detect contradictions** — Flag direct conflicts, implicit tensions, and scope mismatches
5. **Prioritize & report** — Output findings using template in `references/output-template.md`

## Claim Categories

| Category | Examples |
|----------|----------|
| Company stats | Team size, years in business, customers served |
| Capabilities | Services offered, technical specs, supported formats |
| Credentials | Certifications, awards, partnerships |
| Service params | Pricing, turnaround, guarantees, availability |
| Logistics | Addresses, hours, coverage areas, contact details |
| Social proof | Review counts, ratings, case study stats |

## Contradiction Types

- **Direct** — Mutually exclusive values ("50 employees" vs "35 employees")
- **Implicit** — Logical tension ("same-day delivery" vs "3-5 business days")  
- **Scope mismatch** — Specific vs vague in misleading ways ("London only" vs "UK-wide")

## Priority Levels

| Level | Category | Rationale |
|-------|----------|-----------|
| 🔴 Critical | Contact details, legal claims, certifications | Trust/liability exposure |
| 🟡 High | Service specs, pricing, timelines, capabilities | Sets expectations |
| 🟢 Medium | Team bios, history, facility descriptions | Brand consistency |

## Confidence Tags

- ⚠️ **Definite** — Values mutually exclusive
- ❓ **Probable** — Likely conflict, interpretation-dependent
- 📝 **Ambiguous** — Could conflict, needs human judgment

## Exclusions

Ignore phrasing variance preserving meaning:
- "10+ years" ≈ "over a decade"
- "Nationwide" ≈ "across the country"

Focus on substance, not expression.

## Output

Use template in `references/output-template.md` for consistent reporting.
