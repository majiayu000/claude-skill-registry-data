---
name: pyteomics-api-usage
description: Use when when you have polypeptide sequences and need to compute their
  monoisotopic or average mass, isotopic distribution patterns, or other physico-chemical
  properties; or when you need to parse and manipulate MS/LC-MS data, FASTA databases,
  or search engine output in a Python workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0234
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Pyteomics
  - pip
  - NumPy
  - pandas
  - lxml
  - SQLAlchemy
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- Pyteomics is a collection of lightweight and handy tools for Python
- Pyteomics supports recent versions of Python 3.
- pip install pyteomics
- numpy
- numpy <https://numpy.org/>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyteomics_cq
    doi: 10.1021/acs.jproteome.8b00717
    title: pyteomics
  dedup_kept_from: coll_pyteomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00717
  all_source_dois:
  - 10.1021/acs.jproteome.8b00717
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pyteomics-api-usage

## Summary

Use Pyteomics modules to programmatically calculate physico-chemical properties of polypeptides (mass, isotopic distribution, charge, pI) and access proteomics data formats. This skill enables reproducible, rapid prototyping of proteomics data analysis workflows in Python.

## When to use

When you have polypeptide sequences and need to compute their monoisotopic or average mass, isotopic distribution patterns, or other physico-chemical properties; or when you need to parse and manipulate MS/LC-MS data, FASTA databases, or search engine output in a Python workflow.

## When NOT to use

- Input sequences contain ambiguous or non-standard amino acids not recognized by Pyteomics' residue mass tables
- You need real-time or streaming mass calculations on massive datasets—Pyteomics is designed for offline analysis and prototyping, not high-throughput online prediction
- You require mass calculations for non-polypeptide molecules (small organic compounds, lipids, nucleic acids)—Pyteomics is peptide and protein focused

## Inputs

- list of polypeptide sequences (text file, one per line, or CSV format)
- MS or LC-MS data files
- FASTA database files
- search engine output files

## Outputs

- structured table (CSV or pandas DataFrame) with sequence, monoisotopic mass, and average mass
- isotopic distribution patterns
- charge and pI predictions
- chromatographic retention time predictions

## How to apply

Install Pyteomics via pip (or conda with bioconda) along with required dependencies (NumPy) and optional ones (lxml for XML parsing, pandas for tabular data, SQLAlchemy for Unimod access). Import the appropriate Pyteomics module—e.g., pyteomics.mass for monoisotopic and average mass calculation—and apply its functions to each polypeptide sequence. Pass the sequence string to the mass calculation function; it returns numeric mass values. Aggregate results (sequence, monoisotopic mass, average mass) into a structured output table (DataFrame or CSV) and validate that all sequences produced numeric outputs without NaN or negative values.

## Related tools

- **NumPy** (Core numerical dependency for Pyteomics mass and isotopic distribution calculations)
- **pandas** (Optional dependency for tabular aggregation and manipulation of mass calculation results and proteomics data files)
- **lxml** (Optional dependency for parsing XML-based proteomics data formats in Pyteomics modules)
- **SQLAlchemy** (Optional dependency used by pyteomics.mass.unimod for database-backed PTM and residue mass lookups)

## Examples

```
from pyteomics import mass; seqs = ['PEPTIDE', 'SEQUENCE']; masses = [(s, mass.calculate_mass(sequence=s), mass.calculate_mass(sequence=s, mass_type='average')) for s in seqs]; import pandas as pd; df = pd.DataFrame(masses, columns=['sequence', 'monoisotopic_mass', 'average_mass']); df.to_csv('peptide_masses.csv', index=False)
```

## Evaluation signals

- All input sequences produce numeric monoisotopic and average mass values with no NaN or Inf entries
- Mass values are positive and fall within expected biological ranges (typically 50–10000 Da for peptides)
- Output CSV or DataFrame schema matches input: one row per sequence with columns for sequence identifier, monoisotopic mass, and average mass
- No exceptions or import errors when loading pyteomics.mass module and running mass calculation on representative test sequences
- Isotopic distribution histograms show expected envelope pattern (monoisotopic peak tallest, isotopologues decreasing in intensity)

## Limitations

- Pyteomics uses standard IUPAC residue masses; post-translational modifications must be manually added or specified via chemical composition strings
- Accuracy of monoisotopic mass depends on correct sequence input and residue mass tables—ambiguous amino acids (B, Z, X) may not resolve correctly
- No built-in support for non-standard or chemically modified residues without explicit user definition
- Performance scales linearly with sequence length and number of sequences; not optimized for real-time or ultra-high-throughput applications

## Evidence

- [readme] Pyteomics provides modules for calculation of basic physico-chemical properties: "calculation of basic physico-chemical properties of polypeptides: mass and isotopic distribution, charge and pI, chromatographic retention time"
- [methods] Install via pip or conda with optional dependencies: "pip install pyteomics[XML]"
- [other] Workflow aggregates sequence and mass into structured table: "Aggregate sequence, monoisotopic mass, and average mass into a structured table (CSV or pandas DataFrame) and save to output file"
- [readme] Pyteomics is Python-based for reproducible analysis and prototyping: "One of the project's key features is Python itself, an open source language increasingly popular in scientific programming. The main applications of the library are reproducible statistical data"
