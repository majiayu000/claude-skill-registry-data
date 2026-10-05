---
name: mspec-research
description: research step of mspec workflow — investigate via subagent and produce research.md
when_to_use: User runs /mspec:research, or workflow auto-continues to research
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->

<!-- @mspec-delta 2026-05-15-040857-step-checkbox-update/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-015 -->
<!-- Change: step-checkbox-update -->

## Procedure

1. Run `mspec status --change <change-dir> --json` first.
2. Run `mspec continue --change <change-dir> --json` to fetch the ready-made `subagent_prompt`.
3. Read `requires` artifacts (`proposal.md`, `specs/*/spec.md`).
4. Invoke the `mspec-researcher` subagent via the Task tool with `subagent_prompt`. It will perform web search and codebase analysis.
5. Receive the `research.md` body (Decisions / Web References / Codebase Findings / Open Choices) and write it to disk.
6. For any `Open Choices`, ask the user via AskUserQuestion (1 question per call) and update the file.
7. Append the `## Constitution Check` (Phase 0 only).
7a. `readme.md` の `## Artifacts` 節の `- [ ] research.md` を `- [x] research.md` に更新する。
8. Run `mspec validate --change <change-dir>`. validate が失敗した場合は `- [x] research.md` を `- [ ] research.md` にロールバックする。
9. `block: true` — stop and ask the user to run `/mspec:continue`.

<!-- @mspec-delta 2026-05-25-131216-agent-experience-manifest/specs/skill-observability/spec.md -->
<!-- Requirements implemented: FR-001, FR-002 -->
<!-- Change: agent-experience-manifest -->

## Observation (Agent Experience Log)

After the subagent completes (step 4), record the run:

```bash
mspec agent-run record research \
  --change <change-name> \
  --bytes <sum-of-input-artifact-bytes> \
  --artifacts <space-separated-artifact-paths>
```

Example: `mspec agent-run record research --change 2026-05-25-my-feature --bytes 4821 --artifacts proposal.md specs/my-cap/spec.md`

This appends one JSONL entry to `changes/<change>/.agent-runs.jsonl`. Do NOT include prompt text or file contents.

## Verification (C2)

- `mspec validate --change <change>` — アーティファクト整合性チェック
- `mspec anchor check --change <change>` — アンカー解決確認

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
