---
name: biomysterybench
category: ai_collection
description: BioMysteryBench methodology for benchmarking LLM bioinformatics research capabilities on real-world datasets with consensus-based grading and path-independent evaluation
source: Anthropic Research - Evaluating Claude's bioinformatics research capabilities with BioMysteryBench (Apr 29, 2026)
tags: [bioinformatics, benchmarking, evaluation, science, llm-assessment, open-ended-problems]
---

# BioMysteryBench

## Overview

BioMysteryBench is a bioinformatics benchmark that tasks LLMs with analyzing real-world datasets to solve open-ended research problems. Unlike traditional QA benchmarks, it evaluates whether models can devise creative solutions to messy biological problems where multiple valid approaches exist.

## Benchmark Design (99 Questions)

### Three Key Challenges Addressed

1. **Multiple valid approaches** — In biology, many valid methodological approaches exist for the same question
2. **Subjectivity in noisy data** — Small analytical decisions can produce entirely different conclusions from the same biological datasets
3. **Human-unsolvable questions** — The most impactful research questions are ones humans have not yet answered

### The Tetrad of Unique Properties

1. **Method-agnostic** — Models get unrestricted tool access (pip, conda, NCBI, Ensembl). Graded only on final answer, not the path taken
2. **Objective ground-truth answers** — Derived from controllable data properties or orthogonally validated metadata (e.g., PCR-validated viral infection, crystal structure organism)
3. **Superhuman question generation** — Problems solvable in principle (validated by author notebooks showing signal exists) but may not be human-solvable
4. **Validation notebooks required** — Each question author submits a notebook proving signal exists in the data

### Data Sources
Primarily raw/minimally processed DNA/RNA sequencing data: WGS, scRNA-seq, methylation, ChIP-seq, metagenomics, Hi-C, plus some proteomics and metabolomics

### Example Questions
- Which human organ is this single-cell RNA-seq dataset from?
- What gene was knocked out based on RNA-seq data?
- From WGS, which samples are mother/father?
- Which bigWig files are ChIP vs input controls?
- Given H3K27ac ChIP-seq peaks, identify the cell type

### Human Baselining
- Up to 5 domain experts per question
- 76 questions classified as "human-solvable" (at least 1 human answered correctly)
- 23 questions classified as "human-difficult" (after removing 4 malformed/unsolvable ones)

## Key Findings

- Claude's scientific capabilities in biology improve rapidly across generations — current models perform on par with human experts on the human-solvable set
- Latest Claude generations solved many problems that human experts could not — Claude Mythos Preview achieved ~30% solve rate on human-difficult problems
- **Two primary strategies** Claude uses differently from humans:
  - **"Know-it-all"** — Leverages vast internal knowledge from hundreds of thousands of papers, combining structural biology, molecular profiles, and meta-analysis
  - **"Multi-method convergence"** — When uncertain, layers multiple analytical methods and combines evidence from different approaches
- **Reliability gap revealed by per-problem consistency analysis** (5 attempts each):
  - On human-solvable problems: Claude Opus 4.6 shows 86% of solved problems solved reliably (4+/5 attempts)
  - On human-difficult problems: only 44% of solved problems solved reliably; 44% are "brittle wins" (1-2/5 times — lucky reasoning paths)
- **Convergent validation**: Genentech/Roche's CompBioBench independently found Claude Opus 4.6 reaching 81% overall and 69% on their hardest questions

## Benchmark Challenges Addressed

| Challenge | Solution |
|-----------|----------|
| Multiple valid approaches | Path-independent, method-agnostic grading |
| Subjective research decisions | Objective ground-truth from controlled data properties |
| Human-unsolvable questions | Superhuman question generation with validation notebooks |
| Reliability assessment | Per-problem consistency analysis (5 attempts each) |

## Comparison to Other Benchmarks

- **MMLU-Pro, GPQA**: Expert-level QA questions; do not test research workflows
- **LAB-Bench**: Biology knowledge work; limited to reading/interpreting
- **BLADE, BixBench, SciGym**: Move closer to real workflows but still constrained
- **BioMysteryBench**: Open-ended, real-data, method-agnostic, superhuman-question research tasks

## Reusable Patterns

### Pattern: Method-Agnostic Benchmarking
Evaluate LLMs on final output correctness only, with unrestricted tool access during the task.

### Pattern: Superhuman Question Generation
Design questions whose answers are derived from objective properties of controlled data rather than human expert judgment — enables measuring capabilities beyond current human ability.

### Pattern: Per-Question Reliability Analysis
Run each question 5 times to distinguish between reliable solutions (4+/5 consistent) and brittle wins (1-2/5 lucky reasoning paths). The reliability gap is more informative than headline accuracy.

### Pattern: Validation Notebook Requirement
Each question must be accompanied by an author notebook proving the signal exists in the data, ensuring questions are solvable in principle.

### Pattern: Dual Strategy Analysis
Analyze model strategies qualitatively — distinguish between knowledge-based approaches (know-it-all) and method-based approaches (multi-method convergence) to understand how the model solves problems.

## Pitfalls

- For tasks neither humans nor models have solved, it is impossible to be certain whether they are impossible or just extraordinarily difficult
- Validation notebooks ensure signal exists but do not guarantee solvability from scratch
- Headline accuracy alone can be misleading without reliability analysis
- Curating high-quality real-world problems is expensive and time-intensive

## Activation Keywords
biomysterybench, bioinformatics, benchmarking, open-ended evaluation, consensus grading, science evaluation, path-independent, LLM assessment, biological datasets
