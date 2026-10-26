---
name: python
description: Use when writing Python command-line tools, automation scripts, data pipelines, small web dashboards or machine-learning code — project layout with uv, standard-library-first CLIs, subprocess and API calls with retries, unittest or pytest, packaging and running on CPU-only machines. Also use when a script works locally but fails on a scheduler, in a hosted runtime, or after a Python version upgrade.
---

# Python

Default: the current stable CPython, `uv` for environments and dependencies, standard library first, `unittest` or `pytest`, one entry point per tool.

## Setup

1. `uv init` (or `uv venv` for scripts), `uv add <pkg>`, commit `uv.lock`. Run with `uv run`.
2. For single-file tools, declare dependencies inline (PEP 723 `# /// script` block) and run with `uv run script.py`; nothing to install globally.
3. Pin the interpreter (`.python-version`, `requires-python`). A hosted runtime may default to an older version than your machine; check before relying on new syntax.

## Writing tools that other tools can call

- Parse arguments with `argparse`; provide `--help`, `--dry-run` and `--json`.
- Write results to **stdout**, diagnostics to **stderr**, and return meaningful exit codes (0 ok, 1 findings, 2 usage error).
- Make reruns safe: write to a temporary file and `os.replace` it into place; check state before acting.
- Prefer `pathlib`, `subprocess.run([...], check=False, capture_output=True, text=True)` and explicit encodings (`encoding="utf-8"`).
- Wrap network calls with bounded retries and exponential backoff on transient errors only (5xx, rate limits, timeouts); do not retry on 4xx.
- Keep a local cache of the last good response so a tool can still produce output when the network is down, and say in the output that the cache was used.

## Testing

- `python -m unittest discover` needs nothing extra; use `pytest` when fixtures or parametrisation help.
- Mock the boundary (HTTP, subprocess, clock), not internal functions.
- For anything printed to users, test the text that matters, not formatting noise.
- Add a regression test for each bug before fixing it.

## Data and ML

- `pandas` for tabular work, but load with explicit `dtype`s and parse dates deliberately; silent type inference is a common source of wrong numbers.
- CPU-only machine learning: install the CPU wheel index of PyTorch so CUDA libraries are not pulled in, and cap threads (`torch.set_num_threads`) on shared machines.
- Keep random seeds explicit and log them with results.

## Verification loop

1. `uv run ruff check` (or `python -m pyflakes`) — no errors.
2. Tests pass.
3. Run the tool end to end once with real input and once with `--dry-run`.
4. Run with `python -I` when executing code near untrusted files: isolated mode ignores the current directory and user site-packages, so a planted module cannot shadow the standard library.

## Pitfalls

- **Module shadowing:** a local file named `json.py`, `random.py` or `test.py` silently replaces the standard module.
- **`importlib.reload`** does not reload modules that were imported by name into other modules; in hosted app runners it can raise. Restructure instead of reloading.
- **Package `__init__.py` with side effects:** if a runner imports a package as the entry point, code meant for `__main__` runs (or does not). Guard with `if __name__ == "__main__":`.
- **Tkinter is optional** in many distributions; a GUI tool must fall back to a CLI when it is missing.
- **Mutable default arguments** (`def f(x=[])`) persist between calls.
- **Time zones:** use aware datetimes (`datetime.now(tz=...)`); naive ones break around scheduling and comparisons.
- **Scheduled runs** (cron, systemd timers) have a minimal environment: no shell profile, different `PATH`, no virtualenv activation. Use absolute paths and `uv run`.
- **Long-running jobs on a shared PC:** use a lock file (`fcntl.flock`) so a second run does not start, and log progress so a killed run can resume.
