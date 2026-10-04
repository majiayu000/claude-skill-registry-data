---
name: flask-quality
description: Flaskプロジェクトの品質チェック。pytest-flask/mypy(strict)/Black/isortを実行。「Flaskの品質チェック」「Flask テスト」「Flaskのテスト実行」「Flask lint」「Flask型チェック」「Flaskフォーマット」で起動。Do NOT use for Django等の他フレームワーク、汎用Python品質チェック（→ python-quality）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
test: `pytest` (pytest-flask) | types: `mypy --strict` | format: `black` + `isort`

## Flask-specific Fixtures

| Fixture | 用途 |
|---------|------|
| `client` | test_client インスタンス |
| `app` | Flask アプリケーション |
| `app_context` | アプリケーションコンテキスト |

## Standards

| 項目 | 目標 |
|------|------|
| mypy | strict mode |
| カバレッジ | 90%+ |
| black/isort | エラー0 |

## Reference
- [reference.md](reference.md)
