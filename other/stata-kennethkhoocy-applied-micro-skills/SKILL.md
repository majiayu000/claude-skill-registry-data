---
name: stata
description: >-
  Use this skill whenever the user asks to run Stata commands, estimate econometric models,
  work with .dta files, run a .do file, generate Stata output, or do any statistical analysis
  where Stata is involved. Also trigger when the user mentions Stata variables, Stata syntax,
  or econometric tasks where Stata is the natural tool, including regressions, IV estimation,
  diff-in-diff, RDD, panel data, clustering, summary statistics, and margins. Stata runs
  through pystata on StataNow 19.5 BE; configure once with stata_setup, then drive everything
  with stata.run() and exchange data directly with pandas. Prefer this skill over subprocess
  calls or .do-file shelling for Stata work, including cases where the user does not say
  pystata.
---

# Stata Skill — pystata on StataNow 19.5 BE

Run Stata entirely through **pystata**, the official Python integration that
ships with Stata. Configure the session once, then issue every command — and
run every `.do` file — with `stata.run()`. Data crosses between Python and
Stata in memory through pandas, so there is no need to write intermediate
`.dta` files or read `.log` files unless the user wants them.

## The one rule that matters most

**Always execute Stata through pystata.** Both individual commands and entire
`.do` files go through `stata.run(...)`. Never launch `StataBE-64.exe` as a
subprocess and never run a do-file in batch mode — pystata keeps a single live
Stata session in the Python process, gives direct access to data and stored
results, and raises real Python exceptions on errors. Running a do-file is just
`stata.run('do "path/to/file.do"')`.

## Setup

This machine has **StataNow 19.5 BE** at `C:\Program Files\StataNow19`, and it
is already on PATH. `pystata` and `stata_setup` are installed for the system
Python (3.14). Basic Edition (BE) is the only licensed edition; `"se"` and
`"mp"` cannot be initialized.

Configure once per Python process:

```python
import stata_setup
stata_setup.config(r"C:\Program Files\StataNow19", "be")
from pystata import stata
```

For clean output without the StataCorp splash banner, drive `pystata.config`
directly instead:

```python
import sys
sys.path.insert(0, r"C:\Program Files\StataNow19\utilities")
import pystata
pystata.config.init("be", splash=False)
from pystata import stata
```

`config.init` can run only once per process; to start over, launch a fresh
Python process.

## Bundled helper (optional)

`scripts/stata_runner.py` removes the boilerplate: it bakes in the path and
edition, configures pystata lazily on first use, and wraps command-running,
output capture, and data exchange. Reach for it when a script makes several
Stata calls.

```python
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/stata/scripts"))
import stata_runner as sr

sr.run("sysuse auto, clear")
log = sr.run("regress price mpg weight, robust", capture=True)
print(log)
print("R-squared:", sr.ereturn()["e(r2)"])
```

The plain three-line pattern above works just as well; the helper is a
convenience, not a requirement.

## Running commands

```python
stata.run("""
    sysuse auto, clear
    summarize price mpg weight
    regress price mpg weight i.foreign, robust
""")
```

`stata.run(cmd, quietly=False, echo=False)` accepts one command or several
newline-separated commands. `quietly=True` suppresses output while still
storing results; `echo=True` echoes each command line.

## Capturing output

Output prints to stdout by default. To capture it as a string, redirect stdout:

```python
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    stata.run("regress price mpg weight, robust")
log = buf.getvalue()
```

For a persistent `.log` on disk, tee through `set_output_file` — see
`references/pystata-api.md`.

## Error handling

A failing command **raises `SystemError`**, with a message ending in the Stata
return code such as `r(111);`. Catch it directly; there is no log to parse.

```python
try:
    stata.run("regress price nonexistent_var")
except SystemError as e:
    print("Stata error:", e)   # ".. variable nonexistent_var not found  r(111);"
```

Common codes: `r(111)` variable not found, `r(198)` syntax error, `r(601)`
file not found, `r(2000)` no observations.

## Data exchange with pandas

Move data in memory — no `.dta` files needed.

```python
import pandas as pd

# pandas -> Stata (replaces the dataset in memory)
stata.pdataframe_to_data(df, force=True)

# Stata -> pandas
df = stata.pdataframe_from_data()                 # whole dataset
prices = stata.pdataframe_from_data(var=["price", "mpg"])
labeled = stata.pdataframe_from_data(valuelabel=True)   # labels, not codes
```

Named **frames** let several datasets coexist:
`stata.pdataframe_to_frame(df, "aux")` and `stata.pdataframe_from_frame("aux")`.
`numpy` arrays have the parallel `nparray_*` calls. Full options are in
`references/pystata-api.md`.

