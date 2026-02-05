---
name: executing-ai-development-workflow
description: Execute a comprehensive AI-driven development workflow with planning, implementation, multi-layer review (Sub-agents + /review + CodeRabbit CLI), automated fixes, and PR creation. Use when implementing new features, performing large refactorings, developing security-critical features, or when the user mentions "AI開発ワークフロー", "AI development workflow", or "計画的に実装".
---

# Executing AI Development Workflow

## 概要

AI開発のベストプラクティスを体系化した10ステップの自動化ワークフローを実行します。
計画立案から実装、多層レビュー、自動修正、PR作成まで一貫して管理します。

### 主な特徴

- ✅ **多層レビューシステム**: 4つのSub-agent + Claude Code `/review` + CodeRabbit CLI
- ✅ **優先度ベースの修正**: Critical/High/Medium/Lowで自動分類
- ✅ **完全なドキュメント化**: プランとレビュー結果を`_docs/`に保存
- ✅ **妥当性重視**: AIレビューの誤検知を適切に判断
- ✅ **人間の介入ポイント**: 重要な判断箇所で確認を求める

## 使い方

以下のようなリクエストでこのSkillが発動します：

```
「AI開発ワークフローで〜を実装して」
「Use the executing-ai-development-workflow skill to implement...」
「計画的に実装したい」
```

詳細な使用例は [examples.md](examples.md) を参照してください。

## ワークフロー概要

```
1. Planning (プラン作成 - Claude Codeプランモード)
   ↓
2. Documentation (プランを_docs/plans/にチェックボックス付きで保存)
   ↓
3. Implementation (Sub-agentで実装)
   ↓
4. Multi-layer Review
   ├─ 4a. 複数の評価用Sub-agent（並列実行）
   ├─ 4b. Claude Code /review コマンド
   └─ 4c. CodeRabbit CLI
   ↓
5. Review Documentation (_docs/reviews/に統合保存)
   ↓
6. Automated Fixes (Critical/High優先度の妥当なもののみ)
   ↓
7. Human Confirmation (Medium優先度の妥当性判断)
   ↓
8. PR Creation (GitHub PR作成 + CodeRabbitとClaude Codeがレビュー)
   ↓
9. PR Review Response (妥当なもののみClaude Codeで修正)
   ↓
10. Merge (+ 人力レビューを適宜挟む)
```

詳細な各ステップの説明は [workflow.md](workflow.md) を参照してください。

## 主要な実行フロー

### Step 1-3: 計画と実装

1. **プランニング**: プランモードで実装計画を立案
2. **ドキュメント化**: `_docs/plans/YYYY-MM-DD-[feature-name].md` に保存
3. **実装**: 適切なSub-agentに委任

### Step 4-5: 多層レビュー

**4a. Sub-agent Reviews（並列実行）**:
- code-reviewer
- security-auditor
- architect-review
- test-ai-tdd-expert

**4b. Claude Code `/review`**:
```bash
/review
```

**4c. CodeRabbit CLI**:
```bash
coderabbit --prompt-only --type uncommitted
```

結果を `_docs/reviews/YYYY-MM-DD-[feature-name]-review.md` に統合保存。

### Step 6-7: 修正と確認

- **Critical/High**: 妥当なもののみ自動修正
- **Medium**: 人間が妥当性を判断（修正/保留/却下）
- **Low**: 記録のみ

### Step 8-10: PR作成とマージ

1. レビューサマリー付きでPR作成
2. CodeRabbitとClaude Codeが追加レビュー
3. 妥当な指摘のみ修正
4. 人力レビューを適宜挟みながらマージ

## 優先度判定

`config.json` で定義された優先度ルール:

| 優先度 | 内容 | 対応 |
|--------|------|------|
| 🔴 Critical | セキュリティ脆弱性、重大なバグ | 妥当なものを即時自動修正 |
| 🟠 High | パフォーマンス問題、設計問題 | 妥当なものを即時自動修正 |
| 🟡 Medium | コード品質、ベストプラクティス | 人間が妥当性判断 |
| 🟢 Low | スタイル、命名、軽微な改善 | 記録のみ |

## 人間確認ポイント

以下の3つのタイミングで必ず人間の確認を得ます：

1. ✅ **プラン承認時** (Step 1後)
2. ✅ **Medium優先度の修正判断時** (Step 7)
3. ✅ **PR作成前の最終確認** (Step 8前)

## 前提条件

### 必要なツール

- **Git**: バージョン管理
- **GitHub CLI (`gh`)**: PR作成・管理
- **CodeRabbit CLI**: インストール済み & 認証済み

### プロジェクト準備

```bash
# _docs ディレクトリの作成
mkdir -p _docs/plans _docs/reviews
```

## 設定ファイル

### config.json

優先度判定ルールとSub-agent設定を定義:

```json
{
  "priority_rules": {
    "critical": { "keywords": [...], "patterns": [...] },
    "high": { "keywords": [...] },
    "medium": { "keywords": [...] },
    "low": { "keywords": [...] }
  },
  "review_agents": [...],
  "coderabbit_cli": {...},
  "auto_fix_threshold": "high"
}
```

### テンプレート

- `templates/plan.md`: 実装計画テンプレート
- `templates/review.md`: レビュー結果テンプレート

## 重要な考え方

このSkillは、AI駆動開発において**「妥当性」**を重視します。

- ✅ AIレビューの指摘は**すべてが正しいわけではない**
- ✅ Critical/Highでも**誤検知や過剰な提案**がある
- ✅ **人間の判断**が最も重要
- ✅ プロジェクトの文脈を理解した上で**適切に取捨選択**

AIはツールです。最終的な判断は常に人間が行います。

## 関連ファイル

- [workflow.md](workflow.md): 詳細なステップガイド
- [examples.md](examples.md): 具体的な使用例
- [config.json](config.json): 優先度判定ルールと設定
- [templates/plan.md](templates/plan.md): プランテンプレート
- [templates/review.md](templates/review.md): レビューテンプレート

