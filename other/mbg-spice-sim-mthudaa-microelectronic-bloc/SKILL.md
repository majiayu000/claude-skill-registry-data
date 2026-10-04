---
name: mbg-spice-sim
description: Runs ngspice simulations for analog blocks in this repository and turns the raw output into readable data, using mbg.simulation (run_spice, raw_to_csv, parse_dat). Use when the user asks to simulate a netlist, measure gain, bandwidth, delay or offset, sweep corners, or compare pre-layout against post-layout behaviour. Do not use it to generate layout (use mbg-spice-to-gds) or to run DRC, LVS or PEX (use mbg-ic-verify).
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-spice-sim/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG SPICE Simulation


## Preferred API: mbg.analysis.Testbench

`run_spice` is the transport. For anything beyond a raw deck use the analysis
layer, which builds a correct deck and parses the results:

```python
from mbg.analysis import Testbench, fft

tb = Testbench(netlist, cell="ota_5t",
               supplies={"vdd": 3.3, "vss": 0.0},
               sources={"inp": 1.65, "inm": 1.65, "vb": 0.8},
               probes=["out"])

tb.op()                       # operating point
tb.dc("inp", 0, 3.3, 0.01)    # DC sweep
tb.ac(1, 1e9, points=50)      # AC sweep  -> .bandwidth_3db("out")
tb.tran("1n", "1u")           # transient -> .peak_to_peak(), .cross()
tb.monte_carlo("op", runs=50) # mismatch spread -> .stats("out")
freq, mag = fft(result, "out")
```

Three traps it handles for you:

- **`design.ngspice` must be included before the model library.** The GF180
  device subcircuits declare 24 formal parameters, and the statistical ones
  (`par_vth`, `par_k`, `var_vth`, `p_sqrtarea`, ...) are *defined* in
  `design.ngspice`. Without it ngspice reports their missing defaults as
  `Syntax error: letter [$]`, `Mismatch: 24 formal but 15 actual params`,
  `Expression err: $` and finally `Formula() error` — one burst per device.
  All four messages are the same single root cause; `$` is ngspice's marker
  for "no default supplied", not a corrupt netlist.
- **Each analysis reads the file it wrote.** `dc`/`ac`/`tran` drop
  `dc.dat`/`ac.dat`/`tran.dat` into one workdir, so picking "the first .dat"
  hands back a previous analysis's data. A transient that comes back with the
  output node missing is this bug, not a probe problem.
- **AC data is complex.** `wrdata` writes `(freq, re, im)` triplets for AC and
  `(x, y)` pairs for dc/tran. Magnitude is stored under the probe name, with
  `<name>.re` / `<name>.im` alongside for phase.
- **`dc`/`ac`/`tran` probe every port by default**, not just the stimulus —
  recording only the swept source omits the response.
- **An AC source needs an AC magnitude.** Attaching it must match the source
  *line*, not a single-token value: a source written `DC 1.2` silently kept a
  magnitude of zero and returned an all-zero sweep. `ac()` now raises rather
  than returning that.
- **ngspice's exit code is unreliable** — it commonly returns non-zero after a
  `.control` block that succeeded. Results are judged by whether data appeared.
- **Monte Carlo needs the `statistical` corner with `sw_stat_mismatch=1`.**
  GF180 computes `delvto = mis_vth * sw_stat_mismatch`, and the `typical`
  corner leaves that switch at zero, so re-seeding alone returns the same
  number every run. `monte_carlo()` sets both.

## Purpose

Run ngspice on a netlist and read the results back as usable numbers. This skill
covers the pre-layout and post-layout simulation stages of the flow; it does not
build layout and does not run physical verification.

## When to Use

- The user asks to simulate a circuit, run a testbench, or check an operating point.
- The user asks for a measured quantity: DC gain, GBW, phase margin, delay, offset,
  power, or a temperature or corner sweep.
- The user wants a pre-layout versus post-layout comparison of the same block.

## When Not to Use

- Generating GDS from SPICE. Use `mbg-spice-to-gds`.
- DRC, LVS or PEX. Use `mbg-ic-verify`.
- Reading previous results without re-running anything. Use `mbg-design-regression`.

## Required Inputs

- A complete ngspice netlist **including its own analysis and control lines**.
  `run_spice` executes exactly what it is given; it does not append `.tran`,
  `.ac`, `.control` or `.end` for you.
- Model libraries referenced through `$PDK_ROOT`, not an absolute personal path.

## Preconditions

- `ngspice` is on PATH.
- `PDK_ROOT`, `PDK` and `PDKPATH` are set. Inside the IIC-OSIC-TOOLS container the
  project standard is `PDK_ROOT=/foss/pdks`, `PDK=gf180mcuD`. On a host install
  they point at the volare PDK root instead.
- Use `mbg.simulation.pdk_path(subpath)` to build PDK-relative paths rather than
  writing an absolute path into a netlist.

## Workflow

1. Confirm the netlist carries its own analysis statements and a `.end`.
2. Run it:

   ```python
   from mbg.simulation import run_spice, raw_to_csv, parse_dat, pdk_path

   r = run_spice(netlist_text, workdir="sim_out", fmt="raw")
   # r = {"stdout", "stderr", "returncode", "raw_path", "dat_paths", "workdir"}
   ```

   `workdir=None` uses a temporary directory that is cleaned up, so pass an explicit
   `workdir` whenever the artifacts need to survive the call.
   `fmt` selects the output form: `"raw"` (binary), `"dat"` (`wrdata` text), or `"both"`.

3. Check `returncode` first, then read `stderr` — ngspice frequently reports a
   convergence or model-resolution problem while still exiting 0, so a zero return
   code alone is not evidence that the simulation is meaningful.

4. Convert results for analysis:

   ```python
   csv_path = raw_to_csv(r["raw_path"])        # binary raw -> CSV
   columns  = parse_dat(r["dat_paths"][0])     # wrdata text -> column dict
   ```

5. Report measured numbers with the analysis that produced them. Do not infer a
   metric the netlist never asked for.

## Outputs

- A working directory containing the ngspice input and its raw or `.dat` output.
- CSV or parsed column data derived from those files.
- Measured values, each tied to the analysis that produced it.

## Failure Modes

- **`ngspice: command not found`** — the tool is not on PATH; this usually means the
  command is running on the host rather than inside the container.
- **Model or `.lib` not found** — `PDK_ROOT`/`PDKPATH` are unset or point at the wrong
  root. Rebuild the path with `pdk_path()` and re-check the environment.
- **Exit code 0 but empty or flat output** — the netlist had no analysis statement, or
  the analysis ran but every node sat at its initial condition. Read `stdout`.
- **Timeout** — `run_spice` defaults to 300 s. A long transient or corner sweep needs an
  explicit larger `timeout`; do not silently truncate the analysis to fit.

## Reporting Rules

Never report a simulation as passing without the artifact that shows it. Use the
project status vocabulary — `PASS`, `FAIL`, `PARTIAL`, `NOT RUN`, `NOT AVAILABLE` —
and prefer `NOT RUN` over an unsupported claim.
