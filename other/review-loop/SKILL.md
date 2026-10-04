---
name: review-loop
description: "レビュー→検証→修正の自動ループ。問題 0 件まで繰り返す。「/vibecorp:review-loop」「レビューして直して」と言った時に使用。"
---

# 🔁 review-loop: レビュー→検証→修正の自動ループ

> [!IMPORTANT]
> 変更差分に対してレビュー→検証→計画→修正のループを **問題 0 件になるまで** 繰り返す。
> **最大 5 回でループを打ち切る**（無限ループ防止）。上限到達時はコミットせず未解決の指摘一覧を報告する。
> 合議制は **full プリセット** かつ **差分キーワードヒット** 時のみ起動する（standard 以下では起動しない）。

**ultrathink**

変更差分に対してレビュー→検証→計画→修正のループを実行する。

## 🌿 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継ぐ。
- 未指定時は従来通り CWD で実行する（後方互換）。

## 🔄 ループフロー

以下を問題が 0 件になるまで繰り返す。**最大 5 回でループを打ち切る。上限到達時はコミットせず、未解決の指摘一覧を報告してユーザーに判断を委ねる。**

### 1. レビュー実行

`/vibecorp:review` を実行してレビュー結果を取得する（worktree モードでは `--worktree <path>` を引き継ぐ）。

### 1b. 合議制レビュー（full プリセット限定）

`.claude/vibecorp.yml` の `preset: full` の場合、コード差分が特定領域に触れていれば、**平社員合議制（×3 独立実行）+ C*O メタレビュー** を追加で実行する。

`/vibecorp:review`（CodeRabbit CLI を含む）の **置き換えではなく追加レイヤーとして動作する**。

- **`/vibecorp:review`**: 汎用バグ検出・コード品質・ベストプラクティス
- **合議制**: プロジェクト固有ポリシー遵守（`SECURITY.md` / `POLICY.md` / `cost-analysis.md` の MUST / MUST NOT）

両者が同じ観点を指摘した場合、次ステップ「2. 妥当性検証」で `.claude/rules/review-handling.md`（捌き基準）と `.claude/rules/severity/claude-action.md`（severity 定義）に基づき重複排除する。

#### 起動条件

```bash
# preset 取得
preset=$(awk '/^preset:/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml)
```

- `preset` が `full` 以外（minimal / standard / 未定義）の場合、このステップ全体をスキップする（既存挙動を維持）。
- `preset: full` の場合、以下の差分検出に進む。

#### 差分ベーストリガー表

`git diff main...HEAD -U0` の出力に対して以下のキーワードを case-insensitive で検索し、ヒットした領域のみ起動する（複数該当時は該当全 C*O を並列起動）。

| 領域 | diff 内キーワード | 起動 C*O | 平社員合議 |
|---|---|---|---|
| 課金影響 | `API call`, `model:`, `claude -p`, `ANTHROPIC_API_KEY`, `rate limit`, `従量`, `トークン消費`, `npx`, `bunx` | CFO | accounting-analyst×3 |
| セキュリティ | `auth`, `token`, `secret`, `encrypt`, `permission`, `credential`, `curl`, `wget`, `eval`, `exec` | CISO | security-analyst×3 |
| 法務 | `dependency`, `LICENSE`, `third-party`, `規約`, `プライバシー`, `第三者`, `package.json`, `requirements.txt`, `go.mod` | CLO | legal-analyst×3 |

検出例:

```bash
git diff main...HEAD -U0 | grep -iE 'auth|token|secret|encrypt|permission|credential|curl|wget|eval|exec'
```

ヒットなしなら合議制はスキップする（既存挙動を維持）。

#### 平社員 ×3 起動

該当領域の analyst を Agent tool で **同一プロンプト・独立に 3 回** 同時並列で起動する（必須）。

複数領域が該当した場合、各領域の analyst×3 と対応する C*O を同時並列で起動する（例: 課金 + セキュリティなら accounting-analyst×3 + CFO と security-analyst×3 + CISO を並列実行）。

- 課金影響 → `.claude/agents/accounting-analyst.md` を ×3
- セキュリティ → `.claude/agents/security-analyst.md` を ×3
- 法務 → `.claude/agents/legal-analyst.md` を ×3

各 analyst に渡すプロンプトは `skills/review-loop/prompts/agent-call-review-analyst.md` を参照する。

#### C*O メタレビュー

3 件の独立結果を対応 C*O がメタレビューする（1 回）。

- 課金 → `.claude/agents/cfo.md`
- セキュリティ → `.claude/agents/ciso.md`
- 法務 → `.claude/agents/clo.md`

メタレビュー観点:

