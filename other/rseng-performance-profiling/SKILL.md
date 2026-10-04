---
name: rseng-performance-profiling
description: >-
  Covers making research code faster with evidence: profiling before
  optimizing (py-spy and language-native profilers), interpreting hotspots,
  choosing optimizations by measured payoff, benchmark regression tracking
  with airspeed velocity (asv), and scaling measurements. Use when the user
  says their code is slow, asks to optimize or speed something up, wants
  benchmarks or performance regression tests, or before recommending rewrites,
  parallelism or GPUs on performance grounds.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Performance profiling and optimization

The cardinal rule: never optimize unprofiled code. Intuition about
where research code spends time is wrong often enough that acting on
it wastes effort and adds complexity to the wrong places. The
discipline is a loop: measure, find the dominant cost, fix only
that, measure again, stop when it is fast enough for the science.
"Fast enough" is a research judgment - a one-off analysis needs no
tuning; a per-particle inner loop run for months justifies serious
work.

## Profile first

- Whole-program view: a sampling profiler (py-spy for Python:
  `py-spy top --pid` on a live process or `py-spy record` for a
  flame graph) shows where time actually goes with negligible
  overhead and no code changes. Language-native equivalents: perf
  (compiled code), Rprof (R), @profile/BenchmarkTools (Julia).
- Line/function view once a hotspot is known: cProfile+snakeviz,
  line-profiler, or the IDE's profiler.
- Memory matters separately: allocation churn and swapping look like
  CPU slowness; profile memory when RSS grows or the machine swaps.
- Profile REPRESENTATIVE inputs at meaningful scale - toy inputs
  have different hotspots than production ones.

Report findings as fractions ("68% of runtime in distance_matrix"),
not feelings; the fraction bounds the possible speedup (Amdahl's
law) and justifies - or kills - the optimization.

## Optimize in payoff order

1. Algorithmic: a better algorithm or data structure beats any
   micro-optimization; check complexity before code details.
2. Do less: cache repeated computation, hoist work out of loops,
   short-circuit, avoid recomputing unchanged pipeline stages
   (rseng-workflows).
3. Use optimized building blocks: vectorized NumPy/BLAS operations,
   compiled library routines - most scientific speedups come from
   replacing interpreted loops with library calls
   (rseng-language-guides).
4. Compile the hotspot: Numba/Cython/C extension for the proven hot
   function only.
5. Parallelize last, and match the tool to the shape: threads/
   processes on one node, job arrays or MPI on clusters
   (rseng-hpc-computing), GPUs for data-parallel numeric work
   (rseng-gpu-computing), distributed frameworks for larger-than-
   memory data (rseng-big-data-processing).

Preserve correctness at each step: run the tests
(rseng-testing) after every optimization, with numerical tolerances
where results legitimately differ (bit-identical is often the wrong
bar - rseng-numerical-accuracy).

## Keep it fast: benchmark tracking

One-off optimization decays; regressions arrive silently in
innocent-looking commits. airspeed velocity (asv) runs a benchmark
suite across commits, tracks results over time and flags
regressions - the performance analogue of a test suite. Start small:
benchmark the 3-5 operations users actually wait on, wire the run
into CI or a scheduled job (rseng-ci-cd), and treat an unexplained
regression like a failing test.

For quick comparisons during work, timeit/hyperfine with repeated
runs and reported variance beat single stopwatch numbers; pin the
environment (rseng-reproducible-environments) so timings compare
across machines honestly - and record the hardware in any published
benchmark.

## Scaling measurements

Before requesting bigger allocations, measure scaling: run the same
problem at 1, 2, 4, 8 workers (strong scaling) or grow the problem
with workers (weak scaling), and plot efficiency. Recommending more
hardware without a scaling curve is guesswork; the curve also feeds
honest resource requests (rseng-hpc-computing) and energy accounting
(rseng-green-computing).

## Working with this skill

This skill is source-independent: its authority is the profiler and
benchmark-tool documentation linked below and standard performance
engineering practice.

Learn more (verified):
  - https://github.com/benfred/py-spy - sampling profiler for Python
  - https://github.com/airspeed-velocity/asv - benchmark regression
    tracking
  - https://github.com/sharkdp/hyperfine - hyperfine command-line
    benchmarking

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-big-data-processing - memory-bound escalation path
- rseng-ci-cd - benchmark regression tracking in CI
- rseng-gpu-computing - GPU port only after profiling evidence
- rseng-green-computing - speedups cut energy proportionally
- rseng-hpc-computing - scaling curves before big allocations
- rseng-numerical-accuracy - tolerances when optimizations shift results

<!-- related-skills:end -->
