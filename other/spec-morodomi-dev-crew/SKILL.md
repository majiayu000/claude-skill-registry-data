---
name: spec
description: TDDサイクルのコンテキストをplan mode内で設定する（plan mode専用）。Triggers on "spec", "new feature", "start TDD", "add feature", "機能追加", "TDDを始めたい", "新しい機能", "開発を始める", "新規開発". Do NOT use for continuing an existing cycle (check docs/cycles/ first).
allowed-tools: Read, Bash, Grep, Glob, AskUserQuestion
---

## Current State
!`ls -t docs/cycles/*.md 2>/dev/null | head -3 || echo "(none)"`

# TDD INIT Phase (Plan Mode)

plan mode内でTDDコンテキストを設定し、planファイルに記録する。

## Plan Mode Check

**plan modeでない場合**: 「plan modeで開始してください。EnterPlanMode → /spec」と案内して終了。

## Progress Checklist

```
- [ ] STATUS確認 → 環境収集 → 既存cycle確認
- [ ] 実装内容確認 → リスク評価 → スコープ確認
- [ ] planファイルにTDDコンテキスト記録
```

## Restrictions

- planファイルへの記録のみ（Cycle docはsync-planで作成）
- No implementation planning（plan modeの探索・設計で行う）/ No test/implementation code

## Workflow

### Step 1: Check Project Status

`cat docs/STATUS.md 2>/dev/null` — If not found, recommend `onboard`. Also check hooks: [reference.md](reference.md#hooks-check)

#### Version Gate

1. `.claude/dev-crew.json` を読む。missing なら警告して停止。
2. `installed_plugins.json` のdev-crewバージョンと比較。不一致なら警告して停止。

### Step 2: Collect Environment Info

Collect language versions and key packages. Details: [reference.md](reference.md)

### Step 3: Check Existing Cycles

`ls -t docs/cycles/*.md 2>/dev/null | head -1` — If an active cycle exists, recommend continuing it.

### Step 4: Ask What to Implement

Ask "What feature do you want to implement?" e.g., login, CSV export.

### Step 4.5: Risk Score Assessment

Calculate risk score (0-100). Keyword scores: [reference.md](reference.md)

| Score | Result | Action |
|-------|--------|--------|
| 0-29 | PASS | Auto-proceed |
| 30-59 | WARN | Quick questions ([reference.md](reference.md#warn-questions-30-59)) |
| 60-100 | BLOCK | Brainstorm ([reference.md](reference.md#brainstorm-questions-block-60-1)) |

### Step 4.8: Ambiguity Detection ([reference.md](reference.md#ambiguity-detection))

ユーザーの回答から仕様の曖昧さを検出し、Questioning Protocolで解消。カテゴリ: Data, API, UI/UX, Scope, Edge cases

### Step 5: Scope (Layer) Confirmation

Use AskUserQuestion to confirm scope (Backend/Frontend/Both). Layer/Plugin mapping table: [reference.md](reference.md#scope-layer-confirmation-details)

### Step 5.5: Plan Discipline
Step 6 の前に `.claude/rules/plan-discipline.md` を Read する。

### Step 6: Record to Plan File

planファイルにTDDコンテキストを記録。テンプレート: [reference.md](reference.md#plan-file-template)

**必須**: planファイル末尾に `## Post-Approve Action` セクションを含めること。これがcompact後のauto-orchestrateトリガーになる。

### Step 7: Continue in Plan Mode

**Step 7.1: Upstream & Constitution Check** — 上流ドキュメント (`ROADMAP.md` 等) と憲法ドキュメントを読み、設計方針との整合性を確認。差異があれば plan の `## Upstream References` に記録。詳細: [reference.md](reference.md#constitution-check)

specの記録後、plan mode内で続行（specスキル範囲外）: 探索（最低5ファイル）→ 設計 → Test List（Given/When/Then）→ QAチェック（カバレッジ・粒度・セキュリティ・独立性）

**Step 7.2: Forced Recall** — 設計で Files to Change が確定した直後（Step 8 の前）に `bash scripts/recall-candidates.sh . <変更予定ファイル...>` を実行し、上位候補を助言者形式で plan の `## Recall` に記録（0 件時は「関連する過去サイクルなし」）。詳細: [reference.md](reference.md#forced-recall)

→ review --plan → Step 8（承認前 Codex plan review）→ approve（ExitPlanMode）→ 自動orchestrate（sync-plan→RED→GREEN→...）

### Step 8: Pre-Approval Plan Review (Codex)

Step 7 後・ExitPlanMode（承認）前: `codex exec --sandbox read-only "review plan <plan path>"` → findings を draft plan へ直接反映 → 最終版を1回だけ再レビュー（resume、フラグ前置。詳細は reference）→ `## Plan Review Record` を plan に記録。未解消 BLOCK は人間の明示 override が承認提示文で必須。Codex 不在時は skip し Record に `codex_unavailable` を記録。詳細: [reference.md](reference.md#step-8-pre-approval-plan-review)

## Reference

Details: [reference.md](reference.md) | Japanese: [reference.ja.md](reference.ja.md)
