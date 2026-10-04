---
name: branch
description: "GitHub Issue URLからブランチを自動作成するスキル。「/branch https://github.com/owner/repo/issues/12345」のようにIssue URLを指定すると、Issueタイトルを要約してdev/{Issue番号}_{要約}形式のブランチ名を生成し、現在のブランチをベースに新規ブランチを作成・チェックアウトする。「ブランチ作成」「branch作成」と言われた時にも使用。"
---

# 🌿 ブランチ自動作成

> [!IMPORTANT]
> このスキルは Issue URL から **`dev/{Issue番号}_{要約}` 形式のブランチを 1 コマンドで作成する**。
> 結果のみを簡潔に返す。途中経過は出力しない。
> `--worktree` 指定時はブランチ作成と同時に git worktree を作成し、`.claude/` を rsync で同期する。

GitHub Issue URL からブランチを作成する。

## 📖 使用方法

```bash
/vibecorp:branch <Issue URL>
/vibecorp:branch --worktree <Issue URL>
```

## ⚙️ オプション

| オプション | 説明 |
|---|---|
| `--worktree` | ブランチ作成と同時に git worktree を作成し、独立したディレクトリで作業できるようにする |

## 🔄 ワークフロー

### 1. Issue 情報の取得

引数から Issue URL を受け取り、Issue 番号とタイトルを取得する。

```bash
gh issue view <Issue URL> --json number,title --jq '.number,.title'
```

### 2. ブランチ名の生成

タイトルを英語の短い要約（スネークケース）に変換し、以下の形式でブランチ名を生成する。

```text
dev/{Issue番号}_{要約}
```

**要約ルール:**

| 項目 | ルール |
|---|---|
| 表記 | 英語のスネークケース（小文字 + アンダースコア） |
| 文字数 | 最大 30 文字 |
| 除外 | 絵文字・タイプ接頭辞（`feat:`, `fix:` 等）は除外する |
| 単語数 | 内容を端的に表す 2〜4 単語 |

例:

- `✨ feat: /vibecorp:ship Issue指定からマージまでの全自動スキル` → `dev/67_ship_auto_merge`
- `🐛 fix: mvv.md path notation inconsistency` → `dev/41_mvv_path_fix`

### 3. ベースブランチの最新化

```bash
git pull origin HEAD --ff-only
```

### 4. ブランチ作成

`--worktree` オプションの有無で分岐する。

#### 通常モード（`--worktree` なし）

```bash
git checkout -b <ブランチ名>
```

#### ワークツリーモード（`--worktree` あり）

##### 4a. ワークツリーディレクトリの決定

`vibecorp.yml` の `worktree_dir` を読み取る。未設定の場合はデフォルト値を使用する。

```bash
MAIN_DIR=$(git rev-parse --show-toplevel)

# vibecorp.yml の worktree_dir を読み取る（未定義なら空文字）
CONFIG_WORKTREE_DIR=$(awk '/^worktree_dir:[[:space:]]*/ { sub(/^worktree_dir:[[:space:]]*/, ""); sub(/[[:space:]]*$/, ""); print; exit }' "$MAIN_DIR/.claude/vibecorp.yml")

if [ -n "$CONFIG_WORKTREE_DIR" ]; then
  # worktree_dir が定義されている場合: 絶対パスはそのまま、相対パスはプロジェクトルート基準
  case "$CONFIG_WORKTREE_DIR" in
    /*) WORKTREE_BASE="$CONFIG_WORKTREE_DIR" ;;
    *) WORKTREE_BASE="$MAIN_DIR/$CONFIG_WORKTREE_DIR" ;;
  esac
else
  # デフォルト: ../{プロジェクト名}.worktrees
  PROJECT_NAME=$(awk '/^name:[[:space:]]*/ { sub(/^name:[[:space:]]*/, ""); sub(/[[:space:]]*$/, ""); print; exit }' "$MAIN_DIR/.claude/vibecorp.yml" | tr -cs 'A-Za-z0-9._-' '_')
  WORKTREE_BASE="${MAIN_DIR}/../${PROJECT_NAME}.worktrees"
fi
```

##### 4b. ワークツリーの作成

```bash
mkdir -p "$WORKTREE_BASE"
git worktree add "$WORKTREE_BASE/<ブランチ名>" -b <ブランチ名>
```

##### 4c. `.claude/` の同期

メインワークツリーの `.claude/` を worktree にコピーする。git 追跡状況に関わらず全ケースで同じコマンドで動作する。

```bash
rsync -a "$MAIN_DIR/.claude/" "$WORKTREE_BASE/<ブランチ名>/.claude/"
```

## ⚠️ 制約

- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](../../docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- 既存のブランチ名と衝突する場合はユーザーに報告して停止する。

## 📤 返却フォーマット

### 通常モード

```text
<ブランチ名>
```

### ワークツリーモード

```text
<ブランチ名>
worktree: <ワークツリーの絶対パス>
```

## 🔗 関連ルール

- ブランチ命名規約: `.claude/rules/workflow.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
