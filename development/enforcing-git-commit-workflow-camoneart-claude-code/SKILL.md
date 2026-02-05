---
name: Enforcing Git Commit Workflow
description: Enforce semantic commit practices with proper file staging and prefix usage. Use when committing code, managing git history, or when user mentions git/commit/コミット.
allowed-tools: Bash, Read
---

# Enforcing Git Commit Workflow

意味のあるコミット履歴を保つための厳格なGitワークフロー管理スキル。

## いつ使うか

- コードをコミットする時
- ユーザーがgit関連の操作を要求した時
- コミットメッセージの作成が必要な時

## 基本原則

### 1. 機能別コミットを原則とする
各コミットは1つの明確な目的を持つこと。

### 2. `git add -A` 禁止
**例外**: `pnpx changeset version` が生成した大量のパッケージ更新を commit する場合のみ。

### 3. 必ず個別ステージング
```bash
# ✅ 正しい
git add path/to/changed-file.ts
git add another/file.test.ts
git commit -m "test: add edge-case tests for suggest command"

# ❌ 間違い
git add -A
git commit -m "update files"
```

## Prefix 一覧

詳細は [prefix-reference.md](prefix-reference.md) を参照。

### 主要なPrefix

| Prefix       | 用途 (日本語)            | 説明                                                         |
| ------------ | ---------------------- | ------------------------------------------------------------ |
| **fix**      | バグ修正                 | コードの不具合を修正するコミット                             |
| **hotfix**   | クリティカルなバグ修正      | サービス停止レベルの緊急バグ対応                             |
| **add**      | 新規機能追加              | 新しいファイルや小規模機能を追加するコミット                 |
| **feat**     | 新機能                   | ユーザー向けの大きな機能追加または変更                       |
| **update**   | 機能修正                 | 既存機能に対する修正・改善（バグ修正ではない）               |
| **change**   | 仕様変更                 | 仕様そのものを変更するコミット                               |
| **clean**    | 整理                    | 使われていないコードの削除や軽微な整理                       |
| **disable**  | 無効化                  | 機能を一時的に無効化（コメントアウト等）                     |
| **refactor** | リファクタリング          | 挙動を変えずに内部構造のみ改善                               |
| **remove**   | 削除                    | ファイル・ライブラリ・機能を削除するコミット                 |
| **upgrade**  | バージョンアップ          | 依存ライブラリや FW のメジャーアップデート                   |
| **revert**   | 変更取り消し             | 以前のコミットを打ち消すコミット                             |
| **docs**     | ドキュメント             | README やコメントのみの変更                                  |
| **style**    | スタイル修正             | コードフォーマット、空白、セミコロンなど動作に影響しない変更 |
| **perf**     | パフォーマンス            | パフォーマンス改善のための実装変更                           |
| **test**     | テスト                   | テストコードの追加・更新・リファクタ                         |
| **chore**    | 雑多メンテ               | ビルド、CI、依存更新など本番コードに影響しない作業           |

## 実行フロー

### ステップ1: ファイル分類
変更ファイルを目的別にグループ化：
- テストコード
- 実装コード
- ドキュメント
- 設定ファイル

### ステップ2: 個別ステージング
```bash
# テストを先にコミット
git add src/__tests__/feature.test.ts
git commit -m "test: add tests for new feature"

# 次に実装
git add src/feature.ts
git commit -m "feat: implement new feature"
```

### ステップ3: 不明点の確認
判断できない場合は**必ずユーザーに確認**：
- 「この変更はどのカテゴリに属しますか？」
- 「これらのファイルは一緒にコミットして良いですか？」

## 警告・中断処理

以下を検出した場合、**警告を表示し処理を中断**：
- `git add -A` の使用（例外: changeset version）
- 不明確なコミットメッセージ
- 複数の目的が混在するコミット

ユーザーが強制実行を指定しない限り続行しない。

## 自動コミット禁止

Claude Code 自身が判断して Push まで行う場合でも、上記手順に従ってログを分割すること。

## 参考

詳細なPrefix一覧とガイドラインは [prefix-reference.md](prefix-reference.md) を参照。
