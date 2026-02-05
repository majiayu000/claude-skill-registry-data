---
name: work_plan
description: 作業計画を立てたり遂行する際に利用するスキル。作業項目の追加、次のタスク取得、完了マークなどの機能を提供します。
---

# Work Plan

## 概要

作業計画を管理するためのスキルです。作業項目をWORK_PLAN.mdファイルにマークダウン形式で保存し、順次処理していきます。

**重要**: 作業計画を立てる際は、必ず [PLAN.md](./PLAN.md) のガイドラインに従ってください。各作業項目には具体的な作業内容を明記し、テスト・検証を同一ステップ内に含める必要があります。

## 使い方

### 1. 作業項目の追加

新しい作業項目を追加します。

```bash
python3 .claude/skills/work_plan/work_plan.py add "<タイトル>" "<本文>"
```

例（[PLAN.md](./PLAN.md)のガイドラインに従った良い例）：
```bash
python3 .claude/skills/work_plan/work_plan.py add "ユーザー認証機能の実装" "- LoginFormコンポーネントを作成する
    - ユーザー名とパスワードの入力フィールドを追加
    - バリデーションロジックを実装
- JWT認証ロジックを実装する
- LoginFormのユニットテストを追加する
- 全てのユニットテストが通ることを確認する"
```

本文は省略可能ですが、具体的な作業内容を記述することを推奨します：
```bash
python3 .claude/skills/work_plan/work_plan.py add "依存パッケージの更新"
```

### 2. 次の作業項目を取得

未完了の作業項目のうち、最初のものを取得します。

```bash
python3 .claude/skills/work_plan/work_plan.py next
```

出力例：
```
ID: 1
Title: ユーザー認証機能の実装

- LoginFormコンポーネントを作成する
    - ユーザー名とパスワードの入力フィールドを追加
    - バリデーションロジックを実装
- JWT認証ロジックを実装する
- LoginFormのユニットテストを追加する
- 全てのユニットテストが通ることを確認する
```

すべて完了している場合：
```
All work items are completed!
```

### 3. 作業項目を完了にする

指定したIDの作業項目を完了状態にします。

```bash
python3 .claude/skills/work_plan/work_plan.py complete <ID>
```

例：
```bash
python3 .claude/skills/work_plan/work_plan.py complete 1
```

### 4. すべての作業項目を一覧表示

全作業項目の一覧を表示します。

```bash
python3 .claude/skills/work_plan/work_plan.py list
```

出力例：
```
[✓] 1: ユーザー認証機能の実装
    - LoginFormコンポーネントを作成する
[ ] 2: ユーザープロフィール画面の実装
    - UserProfileコンポーネントを作成する
[ ] 3: ドキュメントの更新
    - READMEにAPI仕様を追加する
```

### 5. 作業計画をクリア

すべての作業項目を削除します（WORK_PLAN.mdファイルを削除します）。新しい作業を開始する前に既存の計画をクリアする際に使用します。

```bash
python3 .claude/skills/work_plan/work_plan.py clear
```

出力例：
```
Work plan cleared (WORK_PLAN.md deleted)
```

## データ形式

作業項目は `WORK_PLAN.md` にマークダウンのチェックリスト形式で保存されます。

```markdown
- [x] 1: ユーザー認証機能の実装

    - LoginFormコンポーネントを作成する
        - ユーザー名とパスワードの入力フィールドを追加
        - バリデーションロジックを実装
    - JWT認証ロジックを実装する
    - LoginFormのユニットテストを追加する
    - 全てのユニットテストが通ることを確認する

- [ ] 2: ユーザープロフィール画面の実装

    - UserProfileコンポーネントを作成する
        - プロフィール情報の表示機能を実装
        - プロフィール編集フォームを追加
    - /api/v1/users/:idエンドポイントを作成する
    - UserProfileのユニットテストを追加する
    - 全てのユニットテストが通ることを確認する

- [ ] 3: ドキュメントの更新

    - READMEにAPI仕様を追加する
        - 認証エンドポイントの説明を記述
        - ユーザーエンドポイントの説明を記述
    - 使用例のコードスニペットを追加する
    - ドキュメントに記載した内容が正しく動作することを確認する
```

- `[x]`: 完了
- `[ ]`: 未完了
- 数字: 作業項目ID（自動採番）
- 本文は4スペースでインデント
- 各作業項目には具体的な作業内容とテスト・検証を含める（[PLAN.md](./PLAN.md)参照）

## ワークフロー例

1. 計画フェーズ：必要な作業項目をすべて追加

ガイドライン（[PLAN.md](./PLAN.md)）に従い、各作業項目には具体的な作業内容とテスト・検証を含めます。

```bash
python3 .claude/skills/work_plan/work_plan.py add "ユーザー認証機能の実装" "- LoginFormコンポーネントを作成する
    - ユーザー名とパスワードの入力フィールドを追加
    - バリデーションロジックを実装
- JWT認証ロジックを実装する
    - /api/v1/auth/loginエンドポイントを作成
    - トークンの生成と検証機能を実装
- LoginFormのユニットテストを追加する
- 認証エンドポイントのテストを追加する
- 全てのユニットテストが通ることを確認する"

python3 .claude/skills/work_plan/work_plan.py add "ユーザープロフィール画面の実装" "- UserProfileコンポーネントを作成する
    - プロフィール情報の表示機能を実装
    - プロフィール編集フォームを追加
- /api/v1/users/:idエンドポイントを作成する
- UserProfileのユニットテストを追加する
- 全てのユニットテストが通ることを確認する"

python3 .claude/skills/work_plan/work_plan.py add "ドキュメントの更新" "- READMEにAPI仕様を追加する
    - 認証エンドポイントの説明を記述
    - ユーザーエンドポイントの説明を記述
- 使用例のコードスニペットを追加する
- ドキュメントに記載した内容が正しく動作することを確認する"
```

2. 実行フェーズ：nextコマンドで次のタスクを確認し、作業後にcompleteで完了マーク

```bash
# 次のタスクを確認
python3 .claude/skills/work_plan/work_plan.py next

# 作業を実施...

# 完了マーク
python3 .claude/skills/work_plan/work_plan.py complete 1

# 次のタスクへ
python3 .claude/skills/work_plan/work_plan.py next
```

3. 進捗確認：listコマンドで全体の進捗を確認

```bash
python3 .claude/skills/work_plan/work_plan.py list
```

## コマンドリファレンス

### `add <title> [body]`
新しい作業項目を追加します。

- `title`: 作業項目のタイトル（必須）
- `body`: 作業項目の詳細説明（省略可能）

### `next`
未完了の作業項目のうち、先頭のものを取得します。すべて完了している場合は、その旨を表示します。

### `complete <id>`
指定したIDの作業項目を完了状態にします。

- `id`: 作業項目のID（数値）

### `list`
すべての作業項目を一覧表示します。完了状態も表示されます。

### `clear`
すべての作業項目を削除します（WORK_PLAN.mdファイルを削除します）。新しい作業計画を開始する際に使用します。
