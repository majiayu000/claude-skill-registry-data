---
name: review
description: 統一レビュースキル。mode "plan"（設計レビュー）または "code"（コードレビュー）で動作。Risk-based scaling でエージェント数を最適化。REFACTORの次フェーズ。「レビューして」「review」で起動。
allowed-tools: Task, Read, Edit, Bash, Grep, Glob
---

## Mode Determination

| 引数/コンテキスト | Mode | 入力ソース |
|------------------|------|-----------|
| `--plan` or PLAN直後 | "plan" | planファイル |
| `--code` or REFACTOR直後 | "code" | `git diff HEAD` |
| 引数なし | "code" (default) | `git diff HEAD` |

## Workflow

### Gate (mode別)

**plan mode**: planファイルの存在確認。なければ BLOCK: 「先に spec を実行してください」（**plan file 前提**: Cycle doc は承認後にのみ生成されるため、plan mode review は Cycle doc 不在でも plan ファイル単体で動作する）

**code mode only**:
- Cycle Doc Gate (frontmatter のみ): `for f in docs/cycles/*.md; do [ -f "$f" ] || continue; fm=$(awk '/^---$/{c++;next} c==1{print}' "$f"); echo "$fm" | grep -q '^phase:' || continue; echo "$fm" | grep -q 'phase: DONE' && continue; printf '%s\t%s\n' "$(echo "$fm" | awk 'sub(/^updated: */,""){gsub(/T/," ");print;exit}')" "$f"; done | sort | tail -1 | cut -f2` → found: continue / not found: BLOCK(run spec)
- Cycle doc を読み、これまでの成果を把握する
- Phase Ordering Gate: Progress Log に `REFACTOR` の `Phase completed` 記録があるか確認。なければ BLOCK: 「先に refactor を実行してください」
- **Repo-state pre-check** (cycle 20260424_1119 #3): review 実行前に `git status --short` を先に確認し、`??` (untracked) or ` D` (unstaged deletion) を検出したら WARN + 対応案内。新規 test file / Cycle doc 等が未 staged のまま review されるのを防ぐ。

Mode を判定し出力: `[REVIEW] Mode: plan` or `[REVIEW] Mode: code`

### Step 1-5: Review Pipeline

1. **Risk Classification**: `risk-classifier.sh` で決定論的判定
2. **Review Brief**: review-briefer (haiku) で圧縮 Brief 生成
3. **Lint-as-Code** (code mode のみ): 静的解析ツール実行
4. **Specialist Panel**: Always-on: security-reviewer + correctness-reviewer (code) / design-reviewer (plan)。Risk-gated: performance/product/usability-reviewer。起動前に `.claude/dev-crew.json` の review_policy を読みモデルを解決する（self=orchestrator の現モデル、explicit=指定モデル、HIGH tierはescalate_high_to）。詳細: [steps-subagent.md](steps-subagent.md) / [reference.md](reference.md#review_policy-解決規則)
5. **Verdict Aggregation**: critical≥1=BLOCK(plan→PLAN再設計/code→RED/GREEN/REFACTOR) / important≥1=WARN / else=PASS（severity-verdict.sh が決定論集計）

### Progress Log 更新

code mode: Cycle doc に Progress Log追記(`### {date} - REVIEW\n- {summary}\n- Phase completed`) + frontmatter更新(phase/updated)
plan mode: **plan file 前提** — Cycle doc は承認後にのみ存在する。Cycle doc 不在時は plan ファイルへの追記は行わず（IMMUTABLE、cycle 20260717_1126_approval-reorder）、レビュー結果はそのターンの応答で報告するのみ（skip）

### Step 7: DISCOVERED -> Issue

code mode: Cycle doc の DISCOVERED セクション未起票項目を `gh issue create` で起票。
plan mode: Cycle doc 不在時は skip（DISCOVERED 追跡は承認後の Cycle doc 生成後に一元化する）。詳細: [reference.md](reference.md#discovered-issue-起票)

## Codex Integration

Codex 利用可能時、orchestrate が本スキルと Codex レビューを並行実行し、findings を統合する（competitive review）。単体 `/review` 実行時は Claude-side pipeline のみ動作する。詳細: [steps-codex.md](../orchestrate/steps-codex.md)

## Reference

- 詳細: [reference.md](reference.md)
- Risk Classifier: [risk-classifier.sh](risk-classifier.sh)
- Severity Verdict: [severity-verdict.sh](severity-verdict.sh)
