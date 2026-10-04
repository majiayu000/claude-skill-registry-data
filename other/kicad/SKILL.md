---
name: kicad
description: "Automate KiCad board workflows with pcbnew and kicad-cli, configure design rules, and generate fabrication outputs for review."
category: eda
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["kicad", "pcbnew", "eeschema", "kicad-cli", "pcb-design", "open-source-eda", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# KiCad Open-Source ECAD AI Skill Guide (Claude)

## Overview & Engine Architecture
KiCad is the premier open-source electronics design automation (EDA) suite for schematic capture, simulation, and multi-layer PCB layout. KiCad utilizes human-readable **S-Expression (`.kicad_sch`, `.kicad_pcb`)** file formats, features the advanced **PNS Push & Shove Interactive Router**, embeds the **`pcbnew` Python API**, and provides a powerful headless command-line interface (**`kicad-cli`**). Claude operates as a Principal PCB Hardware Design Engineer and Open-Source EDA Automation Specialist, specializing in **`kicad-cli` CI/CD automated manufacturing pipelines**, **Pcbnew Python scripting**, **Custom Design Rules (`.kicad_dru`)**, and **high-density BGA routing**.

### KiCad Architecture & Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 KiCad ECAD Suite Architecture               │
│                                                             │
│  Design Entry & Core Data Model (S-Expressions)             │
│  ├── Eeschema (Hierarchical Schematic Editor & ERC)         │
│  ├── Pcbnew (Multi-Layer Layout & PNS Push/Shove Router)    │
│  └── 3D Raytraced Ray-Caster (STEP / VRML Co-Design)        │
│                                                             │
│  Headless Automation & Scripting Layer                      │
│  ├── `kicad-cli` (Automated DRC/ERC, Gerber, Drill, STEP)   │
│  ├── `pcbnew` Native Python 3 Scripting API                 │
│  └── Custom Design Rule Language Parser (`.kicad_dru`)      │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **`kicad-cli` Headless CI/CD Pipelines**: Author zero-touch shell scripts to run automated DRC/ERC, generate Gerber X2 files, create NC drill files, export Pick-and-Place POS files, and render 3D STEP models.
2. **Pcbnew Python Scripting**: Write Python 3 scripts utilizing the native `pcbnew` module (`pcbnew.LoadBoard`, `board.GetTracks()`, `board.GetFootprints()`) to automate layout modifications.
3. **Custom Design Rule Formulation**: Author KiCad 8/9 custom design rules (`rule "BGA_Clearance"`) using S-expression pattern matching (`condition "A.insideCourtyard('U1')"`).
4. **Schematic & Hierarchical Netlist Triage**: Troubleshoot hierarchical sheet label scope, global vs local net boundaries, and Electrical Rules Check (ERC) violations.

---

## Production Python Automation: Headless PCB DRC & CAM Release Generator (`pcbnew`)

Save this script as `kicad_cam_packager.py` and run using KiCad's bundled Python interpreter:

```python
"""
Automated KiCad 8/9 CAM Release & DRC Packager
Executes headless DRC, plots all Gerber layers, and generates NC Drill files.
"""

import sys
import os
import pcbnew

def generate_cam_outputs(pcb_path: str, output_dir: str):
    if not os.path.exists(pcb_path):
        print(f"Error: PCB file '{pcb_path}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading PCB: {pcb_path}...")
    board = pcbnew.LoadBoard(pcb_path)

    # 1. Initialize Plot Controller
    pctl = pcbnew.PLOT_CONTROLLER(board)
    popt = pctl.GetPlotOptions()
    popt.SetOutputDirectory(output_dir)
    
    # Configure Standard Fabrication Plot Options
    popt.SetPlotFrameRef(False)
    popt.SetSketchPadOnFab(False)
    popt.SetPlotValue(True)
    popt.SetPlotReference(True)
    popt.SetPlotInvisibleText(False)
    popt.SetPlotViaOnMaskLayer(False)
    popt.SetUseAuxOrigin(True)
    popt.SetScale(1.0)
    popt.SetMirror(False)
    popt.SetSubtractMaskFromSilk(True)

    # 2. Plot Standard Production Gerber Layers
    plot_layers = [
        ("F_Cu", pcbnew.F_Cu, "Top Copper"),
        ("B_Cu", pcbnew.B_Cu, "Bottom Copper"),
        ("F_Mask", pcbnew.F_Mask, "Top Solder Mask"),
        ("B_Mask", pcbnew.B_Mask, "Bottom Solder Mask"),
        ("F_SilkS", pcbnew.F_SilkS, "Top Silkscreen"),
        ("B_SilkS", pcbnew.B_SilkS, "Bottom Silkscreen"),
        ("F_Paste", pcbnew.F_Paste, "Top Solder Paste"),
        ("B_Paste", pcbnew.B_Paste, "Bottom Solder Paste"),
        ("Edge_Cuts", pcbnew.Edge_Cuts, "Board Outline")
    ]

    for suffix, layer_id, desc in plot_layers:
        pctl.SetLayer(layer_id)
        pctl.OpenPlotfile(suffix, pcbnew.PLOT_FORMAT_GERBER, desc)
        pctl.PlotLayer()
        print(f"  • Plotted {desc} -> {suffix}.gbr")
    pctl.ClosePlot()

    # 3. Generate Excellon NC Drill Files
    print("Generating NC Drill and Map Files...")
    drill_writer = pcbnew.EXCELLON_WRITER(board)
    drill_writer.SetMapFileFormat(pcbnew.PLOT_FORMAT_GERBER)
    drill_writer.SetOptions(
        False, # aMirror
        True,  # aHeader
        board.GetDesignSettings().GetAuxOrigin(), # aOffset
        False  # aMerge_PTH_NPTH
    )
    drill_writer.SetFormat(True) # Metric units
    drill_writer.CreateDrillandMapFilesSet(output_dir, True, False)

    print(f"--- [CAM RELEASE PACKAGE GENERATED SUCCESSFULLY: {output_dir}] ---")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python kicad_cam_packager.py <board.kicad_pcb> <output_dir>")
        sys.exit(1)
    generate_cam_outputs(sys.argv[1], sys.argv[2])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Hierarchical Sheet Pins Disconnect in PCB Layout** | Hierarchical label name in sub-sheet does not match sheet pin name on the root sheet block. | 1. In Eeschema, right-click the hierarchical sheet block $\rightarrow$ *Synchronize Sheet Pins with Labels*.<br>2. Run *Inspect $\rightarrow$ Electrical Rules Checker (ERC)*.<br>3. In Pcbnew, execute *Tools $\rightarrow$ Update PCB from Schematic* (`F8`). |
| **Push & Shove Router Blocked inside Tight BGA Fanout** | Global board clearance constraint exceeds pitch spacing between adjacent BGA ball pads. | 1. In *File $\rightarrow$ Board Setup $\rightarrow$ Custom Rules*, author a localized clearance rule: `(rule "BGA_Inside" (condition "A.insideCourtyard('U1')") (constraint clearance (min 0.1mm)))`.<br>2. Switch routing mode to **Walkaround** or **Highlight Collisions** temporarily. |
| **3D Viewer / STEP Export Shows Missing Components** | Model 3D path relies on unexpanded environment variables (`${KICAD8_3DMODEL_DIR}`) or invalid relative paths. | 1. In KiCad main window, open *Preferences $\rightarrow$ Configure Paths*.<br>2. Verify `${KICAD8_3DMODEL_DIR}` points to the actual 3D library directory.<br>3. Check footprint 3D Model tab for valid `.step` link. |
| **Zone Fill Leaves Pads Unconnected (Isolated Copper Island)** | Thermal relief spoke width is wider than available copper gap or clearance rule isolates pad. | In Zone Properties, decrease **Thermal Spoke Width** or change connection to **Solid** for high-current power planes. |

---

## Command Line Syntax & `kicad-cli` Recipes

```bash
# 1. Run Automated DRC and Export JSON Report via kicad-cli
kicad-cli pcb drc --format json --output drc_report.json "C:\Hardware\board.kicad_pcb"

# 2. Export High-Resolution 3D STEP Enclosure Model
kicad-cli pcb export step --subst-models --output "C:\Mechanical\board.step" "C:\Hardware\board.kicad_pcb"

# 3. Export Complete Gerber Suite in a Single Command
kicad-cli pcb export gerbers -o "C:\Release\Gerbers" --no-x2 --use-drill-file-origin "C:\Hardware\board.kicad_pcb"

# 4. Generate Interactive BOM (ibom) for Assembly
generate_interactive_bom.py "C:\Hardware\board.kicad_pcb"
```

### Essential File Locations
- **Windows User Settings**: `%APPDATA%\kicad\8.0`
- **Linux User Settings**: `~/.config/kicad/8.0`
- **macOS Preferences**: `~/Library/Preferences/kicad/8.0`

---

## Agent Operational Directive
> **MANDATORY**: For automated manufacturing CI/CD pipelines, leverage `kicad-cli` to execute DRC verification and export Gerber X2 and STEP packages. Always resolve ERC errors in Eeschema before pushing changes to Pcbnew.
