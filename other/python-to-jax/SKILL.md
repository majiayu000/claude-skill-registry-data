---
name: python-to-jax
description: >-
  Port Python / NumPy / PyTorch code (Orbit Wars envs, agents, policies,
  rollout/PPO loops) to JAX, producing a `<name>_jax.py` (or a `*_jax/`
  package for directory-level ports) that is jit/vmap-friendly, plus a
  numerical-parity pytest that proves the JAX output matches the original
  within float32 tolerance. Use this skill WHENEVER the user asks to
  "convert to JAX", "JAX 化", "jax に書き換え", "port this env/agent to jax",
  "make this jittable / vmappable", "GPU 化したい", "rewrite the rollout in
  JAX", or names a file/directory (e.g. `rollout.py`, `pipeline/reinforce/
  case2/training/`) and asks to translate its Python/NumPy/Torch logic into
  JAX. Trigger even when the user only gives a path or a vague "this" — the
  skill resolves the target and proceeds TDD-style. Do NOT use for writing
  brand-new JAX code with no Python source, for plain JAX bug-fixes, or for
  PyTorch-only work that isn't being ported.
---

# Python → JAX Conversion

Port Python/NumPy/PyTorch code to JAX so it runs jit-compiled and vmap-batched
on GPU, while staying numerically faithful to the original. This repo has done
this conversion many times (`jax_env/`, the `*_jax.py` policy/training files
under `bot/pipeline/reinforce/case1`), and every port is anchored by a **parity
test** that compares the JAX output to the Python original. That test is the
contract — write it first, port until it passes.

## First, check the port can actually pay off (throughput, not latency)

JAX/GPU wins **throughput** — many independent units (episodes, boards,
candidates) computed in parallel under one `vmap`. It does **not** win
**latency**: a single small computation (one agent turn, one short function
call) runs *slower* on GPU than in Python, because the fixed per-call dispatch +
host↔device transfer cost exceeds the work. Measured in this repo: the same
intercept solver hit **681× on a batched (24×24) grid** but **0.18× (5.6×
slower)** when called per-turn inside a rule-based agent's `act()` — a ~6 ms
workload that GPU offload can't beat (the dispatch alone costs more).

So before porting *for speed*, ask: **is there a batch axis to amortize over?**
- RL rollouts / self-play (many episodes), training steps (minibatches),
  evaluating a board over many candidates at once → **yes, port it**, the vmap
  axis is the win.
- A single rule-based turn, an interactive request, any one-shot sub-10 ms call
  with no batch dimension → **GPU can't help**; porting may slow it down. Port
  only if it feeds a batched consumer, and benchmark the *consumer's* unit
  (see `references/benchmark-and-tune.md` §2), not the function in isolation.

Porting for *correctness/reuse* (sharing a kernel with the JAX env, enabling
autodiff) can still be worth it without a speed win — just don't claim a speedup
that the usage pattern can't deliver.

## The core loop (TDD)

The user picked TDD for a reason: a JAX port that "looks right" but silently
diverges (a wrong axis, an off-by-one in a mask, a `+=` that doesn't accumulate
under `scan`) is worse than no port, because the bug surfaces 200 iterations
into a GPU training run. The parity test catches it in seconds on CPU.

1. **Locate & read the source.** Resolve the target (path or natural language).
   Read the full Python/Torch implementation plus anything it imports that also
   needs porting. Note the public contract: function/class names, argument
   shapes, return shapes, dtypes.
2. **Find the parity reference.** Look for an existing `*_jax.py` sibling or a
   `test_*_parity.py` in `bot/tests/` — this repo almost always has a prior
   port to mirror for naming and structure. Read it before writing anything.
3. **Write the parity test FIRST (RED).** Before porting, write a pytest that
   runs the Python original and the (not-yet-existing) JAX version on identical
   inputs and asserts they match within tolerance. It won't import yet — that's
   the RED state. See `## Parity test` below for the idiom.
4. **Port the code (GREEN).** Translate following `references/conversion-patterns.md`.
   Keep shapes fixed, replace control flow with `lax` primitives, make modules
   `eqx.Module`s. Iterate against the parity test until it's green.
5. **Verify the whole suite.** Run `dev/test-bot` (or the targeted pytest) and
   `uv run --directory bot ruff check` + `mypy`. A port isn't done until lint
   and types pass too — this repo bans `Any` / `cast` / `type: ignore`.
