---
name: gale-gpu-perf
description: MANDATORY performance discipline whenever writing or modifying GPU code in gale-gpu — new/changed CUDA `#[kernel]`s, host launch wrappers, or wiring a GPU op into a per-step/per-stage integrator path. Enforces persistent handles, device residency, and an ncu/nsys/dmon profiling gate BEFORE the code is declared done. Use it every time GPU code changes; do not skip the profile step.
---

# gale-gpu performance discipline

GPU simulations in gale must be **fast — faster than anyone else's**. A correct-but-slow kernel is a
defect, not a milestone. We have repeatedly shipped GPU code that was functionally correct but left
the GPU near-idle (one-shot module loads, per-step host↔device ping-pong). That stops here: **every
change to GPU code goes through this checklist before it is called done.**

This is not optional and not "later." If you wrote a kernel or a launch wrapper, you profile it in
the same work session.

## Production GPU code = 100% device-resident, GPU-self-driving (the bar for parameter sweeps)

"Production" here means **ready to run parameter sweeps**. The bar for that, set by the user, is
absolute: **from simulation dispatch to conclusion the run is 100% device-resident — the host does
NO per-step work and issues NO per-step synchronization.** The simulation drives ITSELF on the GPU.

Concretely, a production sim:
- Keeps ALL state (velocity, pressure, conformation Ψ, mesh/metrics) resident on the device for the
  whole run. The host uploads ICs once and reads results back only for occasional I/O.
- Runs the ENTIRE time step as a captured CUDA graph (predictor → pressure solve → correction →
  viscous solve → constitutive RK3 → diffusion → limiter), and runs the WHOLE TIME LOOP as a
  device-driven graph — a `while`/conditional graph that advances N steps (or until a device-computed
  stop criterion) with NO host round-trip per step. Inner solves are nested conditional sub-graphs.
- Does EVERYTHING the host used to do between kernels on the device: axpy/combine, trace limiter,
  spectral clamp, upwind lift, stress-divergence/body-force assembly, the convergence test, AND
  **mesh adaptation (AMR)** — the smoothness indicator, refine/coarsen flagging, mesh/mortar rebuild,
  and field remap must run on the GPU (or be structured so they need no host sync, e.g. a
  fixed-max-level masked representation refreshed inside the device loop).
- Host I/O (trajectory dump) happens every N steps via an async copy, off the critical path — the
  only sanctioned host↔device traffic.

A GPU sim that still has host orchestration per step is a PROTOTYPE, not production. Do not call it
ready for sweeps, and do not launch large sweeps on it. Building a new production sim ⇒ design the
device-resident data layout + the CUDA-graph step + the self-driving loop up front; see the
device-residency project plan/memory.

## RULE ZERO — synchronizing host↔device copies in a loop will MURDER performance

**Any host↔device copy that happens every step (or every RK stage / CG iteration) and forces a
device/stream synchronization is the single most destructive performance bug in this codebase.**
Each `cuMemcpyHtoD`/`cuMemcpyDtoH` that the host then waits on (`cuStreamSynchronize`, a blocking
copy, or `.to_host_vec()`) serializes CPU and GPU: the GPU drains, the host copies + does scalar
work, the GPU restarts. The kernels can be perfectly tuned and the run is still slow because the
device sits idle behind these sync points — exactly the "near-zero GPU utilization with steady PCIe
traffic" symptom. This is not a micro-optimization; it is the difference between 5% and 85% GPU
utilization.

So, as an absolute rule:
- **Do NOT** download a field to the host, do host math (axpy / clip / clamp / lift / reduction /
  convergence test), and re-upload it, inside a time loop. Keep the field **device-resident** and do
  that math in a device kernel.
- **Do NOT** read a scalar back to the host every iteration to branch on it (e.g. a CG residual
  test) — keep the loop on the device (device-side predicate / conditional graph).
- A copy is only acceptable per-step if it is genuinely unavoidable I/O (e.g. a trajectory dump
  every N steps) — and even then it should be async and off the critical path.
