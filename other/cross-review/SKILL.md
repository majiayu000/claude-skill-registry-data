---
name: cross-review
description: 実装・commit 後、`acceptance-check` 通過後・PR 作成前に、実装セッションから独立した reviewer session を実行中 agent runtime に対応する CLI で起動し、diff への second opinion を得る。
version: 3.2.0
---

# Cross Review Skill

実装済みの変更を、実装セッションから独立した **reviewer session** に渡して second opinion を得る。目的は「別 backend / 別モデルであること」の機械的保証ではなく、実装時の会話文脈・自己正当化・途中判断から切り離したレビュー専用セッションを作ること。

Agent Skills は agent-portable な open standard であり、本 skill は特定の Claude Code 固有 primitive (Sub-Agent / Task tool) には依存しない。実行中 agent runtime に対応する外部 CLI を使い、Codex 利用時は Codex CLI、Claude Code 利用時は Claude CLI だけで完結させる。

## 利用タイミング

- 実装・commit 後、`acceptance-check` を通過した時点で PR 作成前に呼び出す（cycle 内では実装/commit → acceptance-check → cross-review → PR の順）。レビュー指摘の修正は **追加 commit** として残し、`git commit --amend` / `rebase` 等で履歴整形しない。
- ユーザーが明示的にレビューを依頼した場合。

## 依存 / 互換性

- **Codex CLI**: Codex runtime で本 skill を使う場合に必要 (`brew install --cask codex`)。`codex exec` + stdin diff pipe 方式で独立 reviewer session を起動する。`codex exec review --base ... [PROMPT]` は少なくとも codex-cli 0.142.5 時点で parser が拒否するため（openai/codex#22145）、本 skill は `codex exec review` のサブコマンド固有の挙動には依存しない。
- **Claude CLI**: Claude Code runtime で本 skill を使う場合に必要 (`npm install -g @anthropic-ai/claude-code`)。`claude -p` で独立 reviewer session を起動する。stdin の 10MB 上限に当たる場合は 4. 分割レビューに切り替える。
- **`gh` CLI**: default branch 解決に必要。未認証 / repo 外実行では本 skill が明示的に停止する（失敗時の対応参照）。

## Reviewer Session の起動方針

実行中の agent runtime に対応する CLI で reviewer session を起動する。backend の自動検出や環境変数 override による切り替えは扱わない。runtime は実行中 agent が自分の環境情報として明示的に把握している値だけで判定し、`command -v codex` / `command -v claude` の存在順から推測しない。

| 実装中の runtime | 使用 CLI | 起動方法 |
| ---------------- | -------- | -------- |
| Codex CLI | Codex CLI | `codex --ask-for-approval never exec --sandbox read-only` |
| Claude Code | Claude CLI | `claude -p --allowedTools "Read"` |

この対応は「同じ製品ファミリーの CLI で別セッションを起動する」ためのものであり、別モデルレビューを保証するものではない。別 backend / 別モデルレビューが必要な場合は、本 skill の責務として残さず別 issue で設計する。

### Codex managed worker の外側 sandbox

`issue-dispatch` が `codex exec --approve-for-me --worktree` で起動した Codex managed worker では、worker の `workspace-write` sandbox 内から nested `codex exec` を通常起動すると、子 process が `failed to initialize in-process app-server client: Operation not permitted (os error 1)` で停止することがある。

この呼び出し方だと確認できる場合に限り、diff は worker の `workspace-write` sandbox 内で一時 file へ生成し、**`codex --ask-for-approval never exec --sandbox read-only ... < '<diff-file>'` という reviewer 起動 command だけ**を、最初の実行から narrowly scoped escalation で Auto-review に要求する。sandbox 外で `git diff` や repository command を実行しない。これは外側の worker sandbox を越えて reviewer process を起動するための例外であり、子 reviewer 自体の sandbox を緩めるものではない。子には常に `--ask-for-approval never` と `--sandbox read-only` を明示し、sandbox 外実行の approval を要求できない read-only non-interactive session に固定する。`--full-auto`、`--sandbox workspace-write`、`danger-full-access`、`--dangerously-bypass-approvals-and-sandbox`、writable root 追加、`--add-dir` は使わない。

