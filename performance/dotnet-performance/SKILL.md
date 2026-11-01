---
name: dotnet-performance
description: "Tunes Puck .NET 11 performance: allocation, LINQ, Vector<T>, SIMD, tiering, AllocationWindow, puck bench, AOT analysis (IsAotCompatible, IL2026). Simulation-value numerics: maths-usage."
---

# .NET 11 performance

Judge a change by code, disassembly and load-independent counts (allocations,
operation counts). A wall-clock benchmark (`puck bench`) is evidence beside
those counts, never alone, and runs on a quiet machine. Keep runtime
improvements apart from workload-specific evidence.

## Route to the relevant evidence

| Area | Read |
|---|---|
| Cross-domain mental model, pattern changes, API shortlist, folklore | [references/core-guidance.md](references/core-guidance.md) |
| JIT, codegen, allocation, inlining, bounds checks, ISA | [references/jit-and-codegen.md](references/jit-and-codegen.md) |
| Collections, LINQ, Frozen/Immutable, `CollectionsMarshal` | [references/collections-and-linq.md](references/collections-and-linq.md) |
| Strings, spans, search, regex, UTF-8, encoding | [references/strings-text-search.md](references/strings-text-search.md) |
| Numerics, SIMD, tensor APIs, randomness, threading | [references/numerics-simd-threading.md](references/numerics-simd-threading.md) |
| I/O, compression, networking, JSON, crypto | [references/io-network-json-crypto.md](references/io-network-json-crypto.md) |
| AOT, reflection, GC handles, diagnostics, DI, runtime | [references/runtime-aot-reflection-diagnostics.md](references/runtime-aot-reflection-diagnostics.md) |

Read only the files relevant to the code under review. The references describe
.NET 11 in general, with magnitudes measured on 10.0 that 11 keeps unless a
section says otherwise; resolve their advice through
[`Directory.Build.props`](../../../Directory.Build.props) and the affected
project file before changing code.

## Apply repository constraints

