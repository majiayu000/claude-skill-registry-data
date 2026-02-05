---
name: dynamo-analyzer
description: Analyze Dynamo (.dyn) graphs to extract workflow, Python/DesignScript code, Revit API patterns, and generate comprehensive reports for C# developers
---

# Dynamo Unified Analyzer

Automatically analyze Dynamo graph definitions (.dyn) to understand workflow structure, extract custom Python and DesignScript code, identify Revit API patterns, and generate comprehensive documentation suitable for porting to C#.

## When to use this skill

Use this skill when the user:
- Asks to analyze a Dynamo file or graph
- Wants to understand the structure of a .dyn workflow
- Needs to extract Python scripts or DesignScript code blocks from Dynamo
- Requests documentation for a BIM automation workflow
- Mentions converting or porting Dynamo logic to C#
- Needs algorithmic breakdown of a Revit automation script
- Wants to understand Revit API usage patterns in a Dynamo graph

## What this skill does

1. **Parses Dynamo JSON** (.dyn format) without requiring Dynamo/Revit runtime
2. **Builds workflow graph** from Nodes and Connectors
3. **Identifies topology**: start/end nodes, branching points, merge points, primary workflow paths
4. **Extracts custom code**: Python scripts (with engine and I/O) and DesignScript code blocks
5. **Catalogs DSFunctions**: ZeroTouch function signatures and Revit API references
6. **Detects patterns**: Revit API usage, transactions, FilteredElementCollector patterns
7. **Identifies dependencies**: Packages and external library references
8. **Generates comprehensive report** with:
   - Executive Summary (purpose, Revit interaction, scope)
   - Workflow Summary (topology and primary flow)
   - Libraries & Dependencies
   - Custom Script Analysis (full Python/DesignScript code with I/O)
   - Algorithmic Analysis (A-E format for C# developers)
   - Definition Summary (node counts, statistics)

## How to use

Execute the unified analyzer script:

```bash
python ~/.claude/skills/dynamo-analyzer/dynamo-analyzer.py "path/to/file.dyn"
```

**Arguments:**
- Path to .dyn file (Dynamo 2.x JSON format)

**Example:**
```bash
python ~/.claude/skills/dynamo-analyzer/dynamo-analyzer.py ~/Desktop/revit-automation.dyn
```

## Output

The analyzer generates a comprehensive Markdown report:
- **Location**: `<input-filename>-dynamo-report.md` (same directory as input)
- **Format**: Single structured Markdown document

### Report Structure

1. **Executive Summary** - Purpose, Revit API usage, Python/DesignScript presence
2. **Workflow Summary** - Start/end nodes, branching, primary flow
3. **Libraries and Dependencies** - Packages, Revit API references
4. **Custom Script Analysis**:
   - Python nodes (engine, inputs, outputs, full code)
   - DesignScript code blocks (full code)
   - DSFunction signatures cataloged
5. **Algorithmic Analysis (A-E format)**:
   - A. High-Level Algorithmic Summary
   - B. Core Algorithm Breakdown (input → processing → output)
   - C. Key Computational Components
   - D. Data Flow Architecture (parameters and processing order)
   - E. Implementation Notes for C# Developer (Revit API, transactions, performance)
6. **Definition Summary** - Statistics (nodes, connections, scripts, functions)

## Requirements

- **Python**: 3.6+
- **Dependencies**: Standard library only (json, os, re, collections)
- **Platform**: Windows/macOS/Linux
- **File Format**: .dyn (Dynamo 2.x JSON) - custom nodes (.dyf) not supported

## Important notes

- The analyzer processes files in-memory without modifying the original
- Report is deterministic and suitable for version control
- Identifies Revit API patterns (transactions, FilteredElementCollector, etc.)
- Detects model-modifying operations (Set, Create nodes)
- Flow diagrams are analyzed but not embedded (topology shown as text)
- Perfect for understanding existing automations or preparing for C# migration
- The algorithmic analysis (A-E format) is specifically structured for C# developers
- Custom nodes (.dyf) are out of scope for this version
