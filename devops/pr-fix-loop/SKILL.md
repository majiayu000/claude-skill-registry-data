---
name: pr-fix-loop
description: "PR上の指摘（コメント＋CI失敗）をマージまで修正し続ける。「/pr-fix-loop」「レビュー対応して」「PRレビュー修正して」と言った時に使用。"
---

# 🔁 PR レビュー修正ループ（同期版）

> [!IMPORTANT]
> このスキルは PR を **MERGED / CLOSED に到達するか escalation 条件に当たるまで** teammate のターン内で同期完遂する。
> `CHANGES_REQUESTED` を検知したら `/vibecorp:pr-fix` を **同期呼び出し** して指摘を消化する。
> `/loop` や `ScheduleWakeup` のような非同期スケジューラには依存しない（メッセージ駆動 teammate での放置を防ぐ）。
> 予算ガード: `/vibecorp:pr-fix` 呼び出しは **最大 20 回 / loop**、総時間 **60 分 / loop** で機械的に上限化する。

PR の状態を `gh pr view` でポーリングし、`MERGED` / `CLOSED` に到達するか escalation 条件に当たるまで、teammate のターン内で完遂する。`CHANGES_REQUESTED` を検知したら `/vibecorp:pr-fix` を同期呼び出しして指摘を消化する。

`/loop` や `ScheduleWakeup` のような非同期スケジューラには依存しない。teammate（`/vibecorp:ship-parallel` 配下の Agent）はメッセージ駆動で idle 化すると wakeup が届かないため、そこで PR が放置される構造欠陥を回避する。

## 📖 使用方法

```bash
/vibecorp:pr-fix-loop                    # 現在のブランチの PR を対象に開始
/vibecorp:pr-fix-loop <PR URL>           # PR URL を直接指定
/vibecorp:pr-fix-loop --worktree <path>  # worktree 内で実行
```

## 🌳 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継いで `/vibecorp:pr-fix` を呼ぶ。
- 未指定時は CWD で実行する（後方互換）。

## ⏱️ ループ制御

| 値 | 設定 | 理由 |
|-----|-----|------|
| polling 間隔 | 30 秒 | CodeRabbit / CI 遷移頻度に対して充分 |
| max iterations | 20 | 30 秒 × 20 = 約 10 分。`/vibecorp:pr-fix` 呼び出しが最大 20 回に制限される |
| timeout | 60 分 | fail-safe |

### 💰 予算ガード

このループは `CHANGES_REQUESTED` を検知するたびに `/vibecorp:pr-fix` を同期呼び出しし、各回が Claude API のトークンを消費する。暴走を防ぐため、**iterations と timeout の二重ガード** で API 呼び出し回数と総時間を機械的に上限化する。

| 上限軸 | 値 | 何を抑える |
|--------|-----|-----------|
| `/vibecorp:pr-fix` 同期呼び出し回数 | **20 回 / loop**（max iterations と同値） | LLM 呼び出しコスト |
| 総経過時間 | **60 分 / loop**（timeout と同値） | スタック時の暴走時間 |

`docs/cost-analysis.md` の「自律改善ループの予算ガード」原則（`/vibecorp:diagnose` の `max_issues_per_run` 等が SOT）と同じ思想で、本スキルでも `pr-fix` 呼び出し回数に独立した上限を設ける。両ガード値を変更する場合は本テーブルと「4. 同期ポーリングループ」「5. escalation」の記述を同時に更新する。

## 🔄 ワークフロー

### 1. PR 情報の特定

PR URL が指定されていればそこから owner/repo/PR 番号を抽出する。未指定なら現在のブランチから自動検出する。

```bash
gh pr view --json number,url,headRefName,baseRefName --jq '{number, url, headRefName, baseRefName}'
```

PR が見つからなければ「PR 未作成のため `/vibecorp:pr` を先に実行してください」と報告して終了する。

### 2. CodeRabbit 有効性の確認

```bash
awk '/^coderabbit:/{found=1; next} found && /^[^ ]/{exit} found && /enabled:/{print $2}' \
  "$CLAUDE_PROJECT_DIR"/.claude/vibecorp.yml
```

- `false` の場合は CodeRabbit レビュー待ちをスキップし、ステップ 4（auto-merge 設定）から実行して終了する。
- `true` または未定義（空）の場合はステップ 3 へ進む。

### 3. auto-merge 設定（冪等）

