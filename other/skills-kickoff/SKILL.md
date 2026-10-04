---
name: kickoff
description: plan modeで承認されたplanファイルからCycle docを生成する。plan approve後にPost-Approve Actionで自動実行される。手動起動も可:「kickoff」「キックオフ」。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

## Progress Checklist

```
KICKOFF Progress:
- [ ] planファイル読み取り → 情報抽出
- [ ] Cycle doc生成（テンプレートから）
- [ ] Test List・設計情報の転記
- [ ] 完了メッセージ表示
```

## 禁止事項

- planファイルの内容を変更しない（読み取りのみ）
- 実装コード作成（GREENで行う）
- テストコード作成（REDで行う）

## Workflow

### Step 1: Read Plan File

plan modeで作成・承認されたplanファイルを読み取り、以下の情報を抽出:

- **TDD Context**: feature name, environment, scope, risk
- **探索結果**: 既存パターン、影響範囲
- **設計方針**: アーキテクチャ、依存関係
- **Test List**: 正常系/境界値/エッジケース/異常系
- **QAチェック結果**: カバレッジ・粒度・セキュリティ・独立性

### Step 2: Generate Cycle Doc

Feature nameからファイル名を生成し、[templates/cycle.md](../spec/templates/cycle.md) からCycle docを作成。

```bash
mkdir -p docs/cycles && NOW=$(date '+%Y-%m-%d %H:%M')
```

`$NOW` をfrontmatter (`created`/`updated`) とProgress Logに使用。Claude Codeは時刻を持たないため `date` 実行が必須。

planファイルから以下をCycle docに転記:

| Cycle doc セクション | planファイルからの転記元 |
|---------------------|----------------------|
| Scope Definition | In Scope / Out of Scope / Files to Change |
| Environment | Layer, Plugin, Risk, Runtime, Dependencies |
| Risk Interview | BLOCK時のインタビュー回答 |
| Context & Dependencies | 依存関係・参照ドキュメント |
| Implementation Notes | Goal, Background, Design Approach |

### Step 3: Transfer Test List

planファイルのTest ListをCycle docのTest Listセクションに転記。

```markdown
## Test List

### TODO
- [ ] TC-01: [test case]
- [ ] TC-02: [test case]

### WIP
(none)

### DISCOVERED
(none)

### DONE
(none)
```

### Step 3.5: Codex Debate (optional)

1. `which codex` でCodex利用可能か確認
2. 利用不可 → 既存 review --plan にフォールバック（結果をProgress Logに記録）、Step 4へ
3. 利用可能 → reference.mdのDebate Workflowを実行
4. 結果をCycle docのImplementation Notesに追記（Accepted/Rejected/Deferred）

### Step 4: Complete
Output: KICKOFF完了。Cycle doc: {path}。次: orchestrate→自動RED / 手動→ /review --plan

## Reference

- [reference.md](reference.md) / Templates: [../spec/templates/cycle.md](../spec/templates/cycle.md)
