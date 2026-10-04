---
name: hospital-manual-builder
description: Use to create or revise non-clinical hospital manuals, procedures, onboarding guides, committee operations manuals, inventory manuals, training operations manuals, rule books, FAQs, checklists, and revision histories. Do not use for clinical procedures, diagnosis, treatment decisions, patient handoff documents, patient explanations, or patient-specific workflows.
---

# hospital-manual-builder

## Artifact output rule

成果物は原則として `outputs/YYYYMMDD-task-name/` にマニュアル `.docx` と、必要に応じてチェックリスト `.xlsx` で作成する。チャットには本文全体を貼らず、保存先、ファイル一覧、確認ポイントだけを返す。

## Purpose

既存マニュアル、メモ、運用ルール、ヒアリング内容、業務フローなどから、病院内で使えるマニュアルや手順書を作成・改訂する。

## When to use

- 業務マニュアル、新人向け手順書、受付対応マニュアルを作りたい。
- 委員会運営、物品管理、研修運営、部署内ルールを整理したい。
- FAQ、チェックリスト、改訂履歴を含めたい。

## When not to use

- 診療手順、治療方針、患者個別対応、患者説明、診療記録、申し送りを扱う場合。
- 医療安全上、専門職の判断が必要な内容を AI だけで整理する場合。

## Inputs

- 現在の手順、対象者、利用場面
- 既存マニュアル、メモ、ヒアリング内容
- 注意事項、よくあるミス、確認者
- 改訂理由、改訂履歴

## Process

1. 目的、対象者、前提条件を明確にする。
2. 手順を時系列または場面別に整理する。
3. 注意事項、例外、確認先を分ける。
4. FAQ とチェックリストを追加する。
5. 新人向け簡易版と管理者向け確認項目を分ける。

## Output format

- マニュアル構成
- 目的
- 対象者
- 手順
- 注意事項
- よくあるミス
- FAQ
- チェックリスト
- 新人向け簡易版
- 管理者向け確認項目
- 改訂履歴案

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「受付で書類を受け取った後の部署内回付手順を、新人向けマニュアルにしたい。」

出力例: 目的、対象者、手順、注意事項、よくあるミス、チェックリスト、FAQ、改訂履歴案を作る。

## Escalation / human review notes

運用変更、監査、法務、個人情報、医療安全に関わるマニュアルは、責任部署の確認を受ける。
