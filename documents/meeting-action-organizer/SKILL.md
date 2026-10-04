---
name: meeting-action-organizer
description: Use to organize non-clinical hospital meeting notes into decisions, open issues, owners, due dates, next actions, minutes drafts, and shareable summaries. Do not use for patient-specific conferences, treatment policy meetings, handoffs, clinical judgment, clinical records, patient explanations, or notes containing patient information.
---

# meeting-action-organizer

## Artifact output rule

成果物は原則として議事録 `.docx` とアクション一覧 `.xlsx` で作成する。チャットには会議内容全文を貼らず、保存先、ファイル一覧、重要な未決事項だけを返す。

## Purpose

病院内の非診療領域の会議メモから、決定事項、未決事項、担当者、期限、次回アクションを整理する。

## When to use

- 委員会、部署会議、医局会議、研修会議、業務改善ミーティングのメモを整理したい。
- 総務、医事課、教育担当の定例会からアクションリストを作りたい。
- 議事録ドラフトや共有文が必要。

## When not to use

- 患者個別情報を含むカンファレンス。
- 診療方針に関わる会議。
- 申し送り。
- 医療判断に関わる議事録。

## Inputs

- 会議名、日時、参加者または部署
- 会議メモ、発言要旨、決定内容
- 担当者、期限、次回会議予定
- 共有先、文体、議事録様式

## Process

1. 患者情報や診療判断が含まれないことを確認する。
2. 決定事項、未決事項、確認事項を分ける。
3. 担当者と期限を抽出し、不明な場合は不足情報にする。
4. 次回までのアクションと共有文を作る。
5. 議事録ドラフトを簡潔に整える。

## Output format

- 会議概要
- 決定事項
- 未決事項
- 担当者
- 期限
- 次回までのアクション
- 議事録ドラフト
- 共有文

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「教育委員会メモ: 新人研修の日程を7月に仮決定。資料担当は教育担当。出席確認は各部署へ依頼。」

出力例: 決定事項、未決事項、担当、期限、共有文、議事録ドラフトを出す。

## Escalation / human review notes

公式議事録、院内決裁、労務、医療安全、患者情報に触れる内容は、責任者が確認する。
