---
name: kc-docs
description: Generate intelligent Python project documentation with UML class diagrams, architecture diagrams, and code analysis. Analyzes codebase structure to recommend and create appropriate visualizations for project overview.
allowed-tools: Read, Grep, Glob, Bash(python:*), Write, Edit
---

# KC Documentation Generator

Generate comprehensive project documentation with architecture diagrams and class visualizations for Python projects.

## Overview

This skill analyzes your Python codebase and automatically generates:
- **Architecture diagrams** - System component overview (Mermaid)
- **Class diagrams** - OOP structure and relationships (PlantUML + pyreverse)
- **Documentation** - Auto-generated API and structure reference
- **Analysis reports** - Codebase metrics and complexity

**Best for**: Understanding large codebases quickly, onboarding new team members, project documentation.

---

## Quick Start

### Generate Full Documentation

```bash
/kc-docs generate <project_path>
```

Analyzes your project and creates **inside the project**:
- `<project_path>/docs/diagrams/generated/` - All diagrams
- `<project_path>/docs/ARCHITECTURE.md` - System overview
- `<project_path>/docs/API_REFERENCE.md` - Classes and functions

Documentation stays with your code in version control!

### View Generated Diagrams

```bash
/kc-docs view <project_path>
```

Opens a browser preview of all generated diagrams and documentation.

### Analyze Project Only

```bash
/kc-docs analyze <project_path>
```

Examines codebase structure without generating diagrams. Returns:
- Number of modules and packages
- Classes and functions count
- Recommended diagram types
- Complexity assessment

---

## Supported Diagram Types

### 1. Architecture Diagram (Mermaid)
- **Shows**: System components and their relationships
- **Best for**: High-level system understanding
- **Recommended when**: Project has multiple modules or packages

### 2. Class Diagram (PlantUML)
- **Shows**: Classes, inheritance, relationships
- **Best for**: OOP structure understanding
- **Recommended when**: Project has >5 classes or deep inheritance

### 3. Module Dependency Graph
- **Shows**: How modules import each other
- **Best for**: Understanding coupling and architecture
- **Recommended when**: Project has multiple interconnected modules

### 4. Auto-generated from Code (pyreverse)
- **Shows**: Exact class structure from source code
- **Best for**: Staying in sync with actual code
- **Recommended always**: Automatic accuracy

---

## Usage Examples

### Example 1: Document an Existing Project

```bash
/kc-docs generate ~/myproject
# Generates inside ~/myproject/:
# - ~/myproject/docs/diagrams/generated/architecture.svg
# - ~/myproject/docs/diagrams/generated/classes_*.svg
# - ~/myproject/docs/ARCHITECTURE.md
# - ~/myproject/docs/API_REFERENCE.md
```

### Example 2: Analyze Before Documenting

```bash
/kc-docs analyze ~/myproject/src
# Output:
# Project Analysis Results:
# - Total modules: 12
# - Total classes: 45
# - Total functions: 156
# - Recommended diagrams: [architecture, class_diagram, dependencies]
# - Complexity: MEDIUM
```

### Example 3: Update Documentation When Code Changes

```bash
/kc-docs generate ~/myproject/src --force
# Forces regeneration of all diagrams (not using cache)
```

---

## How It Works

### Analysis Phase
1. **Scan** Python files for structure (modules, classes, functions)
2. **Extract** relationships and dependencies
3. **Categorize** code complexity and architecture patterns
4. **Recommend** which diagrams would be most useful

### Generation Phase
1. **Create** Mermaid architecture diagrams
2. **Generate** UML class diagrams using PlantUML
3. **Auto-generate** exact class structure with pyreverse
4. **Render** SVG outputs for viewing
5. **Create** markdown documentation with embedded diagrams

### Output Structure

```
docs/
├── diagrams/
│   ├── src/                    # Source diagram definitions
│   │   ├── architecture.mmd    # Mermaid architecture
│   │   └── classes.puml        # PlantUML class diagram
│   └── generated/              # Rendered outputs (gitignored)
│       ├── architecture.svg
│       ├── classes.svg
│       └── dependencies.svg
├── ARCHITECTURE.md              # System overview
├── API_REFERENCE.md             # Classes and functions
└── ANALYSIS_REPORT.md           # Code metrics
```

---

## Configuration

Create `.kc-docs.yaml` in your project root to customize:

```yaml
# .kc-docs.yaml
analysis:
  min_classes_for_diagram: 5    # Only create diagram if > 5 classes
  include_private: false         # Exclude private methods/classes
  max_depth: 3                   # Maximum folder depth to scan

output:
  format: [svg, png, html]       # Output formats
  theme: light                   # light or dark
  documentation: true            # Generate markdown docs

diagrams:
  architecture: true             # Generate architecture diagram
  classes: true                  # Generate class diagram
  dependencies: true             # Generate dependency graph
  sequences: false               # Generate sequence diagrams (if complex flows)
```

