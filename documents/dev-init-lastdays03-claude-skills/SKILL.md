---
name: dev-init
description: Standards for project scaffolding, directory structure, and initial documentation.
---

# Dev Init Standards

## Purpose
To ensure every project starts with a **consistent, professional structure** that integrates seamlessly with Antigravity Agents.

## Standard Layouts

### 1. Python Project
- `src/`: Source code
- `tests/`: Unit and integration tests
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `.gitignore`: Standard Python ignores

### 2. Study Project
- `notebooks/`: Jupyter Notebooks
- `data/`: Raw and processed data (ignored by git)
- `references/`: Papers and PDFs
- `docs/`: Summaries and plans

## Documentation Standards
- **README.md**: Must exist at root.
- **Metadata**: Must include `Status`, `Type`, `Created` in blockquote.
- **Agent Friendly**: `.agent` folder must NOT be git-ignored.
