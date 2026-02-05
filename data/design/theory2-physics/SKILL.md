---
name: theory2-physics
description: Use when performing mathematical physics computations - Lie algebras, quantum chemistry, neural operators, theorem proving, or scientific validation. Provides guidance on Theory2 CLI usage, computational workflows, and verification methodology.
version: 1.0.0
---

# Theory2 Mathematical Physics Tooling

Master the Theory2 suite for mathematical physics computation.

## Quick Reference

All commands use the pattern:
```bash
/home/mikeb/theory2/.venv/bin/theory --json <group> <action> [options]
```

Always use `--json` for structured, parseable output.

## Module Selection Guide

| Task | Module | Key Commands |
|------|--------|--------------|
| Lie algebras, α⁻¹=137 | symbolic | `compute-e7-alpha`, `lie-algebra` |
| Calculus, equations | symbolic | `diff`, `integrate`, `solve` |
| Molecular energies | numerical | `quantum-chemistry --method=dft` |
| Quantum circuits | numerical | `quantum-circuit --circuit=bell` |
| PDE solving | ml | `solve-pde --pde-type=heat` |
| Operator learning | ml | `train-fno`, `train-e3nn` |
| Theorem proving | prove | `lean --statement="..."` |
| Cross-validation | verify | `cross-check --claim="..."` |
| DNA/RNA/protein | symbolic | `bio-sequence`, `bio-protein`, `bio-structure` |
| Graph algorithms | symbolic | `graph --operation=shortest_path` |
| Combinatorics | symbolic | `combinatorics --operation=catalan` |
| Discrete optimization | symbolic | `discrete-opt --problem=tsp` |

## Symbolic Mathematics

### Lie Algebra Computations

The E7 formula connects exceptional Lie algebras to fundamental physics:

```bash
# Compute α⁻¹ from E7 structure
theory --json symbolic compute-e7-alpha --verify

# Query individual properties
theory --json symbolic lie-algebra --type=E7 --query=dimension     # → 133
theory --json symbolic lie-algebra --type=E7 --query=rank          # → 7
theory --json symbolic lie-algebra --type=E7 --query=fundamental_rep  # → 56
```

Formula: α⁻¹ = dim(E7) + fund_rep/(2×rank) = 133 + 56/14 = 137

### Expression Operations

```bash
# Evaluate with substitution
theory --json symbolic eval --expr="(x+y)**2" --substitutions='{"x":1,"y":2}'

# Calculus
theory --json symbolic diff --expr="x**3 * sin(x)" --symbol=x
theory --json symbolic integrate --expr="exp(-x**2)" --symbol=x

# Equation solving
theory --json symbolic solve --expr="x**3 - 8" --symbol=x
```

## Numerical Physics

### Quantum Chemistry

Methods ranked by accuracy/cost:
1. **HF** (Hartree-Fock): Fastest, no correlation
2. **DFT** (B3LYP, PBE): Good balance
3. **CCSD**: Most accurate, expensive

```bash
# Water with DFT
theory --json numerical quantum-chemistry \
  --molecule="H2O" --method=dft --xc=b3lyp --basis=def2-svp

# Custom geometry
theory --json numerical quantum-chemistry \
  --molecule="O 0 0 0; H 0.757 0.587 0; H -0.757 0.587 0" \
  --method=ccsd --basis=cc-pVDZ
```

### Quantum Circuits

```bash
# Bell state measurement
theory --json numerical quantum-circuit --circuit=bell --shots=1024

# GHZ statevector
theory --json numerical quantum-circuit --circuit=ghz3 --statevector
```

## Physics Machine Learning

### Fourier Neural Operators

For learning PDE solution operators:

```bash
# Standard FNO
theory --json ml train-fno --modes=16 --width=64 --layers=4

# Memory-efficient
theory --json ml train-fno --modes=32 --width=128 --factorization=tucker
```

**Tucker factorization** reduces memory ~10x for large models.

### Physics-Informed Neural Networks

Solve PDEs without training data:

```bash
# Heat equation
theory --json ml solve-pde --pde-type=heat --alpha=0.01 --iterations=10000

# Poisson equation
theory --json ml solve-pde --pde-type=poisson --iterations=20000
```

### E3NN Equivariant Networks

For molecular systems respecting 3D symmetry:

```bash
theory --json ml train-e3nn --irreps-hidden="32x0e+16x1o+8x2e" --use-gates
```

## Bioinformatics & Molecular Biology

### Sequence Analysis

Work with DNA, RNA, and protein sequences using Biopython:

```bash
# Transcribe DNA to RNA
theory --json symbolic bio-sequence --sequence="ATGCGTACG" --operation=transcribe

# Translate DNA to protein
theory --json symbolic bio-sequence --sequence="ATGCGTACG" --operation=translate

# Reverse complement
theory --json symbolic bio-sequence --sequence="ATGCGTACG" --operation=reverse_complement

# GC content calculation
theory --json symbolic bio-sequence --sequence="ATGCGTACG" --operation=gc_content
```

### Protein Analysis

```bash
# Calculate molecular weight
theory --json symbolic bio-protein --sequence="MKTAYIAKQR" --operation=molecular_weight

# Compute isoelectric point
theory --json symbolic bio-protein --sequence="MKTAYIAKQR" --operation=isoelectric_point

# Predict secondary structure
theory --json symbolic bio-protein --sequence="MKTAYIAKQR" --operation=secondary_structure
```

### Structure Analysis

Load and analyze protein structures from PDB files:

```bash
# Parse PDB structure
theory --json symbolic bio-structure --pdb-id="1BNA" --operation=get_info

# Extract sequence from structure
theory --json symbolic bio-structure --pdb-id="1BNA" --operation=extract_sequence

# Calculate RMSD between structures
theory --json symbolic bio-structure --pdb-id="1BNA" --reference="1BNB" --operation=rmsd
```

