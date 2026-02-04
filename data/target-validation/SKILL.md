---
name: target-validation
description: |
  Comprehensive target validation assessing druggability, disease association strength,
  tractability, and competitive landscape. Use for go/no-go decisions on target selection.

  Keywords: target validation, druggability, tractability, disease association, genetic validation
category: Target Analysis
tags: [target, validation, druggability, tractability, genetics]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - opentargets
  - gwas-catalog
  - clinvar
  - uniprot
---

# Target Validation Skill

Comprehensive target validation for drug discovery decision-making.

## Quick Start

```
/target-validate EGFR --full
/validate "KRAS G12C" --association oncology
/tractability --target "BCR-ABL" --include genetic,chemical,clinical
```

## Validation Framework

### The 4-Pillar Framework

```
1. Genetic Validation
   ├── GWAS associations
   ├── Mendelian randomization
   ├── CRISPR screens
   └── Animal models

2. Chemical Validation
   ├── Known binders
   ├── Tool compounds
   ├── Co-crystal structures
   └── SAR coverage

3. Clinical Validation
   ├── Approved drugs
   ├── Pipeline drugs
   ├── Genetic therapies
   └── Biomarker linkage

4. Competitive Landscape
   ├── Active companies
   ├── Patent density
   ├── Differentiation potential
   └── Market maturity
```

## Output Structure

```markdown
# Target Validation: EGFR

## Validation Summary

| Pillar | Score | Status |
|--------|-------|--------|
| Genetic | 5/5 | ✓ Strong |
| Chemical | 5/5 | ✓ Strong |
| Clinical | 5/5 | ✓ Strong |
| Competition | 2/5 | ⚠ Crowded |

**Overall Validation**: Strong (17/20)

## Genetic Validation

### Human Genetics

| Evidence | Score | Details |
|----------|-------|---------|
| GWAS | 5/5 | 5 genome-wide significant associations |
| Mendelian | 5/5 | Activating mutations cause lung cancer |
| Somatic | 5/5 | Mutations in 15% NSCLC |
| eQTL | 4/5 | Strong expression QTLs |
| PheWAS | 3/5 | Cancer-associated phenotypes |

**Key Studies**:
- Zhang et al. (2020): OR = 2.5, p = 2×10⁻¹²
- Mendelian randomization supports causality

### Animal Models

| Model | Evidence | Phenotype |
|-------|----------|----------|
| Knockout mouse | 5/5 | Lung development defects |
| Transgenic (mutant) | 5/5 | Tumor formation |
| Zebrafish | 3/5 | Developmental phenotype |

## Chemical Validation

### Known Binders

| Compound | Type | Potency | Status |
|----------|------|---------|--------|
| Erlotinib | Small molecule | 2 nM | Approved |
| Osimertinib | Small molecule | 1 nM | Approved |
| Cetuximab | Biologic | 0.1 nM | Approved |
| Amivantamab | Biologic | 0.5 nM | Phase 3 |

### Structural Coverage

| Metric | Value |
|--------|-------|
| PDB entries | 127 |
| Co-crystals | 89 |
| Active conformations | 45 |
| Inactive conformations | 12 |

**Conclusion**: Excellent structural coverage for SBDD

## Clinical Validation

### Approved Drugs

| Drug | Indication | Year | Sales |
|------|-----------|------|-------|
| Erlotinib | NSCLC | 2004 | $1.5B |
| Gefitinib | NSCLC | 2002 | $0.8B |
| Osimertinib | NSCLC | 2015 | $5.2B |
| Afatinib | NSCLC | 2013 | $0.3B |

### Pipeline Drugs

| Drug | Company | Phase | Indication |
|------|---------|-------|------------|
| Lazertinib | J&J | 3 | NSCLC |
| Nazartinib | Novartis | 2 | NSCLC |

**Clinical Confidence**: Proven mechanism with multiple approvals

## Competitive Landscape

### Active Companies (2024)

| Company | Phase | Assets |
|---------|-------|--------|
| AstraZeneca | 3 | 3rd-gen TKI |
| Johnson & Johnson | 3 | 4th-gen TKI |
| Roche | 2 | Biologics |
| Merck | 1 | ADC |
| BeiGene | 2 | TKI |

### Patent Landscape

| Metric | Value |
|--------|-------|
| Active patents | 245 |
| Key patents expiring | 2030-2035 |
| White space | 4th-gen, combinations |

**Competition Assessment**: High competition but proven market

## Tractability

### Druggability Assessment

| Metric | Score | Details |
|--------|-------|---------|
| Class | A | Kinase, well-characterized |
| Binding site | A | ATP pocket, drug-like |
| Location | A | Cell surface (TKI) |
| Assayability | A | Biochemical, cellular |
| Selectivity | B | Kinome-wide selectivity needed |

**Tractability**: Highly tractable (class A kinase)

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|-----------|
| Safety | Medium | Cardiac toxicity monitoring |
| Resistance | High | 3rd/4th-gen solutions |
| Competition | High | Differentiate on resistance |
| IP | Medium | Novel chemical series |

## Recommendation

**Go/No-Go**: GO - Proceed with EGFR program

**Rationale**:
- Strong genetic validation
- Proven clinical mechanism
- Tractable target
- Large market despite competition

**Strategy**:
- Focus on resistance mutations (C797S)
- Combination approaches
- CNS-penetrant molecules

**Priority Actions**:
1. Review 4th-gen competitive landscape
2. Assess CNS penetration opportunity
3. Evaluate combination strategies
```

