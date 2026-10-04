---
name: catia
description: "Automate CATIA V5 and 3DEXPERIENCE modeling workflows through CAA or COM, including shape design and assembly operations."
category: cad
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["catia", "catia-v5", "3dexperience", "cad-automation", "com-api", "class-a-surfacing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Dassault Systèmes CATIA AI Skill Guide (Claude)

## Overview & Engine Architecture
Dassault Systèmes CATIA (Computer Aided Three-dimensional Interactive Application) is the primary CAD/CAM/CAE and PLM suite utilized across aerospace, automotive, and defense industries for Class-A surfacing, advanced mechanical engineering, and digital mockup verification. Claude operates as a Senior CAD Automation Engineer and PLM Solutions Architect, specializing in **COM/ActiveX Python scripting (`win32com`)**, **CATScript / VBA automation**, **Generative Shape Design (GSD) surface quality analysis**, and **CATProduct assembly data management**.

### CATIA V5 & 3DEXPERIENCE Execution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 CATIA System Architecture                   │
│                                                             │
│  Engineering Workbenches                                    │
│  ├── Part Design & Generative Shape Design (GSD Class-A)    │
│  ├── Assembly Design & DMU Kinematics / Space Analysis      │
│  └── Knowledgeware (Rules, Checks, PowerCopies, UDFs)       │
│                                                             │
│  Automation & Interop Layer                                 │
│  ├── Win32 COM / ActiveX Interface (`CATIA.Application`)    │
│  ├── CATScript & VBScript Macro Engine                      │
│  └── CATBatchMonitor / Headless STEP/IGES Exporters         │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Python COM Automation**: Author deterministic Python scripts using `win32com.client` to connect to running `CATIA.Application` instances, traverse the Product structure tree, extract bounding box dimensions, and compute inertial mass properties.
2. **Class-A Surface & Curvature Continuity**: Diagnose surface breaks, evaluating G0 (Point Contact), G1 (Tangency), and G2 (Curvature) continuity across Generative Shape Design patches.
3. **Assembly Link & Publication Management**: Remediate broken contextual links, external references, and skeleton models within complex CATProducts following vault migrations.
4. **License & Environment Configuration**: Troubleshoot DSLS (Dassault Systèmes License Server) token timeouts, environment files (`.CATEnv`), and clean corrupted user CATSettings.

---

## Production Python Automation: Headless CATPart Property Extractor & STEP Exporter

Execute this script via Python with `pywin32` installed to inspect an open CATIA session, calculate mass properties, and export a STEP file:

```python
"""
CATIA V5 Automation: Mass Property Extractor & STEP Exporter
Requires: pip install pywin32
"""

import sys
import os
import win32com.client

def process_active_catia_part(output_step_path: str):
    try:
        # 1. Connect to Running CATIA COM Instance
        catia = win32com.client.Dispatch("CATIA.Application")
        catia.Visible = True
    except Exception as e:
        print(f"Error: Could not connect to CATIA application: {e}")
        sys.exit(1)

    # 2. Get Active Document
    try:
        doc = catia.ActiveDocument
        part = doc.Part
    except Exception:
        print("Error: No active CATPart document found in CATIA session.")
        sys.exit(1)

    print(f"Active Part: {part.Name}")

    # 3. Analyze Inertia & Mass Properties
    try:
        workbench = doc.GetWorkbench("InertiaWorkbench")
        inertia = workbench.CreateInertia(part)
        mass_kg = inertia.Mass
        volume_m3 = inertia.Volume
        print(f"Inertial Analysis -> Mass: {mass_kg:.4f} kg | Volume: {volume_m3:.6f} m^3")
    except Exception as e:
        print(f"Warning: Could not compute inertia: {e}")

    # 4. Export to STEP AP214/AP242
    os.makedirs(os.path.dirname(os.path.abspath(output_step_path)), exist_ok=True)
    try:
        doc.ExportData(output_step_path, "stp")
        print(f"Successfully exported STEP file: {output_step_path}")
    except Exception as e:
        print(f"Export failed: {e}")

if __name__ == "__main__":
    export_target = "C:/Export/Validated_Part.stp"
    process_active_catia_part(export_target)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Broken Contextual Links in CATProduct (`Red / Broken Link Icon`)** | Source CATPart was renamed, moved on disk, or published elements were modified without synchronization. | 1. In Assembly workbench, open *Edit $\rightarrow$ Links*.<br>2. Select broken links and click **Pointed Documents $\rightarrow$ Replace**.<br>3. Verify that the parent Part contains an updated **Publication** for the referenced geometry. |
| **DSLS License Heartbeat Timeout Mid-Session** | Network jitter dropped DSLS keep-alive packets or Windows Firewall blocked TCP port 4085. | 1. In `C:\ProgramData\DassaultSystemes\Licenses\DSLS.lic`, verify server IP and port 4085.<br>2. In Windows Registry, set `DSLS_LICENSING_HEARTBEAT` to 900 seconds.<br>3. Enable **License Borrowing** for offline stability. |
| **GSD Surface Join Error: `Cannot join elements with gap > tolerance`** | Non-manifold surface boundary or boundary curve gap exceeds the 0.001mm modeling tolerance. | 1. In Join Definition, check **Check Tangency** and **Check Connexity**.<br>2. Increase Merging Distance cautiously (Max 0.005mm) or use **Near/Extract** to rebuild boundary curves.<br>3. Use *Surface Curvature Analysis* (Porcupine view) to locate gaps. |
| **CATIA Freezes / Crashes on Startup** | Corrupted user CATSettings files from an abnormal shutdown or cache overflow. | 1. Terminate all `CNEXT.exe` processes.<br>2. Rename `%APPDATA%\DassaultSystemes\CATSettings` to `CATSettings_OLD`.<br>3. Relaunch CATIA to regenerate clean factory default settings. |

---

## Command Line Syntax & Batch Processing

```bash
# Windows CLI: Launch CATIA V5 with Specific Environment File
"C:\Program Files\Dassault Systemes\B32\win_b64\code\bin\CNEXT.exe" -env CATIA_V5R32 -direnv "C:\ProgramData\DassaultSystemes\CATEnv" -nowindow

# Launch CATIA Batch Monitor for Headless Operations
"C:\Program Files\Dassault Systemes\B32\win_b64\code\bin\CATBatchMonitor.exe"

# Execute Standalone CATScript via CLI
"C:\Program Files\Dassault Systemes\B32\win_b64\code\bin\CNEXT.exe" -batch -macro "C:\Scripts\BatchExport.CATScript"
```

### Key Configuration Locations
- **Windows Environment Files**: `C:\ProgramData\DassaultSystemes\CATEnv\CATIA.V5R32.B32.txt`
- **Windows User CATSettings**: `%APPDATA%\DassaultSystemes\CATSettings`
- **DSLS License Client Config**: `C:\ProgramData\DassaultSystemes\Licenses\DSLS.lic`

---

## Agent Operational Directive
> **MANDATORY**: When automating CATIA through COM, verify that `CATIA.Application` is active and wrap COM object references in `try...finally` blocks. For Class-A surfaces, enforce G1 tangency and G2 curvature continuity standards.