`autoMergeRequest` が未設定なら設定する。既設定ならスキップする。

```bash
gh pr view <pr_number> --json autoMergeRequest --jq '.autoMergeRequest'
gh pr merge <pr_number> --squash --auto
```

### 4. 同期ポーリングループ

`MERGED` / `CLOSED` か escalation 条件に到達するまで、以下を最大 20 反復・60 分以内で繰り返す。

各反復の先頭で PR 状態を一括取得する。

```bash
gh pr view <pr_number> \
  --json state,mergeStateStatus,reviewDecision,autoMergeRequest \
  --jq '{state, mergeStateStatus, reviewDecision, autoMergeRequest}'
```

#### 🗺️ 状態遷移表

| state | reviewDecision | mergeStateStatus | 行動 |
|-------|----------------|-------------------|------|
| MERGED | – | – | **成功終了** |
| CLOSED | – | – | 「PR がクローズされました」と報告して**正常終了** |
| OPEN | CHANGES_REQUESTED | – | `/vibecorp:pr-fix` を同期呼び出し → `sleep 30` → 次反復 |
| OPEN | – | CLEAN | auto-merge 発動待ち（`sleep 30` → 次反復） |
| OPEN | – | BLOCKED / BEHIND / UNSTABLE / UNKNOWN / HAS_HOOKS | CI / approve 待ち（`sleep 30` → 次反復） |
| OPEN | – | DIRTY | **escalate**（マージコンフリクト発生） |
| OPEN | – | DRAFT | **escalate**（Draft PR は対象外） |

#### CHANGES_REQUESTED 時の処理

1. `/vibecorp:pr-fix`（worktree モードでは `--worktree <path>` を引き継ぐ）を Skill ツールで同期呼び出しする。
2. `/vibecorp:pr-fix` が rate limit 停止を返した場合は escalate する。
3. 完了後 `sleep 30` で CodeRabbit 再レビューを待つ。
4. 次反復で再度 `gh pr view` を行う。

#### iterations / timeout 制御

各反復の先頭で経過時間と反復回数を確認する。

- 反復数が 20 を超えた場合 → escalate する。
- 開始から 60 分（3600 秒）を超えた場合 → escalate する。

### 5. escalation

以下のいずれかが満たされたら escalation する。

- max iterations（20）到達。
- timeout（60 分）到達。
- `mergeStateStatus == DIRTY`。
- `mergeStateStatus == DRAFT`。
- `/vibecorp:pr-fix` が rate limit 停止を返した。
- `/vibecorp:pr-fix` が外部要因 CI 失敗を検知した。

#### teammate 配下の場合（SendMessage が利用可能）

`SendMessage` ツールが使える場合は teammate と判断し、team-lead に escalation を送る。

```text
to: team-lead
message: "PR #<番号> で /vibecorp:pr-fix-loop が <理由> により escalation。状態: <state/mergeStateStatus/reviewDecision> 反復: <n>"
```

#### main session の場合（SendMessage が利用不可）

標準出力に escalation 内容を表示して終了する。

### 6. 結果報告

```text
## /vibecorp:pr-fix-loop 完了

- PR: #<pr_number>
- 結果: MERGED / CLOSED / escalated（理由）
- 反復回数: <n>
- 経過時間: <分>
- /vibecorp:pr-fix 呼び出し回数: <n>
```

## ⚠️ 制約

- `--force`、`--hard`、`--no-verify` は使用しない。
- ユーザーの明示的な指示なしに force push しない。
- **jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する（[根拠](docs/design-philosophy.md#jq-string-interpolation-の禁止)）。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- **Bash は 1 コマンド 1 呼び出しに分割する** — `cd ... && cmd | head 2>/dev/null` のように cd + パイプ + リダイレクトを含む compound command は Claude Code 本体の built-in security check で止められる（参照: #258）。
- **`/loop` や `ScheduleWakeup` を使わない** — このスキルは teammate のターン内で同期完遂することが要件（[根拠](docs/ai-review-dependency.md#4-契約--ツール-責任分担表)）。

## 🔗 関連ルール

- PR 単発修正スキル: `/vibecorp:pr-fix`
- PR 作成スキル: `/vibecorp:pr`
- レビュー観点（intent 別）: `.claude/rules/review-observations.md`
- 捌き基準（intent × severity）: `.claude/rules/review-handling.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