## Combinatorics & Discrete Mathematics

### Graph Theory

Using NetworkX for graph algorithms:

```bash
# Create and analyze graph
theory --json symbolic graph --edges="[[0,1],[1,2],[2,0]]" --operation=shortest_path --source=0 --target=2

# Find connected components
theory --json symbolic graph --edges="[[0,1],[2,3]]" --operation=components

# Calculate centrality measures
theory --json symbolic graph --edges="[[0,1],[1,2],[2,0]]" --operation=centrality --method=betweenness

# Check graph properties
theory --json symbolic graph --edges="[[0,1],[1,2],[2,0]]" --operation=is_planar
```

### Enumeration

Compute combinatorial numbers and sequences:

```bash
# Catalan numbers
theory --json symbolic combinatorics --operation=catalan --n=10

# Bell numbers (partitions)
theory --json symbolic combinatorics --operation=bell --n=5

# Stirling numbers (first/second kind)
theory --json symbolic combinatorics --operation=stirling --n=5 --k=2 --kind=second

# Partition function
theory --json symbolic combinatorics --operation=partitions --n=10
```

### Optimization Problems

Solve classic discrete optimization problems:

```bash
# Traveling salesman problem
theory --json symbolic discrete-opt --problem=tsp --distances="[[0,10,15],[10,0,20],[15,20,0]]"

# Knapsack problem
theory --json symbolic discrete-opt --problem=knapsack \
  --weights="[2,3,4,5]" --values="[3,4,5,6]" --capacity=8

# Vertex cover
theory --json symbolic discrete-opt --problem=vertex_cover \
  --edges="[[0,1],[1,2],[2,3]]"

# Maximum flow
theory --json symbolic discrete-opt --problem=max_flow \
  --edges="[[0,1,10],[1,2,5],[0,2,15]]" --source=0 --sink=2
```

## Theorem Proving

### RobustLeanProver (Recommended)

Automatic proof search with intelligent tactic selection:

```bash
# Auto mode - tries 14+ tactics with parallel search
theory --json prove lean --statement="2 + 2 = 4"
theory --json prove lean --statement="∀ n : Nat, n + 0 = n"

# Specific tactics
theory --json prove lean --statement="2 + 2 = 4" --tactic=rfl
theory --json prove lean --statement="10 * 10 = 100" --tactic=decide
theory --json prove lean --statement="∀ x, x + 0 = x" --tactic=omega
```

### Tactic Tiers (Auto Mode)

| Tier | Tactics | Speed | Mode |
|------|---------|-------|------|
| fast | rfl, trivial, decide | ~100ms | Parallel |
| arithmetic | norm_num, omega, ring, simp | ~500ms | Parallel |
| search | simp_all, aesop, tauto | ~3s | Sequential |
| combined | simp; ring, norm_num; simp | ~10s | Sequential |

### Problem Type Detection

| Type | Example | Suggested Tactics |
|------|---------|-------------------|
| arithmetic | `2 + 2 = 4` | rfl, decide, norm_num |
| algebraic | `(a+b)^2 = ...` | ring (needs mathlib) |
| inductive | `List.length ...` | induction, cases |
| logical | `True`, `1 < 2` | decide, tauto |

### Proof Caching

- Successful proofs cached to `~/.cache/theory2/proofs/`
- Cache hits are instant (no REPL call)
- Use `--no-cache` to force re-computation

### Searching & Saving Proofs

```bash
# Save successful proof
theory --json prove lean --statement="3 + 3 = 6" --save

# Search proofs
theory --json prove search --query="continuous" --search-in=both

# List saved
theory --json prove list --verified-only
```

## Scientific Validation Workflow

### Hermeneutic Circle Methodology

Apply iterative refinement:

1. **Part→Whole**: Analyze components individually
2. **Whole→Part**: Use overall structure to inform details
3. **Iterate**: Refine understanding through cycles

### Prior Knowledge Integration

Before computing, search for relevant prior work:

```
mcp__plugin_task-memory_task-memory__search(query="<topic>")
```

### Multi-Method Verification

Always cross-validate critical results:

```bash
theory --json verify cross-check \
  --claim="alpha_inv=137" \
  --methods="symbolic,numerical,experimental" \
  --tolerance=0.001
```

### Documentation

Record for reproducibility:
- Method and parameters used
- Computational environment
- Reference values compared against
- Uncertainty quantification

## MCP Tools

The plugin provides MCP tools for direct invocation:

- `theory2_symbolic_compute_e7_alpha`
- `theory2_symbolic_lie_algebra`
- `theory2_symbolic_eval/simplify/solve/diff/integrate`
- `theory2_numerical_quantum_chemistry`
- `theory2_numerical_quantum_circuit`
- `theory2_ml_train_fno/train_e3nn/solve_pde`
- `theory2_prove_lean/search`
- `theory2_verify_cross_check`

## Agents

- **physics-solver**: Autonomous multi-step problem solving (physics, ML, bioinformatics)
- **physics-verifier**: Cross-validation and verification
- **theorem-prover**: Automated Lean 4 theorem proving with RobustLeanProver
- **bio-analyzer**: Sequence analysis, protein structure, and molecular biology workflows
- **graph-solver**: Graph algorithms and discrete optimization problems

## Best Practices

1. **Always verify**: Use cross-check for important results
2. **Document provenance**: Record methods, parameters, references
3. **Search first**: Check task memory for prior relevant work
4. **Iterate**: Apply hermeneutic refinement to deepen understanding
5. **Quantify uncertainty**: Report tolerances and error bounds
