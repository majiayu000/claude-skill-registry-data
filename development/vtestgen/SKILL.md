---
name: vtestgen
description: Scaffold a Makefile-driven, CPU-bus-controlled testbench project for an IP and generate a comprehensive set of self-checking testcases, validate each with make, and write a testcase list
---

# Verilog Testcase Generator

## Overview

This skill builds the IP-level test environment in two phases:

- **Phase A — Scaffold the bench project.** Parse `<ip>_top`, then generate a
  reusable, Makefile-driven simulation project under `tb/<ip>/`: build system,
  clock/reset generators, a DUT-instance core, CPU-bus BFM tasks, and one
  CPU-controllable stimulus driver per data interface.
- **Phase B — Plan and generate the suite.** Plan testcases across six mandatory
  categories, write each as a thin `tb_*.sv` that drives the bench **only through
  the CPU bus**, validate each with `make`, and write `tc_list.md`.

`vtestrun` later executes the suite through the same Makefile.

The input is an IP name. The outputs are:

```
tb/<ip>/Makefile              top dispatcher (auto-discovers tb_*.sv)
tb/<ip>/script/library.mk     per-testcase xvlog/xelab/xsim recipe
tb/<ip>/script/rtl.f          generated RTL hierarchy filelist
tb/<ip>/script/skip.list      names of skipped testcases, excluded by the Makefile
tb/<ip>/clock.vh              parameterized clock + sync-reset generators
tb/<ip>/dut.vh                reg-map, DUT signals/instance, sti instances, CPU BFM tasks + sequences
tb/<ip>/sti_<iface>.sv        one CPU-controllable stimulus driver per data interface
tb/<ip>/sco_<iface>.sv        one CPU-controllable scoreboard per checkable stream output (optional)
tb/<ip>/tb_<name>.sv          self-checking testcases (CPU-bus only)
tb/<ip>/tc_list.md            testcase index with status
tb/<ip>/sim/<tc>/             disposable build dirs
```

Template files for every artifact live in `templates/` next to this SKILL.md.
Treat them as the canonical shape; fill the `{{...}}` placeholders from the
parsed IP. Testbench code is SystemVerilog (`.sv`) — permitted under `tb/` (see
`.claude/skills/shared/CodingStyle.md`).

**Central design rule — the CPU bus is the single control plane.** Every testcase
drives the whole bench using only `cpu_write` / `cpu_read` / `cpu_read_check` (and
the higher-level sequences built on them in `dut.vh`). The DUT is configured over
the CPU bus; traffic generators live in separate `sti_*.sv` modules that are
themselves CPU-bus slaves, so the test script configures and starts stimulus with
`cpu_write` too.

## Prerequisites

| Tool  | Purpose             | Check             |
|-------|---------------------|-------------------|
| xvlog | compile / lint      | `xvlog --version` |
| xelab | elaborate           | `xelab --version` |
| xsim  | simulate            | `xsim --version`  |
| make  | build orchestration | `make --version`  |

If a required tool is missing, report it and stop — do not fake validation.

---

# Phase A — Scaffold the Bench Project

## Step A1 - Understand the IP and parse the top

Read before generating anything:

1. `./doc/<ip>.md` — full IP behavior, architecture, interface protocols, register map.
2. `./rtl/<ip>_top.v` — exact top-level port list, signal names, and widths.

Parse the top module header and **classify** every port:

| Class                    | How to detect | Bench treatment |
|--------------------------|---------------|-----------------|
| clock                    | name matches `clk*` / `*_clk` | generate in `clock.vh`, period param `T_<NAME>` |
| reset                    | name matches `rst*` / `*_rst*` / `*_n` | generate sync reset in `clock.vh` |
| CPU bus                  | `*cpu*`, or `*_we`/`*_oe`/`*_addr`/`*_din`/`*_dout`, or an APB/AXI-lite-ish group | wire to `cpu_*` and the BFM tasks; build the register map |
| data-plane in            | remaining inputs (valid/data/sof/eof/...) grouped by prefix | driven by an `sti_*.sv` module |
| data-plane out / status  | remaining outputs | status outputs: checked via CPU-readable status registers. A **stream** output (continuous `valid`/`data` beats) gets a `sco_*.sv` scoreboard (Step A6) for per-beat checking |

