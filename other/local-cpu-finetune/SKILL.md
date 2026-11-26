---
name: local-cpu-finetune
description: Use for CPU-only LoRA fine-tuning of local LLMs.
---

# Local CPU Fine-Tuning (no GPU laptop)

Proven path on Damir's 22GB-RAM, no-GPU Windows laptop. Scripts live in
`scripts/training/` (openamer-laptop).

## THE invariant: trainer base == served adapter base (found 2026-10-05)

The retrain loop was silently dead for 9 days. Root cause: **`finetune_cpu.py`
trained `Qwen/Qwen2.5-1.5B` and wrote `lora_out_qwen25/`, but `tool_server.py`
serves `SmolLM2-360M-Instruct` + `lora_out/adapter`.** An adapter for a
different base can never load (LoRA size mismatch), so every nightly retrain
was wasted; the loop's "ok" was the gate passing, not training succeeding.
Two more bugs compounded it:
- the hot-swap copies `lora_out/adapter` — which the trainer never wrote;
- `auto_retrain.py` backed up the adapter AFTER finetune, i.e. it copied the
  freshly-trained one over the backup → no rollback.

**Rules:**
1. `BASE` in the trainer MUST equal `adapter_config.json → base_model_name_or_path`
   of the adapter the server loads (`tool_server.py::_base_for_adapter`).
2. `OUT` MUST be `lora_out` (the hot-swap + server read `lora_out/adapter`).
3. Back up the adapter **before** training (`copytree` precedes the finetune call).
4. Add `--smoke` (a few `max_steps` into a throwaway dir) so the pipeline is
   verifiable without clobbering the production adapter.

**360M is the fast, RAM-safe base:** SmolLM2-360M LoRA on CPU ≈ **7.5 s/step**
(measured), 237 steps ≈ **30 min**, ~13.7 GB free RAM — vs Qwen2.5-1.5B at
~25 s/step (100 min) + OOM risk. Train the base you SERVE, not the biggest one.
Regression pin: `scripts/tests/test_retrain_alignment.py`.

## The invariant is fixed LIVE but still broken on `main` (found 2026-10-06)

The half-shipped state, and the one to check before quoting any of this as done.
Three copies of `tool_server.py` exist (live / `openamer-repo` / `repo-tmp`) and
**they disagree**, so "the fix is in" is a statement about one tree at a time:

```bash
for f in scripts/training/tool_server.py; do
  echo "live=$(md5sum "$OPENAMER_HOME/$f" | cut -d' ' -f1)"
  echo "repo=$(md5sum "/c/Users/damir/openamer-repo/$f" | cut -d' ' -f1)"
done
```

Measured 2026-10-06: live `7037e7be…` ≠ `main` `ce485460…`. `main` still carries
**both** original bugs that the whole loop was built to remove:

```python
BASE = "Qwen/Qwen3.5-2B"                                            # hardcoded
ADAPTER = .../AppData/Local/openamer/scripts/training/lora_out/adapter  # OLD home
```

- `main` hardcodes `BASE` instead of resolving it from the served
  `adapter_config.json` (`_base_for_adapter`); the live file resolves it, with a
  `HuggingFaceTB/SmolLM2-360M-Instruct` fallback.
- `main` still defaults `OPENAMER_HOME` to `.../Local/openamer`, **not** the real
  profile root `.../Local/openamer-laptop` — so a stock install reads an `ADAPTER`
  path that does not exist and silently falls back to the hardcoded base.
- **Never compare two source copies with `diff <(sort a) <(sort b)`.** Sorting
  destroys position, so the live file's *added* lines report as deletions of the
  repo's — it reads as if the live file is *missing* the fix. Diff line-by-line, or
  compare the two constants directly.

The live tree is the working one; the repo tree is what a contributor installs.
Before reporting the loop as fixed, say **which tree** the fix is in.

### Prove a LoRA's base from the safetensors header — no download, no load

The cheapest and strongest evidence for a base mismatch. `lora_A.weight` is
`[r, hidden_in]`, so the second dim **is** the base model's hidden size, and it is
readable from the file's JSON header alone:

