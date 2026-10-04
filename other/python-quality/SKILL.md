---
name: python-quality
description: Python品質チェック。pytest/mypy/Black実行時に使用。「Pythonの品質チェック」「Pythonの静的解析」で起動。Do NOT use for Flask固有の品質チェック（→ flask-quality）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
test: `pytest` | types: `mypy --strict` | lint: `ruff check` | format: `black` + `isort`

## Standards

| 項目 | 目標 |
|------|------|
| mypy | strict mode |
| カバレッジ | 90%+ |
| ruff/black | エラー0 |

## Reference
- [reference.md](reference.md)
