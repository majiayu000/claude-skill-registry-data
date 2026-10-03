---
name: ab-qwen-profiling
description: Run a controlled A/B between llama-server variants on the local Qwen MTP stack — pick the right workload, switch between screening/sustained/end-to-end workloads, get medians with cold restarts and interleaving — then hand the winner to rocm-kernel-trace for per-kernel attribution. Use when comparing two builds, binaries, KV-cache types, quantizations, or env-gated candidates, when deciding which workload length to benchmark at, or when a change needs to be proven before it is committed or deployed.
metadata:
  hermes:
    tags: [benchmark, ab-testing, qwen, llama-cpp, rocm, gfx1151, workload, profiling]
---

# A/B profiling for the Qwen MTP stack

Answer "is variant B faster than variant A, and by how much" in a way that
survives scrutiny. When the answer is "slower," hand the traces to
**`rocm-kernel-trace`** to find out which kernels are responsible.

Division of labour:

| Skill | Answers |
|---|---|
| `benchmark-qwen` | How fast is the *deployed* service? Metric definitions, Pi end-to-end. |
| **`ab-qwen-profiling`** (this) | Is variant B faster than A? Which workload proves it? |
| `rocm-kernel-trace` | *Why* — which kernel categories moved, in ms/token. |

## 1. Pick the workload

All workloads use the same calibrated 20,000-token prompt
(`assets/qwen-prompt-20000.txt`). Only the output length changes, and it changes
the answer — decode TPS at 128 tokens is not decode TPS at 1024.

| Workload | `--tokens` | Time/sample | Use it for |
|---|---|---|---|
| **Screening** | 128 | ~40 s | Fast go/no-go. A loser here is dead; a winner is *not* yet proven. |
| **Sustained** | 1024 | ~90 s | **The acceptance gate.** Report medians from this. |
| **Trace-matched** | 512 | ~60 s | Only when pairing with a `rocm-kernel-trace` run — must match the trace's output length. |
| **Pi end-to-end** | — | ~2 min | Final realism gate. Use `benchmark-qwen`'s `benchmark-pi-agent.sh`. |

Short runs flatter a candidate: in the Q4 KV study the same change measured
+10.66% at 128 tokens but +21.59% at 1024. **Never accept a change on a 128-token
result alone.**

### Switching workload

Just change `--tokens`. Everything else — prompt, temperature 0, seed 42,
cold restart — stays fixed:

```bash
scripts/ab-run.sh --root /tmp/ab-screen    --tokens 128  --samples 3 --variant ...
scripts/ab-run.sh --root /tmp/ab-sustained --tokens 1024 --samples 3 --variant ...
```

> [!TIP]
> **Evaluating Pure Decode Performance:**
> When the primary objective is evaluating **decode throughput / latency**, enable prompt cache (`cache_prompt=true` or warm up prompt cache). This eliminates the prefill latency and GPU power/thermal noise during prefill, while preserving the full 20,000-token KV cache memory footprint and attention workload for every generated decode token.

**A trace-matched run is mandatory before scaling any trace.** `compare_traces.py`
needs real ms/token from a benchmark of the *same output length* as the trace. A
512-token trace scaled by a 1024-token TPS is simply wrong.

### If the prompt asset is missing or the model changed

`assets/qwen-prompt-20000.txt` is text, not token ids, so a tokenizer, model, or
chat-template change requires recalibration:

```bash
python3 scripts/bench_20k_prompt.py calibrate 8101 qwen3.6-35b-q4 /tmp/new-prompt.txt
```

It iterates until `usage.prompt_tokens == 20000` exactly. Verify that on every run
regardless — `summarize_ab.py` rejects the comparison if token counts differ.

## 2. Define the variants

```bash
scripts/ab-run.sh --root /tmp/my-ab --tokens 1024 --samples 3 \
  --variant 'f16prod=/home/chihmin/llama-mtp-deploy/gfx1151-moe-down-weight-07689bc/bin/llama-server' \
  --variant 'q4tiled=/tmp/llama-q4kv-clean/build/bin/llama-server|kv=q4_0|env=GGML_CUDA_EXPERIMENTAL_GFX1151_Q4_KV_TILED=1'
```

Spec format: `label=binary[|kv=TYPE][|env=VAR=VAL][|extra=ARGS]`. First variant is
the baseline.

The driver handles: `performance` profile, stopping `qwen-mtp`/`gemma-mtp`,
isolated port 8101, cold restart per sample, ten consecutive idle-GPU samples
before timing, interleaved run order, and restoring both services on exit.

### FlashHead variants

FlashHead lives in the gguf (three extra tensors) *and* in the binary (`GGML_OP_MUL_MAT_ROWS`),
so a variant spec has to name both, plus the probe count:

```bash
M=/home/chihmin/models/Qwen3.6-35B-A3B-selective-Q4_0-proof
scripts/ab-run.sh --root /tmp/ab-fh --tokens 512 --samples 3 \
  --variant "A_orig=/home/chihmin/llama-mtp-opt/build/bin/llama-server|model=$M/Qwen3.6-35B-A3B-UD-Q4_K_M-selective-Q4_0.gguf" \
  --variant "B_flash=/home/chihmin/llama-mtp-opt/build/bin/llama-server|model=$M/Qwen3.6-35B-A3B-UD-Q4_K_M-selective-Q4_0-flashhead.gguf|env=LLAMA_FLASHHEAD_PROBES=256"
```

**Keep the binary and the KV type identical on both sides.** The two ggufs are byte-identical
apart from the FlashHead tables, and the graph falls back to the dense head when they are
absent, so this spec isolates FlashHead and nothing else. Comparing the flashhead gguf against
the *deployed* `llama-mtp-deploy/...` binary instead mixes in the research branch and the KV
type - that version measured +6.34% where the clean one measured +10.84%.

