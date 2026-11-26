---
name: inference-optimisation
description: >
  Hill-climb the serving speed of a local LLM on any hardware (NVIDIA, AMD, Intel,
  Apple, unified-memory laptops, multi-GPU) and any quantization (GGUF, EXL2/EXL3,
  AWQ/GPTQ, FP8, MLX, BF16): single-user and concurrent decode tok/s, speculative
  decoding, prefill tok/s, KV cache size, startup time and TTFT, under a memory cap
  and with full-context stability. Computes the theoretical ceiling first, runs
  noise-controlled A/B experiments, keeps a ledger, and qualifies the winner before
  publishing it. Use when asked to optimise, tune, speed up, benchmark or hill-climb
  a model server (vLLM, SGLang, llama.cpp, ExLlama/TabbyAPI, MLX, TensorRT-LLM...),
  to find the maximum possible tok/s on a machine, or to publish a tuned recipe.
  Triggers: hill climb, tok/s, decode speed, prefill speed, MTP, EAGLE, draft model,
  speculative decoding, KV cache, TTFT, startup time, theoretical maximum.
personas:
  - DEVOPS
  - SRE
  - DEV
tech_stack: []
vendored_from: https://github.com/sybil-solutions/inference-optimisation-skill (MIT, see LICENSE.upstream)
triggers:
  - inference-optimisation
  - inference
  - optimisation

---

# Inference optimisation (hill-climbing a model server)

You improve how fast a model server runs on one machine, with evidence.
The loop is:

1. Measure the baseline.
2. Calculate the ceiling.
3. Change one thing.
4. Measure it against controls.
5. Keep it or reject it, and write down why.
6. Repeat until the remaining gap needs work out of scope, then qualify and publish.

Detailed references, read when needed:

- `references/ceilings.md`: how to compute theoretical maxima. It includes a worked example.
- `references/methodology.md`: measurement pitfalls and statistics.
- `references/levers.md`: levers by area, ordered by typical payoff, with measured evidence.
- `references/gotchas.md`: engine- and hardware-specific traps.
- `references/publishing.md`: qualification gates, pinning, poster and report.
- `scripts/`: an engine-agnostic harness. It has a bench, ceiling calculator, memory watchdog, serialized queue and ledger.

## 0. Before touching anything

- **Write down the targets and constraints** the user gave. Ask only if one is missing and it changes what you do.
  - Metrics that matter: c1 decode, cN decode, prefill at several lengths, TTFT, startup.
  - Memory cap.
  - Context length that must stay stable.
  - Which quality changes are allowed: lossless only, or labelled lossy trades such as int8 prefill.
- **Inventory the machine:**
  - accelerator, memory type and size, and whether memory is unified;
  - driver, engine version, model, quantization, current launch command.
- **Measure, don't trust spec sheets:**
  - real memory bandwidth (device copy);
  - real matmul throughput (large GEMM);
  - clocks under load.
- **Read any existing experiment log for this machine and model.** Never rerun a rejected experiment without a new reason.
- **Create the working directory:**
  - `PLAN.md`: a timestamped log of every experiment, with numbers, verdict and reason.
  - `THEORY.md`: the ceilings.
  - `ledger.jsonl`: one line per run, from the harness.
  - `configs/`: one JSON per run.
  - `best-config.json`.

## 1. Ceilings first

Compute the theoretical maximum for each metric before optimising (`scripts/ceiling.py`, `references/ceilings.md`):

- **Decode is memory-bandwidth bound.** Count the bytes read per emitted token:
  - dense weights;
  - active experts: top-k ÷ experts × expert bytes;
  - LM head;
  - KV read at the working context.
  - Divide by measured bandwidth.
  - Speculative decoding divides the target's bytes by the accepted length. It also adds the draft's bytes, and the draft's LM head is often the biggest part.
- **Prefill is compute bound.** FLOPs per token ≈ 2 × active params, plus attention at about 4 × layers × hidden × position. Divide by ~50% of measured peak for a practical ceiling.
- **TTFT floor:** one forward pass plus tokenize and schedule.
- **Startup floor:** weight read from disk or page cache plus allocation, assuming JIT and graph caches persist.
- **KV:** bytes per token per layer × the layers that actually have KV (hybrid models have few). That gives how many full-length sequences fit under the memory cap.

Report progress as a percentage of the practical ceiling. If the user's target is above the ceiling, say so early, with the arithmetic.

## 2. Ground rules (non-negotiable)

1. **One change per experiment.** Give each its own config file. Derive new configs from the current best.
2. **Control for noise.** Run-to-run noise is typically ±5–10%.
   - Take ≥6 decode samples per run and use the median.
   - Run controls on both sides of each candidate: control, candidate, control.
   - Accept only if the candidate beats both neighbouring controls on its target metric and regresses nothing by more than ~3%.
   - Repeat any single surprising win.
