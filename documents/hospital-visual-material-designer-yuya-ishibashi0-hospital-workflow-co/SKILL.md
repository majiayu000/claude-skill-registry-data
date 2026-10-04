---
name: hospital-visual-material-designer
description: Use to design non-clinical hospital posters, training flyers, slide outlines, diagrams, PowerPoint or Canva layouts, and optional image generation prompts. Do not require image generation, do not create patient-facing explanation materials, and do not handle diagnosis, treatment, clinical records, handoffs, or patient personal information.
---

# hospital-visual-material-designer

## Artifact output rule

成果物は原則として `.pptx` または `.docx` の実ファイルとして作成する。画像生成が使えない場合も、構成案だけをチャットに返さず、編集可能な資料ファイルを作る。

## Purpose

病院内の非診療領域における掲示物、研修資料、スライド、図解、画像生成プロンプトを設計する。

## When to use

- 院内掲示物、研修案内チラシ、勉強会スライドを作りたい。
- 業務変更の説明資料、新人教育資料、図解、ポスターが必要。
- Canva / PowerPoint / Google スライド / Word で再現できる構成案が必要。
- 画像生成が使える環境で、画像生成プロンプトも欲しい。

## When not to use

- 患者説明文や患者向け医療説明資料を作る場合。
- 診断、治療、診療記録、申し送りに関わる資料。
- 実患者情報や実在職員名を含む資料。

## Inputs

- 目的、読み手、掲示場所、サイズ
- 必須文言、開催日時、申込方法
- 雰囲気、使用ツール、印刷条件
- 画像生成の可否

## Process

1. 読み手と行動目標を整理する。
2. A4 掲示物、スライド、図解のどれが適切か選ぶ。
3. 文面を短くし、見出し、本文、行動指示、問い合わせ先に分ける。
4. 画像生成が使える場合はプロンプトを出す。
5. 画像生成が使えない場合は PowerPoint、Canva、Google スライド、Word での代替手順を出す。

## Output format

- 資料の目的整理
- 読み手
- 文面
- A4 掲示物レイアウト案
- スライド構成
- 図解案
- 画像生成用プロンプト
- 画像生成が使えない場合の代替作成手順
- 印刷・掲示時の注意点

## Safety constraints

- 画像生成そのものを必須にしない。
- 診断・治療判断に使わない。
- 患者個別の医療判断に使わない。
- 患者説明文を作らない。
- 診療記録や申し送り文を作らない。
- 患者個人情報を入力しない。
- 院内規程・所属組織のルールを優先する。
- AI 出力はたたき台であり、人間が確認する。

## Examples

入力例: 「職員向け AI 勉強会の A4 ポスターと 10 枚スライド構成を作りたい。」

出力例: ポスター文面、レイアウト、スライド構成、画像生成プロンプト、PowerPoint での代替作成手順を出す。

## Escalation / human review notes

院外掲示、広報、採用、患者向け公開物は、広報担当、管理者、関係部署の確認を受ける。
