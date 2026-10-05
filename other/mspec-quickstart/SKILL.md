---
name: mspec-quickstart
description: quickstart step of mspec workflow — write quickstart.md
when_to_use: User runs /mspec:quickstart, or workflow auto-continues to quickstart
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-015 -->
<!-- Change: step-checkbox-update -->

<!-- @mspec-delta 2026-05-16-170347-lightweight-change-mode/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-019 -->
<!-- Change: lightweight-change-mode -->

## Procedure

0. **モードスキップ判定**: `readme.md` の `> Mode:` フィールドを読む。ワークフローの `modes.<mode>.skip` にこのステップ（`quickstart`）が含まれる場合は成果物を生成せず終了する（`mspec continue` がスキップ済みとして扱う）。
1. Run `mspec status --change <change-dir> --json` first.
2. Read `design.md`.
3. Write `quickstart.md` from the artifact template: Prerequisites, Setup, Try it (Golden Path), Verify, Troubleshooting.
3a. `readme.md` の `## Artifacts` 節の `- [ ] quickstart.md` を `- [x] quickstart.md` に更新する。
4. Run `mspec validate --change <change-dir>`. validate が失敗した場合は `- [x] quickstart.md` を `- [ ] quickstart.md` にロールバックする。
5. `block: false` — auto-continue.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
