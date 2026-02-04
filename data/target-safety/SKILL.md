---
name: target-safety
description: |
  Target safety assessment including known toxicities, essentiality, and
  off-target concerns. Use for early safety risk evaluation and target
  selection.

  Keywords: target safety, toxicity, essential gene, knockout, safety risks
category: Target Safety
tags: [safety, toxicity, essentiality, knockout, risk-assessment]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - imap-database
  - gwas-catalog
  - clinvar
  - essential-genes
---

# Target Safety Skill

Assess target safety before investing in drug development.

## Quick Start

```
/target-safety EGFR --full
/safety "BCR-ABL" --include knockout,expression
/essentiality-check --target "KRAS" --species human,mouse
```

## Safety Concerns

| Category | Description | Impact |
|----------|-------------|--------|
| Essentiality | Gene required for survival | High |
| Knockout phenotypes | Animal model effects | Medium |
| Human genetics | Disease associations | Medium |
| Pathway crosstalk | Off-target effects | Medium |
| Tissue expression | Safety biomarkers | Low |

## Output Structure

```markdown
# Target Safety Assessment: EGFR

## Summary

| Concern | Level | Impact |
|---------|-------|--------|
| Essentiality | Medium | Manageable |
| Knockout effects | High | Monitor |
| Human genetics | Low | Not concerning |
| Off-target | Medium | Selectivity needed |

**Overall Risk**: Medium - Proceed with safety monitoring

## Essentiality Analysis

### Gene Essentiality

| Species | Essential | Phenotype |
|---------|-----------|----------|
| Human | Likely | Haploinsufficiency possible |
| Mouse | Yes | Embryonic lethal (homozygous) |
| Rat | Yes | Growth defects |

### Human Genetic Data

| Variant | Effect | Frequency | Condition |
|--------|--------|-----------|----------|
| Loss-of-function | Tolerated | Common | Population variants |
| Gain-of-function | Pathogenic | Rare | Cancer syndromes |

**Interpretation**: Heterozygous tolerance observed - manageable risk

## Knockout Phenotypes

### Mouse Models

| Genotype | Viable | Phenotype | Severity |
|----------|--------|----------|----------|
| +/+ | Yes | Normal | - |
| +/- | Yes | Skin defects, hair loss | Medium |
| -/- | No | Embryonic lethal | High |

**Key Findings**:
- Heterozygous viable with mild phenotypes
- Skin-related effects expected
- Dose-dependent toxicity likely

## Tissue Expression

### Expression Profile

| Tissue | Expression Level | Safety Concern |
|--------|-----------------|----------------|
| Skin | High | High (rash, acne) |
| Lung | Medium | Medium (interstitial lung disease) |
| GI Tract | Medium | Medium (diarrhea) |
| Liver | Low | Low |
| Heart | Low | Low |
| CNS | Low | Low |

**Safety Biomarkers**: Skin toxicity, lung function

## Known Safety Issues

### Approved EGFR Inhibitors

| Drug | Safety Issue | Incidence | Management |
|------|---------------|-----------|------------|
| Erlotinib | Rash | 70% | Topical steroids |
| Erlotinib | Diarrhea | 50% | Loperamide |
| Osimertinib | ILD | 3% | Steroids, discontinuation |
| Osimertinib | Cardiac | 2% | Monitoring |

**Class Effects**:
- Skin toxicity (nearly universal)
- GI effects (common)
- Interstitial lung disease (rare but serious)

## Mitigation Strategies

1. **Dose titration**: Start low, go slow
2. **Therapeutic drug monitoring**: PK-guided dosing
3. **Biomarker monitoring**: Skin assessment, pulmonary function
4. **Patient selection**: Exclude pre-existing conditions
5. **Proactive management**: Pre-emptive skin care

## Comparison to Similar Targets

| Target | Safety Profile | Comparable Issues |
|--------|-----------------|-------------------|
| EGFR | Medium | Skin, lung |
| HER2 | Medium | Cardiac |
| VEGFR | High | Hypertension, proteinuria |
| MET | Medium | Edema |

## Recommendations

### Preclinical

1. **Toxicology species selection**: Use relevant species
2. **Safety pharmacology**: Focus on skin, lung, cardiac
3. **Biomarker development**: Skin histopathology
4. **MARG**: Maximum recommended starting dose

### Clinical

1. **First-in-human dose**: Conservative (1/10 STD10)
2. **Cohort expansion**: Include PK/PD modeling
3. **Monitoring plan**:
   - Daily skin assessment (first cycle)
   - Baseline and periodic pulmonary function
   - ECG monitoring
   - Liver function tests

4. **Stopping rules**:
   - Grade 3+ rash >14 days
   - Any Grade 2+ ILD
   - Unresolved diarrhea >14 days

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Skin toxicity | High | Medium | Proactive management |
| ILD | Low | High | Monitoring, early detection |
| Diarrhea | High | Low | Standard supportive care |
| Cardiac | Low | Medium | ECG monitoring |
| Hepatotoxicity | Low | Medium | LFT monitoring |
