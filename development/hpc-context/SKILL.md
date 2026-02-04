---
name: hpc-context
description: SLURM and HPC guidance for Mycelia benchmarks and large-scale analysis
---

# Mycelia HPC Context

Guidance for running Mycelia on HPC systems with SLURM.

## Benchmark Commands

Local small/medium/large benchmarks:
```bash
julia --project=. benchmarking/benchmark_runner.jl small
julia --project=. benchmarking/benchmark_runner.jl medium
julia --project=. benchmarking/benchmark_runner.jl large
```

SLURM submission (resource-intensive):
```bash
sbatch benchmarking/run_all_benchmarks.sh
```

## Key Directories

- `benchmarking/` - Heavy benchmark scripts
- `results/` - Generated artifacts
- `ci/hpc/` - HPC-specific CI configuration

## Resource Considerations

- Use memory estimation utilities from `utility-functions.jl` for large-scale analyses
- Keep external tool calls isolated in helpers under `src/`
- Avoid committing generated outputs or large files
- Note external tool or dataset requirements explicitly

## Portability

- Use `joinpath` for all file paths
- Test on multiple environments when possible
- Document any HPC-specific requirements
- Consider job scheduler compatibility (SLURM, PBS, etc.)

## Tutorial/Benchmark Guidelines

- Do NOT add generally useful functions in `tutorials/`, `test/`, or `benchmarking/`
- If a helper is broadly useful, add it under `src/` and call from tutorial
- Tutorials demonstrate core Mycelia functionality
- Avoid defining new helper functions except true one-offs
- Prefer Rhizomorph graph/assembly functionality over legacy base-graph APIs
