---
name: kinfold
description: Use when simulating stochastic folding kinetics of single-stranded nucleic acids, computing first passage times between structures, or analyzing RNA/DNA folding trajectories.
disable-model-invocation: true
user-invocable: true
---

# kinfold

## Quick Start

- **Command**: `Kinfold [OPTION]... < input.fa`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/Kinfold`
- **Full reference**: See `references/help.md` for complete options and details

## When To Use This Tool

- Simulate stochastic RNA/DNA folding trajectories instead of only equilibrium structures.
- Estimate first-passage or recurrence times between structures.
- Explore co-transcriptional growth effects with chain-extension parameters.
- Output only local minima or low-energy states from kinetic runs.

## Common Patterns

```bash
# 1) Run multiple stochastic trajectories from an open chain
printf 'GGGAAAUCC\n' | Kinfold --num=100 --time=1000
```

```bash
# 2) Use explicit start and stop structures for first-passage simulations
printf 'GGGAAAUCC\n.........\n(((...)))\n' | Kinfold --start --stop --fpt
```

```bash
# 3) Simulate co-transcriptional growth and print local minima only
printf 'GGGAAAUCC\n' | Kinfold --grow=5 --glen=10 --lmin
```

## Recommended Workflow

1. Prepare input file with sequence (required), start structure (if using `--start`), and stop structures (if using `--stop`)
2. Set simulation parameters: temperature (`-T`), max time (`--time`), number of trajectories (`--num`), and random seed (`--seed`) as needed
3. Configure energy model options: dangling ends (`-d`), multiloop energies (`--logML`), and move set constraints (`--noShift`, `--noLP`)
4. Run simulation and interpret output: first passage times (default), local minima (`--lmin`), or structures within energy cutoff (`--cut`)

## Guardrails

- Input file must start with sequence line; start/stop structures require `--start`/`--stop` flags respectively
- Default simulation runs 1 trajectory for 500 time units; increase `--num` and `--time` for adequate sampling
- Use `--noLP` to avoid biologically unrealistic structures with isolated base pairs
