---
name: pr-fix
description: "PRの未解決コメントを1回修正してpushする。定期実行は /pr-fix-loop を使う。「/pr-fix」「コメント直して」と言った時に使用。"
---

# 🐇 PR レビュー修正（単発）

> [!IMPORTANT]
> このスキルは PR の **未解決コメント + CI 失敗** を 1 回だけ修正して push する。
> **定期実行は `/vibecorp:pr-fix-loop` を使う**（本スキルはループしない）。
> レビュー判定の SoT は **Issue ラベル**（PR ラベルではない、Issue #575）。intent は `gh issue view --json labels` で直接参照する。
> 4 段フォールバックで Issue 番号を解決できない場合は **severity-only fallback**（Critical / Major のみ修正、Minor 以下はスキップ）に切替える。

PR の現在の状態を確認し、未解決コメントがあれば修正して push する。1 回の実行で現在の指摘を処理して終了する。

## 📖 使用方法

```bash
/vibecorp:pr-fix                    # 現在のブランチのPRを自動検出
/vibecorp:pr-fix <PR URL>           # PR URLを直接指定
/vibecorp:pr-fix --worktree <path>  # worktree 内で実行
```

## 🌳 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継ぐ。
- 未指定時は従来通り CWD で実行する（後方互換）。
- **`$CLAUDE_PROJECT_DIR`**: worktree モードでは `<path>` に置き換える。

## ✅ 前提条件

- PR が既に作成されていること（未作成なら `/vibecorp:pr` を先に実行する）。
- 現在のブランチが PR の head ブランチであること。

## 🔄 ワークフロー

### 1. PR 情報を取得

**PR URL が指定された場合**: URL から owner/repo/PR 番号を抽出する。

**PR URL が未指定の場合**: 現在のブランチから自動検出する。

```bash
gh pr view --json number,url,headRefName,baseRefName,state --jq '{number, url, headRefName, baseRefName, state}'
```

PR が見つからない場合はエラー。

### 2. マージ済みチェック

```bash
gh pr view {pr_number} --json state --jq '.state'
```

- `MERGED` → 「PR #{pr_number} はマージ済みです」と報告して **正常終了**。
- `CLOSED` → 「PR #{pr_number} はクローズされています」と報告して **正常終了**。
- `OPEN` → ステップ 2.5 へ進む。

### 2.5. CI ステータスの取得

```bash
gh pr view {pr_number} --json statusCheckRollup --jq '.statusCheckRollup[] | {name, status, conclusion, detailsUrl}'
```

#### CI 状態の分類

| conclusion | 分類 | 行動 |
|---|---|---|
| `SUCCESS`, `NEUTRAL`, `SKIPPED` | CI green | 修正不要 |
| `FAILURE`, `CANCELLED`, `TIMED_OUT`, `ACTION_REQUIRED` | CI 失敗 | 修正対象 |
| `null`（`status` が `IN_PROGRESS` / `QUEUED`） | CI 待機（PENDING） | 修正対象外、次イテレーション待ち |

#### CI 失敗時のログ取得

CI 失敗が 1 件以上ある場合、`detailsUrl` から `run_id` を抽出し、失敗ジョブのログを取得する。

```bash
# detailsUrl 例: https://github.com/{owner}/{repo}/actions/runs/{run_id}/jobs/{job_id}
# run_id の抽出: detailsUrl の /runs/ と /jobs/ の間のセグメント
gh run view {run_id} --log-failed
```

末尾 200 行程度に絞り込んで修正コンテキストに渡す。

#### 外部要因 CI 失敗の判定

ログに以下のキーワードが含まれる場合は外部要因と判定し、CEO にエスカレーションして **停止する**。

`Rate limit`, `429`, `ECONNREFUSED`, `network is unreachable`, `could not resolve host`, `npm install failed`, `ETIMEDOUT`, `ENOTFOUND`, `socket hang up`

外部要因と判定した場合:

- 「CI 失敗は外部要因（{キーワード}）のため、リポジトリ側の修正では解消できません」と報告して **停止する**。

#### CI green 判定

全 check run の `conclusion` が `SUCCESS` / `NEUTRAL` / `SKIPPED` のいずれかで、かつ PENDING が 0 件の場合に CI green と判定する。

### 3. CodeRabbit 有効性の確認

```bash
awk '/^coderabbit:/{found=1; next} found && /^[^ ]/{exit} found && /enabled:/{print $2}' \
  "$CLAUDE_PROJECT_DIR"/.claude/vibecorp.yml
```

- 結果が `false` → **CodeRabbit 無効。ステップ 7（auto-merge 確認）へ直接進む**。
- 結果が `true` または空（未定義）→ CodeRabbit 有効。ステップ 4 へ進む。

### 4. rate limit チェック

```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments \
  --paginate \
  --jq '[.[] | select(.user.login | test("coderabbit"; "i")) | select(.body | test("[Rr]ate limit"))] | length'
```

1 以上なら「CodeRabbit が rate limit 中のため停止しています。rate limit 解除後に再実行してください」と報告して **停止する**。

### 5. 未解決スレッドの取得