Measured 2026-08-04, 512 tokens, 3 interleaved cold samples:

```text
variant     decode tps runs          median   ms/tok   MTP%     vs A
A_orig      64.83 61.75 64.14        64.14    15.591  96.764   +0.00%
B_flash     70.00 71.20 71.09        71.09    14.067  98.129  +10.84%
```

Acceptance rises slightly (0.9716 -> 0.9842) because only the draft head is tailored; if a
FlashHead variant ever shows acceptance *falling*, the target head is being approximated too
and the comparison is measuring something else.

Confirm the feature actually engaged before trusting any FlashHead number - the tables are
optional, so a wrong binary or a missing env var degrades silently to the dense head:

```bash
grep -m1 'FlashHead tables found' /tmp/ab-fh/B_flash-1.server.log
```

`LLAMA_FLASHHEAD_PROBES` is read at graph build time, so sweeping it needs one variant per
value - it cannot be changed on a live server.

## 3. Build a candidate binary safely

Never `git checkout` the research worktree — it holds uncommitted work.

```bash
git -C /home/chihmin/llama-mtp-opt worktree add --detach /tmp/llama-cand <commit>
git -C /home/chihmin/llama-mtp-opt diff <commit> <branch> -- path/to/only.cu > /tmp/cand.patch
cd /tmp/llama-cand && git apply /tmp/cand.patch
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_HIP=ON \
  -DAMDGPU_TARGETS=gfx1151 -DGGML_HIP_GRAPHS=ON -DGGML_HIP_NO_VMM=ON \
  -DGGML_BUILD_TESTS=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF \
  -DLLAMA_BUILD_SERVER=ON \
  -DCMAKE_HIP_COMPILER=/opt/rocm-7.2.2/llvm/bin/clang++ \
  -DCMAKE_HIP_FLAGS="-D__AMDGCN_WAVEFRONT_SIZE=32 -DHIP_ENABLE_WARP_SYNC_BUILTINS"
cmake --build build -j 16 --target llama-server
```

Both `-DCMAKE_HIP_*` flags are required; without them the build fails with
`use of undeclared identifier '__AMDGCN_WAVEFRONT_SIZE'`.

**Isolate the patch.** Applying only the files you want beats inheriting a whole
dirty branch: a snapshot branch carrying an unrelated broken change produced a
binary that aborted at warmup (`mmvq.cu:1061 GGML_ASSERT(!ids || dst->ne[2] == 1)`)
for every KV type, wasting a full benchmark round. `ab-run.sh` surfaces the first
`GGML_ASSERT` line when a server dies during load.

Prefer an immutable artifact under `/home/chihmin/llama-mtp-deploy/<name>/` when
one already exists — more reproducible than rebuilding an old commit today.

## 4. Read the result

```bash
python3 scripts/summarize_ab.py /tmp/my-ab
```

Median is the comparison statistic, never best-of. The summary also prints the
`--variant label=<trace_dir>:<ms/tok>` lines that `rocm-kernel-trace` needs.

Reject or rerun when: prompt tokens differ across variants; the sustained run does
not finish at `max_tokens`; MTP acceptance differs materially while raw TPS is
being used as proof; another GPU workload was live; or services were not restored.

## 5. Hand off to kernel attribution

A slower variant is a question, not a conclusion. Trace both sides at 512 tokens
and attribute the difference:

```bash
T=~/.claude/skills/rocm-kernel-trace/scripts
$T/trace-decode.sh --label f16     --root /tmp/tr --bin BIN_A
$T/trace-decode.sh --label q4tiled --root /tmp/tr --bin BIN_B --kv q4_0 --env VAR=1
# ...analyze_trace_db.py + categorize_kernels.py per side, then:
python3 $T/compare_traces.py \
  --variant f16=/tmp/tr/f16:15.444 --variant q4tiled=/tmp/tr/q4tiled:16.945
```

Read `rocm-kernel-trace`'s SKILL.md before running it — rocprofv3 hangs
llama-server on shutdown, and killing it the obvious way destroys the trace.

## Worked example — Q4_0 KV cache, 2026-08-02

Two variants, selective-Q4_0 model, commit `0985f20ae`, sustained 1024-token
workload, 3 interleaved cold samples each:

```text
variant     KV size    decode median    vs F16
f16prod    5588 MiB      63.55 tok/s        —
q4tiled    1572 MiB      59.93 tok/s     -5.7%
```

The A/B established *what*: Q4_0 KV saves 4,016 MiB and the tiled FA kernel
recovers most of its cost. The trace established *why*: at 512 tokens, Flash
Attention with the tiled candidate returned to baseline (−0.017), leaving the ncols=3/4 global dequant
(+0.339) as the largest remaining item.

Caveat carried from the source work and not re-verified here: the tiled path is
approximate, not bit-exact — output diverges after ~100 events at 20K/1024. Speed
A/B is not a correctness gate; run exactness checks separately before deploying:
- **Bit-Exact / Logprob Check**: Verify logprobs/tokens match baseline.
- **Cosine Similarity Fallback**: If bit-exact match cannot be achieved due to accumulation differences in quantized/tiled kernels, verify that the kernel output / logit A/B **Cosine Similarity $\ge 0.99$**.

## Files

| Path | Purpose |
|---|---|
| `scripts/ab-run.sh` | Interleaved cold-start A/B driver across variants |
| `scripts/bench_20k_prompt.py` | One timed request; also `calibrate` mode for the prompt |
| `scripts/summarize_ab.py` | Medians, percent change, trace scale references, validation |
| `assets/qwen-prompt-20000.txt` | Calibrated exactly-20,000-token prompt |