```python
import struct, json
with open(adapter_model_safetensors, "rb") as f:
    n = struct.unpack("<Q", f.read(8))[0]      # 8-byte LE header length
    hdr = json.loads(f.read(n))
print(hdr["base_model.model.model.layers.0.self_attn.q_proj.lora_A.weight"]["shape"])
```

Measured on the served adapter: `[16, 960]` — r=16, hidden **960** = SmolLM2-360M.
`Qwen/Qwen3.5-2B` is hidden 2048, so that pair **cannot** load: startup dies with a
LoRA size mismatch, which is exactly what `main`'s hardcoded `BASE` would cause.
Re-runnable: `scripts/lora_base_probe.py <adapter_dir>` — prints the declared base,
the measured hidden size, and the base's own `config.json` fetched from HF Hub (a few
hundred bytes, no weights) to compare. Offline it reports *unmeasured*, never a guess.
Run it before publishing any "base mismatch" or "loop fixed" claim.

### The data path was the OTHER half of the dead loop

`auto_retrain.py` read the **stale Sep-24 copy** of the brain:

```
~/.openamer/a2a/openamer-brain.jsonl                  57,522,301 B  mtime 2026-09-24
$OPENAMER_HOME/a2a/openamer-brain.jsonl  7,544 records 144,760,807 B  mtime live
```

`brain_collect` **regenerates** the file rather than appending, so counts are not
monotonic and the old `new = brain_ct - last_ct` guard went negative whenever the
dataset shrank — the retrain stayed silent forever. Gate on **dataset mtime vs. the
retrain marker** (`.last_retrain`) plus a minimum size, never on a count delta:

```python
if BRAIN.stat().st_mtime <= MARKER.stat().st_mtime: return   # silent: nothing new
if brain_ct < MIN_NEW_PAIRS: return                          # silent: too small
```

Live `auto_retrain.py` is **byte-identical to `main`** (md5 `86c3e8e6…`) — this
half *did* ship, unlike the `tool_server.py` one. Do not assume the two travelled
together; verify each file separately.

Worked case + exact commands: `references/main-vs-live-retrain-divergence-20261006.md`.

GGUF runtime evidence (which Qwen3.5 GGUFs actually load on this host):
`references/gguf-compatibility-measurement-20261019.md`.

**Correction added 2026-10-19 — the 2B GGUF DOES load.** The matrix above was
wrong: `scripts/training/mini-openamer-2b-q4.gguf` (1.27 GB) is live on
`:18080` and answering. The files that fail are the *3.76 GB* `mini-openamer-q4.gguf`
and the *3.78 GB* `mini-openamer-f16.gguf` — same prefix, different size, only
the 1.27 GB one works. Full corrected state, the tool_server GGUF migration,
the broken `convert_to_gguf.py`, and the venv-selection trap:
`references/gguf-live-state-20261019.md`.

## Diagnose the dataset SHAPE before touching hyperparameters

A fine-tune that "does not work" is usually a dataset whose *shape* nobody
inspected. Measured 2026-11-18 on a 40.6 MB / ~12.2 M-token SFT set that was
believed to be conversation data:

| file | lines | what it actually contained |
|---|---:|---|
| `chatml_50k.jsonl` | **70,550** | Wikipedia articles dressed as Q&A: `{"user":"Was ist Abraham Lincoln?", "assistant":<full lexicon article>}` |
| `chatml.jsonl`, `trainingsdaten.jsonl` | 5,312 | same |
| `trainingsdaten_live.jsonl` | **53** | genuine dialogue — **0.075 %** of the corpus |

The model then behaved exactly as trained: it emitted lexicon articles and
stopped mid-sentence (`"Die Liste der Hauptstädte in Australien und Ozeanien
zeigt …"`) because training targets were ~16 KB against a 300-token inference
cap. Nothing was wrong with the trainer, the LoRA config, or the merge.

**Five checks, in this order:**

1. **Read line 1 of every training file.** One line classifies a file as real
   dialogue / document dump / self-generated. Report the dialogue share as a
   number before tuning anything. `head -1 file.jsonl` is the whole tool.
2. **Compare target length to `max_seq_length`.** Targets longer than the cap
   teach the model to stop mid-sentence. Targets must look like the outputs you
   want, not like the source documents.
