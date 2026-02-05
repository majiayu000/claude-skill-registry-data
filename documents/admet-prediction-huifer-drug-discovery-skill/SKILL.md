---
name: admet-prediction
description: |
  ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) prediction
  for drug candidates. Use for assessing drug-likeness, PK properties, and
  safety risks early in drug discovery.

  Keywords: ADMET, PK, toxicity, drug-likeness, DILI, hERG, bioavailability
category: DMPK
tags: [admet, pk, toxicity, drug-likeness, safety]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - rdkit
  - admet-models
---

# ADMET Prediction Skill

Predict ADMET properties to prioritize compounds for development.

## Quick Start

```
/admet "CC1=CC=C(C=C1)CNC" --full
/pk-prediction --library compounds.sdf --threshold 0.7
/toxicity-screen CHEMBL210 --include hERG,DILI,Ames
```

## What's Included

| Property | Prediction | Model |
|----------|------------|-------|
| Absorption | Caco-2, HIA, Pgp | ML/QSAR |
| Distribution | VDss, PPB, BBB | ML/QSAR |
| Metabolism | CYP inhibition, clearance | ML/QSAR |
| Excretion | Clearance, half-life | ML/QSAR |
| Toxicity | hERG, DILI, Ames, mutagenicity | ML/QSAR |

## Output Structure

```markdown
# ADMET Profile: CHEMBL210 (Osimertinib)

## Summary
| Property | Value | Status |
|----------|-------|--------|
| Drug-likeness | Pass | ✓ |
| Lipinski Ro5 | 0 violations | ✓ |
| VEBER | Pass | ✓ |
| PAINS | 0 alerts | ✓ |
| Brenk | 0 alerts | ✓ |

## Absorption
| Property | Prediction | Confidence |
|----------|------------|-------------|
| HIA | 98% | High |
| Caco-2 | 15.2 × 10⁻⁶ cm/s | High |
| Pgp substrate | Yes | Medium |
| F30% | 65% | Medium |

## Distribution
| Property | Prediction | Confidence |
|----------|------------|-------------|
| VDss | 5.2 L/kg | Medium |
| PPB | 95% | High |
| BBB | Yes | High |
| CNS MPO | 5.5 | Good |

## Metabolism
| Property | Prediction | Confidence |
|----------|------------|-------------|
| CYP3A4 substrate | Yes | High |
| CYP3A4 inhibitor | Yes | Medium |
| CYP2D6 inhibitor | No | High |
| CYP2C9 inhibitor | No | Medium |
| Clearance | 8.5 mL/min/kg | Low |

## Excretion
| Property | Prediction | Confidence |
|----------|------------|-------------|
| Renal clearance | 10% | Medium |
| Half-life | 48 hours | High |

## Toxicity
| Property | Prediction | Confidence |
|----------|------------|-------------|
| hERG inhibition | No | High |
| DILI | Concern | Medium |
| Ames mutagenicity | Negative | High |
| Carcinogenicity | Negative | Medium |
| Respiratory toxicity | No | Low |

## Recommendations
**Strengths**:
- Good oral bioavailability (65%)
- Brain penetration (BBB permeable)
- Low hERG risk

**Concerns**:
- DILI concern - monitor in preclinical studies
- CYP3A4 inhibition - potential DDIs

**Overall**: Good ADMET profile. Progress to in vivo PK.
```

## Property Ranges

### Drug-Likeness

| Rule | Pass Criteria |
|------|---------------|
| Lipinski Ro5 | ≤ 1 violation |
| Veber | RotB ≤ 10, PSA ≤ 140 Ų |
| Egan | LogP ≤ 5, PSA ≤ 131 Ų |
| MDDR | MW ≤ 600, LogP ≤ 5 |

### Absorption

| Property | Good | Moderate | Poor |
|----------|------|----------|------|
| HIA | >80% | 40-80% | <40% |
| Caco-2 | >10 | 1-10 | <1 |
| F30% | >70% | 30-70% | <30% |

### Distribution

| Property | Good | Moderate | Poor |
|----------|------|----------|------|
| VDss | 0.3-5 L/kg | <0.3 or >5 | Extreme |
| PPB | <90% | 90-95% | >95% |
| BBB | LogBB > 0.3 | -0.3 to 0.3 | < -0.3 |

### Toxicity Alerts

| Alert | Action |
|-------|--------|
| hERG inhibition | Cardiotoxicity risk |
| DILI positive | Hepatotoxicity risk |
| Ames positive | Mutagenicity risk |
| PAINS | Assay interference |
| Structural alerts | Investigate further |

## Running Scripts

```bash
# Full ADMET profile
python scripts/admet_predict.py --smiles "CC1=CC=C..." --full

# Batch prediction
python scripts/admet_predict.py --library compounds.sdf --output results.csv

# Specific properties
python scripts/admet_predict.py --smiles "..." --properties hERG,DILI,CYP

# Filter by criteria
python scripts/admet_filter.py --library compounds.sdf --rules lipinski,veber
```

## Requirements

```bash
pip install rdkit

# Optional for advanced models
pip install deepchem admet-x
```

## Reference

- [reference/admet-properties.md](reference/admet-properties.md) - Detailed property reference
- [reference/toxicity-alerts.md](reference/toxicity-alerts.md) - Toxicity alerts reference
- [reference/pk-models.md](reference/pk-models.md) - PK prediction models

## Best Practices

1. **Use multiple models**: Consensus predictions more reliable
2. **Check confidence**: Low confidence = experimental verification needed
3. **Consider chemistry**: Novel structures less reliable
4. **Iterative design**: Use predictions to guide synthesis
5. **Validate early**: Confirm key predictions experimentally

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Over-reliance on predictions | Experimental validation required |
| Ignoring confidence | Check model applicability domain |
| Single model only | Use consensus of multiple models |
| Ignoring chemistry | Novel scaffolds = uncertain predictions |
| Late-stage testing | Early ADMET screening saves time |

## Limitations

- **Models are approximate**: Errors common
- **Novel chemistry**: Less reliable for new scaffolds
- **In vitro-in vivo gap**: Predictions don't always translate
- **Species differences**: Human predictions based on animal data
- **Complex mechanisms**: Some toxicity not predicted
