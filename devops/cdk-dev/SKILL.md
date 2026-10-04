---
name: cdk-dev
description: 'CDK実装の一気通貫ワークフロー。実装→コードレビュー→CI までを人間への確認なしに自律実行する。Issue番号を引数に指定すること（例: /cdk-dev 15）。アプリケーションコードには使用しない。'
argument-hint: '<Issue番号>'
---

# /cdk-dev

Issue番号: $ARGUMENTS

CDK実装 → コードレビュー → レビュー指摘修正 → CI実行 → CI指摘修正 を順次自律実行する。
**全フェーズを人間への確認なしに自律実行すること。**

## 実行手順

1. **Phase 1: CDK実装** - `cdk-imp` スキルを Skill ツールで Issue番号 `$ARGUMENTS` を渡して起動し、CDK実装をこの場（インライン）で実行する（詳細は下記「Phase 1: CDK実装の制約」）。AskUserQuestion が必要な箇所は全て最初の選択肢（デフォルト）で自動選択し、人間への確認なしに最後まで自律実行すること
2. **Phase 2: コードレビュー** - Phase 1 完了後、`cdk-review` スキルを Skill ツールで起動し、完了を待つ
3. **Phase 3: レビュー指摘修正とループ** - 詳細は下記「Phase 2〜3: レビューと修正のループ」
4. **Phase 4: CI実行** - `cdk-ci` スキルを Skill ツールで起動し、完了を待つ
5. **Phase 5: CI指摘修正** - Phase 4 の結果にエラーがある場合、静的解析・スナップショットテスト・cdk synthのエラーを修正する。エラーなしの場合はスキップ
6. 各フェーズの出力を**そのまま全文表示**する（要約・加工・コメント追加は禁止）

## Phase 1: CDK実装の制約

`cdk-imp` スキルを起動する際、以下の制約を守ること：

- 対象は `infra/` 配下のみ。アプリケーションコードのディレクトリ（`app/`）は絶対に実装・変更しない
- 新規に Stack / Construct を書き起こす前に `samples/infra/` を Read する（構造・テストの手本）。`samples/` 自体は変更しない
- Issueのタスク一覧のうち、CDK/インフラに関するタスクのみを対象とする
- 設計書を参照し、CDK実装・テスト・cdk synth まで完了させる
- 完了した CDK タスクのみ `gh issue edit $ARGUMENTS` でGitHub Issueのチェックリストを更新する

## Phase 2〜3: レビューと修正のループ

合否・再レビューの回数・修正範囲は [ai-review-gate-policy](../../../docs/policy/ai-review-gate-policy.md) に従う（自律型ワークフロー）。

- 指摘があれば、severity にかかわらずすべて直す（例外は同ポリシー「直す範囲は毎回すべて」の残してよい例外だけ）。修正後 Phase 2 へ戻り `cdk-review` を再起動する。**再レビューには前回の指摘を渡さない**
- レビューは最大2回（初回を含む）。残してよい例外以外の Critical が0件になった回で合格とし、その回に出た High・Medium もその場で直してから Phase 4 へ進む
- 2回目のレビューで指摘が出たら、直したうえで再レビューせずに Phase 4 へ進む

## エラーハンドリング

- Phase 1 失敗 → Phase 2 以降は実行しない。`/cdk-imp $ARGUMENTS` で個別実行を案内する
- Phase 2 失敗 → Phase 1 の実装は完了済み。`/cdk-review` で個別実行を案内する
- Phase 3 修正不要（指摘なし）→ Phase 4 へスキップ
- Phase 4 失敗 → エラー内容を表示し中断。`/cdk-ci` で個別実行を案内する
- Phase 5 修正後も CI 失敗 → エラー内容を表示し、手動での修正を案内する
