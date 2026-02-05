---
name: project-simplification
description: Simplifies Flutter projects by analyzing structure, cleaning redundant docs, merging configs, refactoring large files, generating module documentation, and running validation tests. Use when optimizing project structure, removing technical debt, improving code organization, or creating project documentation.
allowed-tools: Read, Grep, Glob, Bash(*), Edit, Write
model: claude-sonnet-4-5-20250929
---

# Flutter Project Simplification

A comprehensive skill for optimizing Flutter project structure, removing technical debt, and improving code organization through automated analysis, intelligent refactoring, and documentation generation.

## What This Skill Does

Provides tools and guidance to:
- **Analyze** project structure and identify issues
- **Clean** redundant documentation files
- **Merge** duplicate configuration files
- **Refactor** oversized files into maintainable components
- **Generate** comprehensive module and project documentation
- **Validate** project quality and correctness

Each task can be run independently or combined into a complete workflow.

## Quick Start

Tell Claude what you need:

### Individual Tasks
Run any task independently, in any order:

- **"Analyze my project structure"** - Identify structural issues, duplicates, and large files
- **"Clean up redundant documentation"** - Remove duplicate README and CHANGELOG files
- **"Merge configuration files"** - Consolidate pubspec.yaml, .gitignore, analysis_options.yaml
- **"Refactor large files"** - Break up files over 500 lines into logical components
- **"Generate module documentation"** - Create README files for all modules and project root
- **"Validate my project"** - Run comprehensive quality checks

### Complete Workflow
For full project optimization:

- **"Simplify my Flutter project"** - Execute all tasks in recommended sequence

## Intent-Based Workflows

### "Analyze my project structure"

**What happens:**
- Runs structure analysis script
- Scans lib/ directory and modules
- Identifies duplicates, large files, deep nesting
- Reports circular dependencies and issues
- Generates `analysis_report.json`

**→ [Detailed Guide](guides/analyze-structure.md)**

---

### "Clean up redundant documentation"

**What happens:**
- Finds duplicate README, CHANGELOG, and guide files
- Helps review and merge unique content
- Updates references to consolidated docs
- Removes redundant files

**→ [Detailed Guide](guides/clean-docs.md)**

---

### "Merge configuration files"

**What happens:**
- Finds duplicate pubspec.yaml, analysis_options.yaml, .gitignore
- Guides merging of configurations
- Consolidates into root directory
- Updates references and verifies builds

**→ [Detailed Guide](guides/merge-configs.md)**

---

### "Refactor large files"

**What happens:**
- Identifies files over 500 lines
- Suggests extraction strategies (models, services, widgets)
- Helps split into logical components
- Updates imports and verifies functionality

**→ [Detailed Guide](guides/refactor-files.md)**

---

### "Generate documentation"

**What happens:**
- Extracts module descriptions from code
- Generates README.md for each module
- Creates comprehensive root README with:
  - Module catalog and links
  - Project structure
  - Quick start guide
  - Tech stack overview

**→ [Detailed Guide](guides/generate-docs.md)**

---

### "Validate my project"

**What happens:**
- Runs `flutter analyze` for code quality
- Verifies build integrity
- Runs test suite
- Checks file organization
- Validates documentation links

**→ [Detailed Guide](guides/validate.md)**

---

### "Simplify my entire project"

**Complete workflow** combining all above tasks in optimal sequence:
1. Analyze structure
2. Clean documentation
3. Merge configurations
4. Refactor large files
5. Generate documentation
6. Validate project

**→ [Complete Workflow Guide](guides/complete-workflow.md)**

## Available Scripts

Located in `.claude/skills/project-simplification/scripts/`:

**Analysis & Discovery:**
- `analyze_structure.py` - Analyze project structure and metrics
- `find_redundant_docs.py` - Find duplicate documentation
- `find_large_files.py` - Identify files needing refactoring
- `find_duplicate_configs.py` - Find duplicate configurations

**Documentation Generation:**
- `generate_module_descriptions.py` - Extract module information
- `generate_module_readmes.py` - Create module README files
- `generate_root_readme.py` - Create project root README

**Validation:**
- `validate_project.py` - Run comprehensive quality checks

## Configuration Options

Customize script behavior with environment variables:

```bash
# Analyze specific module only
MODULE=user_module python scripts/analyze_structure.py

# Custom file size threshold (lines)
FILE_SIZE_THRESHOLD=400 python scripts/find_large_files.py

# Check specific documentation patterns
DOC_PATTERNS="README,CHANGELOG,GUIDE" python scripts/find_redundant_docs.py

# Generate docs for specific modules
MODULES="module1,module2,module3" python scripts/generate_module_readmes.py
```

## Additional Resources

- **[Best Practices](guides/best-practices.md)** - Guidelines for successful simplification
- **[Troubleshooting](guides/troubleshooting.md)** - Common issues and solutions
- **[Complete Workflow](guides/complete-workflow.md)** - Step-by-step full process

## Key Principles

✓ **Incremental Changes** - Work on one module or task at a time
✓ **Version Control** - Commit before and after each phase
✓ **Continuous Testing** - Run tests after every change
✓ **Team Communication** - Keep team informed of structural changes
✓ **Documentation First** - Update docs during refactoring, not after

## When to Use This Skill

**Use when:**
- Project has grown organically and needs organization
- Files are becoming too large to maintain
- Documentation is outdated or scattered
- Configuration files are duplicated
- Technical debt is accumulating
- Onboarding new developers is difficult

**Regular usage:**
- Monthly: Quick structure analysis
- Quarterly: Documentation updates
- Annually: Comprehensive refactoring
