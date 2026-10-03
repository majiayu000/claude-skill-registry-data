---
name: rocm-kernel-trace
description: Profile llama.cpp decode on the gfx1151 ROCm GPU with rocprofv3 kernel traces, then attribute a performance regression to individual kernel categories. Use when the user asks which kernels regressed, wants a kernel/dispatch breakdown of decode, asks to profile a KV-cache or quantization change, wants ms-per-token per kernel category, or asks to compare two llama-server variants at the kernel level rather than by TPS alone.
metadata:
  hermes:
    tags: [rocm, gfx1151, rocprof, profiling, llama-cpp, kernel-trace, regression-analysis]
---

# ROCm kernel trace & regression attribution

Turn "variant B is slower than variant A" into "kernel category X costs +N ms per
output token, which is P% of the regression."

TPS tells you *that* something regressed. This skill tells you *what*. It pairs a
rocprofv3 kernel trace with an unprofiled benchmark of the same request, so the
proportions from the trace can be read as real time.

## The one thing that will waste your afternoon

**rocprofv3 writes its trace database while handling SIGTERM. The llama-server
process then hangs, spinning one CPU core, sometimes for 30+ minutes.**

Both halves of that sentence matter:

- `kill -9` right after the request → **no database at all.** The trace is lost.
- `kill -TERM` and then waiting for the process to exit → you wait ~30 minutes
  per variant for a process that is never going to exit.

The correct sequence, implemented in `scripts/trace-decode.sh`:

```text
request returns
  → kill -TERM   (this is what triggers the flush)
  → poll the *_results.db file size until it stops growing
  → kill -9      (the hang is after the flush; the data is already safe)
```

Observed on this box: ~100 MB database for a 20K-prompt / 512-output request,
flushed within ~30 s of SIGTERM, followed by a 27-minute spin at 100% of one core.

## Procedure

### 1. Isolate

Same rules as the `benchmark-qwen` skill, and for the same reasons:

```bash
sudo -n powerprofilesctl set performance
sudo -n systemctl stop qwen-mtp.service gemma-mtp.service
```

Trace on an isolated port (8101), never against production on 8001. Restore both
services and the power profile in an EXIT trap. Two ROCm runtimes on this UMA GPU
invalidate any isolation claim.

### 2. Trace each variant

```bash
scripts/trace-decode.sh \
  --label f16 \
  --bin /home/chihmin/llama-mtp-deploy/gfx1151-moe-down-weight-07689bc/bin/llama-server \
  --root /tmp/my-trace
```

Add `--kv q4_0` for a quantized KV cache, `--env VAR=1` for an env-gated candidate,
and `--extra "…"` for any other argv. Every variant must receive an identical
request: same prompt artifact, `temperature=0`, `seed=42`, same `max_tokens`.
When evaluating decode performance specifically, enable prompt caching (`cache_prompt=true`) to bypass prefill overhead while maintaining the full 20K KV cache attention footprint. Verify `prompt_tokens` and `completion_tokens` on every run — the script asserts them.

`LD_LIBRARY_PATH` must lead with the variant's own `bin/` directory. The
optimization usually lives in `libggml-hip.so`, not in the `llama-server`
executable — `strings llama-server | grep MY_ENV_VAR` will find nothing even when
the feature is present. Check the shared object.

### 3. Slice the decode window and categorize

```bash
python3 scripts/analyze_trace_db.py DB PROMPT_EVAL_MS EVAL_MS OUT.json N_OUTPUT_TOKENS
python3 scripts/categorize_kernels.py DB OUT.json CATEGORIES.json
```

`PROMPT_EVAL_MS` and `EVAL_MS` come from the server log of that same run:

```text
prompt eval time = 14144.95 ms / 20000 tokens
       eval time = 14139.37 ms /   512 tokens
```

Window method: the request's first GPU work is the first dispatch after the
largest multi-second gap (that gap is model load → health → idle). Prefill ends at
`request_start + prompt_eval_ms`. Everything after that, up to
`prefill_end + eval_ms`, is decode.

### 4. Get the unprofiled reference

Run the **same request shape** without the profiler, ≥3 cold samples, and take the
median. Decode TPS depends on output length, so a 512-token trace needs a
512-token baseline — do not reuse a 1024-token number.

### 5. Compare

```bash
python3 scripts/compare_traces.py --out compare.json \
  --variant f16=/tmp/my-trace/f16:15.444 \
  --variant q4=/tmp/my-trace/q4:18.388
```

Each `--variant` is `label=trace_dir:real_ms_per_token`, with the real value from
step 4 (`1000 / decode_tps`). The first variant listed is the baseline.

## Reading the output — this is where people go wrong

The script prints two tables. **They are not equally trustworthy.**