3. **Filter on CONTENT, never on length.** The gate here was
   `len(text) > 20 and len(text) < max_seq*4`, which passed
   `*Inwohner* – die Winnerge der Stadt` and Thai script (`clairestาษา`) inside
   German prose — a model's hallucination saved back as a training *target*.
   Minimum real filter: expected script, duplicate hash, min/max characters.
4. **Do the arithmetic on the feedback set.** A `feedback_korrekturen.jsonl` with
   **7 lines** inside 70,550 examples is **0.01 %**. A loader can print
   "höchste Priorität" and still have zero effect; curated human judgement starts
   moving behaviour around 500+ pairs. Below that it is decoration.
5. **Pin the token budget to a stated target.** 12.2 M tokens is ~82× short of
   the ~1 B minimum for a from-scratch 1B model and ~3,000× short of a 36 B-token
   frontier run — at 40 MB per 3.5 months that is millennia. Fine-tuning needs
   roughly 1e-4 of pre-training compute, which is why a free T4 does it in
   30–50 min. **For a personal corpus the plan is always LoRA on a strong base,
   never from-scratch** — and it is the LoRA path that makes 40 MB a usable
   amount of data instead of a hopeless one.

**And the step that makes 1–5 visible: a fixed eval set before training.** This
run had none — only a falling training loss, which measures "copies the training
data better", not "answers more correctly". That is why a 2/7-scoring model went
unnoticed. One epoch, then measure; three epochs over a copy-pattern only cements
it.

## Pipeline
1. **Distill**: session trajectories are too long for SFT. Use
   `scripts/training/distill_sft.py` to cut brain JSONL into user→assistant pairs
   (answers ~500-2000 chars). Real yield: 94 pairs from 2.8k trajectories —
   after raising the user-turn reject ceiling 4000→20000 chars and trimming to
   the last 3000 instead of dropping (26 pairs recovered). Run a
   rejection-reason breakdown (count each `continue` branch) before accepting
   a filter's yield as natural — a dominant drop-reason means the filter is
   wrong, not the data. Cron-runner `[System note:...]` user turns are
   correctly dropped (1519 hits, ~0 recoverable) — don't "recover" those.
2. **Train**: `scripts/training/finetune_cpu.py` — LoRA (r=16, q/k/v/o_proj) on
   Qwen3.5-2B, FP32 CPU, batch 1 + grad-accum 4, 3 epochs. **Wall time is
   RAM-DEPENDENT, not fixed (25× swing, measured 08.09):** 94 pairs / 72 steps
   ≈ 1 h 12 min (~60 s/step) with ≥6 GB free RAM — but 2 steps in 5 HOURS
   when Windows swaps (training loads the model twice ≈ 7-8 GB; a resident
   tool_server 3.4 GB + a loaded Ollama model 6 GB leaves 0.3 GB free).
   `finetune_cpu.py` now self-guards via `_ram_ok()` (aborts below 6 GB free,
   `GlobalMemoryStatusEx` via ctypes). **Best training window: after the
   tool_server's 30-min idle self-exit** (measured 13.7 GB free). Never start
   CPU training right after a model-heavy task, and never conclude "CPU
   training is impossible" before checking whether RAM was the bottleneck.
4. **Merge adapter → full weights**: `scripts/training/merge_and_export.py` loads the
   base model + LoRA adapter, calls `model.merge_and_unload()`, saves as safetensors
   to `scripts/training/merged/`. Takes ~7 min CPU for Qwen3.5-2B (320 weights, float16).
   Output: `model.safetensors` (~3.6 GB for 2B params in fp16).
5. **Ollama import**: Use a Modelfile pointing to the merged directory:
   ```
   FROM C:\path\to\scripts\training\merged
   TEMPLATE "{{ .Prompt }}"
   PARAMETER temperature 0.7
   ```
   Then: `ollama create openamer-mini -f Modelfile.merged` (~20-30 min on CPU for
   GGUF conversion + quantization).
6. **Post-training benchmark**: After Ollama import, run the benchmark on the new
   model to compare before/after scores. The benchmark uses OpenRouter by default —
   to test the local model, modify `score_answer_gpt` in `benchmark.py` or query
   Ollama directly via `/api/generate`.

