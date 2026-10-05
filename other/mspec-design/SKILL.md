---
name: mspec-design
description: design step of mspec workflow — write design.md + design-rationale.md + architecture-overview.md, full Constitution Check
when_to_use: User runs /mspec:design, or workflow auto-continues to design
---

<!-- @mspec-delta 2026-05-18-044538-revise-artifact-taxonomy/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-022 -->
<!-- Change: revise-artifact-taxonomy -->

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-015 -->
<!-- Change: step-checkbox-update -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Read `research.md`.
3. Write `design.md` from the artifact template (`doc_type: Reference`). Fill: Summary, Technical Context, Phase 0 Constitution Check, Project Structure, Decisions.
   - `design.md` は「何を」設計したかを記述する Reference ドキュメント（構造・API・データモデル・契約）。採用理由・代替案・トレードオフは 3a で書く。
   - `## Decisions` セクションでは、各技術的決定の受け入れ基準を Delta Spec の Scenario（GIVEN/WHEN/THEN）と対応付けて記述する。これにより checklist と tasks.md の E2E タスクへのトレーサビリティを確保する。
   - 冒頭に `<!-- See also: ./design-rationale.md for採用理由・代替案 -->` コメントを追加する。
3a. Write `design-rationale.md` from the artifact template (`doc_type: Explanation`). このファイルは「なぜその設計を選んだか」を記述する Explanation ドキュメント。Fill:
   - `## Context` — この設計判断が必要となった背景・制約を 2-3 段落で記述。
   - `## Decisions` — 各意思決定の採用理由を 2-3 段落で記述。`design.md` の Project Structure / Decisions と相互参照する。
   - `## Alternatives Considered` — 検討した代替案とその評価を箇条書きで記述。
   - `## Trade-offs` — 採用案で受け入れたトレードオフを列挙。
   - `## Rejected Options` — 却下した選択肢と却下理由を列挙。
   - 冒頭に `<!-- See also: ./design.md -->` コメントを付ける。
4. Write `architecture-overview.md` with at minimum a Mermaid System Diagram (required). Add Sequence / Data Model diagrams when applicable. Inline SVG only if Mermaid can't express it.
5. Re-evaluate the Constitution Check on both `design.md` (Phase 1) and `design-rationale.md` (Phase 1) — both Phase 0 and Phase 1 columns must be filled in each file.
6. If any ❌, fill `### Complexity Tracking` with justification (otherwise write "None").
7. Use AskUserQuestion when material design trade-offs need user input.
7a. `design.md` と `design-rationale.md` と `architecture-overview.md` の 3 ファイルがすべて書き込まれた後、`readme.md` の `## Artifacts` 節の `- [ ] design.md / architecture-overview.md` を `- [x] design.md / design-rationale.md / architecture-overview.md` に更新する。
   - `design-rationale.md` のチェックボックス `- [ ] design-rationale.md` が別行にある場合も同様に `- [x]` に更新する。
8. Run `mspec validate --change <change-dir>`. validate が失敗した場合は `- [x] design.md / design-rationale.md / architecture-overview.md` を `- [ ] design.md / design-rationale.md / architecture-overview.md` にロールバックする。
   - `design-rationale.md` が欠落している場合は 3a に戻って作成する。
9. `block: true` — stop and ask the user to run `/mspec:continue`.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認
- `mspec validate --change <change> --strict` — Constitution Check両Phase確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
