---
name: worktree
description: "ワークツリーのライフサイクル管理スキル。一覧表示、マージ済みワークツリーの自動削除、手動削除、ゾンビエージェントプロセスの kill を行う。「/worktree list」「/worktree clean」「/worktree remove」「/worktree kill-zombies」と言った時に使用。"
---

# 🌳 ワークツリー管理

> [!IMPORTANT]
> このスキルは git worktree のライフサイクルを管理する（一覧 / マージ済み自動削除 / 手動削除 / ゾンビ tmux エージェント kill）。
> 結果のみを簡潔に返す。途中経過は出力しない。
> 未コミット変更があるワークツリー・メインワークツリーは **削除対象から除外** する。

git worktree のライフサイクルを管理する。

## 📖 使用方法

```bash
/vibecorp:worktree list
/vibecorp:worktree clean
/vibecorp:worktree remove <ブランチ名>
/vibecorp:worktree kill-zombies
```

## 📦 サブコマンド

| サブコマンド | 用途 |
|---|---|
| `list` | 全ワークツリーの状態を表示する |
| `clean` | マージ済み / 孤立ワークツリーを自動削除し、ゾンビ tmux エージェントも掃除する |
| `remove <ブランチ名>` | 指定したワークツリーを手動削除する |
| `kill-zombies` | ゾンビ tmux エージェントだけを kill する |

## 🗂️ list — ワークツリー一覧

全ワークツリーの状態を表示する。

```bash
git worktree list
```

各ワークツリーについて、ブランチ名でタイプを判定し、対応する情報を取得する。

### 🏷️ ブランチタイプの判定

| パターン | タイプ | PR 確認 |
|---------|--------|---------|
| `worktree-agent-*` | Agent worktree | 不要（PR なし） |
| `dev/*` 等 | 通常 worktree | PR 状態を確認 |

### 通常 worktree の PR 確認

```bash
gh pr list --head <ブランチ名> --state all --json number,state,title --jq 'if length > 0 then .[0] | ("#" + (.number | tostring)) + " " + (.state | ascii_downcase) + " " + .title else "- - -" end'
```

### Agent worktree の状態判定

```bash
# 未コミット変更の有無
git -C <worktree_path> status --porcelain
```

```bash
# ベースブランチとの差分の有無
git -C <worktree_path> diff HEAD..origin/main --quiet
```

| 状態 | 条件 |
|---|---|
| `agent (孤立)` | 未コミット変更なし + 差分なし |
| `agent (作業中)` | 未コミット変更あり or 差分あり |

### 返却フォーマット

```text
| パス | ブランチ | PR | 状態 |
|------|---------|-----|------|
| /path/to/worktree | dev/62_xxx | #123 | open |
| /path/to/worktree2 | dev/99_yyy | #456 | merged |
| .claude/worktrees/agent-abc123 | worktree-agent-abc123 | - | agent (孤立) |
| .claude/worktrees/agent-def456 | worktree-agent-def456 | - | agent (作業中) |
```

## 🧹 clean — マージ済み・孤立ワークツリーの自動削除

マージ済みの PR に対応するワークツリー、および孤立した Agent worktree を自動削除する。
削除完了後、消えた worktree を見続けるゾンビ tmux エージェントも自動 kill する（`kill-zombies` と同じ動作）。

### ワークフロー

1. `git worktree list` で全ワークツリーを取得（メインを除く）。
2. 各ワークツリーのブランチ名でタイプを判定する。

### 通常 worktree（`dev/*` 等）の処理

3. ブランチについて PR の状態を確認する。
4. `merged` 状態の PR に対応するワークツリーを削除対象とする。
5. 削除前に未コミットの変更がないか確認する。

```bash
# 未コミット変更の確認（worktree のパスで実行）
git -C <worktree_path> status --porcelain
```

6. 未コミット変更がある場合はスキップしてユーザーに報告する。
7. 変更がない場合はワークツリーとローカルブランチを削除する。

```bash
git worktree remove <worktree_path>
```

```bash
git branch -d <ブランチ名>
```

### Agent worktree（`worktree-agent-*`）の処理

