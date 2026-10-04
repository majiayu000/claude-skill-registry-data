---
name: gale-v2-refactor
description: >
  Use when working on the gale v2 consolidation/refactor — folding the accumulated CPU+GPU DG
  optimization work into user-friendly building blocks behind src/sim/'s Sim/Device abstraction while
  defending the measured performance edge. Carries the working-discipline rules distilled from the
  optimization sessions (the mistakes that got corrected repeatedly), the measurement gotchas, and the
  v2 design rails. Pair with the gale-gpu-perf skill for the profiling gate. Read docs/gale-v2-refactor.md
  for the full design + benchmark ledger.
---

# gale v2 refactor — discipline, tools, direction

This is a **serious refactor**: consolidate the perf work into clean building blocks **without losing
the numbers**. The design + the benchmark baselines live in `docs/gale-v2-refactor.md` — read it first.
This skill exists mostly to stop the recurring mistakes. Take the working-discipline section literally.

## Working discipline — the mistakes that kept happening (don't repeat them)

These are real corrections from the optimization sessions. Each cost time. Internalize the rule, not
just the example.

1. **Iteration counts are language-independent. NEVER cross-compare them across implementations unless
   the ALGORITHM is identical.** A correct Chebyshev-MG-PCG converges in the same iterations in CUDA or
   cuda-oxide; if a C++ prototype gives 16 and the Rust gives 24, that is **not** a language/cuda-oxide
   effect — it's a *different algorithm* (here: h-MG vs p-MG) or a bug. Comparing C++-iters to Rust-iters
   and blaming the backend wasted a whole analysis. Compare ms/step (same language, same hardware) for
   perf; compare iters only within one algorithm.

2. **A prototype is a "faithful model" only if it runs the SAME algorithm — a coincidental scalar match
   does not prove it.** A C++ *h-multigrid* prototype was called a faithful model of the production
   *p-multigrid* because their Jacobi iteration counts happened to match (29≈28); its 45% win was
   projected onto production, which actually got ~6%. One matching number ≠ same algorithm. Before
   projecting a prototype's win, confirm the prototype's *structure* matches production.

3. **Never say a kernel is "at the floor" / "nothing left" without an ncu number showing the bound and
   what's moving the bytes.** Claiming `op_cheby` was "at the bandwidth floor" was wrong — it was
   BW-bound on the *smoother fields* (b/dinv/dvec), not the matvec, and mixed precision was a ~1.5×
   lever. "It works" ≠ done. "It works + here are the profile numbers (DRAM%, occupancy, the bytes)" =
   done. If you're about to write "we're near optimal," profile it instead.

4. **Measure; don't project. And measure WALL-CLOCK, not API/launch counts.** Don't hedge with "this is
   probably ~X%." Run it. And note: a while-graph A/B that *changed API counts* showed **no wall-clock
   win** — API counts are not performance. An `ncu --graph-profiling graph` number on a while-graph
   kernel is a measurement *artifact*, not a measurement (§ below).

5. **A/B in the PRODUCTION path (the device-resident while-graph), not standalone.** The arith matvec
   was bit-perfect in the standalone `op_profile` but broke the Neumann pressure solve (46× slower) only
   in the resident path — the arithmetic-neighbour opt had silently dropped the per-face BC metadata. A
   standalone win can be a production regression. Validate where it ships.

