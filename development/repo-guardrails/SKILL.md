---
name: repo-guardrails
description: リポジトリの絶対ルール（DB境界・契約ファースト・作業範囲制御）を強制する
metadata:
  short-description: ルール遵守のガードレール
---

# repo-guardrails

この skill は、リポジトリにおける絶対ルールを強制する。

## 絶対ルール

- データベースへのアクセスは `apps/api` のみに限定する。
- `apps/bot` からデータベースへ直接アクセスしない。
- API の入出力定義は `packages/contracts` を正とする。

## 作業範囲

- 依頼されていないファイルやディレクトリを変更しない。
- 明示されていない依存関係の追加を行わない。
- 差分が約200行を超える見込みの場合、作業を止めて確認を求める。

## コマンド実行

- 読み取り専用コマンドは自動実行してよい（例: git status, git diff, git grep, ls）。
- 破壊的または外部影響のあるコマンドは事前確認を行う。
