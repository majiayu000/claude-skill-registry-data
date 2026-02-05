---
name: .claude/skills/matrix-builds/SKILL.md
description: |
  GitHub Actionsのマトリックスビルド戦略（strategy.matrix）の設計と最適化。
  複数のOS、バージョン、環境での並列テスト実行、動的マトリックス生成、include/exclude条件、
  fail-fast制御、max-parallel設定による効率的なCI/CDパイプライン構築を支援。
  
  📖 参照書籍:
  - 『Don't Make Me Think』（Steve Krug）: ユーザビリティ
  
  📚 リソース参照:
  - `resources/Level1_basics.md`: レベル1の基礎ガイド
  - `resources/Level2_intermediate.md`: レベル2の実務ガイド
  - `resources/Level3_advanced.md`: レベル3の応用ガイド
  - `resources/Level4_expert.md`: レベル4の専門ガイド
  - `resources/dynamic-matrix.md`: fromJSON活用、変更ファイルベースの動的テスト選択、条件付きマトリックス生成
  - `resources/legacy-skill.md`: 旧SKILL.mdの全文
  - `resources/matrix-strategy.md`: include/exclude構文、fail-fast制御、max-parallel設定、マトリックス変数アクセス
  - `scripts/generate-matrix.mjs`: マトリックス設定の自動生成（OS/バージョン組み合わせ、YAML出力）
  - `scripts/log_usage.mjs`: 使用記録・自動評価スクリプト
  - `scripts/validate-skill.mjs`: スキル構造検証スクリプト
  - `templates/matrix-template.yaml`: マルチOS・マルチバージョンテスト用マトリックスビルドテンプレート
  
  Use proactively when handling matrix builds tasks.
version: 1.0.0
level: 1
last_updated: 2025-12-24
references:
  - book: "Don't Make Me Think"
    author: "Steve Krug"
    concepts:
      - "ユーザビリティ"
      - "情報設計"
---

# Matrix Builds Skill

## 概要

GitHub Actionsのマトリックスビルド戦略（strategy.matrix）の設計と最適化。
複数のOS、バージョン、環境での並列テスト実行、動的マトリックス生成、include/exclude条件、
fail-fast制御、max-parallel設定による効率的なCI/CDパイプライン構築を支援。

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
- resources/Level1_basics.md を参照し、適用範囲を明確にする
- resources/Level2_intermediate.md を参照し、実務手順を整理する

### 避けるべきこと
- アンチパターンや注意点を確認せずに進めることを避ける

## コマンドリファレンス

### リソース読み取り
```bash
cat .claude/skills/matrix-builds/resources/Level1_basics.md
cat .claude/skills/matrix-builds/resources/Level2_intermediate.md
cat .claude/skills/matrix-builds/resources/Level3_advanced.md
cat .claude/skills/matrix-builds/resources/Level4_expert.md
cat .claude/skills/matrix-builds/resources/dynamic-matrix.md
cat .claude/skills/matrix-builds/resources/legacy-skill.md
cat .claude/skills/matrix-builds/resources/matrix-strategy.md
```

### スクリプト実行
```bash
node .claude/skills/matrix-builds/scripts/generate-matrix.mjs --help
node .claude/skills/matrix-builds/scripts/log_usage.mjs --help
node .claude/skills/matrix-builds/scripts/validate-skill.mjs --help
```

### テンプレート参照
```bash
cat .claude/skills/matrix-builds/templates/matrix-template.yaml
```

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2025-12-24 | Spec alignment and required artifacts added |
