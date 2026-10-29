---
name: mbg-agent-interface
description: How any AI agent drives MBG through its tool surface — the `scripts/mbg` command line or the same tools over MCP (`scripts/mbg mcp`) — discovering what is legal, checking and simulating a netlist, generating and inspecting a layout, steering placement with a hints file, verifying, and reading the one-JSON-envelope result of every call. Use at the start of any design, simulation, layout or verification task in this repository, whatever the harness. Do not use it to change the tools themselves (edit src/mbg/agent/) or for repository setup (use mbg-setup).
metadata:
  short-description: How any AI agent drives MBG through its tool surface — the `scripts/mbg` command line or the same tools over MCP (`scripts/mbg mcp`) — discovering what is…
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-agent-interface/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# Driving MBG as an AI designer

MBG is an EDA you operate by text. Every stage of the analog flow is one tool
call that returns **one small JSON document**; bulk data (logs, waveforms,
reports, GDS) stays on disk and is named in the result. You never write a
Python driver script to run a stage.

Two equivalent surfaces, one registry (`src/mbg/agent/registry.py`):

| surface | how | use it when |
| :--- | :--- | :--- |
| command line | `scripts/mbg <group> <action> [args]` | always works — any harness with a shell (Pi, Codex, OpenCode, Claude Code, Deep Code, …) |
| MCP (stdio) | `scripts/mbg mcp` — configured in `.mcp.json`, `.codex/config.toml`, `opencode.jsonc`, `.cursor/mcp.json`, `.gemini/settings.json` | the harness lists `mbg` MCP tools (`doctor`, `pdk`, `design`, `netlist_check`, `sim_run`, `measure_vref`, `measure_ota`, `spec_check`, `layout_generate`, `layout_view`, `verify`, `flow_run`, `job`) |

`scripts/mbg` finds the repository from its own path and picks the
interpreter from `$MBG_PYTHON`, `$MBG_VENV`, `<repo>/.venv`, then `python3`.
`python -m mbg` is the same program.

## 1. Discover before you design

```bash
scripts/mbg doctor                      # tools, versions, installed PDKs — read this first
scripts/mbg tools                       # every tool, one line each
scripts/mbg tools measure.vref          # one tool's full input schema and examples
scripts/mbg pdk info --pdk gf180mcuD    # legal devices, terminal order, W/L limits, corners, sign-off decks
scripts/mbg pdk info --section devices  # a slice of it
```

`pdk info` is the authority on what you may instantiate. Do not guess model
names, terminal orders or units — gf180mcuD sizes carry an explicit `u`,
sky130A sizes are in microns without a suffix, and both are reported there.

## 2. The result envelope (`mbg.result/1`)

```json
{"schema": "mbg.result/1", "tool": "layout.generate", "ok": true,
 "status": "PASS", "summary": "one line",
 "metrics": {"area_um2": 989.1, "drc_magic": 0, "lvs": "match"},
 "artifacts": {"gds": "outputs/vref1/layout/vref1.gds"},
 "issues": [{"code": "LVS_MISMATCH", "severity": "error", "message": "…", "hint": "…"}],
 "next": ["mbg verify pex …"], "run_dir": "outputs/vref1/layout", "elapsed_s": 41.2}
```

* `status` is one of `PASS`, `FAIL`, `PARTIAL`, `NOT RUN`, `NOT AVAILABLE` —
  the AGENTS.md labels. `ok: false` means the **tool** broke (see `error`);
  `status: FAIL` with `ok: true` means the **design** failed a check.
* Exit codes: 0 PASS · 1 FAIL/PARTIAL · 2 usage error · 3 NOT RUN/NOT AVAILABLE · 4 job still running.
* `issues[].hint` says what to change. `next` lists the calls that usually follow.
* Stdout carries only the envelope; everything the stage printed is in
  `<run_dir>/log.txt`. Read that file only when the envelope is not enough
  (`--verbose` mirrors it to stderr).
* A checker that did not run is `NOT RUN`/`NOT AVAILABLE`, never a pass.

