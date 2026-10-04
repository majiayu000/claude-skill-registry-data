---
name: knowledge-pr
description: "knowledge/buffer ブランチの差分を Issue 起票 → PR 作成 → auto-merge で main に反映する。/vibecorp:review-harvest / /vibecorp:session-harvest が蓄積した差分を定期的に本番化するためのスキル。「/vibecorp:knowledge-pr」「バッファをPR化して」と言った時に使用。"
---

# 📤 knowledge/buffer → PR 化

> [!IMPORTANT]
> このスキルは `knowledge/buffer` worktree に蓄積された knowledge / rules / docs 差分を **Issue 起票 → PR 作成 → auto-merge** で main に反映する。
> **main への直接 push は一切発生しない**。必ず auto-merge 経由（CI + CodeRabbit レビュー通過後）で反映する。
> open 状態の knowledge-pr Issue があれば skip する（再開は既存 Issue の手動 close 後）。

`knowledge/buffer` worktree に蓄積された knowledge / rules / docs 差分を、Issue 起票 → PR 作成 → `gh pr merge --squash --auto` の流れで main に反映する。

## 📖 使用方法

```bash
/vibecorp:knowledge-pr                    # 通常実行
/vibecorp:knowledge-pr --worktree <path>  # worktree 内で実行（非推奨、通常は呼出元プロジェクト直下で実行）
```

## ⚙️ 前提

- `/vibecorp:review-harvest` または `/vibecorp:session-harvest` が `knowledge/buffer` に commit を積んでいる。
- `gh` が認証済みである。
- main への書込は **必ず** auto-merge 経由（CI + CodeRabbit レビュー通過後）。このスキルが直接 main を変更することは一切ない。

## 🔄 ワークフロー

### 1. buffer worktree の最新化

```bash
. "$CLAUDE_PROJECT_DIR/.claude/lib/knowledge_buffer.sh"
if ! knowledge_buffer_ensure; then
  echo "[knowledge-pr] worktree 準備失敗。skip" >&2
  exit 1
fi
echo "[knowledge-pr] worktree 最新化完了" >&2
BUFFER_DIR="$(knowledge_buffer_worktree_dir)"
```

### 2. 差分有無チェック

```bash
DIFF_COUNT="$(git -C "$BUFFER_DIR" log main..HEAD --oneline | wc -l | tr -d ' ')"
if [ "$DIFF_COUNT" -eq 0 ]; then
  echo "[knowledge-pr] 差分なし。skip"
  exit 0
fi

CHANGE_SUMMARY="$(git -C "$BUFFER_DIR" diff main...HEAD --stat)"
```

### 3. 重複 Issue チェック

open 状態の knowledge-pr Issue があれば skip する（再開は既存 Issue の手動 close 後）。

```bash
EXISTING="$(gh issue list \
  --search "📖 docs: 知見バッファの反映 in:title is:open" \
  --json number,title \
  --jq '.[0].number // empty')"

if [ -n "$EXISTING" ]; then
  echo "[knowledge-pr] 既存 Issue #${EXISTING} が open のため skip" >&2
  echo "[knowledge-pr] 再開するには既存 Issue を手動 close してください" >&2
  exit 0
fi
```

### 4. Issue 起票

`/vibecorp:issue` スキル相当のロジック（ラベル自動判定は CPO チェックを省略、preset 依存は持たない）で Issue を起票する。

```bash
# 変更範囲（コミット範囲を拾ってタイトルに含める）
RANGE="$(git -C "$BUFFER_DIR" log main..HEAD --oneline | wc -l | tr -d ' ') commits"

ISSUE_TITLE="📖 docs: 知見バッファの反映 (${RANGE})"

ISSUE_BODY="$(cat <<EOF
## 概要

\`knowledge/buffer\` ブランチに蓄積された knowledge/rules/docs 差分を main に反映する。

## 変更内容

\`\`\`text
${CHANGE_SUMMARY}
\`\`\`

## コミット履歴

\`\`\`text
$(git -C "$BUFFER_DIR" log main..HEAD --format='- %s' | head -50)
\`\`\`

## 完了条件

- [ ] CodeRabbit レビューを通過する
- [ ] CI が通る
- [ ] auto-merge で main に反映される
EOF
)"

ISSUE_URL="$(gh issue create \
  --title "$ISSUE_TITLE" \
  --body "$ISSUE_BODY" \
  --label documentation)"
ISSUE_NUMBER="$(echo "$ISSUE_URL" | awk -F/ '{print $NF}')"
echo "[knowledge-pr] Issue #${ISSUE_NUMBER} を起票" >&2
```

