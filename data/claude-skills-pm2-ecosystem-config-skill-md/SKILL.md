---
name: .claude/skills/pm2-ecosystem-config/SKILL.md
description: |
  PM2エコシステム設定の設計と最適化を専門とするスキル。
  Alexandre Strzelewiczの思想に基づき、ecosystem.config.js の
  構成、実行モード選択、環境設定、監視設定を体系的に設計します。
  
  📖 参照書籍:
  - 『The Pragmatic Programmer』（Andrew Hunt, David Thomas）: 実践的改善
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/config-structure-guide.md`: ecosystem.config.js構造（apps配列、必須/推奨オプション、共通設定）
  - `resources/environment-management.md`: env階層設計、env_production分離、機密情報外部化パターン
  - `resources/execution-modes.md`: fork vs cluster選択基準、instances数決定、負荷タイプ別最適化
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-ecosystem.mjs`: ecosystem.config.js構文検証と設定項目の整合性チェック
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/ecosystem.config.template.js`: PM2設定ファイルテンプレート（実行モード、再起動戦略、環境変数含む）
  
  Use proactively when designing PM2 configurations, optimizing.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "The Pragmatic Programmer"
    author: "Andrew Hunt, David Thomas"
    concepts:
      - "実践的改善"
      - "品質維持"
---

# PM2 Ecosystem Configuration

## 概要

PM2エコシステム設定の設計と最適化を専門とするスキル。
Alexandre Strzelewiczの思想に基づき、ecosystem.config.js の
構成、実行モード選択、環境設定、監視設定を体系的に設計します。

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
- PM2でNode.jsアプリケーションを管理する時
- ecosystem.config.jsを新規作成する時
- 既存PM2設定を最適化する時
- 本番環境でのプロセス管理設定を設計する時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/pm2-ecosystem-config/resources/Level1_basics.md
cat .claude/skills/pm2-ecosystem-config/resources/Level2_intermediate.md
cat .claude/skills/pm2-ecosystem-config/resources/Level3_advanced.md
cat .claude/skills/pm2-ecosystem-config/resources/Level4_expert.md
cat .claude/skills/pm2-ecosystem-config/resources/config-structure-guide.md
cat .claude/skills/pm2-ecosystem-config/resources/environment-management.md
cat .claude/skills/pm2-ecosystem-config/resources/execution-modes.md
cat .claude/skills/pm2-ecosystem-config/resources/legacy-skill.md
```

### スクリプト実行
```bash
node .claude/skills/pm2-ecosystem-config/scripts/log_usage.mjs --help
node .claude/skills/pm2-ecosystem-config/scripts/validate-ecosystem.mjs --help
node .claude/skills/pm2-ecosystem-config/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/pm2-ecosystem-config/templates/ecosystem.config.template.js
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
