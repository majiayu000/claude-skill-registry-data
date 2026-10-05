---
name: rnaeval
description: Use when evaluating the free energy (kcal/mol) of an RNA secondary structure, calculating co-folding energies for two RNA strands, or analyzing consensus structures from multiple sequence alignments.
disable-model-invocation: true
user-invocable: true
---

# rnaeval

## Quick Start

- **Command:** `RNAeval [OPTIONS] [<input>]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/RNAeval`
- **Full reference:** See `references/help.md` for complete options and details

## When To Use This Tool

- Use `RNAeval` when you already have a sequence plus a proposed dot-bracket structure and want its free energy scored.
- It is the right tool for rescoring externally generated structures, checking cofold energies for two strands separated by `&`, or auditing loop-by-loop contributions with `-v`.
- Use `--msa` when the input is a Stockholm multiple-sequence alignment plus a consensus structure.
- Do not use it to predict structures from sequence alone; this program evaluates a supplied structure rather than searching for one.

## Common Patterns

```bash
# Evaluate one sequence/structure pair from stdin
printf 'GGGAAAUCC\n(((...)))\n@\n' | RNAeval

# Print detailed loop-energy contributions
printf 'GGGAAAUCC\n(((...)))\n@\n' | RNAeval -v

# Evaluate a two-strand cofold structure marked with &
printf 'GGGA&AAAUCC\n(((.&.)))\n@\n' | RNAeval

# Read sequence/structure input from a file
RNAeval -i structures.txt
```

## Recommended Workflow

1. Prepare input with RNA sequence and dot-bracket structure (one per line or in file)
2. Run `RNAeval -i <inputfile>` or pipe input via stdin
3. Review energy output in kcal/mol; use `-v` for per-loop breakdown if needed
4. For alignments, use `--msa` with Stockholm 1.0 format input

## Guardrails

- Input must include both sequence and structure; this tool does not predict structures
- End batch input with a line containing only `@` or ensure proper EOF handling
- Ensure sequences use `U` not `T` (or use `--noconv` to disable auto-conversion)
