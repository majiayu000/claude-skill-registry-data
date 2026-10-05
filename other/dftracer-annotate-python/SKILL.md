---
name: dftracer-annotate-python
description: Python annotation rules for dftracer — decorator usage, initialize/finalize, comp types, class methods, and quick checklist
---

## Python Annotation Rules (dftracer)

### Python Rule 1 — Use the decorator for regular functions

```python
from dftracer.logger import dftracer_fn, dft_fn

@dftracer_fn(cat="IO")            # cat groups functions in the trace viewer
def my_read(path: str, size: int) -> bytes:
    ...
```

- The `@dftracer_fn` decorator wraps the function with START/END automatically.
- `cat` (category) is required — use a meaningful group name: `"IO"`, `"Compute"`,
  `"MPI"`, `"Data"`, `"Init"`, etc.
- `dft_fn` is an alias for `dftracer_fn` — prefer `dftracer_fn` for clarity.
- Apply at every function that qualifies under **Rule 0** (see dftracer-annotate-general skill).

### Python Rule 2 — Initialize and finalize the tracer

```python
from dftracer.logger import DFTracer

# At program entry (after MPI.Init if using mpi4py)
tracer = DFTracer.initialize_log(
    log_file="traces/my_app",    # prefix for .pfw trace files
    data_dir="/data",            # directory to monitor for I/O events
    process_id=rank,             # Pointer to MPI rank or 0 for single-process
)

# At program exit (before MPI.Finalize if using mpi4py)
DFTracer.finalize_log()
```

- **With mpi4py**: call `DFTracer.initialize_log` AFTER `MPI.Init()`.
- **With mpi4py**: call `DFTracer.finalize_log()` BEFORE `MPI.Finalize()`.
- Use `process_id=NULL` for single-process runs.

### Python Rule 3 — Environment-variable initialization (alternative)

```bash
export DFTRACER_ENABLE=1
export DFTRACER_LOG_FILE=/tmp/traces/my_app
export DFTRACER_DATA_DIR=/data
python my_app.py
```

The env var only handles INIT/FINI — decorators are still needed for function-level spans.

### Python Rule 4 — Context manager for ad-hoc regions

```python
from dftracer.logger import DFTracer

tracer = DFTracer.get_instance()
with tracer.get_time("IO", "read_loop"):
    for chunk in data:
        process(chunk)
```

Only use context managers when the code block is too coarse-grained to fit a function decorator.

### Python Rule 5 — Classify every annotated function with comp=TYPE

```python
from dftracer.logger import dftracer_fn

@dftracer_fn(cat="IO", comp="io")
def read_checkpoint(path: str) -> dict: ...

@dftracer_fn(cat="COMM", comp="comm")
def broadcast_weights(tensor, comm): ...

@dftracer_fn(cat="CPU", comp="cpu")
def compute_checksum(data: bytes) -> str: ...

@dftracer_fn(cat="MEM", comp="mem")
def copy_batch(src, dst) -> None: ...
```

**Types:** `"io"`, `"mem"`, `"cpu"`, `"comm"` — same taxonomy as C.

If `dftracer_fn` doesn't accept `comp` as a keyword argument:
```python
@dftracer_fn(cat="IO")
def read_checkpoint(path: str) -> dict:
    DFTracer.get_instance().update("comp", "io")   # fallback
    ...
```

### Python Rule 6 — Skip trivial functions (Rule 0 applies)

```python
# ✅ Annotate — does real file I/O
@dftracer_fn(cat="IO")
def read_checkpoint(path: str, rank: int) -> dict:
    with open(path, "rb") as f:
        return pickle.load(f)

# ❌ Skip — trivial property
@property
def rank(self) -> int:
    return self._rank

# ❌ Skip — one-liner string helper
def _fmt_path(self, p: str) -> str:
    return str(Path(p).resolve())
```

### Python Rule 7 — Class methods

```python
class DataLoader:
    @dftracer_fn(cat="IO")
    def load(self, path: str, batch_size: int) -> list:
        ...

    @dftracer_fn(cat="IO")
    def write(self, path: str, data: bytes) -> None:
        ...

    def _validate(self, x):      # ❌ skip — trivial helper
        return x is not None
```

### Python Quick checklist

- [ ] `from dftracer.logger import dftracer_fn` imported at top of file
- [ ] `DFTracer.initialize_log(...)` called at program entry (after MPI.Init if applicable)
- [ ] `DFTracer.finalize_log()` called at program exit (before MPI.Finalize if applicable)
- [ ] ALL non-trivial functions decorated — skip only pure getters/one-liners
- [ ] `@dftracer_fn(cat="<CATEGORY>", comp="<type>")` on every annotated function
- [ ] `comp` is one of `"io"`, `"mem"`, `"cpu"`, `"comm"`
- [ ] Category names are consistent across the codebase
- [ ] For mpi4py: initialize AFTER MPI.Init(), finalize BEFORE MPI.Finalize()
