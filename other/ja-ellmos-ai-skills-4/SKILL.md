---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 自動化ソフトウェア開発パイプライン。プロジェクトのスキャン、タスクの優先順位付け、コード分析、開発ループのオーケストレーションを行います。依存関係ゼロ（Python標準ライブラリのみ）。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="dev-soft-agent banner">

> **日本語** — `dev-soft-agent` の公式日本語版。


# Dev Soft Agent (日本語)

自動化ソフトウェア開発パイプライン。BACH の ATI エージェントから抽出され、
純粋な Python 標準ライブラリのみで完全にスタンドアロンで動作します。

## コンポーネント

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

## Python ライブラリとしての使用

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

## CLI としての使用

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## 命名規則（プロジェクト分類）

プロジェクトはフォルダ名に基づいて分類されます：

| プレフィックス | ラベル | 重み | 意味 |
|--------|-------|--------|---------|
| `RDY` | Ready | 1.0 | 最高優先度 |
| `RDY_FAST` | Fast Ready | 0.5 | 迅速に完了可能 |
| `FAST` | Fast | 0.33 | 小規模タスク |
| `DEV` | Development | 0.17 | 開発中 |
| `REL` | Released | 0.0 | 完了、作業不要 |
| `ARC` | Archived | 0.0 | アーカイブ済み |

重みはランダム選択における確率を決定します。

## TASKS.txt フォーマット

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

## ポリシー

コードに対して自動検証可能な品質ポリシー：

- **NamingPolicy:** モジュール/関数は snake_case、クラスは PascalCase
- **EncodingPolicy:** UTF-8 の強制、BOM の検出、CRLF のフラグ付け
- **PathPolicy:** ハードコードされた絶対パスの検出と報告

## 変更履歴

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/devSoftAgent からスキルライブラリへの移行
- プロジェクトスキャナー、タスクエンジン、コードアナライザー、DevLoop
- 3つのポリシー（命名、エンコーディング、パス）
- 3つのプロンプトテンプレート（タスク、レビュー、分析）