---

## Viewing Diagrams

### In Cursor (Markdown Preview)
1. Open `docs/ARCHITECTURE.md`
2. Use `Ctrl+Shift+V` to preview
3. Click SVG links to view diagrams

### In Browser
```bash
# View all diagrams in browser
python ~/.claude/skills/kc-docs/scripts/serve_docs.py docs/
# Opens: http://localhost:8000
```

### Direct Files
- Diagrams are SVG files → Open in any browser
- PDFs available → Use for printing/sharing
- PNG files available → For embedding in docs

---

## Requirements

### Installed Tools
- Python 3.8+
- Mermaid CLI (auto-installed if missing)
- PlantUML (auto-installed if missing)
- pyreverse (from pylint package)

### Project Structure
- Standard Python project layout
- Readable Python files (.py)
- No special requirements

---

## Architecture Bloat Detection

When generating documentation, kc-docs also checks for **architecture anti-patterns** that inflate class counts and obscure the real domain structure.

### Pydantic Model Bloat

**Problem**: Using Pydantic `BaseModel` for every nested data structure instead of only at API boundaries.

```python
# ❌ BLOAT: 5 classes for simple nested data
class Coordinate(BaseModel):
    lat: float
    lon: float

class Options(BaseModel):
    radius: float

class Request(BaseModel):
    coord: Coordinate
    options: Options

# ✅ LEAN: 1 class for API boundary, rest is inline
class Request(BaseModel):
    lat: float
    lon: float
    radius: float = 30.0
```

**Detection**: kc-docs flags when:
- Pydantic models > 30% of total classes
- Pydantic models with < 5 fields (could be `NamedTuple`)
- Nested Pydantic models used only internally

**Recommendation**:
| Location | Use |
|----------|-----|
| API Request/Response | ✅ Pydantic |
| Internal data passing | `dataclass`, `NamedTuple`, or `dict` |
| Simple value groups | `tuple` or `NamedTuple` |

### Thin Wrapper Classes

**Problem**: Classes with < 50 LOC that just delegate to other classes or stdlib.

```python
# ❌ BLOAT: Reinventing stdlib
class AdvancedCache:
    def __init__(self):
        self._cache = {}
    def get(self, key):
        return self._cache.get(key)
    def set(self, key, value):
        self._cache[key] = value

# ✅ LEAN: Use stdlib
from functools import lru_cache
```

**Detection**: kc-docs flags classes with:
- < 50 lines of code
- < 3 methods
- Names ending in `Manager`, `Handler`, `Wrapper`, `Helper`

### Layer Tax

**Problem**: handler → service → repository → model chains for simple operations.

**Detection**: kc-docs measures import depth and flags when > 4 layers.

### Metrics in Analysis Report

When you run `/kc-docs analyze`, the report now includes:

```
Architecture Health:
├── Pydantic model ratio: 41/169 (24%) ⚠️ HIGH
├── Thin wrappers detected: 8 classes
├── Average LOC per class: 85 ⚠️ LOW (target: 100-300)
├── Max import depth: 5 ⚠️ DEEP
└── Recommendation: Consolidate Pydantic models, merge thin wrappers
```

### Reference: Lean Architecture

See `~/.claude/snippets/lean-architecture-guard.md` for full guidelines.

**Golden rule**: A class should map to a **domain concept** (Turbine, Invoice, RoofPolygon), not an **architecture concept** (Handler, Service, Manager).

---

## Troubleshooting

**"No classes found"**
- Check that your project has at least 5 classes
- Run `/kc-docs analyze` first to verify structure

**"Diagram generation failed"**
- Ensure Mermaid and PlantUML are installed
- Run: `python scripts/check_dependencies.py`

**"Documentation looks outdated"**
- Use `--force` flag: `/kc-docs generate path --force`
- This regenerates all diagrams from scratch

---

## Tips

- **First time**: Run `analyze` to understand what diagrams you'll get
- **Large projects**: Diagrams may be complex. Start with architecture view
- **Keep updated**: Re-run generation after major refactoring
- **Version control**: Commit source files (`.mmd`, `.puml`), gitignore generated SVGs
- **Share**: Export to PNG or PDF for sharing with non-technical stakeholders

---

## File References

- Analysis script: `scripts/analyze_project.py`
- Diagram generator: `scripts/generate_diagrams.py`
- Templates: `templates/`
- Examples: `examples/`

---

**Next step**: Run `/kc-docs analyze <your_project_path>` to get started!
