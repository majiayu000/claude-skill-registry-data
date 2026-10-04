---
name: review
description: "実装レビューを実行する。Claude Code CLI 直接呼び出しとカスタムレビュアーを並列で呼び出す。ユーザーが「/review」「レビューして」と言った時に使用。"
---

# 🔍 実装レビュー

> [!IMPORTANT]
> このスキルは変更差分に対し **ローカル Claude Code CLI と カスタムレビュアー** を並列で実行する。
> 認証経路は **Claude Max OAuth 個人クォータ** であり、`ANTHROPIC_API_KEY` が設定されていると fail-fast する。
> レビュー完了時は `review-ok` スタンプを生成し、PR 作成の前提を満たす。

変更差分をレビューする。以下の手順で実行する。

## 🌳 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継ぐ。
- **`$CLAUDE_PROJECT_DIR`**: worktree モードでは `<path>` に置き換える。
- 未指定時は従来通り CWD で実行する（後方互換）。

## 🔄 ワークフロー

## 1. 変更ファイルの確認

各コマンドは個別に実行する。`&&` で連結しない。

```bash
git diff --name-only HEAD
```

```bash
git diff --name-only --cached
```

## 2. レビュー実行

### 🤖 ローカルレビュー（Claude Code CLI 直接呼び出し）

ローカルレビューは Claude Code CLI（`claude -p`）を直接呼び出して `REVIEW.md` をプロンプトとして渡す。Issue #499（親エピック #455 コメント 8）で確定した経路。CodeRabbit CLI（`cr review --plain`）の Free 枠 3 reviews/hour 制約から外れ、**制約の種類が Claude Max OAuth 個人クォータに切り替わる**（`docs/cost-analysis.md` の個人 Max クォータ枯渇リスク参照、無制限ではない点に注意）。

コスト経路と認証経路の詳細は `docs/cost-analysis.md`（「`/vibecorp:review` ローカル経路のコスト経路シフト」「`/vibecorp:review` の `ANTHROPIC_API_KEY` 混在 fail-fast」）と `docs/ai-review-auth.md`（OAuth トークン）を参照する。

**`coderabbit.enabled` フラグとの関係**: ローカル Claude Code CLI 経路は `coderabbit.enabled` フラグの **影響を受けない**（常に実行）。`coderabbit.enabled` は `.coderabbit.yaml` 配布制御 + CodeRabbit Bot（CI 側）制御専用であり、ローカル経路には作用しない（`docs/ai-review-dependency.md` の意味論変更を参照）。

#### ガード 1: `ANTHROPIC_API_KEY` 混在 fail-fast

`claude -p` の非対話モードは `ANTHROPIC_API_KEY` があると OAuth より優先して API 従量課金経路に自動切替するため、起動前にチェックして fail-fast する。

```bash
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "[ERROR] ANTHROPIC_API_KEY が設定されています。" >&2
  echo "        非対話モード -p で API 従量課金にフォールバックする恐れがあるため、ローカルレビューを中止します。" >&2
  echo "        対処: 'unset ANTHROPIC_API_KEY' で解除するか、docs/ai-review-auth.md を参照して 'claude setup-token' で OAuth 経路に切り替えてください。" >&2
  exit 1
fi
```

#### ガード 2 + 本体: REVIEW.md 存在確認と stdin パイプ実行

REVIEW.md が存在する場合のみ `claude -p` を呼ぶ。不在時は警告を出してローカルレビューをスキップする（後続のカスタムレビュアー / 結果報告は継続する）。worktree モードでは `<path>/REVIEW.md` を参照する（`$CLAUDE_PROJECT_DIR` を `<path>` に置換）。

REVIEW.md 末尾にローカル出力指示を heredoc で連結し、stdin から `claude -p` に渡す。`claude` コマンド未導入環境と REVIEW.md 不在の両ケースで安全にスキップする。

```bash
if ! command -v claude >/dev/null 2>&1; then
  echo "[WARN] claude コマンドが利用できません。ローカルレビューをスキップします。" >&2
  # 後続セクション（カスタムレビュアー / 結果報告）へ進む
elif [[ ! -f "$CLAUDE_PROJECT_DIR/REVIEW.md" ]]; then
  echo "[WARN] REVIEW.md が存在しません。ローカルレビューをスキップします。" >&2
  # 後続セクション（カスタムレビュアー / 結果報告）へ進む
else
  {
    cat "$CLAUDE_PROJECT_DIR/REVIEW.md"
    cat <<'TAIL'

## ローカルレビュー出力指示

stdout に severity マーカー（🔴🟠🟡🔵⚪）付きで指摘を列挙してください:

- 各指摘に「ファイル:行番号」と「修正提案」を含める
- 末尾にサマリ（指摘総数 / severity 別件数）を出力
- GitHub には投稿しない（CI 側 claude-code-action の責務）
TAIL
  } | claude -p --allowed-tools "Bash,Read,Grep,Glob"
fi
```

設計上の注意:

- **`--bare` フラグは絶対に使わない**: `--bare` は OAuth を読まず `ANTHROPIC_API_KEY` 必須になる。Claude Max 定額運用が崩れる。
- **`--allowed-tools` の範囲**: ローカル経路は stdout 出力で完結するため、読取系のみ許可（`Bash,Read,Grep,Glob`）。`Write,Edit,mcp__github_inline_comment__create_inline_comment` 等の書き込み系・GitHub 投稿系は不許可（GitHub 投稿は CI 側 claude-code-action の責務）。
- **`--prompt-file` フラグは使わない**: Claude Code CLI のバージョン依存があるため、Unix 標準の stdin パイプ方式を採用する。
- **GitHub Actions では `CLAUDE_CODE_OAUTH_TOKEN` を明示**: 既存 `templates/.github/workflows/ai-review.yml` で `claude-code-action@v1` 経由で実装済み（本スキルではローカル経路のみを扱う）。
- **スキップ方針**: `claude` 未導入 / `REVIEW.md` 不在 のいずれもローカルレビューを安全にスキップして後続セクションへ進む。レポートにスキップ理由を記載する。

### 🧰 カスタムレビュアー

`.claude/vibecorp.yml` の `review.custom_commands` を確認する。定義がある場合、各コマンドを並列で実行する。

```yaml
review:
  custom_commands:
    - name: shellcheck
      command: "shellcheck **/*.sh"
```

各カスタムコマンドを実行し、結果を収集する。

## 3. レビュー完了スタンプの生成

レビューが完了したら、PR 作成を許可するスタンプを生成する。スタンプは `~/.cache/vibecorp/state/<repo-id>/` 配下に作成される（`.claude/` 配下への書込確認プロンプトを回避）。

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

## 4. 結果報告

全レビュー結果を統合して報告する。

```text
## レビュー結果

### ローカルレビュー（Claude Code CLI）
- {severity マーカー（🔴🟠🟡🔵⚪）付き指摘サマリ}

### {カスタムレビュアー名}
- {指摘サマリ}

### サマリ
- 指摘総数: {件数}
- 🔴 Critical: {件数}
- 🟠 Major: {件数}
- 🟡 Minor: {件数}
- 🔵 Trivial: {件数}
- ⚪ Info: {件数}
```

## 🔗 関連ルール

- レビュー観点（intent 別）: `.claude/rules/review-observations.md`
- レビュー指摘の捌き基準: `.claude/rules/review-handling.md`
- severity 公式定義: `.claude/rules/severity/coderabbit.md`
- severity 実体版: `.claude/rules/severity/claude-action.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
