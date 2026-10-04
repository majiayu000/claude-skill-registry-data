---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Canalización automatizada de desarrollo de software. Escanea proyectos, prioriza tareas, analiza código u orquesta bucles de desarrollo. Cero dependencias (solo la biblioteca estándar de Python).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="dev-soft-agent banner">

> **Español** — Versión oficial en español de `dev-soft-agent`.


# Dev Soft Agent (Español)

Canalización automatizada de desarrollo de software. Extraída del agente ATI de BACH,
se ejecuta de forma totalmente independiente solo con la biblioteca estándar de Python.

## Componentes

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

## Uso como biblioteca de Python

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

## Uso como CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## Convención de nombres (clasificación de proyectos)

Los proyectos se clasifican según el nombre de su carpeta:

| Prefijo | Etiqueta | Peso | Significado |
|--------|-------|--------|---------|
| `RDY` | Ready | 1.0 | Máxima prioridad |
| `RDY_FAST` | Fast Ready | 0.5 | Rápido de completar |
| `FAST` | Fast | 0.33 | Tarea pequeña |
| `DEV` | Development | 0.17 | En desarrollo |
| `REL` | Released | 0.0 | Completado, no requiere trabajo |
| `ARC` | Archived | 0.0 | Archivado |

El peso determina la probabilidad en la selección aleatoria.

## Formato de TASKS.txt

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

## Políticas

Políticas de calidad que se pueden verificar automáticamente en el código:

- **NamingPolicy:** snake_case para módulos/funciones, PascalCase para clases
- **EncodingPolicy:** Aplicar UTF-8, detectar BOM, marcar CRLF
- **PathPolicy:** Detectar e informar rutas absolutas codificadas en el código

## Registro de cambios

### 0.1.0 (2026-03-12)
- Migración desde MODULAR_AGENTS/devSoftAgent a la biblioteca de skills
- Escáner de proyectos, motor de tareas, analizador de código y DevLoop
- 3 políticas (nombres, codificación, rutas)
- 3 plantillas de prompts (tarea, revisión, análisis)
