---
name: sdd-documentation
description: ソフトウェア設計ドキュメント（SDD）を作成・管理・実装します。requirements/、design/、tasks/の作成から、タスク実行・逆順レビューまでの全工程を統括します。SDDワークフロー全体の管理が必要な場合に使用してください。
version: "1.0.0"
---

# SDD ドキュメンテーションスキル

ソフトウェア設計ドキュメント（SDD）の作成・管理・実装を統括するオーケストレータースキルです。

## 概要

このスキルは、以下の6つのサブスキルを連携させて、要件定義から実装・メンテナンスまでの全工程を管理します：

| サブスキル | 役割 | 成果物 |
|-----------|------|--------|
| **requirements-defining** | EARS記法による要件定義 | docs/requirements/ |
| **software-designing** | 技術アーキテクチャ設計 | docs/design/ |
| **task-planning** | AIエージェント向けタスク分解 | docs/tasks/ |
| **task-executing** | タスク実行・逆順レビュー | 実装コード |
| **sdd-troubleshooting** | 問題分析・修正方針策定 | docs/troubleshooting/, docs/tasks/ |
| **sdd-document-management** | ドキュメント管理・メンテナンス | docs/archive/, docs/reports/ |

## ドキュメント構成

```text
docs/
├── requirements/           # 要件定義
│   ├── index.md           # 目次・概要
│   ├── stories/US-XXX.md  # ユーザーストーリー詳細
│   └── nfr/*.md           # 非機能要件
├── design/                # 設計
│   ├── index.md           # 目次・アーキテクチャ概要
│   ├── components/*.md    # コンポーネント詳細
│   ├── api/*.md           # API設計詳細
│   ├── database/schema.md # データベーススキーマ
│   └── decisions/DEC-XXX.md # 技術的決定事項
├── tasks/                 # タスク管理
│   ├── index.md           # 目次・進捗サマリ
│   └── phase-N/TASK-XXX.md # タスク詳細
├── troubleshooting/       # トラブルシューティング
│   └── [YYYY-MM-DD]-[issue-name]/
├── archive/               # アーカイブ（完了済み）
│   ├── tasks/             # 完了済みタスク
│   ├── decisions/         # 古い決定事項
│   └── troubleshooting/   # 完了した問題分析
└── reports/               # 管理レポート
    ├── consistency/       # 整合性チェックレポート
    ├── sync/              # 実装同期チェックレポート
    ├── archive/           # アーカイブレポート
    └── optimize/          # 最適化レポート
```

## このスキルを使用する場面

### 一括初期化
- 新規プロジェクトでSDDドキュメント一式が必要な場合

### 全体管理
- 3つのドキュメント間の整合性を確認したい場合
- 逆順レビュー（タスク → 設計 → 要件）を実施したい場合

### 実装フェーズ
- docs/tasks/に沿って実装を行う場合
- 実装後の逆順レビューが必要な場合

### トラブルシューティング
- システムの動作不良や問題が報告された場合
- 問題の根本原因を分析したい場合
- 修正方針の策定と承認が必要な場合

### ドキュメント管理
- ドキュメント間の矛盾を検出・解消したい場合
- 実装とドキュメントの同期を確認したい場合
- 完了済みタスクをアーカイブしたい場合
- 肥大化したファイルを整理したい場合

### 個別作業が必要な場合
特定の工程のみ実施する場合は、各サブスキルを直接使用：
- 要件定義のみ → `requirements-defining`
- 設計のみ → `software-designing`
- タスク計画のみ → `task-planning`
- 実装のみ → `task-executing`
- 問題分析のみ → `sdd-troubleshooting`
- ドキュメント管理のみ → `sdd-document-management`

## ワークフロー

### 新規開発フロー

```text
1. 初期化 → docs/ディレクトリ構造を作成
      ↓
2. requirements-defining → docs/requirements/
      ↓ ユーザー確認・承認
3. software-designing → docs/design/
      ↓ ユーザー確認・承認
4. task-planning → docs/tasks/
      ↓ ユーザー確認・承認
5. ドキュメント逆順レビュー
      ↓
6. task-executing → 実装コード
      ↓
7. 実装逆順レビュー → 完了
```

### トラブルシューティングフロー

```text
1. 問題事象の確認
      ↓
2. 根本原因の分析
      ↓
3. 仕様との照合（docs/requirements/, docs/design/）
      ↓
4. 修正方針の策定
      ↓
5. ★ ユーザー承認 ★（必須ゲート）
      ↓
6. タスク分割 → docs/tasks/に追加
      ↓
7. task-executing → 修正実装
```

## ドキュメント初期化

「docsディレクトリを初期化してください」と依頼されたら：

1. **ディレクトリ構造の作成**
2. **requirements/index.md** - テンプレート: `requirements-defining/assets/templates/requirements_index_template_ja.md`
3. **design/index.md** - テンプレート: `software-designing/assets/templates/design_index_template_ja.md`
4. **tasks/index.md** - テンプレート: `task-planning/assets/templates/tasks_index_template_ja.md`

## 逆順レビュープロセス

```text
docs/tasks/ → docs/design/ → docs/requirements/
```

詳細なチェック項目は `references/checklist_ja.md` を参照。

## EARS記法クイックリファレンス

| パターン | 形式 | 使用場面 |
|---------|------|----------|
| 基本 | `システムは〜しなければならない` | 常時適用される要件 |
| イベント | `〜の時、システムは〜しなければならない` | イベント駆動要件 |
| 条件 | `もし〜ならば、システムは〜しなければならない` | 状態依存要件 |
| 継続 | `〜の間、システムは〜しなければならない` | 継続的要件 |
| 場所 | `〜において、システムは〜しなければならない` | コンテキスト固有要件 |

## ユーザーとの対話ガイドライン

### 情報分類プロセス

1. **明示された情報**: ユーザーが明確に述べた要件、仕様、制約
2. **不明な情報**: 推測が必要な項目（「おそらく〜」は不明として扱う）

### 確認の形式

```text
ドキュメント作成の前に、以下の点を確認させてください：

【明示された情報】
- [ユーザーから明示的に指定された内容]

【不明/要確認の情報】
1. [項目1]: [選択肢A] / [選択肢B] / その他
2. [項目2]: [具体的な質問]

上記の不明点について教えていただけますか？
```

## リソース

### リファレンス
- ワークフローガイド: `references/workflow_guide_ja.md`
- 検証チェックリスト: `references/checklist_ja.md`

### サブスキル
- 要件定義: `requirements-defining/SKILL.md`
- 設計: `software-designing/SKILL.md`
- タスク計画: `task-planning/SKILL.md`
- タスク実行: `task-executing/SKILL.md`
- トラブルシューティング: `sdd-troubleshooting/SKILL.md`
- ドキュメント管理: `sdd-document-management/SKILL.md`