- 3 件の独立結果で **共通する指摘** を抽出する（重要）。
- 1 件だけの指摘は「偽陽性の可能性」として慎重に扱う。
- 全会一致ルール（CISO / CLO）: 1 人でも Major 以上を検出したら止める。
- 多数決ルール（CFO）: 2/3 以上の指摘を採用する。

#### PR コメント投稿（Major 以上のみ）

C*O メタレビューの結論が **Major 以上** のとき、対応 C*O が PR にコメント投稿する。

- PR が未作成（push 前）なら stdout に出力のみとする。
- Major 未満（Info / Trivial）はスキップする。
- 判定基準は `.claude/rules/review-handling.md`（捌き基準）と `.claude/rules/severity/claude-action.md`（severity 定義）に準拠する。

重複防止のため、マーカー `[<C*O>-consensus-review]`（例: `[CFO-consensus-review]`）で既存コメントを検索して upsert する。

```bash
# owner/repo を取得
repo=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

pr_num=$(gh pr view --json number --jq '.number')
marker="[CFO-consensus-review]"  # C*O に応じて変える
existing_id=$(gh api "repos/${repo}/issues/${pr_num}/comments" --paginate \
  --jq '.[] | select(.body | startswith("'"$marker"'")) | .id' | head -1)

if [ -n "$existing_id" ]; then
  gh api --method PATCH "repos/${repo}/issues/comments/${existing_id}" \
    -f body="${marker}"$'\n\n'"${summary}"
else
  gh pr comment "${pr_num}" --body "${marker}"$'\n\n'"${summary}"
fi
```

### 1c. intent ラベルの取得（Issue 側から直接参照）

レビュー判定（intent × severity）の SoT は **Issue ラベル**。PR には intent ラベルを付与しないため（Issue #575）、Issue 番号を解決して `gh issue view --json labels` で intent を取得する。

**4 段フォールバック**:

| 優先 | 取得経路 | コマンド例 |
|---|---|---|
| 1 | `closingIssuesReferences`（PR 作成後のみ） | `gh pr view --json closingIssuesReferences --jq '.closingIssuesReferences[0].number // empty'` |
| 2 | PR 本文 grep（PR 作成後のみ） | `pr-issue-link-check.yml` 互換正規表現 `(close[sd]?\|fix(es\|ed)?\|resolve[sd]?\|refs?)[[:space:]]+#([0-9]+)` で PR 本文を解析。最初のマッチを採用 |
| 3 | ブランチ名（PR 未作成時はここから開始） | `git branch --show-current` から `dev/<num>_*` パターンの `<num>` 抽出 |
| 4 | 空（severity-only fallback） | warning ログ + severity-only 判定モードに切替 |

```bash
# PR 作成後: closingIssuesReferences → PR 本文 → ブランチ名
# PR 未作成（push 前）: ブランチ名から直接

# PR 番号取得（無ければ空、stderr ノイズは無害）
PR_NUM=$(gh pr view --json number --jq '.number // empty')
ISSUE_NUM=""

if [ -n "$PR_NUM" ]; then
  ISSUE_NUM=$(gh pr view "$PR_NUM" --json closingIssuesReferences --jq '.closingIssuesReferences[0].number // empty')
  if [ -z "$ISSUE_NUM" ]; then
    PR_BODY=$(gh pr view "$PR_NUM" --json body --jq '.body')
    # #N 形式 + GitHub URL 形式の両対応（pr-issue-link-check.yml と互換）
    ISSUE_NUM=$(printf '%s' "$PR_BODY" \
      | grep -oiE '(close[sd]?|fix(es|ed)?|resolve[sd]?|refs?)[[:space:]]+(#[0-9]+|https?://[^[:space:]]+/issues/[0-9]+)' \
      | head -1 \
      | grep -oE '[0-9]+$')
  fi
fi

if [ -z "$ISSUE_NUM" ]; then
  BRANCH=$(git branch --show-current)
  ISSUE_NUM=$(printf '%s' "$BRANCH" | grep -oE '^dev/([0-9]+)_' | grep -oE '[0-9]+')
fi

# 数値検証を経た上でのみ gh に渡す
PR_INTENT=""
if [ -n "$ISSUE_NUM" ]; then
  if [[ "$ISSUE_NUM" =~ ^[0-9]+$ ]]; then
    PR_INTENT=$(gh issue view "$ISSUE_NUM" --json labels --jq '[.labels[].name | select(startswith("intent/"))][0] // empty')
  else
    echo "[WARN] ISSUE_NUM が数値以外（'$ISSUE_NUM'）。intent 取得をスキップして severity-only fallback に切替" >&2
  fi
fi
```

