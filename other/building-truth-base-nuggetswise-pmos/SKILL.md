---
name: building-truth-base
description: Use when starting on a new product, joining a team, or needing a shared understanding of product, customers, and current bets.
---

# Building Truth Base

## Overview

Creates a Day-1 shared map of the product: what it is, who it serves, current roadmap themes, and top unknowns. This becomes the foundation for all other PM work.

## When to Use

- Starting a new PM role or joining a product team
- Need to establish baseline understanding
- Want to document what you've learned from onboarding
- Someone asks "what does this product actually do?"

## Core Pattern

**Step 1: Gather Available Sources**

Read all files in:
- `inputs/roadmap_deck/` - strategy slides, PDFs
- `inputs/product_demo/` - demo notes, walkthroughs
- `inputs/knowledge_base/` - KB articles about the product

If sources are missing, list what's needed and ask user to provide.

**Step 2: Extract Key Information**

From sources, identify:
1. What the product is (1 paragraph)
2. Who it serves (actors, personas, segments)
3. Core terminology (what do key terms mean in this context?)
4. Core workflows (user journeys, key flows)
5. Current roadmap themes (from deck)
6. Known constraints (tech debt, compliance, trust issues)

**Step 3: Identify Unknowns**

List 10-15 open questions you cannot answer from the sources. These become your investigation priorities.

**Step 4: Generate Output**

Write to `outputs/truth_base/truth-base.md` with metadata header:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: building-truth-base
sources:
  - inputs/roadmap_deck/strategy.pdf (modified: YYYY-MM-DD)
  - inputs/product_demo/demo-notes.md (modified: YYYY-MM-DD)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# Truth Base: [Product Name]

## What Is This Product?
[1 paragraph description]

## Who Does It Serve?
| Actor | Description | Key Jobs |
|-------|-------------|----------|
| ... | ... | ... |

## Core Terminology
| Term | Meaning (in this context) |
|------|---------------------------|
| ... | ... |

## Core Workflows
1. **[Workflow Name]:** [Brief description]
   - Trigger: ...
   - Steps: ...
   - Outcome: ...

## Current Roadmap Themes
| Theme | Description | Evidence |
|-------|-------------|----------|
| ... | ... | [source file] |

## Constraints & Risks
| Constraint | Impact | Source |
|------------|--------|--------|
| ... | ... | Evidence/Assumption |

## Top 15 Open Questions
1. [Question] — *Priority: High/Medium/Low*
2. ...

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| ... | Evidence/Assumption/Open Question | ... |
```

**Step 5: Copy to History**

Copy output to `history/building-truth-base/truth-base-YYYY-MM-DD.md`

**Step 6: Update Staleness Tracker**

Update `alerts/stale-outputs.md` with the new output and its sources.

## Quick Reference

| Action | Location |
|--------|----------|
| Input sources | `inputs/roadmap_deck/`, `inputs/product_demo/`, `inputs/knowledge_base/` |
| Output | `outputs/truth_base/truth-base.md` |
| History | `history/building-truth-base/` |
| Downstream | Quarterly charters |

## Common Mistakes

- **Inventing product details:** Only claim what's in sources → Mark unknowns as Open Questions
- **Skipping terminology:** "Catalog" means different things → Define terms explicitly
- **Too few questions:** 3 questions isn't enough → Aim for 10-15 open questions
- **No sources cited:** "The product does X" → Always cite which file told you this

## Verification Checklist

- [ ] All source files read and listed
- [ ] Product description is 1 paragraph (not a page)
- [ ] Actors/personas table populated
- [ ] Terminology table has key domain terms
- [ ] At least 10 open questions identified
- [ ] Every claim has Evidence/Assumption tag
- [ ] Metadata header includes sources and timestamps
- [ ] Output copied to history folder
- [ ] Staleness tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Product does X] | Evidence | [inputs/roadmap_deck/strategy.pdf] |
| [Users are Y segment] | Assumption | [inferred from KB articles] |
| [Integration with Z exists] | Open Question | [not stated in sources] |