3. **Keep the environment fixed.** Stay on AC power, on a fixed performance profile, with an idle host and no other GPU jobs.
   - Make the harness refuse to run otherwise.
   - Record the state at the end of each run, and void the run if it changed.
   - Restore any profile you changed when you finish, and tell the user.
4. **Run one GPU job at a time.** Serialize them with a lock (`scripts/queue.sh`).
   - Never use `pkill -f`/`pgrep -f` patterns that can match your own shell.
   - Detach long queues (`setsid nohup … &`) so they survive agent restarts.
5. **Enforce the memory cap with a watchdog** that kills the run.
   - On unified memory, GPU allocations do not show in cgroup counters or MemAvailable. Measure driver residency (e.g. `drm-resident-*` in `/proc/<pid>/fdinfo`, `nvidia-smi`, or `ioreg`/`vm_stat` on Apple) plus process anonymous memory.
6. **Stability gates.** A config is only "best" after it passes:
   - a long-context retrieval run, with needles in a ~50% then ~100% context document, found exactly;
   - a soak with concurrent full-length requests, if the KV pool is sized for N users;
   - a greedy output equivalence check, if the change claims to be lossless.
7. **Never force-kill a server mid-batch.** Abort requests, wait for the drain, then stop with a timeout. A forced stop mid-prefill has caused GPU driver faults.
8. **Verify outputs, not just speed.** Flag degenerate or looping output, failed requests and an idle GPU. A suspiciously fast result is usually broken output.
9. **Log everything in `PLAN.md`,** including failures and why they failed. Negative results are the most reusable output.
10. **Secrets:** never ask twice for a credential the user already saved. Never print it, and never copy it or its path into anything published.

## 3. The loop

```
baseline → profile → pick the lever with the largest (ceiling gap × likelihood) → config → A/B with controls
   ↑                                                                                         ↓
   └──────── update best-config + PLAN.md + ledger ←──── accept / reject with reason ←───────┘
```

### Lever order

Cheapest first; see `references/levers.md` for evidence.

1. **Persistent JIT, compile and graph caches** (startup −50–70%). Also use eager safetensors loading instead of mmap where it is slow.
2. **Decode graphs** (CUDA/XPU graphs): often 2× c1 on their own.
3. **Speculative decoding:**
   - Choose the method (built-in MTP, EAGLE, a draft model, n-gram).
   - Sweep draft length per concurrency and context; the best length differs.
   - Prune the draft LM head's vocabulary.
   - Keep sampling on the GPU.
   - Make sure verify runs with decode-style attention.
4. **Concurrency and KV sizing:**
   - Set max running requests and the KV pool to N × context.
   - For hybrid SSM/GDN models, size the state slots. They, not KV, often cap concurrency.
   - Explicitly enable prefix caching and confirm `cached_tokens` > 0.
5. **Prefill:**
   - Tune chunk size; it trades throughput against decode stalls.
   - Use a faster attention library.
   - Use int8/fp8 prefill GEMMs as a labelled quality trade.
   - Avoid padding cliffs in grouped MoE GEMMs.
6. **Kernel thread and tile sizes:** defaults are often tuned for a bigger card.
7. **Kernel work:** profile, read the ISA, fix the dominant kernel. Do this only after config levers plateau.

### When a lever fails

- **If kernel-count reductions (fusion) give nothing** under graphs, the time is inside the main kernels. Stop fusing.
- **If higher acceptance doesn't give higher tok/s,** the draft costs too much. Measure per-step time.
- **If a weird result appears,** suspect the measurement first: tokens counted per streamed chunk, prompt length not measured with the real tokenizer, cache hits, thermal state, or the battery.

### Plateau

Declare a plateau when three consecutive levers land inside noise. Write a STATUS section in `PLAN.md` with:

- best numbers vs baseline vs ceiling;
- what limits further gains, with evidence;
- a ranked list of the remaining levers and their estimated cost.

Then keep the loop alive at a slower cadence if the user said "don't stop", or hand back.

## 4. Qualify and publish

See `references/publishing.md`.

- Pin weights by revision, engine by image digest or source commit, and kernels by commit. Build the published artifact from those pins in a clean checkout, never from a dirty tree.
- Run the acceptance gates on the clean build: load, chat, reasoning, tools round-trip, a long-context needle, and speed.
- Then A/B the clean build against your best image to prove they match.
- Report which numbers come from which harness. Gate numbers (e.g. thinking on, first 30 s) and hill-climb numbers (thinking off, medians) are not comparable.

## 5. Reporting to the user

- **Start with a table:** metric, baseline, now, ceiling, how it was measured (median of N, cold or warm, which harness).
- **Then:** what got the gains, why it stops here, the known limitations, and the system state you changed (power profile, running servers, uncommitted code, branches that must not be deleted).
- **Say plainly** what was not verified.
- **When asked to free the GPU:** drain, stop the server, confirm no processes and an idle clock, and end any loop.