6. **Benchmark & tune for speed (GPU only).** A JAX port that's only correct but
   not faster missed the point — the reason to port is GPU throughput. Benchmark
   the Python/Torch original against the JAX version **on a GPU (RunPod), never
   on the local CPU**, then tune the JAX version until it's actually faster,
   **re-running the parity test after every tuning change** so speed never costs
   correctness. The timing idiom (warm-up + `block_until_ready`) and the full
   tuning playbook live in `references/benchmark-and-tune.md` — read it when you
   reach this step. Report the speedup (e.g. "JAX GPU 18× the Torch baseline at
   horizon=500, vmap=16"). If no GPU pod is available, write the GPU bench script
   and say the figure is pending a RunPod run — don't substitute a CPU number or
   guess.

Run pytest from `bot/`:
```bash
uv run --directory bot pytest tests/<path>/test_<name>_jax_parity.py -x -q
```

## Resolving the target

The user may say "convert `rollout.py`", "JAX 化 this directory", or just "this".

- **Single file** → produce `<name>_jax.py` next to it. Suffix convention is
  non-negotiable here: `rollout.py` → `rollout_jax.py`, `model.py` →
  `model_jax.py`. Classes/functions get a `Jax` suffix
  (`ActorCritic` → `ActorCriticJax`, `ppo_update` → `ppo_update_jax`).
- **Directory / env-or-agent "一式"** → port file-by-file in dependency order
  (leaf modules first: geometry/constants → state → step → rollout → train).
  Mirror the layout the repo already uses for `bot/src/jax_env/` (constants,
  state pytree, pure-jax step, host-side reset, observation bridge). Port and
  green one module's parity test before moving up the dependency chain — a
  bottom-up green wave is far easier to debug than porting everything then
  fixing a wall of failures.

### Scope by the hot path, not by file size — the goal is a faster agent

When the goal is "speed up this agent/env" (almost always), the leaf-first
*order* above is right, but **leaf-first must not become leaf-only.** The whole
point is to make `act()` / `step()` / the training loop faster, and that only
happens if you port the code those entry points actually spend time in. Porting
the easy bottom layer (pure geometry, scalar helpers) and stopping there gives a
green parity test and a real GPU speedup *on that function* — while the agent
runs exactly as slow as before, because its entry point is still Python and
never calls your JAX code on the hot path.

So before deciding what to port: **find where the per-turn time actually goes.**
It's usually a function called inside a loop over candidates/pairs/steps — e.g.
an O(P²) `for src: for target:` intercept solver, or a per-step featurizer. That
hot function is the one to port, *even when it's the hard one* (variable-length
search, refinement loops, early-exit) — those constructs are hard precisely
because they're doing the work. Deferring them as "too hard" defeats the task.
Port the hot function so it can be **`vmap`'d over the whole loop domain at
once**, replacing the Python loop with one batched JAX call. Genuinely ragged,
data-dependent bookkeeping that *isn't* compute-bound (dict lookups over a
variable comet list, rolling opponent-model state) is fine to leave on the host
— but say so explicitly and make sure it isn't the bottleneck you're avoiding.

`references/conversion-patterns.md` §12 has the recipes for the three hard
constructs that block these ports (fixed-iter refinement with early-exit,
variable-length search → fixed grid + masked argmin, host-side dispatch for
ragged data). Read it when the hot path has any of them.

If the target is ambiguous (no path, no obvious "this"), ask which file or
directory — don't guess and port the wrong thing.

## The five conversions that matter most

Full detail with before/after examples is in
`references/conversion-patterns.md` — read it when porting. The essentials:

1. **Fixed shapes + masks, never dynamic length.** JAX traces shapes at compile
   time, so a Python list that grows, a `for` over a variable count, or boolean
   indexing that returns a variable-size array all break jit. Pad to a `MAX_*`
   constant and carry a `*_valid` / `*_mask` boolean array; compute over the
   full padded array and `jnp.where(mask, value, neutral)` to ignore padding.
   This is why `EnvState` uses `MAX_PLANETS=48`, `MAX_FLEETS=512` with
   `planet_valid` masks.

2. **`lax.scan` / `vmap` / `cond` replace Python loops.** A `for t in range(T)`
   rollout becomes `jax.lax.scan(step_fn, init_carry, xs)`; N parallel episodes
   become `jax.vmap`; an `if cond:` that depends on traced values becomes
   `jax.lax.cond` or `jnp.where`. Mutations (`state.x = ...`, `list.append`)
   become returning a new carry / stacking scan outputs — JAX arrays are
   immutable, use `.at[idx].set(...)` and `NamedTuple._replace(...)`.

3. **`eqx.Module` for anything with parameters.** PyTorch `nn.Module` → Equinox
   `eqx.Module` (a registered pytree), so the forward pass is jit/vmap-friendly
   and gradients flow via `eqx.filter_value_and_grad`. Optimizers move to Optax
   (`optax.adamw` + `optax.clip_by_global_norm` for `clip_grad_norm_`).

4. **Weights load by name, 1:1.** When porting a trained PyTorch model, the JAX
   module must accept the original `.pt` weights leaf-by-leaf
   (`load_bc_weights_jax`-style: `torch.load(weights_only=True)` → copy by
   parameter name → assert `missing == 0`). The parity test then loads the same
   weights into both and compares forward passes. Mirror the architecture
   exactly (layer order, hidden dims, biases) or the load silently mismatches.

