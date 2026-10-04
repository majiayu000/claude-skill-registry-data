---
name: cycle-metrics
description: >
  Issue サイクル（/ship 1回）の所要時間・トークン量・ボトルネックを実測する。
  PR タイミングと Claude Code セッションログから集計し、
  `~/.cache/vibecorp/state/<repo-id>/cycle-metrics/YYYY-MM-DD.md` に保存する（揮発データ）。full プリセット限定。
  「/cycle-metrics」「サイクル計測」と言った時に使用。
---

# 📊 Issue サイクル実測

> [!IMPORTANT]
> このスキルは直近 N 回の Issue サイクル（`/ship` 1 回 = PR 1 本）の **所要時間・トークン量・各エージェント呼び出し** を実測する。
> **データ生成専用** であり、Critical/Major 等の判断や Issue 起票は行わない（CFO `/audit-cost` 側の責務）。
> **ヘッドレス Claude（`claude -p` / `npx` / `bunx`）を一切伴わない**。計測自体が課金を発生させると本末転倒。

直近 N 回の Issue サイクルについて所要時間・トークン量・各エージェント呼び出しを実測し、改善判断のためのデータを生成する。**full プリセット専用**。

## 📋 前提条件

| 項目 | 条件 |
|---|---|
| プリセット | **full プリセット専用**（`/audit-cost` と同等のスコープ） |
| 認証 | `gh` CLI が認証済み |
| ログ | `~/.claude/projects/<slug>/*.jsonl`（Claude Code セッションログ）が存在 |
| テンプレ | `knowledge/accounting/cycle-metrics-template.md` が配置済み |

## 🚫 ヘッドレス Claude 起動禁止（MUST）

本スキルおよび配下スクリプトは **ヘッドレス Claude（`claude -p` / `npx` / `bunx` 経由の LLM 呼び出し）を一切伴わない**。

- 根拠: `.claude/rules/autonomous-restrictions.md` 第 3 項（課金構造）。計測自体が課金を発生させると本末転倒。
- データ取得は `gh` API（PR timeline / check runs）と Claude Code セッション JSONL の静的読み取りのみ。
- `tests/test_cycle_metrics.sh` で全スクリプトに対する文字列検査を実施し、違反を CI で検出する。

## 🔄 ワークフロー

### 1. プリセット確認

```bash
awk '/^preset:[[:space:]]*/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml
```

`full` 以外の場合は「/vibecorp:cycle-metrics は full プリセット専用です」と報告して終了する。

### 2. PR メトリクス収集

`gh pr list` でマージ済み PR の直近 N 件（デフォルト 20 件）を取得し、PR 単位の所要時間・レビュー時間・CI 時間を JSON で出力する。

```bash
bash skills/cycle-metrics/fetch-pr-metrics.sh --limit 20 > /tmp/cycle-pr.json
```

出力フィールド:

| フィールド | 内容 |
|---|---|
| `number` | PR 番号 |
| `issue_number` | ブランチ名から抽出した Issue 番号（`dev/{番号}_*`） |
| `created_at` / `merged_at` | ISO8601 |
| `total_seconds` | マージまでの総所要時間 |
| `first_review_seconds` | 最初のレビューまでの時間（無い場合は `null`） |
| `ci_seconds` | CI 完了までの所要時間（statusCheckRollup ベース） |
| `additions` / `deletions` | 差分量 |

日付計算は `jq 'fromdateiso8601'` を使用し、`date -d`（GNU 固有）は使わない。

### 3. Agent メトリクス収集

`~/.claude/projects/<slug>/*.jsonl` から、ブランチ単位（`gitBranch == "dev/{Issue番号}_*"`）でセッションを抽出し、トークン量と sidechain 呼び出し回数を集計する。

```bash
bash skills/cycle-metrics/fetch-agent-metrics.sh --since "30 days ago" > /tmp/cycle-agent.json
```

出力フィールド:

| フィールド | 内容 |
|---|---|
| `branch` | 集計対象のブランチ名 |
| `issue_number` | ブランチ名から抽出した Issue 番号 |
| `total_input_tokens` / `total_output_tokens` / `total_cache_creation_tokens` / `total_cache_read_tokens` | トークン内訳 |
| `models` | モデル別集計 |
| `sidechain_count` | サブエージェント呼び出し回数（`isSidechain == true` のメッセージ数） |
| `subagent_types` | `Agent` tool_use の `subagent_type` 別呼び出し回数 |
| `session_count` | 関連セッション数 |