通常の Codex CLI session、Claude Code、または managed worker だと確認できない session では escalation せず、それぞれ従来の起動方法を使う。managed worker で Auto-review が unavailable / denied / timeout の場合、または承認後の exact command が non-zero の場合は、その時点で blocked とし、通常 sandbox での再試行、権限拡大、別 CLI / backend / primitive への暗黙 fallback を行わない。

## 実行手順

### 0. runtime と CLI の事前確認

実行中 agent runtime を明示的に判定する。Codex CLI で実装している場合は Codex CLI、Claude Code で実装している場合は Claude CLI を使う。判定できない場合、または Cursor / Gemini など本 skill に手順が定義されていない runtime の場合は、別 CLI へ自動的に切り替えず停止する。

runtime 判定後、対応 CLI の存在だけを確認する。以下はいずれか一方だけを実行し、両方を連続実行しない。

```bash
# Codex CLI で実装している場合
command -v codex >/dev/null 2>&1 || { printf '%s\n' 'Codex CLI runtime ですが `codex` コマンドが見つかりません。`brew install --cask codex` で導入してください。' >&2; exit 1; }
```

```bash
# Claude Code で実装している場合
command -v claude >/dev/null 2>&1 || { printf '%s\n' 'Claude Code runtime ですが `claude` コマンドが見つかりません。`npm install -g @anthropic-ai/claude-code` で導入してください。' >&2; exit 1; }
```

### 1. base ref の確定

リポジトリの default branch 名を動的に取得し、ローカルで実際に解決可能な ref を `BASE_REF` に確定する。`BASE_REF` は `git diff "$BASE_REF"...HEAD` の base として使う。

```bash
BASE_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
[ -n "$BASE_BRANCH" ] || { echo "default branch を取得できませんでした。gh の認証状態 / repo 内での実行か確認してください。" >&2; exit 1; }

if git rev-parse --verify --quiet "$BASE_BRANCH" >/dev/null; then
  BASE_REF="$BASE_BRANCH"
elif git rev-parse --verify --quiet "origin/$BASE_BRANCH" >/dev/null; then
  BASE_REF="origin/$BASE_BRANCH"
else
  echo "'$BASE_BRANCH' も 'origin/$BASE_BRANCH' も resolve できません。git fetch origin を実行してから再試行してください。" >&2
  exit 1
fi
```

`master` / `develop` / `trunk` を default branch とするリポジトリでも、この `BASE_REF` 経由で同じ手順がそのまま動く。`main` への暗黙フォールバックは行わない（後述「失敗時の対応」参照）。

### 2. 差分の確認

`<resolved-base-ref>` はステップ1で確定した `BASE_REF` の実値へ、shell-safe な単一引用符付き literal として置き換える。前の tool invocation の shell 変数を引き継げると仮定せず、この block 内で再設定・検証する。

```bash
BASE_REF='<resolved-base-ref>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1

# コミット済みの変更（ブランチの差分）
git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD --stat
git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD

# 未コミットの変更がある場合（unstaged + staged）
git diff --no-ext-diff --no-textconv --stat
git diff --no-ext-diff --no-textconv
git diff --no-ext-diff --no-textconv --cached --stat
git diff --no-ext-diff --no-textconv --cached
```

差分のファイル数と行数を確認し、レビュー方法を決定する。

- **差分が 500 行以下**: 一括レビュー（ステップ 3 へ）
- **差分が 500 行超**: ファイル単位で分割レビュー（ステップ 4 へ）
- **差分が 0 行**: レビュー不要としてスキップする

### 3. 一括レビュー

#### 3-a. Codex CLI で実行中の場合

`codex exec` に diff を stdin から渡し、レビュー指示を `[PROMPT]` 引数として渡す。stdin が pipe または redirection で渡され、かつ `[PROMPT]` も指定された場合、codex は stdin を `<stdin>` ブロックとして prompt に append する仕様 (`codex exec --help` 参照)。`codex exec review` のサブコマンド固有の挙動には依存しない。

