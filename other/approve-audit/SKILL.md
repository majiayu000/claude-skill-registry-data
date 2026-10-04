---
name: approve-audit
description: "コマンドログを棚卸しし、settings.local.json の allow リストへの追加を提案・実行する。「/vibecorp:approve-audit」「許可リスト更新」「コマンド棚卸し」と言った時に使用。"
---

# 🛡️ 許可リスト棚卸し

> [!IMPORTANT]
> このスキルはコマンドログを棚卸しし、`settings.local.json` の **allow リストへの追加を提案・実行** する。
> ユーザーの承認なしに `settings.local.json` を変更しない。
> 全提案は `AskUserQuestion` で明示確認を取る。

コマンドログを棚卸しし、`settings.local.json` の allow リストを最適化する。

## worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **`$CLAUDE_PROJECT_DIR`**: worktree モードでは `<path>` に置き換える。
- 未指定時は従来通り CWD で実行する（後方互換）。

## 🔄 ワークフロー

## 1. ログファイルの読み込み

ログファイルを読み込む。

ログファイルパス: `~/.cache/vibecorp/state/<repo-id>/command-log`（`.claude/lib/common.sh` の `vibecorp_state_path command-log` で取得）

```bash
source "$CLAUDE_PROJECT_DIR"/.claude/lib/common.sh
log_file="$(vibecorp_state_path command-log)"
cat "$log_file"
```

ログファイルが存在しない、または空の場合は「記録されたコマンドがありません」と報告して終了する。

## 2. settings.local.json の allow パターン取得

```bash
if [ -f "$CLAUDE_PROJECT_DIR"/.claude/settings.local.json ]; then
  cat "$CLAUDE_PROJECT_DIR"/.claude/settings.local.json
else
  echo '{"permissions":{"allow":[]}}'
fi
```

ファイルが存在しない場合、または `permissions.allow` が空の場合は空リストとして扱う。

`permissions.allow` 配列の各エントリを取得する。パターンの形式は以下のとおり。

| パターン | 意味 |
|---|---|
| `Bash(prefix:*)` | コマンドプレフィックスマッチ |
| `Bash(exact)` | 完全一致 |

## 3. 未許可コマンドの抽出

ログの各コマンドに対して allow パターンとの照合を行い、**マッチしないコマンド** を抽出する。

照合ルール:

- `Bash(prefix:*)` パターン: コマンドが `prefix` で始まればマッチ。
- `Bash(exact)` パターン: コマンドが完全一致すればマッチ。
- 複数回実行されたコマンドはカウントを集計する。

## 4. パターン化と提案

未許可コマンドを分析し、類似コマンドをグルーピングしてパターンを提案する。

パターン化のガイドライン:

- 同じコマンドの異なるサブコマンド → `Bash(command:*)` にまとめる（例: `npm run build`, `npm run test` → `Bash(npm run:*)`）。
- 引数違いのみ → ワイルドカード化（例: `git diff HEAD`, `git diff main` → `Bash(git diff:*)`）。
- 単発のコマンドはそのまま提案する。

提案フォーマット:

```text
## コマンドログ棚卸し結果

ログ期間: {最初のタイムスタンプ} 〜 {最後のタイムスタンプ}
記録コマンド数: {総数}
未許可コマンド数: {件数}

### allow リスト追加提案

| # | パターン | 実行回数 | 代表コマンド |
|---|---------|---------|------------|
| 1 | Bash(npm run:*) | 5 | npm run build, npm run test |
| 2 | Bash(docker compose:*) | 3 | docker compose up, docker compose down |
| 3 | Bash(rm -rf node_modules) | 1 | rm -rf node_modules |

追加するパターンの番号を指定してください（例: 1,2）。
全て追加する場合は「all」、キャンセルする場合は「none」と入力してください。
```

## 5. ユーザー承認

`AskUserQuestion` でユーザーの選択を取得する。

## 6. settings.local.json への書き込み

承認されたパターンを `settings.local.json` の `permissions.allow` に追加する。

```bash
cat "$CLAUDE_PROJECT_DIR"/.claude/settings.local.json
```

ファイルが存在しない場合は新規作成する。

```json
{
  "permissions": {
    "allow": []
  }
}
```

既存の allow リストに承認されたパターンを追加する。**jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する（[根拠](docs/design-philosophy.md#jq-string-interpolation-の禁止)）。

書き込み後、追加されたパターンを報告する。

## 7. ログファイルのクリア（任意）

ユーザーに「ログファイルを削除しますか？」と確認し、承認された場合のみ削除する。

```bash
source "$CLAUDE_PROJECT_DIR"/.claude/lib/common.sh
rm -f "$(vibecorp_state_path command-log)"
```

## 8. 結果報告

```text
## /vibecorp:approve-audit 完了

- 記録コマンド数: {n}
- 未許可コマンド数: {n}
- 追加パターン数: {n}
- 追加先: .claude/settings.local.json
```

## 制約

- `--force`、`--hard`、`--no-verify` は使用しない。
- ユーザーの明示的な指示なしに force push しない。
- **jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する（[根拠](docs/design-philosophy.md#jq-string-interpolation-の禁止)）。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- ユーザーの承認なしに `settings.local.json` を変更しない。

## 🔗 関連ルール

- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
