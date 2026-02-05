---
name: safe-commit
description: git commit を行う際に自動発動。禁止ディレクトリ（ai/, .serena/）のコミット防止と、論理的なコミット分割を支援する。
---

# Safe Commit

コミット前に必ず以下を確認・実行する。

## 禁止ディレクトリのチェック

コミット前に必ず実行:

```bash
# ステージングされた禁止ファイルを確認
git diff --cached --name-only | grep -E '^(ai/|\.serena/)'

# 存在する場合はアンステージ
git reset HEAD -- ai/ .serena/ 2>/dev/null || true
```

### 禁止対象
- `ai/` - セッションログ、一時ファイル
- `.serena/` - Serena MCP設定

これらは **絶対にコミットしない**。

## コミット計画

複数の論理的変更がある場合は `/commit-plan` を実行して分割を検討。

## チェックリスト

コミット実行前:
1. [ ] `git diff --cached --name-only` で禁止ディレクトリがないか確認
2. [ ] 禁止ファイルがあれば `git reset HEAD -- ai/ .serena/`
3. [ ] 変更が論理的に分割されているか確認
4. [ ] コミットメッセージが "why" を説明しているか確認