## Validation Scoring

### Genetic Evidence (0-5)

| Score | Criteria |
|-------|----------|
| 5 | Definitive causal link (Mendelian) |
| 4 | Strong GWAS + functional validation |
| 3 | GWAS association only |
| 2 | Moderate association |
| 1 | Weak genetic evidence |
| 0 | No genetic evidence |

### Chemical Evidence (0-5)

| Score | Criteria |
|-------|----------|
| 5 | Multiple drug classes, many binders |
| 4 | Several binders, good SAR |
| 3 | Some binders, limited SAR |
| 2 | Few tool compounds |
| 1 | Probes only |
| 0 | No chemical matter |

### Clinical Evidence (0-5)

| Score | Criteria |
|-------|----------|
| 5 | Multiple approved drugs |
| 4 | One approved, others in pipeline |
| 3 | Late-stage pipeline |
| 2 | Early clinical evidence |
| 1 | Preclinical only |
| 0 | No clinical evidence |

## Running Scripts

```bash
# Full validation
python scripts/target_validation.py EGFR --full

# Association analysis only
python scripts/target_validation.py KRAS --association oncology

# Tractability assessment
python scripts/tractability.py --target "BCR-ABL" --structure

# Comparison
python scripts/target_validation.py EGFR KRAS ALK --compare
```

## Requirements

```bash
pip install requests pandas numpy

# Optional for advanced features
pip install scipy statsmodels
```

## Reference

- [reference/validation-methods.md](reference/validation-methods.md) - Validation methodology
- [reference/genetics.md](reference/genetics.md) - Genetic validation reference
- [reference/tractability.md](reference/tractability.md) - Tractability assessment

## Best Practices

1. **Use multiple evidence types**: No single source sufficient
2. **Weight clinical highest**: Approved drugs = strongest validation
3. **Consider disease**: Oncology targets different from CNS
4. **Assess timing**: Early targets = higher risk/reward
5. **Review competition**: Impacts differentiation strategy

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Over-reliance on expression | Functional validation needed |
| Ignoring genetics | Human genetics predicts clinical success |
| Late to crowded targets | Early differentiation key |
| Undervaluing safety | Safety failures expensive |
| Single-source bias | Triangulate evidence