- When you must move data, move it **once** (static data uploaded at handle-build / on remesh), and
  batch + overlap the unavoidable transfers; never one-tiny-blocking-copy-per-kernel.

The profiling gate below exists largely to catch this: in `nsys`, watch `cuStreamSynchronize`,
`cuMemcpyHtoD/DtoH` counts (should NOT scale with steps×stages), and steady per-step PCIe traffic in
`nvidia-smi dmon -s t`. If they scale with the step loop, you have a Rule Zero violation — fix it
before anything else.

## The three anti-patterns that keep biting us (check FIRST, by reading the code)

1. **One-shot context/module load in a hot function.** `CudaContext::new(...)` or `kernels::load(...)`
   inside any function called per-step or per-RK-stage = ~0.3 s of host JIT/link per call, GPU idle.
   FIX: a persistent handle (`struct { stream, module, … }`) built ONCE, reused. See `GpuPoisson`,
   `GpuLogConf`. See memory [[gpu-oneshot-kernel-antipattern]].
2. **Per-step synchronizing host↔device round-trips (see RULE ZERO above — the worst offender).**
   Downloading a field to the host, doing host math (axpy/clip/clamp/lift/reduction), and re-uploading
   between kernels in a time loop. Each round-trip is a sync + latency stall that serializes CPU/GPU;
   constant small PCIe traffic in `nvidia-smi dmon -s t` and step-scaling `cuStreamSynchronize` in
   nsys are the tells. FIX: keep fields **device-resident** across stages/steps; do the vector ops
   and the convergence test as device kernels. See memory [[device-resident-flow]],
   [[gpu-sync-host-device-copies]].
3. **Re-uploading static data.** Mesh metrics (rx/ry/sx/sy, diff matrices, masks) re-flattened and
   re-uploaded every call though they only change on an AMR remesh. FIX: cache device buffers in the
   handle, re-upload only when the mesh topology fingerprint changes (see `mesh_fingerprint`).

Also watch: tiny 1-thread kernels at the ~1.5–2.4 µs dispatch floor (fuse them), and launch-bound
solves (CUDA graphs) — see memory [[perf-pass-while-graph]], [[gale-gpu-performance-pass]].

## The profiling gate (RUN THIS — do not eyeball it)

ncu works on this box (`RmProfilingAdminOnly: 0`; ncu 2025.2+ at `/usr/local/cuda/bin`). The old
"ncu blocked by perms" note is obsolete. Build the bin first (`cargo oxide build …`), then profile
the real binary at `target/release/<bin>` (NOT through `cargo oxide run`, which wraps it).

**MANDATORY for ANY direct run of the bare `target/release/<bin>` — profiling it, *just `time`-ing it*,
or simply running it: build with `cargo oxide build --arch sm_70 <bin>`, OR set `CUDA_OXIDE_TARGET=sm_70`
in the env.** This is broader than profiling — it bit us again mid-session merely `time`-ing a binary
that had been `cargo oxide build`-ed without `--arch`. cuda-oxide embeds kernels as NVVM-IR (bundle
target `"nvvm-ir"`) and JIT-links the cubin at runtime for `CUDA_OXIDE_TARGET`, which **defaults to
`sm_120`** when unset. `cargo oxide run` injects `=sm_70` (auto-detected); the bare binary — what the
profilers AND a direct `time ./target/release/<bin>` execute — never does ⇒ an sm_120 cubin ⇒
`cuModuleLoadData` fails with `DriverError(209) "no kernel image is available for execution on the
device"` on the Titan V. The 209 is NOT a CUPTI/perms problem — it's the wrong-arch cubin. So always:
```sh
CUDA_OXIDE_TARGET=sm_70 ncu --launch-count N --kernel-name regex:'…' --set basic -f -o /tmp/p ./target/release/<bin>
```

1. **Utilization + PCIe (cheap, always do this).** While a representative run steps:
   ```sh
   nvidia-smi dmon -s u    # SM/mem utilization — want SM util high (>~80%) once stepping
   nvidia-smi dmon -s t    # PCIe rx/tx MB/s — constant per-step traffic ⇒ residency problem
   ```
   Near-zero util or steady PCIe traffic every sample = a residency/one-shot bug above. Find it.

