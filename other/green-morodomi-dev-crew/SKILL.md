---
name: green
description: テストを通すための最小限の実装を行う。REDの次フェーズ。「実装して」「green」で起動。
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob
---

## Current State
!`ls -t docs/cycles/*.md 2>/dev/null | head -1 || echo "(none)"`

## 禁止事項

- 過剰な実装（テストに必要ない機能）
- リファクタリング（REFACTORで行う）
- 新しいテスト作成（REDで行う）

## Workflow

### Cycle Doc Gate
`for f in docs/cycles/*.md; do [ -f "$f" ] || continue; fm=$(awk '/^---$/{c++;next} c==1{print}' "$f"); echo "$fm" | grep -q '^phase:' || continue; echo "$fm" | grep -q 'phase: DONE' && continue; printf '%s\t%s\n' "$(echo "$fm" | awk 'sub(/^updated: */,""){gsub(/T/," ");print;exit}')" "$f"; done | sort | tail -1 | cut -f2` → found: continue / not found: BLOCK(run spec)

WIPのテストケースを抽出。

### Step 2: ファイル依存関係分析

テストケースを対象ファイル別にグルーピング。同一ファイル→同一workerに割り当て（競合回避）。

### Step 3: green-worker並列起動

Taskツールで `dev-crew:green-worker` を並列起動。

### Step 4: 結果収集・マージ

全workerの完了を待ち、結果を統合。失敗時は該当workerのみ再試行。

### Step 5: 全テスト実行→成功確認

全テストが**成功**すること（GREEN状態）を確認。

### Verification Gate
`All tests pass → PASS(→REFACTOR) | Tests fail → BLOCK(retry worker)`

### Cycle doc更新
Progress Log追記(`### {date} - GREEN\n- {summary}\n- Phase completed`) + frontmatter更新(phase/updated)

### Step 7: 完了

GREEN完了。次: Orchestrate時は自動REFACTOR / 手動時は `/refactor`。

## Reference

- 詳細: [reference.md](reference.md)
- green-worker: [../../agents/green-worker.md](../../agents/green-worker.md)