Also extract **parameters** (name + default, e.g. `DATA_W`, `ID_BIT`, `RS_LV`).

If the IP has **no** CPU bus, still generate the CPU bus in the bench as the
control plane for the `sti_*` drivers, and connect the DUT's data ports directly
to the sti outputs / to observation logic. Note this to the user.

Present a short parse summary (params, classified ports, detected clocks, detected
data interfaces → planned `sti_*` drivers, detected stream outputs → planned
`sco_*` scoreboards) **before** generating files. Adjust on feedback.

## Step A2 - Create the skeleton, copy the build system, generate rtl.f

Create folders `tb/<ip>/` and `tb/<ip>/script/` (and `sim/` is created on demand by
the Makefile). Never delete existing files; if `Makefile` / `script/library.mk`
already exist, diff against the template and only offer to update, do not overwrite
silently.

Copy verbatim:
- `templates/Makefile`   → `tb/<ip>/Makefile`
- `templates/library.mk` → `tb/<ip>/script/library.mk`

Generate `tb/<ip>/script/rtl.f` from `templates/rtl.f`: walk the instantiation
hierarchy of `<ip>_top` following `.claude/skills/shared/HierarchyFilelist.md`, and
list every required file as `RTL_FILES += $(RTL_FOLDER)/...` or
`$(LIB_FOLDER)/...`, top module first. Both Makefiles `include` this fragment, so
it is the single source of the compiled filelist (no wildcard globbing).

## Step A3 - Generate `tb/<ip>/clock.vh`

Expand `templates/clock.vh`: one `always` toggle per detected clock (period
`T_<NAME>`), one synchronous reset per clock domain using `RS_LV` (assert =
`RS_LV`, deassert after `10*T_<NAME>`). One clock is the "system" clock
(`{{SYS_CLK}}`, used by watchdog/run-length); the CPU bus uses `{{CPU_CLK}}` (may
be the same clock).

## Step A4 - Generate `tb/<ip>/dut.vh`

Expand `templates/dut.vh`:

- `{{REGISTER_MAP}}` — `localparam REG_<NAME> = 20'h..;` for every CPU register.
  Take real addresses from `doc/<ip>.md` or the RTL decode; if none exists, emit a
  clearly-marked TODO block with example registers.
- `{{DUT_SIGNALS}}` — declare every DUT port with exact widths/names: bench-driven
  inputs and the CPU bus as `reg`/handled by tasks, DUT outputs as `wire`,
  data-plane inputs as `wire` (driven by sti modules).
- `{{DUT_PARAM_MAP}}` / `{{DUT_PORT_MAP}}` — `.NAME(value)` lines; connect the CPU
  port group to `cpu_*`, data-plane ports to the matching `sti_*` outputs, clocks/
  resets to the generated names. The DUT read-data output connects to a
  `dut_cpu_dout` wire so it can be muxed.
- `{{STI_INSTANCES}}` — one instance per `sti_*.sv` (Step A5), each given a unique
  `STI_ADDR` on a **`0x100`-word window** (`STI_BASE`, `STI_BASE+'h100`, ...),
  sharing the CPU bus. **Bind `RS_LV` (and `DATA_W`) to the DUT's values** so the
  driver resets at the DUT's polarity — a driver left at the default `RS_LV=0`
  while the DUT is `RS_LV=1` is held in reset for the whole run.
- `{{SCO_INSTANCES}}` — one instance per `sco_*.sv` (Step A6), each given a unique
  `SCO_ADDR` on a **`0x100`-word window** (`SCO_BASE`, `SCO_BASE+'h100`, ...),
  sharing the CPU bus and tapping a DUT output. **Bind `RS_LV` (and `DATA_W`) to
  the DUT's values**, same as the sti drivers. Leave empty (and drop `SCO_BASE`)
  if no scoreboard is generated.
