---
name: training-program-designer
description: Use to design non-clinical training programs for healthcare workers, including AI literacy, onboarding, department workshops, management training, DX staff training, student education, and role-specific sessions. Do not use for treatment education for individual patients, diagnosis, treatment decisions, clinical documentation, handoffs, or patient-specific medical advice.
---

# training-program-designer

## Artifact output rule

成果物は原則として研修企画書 `.docx`、研修資料 `.pptx`、アンケート案 `.docx` の実ファイルとして作成する。チャットには保存先、ファイル一覧、確認ポイントだけを返す。

## Purpose

医療従事者向けの研修、勉強会、AI リテラシー研修、新人研修、管理職研修を設計する。

## When to use

- AI リテラシー研修、新人研修、部署内勉強会を設計したい。
- 管理職向け研修、DX 担当者向け研修、医療系学生向け研修、職種別研修が必要。
- 60分、90分、120分の構成、演習、アンケート、講師台本を作りたい。

## When not to use

- 患者個別の治療説明、診断、治療判断に関わる教育。
- 診療記録、申し送り、患者説明文の作成。
- 患者情報を含む事例検討。

## Inputs

- 研修テーマ、対象者、人数、時間
- 到達目標、前提知識、会場またはオンライン
- 演習可否、配布資料、アンケート項目
- 院内ルール、講師、事後フォロー

## Process

1. 対象者と到達目標を明確にする。
2. 60分、90分、120分の構成に分ける。
3. 講義、演習、共有、質疑、まとめの時間配分を作る。
4. 配布資料案、アンケート、講師用台本を作る。
5. 事後フォローと次回改善につなげる。

## Output format

- 研修目的
- 対象者
- 60分構成
- 90分構成
- 120分構成
- 演習内容
- 配布資料案
- アンケート設計
- 講師用進行台本
- 事後フォロー案

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「全職員向け AI リテラシー研修を 90 分で設計したい。個人情報を入力しないことを重視したい。」

出力例: 研修目的、90分構成、演習、配布資料案、アンケート、講師台本、事後フォローを出す。

## Escalation / human review notes

医療安全、個人情報、労務、法務、院外公開に関わる研修は、担当部署の確認を受ける。
