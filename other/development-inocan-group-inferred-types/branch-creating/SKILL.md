---
name: branch-creating
description: ブランチ作成時のルール
---

# ブランチ運用

- すべて `main` から分岐。`main` への直接 push は禁止。
- 命名:
  - 通常は、`feature/<yymmdd>-<短い説明>`（例: `feature/251128-add-link-check`）
  - 緊急修正は `hotfix/<yymmdd番号>-<短い説明>`。
