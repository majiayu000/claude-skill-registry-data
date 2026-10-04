---
name: rdkit
description: Use when an agent needs deterministic local cheminformatics for structure normalization, descriptors, substructure, stereochemistry, similarity, reactions, or conformers.
---

# RDKit

## Overview

This skill exposes lightweight local RDKit tooling through small CLI entrypoints.
Every script reads a request JSON file, writes a stable `result.json`, and can
echo the same top-level payload to stdout with `--json`.

The skill is fully local:
- no network access
- no ChemQA or DebateClaw runtime dependency
- structured JSON errors when RDKit is unavailable

## Command Pattern

```bash
python scripts/run_skill.py \
  --workspace-root . \
  --execution-cwd "$PWD" \
  --script skills/rdkit/scripts/<capability>.py -- \
  --request-json /path/to/request.json \
  --output-dir /tmp/<skill-out> \
  --json
```

`--output-dir` is required and is created automatically.

## Capabilities

- `canonicalize.py`: parse SMILES or InChI, sanitize, optionally strip atom maps, and return canonicalized structure data
- `descriptors.py`: formula, mass, charge, donor/acceptor counts, TPSA, logP, and compact molecule summary
- `functional_groups.py`: curated SMARTS matches for common functional groups and reactive handles
- `substructure.py`: SMARTS matching against one or more molecules
- `rings_aromaticity.py`: ring counts, ring sizes, aromaticity, fused-ring hints, and heteroaromatic features
- `stereochemistry.py`: chiral centers, specified vs unspecified stereochemistry, and double-bond stereo features
- `similarity.py`: Morgan fingerprint similarity ranking against supplied candidates
- `reaction_smarts.py`: reaction SMARTS validation and product generation
- `conformer_embed.py`: ETKDG embedding plus an explicitly selected `MMFF` or
  `UFF` optimization; the request must name the force field
- `conformer_mmff.py`: ETKDG embedding plus MMFF optimization, with an optional
  `MMFF94` or `MMFF94s` variant
- `conformer_uff.py`: ETKDG embedding plus UFF optimization

## Execution Rules

- Canonicalize raw external structures before downstream structural analysis.
- For NMR peak-count questions, use RDKit only for structure facts such as
  canonicalization, formula, ring systems, and stereochemistry. Do not look for
  or create graph-symmetry proton-count tooling; final NMR peak counts require
  manual spectroscopic interpretation.
- Use conformer scripts only when 3D geometry is relevant. Select the force
  field from the task or scientific protocol; never infer it from parameter
  availability and never substitute MMFF for UFF or UFF for MMFF.
- Set `num_conformers` and `random_seed` explicitly for every conformer request.
  The skill does not provide defaults or preferred values for either field.
- Read `routing-rules.md` for script selection and
  `references/contracts.md` for request and result contracts.