**severity-only fallback の挙動**:

Issue 番号 / intent ラベルが解決できない場合、`PR_INTENT` が空となる。この場合は intent 重視軸判定が不可能となるため、`.claude/rules/review-handling.md` の判定基準を **severity のみで** 適用する。

- **Critical / Major**: 通常通り修正対象（intent 問わず必ず対応）。
- **Minor / Trivial / Info**: 全スキップ（intent 重視軸該当判定が不能のため保守的に倒す）。

warning ログ `[WARN] Issue 番号 / intent ラベルが解決できませんでした。severity-only fallback で Critical / Major のみ修正対象とします` を出力する。

### 2. 妥当性検証

`.claude/rules/review-handling.md`（intent × severity の捌き基準）と `.claude/rules/severity/claude-action.md` / `.claude/rules/severity/coderabbit.md`（severity 定義）に従い、`/vibecorp:review` と合議制（full プリセット時）の両方の指摘を統合して分類する。判定の入力としては **1c で取得した `PR_INTENT`** を使う（PR ラベルではなく Issue ラベル直接参照）。

- 同一観点の重複は 1 件にまとめる（出典は両方を残す）。
- Critical / Major は intent 問わず必ず対応、Minor / Trivial / Info は intent の重視軸該当時のみ対応する。
- `PR_INTENT` が空（severity-only fallback）の場合は Minor 以下を全スキップする。

#### 出力形式

```text
## 修正すべき指摘

1. [ファイルパス:行番号] 指摘内容の要約（出典: /vibecorp:review, CFO-consensus）
2. ...

## 却下した指摘

1. [指摘内容の要約] — 却下理由
2. ...
```

**要修正 0 件ならループ終了。**

### 3. 修正計画

要修正リストに対して、各指摘の具体的な修正計画を策定する。**このステップではコードの変更は行わない。**

手順:

1. 指摘箇所の実コードと周辺コードを読む。
2. 既存の類似実装パターンを確認する。
3. 修正による影響範囲を特定する。
4. 具体的な修正手順を策定する。

#### 出力形式

```text
## 修正計画

### 1. [ファイルパス:行番号] 指摘内容の要約

- **修正内容**: 何をどう変更するか
- **影響範囲**: 変更が影響する他のファイル・テスト
- **注意点**: 修正時に気をつけるべきこと
```

### 4. 修正実行

修正計画に従ってコードを修正する。

- **計画に記載された範囲のみを変更する**（計画外の変更は行わない）。
- 修正後、関連するテスト・lint を実行して通過を確認する。

#### 出力形式

```text
## 修正内容

1. [ファイルパス] 修正内容の要約
2. ...

## テスト結果

- {テスト名}: PASS/FAIL
```

### 5. レビュー完了スタンプの生成

ループが問題 0 件で正常終了した場合、PR 作成を許可するスタンプを生成する。スタンプは `~/.cache/vibecorp/state/<repo-id>/` 配下に作成される（`.claude/` 配下への書込確認プロンプトを回避）。

```bash
. "$CLAUDE_PROJECT_DIR/.claude/lib/common.sh"
STAMP_DIR="$(vibecorp_stamp_mkdir)"
touch "${STAMP_DIR}/review-ok"
```

worktree モードの場合:

```bash
. "<path>/.claude/lib/common.sh"
STAMP_DIR="$(vibecorp_stamp_mkdir)"
touch "${STAMP_DIR}/review-ok"
```

**上限到達で打ち切った場合はスタンプを生成しない。**

### 6. 結果報告（ループ終了後）

全イテレーションの結果をまとめて報告する。

```text
## review-loop 結果

### レビューモード
- preset: {minimal/standard/full}
- 合議制: {起動/スキップ} （full プリセット時のみ判定）
- 起動 C*O: {CFO / CISO / CLO}（起動時のみ）

### 修正した指摘
- {ファイル:行番号}: {指摘内容} → {修正内容}（出典: /vibecorp:review / {C*O}-consensus）

### 却下した指摘
- {指摘内容} — 理由: {却下理由}

### サマリ
- ループ回数: {n}回
- 修正: {n}件
- 却下: {n}件
- 最終レビュー: 問題0件
```

## 🚧 制約

- `--force`、`--hard`、`--no-verify` は使用しない。
- `git add` / `git commit` / `git push` は実行しない（呼び出し元に委ねる）。
- 最大 5 回でループを打ち切る（無限ループ防止）。
- 修正前に必ず関連ファイルを読み込む。
- 合議制は **full プリセット** かつ **差分キーワードヒット** 時のみ起動する（standard 以下では起動しない）。
