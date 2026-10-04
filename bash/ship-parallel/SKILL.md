---
name: ship-parallel
description: "複数Issueを並列shipするオーケストレーションスキル。SMエージェントで並列判定し、TeamCreate + 手動worktree + Agentで同時実行する。「/ship-parallel」「並列シップ」「まとめてship」と言った時に使用。"
---

**ultrathink**

# 🚢 並列 ship オーケストレーション

> [!IMPORTANT]
> このスキルは **複数 Issue を並列に `/vibecorp:ship` 実行する**。SM エージェントが Issue 群の依存関係を分析し、スキル実行者が TeamCreate + 手動 worktree + Agent で同時進行する。
> **full プリセット専用**。SM 並列判定が必要なため standard 以下では利用不可（`install.sh` が minimal/standard で物理削除する）。
> Agent 起動 mode は `bypassPermissions` を採用する（隔離レイヤ #293 が FS / network を OS レベルで縛るため安全）。
> 介入ポイントではユーザーの指示を待つ（自動でスキップしない）。1 つの Issue の失敗で他の並列実行を中断しない。

複数の Issue を並列に `/vibecorp:ship` 実行する。**SM エージェントが Issue 群の依存関係を分析**し、その結果に基づいてスキル実行者が TeamCreate + 手動 worktree + Agent で同時進行する。

**full プリセット専用**。SM エージェントによる並列判定が必要なため、standard 以下では利用不可。

## 使用方法

```bash
/vibecorp:ship-parallel <Issue URL 1> <Issue URL 2> [...]
/vibecorp:ship-parallel --all
```

- Issue URL を複数指定: 指定された Issue のみ対象
- `--all`: open な Issue を全て取得し、SM が選別

## 前提条件

- **full プリセット** であること（SM エージェントが必要）
- ベースブランチ（Issue 本文で指定されたブランチ、未指定時は現在のブランチ）を特定できること
- GitHub CLI (`gh`) が認証済みであること
- ベースブランチが最新であること

## 🏛️ アーキテクチャ

**TeamCreate + 手動 worktree + Agent** 方式を採用する。SM は分析専任、オーケストレーションはスキル実行者が直接実行する。

```text
スキル実行者（オーケストレーター）
  ├─ 1. Agent(SM) で Issue 群の並列判定を取得
  │     └─ SM が依存関係を分析し、並列グループ・直列チェーン・保留を返す
  ├─ 2. 実行計画をユーザーに提示・確認
  ├─ 3. 各 Issue の worktree を事前作成（git worktree add + rsync .claude/）
  ├─ 4. TeamCreate でチーム作成 + Agent で起動（各 Agent は /vibecorp:ship --worktree で実行）
  │     └─ Agent は指定された worktree パス内で全操作を実行
  ├─ 5. 各 Agent の進捗を SendMessage で監視
  │     ├─ エラー報告 → スキル実行者が判断（中断/リトライ/スキップ）
  │     └─ 完了報告 → 結果を記録
  ├─ 6. 並列 PR 間のコンフリクト検知
  └─ 7. 結果統合、レポート出力
```

### 方式選定理由

| 検証ポイント | 出典 |
|---|---|
| `Agent(isolation: "worktree")` は TeamCreate 下で機能しない | #127 検証 1 |
| 手動 worktree（`git worktree add` + `rsync .claude/`）で skills / hooks 同期が確実 | #127 検証 2 |
| TeamCreate + Agent（isolation なし）で SendMessage 双方向通信が可能 | #127 検証 3 |
| 複数 Agent 同時起動で worktree 間の完全分離を確認 | #127 検証 4 |
| `/vibecorp:ship --worktree <path>` でスキルチェーン全体が worktree 内で動作 | #128 で実装済み |
| SM は分析専任とし、`/vibecorp:sync-check` 等と同じ「分析エージェント → メイン実行」パターンに統一 | — |

## ワークフロー

### 1. プリセット確認

`vibecorp.yml` の `preset` を確認する。