## bf16 base weights unblock the RAM guard (measured 2026-11-09)

The nightly retrain had been aborting for days on its own guard: `_ram_ok()`
demanded **10 GB** free (peak RSS measured 10.2 GB) while this laptop typically
offers 5–9 GB. The weights are the whole cost — a 2B base at fp32 is
`2e9 × 4 B ≈ 8 GB` before any LoRA state.

**This CPU has AVX512-BF16** (`torch.cpu._is_avx512_bf16_supported()` → `True`
on the Ryzen AI Strix Point), so the frozen base can be narrowed. LoRA adapter
tensors stay fp32 (peft's default); only the untrained base changes precision.

Measured with `scripts/training/bf16_smoke.py` (load + one fwd/bwd through the
adapter, no checkpoint written):

| | fp32 | bf16 |
|---|---|---|
| RSS after load | ~8 GB | **4.32 GB** |
| peak RSS | 10.2 GB | **4.61 GB** |
| loss (1 step) | — | **1.7055, finite** |
| fwd+bwd | — | **1.0 s** |
| load time | — | 5.6 s |

What changed in `finetune_cpu.py`:

1. `OPENAMER_TRAIN_DTYPE` defaults to **`auto`** → bf16 when
   `_is_avx512_bf16_supported()`, else fp32. Values: `auto | bf16 | float32`.
2. The guard threshold follows the dtype: **6.5 GB for bf16, 10.0 GB for fp32**.
   A guard still demanding the fp32 figure refuses a run that would fit.
3. `_ram_ok()` runs *before* the model load, so it must re-derive the dtype
   itself (it cannot read a variable defined further down). Two independent
   resolutions of "which dtype" is a divergence waiting to happen — keep them in
   the same file, adjacent, same default.

Check before accepting any "training is impossible on this box" conclusion:

```bash
venv/Scripts/python.exe -c "
import torch; print(torch.__version__, torch.cpu._is_avx512_bf16_supported())"
```

A **finite loss** is the gate, not the dtype name: bf16 matmuls on a CPU without
the kernel can silently produce NaN. `bf16_smoke.py` fails loudly on
`not torch.isfinite(loss).item()` and prints `SKIP` when the CPU lacks the flag.

**Quote the threshold the run ENFORCED, not the one you remember.** An old build
demanding 10 GB and a new one demanding 6.5 GB produce the same message shape but
mean different things; a run that aborted at 9 GB free was correct under the old
number and would pass under the new one.

## Venv selection pitfall — background processes use wrong python

The `finetune_cpu.py` script must run in the **openamer-laptop** venv
(`.../venv/Scripts/python.exe`), NOT the **openamer-agent** venv
(`.../openamer-agent/venv/Scripts/python.exe`). The latter has no pip, no torch,
no transformers. A background process started with bare `python finetune_cpu.py`
inherits PATH which points to the wrong venv.

**Always use the explicit path** when starting training:
```python
r"C:\Users\damir\AppData\Local\openamer-laptop\venv\Scripts\python.exe"
```
Or wrap in a `.bat` file (see `_run_finetune.bat` pattern in
`windows-subprocess-robustness` skill). Do NOT rely on PATH resolution.

To verify: `python -c "import sys; print(sys.executable)"` should show the
openamer-laptop venv path. If it shows openamer-agent, the training will fail
with `ModuleNotFoundError: No module named 'torch'`.

## Pitfalls (all hit live)
- **Qwen3.5-2B emits "thinking traces"** (Qwen3.5 family is a thinking model):
  answers start with `Here's a thinking process:` + numbered reasoning steps
  before the real answer. The real answer is at the END of the generated text.
  For clean extraction, prefer deterministic first-sentence extraction over
  parsing the model, or strip the JSON/thinking preamble with a regex. The model
  is not dumb — it gives correct answers, just with reasoning noise in front.
- **Model upgrade on CPU: measure latency, not parameter count (2026-09-06).**
  `qwen3.5:4b-q4_K_M` (4.7B) vs the 2B base: answer quality marginally better,
  but ~69s vs ~13s per answer on CPU (5× slower) — a regression for interactive
  use. 4B is only viable for background tasks (learning/summarization). The real
  bottleneck was free RAM (2.3GB), not model size: unloading an unused Ollama
  model (`POST /api/generate {"model":X,"keep_alive":0}`) freed 2.3→7.8GB. Check
  RAM and measure a real end-to-end answer before proposing any model switch.
- **Brain JSONL roles**: `tool` messages dominate; user→assistant pairs are NOT
  adjacent. Walk with a `last_user` pointer, skip tool roles.
- **`tool_calls` key on real answers**: assistant messages carry a `tool_calls`
  field even with genuine text content. Only discard when content is empty —
  filtering on key-presence throws away ~98% of usable pairs.
- **Collator label bug**: labels must be `labels + [-100]*pad_len` (pad-masked,
  same length). Building `[-100]*len + labels` doubles length →
  `ValueError: batch_size (79) vs (158)` in cross_entropy.
- **state.db timestamp**: `messages.timestamp` is REAL unix epoch —
  `date(timestamp,'unixepoch')`, not `date(ts)`.
- **CPU FP32 is slow**: monitor via `powershell Get-Process <pid>` (CPU seconds
  growing = healthy); `tail` pipes buffer background output until exit.
- Base HF weights (`Qwen/Qwen3.5-2B`) may already be in the HF cache — check
  before downloading.
- **Importing the module runs the training**: `finetune_cpu.py` executes the
  full pipeline at import time (no `if __name__` guard). `from finetune_cpu
  import _ram_ok` loads the 2B and starts stepping — kill the process and test
  the function by extracting it via `ast` instead, or run it in a subprocess
  you can kill. Live trap 08.09: a "quick guard test" via import burned the
  model load before it was caught.
**CORRECTION 2026-10-31 — `/admin/swap` is no longer the delivery path.** After the
GGUF migration, `tool_server.py` serves through `gguf_backend` (:18080, a
llama-server) — and a llama-server cannot load a PEFT adapter *at all*. The loop's
real delivery is merge → convert → quantize → swap the served `.gguf` → stop the
backend (it respawns lazily on the next `chat()`). `auto_retrain.py` no longer POSTs
to `:8081`; a tree that still does is the old, decorative version whose "success"
never changed the model. Details: `training-pipeline` →
"A PEFT adapter is invisible to a GGUF backend". The bullet below is kept as history.

- **Adapter roll-out (was canonical until the GGUF migration)**: the running
  `tool_server.py` (:8081) exposes **`POST /admin/swap`** with body
  `{"adapter": "<abs path>"}` → `{"result": "OK: swap queued (#1) — applied on
  next request"}`. The swap is QUEUED, not immediate — it applies on the next
  inference request, so fire one `POST /v1/chat/completions` afterwards and check
  `GET /health` shows `"swaps": 1`. The server adopts the base from
  `adapter_config.json → base_model_name_or_path` (`_base_for_adapter`), which is
  why the trainer's `BASE` must match (see the invariant above).
  (`auto_retrain.py` calls this endpoint after finetune; an older note here
  claimed a `.swap_request` flag file + `adapter_rolling/` copy — that is NOT the
  canonical path the live server uses. If `/admin/swap` 404s, then and only then
  look for the flag-file mechanism.)

## Pitfalls (all hit live, continued)

### GGUF Conversion API mismatch (Qwen3.5, 2026-09-15)
`scripts/training/convert_to_gguf.py` uses `gguf.GGUFWriter`. The API has
changed — these common methods DO NOT exist in gguf>=0.6:
- `GGUFWriter.add_ctx_len()` → AttributeError
- `GGUFWriter.add_embedding_length()` → AttributeError  
- `GGUFWriter.add_block_count()` → AttributeError
- `GGUFWriter.add_head_count()` → AttributeError
- `import GGUFWriter, ModelSpecialTokens` → ImportError (`ModelSpecialTokens`
  removed in recent versions)

**Fix:** Use only `gguf.GGUFWriter.__init__(path, arch)` + 
`gguf_writer.add_tensor(name, data)` + `gguf_writer.write_header()`
+ `gguf_writer.write_kv_data()` + `gguf_writer.write_tensors()`
+ `gguf_writer.close()`. Skip all metadata helpers — set KV pairs manually
via `gguf_writer.add_uint32(key, value)` if needed.

### Ollama unsupported architecture — Qwen3.5 (2026-09-15)
Ollama 0.34.0 does NOT support `Qwen3_5ForCausalLM` architecture:
```
Error: unsupported architecture "Qwen3_5ForCausalLM"
```
The merged safetensors (float16, 3.6 GB) cannot be imported via `ollama create`
with a Modelfile. **Workarounds (in priority order):**
1. Upgrade Ollama to ≥0.35 (may add Qwen3.5 support)
2. Use `llama.cpp`'s `convert_hf_to_gguf.py` (clone repo, run Python script)
3. Keep the merged model as safetensors for direct HuggingFace inference via
   `transformers` — Ollama is not required for local use

### Batch-wrapper pattern for MSYS path translation
All training/merge scripts must run via a `.bat` wrapper to avoid the MSYS
path-doubling bug (`/c/Users/...` → `C:\c\Users\...`):
```batch
@echo off
setlocal
set PYTHON=C:\Users\damir\AppData\Local\openamer-laptop\venv\Scripts\python.exe
set SCRIPT=C:\Users\damir\AppData\Local\openamer-laptop\scripts\training\SCRIPTNAME.py
"%PYTHON%" "%SCRIPT%"
```
Start via: `cmd.exe /c "C:\path\to\_run_script.bat"` (not bare `python`).
Existing wrappers: `_run_finetune.bat`, `_run_merge.bat`, `_run_gguf.bat`.

### Venv verification — always use explicit path
```python
# To check which venv the background process will use:
# In terminal: which python  (should show openamer-laptop venv)
# In Python: import sys; print(sys.executable)
```
If it shows `.../openamer-agent/venv/...`, the script WILL fail with
`ModuleNotFoundError: No module named 'torch'`. The openamer-agent venv has
no pip, no torch, no transformers. Always use the explicit openamer-laptop
venv path for training/merge/inference scripts.

## Measuring a long training run without fooling yourself (2026-10-05/06)

The retrain takes **36 min** (237 steps × ~9 s, SmolLM2-360M, measured
end-to-end). Getting the *state* wrong burned a whole session — three traps:

1. **Never grep process names from a shell whose own command line contains the
   pattern.** `Get-CimInstance Win32_Process | Where CommandLine -like
   '*auto_retrain*'` matches **your own bash invocation** and reports a
   "still running" phantom forever. Filter to the interpreter and the script
   file, and measure CPU to prove liveness:
   ```powershell
   Get-CimInstance Win32_Process -Filter "name='python.exe'" |
     Where-Object { $_.CommandLine -like '*finetune_cpu.py*' } |
     ForEach-Object { $p=Get-Process -Id $_.ProcessId -EA SilentlyContinue;
       '{0} CPU={1}' -f $_.ProcessId,[int]$p.CPU }
   ```
   CPU seconds **growing** = healthy; absent from the list = finished/dead.
2. **One logical run = a process tree, not one PID.** A `bash` wrapper + a
   uv-python parent + the venv-python child all exist at once (`python ... 2>&1
   | tail -25` adds the pipeline). Killing "the process" can leave a child
   still training, and the wrapper can stay alive as a zombie long after.
   `process(action="wait")` on the wrapper is unreliable when its stdout is
   buffered through a pipe — poll the **progress log file** instead.
3. **Foreground is capped** (the tool's ~40 s limit SIGTERMs a long job, leaving
   a half-written artifact). Run training `background=true, notify_on_complete=true`
   and redirect to a log you can `tail`:
   ```bash
   ./venv/Scripts/python.exe scripts/training/finetune_cpu.py > /c/tmp/finetune.log 2>&1
   tail -1 /c/tmp/finetune.log | tr '\r' '\n' | tail -1   # live step counter
   ```

4. **`auto_retrain.py` is ALSO a long job — never launch it from the foreground**
   (hit live 2026-10-10). A cron/one-shot prompt that says "run via terminal:
   `python …/auto_retrain.py`" will print `RETRAIN: <n> records` + the distill
   counts, `copytree` the pre-training backup, start `finetune_cpu.py` (32 min,
   240 steps) — and then the tool cap SIGTERMs the whole tree mid-training:
   distill done, backup done, **no adapter, no `RETRAIN_OK`**. Nothing is lost
   (the backup precedes training, and `.last_retrain` is written only *after* a
   successful finetune, so the 24 h gate does not block the retry) but the CPU
   hour is. Launch it background and tee a log:
   ```bash
   python …/scripts/training/auto_retrain.py 2>&1 | tee logs/auto_retrain_$(date +%Y%m%d).log
   ```
   In a cron/one-shot session `notify_on_complete` is unavailable **and**
   `process(action='wait')` clamps to 60 s → sleep in ≤600 s foreground chunks,
   then read the log (`tr '\r' '\n' < … | tail`) or check liveness with
   `psutil.Process(<wrapper_pid>).children()` for a live `finetune_cpu.py` child
   (`wmic`/`tasklist` often return nothing on this host — psutil is the reliable
   probe). The wrapper also captures the child's stdout via `subprocess.run`, so
   **no incremental loss lines appear until finetune exits** — an apparently
   frozen log is normal; the `\r`-stripped Trainer block arrives all at once.
   Success shape (measured 2026-10-10): 319 distilled pairs → 240 steps →
   `train_runtime 1920 s` (32 min), `train_loss 2.131` → `ADAPTER_SAVED` →
   `HOT_SWAPPED: OK: swap queued (#1)` → `RETRAIN_OK adapter updated`.

**Closed-loop success record** (the shape a working run leaves behind): log ends
`100%|██████████| 237/237 [36:05]` → `ADAPTER_SAVED` → `FINETUNE_EXIT=0`;
`lora_out/adapter/adapter_model.safetensors` mtime is *today* (was frozen 9 days);
`POST /admin/swap` → `swaps: 1`; a `/v1/chat/completions` request answers. The
post-retrain benchmark moved **0.561 → 0.474** on a 314-pair dataset — honest
signal that a 360M base is weak, not that the loop failed. Snapshot the old
adapter to `lora_out/adapter_pre_retrain_<ts>/` before any manual full run
(the automatic path backs it up via the pre-training `copytree`).

## GGUF runtime compatibility matrix (measured 2026-10-19, llama.cpp on this host)

Not all Qwen3.5 GGUFs actually run. Three of four tested fail or misbehave —
**but the matrix below was superseded the same day.** See "the live 2B GGUF
loads" first; it is the one that actually serves today.

### The live 2B GGUF loads — correction to the earlier matrix (measured 2026-10-19)

Earlier this session the 2B GGUFs were judged dead on arrival. **That was
wrong.** The server on `:18080` is `scripts/training/mini-openamer-2b-q4.gguf`
(1.27 GB, 320 tensors) and it is **live and answering**:

- `GET /v1/models` → model id `mini-openamer-2b-q4.gguf`
- `POST /v1/chat/completions` → valid reply, 847 completion tokens, ~15% of the
  prompt survived into the answer, `finish_reason=stop`
- GGUF header: `general.architecture = qwen35`, `general.basename = Qwen3.5`,
  `general.name = Qwen3.5 2B Base`, 24 blocks, 2048 hidden, 262144 context,
  file_type 15 (Q4_K_M-ish), tokenizer `gpt2` / pre `qwen35`

So the 2B GGUF **does** load on this host. The earlier failures were on the
*bigger* files (`mini-openamer-q4.gguf` 3.76 GB and `mini-openamer-f16.gguf`
3.78 GB) — those are the ones that fail. **Name and size matter: the 1.27 GB
`mini-openamer-2b-q4.gguf` is the working one; do not confuse it with the
3.76 GB `mini-openamer-q4.gguf`.** The `merged/Merged-1.5B-*.gguf` files
(Qwen2.5, 28 blocks / 1536 hidden) are legacy artifacts that are **not** served
by anything — ignore them.

### The earlier matrix (kept for reference — superseded above)

| Model | Size | Runs in llama.cpp? | Verdict |
|---|---|---|---|
| `Qwen3.5-4B-Q4_K_M.gguf` | 2.7 GB | ✅ loads, answers correctly | usable |
| `Qwen3.5-0.8B-Q4_K_M.gguf` | ~0.5 GB | ⚠️ loads, **loses itself in thinking** | unusable — see below |
| `mini-openamer-q4.gguf` (2B) | 3.76 GB | ❌ `check_tensor_dims` fails at startup | unusable |
| `mini-openamer-f16.gguf` (2B) | 3.78 GB | ❌ `blk.24.attn_norm.weight not found` | unusable |

**The 0.8B thinking trap (measured, 2026-10-19).** Qwen3.5 is a thinking family:
it emits a `reasoning_content` block before `content`. For a trivial question
("Was ist 7 mal 8?") the 0.8B burned **11,518 reasoning tokens** over 94 s and
returned **empty content** — it never finished thinking. The 4B, by contrast,
reasoned 355 tokens in 13 s and answered `56`. Two lessons:

1. **Never set `max_tokens` below the model's expected reasoning budget.** With
   `max_tokens=512` the 0.8B produced 1,416 reasoning tokens and no content; at
   4,096 it produced 11,518 and still no content. The cap truncates *content*,
   not reasoning, so a tight budget silently loses the answer. Budget for
   reasoning + answer together.
2. **A smaller thinking model is not necessarily faster.** 0.8B ran at 52 tok/s
   (4× the 4B's 10.7 tok/s) but took 7× longer wall-clock because it thought
   longer. Measure **wall-clock to the answer**, not parameter count or tok/s.

### Which model to use

The live `:18080` server answers in ~15% of the prompt's token budget — fast
enough for interactive tool use. The 4B is a fallback for background brain work
where 10–13 s per question is acceptable. **Never propose "use the 2B GGUF" as a
fix without naming the exact 1.27 GB file** — the 3.76 GB same-named file does
not load.

## From-scratch CPU model (`openamer_brain`) — 2026-11-01

A second, different path next to LoRA fine-tuning: a 4.92M-param byte-level
model trained **from scratch** on the collected brain corpus, shipped as
`openamer_brain/` with `openamer brain model | train | say`.

```bash
openamer brain model                      # checkpoint, params, step, loss
openamer brain train --steps 1000         # fresh; --resume to continue
openamer brain say "OpenAmer is a" --tokens 40
```

Requirements and correctness checks: skill `local-cpu-brain` (user-owned).
Measured loss curve, per-condition throughput and generation samples:
`references/cpu-brain-scratch-run-20261101.md`.

Four traps worth carrying into ANY from-scratch CPU model, because they cost
real time here:

1. **Prove causality with the untrained loss.** For a byte-level model with
   vocab 256, an untrained net must score ≈ `ln(256) = 5.545`. It measured
   **2.24** — a full future leak from a global FFT filter. The fix (left-aligned
   causal FIR) restored 5.591. A loss that *starts* below `ln(vocab)` is a bug,
   not fast convergence.
2. **`model(x, x)` is not a loss probe.** Position i legitimately sees token i,
   so the loss drops below `ln(vocab)` with no leak. Always shift:
   `model(x[:, :-1], x[:, 1:])`. This produced a false "leak" alarm and then a
   false "all clear" before it was caught.
3. **Padding the decode step is the usual generation killer.** Decoding with
   the context padded to `max_seq_len` on every token gave **1.4 tok/s**; a KV
   cache plus the FIR buffer gave **280 tok/s** on the same weights — and
   verified bit-identical to full recompute (max Δ 2.7e-7). Cache the attention
   K/V *and* the convolution's last K-1 inputs.
4. **Attribute CPU before believing a throughput number.** Training fell from
   3,900 to 350 tok/s mid-run. Not the model: `llama-server.exe` held 1,635% of
   a 16-core box. Name the top offender, don't just report the total, and never
   publish a tok/s figure without the load condition next to it.

Also: `torch.set_num_threads(16)` on an already-loaded 16-core box is **worse**
than 8 — the trainer took 1,781% alone, and 8 threads were both faster and left
the machine usable.

## Verification discipline
Claim only: distill count + exit code, then "training running" with CPU-time
evidence. Final proof = adapter files exist → Merge complete (adapter → safetensors)
→ `MERGED_SAVED` confirmation. Never claim "GGUF ready" before `ollama list`
shows the model.

## Related
- `dream-cycle` skill (nightly consolidation feeds the brain dataset).