Agent worktree は PR を持たないため、以下の条件で削除を判定する。

3. 未コミットの変更がないか確認する。

```bash
git -C <worktree_path> status --porcelain
```

4. ベースブランチとの差分がないか確認する（Agent が変更を残していないか）。

```bash
git -C <worktree_path> diff HEAD..origin/main --quiet
```

5. **両方とも空**（未コミット変更なし + 差分なし）→ 孤立した Agent worktree として削除する。

```bash
git worktree remove <worktree_path>
```

```bash
git branch -d <ブランチ名>
```

6. **いずれかが非空** → スキップしてユーザーに報告する（作業中 or 未プッシュの変更がある）。

### worktree 削除後のゾンビ kill

ワークツリー削除ステップが完了したら、`kill-zombies` サブコマンドと同じ手順でゾンビエージェントを掃除する（後述「kill-zombies — ゾンビ tmux エージェントの自動 kill」参照）。

### 返却フォーマット

```text
削除: dev/62_xxx (/path/to/worktree)
削除: worktree-agent-abc123 (.claude/worktrees/agent-abc123) [Agent]
スキップ: dev/100_zzz (未コミット変更あり)
スキップ: worktree-agent-def456 (作業中) [Agent]
Killed: ship-parallel-20260405/ship-243 pane=%176 worktree=/path/to/missing
---
削除: 2件, スキップ: 2件, Killed: 1件, Skipped: 0件
```

## 🗑️ remove — 指定ワークツリーの手動削除

指定したブランチ名のワークツリーを削除する。

### ワークフロー

1. `git worktree list` から指定ブランチのパスを特定する。
2. 未コミット変更がないか確認する。
3. 未コミット変更がある場合はユーザーに確認を求める。
4. ワークツリーとローカルブランチを削除する。

```bash
git worktree remove <worktree_path>
```

```bash
git branch -d <ブランチ名>
```

`-d` で削除できない場合（未マージ）はユーザーに報告して停止する。`-D` は使用しない。

### 返却フォーマット

```text
削除: <ブランチ名> (<worktree_path>)
```

## 🧟 kill-zombies — ゾンビ tmux エージェントの自動 kill

ship-parallel が tmux ペインで起動した Agent は、対応する worktree が削除されると `cd: no such file or directory` のループに入り CPU を消費し続ける（Issue #253）。
このサブコマンドは `~/.claude/teams/*/config.json` を走査し、worktree が消えた tmux 連動エージェントの tmux ペインを検出して kill する。

### ワークフロー

実装は `.claude/lib/zombie_agent.sh` に集約されている。スキル実行時はこのスクリプトを呼び出すだけでよい。

```bash
bash "$CLAUDE_PROJECT_DIR/.claude/lib/zombie_agent.sh" kill
```

スクリプトの動作:

1. `~/.claude/teams/*/config.json` を全走査する。
2. `backendType == "tmux"` かつ `tmuxPaneId` 非空のメンバーを抽出する。
3. `prompt` から `worktree パス: <path>` をパースして worktree 絶対パスを取得する。
4. 該当パスのディレクトリが存在しない → ゾンビとして検出する。
5. tmux サーバーが起動しており該当ペインが残存している → `tmux kill-pane -t <paneId>`。
6. tmux ペインが既に消えている / tmux サーバー未起動 → スキップする。

### dry run（kill せずに一覧確認）

```bash
bash "$CLAUDE_PROJECT_DIR/.claude/lib/zombie_agent.sh" list
```

`<team>\t<member-name>\t<tmuxPaneId>\t<missing-worktree-path>` 形式で tab 区切り出力する。

### 返却フォーマット

```text
Killed: ship-parallel-20260405/ship-243 pane=%176 worktree=/path/to/missing
Skipped: ship-parallel-20260405/ship-244 pane=%177 (既に消滅 or tmux 未起動) worktree=/path/to/missing2
---
Killed: 1, Skipped: 1
```

## ⚠️ 制約

- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- `git branch -D`（強制削除）は使用しない。
- 未コミット変更があるワークツリーは自動削除しない。
- メインワークツリーは削除対象から除外する。

## 🔗 関連ルール

- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