**(a) Traced ms/token deltas — use this to attribute a regression.** Every variant
ran under the same profiler overhead, so the *difference between them* is a real
measurement that needs no assumptions.

**(b) Scaled to unprofiled wall time — presentation only.** Scaling multiplies each
category by `real_ms_per_token / traced_kernel_ms_per_token`, which assumes the
profiler inflates every kernel category by the same factor. It does not: rocprof
mainly inflates **launch/dispatch overhead**, so launch-heavy categories
(elementwise at ~240 launches/token, quantize at ~160) are over-credited and
launch-light heavy kernels (an LM head at ~2 launches/token) are under-credited.

The tell that you are looking at a scaling artifact: a category that *cannot* be
affected by your change moves anyway. In the F16→Q4_0 KV study the scaled table
showed the Q6_K LM head at +0.125 ms/token — impossible, since KV type does not
touch the LM head. The traced table correctly showed +0.029.

**If the two tables disagree about which kernels regressed, the traced table is
right.**

## Worked example — F16 KV vs Q4_0 tiled KV, 2026-08-02

Qwen3.6-35B-A3B selective-Q4_0, commit `0985f20ae`, 20K prompt / 512 output.
Unprofiled 512-token medians: **F16 64.75 → Q4_0 tiled 59.02 tok/s (−8.8%)**,
i.e. 15.444 → 16.945 ms/token, in exchange for 4,016 MiB less KV.

Traced ms/token — where that 1.5 ms/token actually goes:

```text
category                      F16   Q4tiled    Δ      share of delta
KV Q4 global dequant        0.000     0.339  +0.339      36.7%
Dense F32/GEMM              0.467     0.630  +0.162      17.6%
MoE Q4_K Gate/Up            1.752     1.892  +0.140      15.2%
MoE Q5_K Down               1.009     1.076  +0.068       7.4%
Dense Q4_0                  1.347     1.409  +0.062       6.7%
Flash Attention compute     1.400     1.383  -0.017      -1.8%
... 13 more categories                +0.169      18.2%
TOTAL                      12.753    13.676  +0.923
```

What this tells you that TPS alone cannot:

- **Flash Attention is already fixed.** −0.017 against F16 — the tiled Q4 loader
  has fully paid back the cost of quantized KV in the attention kernels.
- **The single biggest remaining cost is a kernel that only exists in the Q4
  path**: `dequantize_block_q4_0`, the ncols=3/4 fallback that still materializes
  F16 K/V in global memory. Extending the tiled loader to ncols=3/4 is therefore
  the concrete next target, worth up to ~37% of the residual.
- The rest is diffuse second-order cache behaviour across many categories, not a
  single fixable kernel. Nothing else exceeds 0.17 ms/token.

For reference, the un-tiled Q4 path (`q4vec`, same production binary, no tiled FA)
cost +3.340 ms/token instead of +0.923, of which Flash Attention alone was +2.404
(72%). That contrast is what identified FA as the original culprit — but once the
fix is in, compare against F16 directly as above.

## Guardrails

- Never claim a TPS number from a profiled run. Tracing cost ~44% here
  (64.75 → 36.21 tok/s). Report proportions, launch counts, and deltas.
- Match request shape exactly between trace and unprofiled baseline.
- **Numerical Correctness Gate**: Verify bit-exact/logprob match first; if non-bit-exact due to FP16/Q4 accumulation differences, require Kernel output / logit A/B **Cosine Similarity $\ge 0.99$**.
- Restore `qwen-mtp` / `gemma-mtp` and the `performance` profile, and verify
  `/health` on 8001 and 8002, before reporting.
- Do not `git checkout` the research worktree to build a comparison binary; use
  `git worktree add --detach`.
- Building a candidate on this box needs the explicit HIP toolchain, or it fails
  with `use of undeclared identifier '__AMDGCN_WAVEFRONT_SIZE'`:

  ```bash
  -DCMAKE_HIP_COMPILER=/opt/rocm-7.2.2/llvm/bin/clang++
  -DCMAKE_HIP_FLAGS="-D__AMDGCN_WAVEFRONT_SIZE=32 -DHIP_ENABLE_WARP_SYNC_BUILTINS"
  ```

- Counter collection (`--pmc`) perturbs timing far more than `--kernel-trace`.
  Use it for occupancy/VGPR/cache attribution, never alongside a timing claim.

## Files

| Path | Purpose |
|---|---|
| `scripts/trace-decode.sh` | Launch one variant under rocprofv3, run one deterministic request, flush and kill correctly |
| `scripts/analyze_trace_db.py` | Slice the decode window; per-kernel counts, launches/token, GPU time |
| `scripts/categorize_kernels.py` | Group kernels into LM head / MoE / FA / dense / glue categories |
| `scripts/compare_traces.py` | Traced and scaled per-category deltas across variants |
