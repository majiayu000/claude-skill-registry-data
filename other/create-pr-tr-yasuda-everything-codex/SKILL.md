---
name: create-pr
description: 現在の変更を Conventional Commits 形式で commit・push し、GitHub Pull Request を作成または更新する skill。
disable-model-invocation: true
---

# Create PR

この skill は明示的に呼び出された場合のみ使用する。

```text
$create-pr
```

この skill の呼び出し自体を、commit・push・PR 作成の許可として扱う。

## Workflow

1. 現在の Git repository と変更内容を確認する
2. 必要なテスト・型チェック・lint・build が完了しているか確認する
3. 変更内容に合った Conventional Commits 形式の commit message を作る
4. 変更を stage して commit する
5. current branch を origin へ push する
6. 既存 PR の有無を確認する
7. PR がなければ Draft PR を作成し、存在する場合は更新する

## Commit / PR Title

commit message と PR title は Conventional Commits 形式にする。

```text
<type>(<scope>): <subject>
```

`scope` は省略してよい。

例は次のとおり。

```text
feat: add retry handling
fix(auth): prevent cross-tenant access
refactor: simplify session state handling
test: add regression coverage
```

type は変更内容に最も合うものを選ぶ。

- `feat`
- `fix`
- `refactor`
- `test`
- `docs`
- `style`
- `chore`
- `perf`
- `build`
- `ci`

PR title は、PR 全体の変更内容を表す Conventional Commits 形式にする。

## PR Body

repository に PR template がある場合は、それを使用する。

template がない場合は以下の形式にする。

```markdown
## Why

この変更が必要な理由を書く。

## What Changed

実際に変更した内容を簡潔に書く。
```

会話中に変更理由が説明されている場合は、その内容を PR body に反映する。

過程ではなく、最終的な差分だけを書く。

## Rules

- PR は Draft で作成する
- unrelated changes を commit に含めない
- 既存 PR がある場合は新しい PR を作らない
- PR title と body は実際の差分を確認してから作る
- local absolute path を PR body に書かない
- PR template の必須項目を削除しない
- push や PR 作成に失敗した場合は原因を確認し、解決可能なものは修正して続行する
