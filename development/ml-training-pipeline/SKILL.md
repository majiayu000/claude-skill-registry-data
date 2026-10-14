---
name: ml-training-pipeline
description: Debug ML training pipelines that stop early, OOM on eval, or produce wrong epoch counts.
---

# ML Training Pipeline Skill

## Problem it solves

ML training frameworks have silent failure modes that look like model bugs but are actually pipeline infrastructure issues. TensorFlow's ` keras.utils.Sequence` adapter may produce too few batches per epoch when `__len__` is small, epoch-end evaluation spikes memory and silently kills the process on small GPUs, and virtual environment Python executables are redirector stubs that report wrong PIDs. These issues waste hours because the error messages point at the model, not the pipeline.

## Detection triggers

Activate when:
- Training stops after exactly 1 epoch with no error
- Process silently disappears during epoch-end evaluation
- `StopIteration` or "input ran out of data" during training
- GPU memory usage spikes at epoch boundary then process dies
- `Start-Process` returns a PID with 0 CPU and tiny memory (venv stub)
- Training loss only shows 1 epoch in history despite running for hours

## Protocol

### 1. Check if the data adapter loops

TensorFlow's `model.fit` iterates the adapter once per epoch. If `__len__` returns a small number, you get few batches per epoch and the training appears to stall. If `__len__` is `sys.maxsize` and `shuffle=True`, the adapter does `list(range(len))` and OOMs.

Verify:
```python
import tensorflow as tf
# Check your Sequence's __len__ — is it reasonable?
seq = YourSequence()
print(f"__len__ = {len(seq)}")  # Should be ~samples/batch_size
```

Fix — make `__len__` return a moderate multiple and wrap `__getitem__`:
```python
class LoopingSequence(tf.keras.utils.Sequence):
    def __init__(self, original):
        self.original = original

    def __len__(self):
        # Moderate multiple — NOT sys.maxsize (causes OOM with shuffle=True)
        return len(self.original) * 1000

    def __getitem__(self, idx):
        real_idx = idx % len(self.original)
        item = self.original[real_idx]
        if real_idx == 0:
            self.original.on_epoch_end()
        return item
```

### 2. Disable epoch-end evaluation on small GPUs

Per-epoch mAP/accuracy evaluation builds a second model and can silently OOM-kill the process on 6GB GPUs.

```bash
# BAD — evaluation spikes memory at every epoch boundary
python train.py --epochs 12

# GOOD — skip per-epoch eval, run once at the end
python train.py --epochs 12 --no-evaluation --compute-val-loss
# After training completes:
python evaluate.py --model best_model.h5 --val-data ...
```

### 3. Track the real process PID

Virtual environment `python.exe` on Windows is a redirector stub. `Start-Process` returns the stub PID (0 CPU, ~7MB RAM). The real training process is its child.

```powershell
# BAD — this kills the stub, not the trainer
Stop-Process -Id $stubPid

# GOOD — find the actual trainer by its child relationship
$stub = Get-Process -Id $stubPid -ErrorAction SilentlyContinue
$trainer = Get-CimInstance Win32_Process -Filter "ParentProcessId=$($stub.Id)" | Where-Object { $_.Name -eq "python.exe" }
if ($trainer) { Stop-Process -Id $trainer.ProcessId }
```

### 4. Verify multi-epoch completion

Check the training history keys:
```python
history = model.fit(...)
print(f"Epochs completed: {len(history.history['loss'])}")
# Should match --epochs, not 1
```

If `len(history.history['loss']) == 1`, the adapter isn't looping.

### 5. Match training and inference dimensions

Training image size must match inference:
```python
# Training
python train.py --image-min-side 400 --image-max-side 400

# Inference in app
resize_image(image, min_side=400)  # MUST match
```

Mismatched dimensions cause silent accuracy degradation, not crashes.

## When NOT to use

- PyTorch DataLoader (handles looping natively)
- Pure inference code (no training loop)
- Non-GPU training (no memory spike issues)

## Cross-references

- **debugging-and-error-recovery** — Apply structured debugging when training silently fails.
- **anti-phantom-symbols** — Verify TF/Keras API calls exist in the installed version. `Sequence`, `on_epoch_end`, and adapter internals change across versions.

## Lessons learned

Real bugs caught by this skill:
1. TF `KerasSequenceAdapter` produces few batches when `__len__` is small — make `__len__` return `len(seq)*1000` and wrap `__getitem__` with modulo + `on_epoch_end`
2. `sys.maxsize` as `__len__` causes OOM — the adapter does `list(range(len))` when `shuffle=True`
3. Per-epoch evaluation silently kills the process on 6GB GPUs — use `--no-evaluation` and evaluate once after training
4. venv `python.exe` on Windows is a redirector stub — the real PID is the child process
