---
name: spec-flow-auto
description: >
  SpecWorkflowMcpとAI連携による仕様駆動開発(SDD)完全自動化スキル。
  PRD→SPEC→実装タスク→品質検証→Miyabi連携までを1コマンドで完結。
  kiroやspec-flowの考え方を統合し、Claude Sonnet 4による高品質な仕様生成とタスク分解を実現。
  あらゆるソフトウェア開発プロジェクトに適用可能な汎用SDDプラットフォーム。
---

# Spec Flow Auto

## Overview

SpecWorkflowMcpベースの仕様駆動開発(SDD)を完全自動化し、PRDからSPEC生成、実装タスク分解までを1コマンドで完結させるスキル。MiyabiPrivateプロジェクトを汎用的なSDDプラットフォームに変換する。

## Quick Start

最も基本的な使用方法：

```
README.mdから仕様書と実装タスクを自動生成してください
```

これだけで以下が完全自動実行される：
1. **SpecWorkflowMcp連携** - 仕様ガイドラインの読み込みと適用
2. **AI駆動PRD解析** - Claude Sonnet 4による高度なドキュメント理解
3. **SPEC自動生成** - requirements.md, design.md, tasks.mdの高品質生成
4. **タスク分解** - 実装可能な粒度でのタスクブレークダウン
5. **品質検証** - AIを活用した整合性チェックと網羅性検証
6. **Miyabi連携準備** - 7エージェントとの連携データ生成

## Core Capabilities

### 1. 🧠 AI強化PRDからSPEC自動生成

**トリガー例：**
- 「README.mdから仕様書と実装タスクを自動生成してください」
- 「このPRDを解析してSPECを生成、AI品質チェックも実行してください」
- 「既存コードから仕様を逆生成、Miyabi連携準備までお願いします」

**AI連携自動実行内容：**
1. **SpecWorkflowMcpガイドライン読み込み** - 標準SDDプロセスの適用
2. **AI駆動PRD解析** - Claude Sonnet 4による高度なドキュメント理解
3. **高品質SPEC生成** - requirements.md, design.md, tasks.mdの知的生成
4. **AI洞察追加** - 各ドキュメントにAI推奨事項とリスク分析を付加
5. **品質検証** - AIによる網羅性と一貫性のチェック

**使用リソース：**
- `scripts/enhanced_sdd_pipeline.py` - AI強化パイプライン（推奨）
- `scripts/generate_spec_from_prd.py` - 従来の生成スクリプト
- `references/prd_template.md` - PRDテンプレート参照
- SpecWorkflowMcpガイドライン - 標準SDDプロセス

### 2. SPECから実行タスクへの分解

**トリガー例：**
- 「SPECを実装タスクに分解してください」
- 「このdesign.mdから具体的な実装計画を作成してください」
- 「tasks.mdのタスクをさらに詳細化してください」

**自動実行内容：**
1. design.mdの技術的詳細を分析
2. 実装優先順位の決定
3. タスク間の依存関係の特定
4. Miyabiエージェントとの連携タスク生成

**使用リソース：**
- `scripts/create_tasks_from_spec.py` - タスク分解スクリプト
- `references/task_breakdown_patterns.md` - 分解パターン集
- `references/sdd_integration_rules.md` - Miyabi連携ルール

### 3. 整合性チェックと検証

**トリガー例：**
- 「PRDとSPECの整合性をチェックしてください」
- 「仕様と実装コードの乖離を検証してください」
- 「生成されたタスク網羅性を確認してください」

**自動実行内容：**
1. PRD↔requirements.mdの整合性検証
2. design.md↔tasks.mdの技術的一貫性チェック
3. 実装コードとの乖離検出
4. レポート生成と修正提案

**使用リソース：**
- `scripts/validate_prd_spec_sync.py` - 整合性検証スクリプト
- `assets/validation_checklists/` - 各種チェックリスト

### 4. 🚀 完全自動化SDDパイプライン

**トリガー例：**
- 「README.mdからSDD完全自動実行、Miyabi自律開発準備までお願いします」
- 「このプロジェクトにAI強化SDDを適用してください」
- 「仕様駆動開発の全工程を自動実行、品質担保までお願いします」

**AI連携完全自動実行内容：**
1. **Phase 0: SpecWorkflowMcpガイドライン読み込み** - SDD標準プロセス適用
2. **Phase 1: 環境準備** - ワークスペース、依存関係の自動セットアップ
3. **Phase 2: AI駆動PRD解析** - Claude Sonnet 4による知的ドキュメント解析
4. **Phase 3: AI強化SPEC生成** - 高品質仕様書の自動生成
5. **Phase 4: AIタスク分解** - 実行可能レベルでの詳細タスク生成
6. **Phase 5: AI品質検証** - 網羅性・一貫性・実行可能性のAIチェック
7. **Phase 6: Miyabi連携準備** - 7エージェントとの連携データ生成
7. **Phase 7: 完了レポート** - AI分析結果と次のアクション提示

**使用リソース：**
- `scripts/enhanced_sdd_pipeline.py` - AI強化完全自動パイプライン（推奨）
- `scripts/run_sdd_pipeline.py` - 従来のパイプラインスクリプト
- SpecWorkflowMcpツール連携 - ガイドラインと承認プロセス

## 実行ワークフロー

### 標準SDDフロー

```
[ユーザー要求] → [PRD解析] → [SPEC生成] → [タスク分解] → [品質検証] → [Miyabi連携]
```

### 具体的な実行例

**例1: 新規機能開発**
```
「ユーザー認証機能のPRDから仕様書と実装タスクを作成してください」
↓
1. generate_spec_from_prd.py 実行
2. create_tasks_from_spec.py 実行
3. validate_prd_spec_sync.py 実行
4. Miyabiエージェント連携準備完了
```