GraphQL API で未解決の CodeRabbit レビュースレッドを取得する。レビュースレッドが 100 件を超える PR では 1 ページだけ取ると見落とすため、`pageInfo.hasNextPage` で全ページを巡回する。

```bash
threads_all="[]"
cursor=""
while :; do
  if [ -n "$cursor" ]; then
    after_arg="-f after=$cursor"
  else
    after_arg=""
  fi
  page="$(gh api graphql \
    -f owner="{owner}" \
    -f repo="{repo}" \
    -F number={pr_number} \
    $after_arg \
    -f query='
      query($owner: String!, $repo: String!, $number: Int!, $after: String) {
        repository(owner: $owner, name: $repo) {
          pullRequest(number: $number) {
            reviewThreads(first: 100, after: $after) {
              pageInfo { hasNextPage endCursor }
              nodes {
                isResolved
                id
                comments(first: 10) {
                  nodes {
                    id
                    databaseId
                    author { login }
                    body
                    path
                    line
                  }
                }
              }
            }
          }
        }
      }')"
  page_nodes="$(printf '%s' "$page" | jq '.data.repository.pullRequest.reviewThreads.nodes')"
  threads_all="$(jq -s 'add' <(printf '%s' "$threads_all") <(printf '%s' "$page_nodes"))"
  has_next="$(printf '%s' "$page" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')"
  if [ "$has_next" != "true" ]; then
    break
  fi
  cursor="$(printf '%s' "$page" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')"
done

# 未解決 + 先頭コメントが CodeRabbit のスレッドのみ抽出
unresolved="$(printf '%s' "$threads_all" \
  | jq '[.[] | select(.isResolved == false)
    | select(.comments.nodes[0].author.login | test("coderabbit"; "i"))]')"
```

- `isResolved == false` かつ先頭コメントが CodeRabbit のスレッドのみ抽出する。
- 各スレッドの `id`（thread node ID）は却下時の resolve mutation で使用する。
- ページネーションにより 100 件を超えるレビュースレッドも漏れなく取得する。

**未解決 0 件 かつ CI 失敗 0 件（PENDING 残存は許容）→ 「対応不要」と報告して正常終了する。**
**未解決あり または CI 失敗あり → ステップ 6 へ進む。**

### 6. 指摘の修正

#### 6.0 intent ラベルの取得（Issue 側から直接参照）

レビュー判定（intent × severity）の SoT は **Issue ラベル**。PR には intent ラベルを付与しないため（Issue #575）、Issue 番号を解決して `gh issue view --json labels` で intent を取得する。

**4 段フォールバック**:

| 優先 | 取得経路 | コマンド例 |
|---|---|---|
| 1 | `closingIssuesReferences`（GitHub 自動 close キーワード由来） | `gh pr view {pr_number} --json closingIssuesReferences --jq '.closingIssuesReferences[0].number // empty'` |
| 2 | PR 本文 grep（`--ref` 経由 PR / 手動編集対応） | `pr-issue-link-check.yml` 互換正規表現 `(close[sd]?\|fix(es\|ed)?\|resolve[sd]?\|refs?)[[:space:]]+#([0-9]+)` で PR 本文を解析。最初のマッチを採用 |
| 3 | ブランチ名 | `dev/<num>_*` パターンから `<num>` 抽出（`gh pr view --json headRefName --jq '.headRefName'`）|
| 4 | 空（severity-only fallback） | warning ログ + severity-only 判定モードに切替 |

