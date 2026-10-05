---
name: mspec-visual-prototype
description: visual-mock step of mspec workflow — generate UI prototype HTML and collect feedback
when_to_use: User runs /mspec:prototype, or workflow auto-continues to visual-mock
---

<!-- @mspec-delta 2026-05-23-085322-rename-visual-mock-to-prototype/specs/visual-mock/spec.md -->
<!-- Requirements implemented: FR-005 -->
<!-- Change: rename-visual-mock-to-prototype -->

## Procedure

1. Run `mspec status --change <change-dir> --json` to confirm `current_step: "visual-mock"`.
2. Invoke the `mspec-visual-prototype-runner` subagent to generate `changes/<change>/prototype/index.html`.
   - Pass: the `## Goals` section from `proposal.md` + the detected `FrameworkInfo.promptHint` (run `mspec prototype --change <change-dir>` to get this).
3. Run `mspec prototype --change <change-dir>` to start the local server and display the URL.
4. Instruct the user to open `http://localhost:<port>` in their browser.
5. Wait for the user to review and press Ctrl+C. Feedback is automatically saved to `prototype-feedback.md`.
6. To skip: `mspec skip visual-mock --change <change-dir> --reason "<reason>"`.
7. `block: true` — stop and ask the user to run `/mspec:continue`.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
