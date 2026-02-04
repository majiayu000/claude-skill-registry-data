---
name: structure-search
description: |
  Structure-based similarity search and scaffold analysis for drug discovery.
  Use for lead hopping, scaffold morphing, and chemical space exploration.

  Keywords: similarity search, scaffold hopping, chemical space, fingerprint, Tanimoto
category: Computational Chemistry
tags: [structure, similarity, fingerprint, scaffold, chemical-space]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - rdkit
  - chembl
  - pubchem
---

# Structure Search Skill

Structure-based similarity search and scaffold analysis for drug discovery.

## Quick Start

```
/structure --query "CC1=CC=C(C=C1)CNC" --threshold 0.7
/scaffold-hop --input compound.sdf --scaffold-type murcko
/similar-compounds --chembl "CHEMBL210" --limit 20
```

## Similarity Methods

### Fingerprint-Based

| Fingerprint | Size | Best Use | Speed |
|-------------|------|----------|-------|
| Morgan | 2048 | General purpose | Fast |
| MACCS | 166 | General purpose | Very fast |
| RDKit | 2048 | Structural features | Fast |
| Atom pair | 2048 | Substructure | Medium |
| Topological torsion | 2048 | Conformations | Medium |

### Similarity Coefficients

| Coefficient | Range | Properties |
|-------------|-------|------------|
| Tanimoto | 0-1 | Most common, bounded |
| Dice | 0-1 | Similar to Tanimoto |
| Cosine | 0-1 | Vector-based |
| Tversky | 0-1 | Asymmetric |

## Scaffold Analysis

### Scaffold Types

| Type | Definition | Use Case |
|------|-----------|----------|
| Murcko | Core ring system | General |
| Bemis-Murcko | Rings + linkers | Drug-like |
| RECAP | Rings + functional groups | Medicinal chemistry |
| Graph | Only topology | Very generic |

### Scaffold Hopping

**Strategies**:
1. **Ring replacement**: Bioisosteric substitution
2. **Ring opening/closing**: Modify topology
3. **Linker modification**: Change connectivity
4. **Heteroatom swap**: N→O→S→C

## Output Structure

```markdown
# Structure Search Results

## Query Compound
**SMILES**: CC1=CC=C(C=C1)CNC
**Name**: Erlotinib
**Scaffold**: c1ccc(cc1)CNCC

## Similar Compounds (Tanimoto ≥ 0.7)

| Rank | ID | Name | Similarity | Scaffold Match |
|------|----|-----|------------|----------------|
| 1 | CHEMBL210 | Erlotinib | 1.00 | Yes |
| 2 | CHEMBL214 | Gefitinib | 0.89 | Yes |
| 3 | CHEMBL617 | Afatinib | 0.82 | Yes |
| 4 | CHEMBL12345 | Novel analog | 0.76 | No |
| 5 | CHEMBL98765 | Lead compound | 0.72 | Yes |

## Scaffold Analysis

### Murcko Scaffold

```
Query: c1ccc(cc1)CNCC (Quinazoline core)
```

### Known Compounds with This Scaffold

| Compound | Class | Status |
|----------|-------|--------|
| Erlotinib | 1st-gen TKI | Approved |
| Gefitinib | 1st-gen TKI | Approved |
| Afatinib | 2nd-gen TKI | Approved |
| Dacomitinib | 2nd-gen TKI | Approved |
| Osimertinib | 3rd-gen TKI | Approved |

### Scaffold Frequency

| Scaffold | ChEMBL Count | Use |
|----------|--------------|-----|
| Quinazoline | 2,456 | Kinase inhibitors |
| Pyrimidine | 3,789 | Various targets |
| Pyrrolopyrimidine | 456 | Selective kinases |

## Scaffold Hopping Opportunities

### Ring Replacements

| Original | Bioisostere | Rationale |
|----------|-------------|-----------|
| Benzene | Pyridine | Add H-bond acceptor |
| Benzene | Thiophene | Slightly larger, polarizable |
| Pyridine | Pyrimidine | Add H-bond acceptor |
| Phenyl | Cyclohexyl | Remove aromaticity |

### Novel Scaffolds

**Identified 3 novel scaffolds** with similar topology:

1. **Indazole core**: 3 compounds
2. **Pyrrolopyrimidine**: 5 compounds
3. **Imidazopyridazine**: 2 compounds

## Property Comparison

| Property | Query | Mean (Similar) | Range |
|----------|-------|----------------|-------|
| MW | 393 | 420 | 350-480 |
| LogP | 3.2 | 3.5 | 2.8-4.2 |
| HBD | 1 | 1.2 | 1-2 |
| HBA | 3 | 3.5 | 2-5 |
| PSA | 72 | 78 | 65-95 |

## Recommendations

1. **Explore indazole compounds**: Novel scaffold, good properties
2. **Monitor pyrrolopyrimidines**: Emerging scaffold
3. **Consider scaffold hopping**: If IP crowded
```

## Similarity Thresholds

| Application | Tanimoto | Interpretation |
|-------------|-----------|----------------|
| Identical | 1.0 | Same compound |
| Very similar | 0.9-1.0 | Same analog series |
| Similar | 0.7-0.9 | Same scaffold |
| Related | 0.5-0.7 | Similar structure |
| Distant | 0.3-0.5 | Some similarity |
| Unrelated | <0.3 | Different chemotypes |

## Running Scripts

```bash
# Similarity search
python scripts/structure_search.py --query "SMILES" --threshold 0.7

# Scaffold analysis
python scripts/scaffold_analysis.py --input compounds.sdf --type murcko

# Scaffold hopping
python scripts/scaffold_hop.py --input compound.sdf --output hops.sdf

# Chemical space mapping
python scripts/chemical_space.py --library compounds.sdf --pca
```

## Requirements

```bash
pip install rdkit pandas numpy scikit-learn

# Optional for visualization
pip install plotly seaborn matplotlib
```

## Reference

- [reference/fingerprints.md](reference/fingerprints.md) - Fingerprint reference
- [reference/scaffold-methods.md](reference/scaffold-methods.md) - Scaffold methods
- [reference/chemical-space.md](reference/chemical-space.md) - Chemical space analysis

## Best Practices

1. **Use appropriate thresholds**: 0.7 for similar compounds
2. **Consider scaffold**: Different scaffold may have similar activity
3. **Check properties**: Similar doesn't mean drug-like
4. **Validate experimentally**: In-silico similarity needs confirmation
5. **Use multiple methods**: Fingerprints + alignment for full picture

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| High similarity ≠ same activity | Check bioactivity |
| Ignoring stereochemistry | Use isomeric SMILES |
| Fingerprint bias | Try multiple fingerprint types |
| Scaffold blindness | Explicit scaffold analysis |
| Over-clustering | Appropriate threshold selection