- **Bare-metal Puck intentionally has no GC.** Its own runtime and platform
  host are the target. A port gives engine allocations explicit owners and
  lifetimes and supplies reclamation or reuse; do not propose adding GC or
  hosting stock .NET to preserve implicit managed lifetimes. The GC and JIT
  advice below applies to the existing stock-runtime builds
  ([owner ruling](../../../docs/decisions/runtime-and-delivery.md#the-runtime)).
- **`net11.0` is the repository default.** `Puck.Analyzers` deliberately
  targets `netstandard2.0`; inspect the affected project rather than assuming
  every project inherits the default.
- **`InvariantGlobalization` is on.** Culture-sensitive comparison and
  formatting guidance collapses to the invariant case.
- **`PlatformTarget` is x64 and `OptimizationPreference` is Speed.** Arm-specific
  and size-tuning material is background rather than a work item.
- **`Puck.World` sets `TieredPGO=false`.** Advice that rests on dynamic PGO
  (guarded devirtualization, stack-allocated `foreach` enumerators over
  `IEnumerable<T>`, hot and cold splitting) describes other hosts; for World
  code, read the disassembly of the actual build before relying on it.
- **Test hosts shape allocation evidence.** Test projects run blocking server GC
  (no background GC) so `GC.GetAllocatedBytesForCurrentThread` stays exact, and
  several suites set `System.Runtime.TieredCompilation` to `false` so allocation
  laws measure optimized code. Read the test project's own
  `RuntimeHostConfigurationOption` entries before comparing numbers across
  hosts. Counts are not comparable across different GC modes or tiering
  configurations.
- **`System.Numerics.Tensors` is a NuGet package outside the shared framework,**
  and no Puck project references it directly (it arrives transitively through
  `Microsoft.Extensions.AI`, which `Puck.World.Embeddings` uses). Adding a direct
  reference is a dependency decision.
- **AOT and trim compatibility analysis is the default; Native AOT publication
  is not.** `Directory.Build.props` sets `IsAotCompatible=true`, enabling the AOT
  and trimming analyzers under warnings-as-errors, and executables opt into
  `PublishAot` deliberately when they ship that artifact. A project that cannot
  satisfy the analyzers sets `IsAotCompatible=false` locally with a comment
  naming the blocker (`src/Puck.Launcher/Puck.Launcher.csproj` is one). Discover
  the current set with a search for that property and read each blocker comment
  before adding one; do not copy a count into a skill or document.
- **Fix a reflection-JSON analysis failure with source generation, not an
  opt-out.** Declare a `[JsonSerializable]` partial class deriving from
  `JsonSerializerContext` (`BindingProfileJsonContext` in `src/Puck.Commands` is
  the in-tree example) and call the `JsonTypeInfo` overloads
  (`JsonSerializer.Serialize(value, Context.Default.Type)`) so the analyzer sees
  the supported graph. Set `IsAotCompatible=false` only when the project file can
  document a structural blocker, such as reflection-based document
  serialization that a source-generated context cannot yet replace.
- **World publication uses ReadyToRun.** `Puck.World` restores the `win-x64` and
  `linux-x64` graphs and precompiles published assemblies; ordinary builds still
  produce IL. Compare the exact published artifact with `puck bench startup
  --world-artifact <path>` and account for its larger assemblies. The World
  README owns the publish recipe; CI retains its compile-once contract.

## Determinism outranks throughput

`AGENTS.md` rule 4 binds every value a simulation advances, compares, hashes,
snapshots or replays: the same document and input produce bit-identical state
on every run, machine and backend. Some of the references' strongest
recommendations are unsafe on that path, and they do not say so because they
are not written about this repository.

- Decide whether a value is simulation-significant before measuring. Route
  simulation numerics to [maths-usage](../maths-usage/SKILL.md): use the appropriate
  fixed-point or integer operation. A stable float reduction is still forbidden
  on a simulation or replayed-value path. Throughput alone does not justify a
  changed simulation value; justify a deliberate correction and show repeatability
  with `puck test --reproduce` before measuring it.
- **Presentation-only float SIMD.** `Vector<T>` is machine-width; a float
  reduction can change its order and bits across machines. Fixed-width
  `Vector128/256/512` with explicit lane-combine order and scalar tail gives
  a controlled reduction order when the presentation needs one. Reordering is
  a deliberate presentation choice, not a route for floats into simulation.
  `TensorPrimitives` makes no reduction-order guarantee over float/double.
- **Randomness and parallel completion order are not optimization knobs.**
  `Random.Shared`, `RandomNumberGenerator` and `Parallel.*` never touch a value
  path; [`maths-usage`](../maths-usage/SKILL.md) names the reproducible
  primitives that replace them.

Presentation-only float (shaders, renderer and UI math, capture output) sits
outside this contract and takes the references as written.

## Review discipline

- A capturing local function can allocate its display class at method entry,
  before a cache check returns. Keep a hot cache-check method separate from its
  closure-bearing slow rebuild. A test of it measures warmed calls on an active
  path; an inactive-tick test cannot see the allocation.
- Start with a profile, benchmark, allocation trace or demonstrated hot path. A
  suspected hot path is not one; ask for the evidence, and keep the clearer
  form (LINQ, `foreach`, an interface call) when it does not show a win.
- Route measurements through the existing harnesses: `puck bench kernels` for
  BenchmarkDotNet timing, allocation and disassembly; `puck bench world` for
  server construction and tick workloads; `puck bench startup` for fresh-process
  readiness. The [CLI reference](../../../docs/reference/cli.md#puck-benchthe-puckmaths-microscope)
  owns options, report fields and measurement hygiene.
- Profile a running World's frame thread with `dotnet-trace collect -p <pid>
  --profile dotnet-sampled-thread-time` (frame cost) or `--profile gc-verbose`
  (allocation ticks with stacks, GC heap stats), then `dotnet-trace convert
  --format speedscope` and aggregate the frame thread's stacks yourself; read
  `host.frames` beside it for produce and simulate per iteration. The sampler
  suspends threads at safe points, so samples pile onto `Thread.PollGC` under
  `Buffer.BulkMoveWithWriteBarrier` and other poll sites: charge that time to
  the caller's loop, not to the copy. Per-frame costs that matter here come in
  0.1-0.5 ms pieces; a scan of thousands of objects per call (a cache miss
  each) and a closure a method allocates on entry because one of its lambdas
  captures a parameter are the usual shapes.
- Attribute a trace to the workload's outer frame or thread, including its tiered and inlined stacks. Filtering
  only for an inner `WorldTick.Advance` frame drops steady samples after that method inlines; a short trace can
  then make first-use workspace growth look like the dominant steady allocation. Separate warmup from the measured window.
- Check the folklore section of the core guidance before preserving an old
  hand-optimization, and confirm specialization and call boundaries in optimized
  assembly. Prefer idiomatic code the .NET 11 JIT and libraries recognize.
- Preserve semantics, exception behavior, traversal order and sinks; performance
  evidence does not silently authorize changing them. A hand-written loop
  replaces a LINQ pipeline only with the same deferred-versus-immediate
  execution, the same empty-input and null exceptions and the same ordering.
- Record first-use work separately from warm tables, and distinguish allocated
  bytes from retained pools or peak workspace. Use idle, serial runs; sampled
  timings alone never establish an algorithmic or full-domain claim.
- Keep identities structural on hot read paths: formatting a principal or a parsed
  channel just to check a public policy or compare a channel name creates garbage
  even when the check has no work to do. Format only when the policy or output
  needs text. A placement response-mask change preserves placement ids and order,
  so resolved addresses carry across it; live permission checks refresh on every
  use.
- No law gates a timing: cost laws state deterministic counts. The managed
  allocation meter is `Puck.Abstractions.Counting.AllocationWindow`: `Least`
  takes the least of up to 16 windows of `GC.GetAllocatedBytesForCurrentThread`
  and, when every window allocated, throws naming the window, the GC mode and
  the types the runtime's `AllocationSampled` event sampled on that thread;
  `Measure` returns the same least as a count for a ceiling, and `Total` counts
  one run of a body that cannot repeat. Write allocation laws, stages and
  diagnostics with it rather than reading the counter by hand. Warm the body
  first: it runs more than once and must leave its subject able to run again.
  Outside the existing harnesses, say which harness you built and why it
  measures the claim.
- Record the runtime, build configuration, workload, and the counts or
  disassembly behind a performance claim, plus the `puck bench` result when the
  owner asked for a timing.

## First-call latency and tiering

Judge a hot kernel under default tiering as well as in FullOpts disassembly. A
method runs its tier-0 code until call counting promotes it, and promotion waits
for a spell with no new tier-0 compiles, about a second when the process sees
one processor; generic-math helpers stay calls at tier 0. So a kernel's first
calls in a fresh process can run several times slower than its steady state.

- A compute kernel a request or count enters directly takes
  `[MethodImpl(MethodImplOptions.AggressiveOptimization)]`; the cheap dispatcher
  above several kernels stays tiered, so first use compiles only the path taken.
- A published World is ReadyToRun-compiled, which moves first-use JIT work out
  of startup; an ordinary build still produces IL that tiers. A rendering World
  of either build prepares the engine's non-generic methods on a lowest-priority
  background thread after boot (`WorldCodeWarmer`, `[world.warm]` on stderr),
  so methods prepared before their first use avoid first-call JIT compilation on
  the frame thread and can still tier up. Calls made before preparation finishes,
  methods left unprepared, generic instantiations and static constructors can
  still pay first-use costs. Addon mounting pre-initializes
  `WorldAddonMutationDecoder`'s vocabulary and JSON contracts before its first
  submitted write; this runs no guest and submits no mutation.
- Check each hot method's tier with `DOTNET_JitDisasmSummary` in a scratch
  process pinned to one CPU, and record first-call cost beside the steady state.
  Pinning a harness to one CPU before it warms up starves the background tiering
  thread, so warm up first.

## Route adjacent work

| Skill | Route to it when |
|---|---|
| [`maths-usage`](../maths-usage/SKILL.md) | The code sits on a simulation value path. It owns the determinism contract this file defers to, the primitive that is correct, and which tier the change owes. |
| [`maths-laws`](../maths-laws/SKILL.md) | The optimization changes a public `Puck.Maths` member, or moves a value the law suite pins. |
| [`rendering`](../rendering/SKILL.md) | Shader, HLSL and GPU cost questions, which this skill's host-side C# guidance does not cover. |
| [`gaming-bricks`](../gaming-bricks/SKILL.md) | The optimization changes emulator timing, snapshots, replay, allocation or Post-stage behavior. |
| [`content-search`](../content-search/SKILL.md) | You need to locate a performance pattern, project property, analyzer opt-out or repeated workaround textually. |
| [`symbol-analysis`](../symbol-analysis/SKILL.md) | You are about to delete a hand-optimization the folklore sections retire and need to know what still references it. |