```bash
awk '/^preset:[[:space:]]*/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml
```

`full` 以外の場合は「/vibecorp:ship-parallel は full プリセット専用です」と報告して終了する。

### 2. Issue 一覧の取得

**URL 直接指定の場合:**

各 URL から Issue 情報を取得する。

```bash
gh issue view <Issue URL> --json number,title,body --jq '{number, title, body}'
```

**`--all` の場合:**

open な Issue を一括取得する。

```bash
gh issue list --state open --json number,title,body,labels --limit 500
```

Issue が 1 件以下の場合は「並列実行の対象がありません。単一 Issue には `/vibecorp:ship` を使用してください」と報告して終了する。

### 3. SM エージェントによる並列判定

SM エージェントを Agent ツールで起動し、Issue 群の並列実行可否を判定させる。SM は分析結果のみを返し、オーケストレーションには関与しない。

SM エージェントが Agent ツールの利用可能タイプにない場合は、general-purpose エージェントに SM エージェント定義（`.claude/agents/sm.md`）の内容を渡して代用する。

SM に渡すプロンプトは `skills/ship-parallel/prompts/agent-call-sm-parallel-analysis.md` を参照する。

### 4. 実行計画の提示・ユーザー確認

SM の分析結果に基づき、スキル実行者が実行計画をユーザーに提示し、承認を求める。

```text
## 並列 ship 実行計画

### 並列グループ 1
| Issue | タイトル | 影響範囲 |
|-------|---------|---------|
| #10 | xxx | skills/foo/ |
| #11 | yyy | tests/test_bar.sh |

### 直列チェーン
| 順序 | Issue | タイトル | 依存理由 |
|------|-------|---------|---------|
| 1 | #12 | zzz | - |
| 2 | #13 | www | #12 と同一ファイル変更 |

### 保留（実行対象外）
| Issue | 理由 |
|-------|------|
| #14 | 影響範囲が不明 |

実行しますか？ (y/n)
```

ユーザーが承認しない場合は終了する。

### 5. worktree 作成・チーム組成・Agent 起動

承認後、スキル実行者が worktree を事前作成し、TeamCreate でチームを組成し、各 Issue に対して Agent を起動する。

#### 5a. チーム作成

```text
TeamCreate(team_name: "ship-parallel-{timestamp}")
```

#### 5b. ベースブランチの決定

Issue 本文にベースブランチの指定がある場合はそれを使用する。ない場合は現在のブランチを使用する。

#### 5c. worktree の事前作成

各 Issue に対して、オーケストレーター自身が worktree を作成する。

```bash
# プロジェクト名を取得
project=$(basename "$(pwd)")

# worktree を作成（ブランチも同時に作成）
git worktree add "../${project}.worktrees/dev_${Issue番号}_${要約}" -b "dev/${Issue番号}_${要約}"

# .claude/ ディレクトリを同期（skills, hooks, settings.json 等）
# state/ は worktree ごとに独自に作成・管理されるため除外（main の state を持ち込まない）
# plans/ は XDG 準拠で ~/.cache/vibecorp/plans/<repo-id>/ に配置されるため除外（旧 .claude/plans/ の残置ファイルを worktree に持ち込むと子 Agent が誤認して permission prompt で stuck する: #372）
rsync -a --exclude=state/ --exclude=plans/ .claude/ "../${project}.worktrees/dev_${Issue番号}_${要約}/.claude/"
```

worktree 作成の確認:

```bash
git worktree list
```

- 期待する worktree 数（メイン + 各 Issue）と一致すること
- worktree 作成が失敗した場合は該当 Issue をスキップし、他の Issue の処理は継続する

#### 5d. 並列グループの Agent 起動

並列グループ内の各 Issue に対して、Agent ツールを起動する。**同一グループの全 Agent は 1 つのメッセージで同時に起動する**（並列実行を最大化）。

