---
name: git-review
description: This skill should be used when the user needs to review and respond to GitHub Pull Request comments. It automatically fetches review comments (both inline code comments and PR-level comments) from GitHub Codex, Claude Code, or human reviewers, organizes them by priority, and lets the user select which items to address using AskUserQuestion. After the user selects items, the main agent automatically implements the fixes.
---

# git-review

## 目的

PRのレビューコメント（コード行コメント + PR全体コメント）を自動取得し、優先度別に整理してユーザーに提示する。ユーザーがAskUserQuestionで対応項目を選択すると、メインエージェントが自動的に修正を実施する。

## 使用タイミング

以下の状況でこのスキルを使用する：

- PRにレビューコメントが付いた時
- GitHub Codex / Claude Codeのコメントを確認したい時
- 複数のレビュー指摘を整理して優先順位付けしたい時
- レビュー対応を効率的に進めたい時

## 実行手順

### 1. PR情報とレビューコメントを取得

```bash
# PR基本情報
gh pr view <PR番号> --json number,title,state,author,url

# コード行コメント
gh api repos/{owner}/{repo}/pulls/{PR番号}/comments

# PR全体コメント
gh pr view <PR番号> --comments
```

詳細は `references/command-details.md` を参照。

### 2. レビュー指摘を分類・整理

取得したコメントを以下の基準で分類する：

- **レビュアー別**: GitHub Codex / Claude Code / 人間
- **優先度別**: P0（必須）/ P1（重要）/ P2（推奨）/ P3（軽微）
- **ファイル別**: 各指摘がどのファイルに関連するか

優先度判定ロジックの詳細は `references/command-details.md#コメント分類ロジック` を参照。

### 3. AskUserQuestionで対応項目を選択させる

**重要**: 全ての指摘に自動的に対応せず、必ずユーザーに選択させる。

**AskUserQuestionの制限事項**:
- 1つの質問で最大4つの選択肢まで
- 優先度の高い指摘（P0/P1）を優先的に提示
- P0/P1が4つを超える場合は、P0のみまたはP0+P1の上位4つに絞る
- P2/P3は、P0/P1が4つ以下の場合のみ追加
- 指摘が多い場合は、「残りの指摘は次回対応」と明示

```
AskUserQuestion:
  question: "どのレビュー指摘に対応しますか？（複数選択可）"
  header: "レビュー対応"
  multiSelect: true
  options:
    - label: "[P0] 最優先の指摘"
      description: "ファイル名 - 修正内容の要約"
    - label: "[P1] 重要な指摘"
      description: "ファイル名 - 修正内容の要約"
    # 最大4つまで
```

**選択肢が4つを超える場合の対応**:
1. P0指摘のみを提示（P0が4つ以下の場合）
2. P0が0個の場合、P1の上位4つを提示
3. 残りの指摘については「次回対応」として別途処理

出力フォーマット例は `references/output-examples.md` を参照。

### 4. 選択された項目の詳細をメインエージェントに返す

ユーザーが選択した項目について、以下の情報を含めて返す：

- ファイル名と行番号
- 優先度
- レビュアー名
- 問題内容
- 推奨修正方法
- 該当コード箇所

### 5. メインエージェントでの対応（このスキル外）

**このスキル終了後、メインエージェントは以下を自動的に実施する：**

1. TodoWriteでタスクリスト作成
2. 選択された全項目を修正（ファイル読み込み→編集→ビルド）
3. `git-commit-push` スキルでコミット・プッシュ

**重要**: ユーザーに「修正しますか？」と確認しない。AskUserQuestionで既に選択済みのため、即座に修正を開始する。

## 処理フロー図

```
[git-reviewスキル]
  ↓ PR情報取得
  ↓ レビューコメント取得
  ↓ 指摘事項を分類（優先度順）
  ↓ AskUserQuestionで選択
  ↓ 選択された項目の詳細を返す

[メインエージェント]
  ↓ TodoWrite作成
  ↓ 修正実施
  ↓ git-commit-pushスキル
```

## エラーハンドリング

| エラー | 対処方法 |
|-------|---------|
| PR番号が無効 | 有効なPR番号を再確認する |
| gh未認証 | `gh auth login` を実行するよう指示 |
| レビューコメントなし | "レビューコメントはまだありません" と表示 |
| API制限 | レート制限に達した場合は待機時間を表示 |

## 使用例

### ケース1: 現在のブランチのPRレビューを取得

```
Skill: git-review

現在のブランチのPRレビューを取得してください。
```

### ケース2: 特定のPR番号を指定

```
Skill: git-review

PR #395 のレビューコメントを取得してください。
```

### ケース3: 特定のレビュアーのコメントのみ

```
Skill: git-review

PR #395 のGitHub Codexからのコメントのみを表示してください。
```

## 制限事項

このスキルでは**対応しない**操作（メインエージェントで実行）：

- レビューコメントへの返信
- レビューの承認/却下
- レビューコメントの解決マーク
- コードの修正

## 参照ドキュメント

必要に応じて以下のドキュメントを参照する：

- **`references/command-details.md`**: gh CLIコマンド詳細、コメント分類ロジック
- **`references/output-examples.md`**: 出力フォーマットの具体例（PR #399の実例）
- **`references/lessons-learned.md`**: 実際のレビュー対応から得られた教訓
  - 優先度判定の基準と実例（P0/P1/P2/P3）
  - AskUserQuestionの効果的な活用方法
  - 対応済み判定の注意点（コミットメッセージだけでは不十分）
  - レビュー対応フローとベストプラクティス

## 関連Skill

- `git-commit-push`: レビュー対応後のコミット・プッシュ
- `git-create-pr`: PR作成
