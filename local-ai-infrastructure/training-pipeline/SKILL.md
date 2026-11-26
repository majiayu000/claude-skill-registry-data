---
name: training-pipeline
description: 'Use for LoRA SFT training, merge, GGUF, and serving.'
---

# Training Pipeline

End-to-end flow for training OpenAmer's own model on session data, merging,
converting to GGUF, and deploying on Ollama.

## Choose the training host separately from the inference host

When Damir asks about free GPU training on Google Colab, he means Google's hosted runtime. Answer about that runtime directly; do not probe the laptop or revive an SSH worker. Local CPU inference from the downloaded GGUF is a separate step. When Damir has chosen Colab and asked to proceed, deliver the `.ipynb` rather than repeating the setup instructions or debating the choice. A task card or upstream link is not the notebook. Inspect the upstream loader and data cells: a vision example for the same model family is not a tested text-training recipe. If no hosted session is available, validate the notebook structure and synthetic-data path locally, attach the notebook, and state exactly which GPU and export steps remain untested.

Before uploading data, run `torch.cuda.is_available()` **inside the connected notebook**. If true, record `torch.cuda.get_device_properties(0)`; do not promise a T4, a session duration, or switch to a paid tier. See the [Colab FAQ](https://research.google.com/colaboratory/faq.html). Start with synthetic training examples; using Colab is not permission to upload private session history. Save the adapter and base revision outside the ephemeral runtime, then merge, export, and test the candidate locally against the current model on untouched tasks before replacing it.

## Pipeline Steps

### 1. Prepare SFT Data

```bash
cd scripts/training
python distill_sft.py                    # Extract SFT pairs from brain
```

Input: `~/.openamer/a2a/openamer-brain.jsonl` (raw session data)
Output: `scripts/training/sft_openamer.jsonl` (ChatML pairs)

### 2. Fine-Tune (CPU LoRA)

```bash
cmd.exe /c "C:\Users\damir\AppData\Local\openamer-laptop\scripts\training\_run_finetune.bat"
```

The script (`finetune_cpu.py`) loads a base model, applies LoRA, trains on
SFT pairs, and saves the adapter under `lora_out/` or `lora_out_qwen25/`.

**CRITICAL: always use the Batch wrapper on Windows** — MSYS bash translates
`/c/Users/...` paths to `C:\c\Users\...` (double drive letter) when passing
absolute paths to Python. The Batch wrappers avoid this by using native
Windows paths via `cmd.exe /c`.

Key parameters:
| Parameter | Typical value |
|---|---|
| Base model | `Qwen/Qwen2.5-1.5B` (preferred) or `Qwen/Qwen3.5-2B` |
| LoRA rank | 16 (default in script) |
| Batch size | 1 (CPU constraint) |
| Learning rate | cosine decay 3e-4 → 0 |
| Steps | 48 (3 epochs on 148 pairs) |

### 3. Merge Adapter

```bash
env -u PYTHONPATH PYTHONUTF8=1 HF_HUB_OFFLINE=1 \
  ./venv/Scripts/python.exe scripts/training/merge_and_export.py \
  --adapter scripts/training/lora_out/adapter_rolling
```

`merge_and_export.py` derives the base **from `adapter_config.json`** and refuses a
`--base` that disagrees with it (`FAIL base mismatch`) — merging onto a foreign base
is silent corruption, not a merge. Measured run: **14 s** for a 2B model from the HF
cache (9.1 GB), ~5 GB peak RSS.

After saving it calls `normalize_config(out)`. That step is mandatory for Qwen3.5,
see "Qwen3.5's MTP block" below — without it the file converts cleanly and refuses
to load.

### 4. Convert to GGUF (llama.cpp's converter, vendored)

There is **no usable converter on this box** under `C:\tmp\llama.cpp` or
`C:\Users\damir\llamacpp` (only `llama-server.exe` / `llama-quantize.exe`). The
converter is a vendored sparse checkout, because upstream's
`convert_hf_to_gguf.py` is a 14 KB shim that imports a `conversion/` package:

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/ggml-org/llama.cpp scripts/training/tools/llama-convert
cd scripts/training/tools/llama-convert
git sparse-checkout set --no-cone /conversion/ /convert_hf_to_gguf.py /gguf-py/
```

`--no-cone` is required: `sparse-checkout set convert_hf_to_gguf.py` fails with
`fatal: 'convert_hf_to_gguf.py' is not a directory`. Result: 3.4 MB, 111 modules,
and `conversion/qwen.py` knows `qwen35`.

Then one command does convert + quantize + atomic swap:

```bash
env -u PYTHONPATH PYTHONUTF8=1 ./venv/Scripts/python.exe scripts/training/convert_to_gguf.py
# [convert] ok   [quantize] ok
# GGUF_SAVED: …\mini-openamer-2b-q4.gguf (1.27 GB)
# GGUF_BACKUP: …\mini-openamer-2b-q4.gguf.prev-<ts>
```

It writes F16 with the vendored converter, runs `llama-quantize … Q4_K_M` into a
`.new` file, and only then `shutil.move`s it over the served name — a failed
conversion leaves the previous model intact. Never write the hand-rolled
`gguf.GGUFWriter` variant: it renamed tensors (`name.replace(".", "_")`) and
declared architecture `qwen3_5`, neither of which llama.cpp accepts.

### 5. Quantize & Deploy on Ollama

```powershell
cd C:\Users\damir\AppData\Local\openamer-laptop\scripts\training
ollama create openamer/openamer-mini --quantize q4_K_M -f Modelfile
ollama push openamer/openamer-mini
```

The Modelfile must point to the correct GGUF (update FROM line).

## A retrain must outlive the agent — and it must be observable

Two failures measured on the same run (2026-10-31), each of which made a correct pipeline
useless:

### The run died with the shell that started it

13+ CPU-hours of training vanished when the agent restarted: adapter unchanged, marker
correctly not advanced, no error anywhere. A nightly job that only survives as long as a
chat window is open is not a nightly job.

```bash
python scripts/training/start_retrain_detached.py            # returns immediately
python scripts/training/start_retrain_detached.py --status    # pid alive?
```

The launcher uses `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW` and
`close_fds=True`, so closing the agent or the desktop app leaves the child running. A pid
file with a **verified** pid prevents a second run (`tasklist /FI "PID eq <n>"`); a stale
pid file must never block the next night. Decode `tasklist` with `errors="replace"` — a
German Windows console emits cp850 bytes that are not valid UTF-8 and the check then raises
inside pytest.

Prove detachment without starting a 3-hour job: a parent spawns `python -c "sleep(6);
write(result)"` detached, the parent exits, and the result file must appear afterwards.
Wire the **cron job** to the launcher, not to `auto_retrain.py`, or the training hangs off
the gateway process and dies with it.

### The run was invisible

HF `Trainer` writes progress through tqdm with carriage returns to stderr and keeps it
buffered whenever stdout is not a TTY: a 13-hour run and a hung process looked identical, and
the only signal left was sampling CPU time externally. `finetune_cpu.py` now attaches a
`TrainerCallback` that appends one flushed line per step
(`logs/finetune-progress.log`: `18:04:25 step=21/315 (6.7%) epoch=0.201 loss=1.7256`), with
`logging_steps=1`; `scripts/training/watch_finetune.py [--follow]` reads it. Regression:
`tests/test_finetune_progress.py`.

That progress file is also what turns a *deadline* into a measurement. The next run died at
`subprocess.TimeoutExpired` after exactly `timeout=7200` — and the log said where: **198 of
315 steps in 120 min**, i.e. ~3.2 h for a full pass. Two rules follow:

- **Size the cap from a measured rate, not from optimism.** `auto_retrain.py` now allows
  6 h for the finetune. A cap that fires on a healthy run throws away every hour already
  spent (the marker correctly did not advance, so nothing was corrupted — just wasted).
- **A timeout must report progress, not just raise.** The `TimeoutExpired` handler reads the
  last line of `logs/finetune-progress.log` and puts it in the error, so the report says
  "killed at step 198/315" instead of a bare traceback.

### A guard must print the number it actually enforces

`finetune_cpu.py` aborts below `OPENAMER_TRAIN_MIN_GB` (default **10.0**) because the 2B fp32
run peaks at **10.2 GB RSS** (measured with 10.8 GB free) and Windows would otherwise swap —
10-50x slower. The message hardcoded `(need >= 6.0)`, so it read
`ABORT: only 8.7 GB free RAM (need >= 6.0)`: a guard that contradicts itself and sends you
hunting a bug that does not exist. Print the variable, never a literal:

```python
_ram_need = float(os.environ.get("OPENAMER_TRAIN_MIN_GB", 10.0))
_ram_ok_val, _ram_free = _ram_ok(_ram_need)
if not _ram_ok_val:
    print(f"[finetune] ABORT: {_ram_free} GB free RAM, need >= {_ram_need:.1f} GB — …")
```

Corollary: when the guard refuses, **free RAM you actually own before overriding it**. This
session found the missing gigabytes in 118 orphaned `gateway` processes (3.2 GB) rather than in
a lowering of the threshold — see `windows-python-service-ops`
(`references/orphaned-process-fleets.md`). Do not lower a measured guard to make one night's
run start.

### Check the driver before concluding the loop never learns

`mini-openamer-retrain` (`0 4 * * *`) sat **paused since 2026-10-14** with
`paused_reason: null` — 505 h without a run while `last_status` said `ok`. "The model never
learned" had two independent causes: the delivery was broken *and* the scheduler was off.
Always read `enabled` / `state` / `paused_reason` / `next_run_at` in `cron/jobs.json` before
diagnosing the pipeline itself; resume with `openamer cron resume <id>`.

Numbers, probe and callback source: `references/long-run-detachment-and-observability.md`.

## Known Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| MSYS path translation | `C:\c\Users\...` error | Use Batch wrapper (`_run_*.bat`) |
| Wrong venv | `ModuleNotFoundError: torch` | Use `openamer-laptop/venv`, not PATH python |
| sentencepiece missing | GGUF converter fails at `set_vocab` | `pip install sentencepiece` in right venv |
| Q8_0 re-quantize | `quantization only for F16/BF16/F32` | Use `--outtype f16` then `--quantize q4_K_M` |
| Ollama create path | `no Modelfile found` | `cd` to scripts/training first |
| MTP block claimed, weights absent | `check_tensor_dims: tensor 'blk.24.attn_norm.weight' not found` | `normalize_config()` — see below |
| Arch stays `Qwen3_5ForCausalLM` | converter asserts `opt_num_mtp_layers != 0` | set `architectures: ["Qwen3_5TextModel"]` when the weights hold no `mtp.*` |
| Stale adapter, other base | merge raises `FAIL base mismatch` | train an adapter for the served base, or point `--adapter` at one |
| Old GGUF still answering | new file on disk, old behaviour in RAM | stop the backend; `gguf_backend` respawns lazily on the next `chat()` |
| Regression test reads prose, not code | `assert "/admin/swap" not in src` fails although the call is gone — the new comment *explains* the removed bug | strip comments + docstrings before asserting (`_code_only()` in `tests/test_retrain_alignment.py`) |

## Architecture Selection (measured 2026-10-30)

**Qwen3.5-2B is the served base and it works.** The earlier "Qwen3.5 too new, use
Qwen2.5" advice is obsolete on this host: with the 2026 llama.cpp converter
(`conversion/qwen.py`, arch `qwen35`), the merged Qwen3.5-2B converts, quantizes to
Q4_K_M (1.27 GB) and answers at **~28–30 tok/s on CPU**. `Ollama 0.34` was the old
constraint; the serving path is now `llama-server` on `:18080` via `gguf_backend.py`,
not Ollama.

Qwen2.5 remains fine as a training target (more LoRA modules, faster), but do not
downgrade the *served* model on account of a converter limit that no longer exists —
check the converter first, it is vendored and versioned in the repo now.

### Qwen3.5's MTP block is the reason a merge "converts cleanly but will not load"

`config.json` carries `mtp_num_hidden_layers: 1` (a multi-token-prediction head).
Upstream's converter only skips it for architecture `Qwen3_5TextModel`; a
`Qwen3_5ForCausalLM` merge materialises the text tower only, so the converter adds
that block to `block_count` (24 → 25) and llama.cpp then demands a tensor that does
not exist:

```
E llama_model_load: error loading model: check_tensor_dims: tensor 'blk.24.attn_norm.weight' not found
```

`normalize_config()` (in `merge_and_export.py`, runs automatically) fixes it from the
weights themselves: layer count = highest `layers.<n>` index present, `mtp_*` dropped
when no `mtp.` tensor exists, and `architectures` set to `Qwen3_5TextModel` so the
converter's `no_mtp` branch applies. Note the ordering trap: setting only
`mtp_num_hidden_layers: 0` while keeping `Qwen3_5ForCausalLM` makes the converter
**assert** (`assert self.opt_num_mtp_layers != 0`) — the architecture name is the
switch that matters.

## Verification

### The served artifact must identify itself — else the loop is decoration

Read the GGUF header, not the file name:

```python
head = open(served, "rb").read(300_000).decode("latin-1", "replace")
# general.name / general.finetune tell you WHERE the file came from
```

Live 2026-10-30, that check was the whole finding: the file the backend loaded was
`general.name = "Qwen3.5 2B Base"` with `general.finetune = "Base"` — i.e. the
**untouched upstream model**. Months of "retraining" never reached production, and
every other signal (cron green, adapter mtimes advancing, `RETRAIN_OK` in the log)
looked healthy. After the pipeline fix the same check returns
`name = Mini_OpenAmer_2B | blocks = 24 | tensors = 320`.

So a retrain loop needs a test asserting the served file carries an OpenAmer marker
(`"openamer" in general.name`), and a directory name that produces it — llama.cpp
derives `general.name` from the merged model's folder, hence `pipeline_paths.merged_dir()`
returns `Mini_OpenAmer_2B` rather than `merged`.

### A PEFT adapter is invisible to a GGUF backend

`auto_retrain.py` used to end by POSTing the adapter to `:8081/admin/swap` — a
llama-server, which cannot load a PEFT adapter at all. The correct delivery is
merge → convert → quantize → swap the file → **stop the backend** (`gguf_backend`
spawns llama-server lazily, so the next `chat()` loads the new weights). Advance the
24 h marker only *after* the artifact changed, and assert that ordering in a test
(`MARKER.write_text` must come after the `convert_to_gguf.py` call).

### One source of truth for the chain's paths

Four stages carried four names for one artifact (trainer `lora_out` → merge
`lora_out_qwen25/adapter` → converter `mini-openamer-q4.gguf` → backend
`mini-openamer-2b-q4.gguf`). `scripts/training/pipeline_paths.py` now anchors
everything on the **served** file: `SERVED_GGUF`, `F16_GGUF`, `adapter_dir()`,
`merged_dir()`, `llama_convert_script()`, and `chain()` for the regression test.

### Prove the produced file LOADS, not just that it exists

A 1.27 GB GGUF with plausible metadata can still be unloadable. Start
`llama-server --model <new file> --port <free>`, wait for `/health`, and send one
real completion before swapping it in. Then A/B it against the current served model
on 2–3 short prompts: the swap is justified by measured behaviour, not by the fact
that the conversion exited 0. Live: base answered `17*3 → 49`, the merged model
`→ 51`; `Paris` and `xs.sort()` were identical.

Full worked transcript — exact commands, error texts, the sparse-checkout fix, the
MTP diagnosis, the A/B numbers and the reload step:
`references/gguf-pipeline-qwen35.md`.