Agent 起動時は `mode: "bypassPermissions"` を指定する。`/vibecorp:ship-parallel` は full プリセット専用配布であり、full プリセットは隔離レイヤ（#293: macOS `sandbox-exec` / Linux `bwrap`）が FS / network を縛る。隔離レイヤが最後の砦として機能している前提で、Agent 起動の承認ダイアログを `bypassPermissions` で完全に抑制する（隔離外への到達は OS 側で deny されるため安全）。これにより `--dangerously-skip-permissions` で起動した子 Claude と組み合わせて、並列実行時の承認介入を発生させない（参照: `docs/design-philosophy.md` の「承認フローへの非介入」、隔離レイヤ #293、#260）。

minimal / standard プリセットでは `install.sh` が `/vibecorp:ship-parallel` 自体を物理削除するため、`bypassPermissions` は配布されない（隔離レイヤ非提供環境で `bypassPermissions` を渡さないことを install.sh の skill 削除で担保している）。

各 Agent に渡すプロンプトは `skills/ship-parallel/prompts/agent-call-child-agent-ship.md` を参照する。

#### 5e. 直列チェーンの順序実行

直列チェーンがある場合、前の Issue の Agent が完了してから次の Issue の Agent を起動する。SendMessage で前の Agent の完了を確認し、成功していれば次を起動する。

### 6. 進捗監視・結果収集

TeamCreate + SendMessage によるリアルタイム監視を行う。

- 各 Agent の完了報告を SendMessage で受け取る
- エラー発生時は即座に通知される
- 必要に応じて介入が可能（中断・優先度変更・方針変更）

### 7. 並列 PR コンフリクト検知

並列グループの全 Agent が完了した後、PR 間のコンフリクトを検知する。

```bash
# 各 PR のブランチを順にマージして衝突を検出（ドライラン）
git merge-tree $(git merge-base HEAD <branch_a>) HEAD <branch_a>
```

- コンフリクトが検出された場合、対象 PR とファイルをユーザーに報告する
- 解消方法の提案（どちらを先にマージすべきか等）を提示する
- **自動解消は行わない** — ユーザーの判断を待つ

### 8. 結果報告

```text
## /vibecorp:ship-parallel 完了

### 成功
| Issue | PR | ブランチ |
|-------|-----|---------|
| #10 | #20 | dev/10_xxx |
| #11 | #21 | dev/11_yyy |

### 失敗
| Issue | 理由 |
|-------|------|
| #12 | テスト失敗（詳細: ...） |

### 保留（未実行）
| Issue | 理由 |
|-------|------|
| #14 | 影響範囲が不明 |

### 後始末
完了した worktree は `/vibecorp:worktree clean` で自動削除できます。
```

## 介入ポイント

以下の状況ではユーザーに報告して判断を委ねる。

| 状況 | タイミング |
|------|-----------|
| full プリセットでない | ステップ 1 |
| Issue が 1 件以下 | ステップ 2 |
| SM が全 Issue を保留に分類 | ステップ 3 |
| ユーザーが実行計画を承認しない | ステップ 4 |
| 個別の /vibecorp:ship が介入ポイントに到達 | ステップ 5 |
| 並列 PR 間でコンフリクト検出 | ステップ 7 |

## 制約

- **worktree 作成（`git worktree add`）が失敗した場合は該当 Issue をスキップ**し、他の Issue の処理は継続する
- `--force`、`--hard`、`--no-verify` は使用しない
- ユーザーの明示的な指示なしに force push しない
- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）
- 介入ポイントではユーザーの指示を待つ（自動でスキップしない）
- 1つの Issue の失敗で他の並列実行を中断しない

## 🔗 関連ルール

- 単一 Issue 用: `/vibecorp:ship`
- 自律改善ループ: `/vibecorp:autopilot`
- worktree 管理: `/vibecorp:worktree`
- Agent プロンプト: `skills/ship-parallel/prompts/agent-call-child-agent-ship.md`
- SM 分析プロンプト: `skills/ship-parallel/prompts/agent-call-sm-parallel-analysis.md`
- 隔離レイヤ設計: `docs/design-philosophy.md` の「承認フローへの非介入」/ #293 / #260
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
