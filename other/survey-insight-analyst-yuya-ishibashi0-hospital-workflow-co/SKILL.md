---
name: survey-insight-analyst
description: Use to analyze non-clinical training surveys, staff surveys, workshop questionnaires, free-text comments, satisfaction trends, improvement requests, and next-theme planning in hospital contexts. Do not use with patient information, clinical outcomes, diagnosis, treatment decisions, patient explanations, clinical records, or handoff content.
---

# survey-insight-analyst

## Artifact output rule

成果物は原則として集計表 `.xlsx` と報告書 `.docx` で作成する。チャットには分析全文を貼らず、保存先、主要傾向、確認ポイントだけを返す。

## Purpose

研修アンケート、職員アンケート、勉強会アンケートを分析し、改善示唆を出す。

## When to use

- 研修アンケート、職員アンケート、勉強会アンケートを整理したい。
- 自由記述、満足度、改善要望、次回テーマを分類したい。
- 報告書ドラフトや次回研修への示唆が欲しい。

## When not to use

- 患者情報、診療結果、医療判断に関わるアンケートを扱う場合。
- 個人を特定できる職員情報を含む場合。
- 診断、治療、患者説明、診療記録、申し送りに関わる場合。

## Inputs

- アンケート項目、回答件数、集計表
- 自由記述、満足度、属性カテゴリ
- 研修目的、対象者、次回検討したい観点

## Process

1. 回答データから個人情報がないか確認する。
2. 定量項目と自由記述を分ける。
3. 自由記述を肯定的意見、改善要望、質問、次回テーマに分類する。
4. 全体傾向と部門文脈に合う示唆を整理する。
5. 報告書ドラフトと次回テーマ案を作る。

## Output format

- 全体傾向
- 満足度の傾向
- 自由記述の分類
- ポジティブな意見
- 改善要望
- 次回研修への示唆
- 報告書ドラフト
- 次回テーマ案

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「AI 研修後アンケート 30 件。満足度平均 4.2。自由記述は、演習がよかった、時間が短い、事例がもっと欲しい、など。」

出力例: 全体傾向、分類表、改善要望、次回テーマ案、報告書ドラフトを出す。

## Escalation / human review notes

人事評価、懲戒、個人特定、ハラスメント、労務問題につながる内容は、担当部署に確認する。