2. **Per-kernel with ncu** (profile a FEW launches of the hot kernel, not the whole run):
   ```sh
   cargo oxide build --features traj --bin <bin>          # ensure target/release/<bin> exists
   ncu --launch-count 30 --kernel-name regex:'psi_rhs|operator|cg_' \
       --set basic --target-processes all \
       --export /tmp/prof_<bin> -f \
       ./target/release/<bin>                              # set short env (e.g. TRAJ_STEPS=20)
   ncu -i /tmp/prof_<bin>.ncu-rep --page details | head -120
   ```
   Read: Compute vs Memory throughput (which bound?), Achieved Occupancy, Duration, and whether the
   kernel is at the dispatch floor. `--set full` for roofline/memory-workload detail when needed.

3. **Timeline with nsys** when util is low and you need to see the gaps (launch overhead, sync
   stalls, host work between kernels):
   ```sh
   nsys profile -o /tmp/nsys_<bin> --force-overwrite true ./target/release/<bin>
   nsys stats /tmp/nsys_<bin>.nsys-rep | head -60      # cuda_api_sum, gpu_kern_sum, gpu_mem_time_sum
   ```

## CRITICAL: ncu does NOT support kernels inside conditional (while/if) CUDA graphs — its numbers are ARTIFACTS

This bit us hard (2026-06: a whole matvec-redesign plan was built on a *wrong* "<20% HBM2,
latency-bound, 245 µs" reading that was pure measurement artifact — the real kernel is 46 µs at 76%
DRAM, bandwidth-bound). The device-resident solves run their PCG loop as a **conditional WHILE graph**,
and that breaks ncu's per-kernel profiling:

- **`ncu --graph-profiling=node`** (default — profile individual kernel nodes): **UNSUPPORTED when the
  graph contains conditional nodes.** Fails with *"Kernel nodes of a graph which can have conditional
  nodes are not supported."* You cannot get per-kernel SOL/DRAM%/stalls this way for any while-graph kernel.
- **`ncu --graph-profiling=graph`** (profile the whole graph as one unit): *runs*, but **aggregates ALL
  kernels into one measurement.** If you pass `--kernel-name regex:'gradient'` and read off a duration /
  DRAM%, it is the whole-graph replay mis-attributed to that name — **garbage. Do not trust it.**
- Root cause is the layer: CUPTI **Activity** tracing (what nsys uses) handles graph nodes fine; CUPTI
  **range/PerfWorks** profiling (what ncu uses) has the conditional-graph gap. Persists in ncu 2025.2.

**What DOES work:**
- **nsys `--cuda-graph-trace=node`** — trustworthy per-kernel **name / duration / count / timeline**
  inside conditional graphs (the bodies execute as real kernels; Activity API sees them). Use this for
  the "which kernel dominates / how many launches / iteration count" breakdown that drives decisions.
  It does NOT give hardware counters (no DRAM%, occupancy, stall reasons) — only timing.
- **ncu on the kernel OUT of the graph** — for real SOL/BW/occupancy, profile the kernel as a plain
  launch, NOT captured. Two ways: (a) a standalone microbench / the C++ ref / `op_profile`
  (`MG_P=3 MG_GRID=256 cargo oxide run --bin op_profile` prints clean event-timed matvec kernels), or
  (b) **run the real solver with the graph DISABLED** — `resident-ve-perf` honours **`RVP_NOGRAPH=1`**
  (sets `GpuResidentVe::with_while_graph(false)`), so every solve kernel launches normally and ncu
  profiles it directly with full sections. Same kernels, same data, just not captured.

**Rule:** never report a DRAM%/duration/occupancy for a while-graph solve kernel straight from
`ncu --graph-profiling graph`. Cross-check against `op_profile` (event timing) or an out-of-graph run
(`RVP_NOGRAPH=1`) before believing it. nsys for the in-situ breakdown; ncu out-of-graph for the deep dive.

