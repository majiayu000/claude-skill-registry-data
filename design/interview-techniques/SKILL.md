---
name: interview-techniques
description: |
  ユーザーインタビュー、要件ヒアリング、ステークホルダー聞き取り時に使用するスキル。
  オープンエンド質問、要求の深掘り、前提の明確化を通じて、ユーザーの真のニーズを引き出します。

  Anchors:
  • Interviewing Users (Steve Portigal) / 適用: インタビュー設計と実施 / 目的: バイアスを避け深い洞察を得る
  • Just Enough Research (Erika Hall) / 適用: 実践的なヒアリング / 目的: 限られた時間で最大の洞察を得る
  • Software Requirements (Karl Wiegers) / 適用: 要件分析と構造化 / 目的: 曖昧さを排除し完全性を確保
  • The Mom Test (Rob Fitzpatrick) / 適用: 過去の具体的行動の質問 / 目的: 仮定的な話を避け真の課題を発見

  Trigger:
  Use when conducting user interviews, requirements gathering, stakeholder hearing.
  Open-ended question design, ambiguous requirement clarification, hidden needs discovery, 5Why analysis.
allowed-tools:
  - Grep
  - Read
  - Edit
  - mcp__claude-in-chrome__find
  - mcp__claude-in-chrome__read_page
references:
  - book: "The Pragmatic Programmer"
    author: "Andrew Hunt, David Thomas"
    concepts:
      - "実践的改善"
      - "品質維持"
---

# Interview Techniques（インタビューテクニック）

## 概要

要求抽出のためのヒアリングスキル。オープンエンド質問、要求の深掘り、前提の明確化を通じて、ユーザーの真のニーズを引き出すための体系的アプローチです。

このスキルは以下の場面で活用できます:

- ユーザー要件のヒアリング
- ステークホルダーからのニーズ抽出
- 曖昧な要求の明確化
- 隠れたニーズや潜在ニーズの発見

詳細な手順や背景は `references/Level1_basics.md`（基礎）から `references/Level4_expert.md`（専門）の段階別ガイドを参照してください。

## ワークフロー

### Phase 1: インタビュー準備と前提整理

**目的**: インタビューの目的、対象者、質問項目を明確にする

**詳細アクション**:

1. **現状確認**: `references/Level1_basics.md` でインタビューの基本概念を確認
2. **目的設定**: 何を知りたいのか（要件、ニーズ、痛点など）を定義
3. **対象者分析**: 誰にどのような形式でヒアリングするかを決定
4. **質問設計**: `references/question-types.md` で質問タイプを選択
5. **準備ツール**: `scripts/prepare-interview.mjs` で質問セットを自動生成

**出力例**: ヒアリング計画書、質問リスト、準備チェックリスト

### Phase 2: インタビュー実施と深掘り

**目的**: 実際のインタビューを実施し、深い洞察を得る

**詳細アクション**:

1. **フロー開始**: `assets/interview-guide.md` でインタビューフローを確認
2. **初期質問**: オープンエンド質問から始めて、相手の背景を理解
3. **深掘り**: `references/why-analysis.md` で5Why分析を実施
4. **仮説検証**: `references/question-types.md` の検証質問で確認
5. **メモ記録**: 重要な発言や着眼点をリアルタイムで記録

**出力例**: インタビュー記録、重要ポイント抽出、初期分析メモ

### Phase 3: 分析・整理と検証

**目的**: ヒアリング結果を分析・整理し、隠れた要件を構造化する

**詳細アクション**:

1. **要件整理**: `references/5w1h-framework.md` でWhy/Who/What/When/Where/Howに分類
2. **ニーズ抽出**: 表面的な要求から潜在ニーズを抽出
3. **優先順位付け**: ステークホルダーのニーズを評価・優先付け
4. **検証実施**: `scripts/validate-skill.mjs` で抽出内容の完全性を確認
5. **記録保存**: `scripts/log_usage.mjs` でインタビュー記録とラーニングを保存

**出力例**: 要件一覧、ニーズマップ、優先度表、実施レポート

## Task仕様ナビ

このスキルで対応できるタスク一覧:

| Task ID | タスク名                   | 説明                                       | 参照リソース           | 使用スクリプト        |
| ------- | -------------------------- | ------------------------------------------ | ---------------------- | --------------------- |
| INT-001 | 初期ヒアリング計画         | インタビューの目的・対象者・方法を定義     | Level1_basics.md       | prepare-interview.mjs |
| INT-002 | オープンエンド質問設計     | 相手を誘導しない質問の構成                 | question-types.md      | prepare-interview.mjs |
| INT-003 | 深掘り分析実施             | 5Why分析による根本ニーズ発見               | why-analysis.md        | -                     |
| INT-004 | 仮説検証インタビュー       | 仮説を検証する質問設計                     | question-types.md      | prepare-interview.mjs |
| INT-005 | 5W1Hフレームワーク適用     | 要件を網羅的に整理                         | 5w1h-framework.md      | -                     |
| INT-006 | ステークホルダーヒアリング | 複数利害関係者の要望を集約                 | Level2_intermediate.md | prepare-interview.mjs |
| INT-007 | 要件の曖昧さ解消           | 曖昧な要求を具体化・明確化                 | Level2_intermediate.md | -                     |
| INT-008 | インタビュー記録分析       | ヒアリング結果から洞察を抽出               | Level3_advanced.md     | log_usage.mjs         |
| INT-009 | ニーズ・ウォント区別       | 真のニーズと一時的な要望を区別             | Level3_advanced.md     | -                     |
| INT-010 | ペルソナ構築               | インタビュー結果からユーザーペルソナを作成 | Level4_expert.md       | -                     |

