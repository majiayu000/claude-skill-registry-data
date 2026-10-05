---
name: mspec-archive
description: archive step of mspec workflow — deterministic merge into SoT spec and archive move
when_to_use: User runs /mspec:archive, or workflow auto-continues to archive
---

<!-- @mspec-delta 2026-05-15-063805-fix-command-name-consistency/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-017 -->
<!-- Change: fix-command-name-consistency -->
<!-- @mspec-delta 2026-05-28-112728-improve-postmortem-quality/specs/mspec-nextaction-planner/spec.md -->
<!-- Requirements implemented: FR-003 -->
<!-- Change: improve-postmortem-quality -->
<!-- @mspec-delta 2026-05-18-044538-revise-artifact-taxonomy/specs/claude-integration/spec.md -->
<!-- Requirements implemented: FR-023 -->
<!-- Change: revise-artifact-taxonomy -->
<!-- @mspec-delta 2026-05-27-115017-postmortem-archive-integration/specs/mspec-archive/spec.md -->
<!-- Requirements implemented: FR-001, FR-002, FR-003, FR-004 -->
<!-- Change: postmortem-archive-integration -->
<!-- @mspec-delta 2026-05-28-115937-fix-specviewer-purpose-regression/specs/mspec-archive/spec.md -->
<!-- Requirements implemented: FR-005 -->
<!-- Change: fix-specviewer-purpose-regression -->
<!-- postmortem-hook: v1 -->

## Procedure

1. Run `mspec status --change <change-dir> --json` and confirm all prior steps are `done` or `skipped`.
2. Run `mspec archive <change-dir> --dry-run` and show the diff to the user.
3b. Read the full content of the change directory — all artifacts (proposal, research, design, design-rationale, checklist, tasks) and the confirmed Delta Spec requirements. Generate a `## Summary (Lessons / Next Steps)` section with:
   - `### Lessons` — 3-5 bullet points (1-2 lines each) summarizing: what was learned, what worked well, what was surprising, Constitution Check ⚠️/❌ items and their resolution.
   - `### Next Steps` — 2-4 bullet points (1 line + related FR-ID link) identifying: follow-up changes needed, open choices left unresolved, RENAMED requirements deferred.
   Keep total length ≤ 30 lines / 1,500 characters.
   Replace the placeholder comment `<!-- archive ステップで AI が生成 -->` (or `<!-- archive step will auto-fill -->`) in `changes/<change-dir>/readme.md` with this generated content.
   This step MUST complete before step 3 (the `mspec archive -y` call) so that the filled readme is present when the CLI validates and moves the change directory.
3. On confirmation, run `mspec archive <change-dir> -y`. The CLI:
   - Validates the change.
   - Parses the Delta Spec sections and applies ADDED / MODIFIED / REMOVED / RENAMED to `specs/<capability>/spec.md` (no LLM involved).
   - Moves `changes/<change-dir>/` → `changes/archive/<change-dir>/` via `git mv`.
   - Re-runs `mspec anchor check` to confirm anchors still resolve.

3c. **[ポストモーテムフック]** archive 完了後、以下の 2 フローを順番に実行する。

**Lessons 分析フロー**:

1. アーカイブ済み readme.md のパスを確認する：`changes/archive/<change-dir>/readme.md`
2. `### Lessons` セクションの存在と内容を確認する
3. 空または存在しない場合は「Lessons なし: スキップ」を通知してスキップする
4. 存在する場合は `mspec-lessons-analyzer` サブエージェントを Agent tool でインライン起動する：
   ```
   Agent(prompt="...", subagent_type="mspec-lessons-analyzer")
   入力: { readme_path: "<絶対パス>" }
   ```
5. 返ってきた `LessonsProposal[]` が空の場合はスキップして通知する
6. 空でない場合は AskUserQuestion（multi-select）で全提案を一覧表示する：
   ```
   Q: constitution.md に追加する原則・制約を選択してください（複数選択可）
   Options: 各提案の text と target_section と source_lesson を表示
   ```
7. ユーザーが承認したエントリのみ `memory/constitution.md` の指定セクションに追記する：
   - `target_section = "Core Principles"` → `## Core Principles` セクション末尾に追記
   - `target_section = "Additional Constraints"` → `## Additional Constraints` の箇条書き末尾に追記
8. **MUST NOT**: ユーザーが却下したエントリは constitution.md に一切書き込まない

**Next Steps 評価フロー**:

1. 同じ readme.md の `### Next Steps` セクションの存在と内容を確認する
2. 空または存在しない場合は「Next Steps なし: スキップ」を通知してスキップする
3. 存在する場合は `mspec-nextaction-planner` サブエージェントを Agent tool でインライン起動する：
   ```
   Agent(prompt="...", subagent_type="mspec-nextaction-planner")
   入力: { readme_path: "<絶対パス>" }
   ```
4. 返ってきた `NextActionProposal[]` が空の場合はスキップして通知する
5. 空でない場合は AskUserQuestion（multi-select）で全提案を優先度付きで一覧表示する：
   ```
   Q: 新しいチェンジとして登録する Next Steps を選択してください（複数選択可）
   Options: [HIGH/MEDIUM/LOW] kebab_name: summary
   ```
6. ユーザーが承認したエントリについて、`request_summary` フィールドが存在する場合は `mspec new <kebab_name> --request "<request_summary>"` を実行し、存在しない場合は `mspec new <kebab_name>` にフォールバックする（`changes/` 配下のみ）
   - kebab_name はサブエージェントが正規化済みのため、そのまま引数に使用する
   - request_summary はサブエージェントが生成した1行テキスト（改行・`"`・`$`・バックティック・`\` を含まないことが保証済み）
7. **MUST NOT**: ユーザーが却下したエントリに対して `mspec new` を実行しない

3d. **[Purpose 自動生成]** archive 完了後、以下の手順でアーカイブ対象 capability の `## Purpose` フィールドを自動生成する:

1. Delta Spec のパス（`changes/archive/<change>/specs/*/spec.md`）から capability 名を抽出する
2. 各 capability について `specs/<capability>/spec.md` を読む
3. `## Purpose` セクションの内容がテンプレートプレースホルダー（`<このスペックがカバーする外部から観測可能な振る舞いの概要>`）と完全一致する場合:
   a. `## Requirements` セクション以下の内容を読む
   b. Requirements を基に、このスペックが**外部から観測可能な振る舞い**を 1〜2 文で要約する（locale 設定に従い ja→日本語/en→英語）
   c. プレースホルダーを生成した文章で置き換えて `specs/<capability>/spec.md` に書き込む
4. Purpose が既にプレースホルダー以外のテキストで記述済みの場合は**スキップ**する（べき等性）
5. 複数 capability のうち一部の生成が失敗した場合は **skip-and-continue** とし、失敗した capability を「Purpose 未生成: `<capability>`」としてマージサマリーに記録して残りを続行する

4. Report the merge summary to the user. Workflow complete.

## Verification (C2)

- `mspec archive <change> --dry-run` — マージ差分の事前確認
- `mspec anchor check` — アーカイブ後のアンカー解決確認
- `mspec validate --change <change>` — アーティファクト整合性チェック

## Learning (C3)

このスキルの実行で発生した学習候補を記録する:

```
<!-- LEARNING: <パターン説明> | source: <FR-ID> | confidence: low|medium|high -->
```

`mspec learn` コマンドが archive 済み changes からこれらを収集してpost-condition候補をproposeする。
