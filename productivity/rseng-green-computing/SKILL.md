---
name: rseng-green-computing
description: >-
  Covers the environmental footprint of research computing: measuring and
  reporting energy use and carbon emissions of computations (CodeCarbon),
  reducing them through efficient code, right-sized hardware and carbon-aware
  scheduling (CATS), the GREENER principles and the Software Carbon Intensity
  metric. Use when the user asks about the carbon or energy cost of their
  computations, wants to make workloads greener, mentions sustainability of
  computing, CodeCarbon, CATS or the Software Carbon Intensity metric. Use
  PROACTIVELY when planning large training runs, simulations or
  parameter sweeps - footprint measurement is worthless retrospectively.
  (Keeping the software project itself alive is
  rseng-maintenance-sustainability; making code faster is
  rseng-performance-profiling.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Environmentally sustainable research computing

Research computing has a real carbon footprint - large simulations,
ML training runs and always-on services consume energy at a scale
funders and institutions increasingly ask about. The GREENER
principles for computational science frame the practice: Governance,
Responsibility, Estimation, Energy and embodied impacts, New
collaborations, Education and Research. For an agent the working core
is: measure first, reduce second, schedule smart, report honestly.

## Measure before optimizing

Never guess at footprint - estimate it:

- CodeCarbon instruments Python code with a few lines (or a CLI
  wrapper) and estimates energy plus location-adjusted CO2e; add it
  to representative runs, not every run.
- For non-Python or cluster workloads, estimate from job accounting
  (CPU/GPU hours x hardware power draw x facility PUE x grid carbon
  intensity) and state the assumptions.
- Record estimates alongside results the same way runtimes are
  recorded, so the cost of a paper's computations is reportable.

The Software Carbon Intensity (SCI) specification (an ISO standard)
gives a defensible formula when a formal number is needed:
operational plus embodied emissions per functional unit.

## Reduce

Order interventions by leverage, and quantify the win when possible:

1. Compute less: cache intermediate results, avoid re-running
   unchanged pipeline stages (rseng-workflows), kill zombie jobs,
   right-size parameter sweeps before launching them.
2. Compute efficiently: profile first (rseng-performance-profiling) -
   a 5x speedup is usually a ~5x energy cut; use appropriate
   precision; prefer vectorized/compiled paths in hot loops
   (rseng-language-guides).
3. Match hardware to the job: GPUs are more energy-efficient than
   CPUs for the workloads that suit them (rseng-gpu-computing) and
   wasteful for the ones that do not; do not reserve more nodes,
   memory or walltime than the job uses.
4. Store less: data has a footprint too - prune intermediates,
   compress archives, apply retention rules (rseng-data-management).

## Schedule smart

Grid carbon intensity varies by hours and by region. Carbon-aware
scheduling shifts flexible batch work to cleaner windows:

- CATS (Climate-Aware Task Scheduler) picks the lowest-carbon start
  time for a job of a given duration on UK-grid data; the same
  delay-tolerant principle applies anywhere batch work is flexible.
- Cloud users can choose lower-carbon regions for flexible workloads;
  cluster users can prefer off-peak windows where the operator
  exposes them.

## Report and advocate

- Include a brief compute-footprint statement in papers and READMEs
  for compute-heavy projects (estimated kWh/CO2e and the estimation
  method) - normalize the practice.
- When proposing CI pipelines, keep them lean: cache dependencies,
  skip redundant matrix entries, avoid scheduled jobs nobody reads
  (rseng-ci-cd).
- Educate while doing: a measured number ("this sweep emitted an
  estimated 12 kg CO2e") lands better than generic advice.

## Working with this skill

This skill is source-independent: its authority is the GREENER
principles, the SCI specification and the tool documentation linked
below.

Learn more (verified):
  - https://www.nature.com/articles/s43588-023-00461-y - GREENER
    principles for environmentally sustainable computational science
  - https://codecarbon.io - CodeCarbon energy/CO2e estimation
  - https://greensoftware.foundation/standards/sci/ - Software Carbon
    Intensity specification
  - https://github.com/GreenScheduler/cats - Climate-Aware Task
    Scheduler

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - lean pipelines waste less compute
- rseng-data-management - storage retention has a footprint
- rseng-gpu-computing - matching hardware to workload efficiency
- rseng-hpc-computing - right-sized resource requests save energy
- rseng-performance-profiling - speedups cut energy roughly proportionally
- rseng-workflows - caching avoids recomputing pipeline stages

<!-- related-skills:end -->