## 3. The design loop

```bash
scripts/mbg design init vref1 --pdk gf180mcuD --netlist vref.spice \
    --prompt "1.2 V reference, VDD 3.3 V" --model "<model id>"   # workspace outputs/vref1/
scripts/mbg netlist check --design vref1          # before anything else: models, units, body ties, ceiling
scripts/mbg sim run --design vref1 --analysis op --supplies '{"VDD":3.3,"VSS":0}' \
    --isources '{"IBIAS":20e-6}' --probes VREF PG  # internal nets are probed by name
scripts/mbg measure vref --design vref1 --spec vref_md --corners all
scripts/mbg layout generate --design vref1        # layout + Magic/KLayout DRC + LVS + PEX
scripts/mbg layout view --design vref1            # ASCII floorplan, device boxes, failures
scripts/mbg measure vref outputs/vref1/layout/vref1.pex.spice --post-layout --spec vref_md --corners all
scripts/mbg design status vref1                   # every stage's status in one view
```

Or one call for the whole chain:
`scripts/mbg flow run --design vref1 --recipe vref --spec vref_md`
(`--recipe` is `vref`, `ota` or `none`; `--recipe-args` passes the recipe's
own arguments as JSON).

* `--design <name>` puts each stage under `outputs/<name>/<stage>/` and keeps
  `experiment.json` current. Without it a run lands in `outputs/runs/<id>/`.
* Give the model identifier with `design init --model`; AGENTS.md requires it.
* Arrays take several words (`--probes VREF PG`, `--corners typical ss ff`);
  objects take inline JSON or a path to a `.json` file.
* Change one thing per candidate, keep a log of candidates and results, and
  bound the loop (AGENTS.md: every refinement loop has a maximum).

## 4. Steering placement — hints instead of drag and drop

`layout view` reports devices, rows and coordinates in the same terms a hints
file uses. Edit the file, re-run `layout generate --hints file.json`:

```json
{"rows":   {"XM5": 1, "XM6": 1},
 "order":  {"3": ["XR2a", "XR2b", "XR1", "XR2c", "XR2d"]},
 "groups": [{"kind": "diff_pair", "devices": ["XM5", "XM6"]}],
 "array":  [{"devices": ["XQ1", "XQ2a", "XQ2b", "XQ3"], "cols": 4}],
 "fixed":  {"XM9": {"x": 30.0, "y": 0.0}}}
```

`groups[].kind` is `diff_pair`, `current_mirror` or `generic`; a hinted group
replaces whatever the detector grouped those devices into.

Overlaps a hint would cause are reported in `metrics.hint_overlaps`, never
silently moved. Typical reasons to hint: interdigitate ratioed resistors,
keep a differential pair in one row, put matched BJTs side by side.

## 5. Long runs and jobs

`layout generate`, `verify *` and `flow run` can take minutes. The CLI waits
up to `--wait-s` (540 s; 50 s over MCP). If the run is unfinished you get
`status: NOT RUN`, `job: {id, state: "running"}` and exit code 4; continue with

```bash
scripts/mbg job wait <id> --wait-s 600   # or: job status <id>, job cancel <id>
```

The job keeps running between calls, so a harness tool-timeout never loses work.

## 6. Verification on an existing GDS

```bash
scripts/mbg verify drc path/to/cell.gds
scripts/mbg verify lvs path/to/cell.gds --netlist path/to/cell.spice
scripts/mbg verify pex path/to/cell.gds
```

## Rules that keep the results honest

* Read numbers from envelopes and the files they name — never from memory.
* `layout generate` PASS means all four legs: Magic DRC clean, KLayout deck
  clean (where the PDK has one; sky130A is Magic-only and says so in
  `metrics.drc_engines`), LVS match, internal connectivity clean.
* Verified is not finished: the tapeout gate also needs the PEX netlist
  simulated against the specification (`measure … --post-layout`).
* A netlist above the tested ceiling (`ABOVE_TESTED_CEILING`) may still lay
  out, but say so in the report.