- **Each slave owns a 256-word window**, so its registers — including any
  width-dependent payload/capture that spans `NW = DATA_W/32` words — never reach
  the next slave's base (good for `DATA_W` up to 8192). Keep every slave base
  `0x100`-aligned and any word-addressed payload within its window.
- `{{STI_DOUT_OR}}` / `{{SCO_DOUT_OR}}` — OR of each sti / sco instance's `*_dout`
  for the read mux. Substitute `32'h0` for either term when that group is empty.
- `{{CPU_CLK}}` / `{{CPU_CLK_UPPER}}` — the CPU-domain clock name used by the BFM tasks.

The three BFM tasks (`cpu_write`, `cpu_read`, `cpu_read_check`) are already in the
template; keep them, only fix the clock name. `cpu_read_check` prints
`[FINISH] FAIL` + `$finish` on mismatch — this is the failure path of the contract.

Each access is held for a parameterized number of CPU clocks — `CPU_WR_LAT` for
writes, `CPU_RD_LAT` for reads (declared by the testcase, default 1). Set these
higher when the DUT's CPU slave needs more than one cycle per access; read data is
sampled at the end of the `CPU_RD_LAT` window while `cpu_oe` is still asserted. For
a slave with a variable-latency `ready`/`ack` handshake, poll that signal in the
task instead of using a fixed latency.

**Put reusable high-level sequences in `dut.vh`, not in the testcases.** Any
multi-step CPU sequence more than one testcase will repeat — load a key/config
block, trigger+poll a "done" bit, load a payload word-by-word, fire a beat and wait
for capture, read a payload back — belongs here as a task built on the BFM tasks
(e.g. `load_key`, `cfg_run`, `sti_load`, `sti_read`, `sti_beat`). Make them
width-generic by looping `0..NW-1` over the word-addressed `sti_*` registers. This
keeps every `tb_*.sv` to pure intent and lets a testcase at a different `DW` reuse
the exact same sequences. The template already ships a commented `arm_stream` /
`check_stream` pair (the driver↔scoreboard runtime-sync handshake from Step A5):
uncomment and keep it when the bench has an `sti_*`/`sco_*` pair, drop the sco half
otherwise.

## Step A5 - Generate `tb/<ip>/sti_<iface>.sv` per data interface

For each data-plane input group from Step A1, expand `templates/sti_template.sv`:

- Name it `sti_<iface>.sv`, module `sti_<iface>`.
- Keep the CPU-slave wrapper (write-decode of `ENA/RATE/MODE/SEED/CLR`, read-decode
  into `cpu_dout`, address self-decode from `STI_ADDR`) **unchanged** — this is what
  makes the driver controllable from the test script via `cpu_write` only.
- The `GENERATOR BODY` ships **MODE-selectable** (chosen at run time via the
  `MODE` register, no recompile): `MODE_LFSR` (pseudo-random, replicated to fill
  `DATA_W`), `MODE_COUNT` (byte-stream counter-up), and `MODE_FILE` (replay
  `DATA_W`-wide words from `PATTERN_FILE` via `$readmemh`). Keep the modes that
  fit this interface, add ones it needs (packet burst, AXI master, sof/eof
  framing, ...), and match the DUT's handshake (valid/ready) and data width. A
  per-project "specific pattern" belongs in a hex file driven by `MODE_FILE`, not
  hardcoded in the body.
- **Runtime sync with the mirroring `sco_*`.** The driver and scoreboard are two
  independent generators; the `CLR` register arms each one back to the start of its
  sequence (reseed from `SEED`, counters to 0) without a full DUT reset. The
  testcase syncs them by: write the **same** `MODE`/`SEED` to both → pulse `CLR` on
  both → enable the sco → enable the driver. This holds across DUT latency and
  back-pressure because the sco advances per accepted output beat, **but only when
  the DUT carries the stream 1:1 in order** (FIFO/CDC/passthrough). For a DUT that
  drops/reorders/transforms beats, the mirror is invalid — use a reference-model
  `sco_*` (Step A6). Put the arm-and-enable handshake in a `dut.vh` sequence so
  every testcase reuses it.
