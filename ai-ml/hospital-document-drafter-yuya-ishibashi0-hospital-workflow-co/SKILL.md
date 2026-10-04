---
name: hospital-document-drafter
description: Use to draft non-clinical internal hospital documents, announcements, requests, reports, FAQs, training invitations, survey requests, committee notices, manager proposals, and staff-facing explanations. Do not use for patient explanation documents, clinical records, handoff notes, diagnosis, treatment, or patient-specific medical content.
---

# hospital-document-drafter

## Artifact output rule

成果物は原則として `outputs/YYYYMMDD-task-name/` に `.docx` で作成する。チャットには文書全文を貼らず、保存先、ファイル名、確認ポイントだけを返す。

## Purpose

病院内の非診療文書、依頼文、報告文、FAQ、共有文を作成する。

## When to use

- 院内お知らせ、部署内共有文、依頼文、報告文を作りたい。
- FAQ、研修案内文、アンケート依頼文、委員会からの周知文が必要。
- 上司向け改善提案文、スタッフ向け説明文を整えたい。

## When not to use

- 患者説明文、診療記録、申し送り文を作る場合。
- 診断や治療に関わる文書。
- 患者個人情報を含む文書。

## Inputs

- 文書の目的、読み手、配布方法
- 伝えたい内容、締切、依頼事項
- 文体、長さ、院内ルール
- 必須文言、問い合わせ先

## Process

1. 読み手と目的を確認する。
2. 必須情報、不明情報、注意書きを分ける。
3. 簡潔で誤解の少ない構成にする。
4. 院内規程や確認者が必要な箇所を明記する。
5. 件名、本文、補足、問い合わせ先を整える。

## Output format

- 件名
- 宛先
- 本文
- 依頼事項
- 締切
- 問い合わせ先
- 確認が必要な点
- 短縮版または掲示版

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「来月の AI リテラシー研修の参加依頼文を、全職員向けに作りたい。申込締切は架空の日付でよい。」

出力例: 件名、案内本文、申込方法、締切、問い合わせ先、掲示用短縮文を作る。

## Escalation / human review notes

院外公開、採用、労務、法務、個人情報、医療安全に関わる文書は担当部署の確認を受ける。