## Measurement traps that have actually cost us (reasoning mistakes the mechanics don't catch)

The profiling mechanics above are necessary but not sufficient. These are the *reasoning* misses that
slipped through even with this skill loaded — internalize each:

- **Profile the WHOLE step BEFORE optimizing any kernel.** Confirm the kernel actually dominates
  (`nsys --cuda-graph-trace=node` → the per-kernel time breakdown) — don't sink effort into a kernel
  that's 5% of the step. The per-kernel ncu pass comes AFTER you know what dominates, not before.
- **Profile the ACTUAL kernel and account for ALL its bytes — never reason from a proxy.** Calling a
  smoother "at the matvec's bandwidth floor" was wrong: `op_cheby` moves the matvec's data PLUS its own
  fields (`b`/`dinv`/`dvec` read, `dvec`/`out` written) — **3.6× the matvec's bytes**, BW-bound on the
  *fields*, with a ~1.5× mixed-precision lever the matvec lacks. Profile THE kernel, not a cousin. And
  reconcile: compute its expected bytes (which fields × ndof × dtype) vs the measured `dram__bytes.sum`;
  a mismatch means you're missing traffic and haven't found the bound yet.
- **The perf metric is wall-clock ms/step (or event-timed kernel µs) — API / launch / sync counts are
  NOT.** A while-graph A/B that changed launch/sync counts won the wall-clock by ~0%. Never report an
  API-count delta as a speedup; the stopwatch decides.
- **A/B the PERF in the PRODUCTION path (the device-resident integrator / while-graph), not a standalone
  microbench.** The arith matvec was bit-perfect in `op_profile` but **46× slower** in the resident
  pressure solve — the arithmetic-neighbour opt had silently dropped per-face BC metadata, harmless
  standalone, catastrophic in the real Neumann solve. A standalone win can be a production regression.
- **Metric hierarchy — don't conflate the three.** wall-clock ms/step (the perf truth) ⊃ kernel µs (one
  kernel) ⊃ **iteration count (ALGORITHMIC — language/hardware-independent; NEVER cross-compare across
  implementations).** A C++-prototype-iters vs Rust-iters gap is the *algorithm* differing (or a bug),
  never cuda-oxide. A faster ms/step is fewer iters OR a faster kernel OR recovered residency — only the
  triplet tells you which, and only ms/step is the win.

## The gate, concretely — before declaring GPU work done

- [ ] **RULE ZERO:** no per-step/per-stage/per-iteration synchronizing host↔device copy. In nsys,
      `cuStreamSynchronize` / `cuMemcpyHtoD` / `cuMemcpyDtoH` counts do NOT scale with steps×stages,
      and `nvidia-smi dmon -s t` shows no steady per-step PCIe traffic. This check is mandatory.
- [ ] Read the new/changed code for the three anti-patterns. Fix any found.
- [ ] Whole-step profile (`nsys --cuda-graph-trace=node`) confirms the kernel you optimized actually
      DOMINATES the step — you didn't sink effort into a 5%-of-step kernel.
- [ ] Measured **wall-clock step time** (or event-timed kernel µs) before vs after, reported as a number
      — NOT an API / launch / sync-count delta (those are not perf results).
- [ ] ncu confirms **this** kernel's bound (compute/memory) — profiled the actual kernel, not a proxy,
      and its measured DRAM bytes reconcile with the bytes it should move.
- [ ] `nvidia-smi dmon` shows healthy SM util and no per-step PCIe ping-pong, OR you've explained why.
- [ ] If util is still low, ran nsys and identified the gap before moving on.
- [ ] Perf (and correctness) A/B'd in the **PRODUCTION path** (the real device-resident integrator /
      while-graph), not just a standalone microbench — a standalone win can be a production regression.
- [ ] Correctness regression still passes (e.g. `ve-check`, `ns-check`) — speed must be bit-safe.

Report the before/after numbers in the summary. "It works" is not done; "it works and here are the
profile numbers" is done.
