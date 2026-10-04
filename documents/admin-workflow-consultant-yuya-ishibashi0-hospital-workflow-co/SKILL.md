---
name: admin-workflow-consultant
description: Use for improving non-clinical administrative workflows in Japanese hospitals, such as duplicate entry, paper handoffs, Excel tracking, print formatting, and report rework. Do not use for diagnosis, treatment decisions, patient-specific advice, clinical documentation, patient handoffs, patient explanations, EHR integration, or work containing patient personal information.
---

# admin-workflow-consultant

## Artifact output rule

成果物は原則として `outputs/YYYYMMDD-task-name/` に `.docx` または `.xlsx` で作成する。チャットには本文全体を貼らず、保存先、ファイル一覧、確認ポイントだけを返す。

## Purpose

病院内の非診療領域における事務作業・間接業務の無駄を整理し、低リスクで始められる改善案を作る。

## When to use

- 二重入力、多重入力、転記、紙運用を整理したい。
- Excel 管理、印刷フォーマット調整、部署間情報共有に手戻りがある。
- 報告書作成、会議資料作成、委員会資料作成が重複している。
- 上司や関係部署に説明する改善提案文が必要。

## When not to use

- 診断・治療判断、患者個別の医療判断に関わる場合。
- 患者説明文、診療記録、申し送り文を作る場合。
- 患者個人情報や電子カルテ内容を扱う場合。
- 医療安全上、AI 出力をそのまま使う業務。

## Inputs

- 対象部署、業務名、現在の手順
- 使っている紙、Excel、Word、PowerPoint、院内様式
- 関係者、頻度、締切、困りごと
- 既存ルール、変更できない制約

## Process

1. 業務の目的と成果物を確認する。
2. 現状フローを入力、加工、確認、提出、共有に分ける。
3. 二重入力、転記、待ち時間、手戻り、印刷調整を探す。
4. 原因を、様式、ルール、担当、ツール、確認経路に分ける。
5. 小さく試せる改善案と、AI で支援できる部分を分ける。
6. AI を使わない方がよい部分と人間確認点を明記する。

## Output format

- 業務課題の要約
- 現状業務フロー
- 無駄の発生ポイント
- 原因分析
- 改善案
- 低リスクで始められる施策
- AI で支援できる部分
- AI を使わない方がよい部分
- 人間が確認すべき点
- 上司向け提案文

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「研修参加者名簿を紙で回収し、Excel に入力し、別の報告書にも転記している。月 2 回、教育担当が対応している。」

出力例: 転記箇所を表にし、Forms 入力、Excel 集計、報告書様式の共通項目化、試行範囲、上司向け提案文を作る。

## Escalation / human review notes

院内規程、個人情報保護、システム変更、部署間ルール変更が関わる場合は、上司、システム担当、個人情報保護担当に確認する。
