---
name: compound-profile
description: |
  Generate comprehensive compound profiles including structure, properties,
  bioactivity, and development status. Use for drug analysis, SAR studies,
  and competitive profiling.

  Keywords: compound, drug, molecule, structure, SMILES, bioactivity, IC50
category: Compound Analysis
tags: [compound, drug, structure, bioactivity, chembl]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - chembl-database
  - pubchem-database
  - drugbank-database
---

# Compound Profile Skill

Comprehensive compound analysis for drug discovery and medicinal chemistry.

## Quick Start

```
/compound erlotinib
/compound-profile CC1=CC=C(C=C1)CNC(=O)C1=NC=C(C=C1)N
Analyze osimertinib properties and bioactivity
Compare gefitinib, erlotinib, afatinib profiles
```

## What's Included

| Section | Description | Data Source |
|---------|-------------|-------------|
| Basic Info | Name, type, status, company | ChEMBL, DrugBank |
| Structure | SMILES, InChI, molecular weight | PubChem, ChEMBL |
| Properties | LogP, HBD, HBA, TPSA, RO5 | Calculated, PubChem |
| Bioactivity | Target affinity, IC50, Ki | ChEMBL, BindingDB |
| Development | Phase, indications, status | Drugs@FDA |
| Similar Compounds | Structure similarity search | ChEMBL |
| Safety | Known toxicity, warnings | SIDER, PubChem |

## Output Structure

```markdown
# Compound Profile: Erlotinib

## Executive Summary
Erlotinib is a first-generation EGFR TKI approved for NSCLC (2004).
Key characteristics: Oral bioavailability, good brain penetration,
resistance mutations limit long-term efficacy.

## Basic Information
| Field | Value |
|-------|-------|
| Name | Erlotinib |
| Brand Names | Tarceva |
| ChEMBL ID | CHEMBL880 |
| Type | Small molecule |
| Class | Kinase inhibitor |
| Status | Approved |
| Approval Year | 2004 |
| Company | Astellas (OSI) |
| Indications | NSCLC, pancreatic cancer |

## Structure & Properties
**SMILES:** `COc1cc2nc(Nc3ccc(Oc4ccc(O)cc4)cc3)nc2cc1OC`

| Property | Value | Rule of 5 Check |
|----------|-------|----------------|
| MW | 393.4 Da | ✓ (<500) |
| LogP | 3.1 | ✓ (<5) |
| HBD | 1 | ✓ (≤5) |
| HBA | 7 | ✓ (≤10) |
| TPSA | 76.3 Ų | ✓ (<140) |
| Rotatable Bonds | 6 | |

## Bioactivity

| Target | Type | Affinity | Units |
|--------|------|----------|-------|
| EGFR | IC50 | 0.5 | nM |
| ERBB2 | IC50 | 1200 | nM |
| LCK | IC50 | 5 | nM |

## Development History
| Year | Milestone |
|------|-----------|
| 2004 | FDA Approval (NSCLC) |
| 2005 | EMEA Approval |
| 2010 | Pancreatic cancer approval |
| 2011 | Generic launch (US) |

## Similar Compounds
| Compound | Similarity | Difference |
|----------|------------|------------|
| Gefitinib | 85% | Different core scaffold |
| Afatinib | 72% | Irreversible binder |
| Osimertinib | 68% | 3rd-gen, mutant-selective |
| Icotinib | 82% | China-approved analog |

## Safety Profile
**Common AEs:** Rash, diarrhea, fatigue, anorexia
**Boxed Warning:** Interstitial lung disease
**Contraindications:** Hypersensitivity to erlotinib

## Patent Status
| Patent | Number | Expiry |
|--------|---------|--------|
| Base patent | US5747498 | 2019 (expired) |
| Formulation | US6943129 | 2020 |
| Method of use | US6900221 | 2021 |
```

## Examples

### By Name
```
/compound erlotinib
/compound-profile sotorasib
```

### By Structure
```
/compound "CC1=CC=C(C=C1)CNC(=O)C1=NC=C(C=C1)N"
/compound-profile SMILES
```

### Comparison
```
Compare compounds erlotinib, gefitinib, afatinib
Analyze bioactivity across EGFR inhibitors
```

### Property Analysis
```
/compound erlotinib --focus properties
Analyze drug-likeness of this compound
Check Lipinski rule of 5 violations
```

## Running Scripts

```bash
# Fetch compound by name
python scripts/fetch_compound_data.py erlotinib --output compound.json

# Fetch by SMILES
python scripts/fetch_compound_data.py --smiles "CC1=CC=C..." -o data.json

# Similarity search
python scripts/fetch_compound_data.py --similar CHEMBL880 --threshold 0.7

# Bioactivity summary
python scripts/fetch_compound_data.py erlotinib --bioactivity -o activity.json

# Structure search
python scripts/fetch_compound_data.py --scaffold quinazoline --limit 20
```

## Requirements

```bash
pip install requests pandas rdkit
```

## Additional Resources

- [ChEMBL API Reference](reference/chembl-api.md)
- [PubChem API](reference/pubchem-api.md)
- [Property Calculation](reference/properties.md)

## Best Practices

1. **Use standard names**: Generic names preferred over brand
2. **Verify ChEMBL ID**: Most reliable identifier
3. **Check bioactivity**: Cross-reference multiple sources
4. **Analog analysis**: Use similarity searches for SAR
5. **Validate SMILES**: Check structure validity

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Name ambiguity | Use ChEMBL ID when possible |
| Stereochemistry | SMILES may not capture isomerism |
| Outdated data | Check multiple sources |
| Salt forms | API may have multiple entries |
| Tautomerism | Different SMILES for same structure |