5. **One trace, not one-per-input.** Threading a Python `int` (e.g. `seed`) into
   a jitted function recompiles per distinct value and can blow the compile
   cache to multiple GB (this repo hit a >3 GB cache → SIGABRT exactly this
   way). Build per-call state on the host, stack into a batched pytree, and pass
   the *array* in — scalars that vary should be traced arrays or `static`.

## Parity test

The parity test is the deliverable's spine. It must run the Python original and
the JAX port on byte-identical inputs and assert closeness. Tolerance bands this
repo uses:

- **Forward-pass / pure-numeric parity** (model logits, featurizer, geometry):
  `float32` tolerance `1e-4`. JAX defaults to float32; if the Python side is
  float64 (e.g. NumPy), cast inputs to float32 first so the comparison is fair.
- **Multi-step trajectory parity** (env rollouts): positions drift because
  float32 accumulates differently than float64. Compare *macro* state
  (planet owner, ship counts — integer/categorical) exactly, and either allow a
  wider band on float positions or record disagreements rather than hard-fail,
  following `bot/tests/unit/jax_env/test_parity.py`.

Use the existing parity tests as templates — read the closest one and copy its
structure:
- Model/forward: `bot/tests/unit/pipeline/reinforce/case1/test_model_jax_parity.py`
- Featurizer: `bot/tests/unit/pipeline/reinforce/case1/test_featurizer_jax_parity.py`
- Env/trajectory: `bot/tests/unit/jax_env/test_parity.py`,
  `test_trajectory_parity.py`

A parity test for a freshly-ported model typically: seeds the Python model,
saves its `state_dict` to a temp `.pt`, loads it into the JAX module, runs both
on the same observation, and asserts `max|diff| < 1e-4` on each output head.
Also assert **parameter count matches** (`sum(p.numel())` vs the JAX pytree leaf
sizes) — a count mismatch means the architecture diverged.

## Conventions this repo enforces (don't skip)

- Place the JAX file beside its source; place its parity test mirroring `src/`
  → `tests/unit/` layout. Env-level work goes under `bot/src/jax_env/`.
- Top-of-file docstring should state **which Python file it mirrors** and any
  intentional deviations (deferred features, zeroed columns), exactly like the
  existing `*_jax.py` headers — future readers rely on this to trust parity.
- Python 3.13 types, no `Any` / `cast` / `type: ignore`. Annotate arrays as
  `jax.Array`. Config/output containers are `NamedTuple` or frozen
  `@dataclass` / `eqx.Module`.
- Never mutate; always return new instances (`_replace`, `.at[].set`).
- Imports at the top of the file (the repo's one exception is the
  `# noqa: E402` sys.path-injection block in parity tests that pull the
  vendored simulator — mirror that exact pattern, don't invent a new one).

## Benchmark & tune

Correctness is the floor; speed is the goal. Once parity is green, measure and
improve throughput **on GPU (RunPod), never on the local CPU** — CPU wall-clock
doesn't predict GPU behavior, and the vmap-scaling that justifies the port only
shows up on-device.

**Benchmark the entry point's unit of work, not the isolated function.** If the
goal was a faster agent, the headline number is *per-turn `act()` wall-clock
(Python vs JAX)* — or, equivalently, the per-pair cost of the hot loop you
replaced with a `vmap`. Time the Python double loop and the single batched JAX
call on the *same* (src×target) grid, and report per-pair wall-clock plus the
speedup at realistic grid sizes (sweep them — the speedup grows with the grid,
which is the whole point of vmap). A microbenchmark of one leaf function in
isolation can show a big ratio while the agent is unchanged; don't let that
stand in for the agent getting faster. The honest-timing idiom (warm-up to exclude compile cost,
`block_until_ready` to defeat async dispatch) and the full tuning playbook
— profile → JIT & loops → memory & precision → parallelize → data pipeline,
with the specific traps this repo hit — are in
`references/benchmark-and-tune.md`. **Read that file when you reach this step**;
don't tune from memory. After every tuning change, re-run the parity test so
speed never costs correctness. If no GPU pod is reachable, write the bench
script and report the GPU figure as pending a RunPod run — never a CPU
substitute or a guess.

## When you're done

Report: which files were created, the parity test path and its tolerance, the
green test output, the **speed comparison** (Python baseline vs JAX, with the
device, horizon/batch settings, and the vmap-scaling curve or the headline
speedup), which tuning changes you applied and that parity still held after
them, and any intentional deviations from the Python original (deferred
features, wider tolerance bands, host-side vs device-side splits) so the user
knows exactly what was and wasn't proven equivalent. If the GPU number is
pending a RunPod run, say so — don't fabricate it.
