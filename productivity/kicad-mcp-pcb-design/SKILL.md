---
name: kicad-mcp-pcb-design
description: Use when installing or using KiCad with MCP/agent automation to inspect existing PCB projects, generate or edit KiCad boards, save component datasets, validate DRC, export Gerbers/STEP, and render board previews.
triggers:
  - KiCad MCP
  - kicad-cli
  - draw a PCB
  - generate KiCad board
  - PCB render
  - Gerber export
  - pcbnew automation
  - agent PCB design
---

# KiCad MCP PCB Design

Use this skill when an agent must control KiCad, research components, clone an existing PCB style, produce a new board, and prove the result with KiCad-native validation artifacts.

## Core Rules

- Treat PCB output as an engineering draft until a human verifies electrical, thermal, and mechanical constraints.
- Save source-backed component assumptions in a dataset file, including URLs, model numbers, dimensions, currents, voltages, thermal notes, and uncertainty.
- Prefer KiCad-native tooling for validation: `kicad-cli pcb drc`, `export step`, `export gerbers`, `export drill`, and `render`.
- Use `/usr/bin/python3` or a venv made with `--system-site-packages` when Python code needs `pcbnew`; Conda Python usually cannot import KiCad bindings.
- Stage only intended generated PCB files. Do not accidentally commit large unrelated PCB archives, extracted vendor zips, `__MACOSX/`, `.DS_Store`, `fp-info-cache`, or local `.kicad_prl` UI-state files.
- For research hardware, document the future system intent separately from the immediate board so assumptions do not get buried inside fabrication files.

## Setup

Check KiCad first:

```bash
kicad-cli version
/usr/bin/python3 -c 'import pcbnew; print(pcbnew.GetMajorMinorVersion())'
```

Ubuntu KiCad 10 install pattern:

```bash
sudo add-apt-repository -y ppa:kicad/kicad-10.0-releases
sudo apt-get update
sudo apt-get install -y kicad kicad-footprints kicad-symbols kicad-packages3d kicad-templates xvfb imagemagick python3-venv
```

MCP baseline used successfully:

```bash
git clone https://github.com/Seeed-Studio/kicad-mcp-server ~/.local/share/appautoaction/mcp/kicad-mcp-server
/usr/bin/python3 -m venv --system-site-packages ~/.local/share/appautoaction/mcp/kicad-mcp-server/.venv
~/.local/share/appautoaction/mcp/kicad-mcp-server/.venv/bin/python -m pip install -e ~/.local/share/appautoaction/mcp/kicad-mcp-server
```

MCP client command:

```json
{
  "type": "stdio",
  "command": "$HOME/.local/share/appautoaction/mcp/kicad-mcp-server/.venv/bin/python",
  "args": ["-m", "kicad_mcp_server"],
  "cwd": "$HOME/.local/share/appautoaction/mcp/kicad-mcp-server"
}
```

Consider `belaszalontai/kipilot-mcp` when the task needs live KiCad 10 GUI edits through the official IPC path. Use Seeed's server or deterministic scripts for headless repository work.

## Board Generation Workflow

1. Inspect existing reference boards:

```bash
rg --files path/to/old/pcb
rg 'gr_circle|gr_rect|footprint|pad|segment|zone' path/to/old/board.kicad_pcb
```

2. Extract reusable constraints: outline, mounting holes, connector position, layer stack, net names, track widths, clearances, and silkscreen style.
3. Create a deterministic generator script when changes are repeatable. It should write `.kicad_pro`, `.kicad_pcb`, `.kicad_sch` stub if needed, `fp-lib-table`, local `.pretty` footprints, BOM/CSV, dataset JSON, and README.
4. Include a project-local `.gitignore` with `*.kicad_prl`; for imported PCB reference dumps also ignore local-only archives and extracted folders such as `*.zip`, `__MACOSX/`, and `.DS_Store`.
5. Keep generated footprints embedded or project-local so the board opens on another machine.

## Research Memory

When the board is part of a larger instrument plan, add a concise roadmap document under the target repo's `docs/` or hardware folder. Include:

- local reference repositories and their relevant files;
- external source URLs;
- immediate board scope vs future system architecture;
- safety constraints, especially high voltage, vacuum, radiation, heat, and detector exposure;
- staged milestones that can become future PCB or firmware tasks.

## Validation And Exports

Run these before claiming completion:

```bash
kicad-cli pcb upgrade project.kicad_pcb
kicad-cli pcb drc --format json --severity-all -o artifacts/drc.json project.kicad_pcb
kicad-cli pcb export step --force --include-pads --include-tracks --include-silkscreen --include-soldermask -o artifacts/board.step project.kicad_pcb
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Fab,B.Fab --precision 6 -o gerber project.kicad_pcb
kicad-cli pcb export drill --generate-map --map-format svg --generate-report --report-path artifacts/drill-report.txt -o gerber project.kicad_pcb
xvfb-run -a kicad-cli pcb render --output artifacts/render.png --width 1400 --height 1000 --background opaque --quality high --floor --perspective --rotate 315,0,35 --zoom 2.2 project.kicad_pcb
xvfb-run -a kicad-cli pcb render --output artifacts/render-full.png --width 1400 --height 1000 --background opaque --quality high --floor --perspective --rotate 315,0,35 --zoom 0.95 project.kicad_pcb
identify artifacts/render.png
identify artifacts/render-full.png
```

If DRC reports warnings, inspect the JSON and either fix the board or document why an ignored check is intentional. Electrical clearance, copper connectivity, and unconnected items must not be hand-waved.

Gerber completeness checklist:

- front/back copper: `F_Cu.gtl`, `B_Cu.gbl`;
- front/back mask: `F_Mask.gts`, `B_Mask.gbs`;
- front/back silkscreen: `F_Silkscreen.gto`, `B_Silkscreen.gbo`;
- board outline: `Edge_Cuts.gm1`;
- job file: `*.gbrjob`;
- drill file and map/report: `*.drl`, drill map, drill report.

## Final Report

Report the KiCad version, MCP server used, generated board path, dataset path, DRC/ERC result, close render path, full-board render path, Gerber/drill/STEP outputs, commit hash, push status, and any physical verification still required.
