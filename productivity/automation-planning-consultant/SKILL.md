---
name: automation-planning-consultant
description: Use for planning low-risk workload reduction options for non-clinical hospital administrative work, including Excel, forms, CSV, shared folders, existing system settings, department consultation, and workflow changes. Do not use for clinical decisions, patient data processing, EHR integration, or automation that could directly affect patient safety without human review.
---

# automation-planning-consultant

## Artifact output rule

成果物は原則として `outputs/YYYYMMDD-task-name/` に検討メモ `.docx` と比較表 `.xlsx` で作成する。チャットには本文全体を貼らず、保存先、ファイル一覧、確認ポイントだけを返す。

## Purpose

病院内の事務作業・間接業務について、自動化ありきにせず、省力化や運用改善の選択肢を整理する。

## When to use

- Excel 関数、Excel マクロ、Google Forms / Microsoft Forms、CSV 運用を比較したい。
- 共有フォルダ、既存システムの設定変更、関係部署への相談の論点を整理したい。
- ツール導入前に、業務フロー変更だけで改善できるか見たい。

## When not to use

- 診断・治療判断、患者個別の医療判断に関わる場合。
- 患者情報、電子カルテ内容、診療記録、申し送りを扱う場合。
- 自動化の失敗が医療安全に直接影響する場合。

## Inputs

- 業務内容、頻度、件数、所要時間
- 使用ツール、ファイル形式、転記元と転記先
- エラー例、確認者、承認経路
- 変更可能な範囲、予算、システム担当の有無

## Process

1. 作業を収集、確認、加工、転記、通知、保管に分ける。
2. 定型性、例外の多さ、ミスの影響、個人情報有無を確認する。
3. Excel、Forms、CSV、共有フォルダ、既存システム設定、業務フロー変更を比較する。
4. 自動化しない方がよい作業を分ける。
5. 小さく試す案と確認事項を作る。
6. システム担当者や関係部署への相談文を作る。

## Output format

- 自動化できそうな作業
- 自動化しない方がよい作業
- 改善手段の選択肢
- 難易度
- リスク
- 必要な確認事項
- 小さく試す案
- システム担当者への相談文
- 関係部署へ確認すべきこと

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「研修申込者をメール本文から Excel に転記している。月 100 件程度。部署名、氏名、参加希望日を集計する。」

出力例: Forms 化、CSV 出力、Excel 集計、メール運用継続時のチェック表、小さく試す案、システム担当への相談文を出す。

## Escalation / human review notes

システム設定変更、外部サービス利用、外部送信、権限変更は、システム担当と管理者に確認する。
