---
name: refactor
description: refactorフェーズを実行し、チェックリスト駆動でコード品質改善を行う。Verification Gateで品質確認。GREENの次フェーズ。「リファクタして」「refactor」で起動。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

## Naming

- **Skill**: refactor (lowercase)
- **Phase**: REFACTOR (uppercase)

## 禁止事項

- テストを壊す変更
- 新機能の追加（次のサイクルで）
- テストの削除・変更

## Workflow

### Cycle Doc Gate
`for f in docs/cycles/*.md; do [ -f "$f" ] || continue; fm=$(awk '/^---$/{c++;next} c==1{print}' "$f"); echo "$fm" | grep -q '^phase:' || continue; echo "$fm" | grep -q 'phase: DONE' && continue; printf '%s\t%s\n' "$(echo "$fm" | awk 'sub(/^updated: */,""){gsub(/T/," ");print;exit}')" "$f"; done | sort | tail -1 | cut -f2` → found: continue / not found: BLOCK(run spec)

Cycle doc を読み、これまでの成果を把握する。

### Step 2: テスト確認

全テストがPASSすることを確認してから開始。

### Step 3: チェックリスト駆動リファクタリング

今回のサイクルで変更・作成したファイルを対象に、以下のチェックリストを順に確認する。
1改善→テスト実行→次改善 のインクリメンタルアプローチで進める。

| # | 項目 | 確認観点 |
|---|------|---------|
| 1 | 重複コード | 同一・類似ロジックの共通化 (DRY) |
| 2 | 定数化 | マジックナンバー・マジックストリングの定数抽出 |
| 3 | 未使用import | 不要なimport/require/useの削除 |
| 4 | let→const | 再代入のないletをconstに変更 |
| 5 | メソッド分割 | 長いメソッドの責務分割 |
| 6 | N+1クエリ | ループ内のDB/APIクエリを一括取得に変換 |
| 7 | 命名一貫性 | プロジェクト規約に沿った命名統一 |

各項目で改善が不要なら次へ進む。全項目確認後、Verification Gate に進むこと。

### Verification Gate
`Tests PASS + lint 0 + format OK → PASS(→REVIEW) | fail → fix & retry`

### Cycle doc更新
Progress Log追記(`### {date} - REFACTOR\n- {summary}\n- Phase completed`) + frontmatter更新(phase/updated)

### 完了
Output: REFACTOR完了。次: orchestrate→自動REVIEW / 手動→ /review

## Codex Execution

チェックリスト駆動のため Claude/Codex どちらでも実行可能（cross-tool compatible）。

## Reference

- 詳細: [reference.md](reference.md)
