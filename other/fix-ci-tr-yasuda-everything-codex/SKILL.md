---
name: fix-ci
description: GitHub Pull Request の失敗している CI を調査し、コードで解決できる問題を修正して commit・push する skill。
disable-model-invocation: true
---

# Fix CI

この skill は明示的に呼び出された場合のみ使用する。

```text
$fix-ci
$fix-ci pr#123
$fix-ci owner/repo#123
```

- 引数なし: 現在のブランチに対応する PR を対象にする
- `pr#<number>`: 現在の repository の指定 PR を対象にする
- `owner/repo#<number>`: 指定 repository の PR を対象にする

この skill の呼び出し自体を、対象 PR に対するコード変更・commit・push の許可として扱う。

## Workflow

1. 対象 PR を特定する
2. 失敗している CI を確認する
3. 失敗した job / step のログを確認し、原因を特定する
4. コード・テスト・CI 設定で解決すべき問題だけを修正する
5. 関連するテスト・型チェック・lint・build を実行する
6. Conventional Commits 形式で commit する
7. PR のブランチへ push する
8. 解決できなかった CI の失敗があれば報告する

## 原因の確認

CI が失敗していることだけを理由にコードを変更しない。

原因が次のどれに当たるか確認する。

- コード・テスト・CI 設定の問題
- flaky なテストや処理
- repository 外の環境・権限・外部サービスの問題

コード・テスト・CI 設定に原因がある場合は修正する。

repository 外に原因がある場合は、無理にコードを変更せず原因を報告する。

flaky な場合は可能な範囲で根本原因を確認し、単純な retry や sleep だけで隠さない。

## 修正

修正は、CI の失敗原因を解消するための最小限の変更にする。

- 無関係な箇所は変更しない
- CI を通すためだけに test、型チェック、lint、validation を弱めない
- 既存の設計・命名・テストパターンを優先する

失敗しているテストが正しい仕様を表している場合は、本番コードを修正する。

テスト側が誤っている場合は、根拠を確認したうえでテストを修正する。

## 検証

修正後は、失敗していた CI に対応する検証をローカルで実行する。

失敗した CI の原因がテスト・型・lint・build に関わる場合は、対応する検証も実行する。

- 関連テスト
- 型チェック
- lint
- build

実行できない検証がある場合は、可能な代替検証を行う。

## Commit

commit message は Conventional Commits 形式にする。

```text
<type>(<scope>): <subject>
```

例は次のとおり。

```text
fix: handle empty response in session lookup
test: remove timing dependency from reconnect test
ci: fix node setup for pnpm cache
```

複数の CI の失敗が同じ根本原因から発生している場合は、1つの commit にまとめてよい。

## Rules

- PR のブランチ以外へ push しない
- 原因を確認せずに修正しない
- repository 外の問題をコード変更で無理に解決しない
- Git の破壊的な操作を避ける

## Completion

完了時に以下を短く報告する。

- 特定した原因
- 行った修正
- 実行したテスト・検証
- commit / push の結果
- 解決できなかった CI の失敗