- **Wire the handshake `ready` on both sides.** The driver consumes the DUT
  *input* `ready` via its `out_ready` port — it holds each beat until accepted and
  advances only then, so it stays in lock-step with the sco under back-pressure;
  tie `out_ready` to `1'b1` in `dut.vh` if the input has no `ready`. The DUT
  *output* `ready` is only *tapped* by the sco — something else must drive it: tie
  it high for a plain run, or add a small ready/throttle driver (an `sti_*`-style
  CPU slave) for back-pressure testcases.
- Expose every output the DUT data port needs; expose status counters and any
  captured output as readable registers so testcases can `cpu_read_check` them.
- **Make the driver width-generic — never hardcode the data width.** Parameterise
  by the DUT's data width (`DW`, plus `UW`/`EW` sidebands), derive everything from
  it (`localparam NW = (DW+31)/32;`, `NB = DW/8;`). Every payload/capture register
  and `out_data` must be `[DW-1:0]`; the shipped modes already size off `DW`. A
  driver hardcoded to one width silently works at the default `DW` then fails the
  first multi-block (`DW=N*128`) testcase.
- If a testcase must push an **exact payload over the CPU bus** (rather than via
  `MODE_FILE`), expose it as **word-addressed** registers — the CPU is 32-bit — at
  a base offset (`PT` word `i` at `STI_PT+i`, `i = 0..NW-1`) decoded with a range
  check + variable indexed part-select (`pt[(cpu_addr-STI_PT)*32 +: 32]`), exactly
  the same way `sco_template.sv` word-addresses its capture payload. Such a payload
  occupies `NW` CPU words, so the slave's address stride must clear it (see Step A4).

Additional `sti_*.sv` files can be added later; they are picked up automatically by
the `sti_*.sv` glob in the Makefiles.

## Step A6 - Generate `tb/<ip>/sco_<iface>.sv` per checkable stream output (optional)

Generate a scoreboard only for data-plane outputs that produce a **continuous
stream** (`valid`/`data` beats), where per-beat checking adds value over reading a
final status register. Skip it for IPs whose only outputs are status registers —
those are checked directly with `cpu_read_check`. If no scoreboard is generated,
also drop the `SCO_INSTANCES`/`SCO_DOUT_OR`/`SCO_BASE` hooks from `dut.vh`.

For each such output, expand `templates/sco_template.sv`:

- Name it `sco_<iface>.sv`, module `sco_<iface>`.
- Keep the **CPU-slave wrapper unchanged** (write-decode of `ENA/MODE/SEED/CLR`,
  read-decode of `ERRCNT/CHKCNT` + word-addressed first-mismatch capture, address
  self-decode from `SCO_ADDR`). This is what lets the test script configure and read
  the scoreboard via the CPU bus only.
- The scoreboard **taps** the DUT output (`in_valid`/`in_ready`/`in_data`) — it must
  never drive the DUT. Wire the tap in `dut.vh`'s `{{SCO_INSTANCES}}`.
- Replace only the `COMPARE BODY` to match the interface handshake. **Default:** the
  scoreboard **regenerates** the expected stream itself from `MODE`/`SEED`/
  `PATTERN_FILE` — the same `MODE_LFSR`/`MODE_COUNT`/`MODE_FILE` sources as
  `sti_*.sv` — so no expected payload is pushed over the CPU bus. The testcase just
  sets the scoreboard's `MODE`/`SEED` to match the driver feeding the DUT.
  **Alternatives:** build a reference model that recomputes expected from observed
  DUT inputs (use only when the transform is non-trivial); or, for irregular
  expected data, add a word-addressed `EXP` register written by the testcase.
