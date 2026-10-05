---
name: mspec-tasks
description: tasks step of mspec workflow — produce tasks.md with anchor blocks
when_to_use: User runs /mspec:tasks, or workflow auto-continues to tasks
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-015 -->
<!-- Change: step-checkbox-update -->

<!-- @mspec-delta 2026-05-21-055911-ui-visual-mock-workflow/specs/visual-mock/spec.md -->
<!-- Requirements implemented: FR-004 -->
<!-- Change: ui-visual-mock-workflow -->

<!-- @mspec-delta 2026-05-24-085415-risk-tier-field/specs/verify-routing/spec.md -->
<!-- Requirements implemented: FR-002 -->
<!-- Change: risk-tier-field -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Before generating tasks.md, check if `changes/<change>/mock-feedback.md` exists and is not a skipped placeholder (`<!-- mspec: skipped step -->`). If it exists and is not a placeholder, read its content and incorporate the feedback as additional context when writing tasks.md.
3. Read `design.md` and `checklist.md`.
4. Write `tasks.md` from the template: Phase 1 Setup / Phase 2 Foundational / Phase 3 User Story / Phase 4 Polish.
5. For each implementation and E2E task, attach the 3-line `anchor:` block:
   ```
   @mspec-delta <change-dir>/specs/<capability>/spec.md
   Requirements implemented: FR-NNN[, FR-NNN, ...]
   Change: <feature-kebab>
   ```
6. Tests-first: every Scenario in the Delta Spec needs an E2E task **before** its implementation task. Implementation tasks list the same FR-IDs as the E2E that exercises them.
6a. **verify アノテーションの risk_tier 分岐**: 各タスクの `anchor: Requirements implemented: FR-NNN` に対応する FR の `risk_tier` を Delta Spec から読み込み、以下のルールで verify アノテーションを付与する:
   - `risk_tier: critical` → `<!-- verify: human -->` を付与（人間レビュー必須）
   - `risk_tier: standard` または未記載 → `<!-- verify: fr-NNN -->` を付与（既存動作）
   - `risk_tier: trivial` → verify アノテーションを付与しない
7. Append the `## Constitution Check` table (Phase 0 only).
7a. `readme.md` の `## Artifacts` 節の `- [ ] tasks.md` を `- [x] tasks.md` に更新する。
8. Run `mspec validate --change <change-dir>`. validate が失敗した場合は `- [x] tasks.md` を `- [ ] tasks.md` にロールバックする。
9. `block: true` — stop and ask the user to run `/mspec:continue`.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — tasks.md内アンカーブロックの解決確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