`--ask-for-approval never` と `--sandbox read-only` を明示することで、汎用 `codex exec` を使いながらも sandbox 外実行の approval を要求できない read-only non-interactive session とし、cross-review の「報告のみ・自動修正しない」原則を CLI レイヤーで担保する（`--full-auto` は workspace-write が付くため使わない）。

まず次の diff 生成 block を通常 sandbox 内で実行する。`mktemp` が作った 0600 の一時 file へ、external diff / textconv を明示的に無効化した差分だけを書き出す。生成失敗時は reviewer を起動せず一時 file を削除して停止する。

`<resolved-base-ref>` はステップ1で確定した `BASE_REF` の実値へ、shell-safe な単一引用符付き literal として置き換える。tool invocation ごとに新しい shell が起動する runtime でも値を失わないよう、placeholder や前の shell の変数に依存したまま実行しない。

```bash
BASE_REF='<resolved-base-ref>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1
DIFF_FILE=$(mktemp "${TMPDIR:-/tmp}/cross-review.XXXXXX") || exit 1
chmod 600 "$DIFF_FILE" || { rm -f "$DIFF_FILE"; exit 1; }
(
  echo "=== Committed diff ($BASE_REF...HEAD) ==="
  git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD || exit 1
  echo
  echo "=== Unstaged diff ==="
  git diff --no-ext-diff --no-textconv || exit 1
  echo
  echo "=== Staged diff ==="
  git diff --no-ext-diff --no-textconv --cached || exit 1
) > "$DIFF_FILE" || { rm -f "$DIFF_FILE"; exit 1; }
printf '%s\n' "$DIFF_FILE"
```

`<diff-file>` は直前に出力された一時 file の実 path へ shell-safe な単一引用符付き literal として置き換える。Codex managed worker では次の **reviewer 起動 command だけ**を exact command として scoped escalation 付きで最初から実行する。その他の Codex CLI session では通常 sandbox 内で実行する。

```bash
codex --ask-for-approval never exec --sandbox read-only "You are a senior code reviewer providing a second opinion. Do not modify any files; output the review only. The diff is supplied via stdin (codex wraps it as a <stdin> block). First, read the repository's AGENTS.md (if it exists) to understand project conventions and coding standards.

Then evaluate the diff from these perspectives:

1. **Correctness**: Are there logic errors, edge cases, or incorrect assumptions?
2. **Readability**: Are names clear and intent obvious? Is the code self-documenting?
3. **Consistency**: Do the changes follow existing patterns, naming conventions, and style in the codebase?
4. **Security**: Is there proper input validation? Are secrets or credentials exposed?
5. **Performance**: Are there unnecessary computations or inefficient patterns?
6. **Tests**: If the project has tests, is coverage adequate for the changes?
7. **Documentation**: Are related docs (README, CLAUDE.md, AGENTS.md, inline comments, etc.) updated to reflect the changes? Flag missing or outdated documentation.
8. **Related-file consistency**: When a file changes, are sibling/peer files that must stay in sync also updated? Examples: cross-references between skills, generated files, lock files, schema and its migration, config and its documentation. Flag any consistency gap where one side of a known pair was changed but the other was not.

Output format (respond in Japanese):
- List each finding with severity: critical / warning / info
- For each finding, include: file path, line number or range, description, and a concrete fix suggestion
- If no issues found, state that the code looks good
- End with a summary table: total findings by severity" < '<diff-file>'
```

reviewer の成功・失敗にかかわらず、結果と exit code / stderr を記録した後、通常 sandbox 内で `rm -f '<diff-file>'` を実行する。削除後に reviewer 結果の処理または blocker 報告へ進む。

#### 3-b. Claude Code で実行中の場合

`claude -p` で Claude CLI に diff を stdin 経由で渡す。`--bare` は OAuth / keychain のログイン状態を読まず `ANTHROPIC_API_KEY` または `--settings` の `apiKeyHelper` 前提になるため、ローカルの Claude.ai ログイン運用でも動くように使わない。`AGENTS.md` を読ませるために `--allowedTools "Read"` を付与する。

