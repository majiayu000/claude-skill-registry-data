---
name: codify-insight
description: "TDD サイクルの retrospective insights を自動 triage し、必要時のみ codify/defer/no-codify を確認する decide gate スキル。次サイクル開始時に /orchestrate Block 0 から自動起動。「codify」「codify-insight」「insight codify」「次サイクル開始時」で手動起動も可。"
allowed-tools: Read, Edit, AskUserQuestion, Glob
---

# codify-insight

## Workflow

### Hard Gate

Captured cycles scan (frontmatter-only):

```bash
for f in docs/cycles/*.md; do
  awk '/^---$/{c++;next} c==1{print}' "$f" | grep -q 'retro_status: captured' && echo "$f"
done
```

非空 → 処理対象 cycles を収集。
空 → no-op exit 0: 「No captured cycles found. Nothing to codify.」を出力して終了。

### Idempotency Check

各 cycle doc の `retro_status` を確認:
- `retro_status: resolved` → skip（既に全 insight 判定済み）
- `retro_status: none` → skip（retrospective 未実行）
- `retro_status: captured` → 処理対象

`## Codify Decisions` セクション内の `### Insight N` heading 存在 = 該当 insight 判定済み。
partial 完了時は未判定 insight のみ処理し、captured を維持して再起動で残分を処理。

### Recurrence-aware Pre-triage (質問を減らす一次フィルタ)

autonomous triage の前に、直近 10 cycle docs の `## Retrospective` + `## Codify Decisions` を scan し頻度判定:

- **同 key phrase が 2+ 回再発** → 自動 `codified` → `rule` (質問スキップ、promotion 確定)
- **過去 cycle で同 insight が `no-codify` 判定済み** → 自動 `no-codify` (質問スキップ、duplicate)
- **1 回以下 (novel / 初出)** → 下記 autonomous triage へ

scan 詳細 + threshold 調整は reference.md 参照。

### Default: Autonomous Batch Triage

pre-triage で処理されなかった insight は 1 cycle 分まとめて自動 triage。per-insight AskUserQuestion をデフォルトにしない。

優先ルール:
- 次 cycle の TDD をすぐ harden できるもの → `codified` with `rule` or `inline-update`
- post-TDD の広い改善、repo-wide sweep → `deferred`（通常 `new-cycle`）
- observation-only / 2nd-order note → `no-codify`
- `skill` destination は rare。2+ cycles 再発 + 複数 phase / repo 再利用時のみ
- destination `rule` は tier（`always` / `cycle-scoped` / `file-scoped`）を必須指定する
- tier ごとの paths・交換条件・反映責務は [reference.md](reference.md#rule-tier-contract) に従う

### AskUserQuestion Fallback (only when needed)

以下の場合のみ AskUserQuestion (1 cycle max 1 回の batch、per-insight 不可):
- `skill` 候補で destination 妥当性の確認が必要
- autonomous triage で `codified` vs `deferred` の境界が低確信
- ユーザーが対話的 codify を明示要求

全件 recurrence or high-confidence triage なら質問 0 件で summary のみ print。

### Output

Cycle doc EOF に `## Codify Decisions` セクションを append (APPEND-ONLY):

```markdown
## Codify Decisions

### Insight N
- **Decision**: codified
- **Destination**: rule
- **Tier**: cycle-scoped (rule のみ必須: always / cycle-scoped / file-scoped)
- **Paths**: (file-scoped のみ必須: repo-relative glob)
- **Reason**: (optional)
- **Decided**: YYYY-MM-DD HH:MM
```

既存 `## Retrospective` セクションは一切変更しない。

### State Transition

全 insight triage 完了時: `retro_status: captured` → `resolved` + `updated` を更新。
partial 完了時: frontmatter 遷移なし（captured 維持）。

### Exit Contract (orchestrate 連携)

cycle-retrospective precedent 準拠の block-or-complete 契約:
- **全 captured cycles が resolved** → exit 0。orchestrate Block 0 は次ステップへ進行。
- **User mid-gate abort** → exit 1 + stderr「codify-insight aborted by user. orchestrate should BLOCK and re-invoke /orchestrate」。orchestrate は BLOCK (cycle-retrospective abort と同じ pattern)。
- **captured 残存 (skill 異常終了)** → orchestrate は次回 /orchestrate 起動時に再度 Block 0 codify gate でスキャン、再処理。

## Reference

詳細: [reference.md](reference.md)
