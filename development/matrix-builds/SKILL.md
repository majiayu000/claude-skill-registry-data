---
name: matrix-builds
description: |
  GitHub Actionsマトリックスビルド戦略設計・最適化スキル。複数OS、バージョン、環境での並列テストを実現。

  Anchors:
  • GitHub Actions Documentation / 適用: strategy.matrix / 目的: 並列CI/CD
  • GitHub Actions Workflow Syntax / 適用: include/exclude / 目的: 条件付きビルド

  Trigger:
  Use when configuring matrix builds, multi-environment testing, CI parallelization,
  dynamic matrix generation, or optimizing max-parallel settings.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Matrix Builds

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

GitHub Actions のマトリックスビルド戦略設計スキル。

**対象機能**:

| 機能            | 説明                           |
| --------------- | ------------------------------ |
| strategy.matrix | OS/バージョン/環境の組み合わせ |
| include/exclude | 条件付きマトリックス拡張・除外 |
| fail-fast       | ビルド失敗時の制御             |
| max-parallel    | 最大並列実行数                 |
| fromJSON()      | 動的マトリックス生成           |

---

## ワークフロー

### Phase 1: 要件分析

**Task**: `agents/analyze-requirements.md`

| 入力       | 出力             |
| ---------- | ---------------- |
| テスト要件 | マトリックス設計 |

**参照**: `references/basics.md`

### Phase 2: マトリックス設計

**Task**: `agents/design-matrix.md`

| 入力             | 出力              |
| ---------------- | ----------------- |
| マトリックス設計 | ワークフロー YAML |

**参照**: `references/patterns.md`, `references/dynamic-matrix.md`

### Phase 3: 検証

**Task**: `agents/validate-matrix.md`

| 入力              | 出力         |
| ----------------- | ------------ |
| ワークフロー YAML | 検証レポート |

---

## ベストプラクティス

| すべきこと                        | 避けるべきこと                    |
| --------------------------------- | --------------------------------- |
| 必要な変動軸を明確に定義          | 過度な組み合わせ爆発              |
| fail-fast: false で全結果確認     | デフォルト fail-fast の無意識使用 |
| max-parallel で並列数を最適化     | 無制限並列によるリソース枯渇      |
| fromJSON() で動的マトリックス生成 | ハードコードされたマトリックス    |
| include/exclude で条件付き拡張    | 複雑すぎる条件の組み合わせ        |

---

## Task ナビゲーション

| Task                      | 目的                           | 参照リソース  |
| ------------------------- | ------------------------------ | ------------- |
| `analyze-requirements.md` | テスト環境・バージョン要件分析 | `basics.md`   |
| `design-matrix.md`        | マトリックス構造設計           | `patterns.md` |
| `validate-matrix.md`      | YAML 構文・動作検証            | scripts       |

---

## リソース参照

### References

| ファイル             | 内容                                | 読込条件   |
| -------------------- | ----------------------------------- | ---------- |
| `basics.md`          | マトリックス基礎構文                | 初回使用時 |
| `patterns.md`        | include/exclude、fail-fast パターン | 設計時     |
| `dynamic-matrix.md`  | fromJSON() 動的生成                 | 動的生成時 |
| `matrix-strategy.md` | 詳細戦略ガイド                      | 最適化時   |

### Assets

| ファイル               | 内容                           |
| ---------------------- | ------------------------------ |
| `matrix-template.yaml` | マトリックスビルドテンプレート |

### Scripts

| スクリプト            | 用途                 |
| --------------------- | -------------------- |
| `generate-matrix.mjs` | マトリックス自動生成 |
| `log_usage.mjs`       | 使用記録             |

---

## クイックリファレンス

### 基本構文

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
```

### include/exclude

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
    exclude:
      - os: windows-latest
        node: 18
    include:
      - os: ubuntu-latest
        node: 22
        experimental: true
```

### fail-fast 制御

```yaml
strategy:
  fail-fast: false # 全ジョブ完了まで継続
  max-parallel: 4 # 最大並列数
```

---

## 関連スキル

- `github-actions-syntax` - ワークフロー構文
- `caching-strategies-gha` - キャッシュ戦略
- `reusable-workflows` - 再利用可能ワークフロー