## ベストプラクティス

### すべきこと (Do)

- **ユーザーから要望をヒアリングする時**: オープンエンド質問で相手の自由な表現を促す
- **曖昧な要求を明確化する時**: 具体例や理由を深掘りして背景を理解する
- **隠れたニーズを発見する時**: 5Why分析で根本原因をたどる
- **ステークホルダーの優先順位を確認する時**: 複数の視点から優先度を検証
- **インタビュー前に**: `prepare-interview.mjs` で質問セットを準備
- **インタビュー中に**: アクティブリスニングで相手の真意を引き出す
- **インタビュー後に**: `log_usage.mjs` で記録を保存し、経験値を蓄積

### 避けるべきこと (Don't)

- 誘導的な質問（yes/no質問が先行）を避ける → 相手の回答が限定される
- インタビューの目的を明確にせずに開始することを避ける → 的外れなヒアリングになる
- アンチパターンや注意点を確認せずに進めることを避ける
- メモを取らない → 重要なニュアンスを見落とす
- 相手の発言を遮断する → 本当の要望が出てこない
- 自分の仮説を押し付ける → バイアスがかかる
- インタビュー結果を記録しない → 次のインタビューに活かせない

## リソース参照

### 学習資料 (references/)

| ファイル                            | 対象レベル | 内容                                                                        |
| ----------------------------------- | ---------- | --------------------------------------------------------------------------- |
| `references/Level1_basics.md`       | 初心者     | インタビューの基本概念、基本的な質問タイプ、はじめる心得                    |
| `references/Level2_intermediate.md` | 実務者     | 実務的なインタビュー設計、ステークホルダー管理、記録方法                    |
| `references/Level3_advanced.md`     | 上級者     | 複雑なニーズ分析、複数ステークホルダーの調整、仮説検証                      |
| `references/Level4_expert.md`       | 専門家     | ペルソナ構築、カスタマージャーニーマップ、組織的ヒアリング戦略              |
| `references/5w1h-framework.md`      | 全レベル   | Why/Who/What/When/Where/Howの構造化フレームワーク                           |
| `references/question-types.md`      | 全レベル   | 7種類の質問タイプ（オープン/クローズド/深堀り/仮説検証/シナリオ/比較/反転） |
| `references/why-analysis.md`        | 全レベル   | 5回のWhy繰り返しによる根本ニーズ発見手法                                    |
| `references/legacy-skill.md`        | 参考       | 旧SKILL.mdの全文（履歴参照用）                                              |

### 実行ツール (scripts/)

| スクリプト                      | 目的           | 用途例                                                 |
| ------------------------------- | -------------- | ------------------------------------------------------ |
| `scripts/prepare-interview.mjs` | ヒアリング準備 | インタビュー前の質問セット自動生成、チェックリスト生成 |
| `scripts/log_usage.mjs`         | 使用記録・評価 | インタビュー結果の記録、学習成果の追跡                 |
| `scripts/validate-skill.mjs`    | 構造検証       | スキルの構造完全性確認、リソース整合性確認             |

### テンプレート (assets/)

| テンプレート                | 用途                                             |
| --------------------------- | ------------------------------------------------ |
| `assets/interview-guide.md` | インタビュー実施ガイド、フロー制御、質問順序管理 |

### コマンドリファレンス

```bash
# リソース確認
cat .claude/skills/interview-techniques/references/Level1_basics.md
cat .claude/skills/interview-techniques/references/Level2_intermediate.md
cat .claude/skills/interview-techniques/references/question-types.md
cat .claude/skills/interview-techniques/references/5w1h-framework.md
cat .claude/skills/interview-techniques/references/why-analysis.md

# インタビュー準備
node .claude/skills/interview-techniques/scripts/prepare-interview.mjs --help
node .claude/skills/interview-techniques/scripts/prepare-interview.mjs --generate

# テンプレート参照
cat .claude/skills/interview-techniques/assets/interview-guide.md

# 検証・記録
node .claude/skills/interview-techniques/scripts/validate-skill.mjs
node .claude/skills/interview-techniques/scripts/log_usage.mjs --record "Interview with User A"
```

## 変更履歴

| Version | Date       | Changes                                                                                                                                |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠（YAML frontmatter拡張、Anchors・Trigger追加、Task仕様ナビ追加、ワークフロー詳細化、ベストプラクティス充実） |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                                                                                            |
