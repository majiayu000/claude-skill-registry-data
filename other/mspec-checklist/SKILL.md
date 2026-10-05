---
name: mspec-checklist
description: checklist step of mspec workflow — produce checklist.md via subagent
when_to_use: User runs /mspec:checklist, or workflow auto-continues to checklist
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-015 -->
<!-- Change: step-checkbox-update -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Run `mspec continue --change <change-dir> --json` to fetch `subagent_prompt`.
3. Read `requires` (`specs/*/spec.md`, `design.md`).
4. Invoke `mspec-checklist-auditor` subagent (Task tool) — it should also scan related capability SoT specs for regression risk.
5. Write the returned `checklist.md` (Delta Spec Coverage / Source-of-Truth Regression / Constitution).
5a. `readme.md` の `## Artifacts` 節の `- [ ] checklist.md` を `- [x] checklist.md` に更新する。
6. Run `mspec validate --change <change-dir>`. validate が失敗した場合は `- [x] checklist.md` を `- [ ] checklist.md` にロールバックする。
7. `block: false` — auto-continue.

<!-- @mspec-delta 2026-05-25-131216-agent-experience-manifest/specs/skill-observability/spec.md -->
<!-- Requirements implemented: FR-001, FR-002 -->
<!-- Change: agent-experience-manifest -->

## Observation (Agent Experience Log)

After the subagent completes (step 4), record the run:

```bash
mspec agent-run record checklist \
  --change <change-name> \
  --bytes <sum-of-input-artifact-bytes> \
  --artifacts <space-separated-artifact-paths>
```

Example: `mspec agent-run record checklist --change 2026-05-25-my-feature --bytes 12340 --artifacts proposal.md specs/my-cap/spec.md design.md`

This appends one JSONL entry to `changes/<change>/.agent-runs.jsonl`. Do NOT include prompt text or file contents.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認
- `mspec verify llm --change <change>` — FR-IDごとのLLM評価プロンプトを生成してClaude Codeで実行（C2強化）
- checklist.md の `verify: fr-NNN` アノテーションがDelta Specの全FR-IDを網羅しているか手動確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
