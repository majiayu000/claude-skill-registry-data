---
name: prisma-tracking
description: Track PRISMA 2020 flow for systematic literature reviews. Updates counts at each stage of literature acquisition. Generates compliant flow diagrams.
user-invocable: false
---

# PRISMA Flow Tracking

Track the PRISMA 2020 flow throughout literature acquisition.

## PRISMA 2020 Stages

```
Identification
├── Records from databases (OpenAlex, PubMed, Semantic Scholar)
├── Records from citation searching
└── Records from other sources

Screening
├── Records after duplicates removed
├── Records screened
└── Records excluded (with reasons)

Eligibility
├── Reports sought for retrieval
├── Reports not retrieved (with reasons)
├── Reports assessed for eligibility
└── Reports excluded (with reasons)

Included
├── Studies included in review
└── Reports of included studies
```

## World Model Integration

Track in `$SESSION_DIR/world_model.json`:

```json
{
  "prisma_flow": {
    "identification": {
      "databases": {
        "openalex": 250,
        "pubmed": 180,
        "semantic_scholar": 120
      },
      "citation_searching": 85,
      "other_sources": 15,
      "total_identified": 650
    },
    "screening": {
      "after_duplicates_removed": 420,
      "records_screened": 420,
      "records_excluded": 280,
      "exclusion_reasons": {
        "not_relevant_to_rqs": 150,
        "wrong_study_type": 80,
        "wrong_language": 30,
        "retracted": 20
      }
    },
    "eligibility": {
      "reports_sought": 140,
      "reports_not_retrieved": 25,
      "not_retrieved_reasons": {
        "paywalled": 15,
        "link_broken": 10
      },
      "reports_assessed": 115,
      "reports_excluded": 45,
      "exclusion_reasons": {
        "insufficient_data": 25,
        "duplicate_cohort": 12,
        "wrong_outcomes": 8
      }
    },
    "included": {
      "studies_in_review": 70,
      "reports_of_studies": 70
    }
  }
}
```

## Update Functions

After each literature acquisition step, update PRISMA counts:

### After Initial Search
```python
prisma_flow["identification"]["databases"]["openalex"] = len(openalex_results)
prisma_flow["identification"]["databases"]["pubmed"] = len(pubmed_results)
prisma_flow["identification"]["total_identified"] = sum(all_results)
```

### After Deduplication
```python
prisma_flow["screening"]["after_duplicates_removed"] = len(unique_papers)
```

### After Relevance Filtering
```python
prisma_flow["screening"]["records_excluded"] = excluded_count
prisma_flow["screening"]["exclusion_reasons"]["not_relevant_to_rqs"] = not_relevant
```

### After Citation Expansion
```python
prisma_flow["identification"]["citation_searching"] += new_from_citations
```

### After Full-Text Retrieval
```python
prisma_flow["eligibility"]["reports_sought"] = attempted
prisma_flow["eligibility"]["reports_not_retrieved"] = failed
```

### After Final Inclusion
```python
prisma_flow["included"]["studies_in_review"] = final_count
```

## Generate PRISMA Diagram

Use matplotlib to generate the flow diagram:

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def generate_prisma_diagram(prisma_flow, output_path):
    fig, ax = plt.subplots(1, 1, figsize=(12, 16))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Identification box
    id_box = mpatches.FancyBboxPatch((0.5, 13), 11, 2.5,
                                      boxstyle="round,pad=0.1",
                                      facecolor='lightblue', edgecolor='black')
    ax.add_patch(id_box)
    ax.text(6, 14.5, 'Identification', fontsize=14, fontweight='bold', ha='center')
    ax.text(6, 13.8, f"Records from databases (n={prisma_flow['identification']['total_identified']})",
            ha='center')

    # ... continue for Screening, Eligibility, Included

    plt.savefig(output_path.replace('.pdf', '.png'), dpi=300, bbox_inches='tight')
    plt.savefig(output_path, bbox_inches='tight')
```

## Validation

Before synthesis, verify PRISMA flow is complete:

```python
def validate_prisma(prisma_flow):
    errors = []

    if prisma_flow["identification"]["total_identified"] == 0:
        errors.append("No papers identified - literature search not run")

    if prisma_flow["screening"]["after_duplicates_removed"] == 0:
        errors.append("Deduplication not tracked")

    if prisma_flow["included"]["studies_in_review"] == 0:
        errors.append("No studies included - check filtering")

    # Flow consistency
    if prisma_flow["screening"]["after_duplicates_removed"] > prisma_flow["identification"]["total_identified"]:
        errors.append("More papers after dedup than identified - impossible")

    return errors
```

## Completion Checklist

- [ ] All identification sources logged with counts
- [ ] Duplicates removed count recorded
- [ ] Exclusion reasons documented at each stage
- [ ] Full-text retrieval attempts logged
- [ ] Final included count matches cited papers
- [ ] PRISMA diagram generated (PNG + PDF)

**Track every paper. Document every exclusion. Generate compliant diagrams.**