エージェント別の正確な紐付け（sidechain と subagent_type の対応）は best-effort で実装する。

### 4. レポート生成（揮発データ → ~/.cache/）

PR と Agent の JSON を読み込んで Markdown レポートを生成する。出力先は **`~/.cache/vibecorp/state/<repo-id>/cycle-metrics/`** の揮発データ領域（`.claude/knowledge/` には書かない）。

```bash
. "${CLAUDE_PROJECT_DIR:-.}/.claude/lib/common.sh"
today=$(date -u +%Y-%m-%d)
state_dir="$(vibecorp_state_dir)"
mkdir -p "${state_dir}/cycle-metrics"
out="${state_dir}/cycle-metrics/${today}.md"
bash skills/cycle-metrics/generate-report.sh /tmp/cycle-pr.json /tmp/cycle-agent.json "$out"
```

レポートは `cycle-metrics-template.md` の雛形を埋める形で出力する（テンプレート読取先は `.claude/knowledge/accounting/cycle-metrics-template.md` のまま、出力先のみ `~/.cache/` に変更）。

### 5. 結果報告

```text
## /vibecorp:cycle-metrics 完了

### 集計範囲
- PR: 直近 N 件（マージ済み）
- セッション: 直近 30 日間

### サマリ
- 平均サイクル時間: X 時間
- 最長フェーズ: {フェーズ名} (Y 時間)
- 総トークン消費: Z（input / output / cache 内訳）

### 出力
- レポート: ~/.cache/vibecorp/state/<repo-id>/cycle-metrics/YYYY-MM-DD.md
```

## 🤝 CFO 監査との関係

本スキルの出力は CFO が `/audit-cost` 監査時に **データ源** として参照する。ファイル名で責務を区別する。

| ファイル | 場所 | 担当 | 内容 |
|---|---|---|---|
| `audit-log/YYYY-QN.md` | `.claude/knowledge/accounting/` | CFO（`/audit-cost`） | 監査判断（Critical/Major、Issue 起票要否） |
| `cycle-metrics/YYYY-MM-DD.md` | `~/.cache/vibecorp/state/<repo-id>/` | `/cycle-metrics` | 実測データのみ（判断ロジックなし、揮発） |

## ⚠️ 制約

- **コード変更を一切行わない** — レポート保存と stdout 出力のみ。
- **ヘッドレス Claude 起動禁止** — 上記 MUST 節を参照。
- **判断ロジックを含めない** — Critical / Major の付与、Issue 起票は CFO の `/audit-cost` 側の責務。
- `git add` / `git commit` / `git push` は実行しない。
- `--force`、`--hard`、`--no-verify` は使用しない。
- **jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない。
- `date -d`（GNU 固有）を使わない — `jq 'fromdateiso8601'` で BSD/GNU 両対応にする。

## 🗂️ buffer worktree / .claude/knowledge/ への保存はしない

本スキルの出力 `cycle-metrics/YYYY-MM-DD.md` は **揮発データ** であり、`~/.cache/vibecorp/state/<repo-id>/cycle-metrics/` 配下に保存する。`.claude/knowledge/` にも `knowledge/buffer` にも載せない（Issue #442 で確定した方針）。

理由:

- 揮発データを git 履歴に永続化する設計誤りを避ける（Issue #442 の三領域分離方針）。
- 監査判断（buffer 化対象）は `audit-log/YYYY-QN.md` 側に集約され、`cycle-metrics/` は同日中に CFO が消費する一過性データのため。
- `protect-knowledge-direct-writes.sh` フックの deny パターン（`*/audit-log/*`）に該当しない（出力先が `.claude/knowledge/` 外）。

CFO 監査結果（`audit-log/YYYY-QN.md`）は `/audit-cost` が `${BUFFER_DIR}/.claude/knowledge/accounting/audit-log/` 経由で buffer に保存し、`/vibecorp:knowledge-pr` で main に反映される。

## 🔗 関連ルール

- 自律実行不可領域: `.claude/rules/autonomous-restrictions.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
