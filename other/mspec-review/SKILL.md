---
name: mspec-review
description: self-review step of mspec workflow — sanity-check all artifacts via subagent
when_to_use: User runs /mspec:review, or workflow auto-continues to self-review
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Run `mspec continue --change <change-dir> --json` to fetch `subagent_prompt`.
3. Read all `requires` (`checklist.md`, `design.md`, `architecture-overview.md`, `quickstart.md`).
4. Invoke `mspec-self-reviewer` subagent (Task tool) with `subagent_prompt`.
5. Append the subagent's review notes as a `## Self-Review` section to `design.md` (no new files; `produces: []`).
6. Update Constitution Check tables across artifacts where the reviewer flagged gaps.
7. Run `mspec validate --change <change-dir>`.
8. `block: true` — stop and ask the user to run `/mspec:continue`.

<!-- @mspec-delta 2026-05-25-131216-agent-experience-manifest/specs/skill-observability/spec.md -->
<!-- Requirements implemented: FR-001, FR-002 -->
<!-- Change: agent-experience-manifest -->

## Observation (Agent Experience Log)

After the subagent completes (step 4), count `[blocker]` lines in the review output, then record the run:

```bash
mspec agent-run record self-review \
  --change <change-name> \
  --bytes <sum-of-input-artifact-bytes> \
  --artifacts <space-separated-artifact-paths> \
  --edits <count-of-[blocker]-lines>
```

Example: `mspec agent-run record self-review --change 2026-05-25-my-feature --bytes 22180 --artifacts checklist.md design.md tasks.md --edits 2`

This appends one JSONL entry to `changes/<change>/.agent-runs.jsonl`. Do NOT include prompt text or file contents.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認
- self-review の `[blocker]` 指摘がゼロになっているか確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