6. **For GPU perf work, "C++" means CUDA/C++ (GPU).** When asked to prototype "in C++", prototype on the
   GPU. The CPU is only the cheap way to answer an *algorithm/iteration-count* question (e.g. "does FP32
   smoothing hold the iteration count?") — not a perf prototype.

7. **Push to the measured answer; but surface genuine forks honestly with the data.** Don't stop short
   or checkpoint to avoid work. *Do* surface a real architecture fork (e.g. "the win needs h-multigrid,
   a separate solver") with the measurement that motivates it — that's not hedging, it's the user's call
   to make. The test: are you stopping because you're unsure (then measure) or because there's a genuine
   large speculative investment with a real decision (then present the data + recommend)?

8. **Be honest about what a commit bundles and what you left alone.** poisson.rs carried prior
   uncommitted work mixed in-file; say so. Don't sweep unrelated WIP into a feature commit silently.

## Build & measurement gotchas (these bite every session)

- **`cargo oxide build --arch sm_70`** for the Titan V, OR `CUDA_OXIDE_TARGET=sm_70` when running the
  bare binary. cuda-oxide embeds kernels as NVVM-IR and JIT-links the cubin at runtime for
  `CUDA_OXIDE_TARGET` (**defaults to sm_120**). A plain `cargo oxide build` + running
  `target/release/<bin>` directly → `DriverError(209) "no kernel image available"` — that's the
  wrong-arch cubin, **not** a perms/CUPTI problem. `cargo oxide run` auto-detects and injects sm_70;
  the bare binary (what profilers run) does not.
- **ncu CANNOT profile kernels inside conditional (while/if) CUDA graphs** — its per-kernel numbers are
  artifacts. To profile a solve kernel: take it **out of the graph** (`RVP_NOGRAPH=1` /
  `GpuResidentVe::with_while_graph(false)`, or `op_profile`) and ncu the plain launch. Use
  **nsys `--cuda-graph-trace=node`** for the in-situ which-kernel-dominates breakdown (timing only, no
  HW counters). See the gale-gpu-perf skill for the full gate.
- Run **`cargo oxide`**, not `cargo-oxide` (env/cache differ — a stale backend is used silently).
- The mandatory gate before calling GPU work done (from gale-gpu-perf): RULE ZERO (no per-step host↔dev
  sync — nsys memcpy/sync counts must NOT scale with steps×stages), the kernel's bound via ncu,
  before/after ms reported as a number, correctness regression still green.

## v2 design rails (the direction — full detail in docs/gale-v2-refactor.md)

- **Three residency levels.** L0 CPU (host loop, oracle). L1 GPU host-orchestrated (device-resident
  *state*, host calls `step()` per step — a *prototype*; any per-step readback violates RULE ZERO). L2
  GPU fully device-resident (whole step a captured graph, whole loop a while-graph, **no host per-step
  work** — the *production* bar for sweeps). `GpuDualSplitting` is L1 via `StateIntegrator`;
  `GpuResidentVe/Ns` is L2 and **cannot** be a per-step `StateIntegrator`.
- **Sim-as-spec, Device-as-compiler.** `Sim` is a declarative physics spec; `Device::plan(spec)` picks
  the backend + the highest residency level the spec supports. Add a `ResidentIntegrator` seam
  (`run_resident(state, nsteps, io_every, writers)`) for L2 alongside the `StateIntegrator` seam for L1.
- **Dual-impl building blocks.** Each Term/StageHook/Updater/Writer carries a CPU impl + optionally a
  device-resident (kernel) impl. Closure-only blocks cap a sim at L1; giving them kernel twins is what
  lets a sim reach L2.
- **`gpu` cargo feature (default-on).** Gates the optional `gale-gpu` dep + every `Cuda` arm. Without it:
  CPU-only, no cuda-oxide. With it: the user builds via cuda-oxide (like nvcc). No silent CPU fallback
  for `Device::Cuda`.
- **The `Device` enum exists but is currently dormant** (never read by `Simulation::run`); the real seam
  today is `StateIntegrator`, and GPU is reached by *manually* constructing `GpuDualSplitting`. The
  refactor makes `Device` the compiler that resolves this.

## Order of operations (don't skip step 1)

1. **Freeze the §4 baselines into `benches/` first** (the ms/step·ms/kernel·ms/iter triplet + the
   RULE-ZERO check). Refactoring without a regression baseline is how the perf edge silently dies.
2. Feature-flag the GPU. 3. `Device::plan` + integrator factory (L1, already exists). 4. The
   `ResidentIntegrator` seam (L2 — where the ~1.5× lives). 5. Dual-impl the hooks/updaters. 6.
   examples/benches/tests reorg. 7. Autotuning hooks (swappable scalar type + launch configs).

Each step ends **green on the regression triplet**. A >~5% move without an explanation is a bug.

## Magic-number levers worth autotuning (don't hand-tune per GPU)
block-size / elements-per-block (biggest knob, hardware-specific), mixed-precision toggle (FP32 vs FP64
smoother), coarse-iteration count + Krylov tolerance, the hp hierarchy balance, graph-vs-no-graph. Make
the scalar type and launch configs swappable so an autotuner has something to turn. The *algorithm*
(hp-MG + Chebyshev + restructured matvec + residency) is portable and good; new-hardware work is mostly
autotuning + two measured investigations (FP64 tensor-core contractions on A100+, mixed-precision
iterative refinement for FP64-weak parts).
