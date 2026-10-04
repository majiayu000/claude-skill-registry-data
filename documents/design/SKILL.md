---
name: design
description: 'GitHub Issue をもとに設計書（docs/design/）を更新し、レビューと修正まで自律実行する。Issue番号を引数に指定すること（例: /design 15）'
argument-hint: '<Issue番号>'
---

# /design

Issue番号: $ARGUMENTS

設計書更新（Phase 1）→ 設計書レビュー（Phase 2）→ レビュー結果に基づく修正（Phase 3）を順次実行する。  
人間への確認なしに自律的に実行する。

## 実行手順

1. **Phase 0（Issue読み込み）**: `gh issue view $ARGUMENTS --json number,title,body,labels` でIssue情報を取得し、以降のPhaseで参照できるよう保持する
2. **Phase 1**: `update-design` スキルを Skill ツールで Issue番号 `$ARGUMENTS` を渡して起動し、設計書更新をこの場（インライン）で実行する。設計書を新規に書き起こす場合は、書き始める前に `samples/docs/design/` を Read する（構成・図の粒度・表の書きぶりの手本）。`samples/` 自体は変更しない
3. **Phase 2**: Phase 1 完了後、`doc-review` スキルを Skill ツールで起動し、完了を待つ。引数には次を渡すこと
   - Phase 1 で更新された設計書のパス（レビュー対象）
   - Phase 0 で取得したIssue情報（番号・タイトル・スコープ）と、「このIssueの意図に基づいて設計書が更新されている」こと
   - 更新後の設計書が **`docs/requirements.md` の要件（機能・非機能・SLO を含む）を満たしているか**を照合し、未充足・矛盾があれば指摘するという指示（設計が要件を満たすことの検証。とくに SLO はアーキテクチャの構造が目標を満たせるかに直結する）
   - `--full` は渡さない。Phase 1 の更新は未コミットなので、`/doc-review` は今回の更新が生んだ違反だけを判定する（要件定義書との照合も同じ範囲）
4. **Phase 3: レビュー指摘修正とループ** - 詳細は下記「Phase 2〜3: レビューと修正のループ」
5. 各フェーズの出力を**そのまま全文表示**する（要約・加工・コメント追加は禁止）

## Phase 2〜3: レビューと修正のループ

合否・再レビューの回数・修正範囲は [ai-review-gate-policy](../../../docs/policy/ai-review-gate-policy.md) に従う（自律型ワークフロー）。

Phase 3 では、Phase 2 のレビュー結果をもとに、再度 `update-design` スキルの手順で設計書の修正をインライン実行する。その際以下を反映すること：

- Phase 2 の出力（レビュー結果）をそのまま含める
- Phase 0 で取得したIssue情報を含める
- **「Issueの意図に反する修正は行わないこと。レビュー指摘がIssueの計画と矛盾する場合は、Issueの意図を優先し、該当指摘はスキップすること」** という指示を明記する。**ただしスキップする指摘が Critical のときは、スキップする前にその1件を `.claude/skills/quick-issue/SKILL.md` の書式で `gh issue create` により起票する**（ai-review-gate-policy が定める残してよい例外の1つ。起票せずに直さず残すことは禁止）。起票した Issue 番号は、指摘の観点名・引用とあわせて「スキップ一覧」として保持する
- 上記スキップ対象を除き、指摘は severity にかかわらずすべて直す
- 修正後 Phase 2 へ戻り `doc-review` を再起動する。**再レビューには前回の指摘を渡さない**（スキップ一覧も渡さない。同じ指摘が再度出たら、新しく Issue を作らず、スキップ一覧の既存の Issue 番号のまま数える。同じ指摘かどうかは、スキップ一覧の観点名・引用と突き合わせ、ai-review-gate-policy の「再レビューで同じ指摘が出たら、既存の Issue 番号で数える」で決める）
- レビューは最大2回（初回を含む）。残してよい例外（`issue:needs-human-decision` に回した食い違い、上でスキップして Issue 化した Critical）以外の Critical が0件になった回で合格とし、その回に出た High・Medium もその場で直して完了する
- 2回目のレビューで指摘が出たら、直したうえで再レビューせずに完了する
- 完了時、最終報告に「スキップ一覧」（Issue 番号・観点名・引用・指摘の概要）を含める

## エラーハンドリング

- Phase 1 失敗 → Phase 2, 3 を実行しない。`/update-design $ARGUMENTS` で個別実行を案内する
- Phase 2 失敗 → Phase 1 の変更は適用済み。`/doc-review` で個別実行を案内する
- Phase 3 失敗（実行エラー） → Phase 2 のレビュー結果は出力済み。手動での修正を案内する
