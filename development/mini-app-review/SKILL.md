---
name: mini-app-review
description: "デプロイ済みアプリの作成者レビューを実施する。「レビュー」「改善」「ブラッシュアップ」を依頼されたときに使用する。"
---

# Mini App Review Workflow

デプロイ済みアプリを作成者視点でレビューし、改善点を洗い出す。主成果物はreview_report.md（レビュー結果・改善提案・優先度付きアクションリスト）。

## Instructions

### 1. Preflight（事前確認）
- ドキュメント精査原則（Preflight必須）：テンプレート確認後、生成前に必ず以下を実施すること。
  - requirements.md、design.mdを読み込み、当初の意図を把握する。
  - 実装コード（index.html, style.css, app.js）を精読する。
  - 公開URLにアクセスして実際の動作を確認する。
  - test_report.md、deploy_log.mdがあれば確認する。
  - これらを完了するまでレビューを開始しない。
- `./assets/review_template.md` を先に読み、レビューレポートの構造を確認する（テンプレートファースト）。
- `./assets/review_checklist.md` でレビュー観点を確認する。

### 2. 生成
- `./questions/review_questions.md` を使ってレビュー方針を確認する。
- 以下の観点でレビューを実施する:
  1. **機能面**: 要件充足度、ユーザビリティ、エッジケース対応
  2. **コード品質**: 可読性、保守性、パフォーマンス、セキュリティ
  3. **デザイン面**: UI/UX、レスポンシブ、アクセシビリティ
  4. **技術的負債**: リファクタリング候補、改善余地
  5. **拡張性**: 将来の機能追加への対応しやすさ
- 改善点を優先度（High/Medium/Low）で分類する。
- 具体的な修正案をコード例とともに提示する。
- review_report.mdを作成する。

### 3. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-mini-app-qc`）に評価・チェックを委譲する。
- Subagentは最初に `./evaluation/evaluation_criteria.md` をReadし、評価指標に基づいてQCを実施する。
- 指摘を最小差分で反映する（テンプレの章立ては崩さない）。
- 再度SubagentでQCする。
- これを最大3回まで繰り返し、確定する。
- 指摘に対し「修正した/しない」と理由を成果物に残す。

### 4. バックログ反映
- review_report.mdを`app/{app_name}/docs/`配下に保存する。
- 改善アクションをユーザーに提示し、対応方針を確認する。
- ユーザーが改善実施を希望した場合、mini-app-buildに連携する。
- review_done=true を記録してから次工程へ進む。
- **status-updater**を呼び出してステータスを更新する。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-mini-app-qc: レビュー観点の網羅性、改善提案の妥当性、優先度の適切性を検査

## Resources
- questions: ./questions/review_questions.md
- assets: ./assets/review_template.md
- assets: ./assets/review_checklist.md
- evaluation: ./evaluation/evaluation_criteria.md
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
