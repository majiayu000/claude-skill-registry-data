---
name: .claude/skills/repository-pattern/SKILL.md
description: |
  Martin FowlerのPoEAAに基づくRepositoryパターン設計と実装を専門とするスキル。
  アプリケーション層とデータアクセス層を分離し、ドメインエンティティをコレクション風
  インターフェースで操作する抽象化を提供します。
  
  📖 参照書籍:
  - 『Design Patterns』（Erich Gamma et al.）: 設計パターン
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/design-principles.md`: Repository設計原則
  - `resources/entity-mapping.md`: エンティティマッピングガイド
  - `resources/implementation-patterns.md`: Repository実装パターン
  - `resources/interface-patterns.md`: Repositoryインターフェース設計パターン
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-repository.mjs`: Repository構造検証スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/repository-implementation-template.md`: Repository実装テンプレート
  - `templates/repository-interface-template.md`: Repositoryインターフェーステンプレート
  - `resources/requirements-index.md`: 要求仕様の索引（docs/00-requirements と同期）
  
  Use proactively when handling repository pattern tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "Design Patterns"
    author: "Erich Gamma et al."
    concepts:
      - "設計パターン"
      - "拡張性"
---

# Repository Pattern

## 概要

Martin FowlerのPoEAAに基づくRepositoryパターン設計と実装を専門とするスキル。
アプリケーション層とデータアクセス層を分離し、ドメインエンティティをコレクション風
インターフェースで操作する抽象化を提供します。

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
- Repositoryインターフェースを設計する時
- Repository実装を作成する時
- ドメインエンティティとDB型の変換を設計する時
- 既存のRepositoryをリファクタリングする時

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/repository-pattern/resources/Level1_basics.md
cat .claude/skills/repository-pattern/resources/Level2_intermediate.md
cat .claude/skills/repository-pattern/resources/Level3_advanced.md
cat .claude/skills/repository-pattern/resources/Level4_expert.md
cat .claude/skills/repository-pattern/resources/design-principles.md
cat .claude/skills/repository-pattern/resources/entity-mapping.md
cat .claude/skills/repository-pattern/resources/implementation-patterns.md
cat .claude/skills/repository-pattern/resources/interface-patterns.md
cat .claude/skills/repository-pattern/resources/legacy-skill.md
```

### スクリプト実行
```bash
node .claude/skills/repository-pattern/scripts/log_usage.mjs --help
node .claude/skills/repository-pattern/scripts/validate-repository.mjs --help
node .claude/skills/repository-pattern/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/repository-pattern/templates/repository-implementation-template.md
cat .claude/skills/repository-pattern/templates/repository-interface-template.md
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
