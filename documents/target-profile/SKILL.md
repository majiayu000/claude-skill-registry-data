---
name: target-profile
description: |
  Generate comprehensive target profiles including druggability assessment,
  disease associations, pathway context, and competitive landscape.

  Use this skill when analyzing drug targets for validation, dossier creation,
  or competitive intelligence. Supports gene symbols (EGFR), protein names,
  or UniProt IDs.

  Keywords: target, dossier, validation, druggability, tractability, target analysis
category: Target Analysis
tags: [target, drug-discovery, dossier, validation]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - opentargets-rest-api
  - uniprot-rest-api
  - chembl-rest-api
---

# Target Profile Skill

Generate comprehensive target dossiers for drug discovery decision-making.

## Quick Start

```
/target EGFR
/target-profile KRAS G12C
Create a target dossier for HER2 including clinical trials
Analyze druggability of BRAF V600E
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| **Executive Summary** | Key insights in one page | Aggregated |
| **Target Overview** | Gene/protein name, class, location | UniProt |
| **Druggability** | Tractability scores, target class | Open Targets |
| **Disease Associations** | Associated diseases, evidence scores | Open Targets |
| **Pathways** | Signaling pathways, interactions | KEGG, Reactome |
| **Competition** | Existing drugs, pipeline | ChEMBL, DrugBank |
| **Safety** | Known safety concerns | Pharos, SIDER |

## Data Sources

| Source | API | Coverage |
|--------|-----|----------|
| Open Targets | `api.opentargets.org` | 20k+ targets, 1.2M associations |
| UniProt | `rest.uniprot.org` | 200M+ proteins |
| ChEMBL | `www.ebi.ac.uk/chembl/api` | 2.5M+ compounds |
| KEGG | `rest.kegg.jp` | 500+ pathways |
| Reactome | `reactome.org` | 2600+ pathways |

## Output Structure

```markdown
# EGFR Target Profile

## Executive Summary
EGFR is a high-tractability receptor tyrosine kinase with strong validation
in NSCLC. 9 drugs approved, 34 in development. Key opportunity: resistance
mechanisms and combination therapies.

## Quick Stats
| Metric | Value |
|--------|-------|
| Tractability | 8.2/10 (Small molecule) |
| Disease Associations | 142 diseases |
| Approved Drugs | 9 |
| Pipeline Candidates | 34 |
| Safety Tier | 2 (Moderate risk) |

## 1. Target Overview
- **Gene**: EGFR (ERBB1)
- **Protein**: Epidermal growth factor receptor
- **Class**: Receptor tyrosine kinase
- **Location**: Cell membrane (Plasma membrane)
- **Length**: 1210 amino acids
- **MW**: 134 kDa

## 2. Druggability Assessment
### Tractability Scores
| Modality | Score | Evidence |
|----------|-------|----------|
| Small molecule | 8.2/10 | 9 approved drugs |
| Antibody | 7.8/10 | 4 approved antibodies |
| PROTAC | 6.5/10 | Emerging approach |

### Target Development Level
**Tclin (Highest)** - Target with drugs approved for clinical use

## 3. Disease Associations
| Disease | Association Score | Evidence Type |
|---------|------------------|---------------|
| Lung adenocarcinoma | 0.95 | Genetic association |
| Glioblastoma | 0.87 | Somatic mutation |
| Head and neck cancer | 0.82 | Genetic association |

## 4. Pathway Context
- **Primary Pathway**: ErbB signaling pathway (KEGG: hsa04012)
- **Upstream**: EGF, TGF-alpha, Amphiregulin
- **Downstream**: MAPK, PI3K-Akt, JAK-STAT
- **Cross-talk**: MET, HER2, HER3

## 5. Competitive Landscape
### Approved Drugs
| Drug | Company | Year | Type | Indication |
|------|---------|------|------|------------|
| Erlotinib | Astellas | 2004 | TKI | NSCLC |
| Gefitinib | AstraZeneca | 2003 | TKI | NSCLC |
| Osimertinib | AstraZeneca | 2015 | 3rd-gen TKI | NSCLC |

### Pipeline (Selected)
| Drug | Company | Phase | Differentiation |
|------|---------|-------|----------------|
| Lazertinib | Yuhan | III | 3rd-gen, wild-type sparing |
| Nazartinib | Novartis | III | 3rd-gen, CNS active |

## 6. Safety Considerations
- **On-target toxicity**: Skin rash, diarrhea (class effect)
- **Off-target concerns**: Cardiac toxicity (rare)
- **Safety Tier**: 2 (Manageable risk)

## 7. Key Opportunities
1. Resistance mechanisms (C797S, MET amplification)
2. Combination therapies (EGFR + MET)
3. CNS-penetrant candidates
4. Biomarker-driven patient selection

## 8. Key Risks
1. Crowded competitive space
2. Generic competition (1st gen)
3. Resistance development
```

## Examples

### Basic Profile
```
/target EGFR
```

### With Specific Focus
```
/target KRAS --focus safety
Analyze safety profile of BTK
/target HER2 --focus competition
```

### Compare Multiple Targets
```
Compare targets EGFR, HER2, HER3 for NSCLC treatment
Rank KRAS, NRAS, HRAS by druggability
```

### Specific Analysis
```
/target BRAF V600C
Assess druggability of mutant BRAF
What is the tractability of KRAS G12C?
```

## Running Scripts

The `scripts/` directory contains data fetching utilities:

```bash
# Fetch basic target data
python scripts/fetch_target_data.py EGFR --output data.json

# Include all sources
python scripts/fetch_target_data.py EGFR --uniprot --chembl --pathways -o full.json

# Specific data only
python scripts/fetch_target_data.py KRAS --diseases-only
```

## Requirements

None for basic use (uses public APIs).

For advanced features and scripts:
```bash
pip install requests pandas
```

## Additional Resources

- [Open Targets API Reference](reference/opentargets-api.md)
- [Data Schema Definition](reference/data-schema.md)
- [Fetch Script Usage](reference/fetch-script.md)

## Best Practices

1. **Use official gene symbols** (HGNC nomenclature) for best results
2. **Include mutation** if relevant (e.g., "KRAS G12C")
3. **Specify focus** when you need deeper analysis on one area
4. **Compare targets** to support decision-making

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Ambiguous gene names | Use official HGNC symbols |
| Multiple isoforms | Specify isoform number if needed |
| Species confusion | Assume human unless specified |
| Outdated info | Data is current as of last API fetch |