```bash
BASE_REF='<resolved-base-ref>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1
set -o pipefail
(
  echo "=== Committed diff ($BASE_REF...HEAD) ==="
  git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD || exit 1
  echo
  echo "=== Unstaged diff ==="
  git diff --no-ext-diff --no-textconv || exit 1
  echo
  echo "=== Staged diff ==="
  git diff --no-ext-diff --no-textconv --cached || exit 1
) | claude -p \
  --allowedTools "Read" \
  --append-system-prompt "You are a senior code reviewer providing a second opinion. The diff is supplied via stdin. First, read the repository's AGENTS.md (if it exists) to understand project conventions and coding standards." \
  "Evaluate the diff from these perspectives:

1. **Correctness**: Are there logic errors, edge cases, or incorrect assumptions?
2. **Readability**: Are names clear and intent obvious? Is the code self-documenting?
3. **Consistency**: Do the changes follow existing patterns, naming conventions, and style in the codebase?
4. **Security**: Is there proper input validation? Are secrets or credentials exposed?
5. **Performance**: Are there unnecessary computations or inefficient patterns?
6. **Tests**: If the project has tests, is coverage adequate for the changes?
7. **Documentation**: Are related docs (README, CLAUDE.md, AGENTS.md, inline comments, etc.) updated to reflect the changes? Flag missing or outdated documentation.
8. **Related-file consistency**: When a file changes, are sibling/peer files that must stay in sync also updated? Examples: cross-references between skills, generated files, lock files, schema and its migration, config and its documentation. Flag any consistency gap where one side of a known pair was changed but the other was not.

Output format (respond in Japanese):
- List each finding with severity: critical / warning / info
- For each finding, include: file path, line number or range, description, and a concrete fix suggestion
- If no issues found, state that the code looks good
- End with a summary table: total findings by severity"
```

### 4. 分割レビュー（差分が大きい場合）

差分をファイル単位に分割し、ファイルごとに reviewer session を呼ぶ。最後に全ファイルのレビュー結果を集約してサマリーを作成する。

ここでも `<resolved-base-ref>` をステップ1で確定した実値へ shell-safe な単一引用符付き literal として置き換え、この block 内で再設定・検証する。

```bash
BASE_REF='<resolved-base-ref>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1

# 変更ファイル一覧を取得（コミット済み + unstaged + staged の和集合）
git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD --name-only
git diff --no-ext-diff --no-textconv --name-only
git diff --no-ext-diff --no-textconv --cached --name-only
```

#### 4-a. Codex CLI で実行中の場合

`FILE_PATH` でファイルパスを変数化し、空白や shell メタ文字を含むファイル名でも壊れないようにする（3-a と同じく `--ask-for-approval never` と `--sandbox read-only` で sandbox 外実行の申請と書き込みを禁止）。`<file-path>` は placeholder で、実利用時は単一引用符付きで実パスに置き換える（例: `FILE_PATH='skills/cross-review/SKILL.md'`）。

Codex managed worker ではファイルごとに diff file を通常 sandbox 内で生成し、reviewer 起動 command だけを scoped escalation 付きで実行する。各 reviewer launch は個別に承認を要求し、1つが拒否・timeout・失敗した時点で残りへ進まず blocked とする。

`<resolved-base-ref>` はステップ1で確定した実値へ、`<file-path>` は対象 file の実値へ、それぞれ shell-safe な単一引用符付き literal として置き換える。前の shell の `BASE_REF` / `FILE_PATH` を引き継げると仮定しない。

```bash
BASE_REF='<resolved-base-ref>'
FILE_PATH='<file-path>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1
DIFF_FILE=$(mktemp "${TMPDIR:-/tmp}/cross-review.XXXXXX") || exit 1
chmod 600 "$DIFF_FILE" || { rm -f "$DIFF_FILE"; exit 1; }
(
  echo "=== Diff for $FILE_PATH ==="
  git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD -- "$FILE_PATH" || exit 1
  git diff --no-ext-diff --no-textconv -- "$FILE_PATH" || exit 1
  git diff --no-ext-diff --no-textconv --cached -- "$FILE_PATH" || exit 1
) > "$DIFF_FILE" || { rm -f "$DIFF_FILE"; exit 1; }
printf '%s\n' "$DIFF_FILE"
```