```bash
# Step 1: closingIssuesReferences（実機検証済み: フラット配列、nodes ラッパー無し）
ISSUE_NUM=$(gh pr view {pr_number} --json closingIssuesReferences --jq '.closingIssuesReferences[0].number // empty')

# Step 2: PR 本文 grep（#N 形式 + GitHub URL 形式の両対応、pr-issue-link-check.yml と互換）
if [ -z "$ISSUE_NUM" ]; then
  PR_BODY=$(gh pr view {pr_number} --json body --jq '.body')
  ISSUE_NUM=$(printf '%s' "$PR_BODY" \
    | grep -oiE '(close[sd]?|fix(es|ed)?|resolve[sd]?|refs?)[[:space:]]+(#[0-9]+|https?://[^[:space:]]+/issues/[0-9]+)' \
    | head -1 \
    | grep -oE '[0-9]+$')
fi

# Step 3: ブランチ名
if [ -z "$ISSUE_NUM" ]; then
  HEAD_REF=$(gh pr view {pr_number} --json headRefName --jq '.headRefName')
  ISSUE_NUM=$(printf '%s' "$HEAD_REF" | grep -oE '^dev/([0-9]+)_' | grep -oE '[0-9]+')
fi

# Step 4: intent ラベル取得（ISSUE_NUM の数値検証を実施した上で gh に渡す）
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

Step 1-3 で Issue 番号を解決できない、または Issue に intent ラベルが付いていない場合、`PR_INTENT` が空となる。この場合は intent 重視軸判定が不可能となるため、`.claude/rules/review-handling.md` の判定基準を **severity のみで** 適用する。

- **Critical / Major**: 通常通り修正対象（intent 問わず必ず対応）。
- **Minor / Trivial / Info（Minor 以下）**: 全スキップ（intent 重視軸該当判定が不能のため保守的に倒す）。

warning ログ `[WARN] Issue 番号 / intent ラベルが解決できませんでした。severity-only fallback で Critical / Major のみ修正対象とします` を出力する。

**複数 Issue close PR の優先順位**: 1 PR で複数 Issue を close する場合、`closingIssuesReferences[0]` が採用される（GitHub 仕様順）。1 PR 1 Issue 運用が `pr-issue-link-check.yml` で前提化されているため実運用上稀。

#### 6.1 妥当性検証

`.claude/rules/review-handling.md` の捌き基準（intent × severity）と `.claude/rules/severity/claude-action.md` / `severity/coderabbit.md` の severity 定義に従い、指摘を分類する。判定の入力としては **6.0 で取得した `PR_INTENT`** を使う（PR ラベルではなく Issue ラベル直接参照）。設計方針に関わる大きな変更はユーザーに確認する。

#### 6.2 修正計画

要修正リストに対して、各指摘の具体的な修正計画を策定する。**このステップではコードの変更は行わない。**

手順:

1. 指摘箇所の実コードと周辺コードを読む。
2. 既存の類似実装パターンを確認する。
3. 修正による影響範囲を特定する。
4. 具体的な修正手順を策定する。

各指摘について以下を明記する。

| 項目 | 内容 |
|---|---|
| 修正内容 | 何をどう変更するか |
| 影響範囲 | 変更が影響する他のファイル・テスト |
| 注意点 | 修正時に気をつけるべきこと |

#### 6.3 修正実行

修正計画に従ってコードを修正する。未解決コメントと CI 失敗を同一コンテキストで修正する。

- **計画に記載された範囲のみを変更する**。
- 修正後、関連するテスト・lint を実行して通過を確認する。

#### 6.4 却下した指摘に返信・resolve

**修正した指摘**: 返信不要。次のステップ（6.5）の push 時に CodeRabbit の auto-resolve で自動的に resolved になる。

**却下した指摘**: 却下理由を返信した後、GraphQL mutation でスレッドを resolve する。

却下理由の返信:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  -X POST \
  -f body="{却下理由の markdown}" \
  -F in_reply_to={comment_database_id}
```

- `{comment_database_id}` はステップ 5 で取得した先頭コメントの `databaseId`（REST API 整数 ID）。

返信後、即座にスレッドを resolve する:

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: { threadId: "{thread_node_id}" }) {
      thread { isResolved }
    }
  }'
```

- `{thread_node_id}` はステップ 5 で取得した各スレッドの `id` フィールド（例: `PRRT_xxx`）。
- 返信 → resolve の順序で実行する（resolve 済みスレッドには CodeRabbit は再反応しない）。

#### 6.5 コミット・push

`/vibecorp:commit` を使用してコミットし（worktree モードでは `--worktree <path>` を引き継ぐ）、リモートに push する。

```bash
git push
```

### 7. 結果報告

```text
## /vibecorp:pr-fix 完了

- PR: #{pr_number}
- レビュー修正: {n}件
- レビュー却下: {n}件
- CI 修正: {n}件
- CI 待機: {n}件
```

**マージ済みの場合:**

```text
## /vibecorp:pr-fix 完了

- PR: #{pr_number}
- 状態: マージ済み
```

**対応不要の場合:**

```text
## /vibecorp:pr-fix 完了

- PR: #{pr_number}
- 未解決コメント: なし
- CI: green（または PENDING {n}件）
```

## ⚠️ 制約

- `--force`、`--hard`、`--no-verify` は使用しない。
- ユーザーの明示的な指示なしに force push しない。
- 判断に迷う指摘はユーザーに確認する。
- 修正前に必ず関連ファイルを読み込む。
- **`@coderabbitai approve` の投稿は禁止** — approve は CodeRabbit が自動発行するか、人間が手動で行う。
- **PR 本文修正時は auto-close キーワード `Closes #N` / `Refs #N` を保持する** — `gh pr edit --body` で本文を書き換える場合、既存の `Closes #N` / `Refs #N` 行を消さない。新規追加する場合も `#N` 形式（URL 形式不可）で記載する。詳細は `.claude/rules/workflow.md`「PR 本文の Issue リンク（auto-close キーワード）」を参照。
- **jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する（[根拠](docs/design-philosophy.md#jq-string-interpolation-の禁止)）。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。

## 🔗 関連ルール

- 定期実行ループ: `/vibecorp:pr-fix-loop`
- PR 作成スキル: `/vibecorp:pr`
- 捌き基準（intent × severity）: `.claude/rules/review-handling.md`
- レビュー観点（intent 別）: `.claude/rules/review-observations.md`
- severity 公式定義: `.claude/rules/severity/coderabbit.md`
- severity 実体版: `.claude/rules/severity/claude-action.md`
- intent ラベル定義: `.claude/rules/intent-labels.md`
- ワークフロー規約: `.claude/rules/workflow.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
