---
name: competitor-landscape
description: |
  Analyze competitive landscape for drugs including clinical pipeline,
  mechanism of action, development status, and company profiles.

  Use this skill for competitive intelligence, pipeline tracking, market
  analysis, and investment due diligence. Supports drug names, target areas,
  or disease indications.

  Keywords: competitor, competition, landscape, pipeline, drugs, market analysis
category: Competitive Intelligence
tags: [competitor, pipeline, landscape, drugs]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - chembl-database
  - drugbank-database
  - clinicaltrials-database
---

# Competitor Landscape Skill

Comprehensive competitive intelligence for drug development decisions.

## Quick Start

```
/competitor EGFR inhibitors
/competitor-landscape KRAS G12C drugs
Compare all EGFR TKIs in clinical development
Who's developing GLP-1R agonists for obesity?
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| **Market Overview** | Approved drugs, pipeline count, market size | Aggregated |
| **Competitive Map** | Company-by-portfolio breakdown | PharmaProjects |
| **Mechanism Analysis** | MOA classification, differentiation | ChEMBL, literature |
| **Clinical Status** | Phase distribution, readouts, timelines | ClinicalTrials.gov |
| **Key Players** | Company profiles, partnerships, deals | Company data |
| **Differentiation** | Competitive positioning, white space | Analysis |

## Output Structure

```markdown
# EGFR Inhibitors - Competitive Landscape

## Executive Summary
The EGFR inhibitor market is mature but evolving. 9 drugs approved with
3rd-generation TKIs dominating. Pipeline focuses on resistance mechanisms
and CNS penetration. Key battleground: 4th-generation agents for C797S.

## Market Overview
| Metric | Value |
|--------|-------|
| Approved Drugs | 9 (5 TKIs, 4 antibodies) |
| In Development | 34 candidates (21 clinical) |
| Market Size | $12B globally (2023) |
| Key Companies | AstraZeneca, Roche, Boehringer |

## 1. Competitive Map by Company

### AstraZeneca (Leader)
| Drug | Type | Phase | Differentiation |
|------|------|-------|----------------|
| Osimertinib | 3rd-gen TKI | Approved | Standard of care |
| AZD9291 + savolitinib | Combo | III | MET amp resistance |

### Roche
| Drug | Type | Phase | Status |
|------|------|-------|--------|
| Erlotinib | 1st-gen TKI | Approved | Generic |
| Tiragolumab + atezo | TIGIT + EGFR | III | Combo |

[... more companies ...]

## 2. Approved Drugs Analysis

| Drug | Company | Launch | Type | Key Indication | Sales 2023 |
|------|---------|--------|------|----------------|------------|
| Osimertinib | AstraZeneca | 2015 | 3rd-gen TKI | NSCLC 1st line | $5.8B |
| Erlotinib | Astellas | 2004 | 1st-gen TKI | NSCLC 2nd line | $0.3B |
| Gefitinib | AstraZeneca | 2003 | 1st-gen TKI | NSCLC | $0.2B |
| Necitumumab | Eli Lilly | 2015 | Antibody | Squamous NSCLC | Discontinued |
| Amivantamab | J&J | 2021 | Bispecific | Exon20ins | $0.2B |

## 3. Pipeline by Development Phase

### Phase III
| Drug | Company | Differentiation | Readout |
|------|---------|----------------|---------|
| Lazertinib | Yuhan/J&J | 3rd-gen, WT sparing | 2024 H2 |
| Nazartinib | Novartis | CNS active | 2024 Q3 |
| Patritumab deruxtecan | Daiichi Sankyo | ADC | 2025 |

### Phase II
| Drug | Company | Mechanism | Novelty |
|------|---------|-----------|---------|
| BLU-945 | Blueprint | 4th-gen (C797S) | First-in-class |
| BPI-9016M | Betta | 4th-gen | C797S focus |
| ... | ... | ... | ... |

## 4. Mechanism of Action Classification