If the user explicitly wants a `.dta` artifact, write one from Stata
(`save "out.dta", replace`) or from pandas (`df.to_stata("out.dta")`).

## Reading stored results

After any command the stored results are plain Python dicts:

```python
stata.run("summarize price", quietly=True)
r = stata.get_return()        # {'r(mean)': 6165.26, 'r(N)': 74.0, ...}

stata.run("regress price mpg weight", quietly=True)
e = stata.get_ereturn()       # {'e(N)': 74.0, 'e(r2)': 0.4996, 'e(b)': <ndarray>, ...}
```

Scalars are floats, macros are strings, and matrices (`e(b)`, `e(V)`) come back
as numpy arrays. For single values inside `python:` blocks, the bundled `sfi`
module exposes `Scalar`, `Macro`, `Matrix`, and `Data` — see the reference.

## Running an existing .do file

```python
stata.run('do "C:/path/to/analysis.do"')
```

Capture its output with the same `redirect_stdout` pattern if the user wants
the log. The do-file shares the live session, so any data or results it leaves
behind are immediately reachable from Python.

## BE edition constraints

StataNow 19.5 BE differs from SE/MP:

- **Variable ceiling of 2048** (`c(maxvar)`); SE allows 32,767 and MP up to
  120,000. Trim wide datasets with `keep`/`drop` before loading, or the load
  fails.
- **Single computational core** for estimation — BE has no MP parallelism, so
  very large models run slower.
- **`set matsize` is irrelevant** — it was removed in Stata 16; matrix size is
  managed automatically. Do not reintroduce it.
- Most commands run unchanged in BE; the practical limits are dataset width and
  speed, not command availability.

## Stata 19 capabilities (absent in the old Stata 16 setup)

Because this is Stata 19, several things the previous version could not do are
now available:

- **`didregress` / `xtdidregress`** for difference-in-differences (introduced in
  Stata 17). For the user's applied-micro work, still prefer `reghdfe` for
  high-dimensional or staggered-adoption designs; reach for modern estimators
  (`csdid`, `did_multiplegt`) when treatment timing varies.
- **`python:` blocks** inside do-files, with `sfi` for reading and writing Stata
  objects from Python.
- **Frames** with full Python integration, as shown above.

## Econometric workflow conventions

These reflect the user's applied-microeconomics practice. Follow them unless the
user says otherwise.

**Standard errors.** Default to robust (`, robust`) for cross-sectional
regressions. For panel data, cluster at the unit level (`, vce(cluster panelid)`).
Honor any clustering variable the user specifies. When the clustering level is
genuinely ambiguous, ask, because it is a consequential choice.

**Estimation.** For IV use `ivregress` and always report the first-stage
F-statistic (`estat firststage` after `ivregress 2sls`). For high-dimensional
fixed effects prefer `reghdfe` (`reghdfe y x, absorb(id year) cluster(id)`); for
simpler panels `xtreg` or `areg` are fine, and always `xtset` before `xtreg`.

**Output.** For side-by-side specifications use `esttab` from the `estout`
package; do not use `outreg2`. Display N and R-squared prominently.

**Data inspection.** On an unfamiliar dataset run `describe`, `summarize`, and
`codebook, compact` first, and flag missing values, string-encoded numerics, and
duplicate ID values.

User-written commands (`reghdfe`, `ftools`, `estout`, `csdid`) install with
`ssc install <pkg>` from inside a `stata.run(...)` call. Check availability with
`which <cmd>` before assuming a package is present.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `FileNotFoundError: ... shared library` on `init("se"/"mp")` | Only BE is installed/licensed | Initialize with `"be"` |
| `init` raises "already initialized" | `config.init` called twice in one process | Guard with `pystata.config.is_stata_initialized()`, or use a fresh process |
| `SystemError: ... r(111);` | Stata command error (here, variable not found) | Read the code in the message; fix the command |
| Output is empty when captured | Command run with `quietly=True` | Drop `quietly`, or read results via `get_return()`/`get_ereturn()` |
| Load fails on a wide dataset | Exceeds BE's 2048-variable ceiling | `keep`/`drop` columns before `pdataframe_to_data` |
| `unrecognized command` for a user package | Not installed | `stata.run("ssc install <pkg>")`, then retry |

## What this skill does not do

- It does not launch a Stata GUI window.
- It does not call `StataBE-64.exe` as a subprocess or run do-files in batch
  mode — everything goes through pystata's live session.
- It does not leave permanent `.do` files for the user to run by hand unless
  they ask for one.
