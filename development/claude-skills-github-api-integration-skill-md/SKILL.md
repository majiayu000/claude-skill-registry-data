---
name: .claude/skills/github-api-integration/SKILL.md
description: |
  GitHub API を GitHub Actions 内で活用するための統合スキル。
  専門分野:
  
  📖 参照書籍:
  - 『RESTful Web APIs』（Leonard Richardson）: リソース設計
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/graphql-api.md`: graphql-api の詳細ガイド
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/rest-api.md`: rest-api の詳細ガイド
  - `scripts/api-helper.mjs`: apihelperを処理するスクリプト
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/api-workflow.yaml`: api-workflow のテンプレート
  
  Use proactively when handling github api integration tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "RESTful Web APIs"
    author: "Leonard Richardson"
    concepts:
      - "リソース設計"
      - "HTTP設計"
---

# GitHub API Integration in Actions

## 概要

GitHub API を GitHub Actions 内で活用するための統合スキル。
専門分野:

詳細な手順や背景は `resources/Level1_basics.md` と `resources/Level2_intermediate.md` を参照してください。


## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `resources/Level1_basics.md` と `resources/Level2_intermediate.md` を確認
2. 必要な resources/scripts/templates を特定

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. 成果物が目的に合致するか確認
3. `scripts/log_usage.mjs` を実行して記録を残す


## ベストプラクティス

### すべきこと
- ワークフローからGitHub APIを呼び出す時
- gh CLIやcurlでGitHub操作を自動化する時
- IssueやPull Requestを自動作成・更新する時
- GraphQL APIで複雑なデータ取得を行う時
- API認証や権限設定に関する問題を解決する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/github-api-integration/resources/Level1_basics.md
cat .claude/skills/github-api-integration/resources/Level2_intermediate.md
cat .claude/skills/github-api-integration/resources/Level3_advanced.md
cat .claude/skills/github-api-integration/resources/Level4_expert.md
cat .claude/skills/github-api-integration/resources/graphql-api.md
cat .claude/skills/github-api-integration/resources/legacy-skill.md
cat .claude/skills/github-api-integration/resources/rest-api.md
```

### スクリプト実行
```bash
node .claude/skills/github-api-integration/scripts/api-helper.mjs --help
node .claude/skills/github-api-integration/scripts/log_usage.mjs --help
node .claude/skills/github-api-integration/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/github-api-integration/templates/api-workflow.yaml
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