ラベル `documentation` がリポジトリに存在しない場合は `--label` を省略する（フォールバック）。

### 5. PR 作成

`knowledge/buffer` ブランチを base=main で PR 化する。

```bash
# push が必要な場合先に push（knowledge_buffer_push は exit 3 で失敗検知）
if ! knowledge_buffer_push; then
  echo "[knowledge-pr] push 失敗。Issue #${ISSUE_NUMBER} を手動 close するか次回実行で再試行してください" >&2
  exit 3
fi

PR_TITLE="$ISSUE_TITLE"
PR_BODY="$(cat <<EOF
## 概要

\`knowledge/buffer\` の差分を main に反映する自動 PR。

close #${ISSUE_NUMBER}

## 変更内容

\`\`\`text
${CHANGE_SUMMARY}
\`\`\`

## 自動化ポリシー

- 生成: \`/vibecorp:knowledge-pr\` スキル
- 書込先: \`.claude/knowledge/\`, \`.claude/rules/\`, \`docs/\` のみ
- CodeRabbit レビュー・CI 通過後に GitHub auto-merge が main に反映する
EOF
)"

if ! PR_URL="$(cd "$BUFFER_DIR" && gh pr create \
  --title "$PR_TITLE" \
  --body "$PR_BODY" \
  --base main \
  --head knowledge/buffer)"; then
  echo "[knowledge-pr] PR 作成失敗。Issue #${ISSUE_NUMBER} を手動 close するか次回実行で再試行してください" >&2
  exit 4
fi

PR_NUMBER="$(echo "$PR_URL" | awk -F/ '{print $NF}')"
echo "[knowledge-pr] PR #${PR_NUMBER} を作成" >&2
```

### 6. auto-merge 設定

```bash
if ! (cd "$BUFFER_DIR" && gh pr merge "$PR_NUMBER" --squash --auto); then
  echo "[knowledge-pr] auto-merge 設定失敗。手動で gh pr merge してください" >&2
  exit 5
fi
echo "[knowledge-pr] auto-merge を有効化" >&2
```

### 7. 結果報告（stdout）

```text
## knowledge-pr 結果

- Issue: #${ISSUE_NUMBER}
- PR: #${PR_NUMBER}
- 変更コミット数: ${DIFF_COUNT}
- auto-merge: 設定済み
- 後処理: CodeRabbit + CI 通過後に GitHub が main に反映
```

## 🛟 介入ポイント

以下の状況では人手介入が必要。次回実行では重複チェックで skip されるため、自動では復旧しない。

| 状況 | 復旧手順 |
|---|---|
| push 失敗 (exit 3) | ネットワーク復旧後に `git -C <buffer_dir> push origin knowledge/buffer` |
| PR 作成失敗 (exit 4) | Issue を手動 close、次回 `/vibecorp:knowledge-pr` で再試行 |
| auto-merge 設定失敗 (exit 5) | `gh pr merge <PR番号> --squash` で手動マージ |
| 既存 open Issue あり | 既存 Issue を確認し、不要なら close してから再実行 |

## 🚧 制約

- **main への直接 push は発生しない** — 必ず auto-merge 経由とする。
- knowledge/buffer ブランチは auto-merge 後もそのまま残す（次回 harvest の蓄積先）。
- **jq では string interpolation `\(...)` を使わない** — `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null` / `|| echo` 等のフォールバックを付加しない（明示的にリトライ・タイムアウトが必要な箇所を除く）。
- preset minimal では呼ばれない（install.sh の minimal 引き算で除外）。

## 🔗 関連ルール

- 動作主語ルール: `.claude/rules/communication.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
- 上流スキル（PR レビュー指摘収集）: `/vibecorp:review-harvest`
- 上流スキル（セッション知見吸い上げ）: `/vibecorp:session-harvest`
