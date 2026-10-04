---
name: zbrush
description: "Automate ZBrush sculpting workflows with ZScript, prepare retopology with ZRemesher, and manage mesh decimation or exports."
category: 3d
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["zbrush", "digital-sculpting", "zscript", "zremesher", "decimation-master", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Maxon ZBrush AI Skill Guide (Claude)

## Overview & Engine Architecture
Maxon ZBrush is the industry benchmark for organic and hard-surface digital sculpting, handling meshes exceeding 100 million polygons. Claude acts as a Senior Digital Sculpting TD and Pipeline Engineer, specializing in **ZScript automation**, **ZRemesher quad topology generation**, **Decimation Master optimization**, **32-bit Displacement/Normal map extraction**, and **GoZ inter-application bridges**.

### ZBrush Engine & Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 ZBrush 2.5D Pixol & 3D Core                 │
│                                                             │
│  Geometry Subsystems                                        │
│  ├── Multi-Resolution Subdivision & SDiv Level Baking       │
│  ├── Dynamic Topology (DynaMesh Voxelizer & Sculptris Pro)  │
│  ├── ZRemesher Quad Flow (Curvature-guided autoretopology)  │
│  └── SubTool Hierarchy & PolyGroup Segmentation             │
│                                                             │
│  Automation & Pipeline Interfaces                           │
│  ├── ZScript Command Language (Macros, Buttons, Menus)      │
│  ├── Decimation Master & Multi-Map Exporter Plugins         │
│  └── GoZ Universal Interchange System (Maya, C4D, Blender)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **ZScript Macro Authoring**: Write clean, error-free ZScript files (`.txt`/`.zsc`) using commands like `[IPress, ...]`, `[VarSet, ...]`, `[SubToolSelect, ...]`, and `[FileNameSetNext, ...]` to automate repetitive sculpting tasks.
2. **Mesh Decimation & Export Automation**: Script Decimation Master workflows to reduce 50M polygon sculpts to 500k game-ready proxies while preserving silhouettes and surface normals.
3. **Map Extraction & Baking**: Configure 32-bit floating-point multi-tile (UDIM) displacement map extraction with Mid-point 0.0, 3-channel vector displacement, and tangent-space normal maps.
4. **Topology & PolyGroup Diagnostics**: Remediate non-manifold edges, high-valence poles, and unclosed mesh shells using Dynamesh and Close Holes algorithms.

---

## Production ZScript Automation: Batch SubTool Decimator & Exporter

Save this macro as `BatchDecimateExport.txt` inside `ZStartup/ZPlugs64/` to automate processing of all visible SubTools:

```zscript
// ZScript: Batch Decimate and Export All Visible SubTools
[IButton, "ZPlugin:Pipeline:BatchDecimate", "Pre-processes and decimates all visible SubTools to 20% and exports OBJ",
    [VarSet, totalSubTools, [SubToolGetCount]]
    [VarSet, activeIdx, 0]
    
    // Disable Screen Update for Maximum Execution Speed
    [IFreeze,
        [Loop, totalSubTools,
            [SubToolSelect, activeIdx]
            
            // Check if SubTool is visible
            [If, [SubToolGetStatus, activeIdx] == 1,
                // 1. Pre-process Current SubTool in Decimation Master
                [IPress, "ZPlugin:Decimation Master:Pre-process Current"]
                
                // 2. Set Decimation Target to 20%
                [ISet, "ZPlugin:Decimation Master:% of decimation", 20]
                [IPress, "ZPlugin:Decimation Master:Decimate Current"]
                
                // 3. Export Decimated OBJ
                [VarSet, subToolName, [IGetTitle, "Tool:ItemInfo"]]
                [FileNameSetNext, [StrMerge, "C:/Export/Decimated_", subToolName, ".obj"]]
                [IPress, "Tool:Export"]
            ]
            [VarInc, activeIdx]
        ]
    ]
    [Note, "Batch Decimation and Export Completed Successfully!", , 2]
]
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Viewport Freezes / Canvas Lag Above 30M Polygons** | Single-threaded 2.5D Pixol rasterization canvas overloaded by displaying all SubTools simultaneously. | 1. Enable **Solo Mode** (`Dynamic` button under viewport).<br>2. Hide inactive SubTools.<br>3. Split dense geometry into discrete SubTools by PolyGroup (*Tool $\rightarrow$ SubTool $\rightarrow$ Split $\rightarrow$ Group Split*). |
| **ZRemesher Output Has Spiral Edge Loops on Cylinders** | Flow guide symmetry or guide curves are conflicting with boundary geometry. | 1. Draw **ZRemesher Guides** along cylindrical flow lines.<br>2. Enable **Keep Groups** and **Smooth Groups = 0**.<br>3. Enable **Detect Edges** in ZRemesher settings. |
| **GoZ Fails Silently to Send Mesh to Target Application** | Corrupted GoZ path cache or missing application plugin scripts. | 1. Navigate to *Preferences $\rightarrow$ GoZ $\rightarrow$ Path to Maya/Blender/C4D*.<br>2. Re-point to the target DCC executable.<br>3. Clear cache at `C:\Users\Public\Pixologic\GoZBrush\GoZ_ObjectList.txt`. |
| **Displacement Map Baking Shows Staircase Artifacts** | Map exported as 8-bit or 16-bit integer image instead of 32-bit floating point EXR/TIFF. | 1. In Multi Map Exporter, enable **32Bit** displacement mode.<br>2. Set SubTool to lowest SDiv level before generation.<br>3. Export as 32-bit Multi-channel OpenEXR. |

---

## Command Line Syntax & ZScript Execution

```bash
# Windows CLI: Launch ZBrush and Auto-Execute Startup ZScript
"C:\Program Files\Maxon ZBrush 2025\ZBrush.exe" -zscript "C:\Pipeline\auto_setup.zsc"

# Force ZScript Compilation from Text to ZSC
"C:\Program Files\Maxon ZBrush 2025\ZBrush.exe" "C:\Scripts\BatchDecimateExport.txt"
```

### Essential File & Directory Paths
- **Windows Startup Plugins**: `C:\Program Files\Maxon ZBrush 2025\ZStartup\ZPlugs64`
- **Windows Config Files**: `C:\Program Files\Maxon ZBrush 2025\ZStartup\ConfigFiles`
- **Public GoZ Cache**: `C:\Users\Public\Pixologic\GoZBrush`
- **macOS Startup Plugins**: `/Applications/Maxon ZBrush 2025/ZStartup/ZPlugs64`

---

## Agent Operational Directive
> **MANDATORY**: When writing ZScript automation macros, always wrap execution loops inside `[IFreeze, ...]` to disable viewport redraws and prevent memory thrashing. Export displacement maps as 32-bit floating point EXR files.
