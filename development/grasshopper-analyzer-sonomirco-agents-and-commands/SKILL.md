---
name: grasshopper-analyzer
description: Analyze Grasshopper (.ghx/.xml) files to extract workflow, custom scripts, algorithmic patterns, and generate comprehensive reports for C# developers
---

# Grasshopper Unified Analyzer

Automatically analyze Grasshopper XML definitions (.ghx) to understand workflow structure, extract custom C#/Python scripts, and generate comprehensive documentation suitable for porting to C#.

## When to use this skill

Use this skill when the user:
- Asks to analyze a Grasshopper file or definition
- Wants to understand the structure of a .ghx file
- Needs to extract C# or Python scripts from Grasshopper components
- Requests documentation for a parametric workflow
- Mentions converting or porting Grasshopper logic to C#
- Needs algorithmic breakdown of a computational design script

## What this skill does

1. **Parses Grasshopper XML** (.ghx/.xml format) without requiring Rhino/Grasshopper runtime
2. **Builds workflow graph** from components and connections
3. **Identifies topology**: start/end nodes, branching points, merge points, primary workflow paths
4. **Extracts custom scripts**: Full C# and Python code with input/output parameters
5. **Detects dependencies**: Libraries, Rhino.Geometry, RhinoCommon SDK references
6. **Generates comprehensive report** with:
   - Executive Summary (purpose and scope)
   - Workflow Summary (topology and primary flow)
   - Libraries & Dependencies
   - Custom Script Analysis (full code with I/O metadata)
   - Algorithmic Analysis (A-E format for C# developers)
   - Definition Summary (component counts, statistics)

## How to use

Execute the unified analyzer script:

```bash
python ~/.claude/skills/grasshopper-analyzer/gh-unified-analyzer.py "path/to/file.ghx"
```

**Arguments:**
- Path to .ghx or .xml file (binary .gh files are NOT supported)

**Example:**
```bash
python ~/.claude/skills/grasshopper-analyzer/gh-unified-analyzer.py ~/Desktop/parametric-design.ghx
```

## Output

The analyzer generates a comprehensive Markdown report:
- **Location**: `<input-filename>-grasshopper-report.md` (same directory as input)
- **Format**: Single structured Markdown document

### Report Structure

1. **Executive Summary** - Purpose, scope, and component counts
2. **Workflow Summary** - Start/end nodes, branching, primary flow
3. **Libraries and Dependencies** - External assemblies and references
4. **Key Grasshopper Components** - Standard components used (grid, remap, etc.)
5. **Custom Script Analysis** - Full code listings with I/O parameters
6. **Algorithmic Analysis (A-E format)**:
   - A. High-Level Algorithmic Summary
   - B. Core Algorithm Breakdown (input → processing → output)
   - C. Key Computational Components (purpose, algorithm, dependencies)
   - D. Data Flow Architecture (parameters and processing order)
   - E. Implementation Notes for C# Developer (dependencies, performance, edge cases)
7. **Definition Summary** - Statistics (component count, scripts, libraries, paths)

## Requirements

- **Python**: 3.6+
- **Dependencies**: Standard library only (xml.etree.ElementTree, os, sys, re)
- **Platform**: Windows/macOS/Linux
- **File Format**: .ghx (XML) or .xml only - binary .gh must be saved as .ghx first

## Important notes

- The analyzer processes files in-memory without modifying the original
- Report is deterministic and suitable for version control
- Custom components beyond standard scripts are treated generically
- Flow diagrams are analyzed but not embedded (topology shown as text)
- Perfect for understanding existing definitions or preparing for C# migration
- The algorithmic analysis (A-E format) is specifically structured for C# developers