`<file-path>` と `<diff-file>` はそれぞれ確定済みの実値へ shell-safe な単一引用符付き literal として置き換える。Codex managed worker では次の reviewer 起動 command だけを scoped escalation 付きで実行する。

```bash
FILE_PATH='<file-path>'
codex --ask-for-approval never exec --sandbox read-only "You are a senior code reviewer providing a second opinion. Do not modify any files; output the review only. The diff for a single file is supplied via stdin (codex wraps it as a <stdin> block). Review the changes to $FILE_PATH.

Evaluate from: Correctness, Readability, Consistency, Security, Performance, Tests, Documentation, Related-file consistency.

Output (respond in Japanese):
- Each finding with severity (critical / warning / info), file path, line number, description, fix suggestion
- If no issues, state the file looks good" < '<diff-file>'
```

結果と exit code / stderr を記録後、通常 sandbox 内で `rm -f '<diff-file>'` を実行してから次の file または blocker 報告へ進む。

#### 4-b. Claude Code で実行中の場合

```bash
BASE_REF='<resolved-base-ref>'
FILE_PATH='<file-path>'
git rev-parse --verify --quiet "$BASE_REF" >/dev/null || exit 1
set -o pipefail
{
  echo "=== Diff for $FILE_PATH ==="
  git diff --no-ext-diff --no-textconv "$BASE_REF"...HEAD -- "$FILE_PATH" || exit 1
  git diff --no-ext-diff --no-textconv -- "$FILE_PATH" || exit 1
  git diff --no-ext-diff --no-textconv --cached -- "$FILE_PATH" || exit 1
} | claude -p \
  --allowedTools "Read" \
  --append-system-prompt "You are a senior code reviewer providing a second opinion. The diff for a single file is supplied via stdin." \
  "Review the changes to $FILE_PATH.

Evaluate from: Correctness, Readability, Consistency, Security, Performance, Tests, Documentation, Related-file consistency.

Output (respond in Japanese):
- Each finding with severity (critical / warning / info), file path, line number, description, fix suggestion
- If no issues, state the file looks good"
```

### 5. 結果の集約と報告

reviewer session の結果を確認し、ユーザーへ報告する。

- **critical** の指摘がある場合: 修正案を提示し、ユーザーに対応方針を確認する
- **warning** の指摘がある場合: agent 自身で対応要否を判断する。妥当な指摘は自律的に修正し、見送る場合は理由を添えて報告する（ユーザー確認は不要）
- **info** のみの場合: 指摘を共有し、PR 作成に進む

## 失敗時の対応

