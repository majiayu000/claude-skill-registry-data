---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Automated software development pipeline. Scans projects, prioritizes tasks, analyzes code, and orchestrates development loops. Zero dependencies (Python stdlib only).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="dev-soft-agent banner">

> **English** — Official English version of `dev-soft-agent`.


# Dev Soft Agent (English)

Automated software development pipeline. Extracted from BACH's ATI agent,
runs fully standalone with pure Python standard library.

## Components

```
scripts/
  config.py              Configuration (scan folders, naming prefixes, weights)
  project_manager.py     Project scan + classification by naming convention
  task_engine.py          TASKS.txt parser + code scanner (TODO/FIXME)
  code_analyzer.py       Static analysis (LOC, imports, classes, functions)
  dev_loop.py            Orchestrator (DevLoop)
  policies/
    naming.py            snake_case / PascalCase / SCREAMING_SNAKE validation
    encoding.py          UTF-8 enforcement + BOM detection
    paths.py             Hardcoded path detection
  prompt_templates/
    task_prompt.txt      LLM prompt for task processing
    review_prompt.txt    LLM prompt for code review
    analysis_prompt.txt  LLM prompt for project analysis
```

## Usage as Python Library

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Scan projects (Deutsch)
projects = loop.scan_projects()

# Select project (weighted random selection by naming convention) (Deutsch)
project = loop.select_project()

# Analyze code (Deutsch)
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Load and prioritize tasks (Deutsch)
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Complete dev session (Deutsch)
result = loop.run_session()
loop.save_session()
```

## Usage as CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## Naming Convention (Project Classification)

Projects are classified based on their folder name:

| Prefix | Label | Weight | Meaning |
|--------|-------|--------|---------|
| `RDY` | Ready | 1.0 | Highest priority |
| `RDY_FAST` | Fast Ready | 0.5 | Quick to complete |
| `FAST` | Fast | 0.33 | Small task |
| `DEV` | Development | 0.17 | In development |
| `REL` | Released | 0.0 | Done, no work needed |
| `ARC` | Archived | 0.0 | Archived |

Weight determines the probability in random selection.

## TASKS.txt Format

```markdown
# TASKS - ProjectName (Deutsch)
# As of: 2026-03-12 (Deutsch)

## OPEN
- [ ] [BUG] Description of the bug
- [ ] [FEATURE] New feature

## IN PROGRESS
- [-] [REFACTOR] Code restructuring

## DONE
- [x] [BUG] Fixed bug -- DONE 2026-03-01
```

## Policies

Quality policies that can be automatically checked against code:

- **NamingPolicy:** snake_case for modules/functions, PascalCase for classes
- **EncodingPolicy:** Enforce UTF-8, detect BOM, flag CRLF
- **PathPolicy:** Detect and report hardcoded absolute paths

## Changelog

### 0.1.0 (2026-03-12)
- Migration from MODULAR_AGENTS/devSoftAgent to skill library
- Project scanner, task engine, code analyzer, DevLoop
- 3 policies (naming, encoding, paths)
- 3 prompt templates (task, review, analysis)