- On a mismatch the scoreboard prints `[ERROR] ...` then `[FINISH] FAIL` + `$finish`
  (self-fail, consistent with `cpu_read_check`). `ERRCNT` is still exposed so a
  testcase may instead defer the verdict with `cpu_read_check(SCO_ERRCNT, 32'd0)`.
- **Width-generic** like the sti drivers — parameterise by `DATA_W`, derive `NW`/`NB`
  from it, word-address the capture payload, never hardcode the width.

Additional `sco_*.sv` files are picked up automatically by the `sco_*.sv` glob in the
Makefiles.

---

# Phase B — Plan and Generate the Suite

## Step B1 - Plan the test suite

List all planned testcases across the six mandatory categories:

| Category       | Coverage target |
|----------------|-----------------|
| Reset          | DUT reaches defined idle state after reset; all outputs at documented reset values |
| Basic          | One test per documented feature or operating mode |
| Edge           | Boundary data values (0, all-ones, max-minus-1), empty/full conditions, single-cycle bursts |
| Back-pressure  | Valid/ready handshakes held off; pipeline stalls and drains correctly under sustained back-pressure |
| Error inject   | Out-of-spec stimulus, concurrent events, overflow/underflow conditions |
| Stress         | Back-to-back transactions with no idle cycles; maximum throughput for at least 1000 clock cycles |

Present the full plan as a table before writing any code. Adjust on feedback.

## Step B2 - Write each testcase

For each planned testcase, create `tb/<ip>/tb_<category>_<name>.sv` by expanding
`templates/tb_basic.sv`. File name lowercase, underscores, no spaces, `tb_` prefix
(so the Makefile auto-discovers it).

Each testcase must:

