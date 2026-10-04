---
name: gen-requirements
description: Auto-generates clean, categorized requirements.txt and PEP 621 pyproject.toml by scanning Python codebase imports via AST. Resolves PyPI package names and installed versions.
version: 1.0.0
author: Human Skill Team
tags: ["python", "dependencies", "requirements", "pyproject", "ast", "scaffold"]
trigger_patterns:
  - "generate requirements"
  - "create requirements.txt"
  - "generate pyproject.toml"
  - "scan dependencies"
  - "auto requirements"
  - "pip requirements"
---

# Requirements & Dependency Generator

> *"One command. Zero manual dependency hunting."*

Auto-generates clean, categorized `requirements.txt` and PEP 621-compliant `pyproject.toml` files by analyzing Python codebase imports using Abstract Syntax Trees (AST).

---

## When to Use

Activate this skill when:
- Creating or updating `requirements.txt` for a Python project
- Generating PEP 621 `pyproject.toml` with dependencies and dev-dependencies
- Scanning a codebase to identify missing or used third-party packages
- Preparing a project for production deployment or distribution

---

## How to Use

### Via `human-skills` CLI

#### 1. Standard Generation (Minimum Constraints `>=X.Y.0`)
```bash
human-skills '{
    "tool_name": "gen_requirements",
    "tool_args": {
        "path": "/path/to/your/project"
    }
}'
```

#### 2. Exact Pinned Versions (`==X.Y.Z`)
```bash
human-skills '{
    "tool_name": "gen_requirements",
    "tool_args": {
        "path": "/path/to/your/project",
        "exact": "true"
    }
}'
```

#### 3. Custom Output Directory and Project Name
```bash
human-skills '{
    "tool_name": "gen_requirements",
    "tool_args": {
        "path": "/path/to/your/project",
        "name": "my-awesome-app",
        "output_dir": "/path/to/your/project"
    }
}'
```

#### 4. Specific Output Format
```bash
# Only requirements.txt
human-skills '{
    "tool_name": "gen_requirements",
    "tool_args": {
        "path": "/path/to/your/project",
        "format": "requirements"
    }
}'

# Only pyproject.toml
human-skills '{
    "tool_name": "gen_requirements",
    "tool_args": {
        "path": "/path/to/your/project",
        "format": "pyproject"
    }
}'
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|:---|:---|:---|:---|:---|
| `path` | string | No | `.` | Target Python project root directory to scan. |
| `exact` | string | No | `"false"` | Use exact pinned versions (`==X.Y.Z`) if `"true"`, otherwise `>=X.Y.0`. |
| `name` | string | No | Dir name | Project name written in `pyproject.toml`. |
| `output_dir` | string | No | `path` | Output directory where files will be created. |
| `format` | string | No | `"both"` | Output format: `"both"`, `"requirements"`, or `"pyproject"`. |
| `ignored_dirs` | string | No | `""` | Additional comma-separated directories to ignore during scan (e.g. `'tests,docs,demo'`). |
| `only_installed` | string | No | `"true"` | When `"true"`, filters out unverified/custom modules with no installed package version. When `"false"`, includes unversioned packages. |

---

## Key Features

1. **Target Virtualenv Resolution:** Automatically locates project-specific virtual environments (`.venv/`, `venv/`, `env/`) and queries installed package versions directly via subprocess `pip list`, eliminating host environment pollution.
2. **Double-Verification & Custom Module Defense:** Resolves exact installed versions from environment metadata (`importlib.metadata` and project venv). Any imported module that lacks installed distribution metadata is identified as a local/custom script or phantom import and excluded by default (`only_installed="true"`).
3. **AST-Powered Inspection:** Parses abstract syntax trees without executing untrusted code.
4. **Full `src/` & Local Module Discovery:** Recursively detects root packages, `src/`, `app/`, and `lib/` modules so local code is never misidentified as a third-party dependency.
5. **Namespace Package Support:** Accurately extracts and maps namespace packages like `google.generativeai` (`google-generativeai`), `azure.storage` (`azure-storage-blob`), etc.
6. **Universal & Clean Ignores:** Only ignores true build/VCS artifacts by default (`.git`, `.venv`, `__pycache__`, `node_modules`, etc.), while honoring `.gitignore` and allowing custom ignore overrides.
7. **Standard Library Filtering:** Automatically ignores all Python standard library modules (`os`, `sys`, `json`, `asyncio`, `pathlib`, etc.).
8. **Extended PyPI Distribution Mapping:** Maps non-trivial import names (`cv2` → `opencv-python`, `PIL` → `pillow`, `pydantic_settings` → `pydantic-settings`, `attr` → `attrs`, `markdown_it` → `markdown-it-py`).
9. **Functional Categorization:** Groups packages in `requirements.txt` by role (Core Math, Web/Networking, AI/Deep Learning, Configuration, Testing, etc.).
10. **PEP 621 Standard:** Outputs standard `pyproject.toml` with separate `dependencies` and `[project.optional-dependencies] dev`.
11. **Clear Failure Reporting:** Reports unparseable files, virtual environment status, and uninstalled packages without silent suppression.