- **実行中 runtime に対応する CLI が見つからない場合**: Codex CLI で実装しているなら `codex`、Claude Code で実装しているなら `claude` が必要。該当 CLI が無ければ明示的に停止し、Codex CLI は `brew install --cask codex`、Claude CLI は `npm install -g @anthropic-ai/claude-code` を案内する。Codex CLI 初回利用時は `codex login` で OpenAI アカウント認証が必要。Claude CLI 初回利用時は `claude` を一度起動して認証する。
- **実行中 runtime を判定できない場合**: 自動検出で別 CLI へ切り替えず停止する。Codex CLI / Claude Code 以外の runtime 向け手順は別 issue で扱う。
- **default branch の取得失敗時**: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` が空文字を返す、もしくは `gh` がエラーを返した場合は、その時点で停止しエラーメッセージを出す。`main` への暗黙フォールバックは行わない（誤った base に対する diff でレビュー結果が破綻するため）。よくある原因は、`gh` 未認証 (`gh auth status` で確認) / git repo 外での実行 / リモートが GitHub 以外。原因を解消してから再実行する。
- **base ref の resolve 失敗時**: `BASE_BRANCH` 名は取れたが、ローカルに該当 ref も `origin/$BASE_BRANCH` も存在しない場合（例: 浅い clone / default branch を local 側で削除した worktree 等）も停止する。`git fetch origin` で remote-tracking ref を取得すれば多くの場合解消する。
- **Codex managed worker の diff 生成が失敗した場合**: reviewer を起動せず一時 file を削除し、diff 生成の exit code / stderr を報告して停止する。sandbox 外へ diff 生成を移さない。
- **Codex managed worker の reviewer 起動が拒否・timeout・失敗した場合**: exact reviewer process command、Auto-review の状態または表示された rationale、exit code / stderr を blocker として報告し、一時 file を通常 sandbox 内で削除して停止する。通常 sandbox での reviewer 再試行、権限拡大、`claude -p` 等への切り替え、別 primitive への fallback は行わない。子 reviewer の `--ask-for-approval never` と `--sandbox read-only` も変更しない。
- **Codex CLI で `codex exec review --base ... [PROMPT]` 系のエラーに遭遇した場合**: Codex CLI 側の既知制約として、native review target (`--base` / `--commit` / `--uncommitted`) と custom prompt は同時に受け付けられない。本 skill の実行例は `git diff "$BASE_REF"...HEAD` を stdin で `codex --ask-for-approval never exec --sandbox read-only` に渡す方式なので、`codex exec review` へ置き換えない。古いメモや shell history に残った `codex exec review --base ... [PROMPT]` の呼び出しは破棄する。
- **差分がない場合**: レビュー不要としてスキップする。
- **reviewer session がタイムアウトした場合**: Codex managed worker では上記の blocker 規則に従って停止する。それ以外の runtime / session では差分を分割して再試行する（ステップ 4）。
- **Claude CLI で stdin が 10MB を超える場合**: Claude CLI が明示的にエラーで停止するので、ステップ 4 の分割レビューに切り替える。

## Codex managed worker 経路の再現可能な検証

この経路を変更した場合は disposable な `codex exec --approve-for-me --worktree` worker で、次の成功・失敗両方を確認し、実行条件、exact reviewer-launch command、Auto-review の判定、exit code / stderr、reviewer 出力、一時 file の削除、変更前後の `git status --porcelain` を PR description に残す。秘密情報やローカル絶対 path は記録しない。

1. **成功経路**: diff が worker sandbox 内の 0600 一時 file に生成され、Auto-review が reviewer process の exact command を承認する環境でステップ 3 または 4 を実行する。reviewer 結果が worker に返り、reviewer 前後で repository file と Git metadata に意図しない変更がなく、一時 file が削除されたことを確認する。子 command に `--ask-for-approval never` と `--sandbox read-only` が含まれ、起動ログが `approval: never` / `sandbox: read-only` を示すことも記録する。
2. **失敗経路**: disposable worker で reviewer-launch escalation を拒否するか timeout / non-zero failure を再現する。worker が一時 file を削除して blocker を返し、通常 sandbox での reviewer 再試行、権限拡大、別 CLI / backend / primitive への fallback が行われないことを確認する。

reviewer の read-only 境界そのものを追加検証する場合は、disposable branch で repository file と Git ref への書き込みを reviewer に要求し、両方が拒否され、実行前後の `git status --porcelain` と ref 一覧が一致することを確認する。通常の実装 branch に probe file や probe ref を残さない。

## やらないこと

- backend / CLI の自動検出や環境変数 override による切り替え。実行中 runtime に対応する CLI で独立 reviewer session を起動する。
- 別 backend / 別モデルレビューの保証。必要なら別 issue として扱う。
- レビュー結果の自動修正適用（報告のみ）。
- reviewer session の出力フォーマットの統一（各 CLI の出力をそのまま使う）。
- 追加 backend (Gemini / OpenAI 直 API 等) の実装。構造を残しつつ別 issue 化。
- Codex managed worker で reviewer 起動が拒否・timeout・失敗した後、通常 sandbox、より広い権限、別 CLI / backend / primitive へ切り替えて review を通したことにすること。
- codex-cli 0.124 系以前への downgrade 案内。upstream の意思決定に追従しない一時しのぎになり、依存 CLI のバージョン分岐が発散するため採らない（`codex exec` + stdin diff pipe で正面突破する）。
