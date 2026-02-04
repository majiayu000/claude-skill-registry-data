---
name: deckrd-coder
description: An agent that codes tasks in BDD-style. Automatically does not commit.
allowed-tools: Task, Bash, Read, Grep, Glob
license: MIT
meta:
  author: atsushifx
  version: 0.0.3
---

<!-- textlint-disable ja-technical-writing/no-exclamation-question-mark -->

# /deckrd-coder スキル - Deckrd タスク実装ガイド

**このスキルは、Deckrd セッションで定義されたタスクを BDD 厳格プロセスに従って実装します。**

---

## ⚠️ 重要事項

### コミット除外

このスキルは **実装まで行いますが、コミットはしません**。実装後のコミットはユーザーが手動で実施してください。

```bash
(NG) git add .
(NG) git commit -m "..."
(NG) /idd-pr  # PR 生成も禁止
```

### テスト・品質ゲート必須

- 実装終了時点で、すべてのテストが PASS
- Lint・型チェック・その他の品質ゲートが合格

---

## 概要

### What (何をするのか)

Deckrd セッションで定義されたタスクを、**BDD (Behavior-Driven Development) の厳格プロセス** に従って実装します。
**1つのスキル呼び出し = 1つのタスク実装** という原則を厳守します。

### Why (なぜこの方法を使うのか)

- 品質保証: Red-Green-Refactor サイクルで高品質なコードを実現
- 追跡可能性: 各ステップが記録され、何をいつなぜ実装したかが明確
- トークン効率化: プロジェクトメモリ & serena-mcp により不要な説明を削減

### How (どのように実装するのか)

8 つのステップ (Step 1～8) で構成される実装フロー:

1. **Step 1**: 品質ゲート用コマンド取得
2. **Step 2**: 実装タスクリスト取得
3. **Step 3-4**: BDD サイクル (Red-Green-Refactor)
4. **Step 5**: 品質ゲート実行 (全体検証)
5. **Step 6**: 進捗記録
6. **Step 7**: Refactor フェーズ (全体コード整理)
7. **Step 8**: 完了判定

詳細は [IMPLEMENTATION.md](./references/implementation.md) を参照。

---

## 基本的な使い方

### コマンド形式

```bash
# 単一タスク実装 (推奨)
/deckrd-coder T01-02
```

> 注意
>
> オプションは現在のところ実装していません。

### Task ID 指定形式

| ID 形式       | 例          | 説明                              |
| ------------- | ----------- | --------------------------------- |
| セクション ID | `T01-02`    | **推奨** (単一テストケース対応)   |
| 詳細 ID       | `T01-02-01` | **非推奨** (テストケース詳細指定) |

> 注意
>
> 複数タスク指定は非推奨 (1 message = 1 task の原則)

詳細な使用方法とよくある質問は [FAQ.md](./references/faq.md) を参照。

---

## 全体的な戦略

### 6 つの Phase で構成

```bash
Phase 0: 開発環境の初期化
    ↓
Phase 1: deckrd セッション・タスク情報の取得
    ↓
Phase 2: 実装タスクリスト (細分化) の作成
    ↓
Phase 3: Red-Green-Refactor による実装
    ↓
Phase 4: 品質ゲート (Lint・型チェック・テスト) の実行
    ↓
Phase 5: 完了確認
```

### 各 Phase の概要

| Phase | 役割         | 詳細                                         |
| ----- | ------------ | -------------------------------------------- |
| 0     | 開発環境確認 | Node.js、npm、テストフレームワークなどの確認 |
| 1     | 情報取得     | セッション・タスク定義から実装内容を抽出     |
| 2     | タスク細分化 | 実装タスクを小さなステップに分割             |
| 3     | BDD 実装     | Red-Green-Refactor サイクルで実装            |
| 4     | 品質ゲート   | Lint・型チェック・テスト実行                 |
| 5     | 完了確認     | すべての条件が満たされたか確認               |

詳細は [WORKFLOW.md](./references/workflow.md) を参照してください。

---

## リファレンス

### 参照ドキュメント一覧

このスキルは以下のドキュメントを厳密に参照・遵守します。

#### 1. [WORKFLOW.md](./references/workflow.md)

**対象**: Phase 0～5 の全体フロー
**用途**: スキル実行前に全体を理解したいとき。

#### 2. [IMPLEMENTATION.md](./references/implementation.md)

**対象**: Step 1～8 の詳細手順
**用途**: 実装中に困ったとき、エラーが発生したとき。

**主要な原則**:

- 1 message = 1 test: 複数タスクは実装しない
- Step 順序の厳密性: ステップをスキップしない
- 最小実装の遵守: Green フェーズは過剰実装を禁止
- 品質ゲート必須: Step 5 は必ず実行、失敗時は 3 回まで対応

#### 3. [TROUBLESHOOTING.md](./references/troubleshooting.md)

**対象**: WORKFLOW・IMPLEMENTATION から逸脱した場合の対応
**用途**: エラー発生時、フロー判定に迷ったとき。

#### 4. [FAQ.md](./references/faq.md)

**対象**: よくある質問と回答
**用途**: 実装方法の詳細、Q&A 確認。

---

### 内部エージェント: bdd-coder

**位置**: `plugins/deckrd-coder/agents/bdd-coder.md`

**役割**: このスキルの **Step 3** で自動起動され、以下を担当:

- Red フェーズ: テスト実装 → テスト失敗確認
- Green フェーズ: 最小実装 → テスト合格確認
- Refactor フェーズ: 軽微な整理 (ユーザー相談なし)
- 品質ゲート確認: Lint・型チェック合格確認

詳細は `plugins/deckrd-coder/agents/bdd-coder.md` を参照。

---

## トークン効率化メカニズム

### 1. プロジェクトメモリ活用

スキル実行時に以下のメモリを自動参照:

- `code_style_and_conventions`: コーディング規約
- `project_overview`: プロジェクト概要
- `project_structure`: プロジェクト構成
- `suggested_commands`: 実行コマンド

### 2. serena-mcp による高速検索

- シンボル検索、型情報取得を効率化
- 不要なファイル全文読み込みを削減

### 3. bdd-coder エージェント

- 親スキルは高レベル指示のみ
- bdd-coder が TodoWrite で詳細な進捗管理
- コンテキスト分割によるメモリ削減

---

## 変更履歴

<!-- textlint-disable -->

- v0.0.1: 初版
- v0.0.2: workflow.md, implementation.md, troubleshooting.md, bdd-coder.md への参照を明示し、ユーザーおよびエージェント AI 向けの包括的ガイドに改定
