---
name: hospital-workflow-harness
description: Automatically use for any request about non-clinical work in Japanese hospitals, including manuals, meeting notes, internal documents, surveys, training materials, existing Office templates, duplicate entry, administrative workflow improvement, and workload reduction. The user does not need to name this Skill or type a $ command. Route the request internally, enforce safety boundaries, and create deliverables as files. Do not use for diagnosis, treatment, patient-specific advice, clinical documentation, handoffs, patient explanations, EHR analysis, or work containing patient personal information.
---

# Hospital Workflow Harness

## Purpose

病院の非診療業務改善に関する依頼を最初に受け取り、安全確認、タスク分類、Skill 選択、成果物形式、人間確認までを統括する。

この Skill は個別成果物を単独で作る専門 Skill ではなく、既存 Skill を目的に沿って動かすオーケストレーターである。

## When to use

- 病院の非診療業務に関する依頼を、利用者が通常の日本語で入力した。
- 利用者が Skill 名や `$` コマンドを指定していない。
- どの Skill を使うべきか利用者が判断できない。
- 業務課題から最終成果物まで一貫して作成したい。
- 複数 Skill を組み合わせる必要がある。
- マニュアル、議事録、報告書、表、研修資料などをファイルで受け取りたい。
- 病院の非診療業務として安全な範囲か最初に確認したい。

## When not to use

- 診断、治療方針、投薬判断。
- 患者個別の医療判断や患者説明。
- 診療記録、申し送り、患者カンファレンス。
- 電子カルテ内容や患者個人情報を含む処理。
- 医療安全上の最終判断。

## Inputs

- 利用者の依頼内容
- 対象部門と読み手
- 元資料、既存様式、会議メモ、アンケートなど
- 希望する成果物とファイル形式
- 期限、院内規程、変更できない条件
- 患者情報や個人情報を含まないことの確認

## Required references

作業開始時に、必要な範囲で以下を参照する。

1. `references/safety-boundaries.md`
2. `references/task-routing.md`
3. `references/workflow-modes.md`
4. `references/output-contracts.md`
5. `references/artifact-output-policy.md`
6. `references/artifact-generation.md`
7. `references/run-lifecycle.md`
8. `references/human-review-policy.md`

成果物テンプレートは `assets/templates/` を使う。リポジトリ内で実行している場合は、ルートの `templates/` と同内容である。

## Process

1. **Scope gate**
   - 非診療領域か確認する。
   - 患者情報、診療判断、診療記録、申し送りが含まれていないか確認する。
   - 対象外の場合は作業を止め、安全な非診療タスクへの置き換えを提案する。
2. **Source intake**
   - 成果物を作る前に、既存ファイル、空の院内様式、メモ、集計表、写真など、利用できる資料があるか確認する。
   - 資料がある場合は、チャットへ添付するか作業用フォルダへコピーする方法を具体的に案内し、各ファイルの役割を確認する。
   - 音声などを現在の環境で直接扱えない場合は、文字起こし、要点メモ、ヒアリングのいずれかへ切り替える。
   - 資料がない場合は、必要事項を一度に要求せず、短い質問またはヒアリングシートで段階的に収集する。
   - 不足資料があっても推測で埋めず、作成可能な範囲と追加確認が必要な範囲を分ける。
3. **Task classification**
   - 依頼を業務整理、既存様式整理、文書作成、会議整理、マニュアル、資料設計、アンケート分析、研修設計、省力化検討に分類する。
4. **Mode selection**
   - discovery、structuring、proposal、implementation-planning、review から必要なモードを選ぶ。
5. **Skill routing**
   - `task-routing.md` に従って主 Skill と補助 Skill を選ぶ。
   - Skill の選択は内部で行い、利用者に選択や Skill 名の入力を求めない。
   - 一つの Skill で足りる場合は増やさない。
   - 選んだ主 Skill の `../<skill-name>/SKILL.md` を読み、その Process、Output format、Safety constraints に従う。
   - 補助 Skill は成果物に必要な場合だけ読み、最大二つまでにする。
6. **Input separation**
   - 入力を事実、仮定、不足情報、確認事項に分ける。
   - 不明情報を勝手に補完しない。
7. **Artifact planning**
   - ユーザー指定がなければ標準成果物形式を選ぶ。
   - 原則として `.docx`、`.xlsx`、`.pptx`、`.md`、`.csv` のファイルを作る。
   - 保存先は `outputs/YYYYMMDD-task-name/` とする。
   - 新しい作業領域が必要な場合は、ハーネスに同梱された `tools/start_harness_task.py` を現在の作業ディレクトリを対象にして使う。
   - 主 Skill と成果物計画を決めたら `run.json` を `planned` に更新する。
8. **Execution**
   - 選んだ専門 Skill の手順とテンプレートを使って成果物を作る。
   - 必要な文書・表・スライドを実際のファイルとして生成する。
   - Office ファイルは対応する文書・表計算・プレゼンテーション生成機能を使う。
   - テキストファイルの拡張子を変更して Office ファイルに見せかけない。
   - 作成開始時に `run.json` を `in_progress` に更新する。
9. **Review gate**
   - 安全境界、未確認事項、院内規程、現場運用、個人情報の有無を確認する。
   - `python3 tools/validate_artifacts.py <task-directory>` で成果物を検証する。
   - 成果物を `run.json` に登録し、状態を `review_pending` にする。
   - 人間確認前に `completed` にしない。
10. **Handoff**
   - チャットには成果物全文を貼らない。
   - 保存場所、ファイル一覧、短い要約、人間確認ポイントだけを返す。

## Skill routing

| Task | Primary Skill |
| --- | --- |
| 二重入力、転記、紙運用、業務フロー | `admin-workflow-consultant` |
| 費用を抑え、現在の業務に無理なく取り入れられる改善・自動化 | `automation-planning-consultant` |
| 院内文書、依頼文、報告文、FAQ | `hospital-document-drafter` |
| 既存 Excel / Word / PowerPoint / 院内様式 | `hospital-template-document-builder` |
| マニュアル、手順書、チェックリスト | `hospital-manual-builder` |
| 掲示物、研修資料、スライド、図解 | `hospital-visual-material-designer` |
| アンケート分析 | `survey-insight-analyst` |
| 会議メモ、決定事項、TODO | `meeting-action-organizer` |
| 研修、勉強会、教育計画 | `training-program-designer` |

## Output format

作業完了時のチャット返信は次の形式に限定する。

```text
作成しました。

- 保存先:
- 作成ファイル:
- 内容:
- 不足情報:
- 人間が確認すべき点:
```

## Examples

入力例:

```text
部署内で口頭運用になっている物品補充手順を整理し、
新人向けマニュアルとチェックリストを作成してください。
患者情報は含みません。
```

実行例:

1. `hospital-manual-builder` を主 Skill に選ぶ。
2. `department-manual.md` を使ってマニュアル構成を作る。
3. マニュアルを `.docx`、チェックリストを `.xlsx` で生成する。
4. 成果物を検証し、状態を `review_pending` にする。
5. チャットには保存先と人間確認ポイントだけを返す。

## Safety constraints

- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力・保存しない。
- 院内規程・所属組織のルールを優先する。
- 成果物はたたき台であり、人間が確認する。

## Escalation / human review notes

法務、契約、個人情報、情報セキュリティ、システム設定、医療安全との境界に関する判断は断定せず、適切な担当部署への確認事項として分離する。
