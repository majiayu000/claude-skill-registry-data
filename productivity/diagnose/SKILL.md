---
name: diagnose
description: 複雑なバグの並列仮説調査。Subagent/Agent Teams両モード対応。「原因調査」「investigate」「diagnose」で起動。
allowed-tools: Task, Read, Bash, Grep, Glob
---

# TDD Diagnose Phase

複雑なバグに対し、複数の仮説を並行調査し根本原因を特定する。

## Progress Checklist

```
DIAGNOSE Progress:
- [ ] バグ情報収集（カテゴリ・重要度・症状）
- [ ] 仮説生成（3つ以上）
- [ ] 調査実行（モード自動選択）
- [ ] 結果統合・分岐判定
- [ ] Cycle doc更新 → 完了メッセージ表示
```

## Workflow

### Step 1: バグ情報収集

**1a.** AskUserQuestion で構造化入力:
- バグカテゴリ: regression / new behavior / intermittent / performance degradation
- 重要度: blocking development / blocking users / workaround exists

**1b.** 続けて自然言語で質問:
- 「エラーメッセージやログを貼り付けてください」
- 「関連するファイルパスがあれば教えてください」

詳細: [reference.md](reference.md#バグ情報収集)

### Step 2: 仮説生成

収集した情報から原因候補を **3つ以上** リスト:

| # | 仮説 | 調査方針 |
|---|------|---------|
| H1 | [原因候補1] | [検証方法] |
| H2 | [原因候補2] | [検証方法] |
| H3 | [原因候補3] | [検証方法] |

仮説テンプレート: [reference.md](reference.md#仮説テンプレート)

### Step 3: 調査実行

`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 環境変数でモードを選択:

| 環境変数 | モード | 手順 |
|----------|--------|------|
| 有効 (`1`) | 討論型 (Agent Teams) | [steps-teams.md](steps-teams.md) |
| 無効 / 未設定 | 並行型 (Subagent) | [steps-subagent.md](steps-subagent.md) |

### Step 4: 調査結果統合

各仮説の検証結果を集約し、分岐判定:

#### 根本原因が特定された場合 (Identified)
→ Cycle doc に根本原因を記録、Step 5 へ

#### 2-3候補に絞込まれた場合 (Narrowed)
→ AskUserQuestion で候補からユーザーが選択、Step 5 へ

#### 不明・全仮説否定の場合 (Inconclusive)
```
調査結果が不明確です。
1. 仮説を追加して再調査（最大2回まで）
2. 手動調査へエスカレート（現時点の発見事項を記録）
```

再調査2回で未解決の場合、選択肢2へ強制遷移。

### Step 5: Cycle doc 更新 → 完了

調査結果を Cycle doc に記録。

```
================================================================================
DIAGNOSE完了
================================================================================
根本原因を特定し、Cycle docに記録しました。

次のステップ:
- Orchestrate使用時: 自動的にsync-planが実行されます
- 手動実行時: /spec でTDDコンテキスト設定を開始してください
================================================================================
```

## Reference

- 詳細: [reference.md](reference.md)
