---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 自动化软件开发流水线。扫描项目、优先处理任务、分析代码并编排开发循环。零依赖（仅限 Python 标准库）。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="dev-soft-agent banner">

> **中文** — `dev-soft-agent` 官方中文版本。


# Dev Soft Agent (中文)

自动化软件开发流水线。提取自 BACH 的 ATI 智能体，
仅使用 Python 标准库完全独立运行。

## 组件

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

## 作为 Python 库使用

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

## 作为 CLI 使用

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## 命名规范（项目分类）

项目根据其文件夹名称进行分类：

| 前缀 | 标签 | 权重 | 含义 |
|--------|-------|--------|---------|
| `RDY` | Ready | 1.0 | 最高优先级 |
| `RDY_FAST` | Fast Ready | 0.5 | 快速完成 |
| `FAST` | Fast | 0.33 | 小型任务 |
| `DEV` | Development | 0.17 | 开发中 |
| `REL` | Released | 0.0 | 已完成，无需进一步工作 |
| `ARC` | Archived | 0.0 | 已归档 |

权重决定了随机选择中的概率。

## TASKS.txt 格式

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

## 策略

可以对代码进行自动检查的质量策略：

- **NamingPolicy：** 模块/函数使用 snake_case，类使用 PascalCase
- **EncodingPolicy：** 强制使用 UTF-8，检测 BOM，标记 CRLF
- **PathPolicy：** 检测并报告硬编码的绝对路径

## 变更日志

### 0.1.0 (2026-03-12)
- 从 MODULAR_AGENTS/devSoftAgent 迁移至技能库
- 项目扫描器、任务引擎、代码分析器和 DevLoop
- 3 项策略（命名、编码、路径）
- 3 个提示词模板（任务、审查、分析）
