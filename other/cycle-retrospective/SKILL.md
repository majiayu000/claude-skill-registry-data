---
name: cycle-retrospective
description: "TDD サイクル末尾で「最初の失敗 → 最終解 → 事前知識化」のペアを抽出する advisory スキル。失敗-成功ペアの言語化に特化、dedup/codify 分類は codify-insight (Cycle B) に委譲。「retrospective」「振り返り」「サイクル振り返り」で起動。"
allowed-tools: Read, Edit, AskUserQuestion
---

# cycle-retrospective

## Workflow

### Hard Gate

1. **Cycle doc 存在**: 不在 → BLOCK: 「先に spec/orchestrate を実行してください」
2. **Phase 制約** (Codex P2-1 対応、mid-cycle 実行で A2b inline 呼び出しの順序が永続破壊されるのを防ぐ): phase が `REVIEW` / `COMMIT` / `DONE` のいずれかのみ許可。`INIT` / `KICKOFF` / `RED` / `GREEN` / `REFACTOR` → BLOCK: 「cycle-retrospective は REVIEW phase 以降で実行してください (現 phase: $phase)」

### Idempotency Check

- frontmatter `retro_status` が `none` 以外 (captured / resolved / フィールド不在) → skip + 「既に処理済み (retro_status: $value)」を出力して exit 0
- `retro_status: none` の場合のみ抽出フェーズへ進む

### Extraction (LLM)

- Cycle doc 全体を読む (plan / phase summaries / review verdicts / test failures / retry log / DISCOVERED)
- Failure → Final fix → Insight ペアを抽出 (詳細手順: reference.md)
- 想起漏れ設問を評価: 今回の手戻りは過去のどの cycle doc を最初に読んでいれば防げたか（該当なし可、reference.md の `### 想起漏れ` スキーマで記録）
- **抽出 0 件 (no reusable lesson)** — 抽出は成功したが再利用可能な知見が見つからないケース (Codex P2-2 対応): 通常 exit path、Retrospective に `No reusable lesson this cycle` を記録して retro_status: resolved に遷移 (user intervention 不要、AskUserQuestion も実行しない)
- **抽出エラー (LLM error / parse error)** — LLM 実行自体が失敗したケース: retry N=2 → 全失敗時は AskUserQuestion で override (proceed / abort)。no-lesson path と混同しない

### Output (Cycle doc 更新)

state-ownership.md の cycle-retrospective 行に従う:

- **Body**: `## Retrospective` を Cycle doc EOF (`## Next Steps` の後) に append (APPEND-ONLY 遵守、middle-insert 禁止、既存内容は一切変更しない)
- **想起漏れ記録**: 全正常終了経路（通常テンプレート / no-lesson / override-proceed）で `### 想起漏れ` を記録する。abort（ファイル非変更）のみ対象外
- **frontmatter**: `retro_status` (none → captured / none → resolved) と `updated` のみ更新
  - `captured`: 有効な insight を追記した場合
  - `resolved`: no-lesson / override-proceed (`Extraction skipped by override` または `Extraction failed after N retries`) の場合
- **abort 選択時**: Cycle doc は変更せず、stderr に「Retrospective aborted by user. orchestrate should BLOCK commit.」を出力して exit 1

## Reference

詳細: [reference.md](reference.md)
