---
name: mspec-new
description: new step of mspec workflow — bootstrap a change directory and readme.md
when_to_use: User runs /mspec:new, or workflow auto-continues to new
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-16-170347-lightweight-change-mode/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-018 -->
<!-- Change: lightweight-change-mode -->

## Procedure

1. Run `mspec status --json` (no `--change`) to confirm overall repo state.
2. Read the user's request and propose a kebab-case feature name (ask once if ambiguous).
3. Run `mspec new <feature-kebab>` — the CLI creates `changes/<YYYY-MM-DD-HHMMSS>-<feature>/readme.md`.
4. Open `readme.md` and write a 1–3 line `## Request` summary based on the user's words. Leave `## Artifacts` checkboxes unchecked and `## Skipped Steps` empty.
4a. **モード推定**（`--mode` 明示指定がない場合のみ）:
    - 説明文から AI がモード（`typo` / `minor` / `bugfix`）を推定する。
    - AskUserQuestion で「`<mode>` モードと判断しました。正しいですか？」と 1 問確認する。
    - 承認されたら `readme.md` の `## Request` 直後に `> Mode: <mode>` 行を追記する。
    - `--mode <value>` 明示指定の場合は推定・確認をスキップして直接追記する。
    - フルフロー変更（typo / minor / bugfix 以外）の場合は `> Mode:` 行を追記しない。
5. Run `mspec validate --change <change-dir>`.
6. `block: true` — stop and ask the user to run `/mspec:continue` when ready.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認
- `mspec status --json` — リポジトリ全体の状態確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