| Class | Count | Status |
|-------|-------|--------|
| 1st-gen TKI | 3 approved | Generic |
| 2nd-gen TKI | 2 approved | Mature |
| 3rd-gen TKI | 3 approved | Dominant |
| 4th-gen TKI | 5 in clinic | Emerging |
| Antibodies | 4 approved | Niche |
| Bispecifics | 3 in clinic | Emerging |
| ADCs | 4 in clinic | Hot area |

## 5. Key Development Trends

### 2023-2024 Trends
1. **4th-generation TKIs**: Focus on C797S resistance mutation
2. **CNS penetration**: Critical for brain mets
3. **Combination therapies**: EGFR + MET, EGFR + chemotherapy
4. **ADC approach**: HER3-ADC, MET-ADC combinations
5. **Bispecifics**: Amivantamab leading

### White Space Opportunities
| Area | Rationale |
|------|-----------|
| 4th-gen TKI | C797S mutation unaddressed |
| Brain mets | High unmet need |
| Early detection | Neoadjuvant setting |
| Resistance combo | MET amp, HER3 upregulation |

## 6. Company Profiles

### AstraZeneca (Market Leader)
- **Portfolio**: Osimertinib (core), Tagrisso + chemoprev (adjuvant)
- **Strategy**: Extend osimertinib lifecycle (adjuvant, combo)
- **Strengths**: First-mover, brand recognition
- **Weaknesses**: Patent cliff approaching

### Emerging Players
- **Blueprint Medicines**: 4th-gen TKI leader (BLU-945)
- **J&J**: Combo strategy (lazertinib + EGFR/c-MET bispecific)
- **Daiichi Sankyo**: ADC approach (patritumab deruxtecan)

## 7. Investment & Deals (Recent)

| Deal | Type | Value | Year |
|------|------|-------|------|
| J&J / Yuhan | Licensing | $1.2B | 2018 |
| Merck / Daiichi Sankyo | Combo partnership | $4.5B | 2023 |
| BMS / Turning Point | Acquisition | $4.1B | 2023 |

## 8. Go/No-Go Considerations

### Green Light Signals
- C797S mutation space open
- CNS penetration unmet
- Combination approaches working

### Red Light Signals
- 3rd-gen crowded
- Generic erosion (1st/2nd gen)
- High clinical trial costs

### Yellow Light Signals
- 4th-gen clinical risk (first-in-class)
- Combination regulatory complexity
```

## Examples

### Drug Class Analysis
```
/competitor EGFR TKIs
/competitor GLP-1R agonists
/competitor PCSK9 inhibitors
```

### Disease Area Analysis
```
/competitor NSCLC therapies
Compare Alzheimer's drugs in development
/competitor obesity medications --phase 2-3
```

### Company Portfolio
```
What is AstraZeneca's oncology pipeline?
Compare Roche vs Novartis in hematology
/competitor "Company Name" portfolio
```

### Mechanism Focus
```
/competitor KRAS G12C inhibitors
Compare all PROTAC degraders in clinic
/competitor antibody-drug conjugates
```

## Running Scripts

```bash
# Fetch competitive landscape data
python scripts/fetch_competitor_data.py "EGFR inhibitors" --output data.json

# Include clinical trials
python scripts/fetch_competitor_data.py "KRAS" --clinical-trials -o full.json

# Company-specific
python scripts/fetch_competitor_data.py --company "AstraZeneca" --indication oncology
```

## Requirements

```bash
pip install requests pandas lxml
```

## Additional Resources

- [ChEMBL API Reference](reference/chembl-api.md)
- [Competitive Analysis Framework](reference/analysis-framework.md)
- [Company Data Sources](reference/company-data.md)

## Best Practices

1. **Be specific**: Use drug class names (e.g., "3rd-gen EGFR TKI")
2. **Define scope**: Specify indication, phase, or company
3. **Compare**: Ask for competitive positioning
4. **Look for white space**: Ask about unaddressed areas

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too broad | Specify drug class or indication |
| Missing context | Include disease area |
| Outdated pipeline | Check date of data |
| Public vs private | Public sources only |
