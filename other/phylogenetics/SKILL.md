---
name: phylogenetics
description: Workflow for multiple sequence alignment, tree inference, annotated tree visualization, and distance-based evolutionary comparison.
tool_type: python
primary_tool: IQ-TREE
---

# Phylogenetics

## Version Compatibility

Reference examples assume recent stable releases of the preferred tools, especially `IQ-TREE` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.


## Overview

Workflow for multiple sequence alignment, tree inference, annotated tree visualization, and distance-based evolutionary comparison.

## When To Use This Skill

- use when the task is tree building or evolutionary relationship analysis
- use when aligned sequences or genomes must be compared in phylogenetic context
- use when the user needs annotated trees or support metrics

## Quick Route

- If the input is raw or minimally processed data, start with validation and QC before any modeling.
- If the input is already processed, skip directly to the first workflow step that matches the user goal.
- If the user asks for a biological conclusion, always produce at least one QC or confidence artifact alongside the final result.


## Progressive Disclosure

- Read `references/technical_reference.md` when you need deeper tool-selection rules, environment adaptation notes, or extra validation guidance.
- Keep `SKILL.md` as the main execution path and load the reference file only when the task or failure mode needs the extra detail.


## Default Rules

- Prefer Python-first workflows unless the task explicitly requires something else.
- Keep intermediate and final outputs separated.
- Record software versions, reference builds, and key parameters when they affect interpretation.
- Favor reproducible tables and figures over one-off interactive-only outputs.

## Expected Inputs

- aligned sequences
- optional metadata
- model assumptions

## Expected Outputs

- phylogenetic trees
- annotated tree figures
- distance or support summaries

## Preferred Tools

- alignment tools
- tree inference tools
- ete toolkit-style plotting
- matplotlib

## Starter Pattern

```bash
mafft --auto input.fasta > aligned.fasta
iqtree2 -s aligned.fasta -m MFP -B 1000
```

## Workflow

### 1. Prepare alignment

Trim or mask poorly aligned regions and confirm sequence comparability.

### 2. Choose an inference strategy

Pick distance, maximum likelihood, or other tree approaches matched to the problem.

### 3. Assess support

Include bootstrap or comparable support metrics where relevant.

### 4. Annotate with metadata

Overlay sample metadata on trees for interpretation.

### 5. Export publishable trees

Save tree files plus readable static figures.


## Output Artifacts

- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
- `phylogenetic trees`
- `annotated tree figures`
- `distance or support summaries`


## Quality Review

- Confirm identifiers and metadata join correctly before modeling or summarizing.
- Generate at least one QC artifact before final biological interpretation.
- Keep raw or minimally processed inputs separate from transformed outputs.
- Review sample contamination, depth differences, and database choice before comparing communities.
- State clearly whether outputs are relative abundance, counts, or derived functions.

## Anti-Patterns

- building trees from poor-quality or incompatible alignments
- omitting support metrics on uncertain topologies
- over-interpreting branch differences without scale context

## Related Skills

- `Metagenomics`
- `Microbiome Amplicon`
- `Pathogen Epidemiological Genomics`

## Optional Supplements

- `etetoolkit`