- declare the clock-period params (`T_*`), `RS_LV` (set to the DUT's own `RS_LV`
  default parsed from `<ip>_top`, so the bench resets at the DUT's polarity), the
  cpu access latencies (`CPU_WR_LAT`, `CPU_RD_LAT`), and clk/rst regs, then
  `` `include "clock.vh" ``;
- declare the DUT parameters, then `` `include "dut.vh" ``;
- contain a watchdog `initial` that prints `[FINISH] FAIL` on timeout;
- have a single test-script `initial` block that uses **only** the reusable
  sequences from `dut.vh` plus `cpu_write`/`cpu_read`/`cpu_read_check` to: release
  reset, configure the DUT, configure+start the `sti_*` drivers, let traffic run,
  check status/captured output via `cpu_read_check`, and finish with `[FINISH] PASS`.

Keep the testcase thin — sequence calls and the golden check, no bus-level poking
and no direct access to DUT or sti internals.

### Checking and verdict convention

- Status/register outputs are checked with `cpu_read_check` against CPU-readable
  registers. On mismatch it prints `[ERROR] time= ... MISMATCH ...` then
  `[FINISH] FAIL` and `$finish` automatically.
- **Stream outputs are checked by their `sco_*` scoreboard:** the test script sets
  the scoreboard's `MODE`/`SEED` to match the driver feeding the DUT and enables it
  with `cpu_write`; the scoreboard regenerates the expected stream and self-fails on
  the first mismatched beat. For a deferred verdict, end the run and
  assert `cpu_read_check(SCO_ERRCNT, 32'd0)` instead. Either way the test script
  still touches the bench only through the CPU bus.
- For extra diagnostic context before a manual failure, print an `[ERROR] time= ...`
  line with the relevant signal values, then `[FINISH] FAIL` and `$finish`.
  `vtestrun` harvests `[ERROR]` lines into the issue report.
- A passing testcase ends with `[FINISH] PASS` then `$finish`. This token is the
  single machine-readable verdict (see `.claude/skills/shared/CodingStyle.md`).

For an algorithmic block, also emit a second testcase at a non-default width
(`DW=N*128`, etc.) that reuses the same `dut.vh` sequences — it proves the generated
`sti_*.sv` is genuinely width-generic.

## Step B3 - Self-check each testcase with make

Run from inside `tb/<ip>/`:

```bash
make tb_<category>_<name>
```

This compiles RTL + `sti_*.sv` + the one testcase, elaborates, and simulates under a
timeout.

**The self-check is a structural gate, not a verdict.** It passes when the testcase
produces a clean `[FINISH]` token — `PASS` **or** `FAIL` — within the timeout. The
goal is a well-formed, runnable testcase, not a passing DUT. Determining the
authoritative pass/fail is `vtestrun`'s job. Do **not** tune a testcase to force
`[FINISH] PASS`: that can hide a real DUT bug.

> Re-run note: `make tb_<name>` is a no-op while a `simulate.log` already exists for
> that testcase. After editing, clear the stale result first — `make cleanf` (drops
> non-PASS sim dirs) or `rm -rf sim/tb_<name>` — then re-run.

| Result | Action |
|--------|--------|
| compile error (xvlog)    | fix signal name/width/port-map in `dut.vh` or the sti module; clear + rerun |
| elaborate error (xelab)  | add the missing RTL/lib file to `rtl.f`; confirm each `sti_*.sv` compiled; clear + rerun |
| sim timeout (no `[FINISH]`) | stimulus never started or DUT stalled — check the `cpu_write` enable sequence / handshake; clear + rerun |
| no `[FINISH]` token      | testcase ended without printing the verdict — fix the result block; clear + rerun |
| `[FINISH] FAIL`          | the testcase ran cleanly — self-check **passes**. First confirm the testcase's own expected value is correct: if it is wrong, fix it; if the expected value is right and the DUT disagrees, leave it — that is a real finding for `vtestrun`/`vdebug`. Either way mark the testcase `OK`. |

Maximum 2 rewrite attempts per testcase. If after 2 attempts it still cannot produce
a clean `[FINISH]` (compile/elaborate error, or timeout with no token), record it as
`SKIPPED` in `tc_list.md` and continue. Do not block the suite on one testcase.

## Step B4 - Write the testcase list

After all testcases are written and self-checked, write `tb/<ip>/tc_list.md`:

```markdown
# Testcase List: <ip>

## Bench

Makefile-driven project at `tb/<ip>/`. Run a testcase with `make tb_<name>`;
summarize with `make report`. RTL filelist: `tb/<ip>/script/rtl.f`. `SKIPPED`
testcases are mirrored into `tb/<ip>/script/skip.list`, which the Makefile excludes
from `make`/`make report` (the `.sv` files stay in place).

## Testcases

| # | File | Module | Category | Description | Status |
|---|------|--------|----------|-------------|--------|
| 1 | tb_reset_basic.sv | tb_reset_basic | Reset | DUT reaches idle after reset | OK |
| 2 | tb_basic_stream.sv | tb_basic_stream | Basic | Single packet flows end-to-end | OK |
| 3 | tb_edge_empty.sv | tb_edge_empty | Edge | Empty input condition | SKIPPED |
```

Status values: `OK` (well-formed testcase — self-check produced a clean `[FINISH]`,
PASS or FAIL), `SKIPPED` (could not produce a clean `[FINISH]` after 2 attempts).
A testcase whose `[FINISH] FAIL` reflects a real DUT bug is still `OK` here — the
failure is reported by `vtestrun`, not hidden at generation time.

Then **regenerate** `tb/<ip>/script/skip.list` as a mirror of the current `SKIPPED`
rows: overwrite it with exactly the testcase names (e.g. `tb_edge_empty`) whose
status is `SKIPPED`, one per line. Always rewrite from the current `tc_list.md` —
do not append. This way a previously-skipped testcase that now self-checks clean is
`OK` in `tc_list`, so it drops out of `skip.list` automatically and the Makefile
runs it again; a testcase still skipped stays excluded. `tc_list.md` is the single
source of truth; `skip.list` is just its machine-readable projection for the
Makefile. If no testcase is skipped, write an empty `skip.list` (or omit it).

## Conventions (must hold)

- **CPU-bus-only:** test scripts touch the bench only through the CPU BFM tasks and
  `dut.vh` sequences. No direct poking of DUT or sti internals from `tb_*.sv`.
- **Verdict:** print `[FINISH] PASS` / `[FINISH] FAIL` then `$finish`; `cpu_read_check`
  auto-fails on mismatch; no token ⇒ FAIL.
- **Width-generic** `sti_*.sv`, `sco_*.sv`, and `dut.vh` sequences — never hardcode the data width.
- **Reset-polarity-generic:** `sti_*.sv`/`sco_*.sv` reset against their `RS_LV` parameter, never a hardcoded `!rst_n`; `dut.vh` binds `RS_LV` on every sti/sco instance to the DUT's value (the bench reset in `clock.vh` is already `RS_LV`-driven).
- **Scoreboards are CPU-slave observers:** a `sco_*.sv` taps a DUT output and never drives it; it is configured/read over the CPU bus like any other slave.
- **Reusable sequences live in `dut.vh`**, not in testcases.
- Testbench is SystemVerilog under `tb/`; RTL stays Verilog-2005.

## Known Issues and Fixes

### [xsim] - unpacked array local to a `function automatic` is not retained per-index
**Symptom:** A reference-model `sco_*.sv` (or any TB function) that builds a table
in a local unpacked array — e.g. `reg [31:0] rk [0:31];` inside a
`function automatic` — produces wrong results; on inspection **every element reads
back as element 0** (the array does not hold per-index writes across the function
body in xsim 2020.2). For a cipher reference model this silently runs every round
with `rk[0]`, so the scoreboard flags a (spurious) DUT mismatch.
**Cause:** xsim mis-handles unpacked-array automatic-function locals.
**Fix:** use a **packed** vector and part-select instead:
`reg [1023:0] rkv; rkv[32*i +: 32] = val;  ... rkv[32*j +: 32]`. Packed locals work
reliably. (Module-level unpacked `reg` arrays in RTL are fine — this is specific to
automatic-function locals.)

### [make] - `#` inside `$(shell …)` breaks Makefile parsing
**Symptom:** `make` aborts with "unterminated call to function 'if': missing ')'".
**Cause:** GNU make treats `#` as a comment even inside `$(shell …)`, so a `sed`
program containing `#` (e.g. `sed 's/#.*//'` for the skip.list) truncates the line.
**Fix:** escape it — `sed 's/\#.*//'`. (Already fixed in `templates/Makefile`; keep
it escaped if you hand-edit.)

### [xsim] - testcase `RS_LV` must be 1-bit for the reset-release compare
**Symptom:** every testcase hangs to the watchdog with no output; the test script
is stuck at `wait (rst_n_clk === ~RS_LV)`.
**Cause:** declaring `parameter RS_LV = 0` makes it 32-bit, so `~RS_LV = 32'hFFFF_FFFF`
never `===` the 1-bit `rst_n_clk`.
**Fix:** declare `parameter RS_LV = 1'b0` in every testcase (as the `tb_basic.sv`
template does). Keep it 1-bit.

### [xsim] - cannot part-select a sized literal
**Symptom:** `syntax error near '['` on a line like `cpu_write(REG, 128'h..[127:96])`.
**Cause:** a part-select/bit-select directly on a sized literal is illegal.
**Fix:** assign the constant to a `localparam`/`reg` first, then slice that
(`localparam [127:0] V = 128'h..; ... V[127:96]`).

### [Verilog] - `always @(*)` with a constant-only RHS may never fire
**Symptom:** an output driven by `always @(*) y = {W{1'b0}};` stays `X` in sim.
**Cause:** the block has an empty sensitivity list (no signals on the RHS), so it
is not guaranteed to execute. **Fix:** drive constants with a continuous `assign`
(make the port a `wire`), or include a real signal in the block.
