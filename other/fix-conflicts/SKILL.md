---
name: fix-conflicts
description: GitHub Pull Request の merge conflict を base branch の最新変更を取り込みながら解消し、検証して commit・push する skill。
disable-model-invocation: true
---

# Fix Conflicts

この skill は明示的に呼び出された場合のみ使用する。

```text
$fix-conflicts
$fix-conflicts pr#123
$fix-conflicts owner/repo#123
```

- 引数なし: 現在のブランチに対応する PR を対象にする
- `pr#<number>`: 現在の repository の指定 PR を対象にする
- `owner/repo#<number>`: 指定 repository の PR を対象にする

この skill の呼び出し自体を、対象 PR に対する merge・コード変更・commit・push の許可として扱う。

## Workflow

1. 対象 PR と base branch、PR のブランチを特定する
2. remote の最新状態を取得する
3. base branch の最新変更を PR のブランチへ merge する
4. 発生した conflict を確認する
5. base 側と PR 側の変更意図を確認して conflict を解消する
6. 関連するテスト・型チェック・lint・build を実行する
7. merge を commit する
8. PR のブランチへ push する

## Conflict の解消

conflict は機械的に片側を採用せず、両方の変更内容を確認して解消する。

以下を確認する。

- base 側で何が変更されたか
- PR 側で何を変更しようとしているか
- 両方の変更を維持する必要があるか
- 既存の仕様や呼び出し側と矛盾しないか

`ours` / `theirs` の一括採用で解消してはいけない。

仕様判断が必要で、既存コードやテストから判断できない場合は推測で決めない。

## 修正

conflict 解消に必要な範囲だけ変更する。

- 無関係なリファクタリングを行わない
- conflict と関係のない仕様は変更しない
- 既存の設計・命名・テストパターンを優先する

merge によって新たな不整合が生じた場合は、その解消に必要な範囲で修正してよい。

## 検証

conflict 解消後は、変更箇所に関連する検証をする。

merge による変更がテスト・型・lint・build に影響する場合は、対応する検証も実行する。

- 関連テスト
- 型チェック
- lint
- build

実行できない検証がある場合は、可能な代替検証を行う。

## Commit

base branch の取り込みによって生成される merge commit を使用する。

conflict 解消後に追加修正した場合は、別の commit に分けてよい。

追加 commit の message は Conventional Commits 形式にする。

```text
<type>(<scope>): <subject>
```

## Rules

- rebase は使用しない
- force push は行わない
- PR のブランチ以外へ push しない
- conflict を機械的に片側採用で解消しない
- 無関係な変更を commit に含めない
- Git の破壊的な操作を避ける

## Completion

完了時に以下を短く報告する。

- 取り込んだ base branch
- 解消した conflict
- conflict 解消時に行った判断
- 実行したテスト・検証
- commit / push の結果
