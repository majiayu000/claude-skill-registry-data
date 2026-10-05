---
name: mspec-implement
description: implement step of mspec workflow — write code/tests with TDD red→green and anchors
when_to_use: User runs /mspec:implement, or workflow auto-continues to implement
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-14-105021-checklist-ai-driven-verification/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-012, FR-013, FR-014 -->
<!-- Change: checklist-ai-driven-verification -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-016 -->
<!-- Change: step-checkbox-update -->

<!-- @mspec-delta 2026-05-24-085415-risk-tier-field/specs/verify-routing/spec.md -->
<!-- Requirements implemented: FR-004 -->
<!-- Change: risk-tier-field -->

<!-- @mspec-delta 2026-05-26-123041-p2-implement-iteration-loop/specs/cli-workflow-engine/spec.md -->
<!-- Requirements implemented: FR-024, FR-025 -->
<!-- Change: p2-implement-iteration-loop -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Read `tasks.md`.
3. For each task in dependency order:
   - Copy its 3-line `anchor:` block to the head of the target file (within the first 10 lines, language-appropriate comment).
   - If it is an **E2E test** task: write the failing test, then run `mspec test --expect-red <task-id> --change <change-dir>` to record red evidence.
   - If it is an **implementation** task: implement the code, then run `mspec test --expect-green <task-id> --change <change-dir>` to record green evidence.
   - After `--expect-green` is recorded, read the task's anchor `Requirements implemented: FR-NNN` list. For each FR-NNN, scan `checklist.md` and update any `- [ ] ... <!-- verify: fr-NNN -->` lines to `- [x] ... <!-- verify: fr-NNN -->` (idempotent: skip lines already `- [x]`; skip if no matching annotation found — checklist.md remains unchanged). <!-- FR-012 auto-check -->
   - After `--expect-green` is recorded (全テスト GREEN の場合のみ)、`tasks.md` の当該タスク行 `- [ ] TNNN: …` を `- [x] TNNN: …` に更新する（冪等: すでに `- [x]` の行は変更しない）。<!-- FR-016 tasks-checkbox -->
3a. **max_iterations エスカレーション**（FR-025）: 各タスクで TDD red→green サイクルを試みる際、`mspec schema show` で `max_iterations` を読み込む。同一タスクで green が `max_iterations` 回連続して失敗した場合は以下を実行する:
   1. `design.md` 末尾に以下のセクションを追記する（既存セクションには触れない）:
      ```markdown
      ## Escalation Summary
      - Task: <task-id>
      - Iterations: <n> / <max_iterations>
      - Reason: <失敗理由の要約（テストエラー・設計上の矛盾点）>
      - Recommendation: 設計変更 | 仕様見直し | 環境確認
      ```
   2. AskUserQuestion でユーザーに判断を委ねる（「設計を変更しますか？仕様を見直しますか？」）。ユーザーの回答に従い継続または中断する。
4. Use AskUserQuestion if any decision deviates from `design.md`.
4a. **critical FR の verify: human 未達警告**（verify-routing FR-004）: `--expect-green` 記録後、checklist.md に `risk_tier: critical` の FR に対応する `<!-- verify: human -->` 未チェック項目が残っている場合、以下の警告を出力して処理を継続する（エラー停止はしない）:
   `Warning: FR-NNN (critical) requires human review. Mark as verify: human before archive.`
5. After all tasks complete, scan `checklist.md` for remaining unchecked items and report: <!-- FR-013 report -->
   - `verify: human` 未チェック項目あり → 一覧をユーザーに提示し、人間レビューを要求してブロックする（block）
   - `verify: fr-NNN` 未チェック項目あり（gap）→ 対象 FR 番号とギャップ（tasks.md の `Requirements implemented` アンカーに対応 FR が存在しない）を警告し、ユーザーの確認を待つ（警告 + block）
   - 未チェック項目ゼロ → 実装完了を宣言（block なし）
6. After all tasks:
   - Run `mspec anchor check --change <change-dir>` (must pass; `enforce_anchor: true`).
   - Run `mspec validate --change <change-dir>` (checks `enforce_e2e` and `enforce_tdd`).
7. `block: true` — stop and ask the user to run `/mspec:continue`.

## Verification (C2)

- `mspec test expect-green <task-id> --change <change>` — TDD green確認
- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認
- `mspec validate --change <change> --strict` — enforce_anchor / enforce_tdd 確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
