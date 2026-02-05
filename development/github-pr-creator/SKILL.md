---
name: github-pr-creator
description: GitHub CLI で Pull Request を作成する。実装完了後や変更 push 後に PR を提出したい時に使用する。
---

# GitHub Pull Request Creator

GitHub CLI を使用して Pull Request を作成する。

## When to Use

以下の状況でこの Skill を使用する。

- ユーザーが変更を push した後、PR を作成したい時
- ユーザーが機能実装やタスクを完了し、PR を出したい時
- ユーザーが「PR作って」「プルリクエスト出して」などと言及した時

## Prerequisites

- ブランチが作成済み
- 変更がコミット済み
- 変更がリモートに push 済み

上記が満たされていない場合、git-operator skill を参照して Git 操作を完了させる。

## Procedure

### Issue Linking の確認

ユーザーが Issue を指定した場合、その Issue を使用する。

ユーザーが「Issue 不要」と明示した場合、Issue 紐づけなしで進める。

ユーザーが指定していない場合、PR の実装内容を簡潔に要約し、どの Issue に紐づけるか、または紐づけ不要かを確認する。

### テンプレート検出

PR テンプレートを検出する。
ファイル名は大文字小文字を区別しない。

単一ファイルテンプレートは以下の順序で検索する。
`.github/pull_request_template.md`、`pull_request_template.md`（リポジトリルート）、`docs/pull_request_template.md` の順に確認し、最初に見つかったものを使用する。

複数テンプレートディレクトリは以下の場所を確認する。

- `.github/PULL_REQUEST_TEMPLATE/`
- `PULL_REQUEST_TEMPLATE/`（リポジトリルート）
- `docs/PULL_REQUEST_TEMPLATE/`

単一ファイルが見つかった場合、読み込んで使用する。
ディレクトリが見つかった場合、利用可能なテンプレート一覧を表示し、ユーザーに選択を求める。
テンプレートが存在しない場合、[templates/default.md](templates/default.md) を使用する。

### PR 作成

`gh pr create` で Pull Request を作成し、PR URL をユーザーに報告する。

## Issue Link Format

PR テンプレートの有無に関わらず、Issue 紐づけには常にフル URL 形式を使用する。

```
- https://github.com/{owner}/{repo}/issues/xxx
```

## Title Guidelines

タイトルはタスクと実装内容を要約した自然言語の文にする。
コミットメッセージ形式（例: "chore(update): xxx"）は使用しない。

## Language

デフォルトで PR 内容は日本語で記述する。
ユーザーが英語を明示的にリクエストした場合は英語で記述する。