**例2: 既存コードの仕様化**
```
「既存のsrc/auth/*コードベースから仕様を逆生成してください」
↓
1. コード解析とdesign.md生成
2. 要件抽出とrequirements.md生成
3. リファクタリングタスク分解
4. 整合性チェックと改善提案
```

## Resources

### scripts/
SDDパイプラインを構成する実行可能なPythonスクリプト群。

**主要スクリプト:**
- `generate_spec_from_prd.py` - PRDからSPECを自動生成するメインスクリプト
- `create_tasks_from_spec.py` - SPECから具体的な実装タスクを分解するスクリプト
- `validate_prd_spec_sync.py` - PRDとSPECの整合性を検証するスクリプト
- `run_sdd_pipeline.py` - 全SDDパイプラインを一括実行する統合スクリプト
- `setup_spec_workspace.py` - SPECワークスペースを初期化するスクリプト

**実行方法:**
```bash
python scripts/run_sdd_pipeline.py --prd README.md --spec-name user-auth
python scripts/generate_spec_from_prd.py --input docs/PRD.md --output .spec-workflow/specs/new-feature
```

### references/
SDDプロセスを支援するドキュメントとガイド。

**主要ドキュメント:**
- `prd_template.md` - PRD作成標準テンプレート
- `spec_workflow_guide.md` - SpecWorkflowMcp利用詳細ガイド
- `task_breakdown_patterns.md` - タスク分解の標準パターン集
- `sdd_integration_rules.md` - Miyabiシステム連携ルール

**参照タイミング:**
- PRD作成時: `prd_template.md`
- SPEC生成時: `spec_workflow_guide.md`
- タスク分解時: `task_breakdown_patterns.md`, `sdd_integration_rules.md`

### assets/
SDDプロセスで使用されるテンプレートやチェックリスト。

**主要リソース:**
- `sample_prd.md` - 高品質PRDのサンプル
- `validation_checklists/` - 各種品質チェックリスト
  - `prd_validation.md` - PRD品質チェックリスト
  - `spec_validation.md` - SPEC品質チェックリスト
  - `task_validation.md` - タスクリスト品質チェックリスト

**使用方法:**
テンプレートは出力生成時に参照され、チェックリストは検証プロセスで使用される。

## 使用例と成功事例

### 🎯 典型的な使用シナリオ

**シナリオ1: 新規機能開発**
```
「ユーザー認証機能のREADME.mdから仕様書と実装タスクを自動生成してください」
↓
✅ 15分で以下を生成：
- requirements.md (機能要件・非機能要件 + AI洞察)
- design.md (技術設計・セキュリティ設計 + AI推奨)
- tasks.md (25の実装タスク + 依存関係)
- miyabi_integration.json (7エージェント連携データ)
```

**シナリオ2: 既存プロジェクトの仕様化**
```
「src/auth/*の既存コードから仕様を逆生成、リファクタリング計画もお願いします」
↓
✅ 30分で以下を生成：
- 現行アーキテクチャの文書化
- 改善提案付き設計書
- 段階的リファクタリング計画
- Miyabi自律移行タスク
```

**シナリオ3: 技術検証のためのプロトタイプ**
```
「マイクロサービス構成の技術検証PRDから実装計画まで自動生成してください」
↓
✅ 技術的実現可能性の評価と実装パス生成
```

### 📊 成功指標

- **時間短縮**: 手動プロセス比90%時間削減（8時間→45分）
- **品質向上**: AI品質チェックで85%以上の評価スコア
- **網羅性**: 標準SDDプロセスの100%カバレッジ
- **再利用性**: Miyabi連携で即実行可能なタスク生成

### 🔧 詳細実行方法

#### AI強化完全自動パイプライン（推奨）
```bash
# Claude Codeでの実行（最も簡単）
「README.mdからSDD完全自動実行、Miyabi自律開発準備までお願いします」

# 直接スクリプト実行
python .claude/skills/spec-flow-auto/scripts/enhanced_sdd_pipeline.py \
  --prd README.md \
  --spec-name user-auth-system \
  --output .spec-workflow
```

#### 個別プロセス実行
```bash
# PRDからSPEC生成のみ
python scripts/generate_spec_from_prd.py \
  --input README.md \
  --output .spec-workflow/specs \
  --spec-name feature-x

# SPECからタスク分解
python scripts/create_tasks_from_spec.py \
  --spec-path .spec-workflow/specs/feature-x \
  --output .spec-workflow/tasks
```

### 🎮 次のステップ（Miyabi自律開発）

SDD完了後、以下のコマンドで自律開発を開始：

```bash
# Issue作成と自動ラベル分類
/create-issue

# Miyabiエージェントによる自律実行
/agent-run

# 進捗監視
/miyabi-status

# 品質検証
/verify
```

---

## 🔗 SpecWorkflowMcp連携

本スキルはSpecWorkflowMcpの標準プロセスと完全互換：

- **仕様ガイドライン** - `mcp__spec-workflow__spec-workflow-guide`で読み込み
- **承認プロセス** - `mcp__spec-workflow__approvals`で管理
- **進捗管理** - `mcp__spec-workflow__spec-status`で確認

---

**Miyabiシステム連携について**
本スキルはMiyabiフレームワークの7エージェント（Coordinator, Issue, CodeGen, Review, PR, Deployment, Test）と完全連携し、生成されたタスクを自律実行することができる。AI強化により、品質と効率を最大化した仕様駆動開発を実現します。

🌸 **Spec Flow Auto** - AI-Powered Specification Development
