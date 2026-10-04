---
name: unity-assembly-management
description: Manage project boundaries using Assembly Definitions (.asmdef) for faster compile times and modular architecture. Based on the patterns by Adam Myhre. Enforces responsibility-based organization and handles Runtime/Editor/Tests splits.
---

# Unity Assembly Management

Manage project boundaries using Assembly Definitions (.asmdef) for faster compile times and modular architecture. Based on the patterns by Adam Myhre.

## Core Features
- **Hybrid Approach**: Supports both "Pro Path" (Explicit GUIDs, Version Defines) and "Light Path" (Auto-referenced modules).
- **Rule Enforcement**: Enforces "Runtime never depends on Editor" and inward dependency flows.
- **Scaffolding**: Automated creation of Runtime/Editor/Tests assembly splits.

## Core Files
- `AsmdefTemplate.json.txt`: Flexible template for various assembly configurations.
- `AsmdefScaffolder.cs.txt`: Editor utility to generate standard module structures.
- `AsmdefValidator.cs.txt`: Script to verify architectural boundaries.

## Usage
1. Use `AsmdefScaffolder` to create a new module partition.
2. Define dependencies explicitly in the Inspector using GUIDs.
3. Validate regularly to ensure no architectural drift has occurred.
