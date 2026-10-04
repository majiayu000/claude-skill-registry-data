---
name: hospital-template-document-builder
description: Use to extract and organize non-clinical information from notes, surveys, minutes, CSV, or source materials into existing Excel, Word, PowerPoint, or hospital templates. Do not invent missing data, add fields not in the template, process patient information, or create clinical records, patient handoffs, or patient explanation documents.
---

# hospital-template-document-builder

## Artifact output rule

成果物は元の様式に合わせて `.xlsx`、`.docx`、`.pptx` の実ファイルとして作成する。既存ファイルが渡された場合は、可能な範囲でそのファイルを複製して編集する。チャットには保存先、不足情報、確認ポイントだけを返す。

## Purpose

資料、メモ、アンケート結果、議事録、CSV などから必要情報を抽出し、既存の Excel / Word / PowerPoint / 院内様式に沿って整理する。

## When to use

- 研修報告書 Excel、出席簿、業務改善提案書、委員会報告書、月次報告書に整理したい。
- チェックリスト、FAQ 一覧表、研修計画表、物品管理表に転記したい。
- 元資料とテンプレートの対応関係を明示したい。

## When not to use

- 患者情報、診療記録、申し送り、患者説明文を扱う場合。
- 不明情報を推測で埋める必要がある場合。
- テンプレート外の項目を勝手に追加したい場合。

## Inputs

- 元資料、テンプレート項目、様式の制約
- 出力したい形式、空欄の扱い
- 必須項目、任意項目、確認者

## Process

1. テンプレート項目を一覧化する。
2. 元資料から対応する情報を抽出する。
3. 不明、不足、矛盾、要確認を分ける。
4. テンプレートにない項目は追加せず、備考で扱うか確認事項にする。
5. Excel、Word、PowerPoint の出力案に整える。

## Output format

- テンプレート項目ごとの対応表
- 抽出した情報
- 不足情報リスト
- 転記ルール
- Excel 表形式の出力案
- Word 報告書の構成案
- PowerPoint 資料構成案
- 人間が確認すべき項目

## Safety constraints

- 不明な情報を勝手に補完しない。
- 空欄は空欄として残す。
- 元資料とテンプレートの対応関係を明示する。
- テンプレートにない項目を勝手に追加しない。
- 提出前に人間が確認する。
- 診断・治療判断、患者個別の医療判断、患者説明文、診療記録、申し送り文には使わない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。

## Examples

入力例: 「研修アンケート集計メモを、研修報告書の項目: 目的、対象、参加人数、満足度、主な意見、次回改善点に整理したい。」

出力例: 各項目への対応表、不足情報、空欄、Word 報告書案、Excel 表案を出す。

## Escalation / human review notes

提出様式、公式報告、監査資料、院外提出資料は、担当者と管理者が最終確認する。
