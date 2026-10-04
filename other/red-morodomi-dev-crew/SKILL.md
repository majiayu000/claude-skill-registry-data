---
name: red
description: テストコードを作成し、失敗することを確認する（並列実行対応）。PLANの次フェーズ。「テスト書いて」「red」で起動。
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob
---

## Current State
!`ls -t docs/cycles/*.md 2>/dev/null | head -1 || echo "(none)"`

## 禁止事項

- 実装コード作成（GREENで行う）
- テストを通すための実装

## Workflow

### Cycle Doc Gate
`for f in docs/cycles/*.md; do [ -f "$f" ] || continue; fm=$(awk '/^---$/{c++;next} c==1{print}' "$f"); echo "$fm" | grep -q '^phase:' || continue; echo "$fm" | grep -q 'phase: DONE' && continue; printf '%s\t%s\n' "$(echo "$fm" | awk 'sub(/^updated: */,""){gsub(/T/," ");print;exit}')" "$f"; done | sort | tail -1 | cut -f2` → found: continue / not found: BLOCK(run spec)

### Pre-RED Gate (deterministic)

Cycle doc の Progress Log を確認し、以下が全て満たされなければ BLOCK:

1. **sync-plan完了**: Progress Log に `SYNC-PLAN` または `sync-plan` セクションがあり、`Phase completed` 記録がある
2. **Plan Review完了**: Progress Log に `Plan Review` または `plan-review` の記録がある

```bash
# Cycle doc を取得（Cycle Doc Gate で既に特定済み）
# 1. sync-plan チェック
awk '/SYNC.PLAN|sync-plan/,/Phase completed/' "$CYCLE_DOC" | grep -qi 'Phase completed'
# 2. Plan Review チェック
grep -qiE 'Plan Review|review.*plan' "$CYCLE_DOC"
```

いずれか失敗 → BLOCK（不足ステップを案内）

Test ListのTODOからテストケースを選択してWIPに移動。

### Complexity Gate

Test List に対してREDフェーズ開始時に評価する。詳細: [reference.md](reference.md#complexity-classification)

| Class | Criteria | Stages |
|-------|----------|--------|
| trivial | 1-2 items, Example only, no escalation triggers | Stage 1 as 1-line GWT; Stage 2 skip; Stage 3 |
| standard | 3-5 items, Example only, no complex escalation triggers | Stage 1 simplified; Stage 2 Review skip; Stage 3 |
| complex | 6+ items OR any non-Example paradigm | Full 3-stage (all stages) |

### Stage 1: Test Plan

Cycle doc の Test List を Given/When/Then + 具体テストデータに展開。詳細: [reference.md](reference.md#test-plan-stage)

### Stage 2: Test Plan Review

要件とテスト計画を照合（網羅性・カテゴリバランス）。Gap発見時は追加。詳細: [reference.md](reference.md#tp-review)

### Stage 3: Test Code

テストファイル依存関係分析 → red-worker並列起動 → 結果収集・マージ → テスト実行で**失敗**確認。
詳細: [reference.md](reference.md#dependency-analysis)

### Stage 3.5: False-pass 自己証明

新規 test の literal が「false-pass 不在を自己証明」できることを確認（対象行除去 → count 0 / FAIL の実証）。手順: [reference.md](reference.md#false-pass-self-proof)

### exspec check (optional)

`command -v exspec` で存在確認。インストール済みかつ対応言語なら `scripts/gates/exspec-check.sh` を実行。
BLOCK検出時はRED失敗（修正→再実行）。未インストール or 非対応言語はスキップ。
詳細: [reference.md](reference.md#exspec)

### Verification Gate
`Tests fail → PASS(→GREEN) | Tests pass → BLOCK(review test conditions)`

### Cycle doc更新
Progress Log追記(`### {date} - RED\n- {summary}\n- Phase completed`) + frontmatter更新(phase/updated)

### 完了

RED完了。次: Orchestrate時は自動GREEN / 手動時は `/green`。

## Reference

- 詳細: [reference.md](reference.md)
- red-worker: [../../agents/red-worker.md](../../agents/red-worker.md)
