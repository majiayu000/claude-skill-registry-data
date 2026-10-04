---
name: autopilot
description: "diagnose→ship の自律改善ループを1回実行する。Issue がなければ diagnose で起票し、あれば ship-parallel で実装する。「/autopilot」「自律改善」と言った時に使用。"
---

**ultrathink**

# 🤖 自律改善ループ

> [!IMPORTANT]
> このスキルは `/vibecorp:diagnose` → `/vibecorp:ship-parallel` のサイクルを **1 回だけ** 実行する。
> 起票済み Issue は **起票側の 3 者承認ゲート（CISO + CPO + SM）** を信頼し、ship 側で再フィルタしない。
> main への直接 push は **一切発生しない**（knowledge/buffer 反映は auto-merge 経由）。
> 介入ポイントではユーザーの指示を待つ（自動でスキップしない）。

`/vibecorp:diagnose` → `/vibecorp:ship-parallel` のサイクルを 1 回実行する。定期実行は `/loop 12h /vibecorp:autopilot` で行う。

## 使用方法

```bash
/vibecorp:autopilot              # ship 前にユーザー確認（デフォルト）
/vibecorp:autopilot --auto       # 確認なしで全自動
/loop 12h /vibecorp:autopilot    # 12時間ごとに定期実行（確認あり）
```

## 前提条件

| 項目 | 内容 |
|---|---|
| プリセット | **full プリセット専用**（`/vibecorp:diagnose` と `/vibecorp:ship-parallel` が必要） |
| ブランチ | main ブランチにいること |
| 隔離レイヤ | full プリセットは macOS `sandbox-exec` / Linux `bwrap` による隔離レイヤ（#293）を提供する。本スキルが委譲する `/vibecorp:ship-parallel` は Agent 起動時に `mode: "bypassPermissions"` を指定して承認ダイアログを抑制するが、隔離レイヤが FS / network 境界を OS レベルで強制するため安全に動作する |
| 対象 Issue | open な全 Issue（ラベル問わず）。不可領域フィルタ（認証 / 暗号 / 課金構造 / ガードレール / MVV）は起票側（`/vibecorp:diagnose` と `/vibecorp:issue`）の 3者承認ゲートで実施済みであり、ship 側は起票済み Issue を信頼して実行する |
| diagnose ラベル | 自体は **起票経路の識別用途** として残る（`/vibecorp:diagnose` が付与）。ship 可否の判定には使わない |
| knowledge/buffer フロー | ship 後に `/vibecorp:review-harvest` → `/vibecorp:knowledge-pr` を実行する。main への反映は必ず auto-merge 経由（`/vibecorp:knowledge-pr` が PR を起こして CodeRabbit + CI を通す）。main への直接 push は一切発生しない |

## ワークフロー

### 1. プリセット確認

```bash
awk '/^preset:[[:space:]]*/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml
```

`full` 以外の場合は「/vibecorp:autopilot は full プリセット専用です」と報告して終了する。

### 2. ブランチ確認

```bash
git branch --show-current
```

main でない場合は「main ブランチに切り替えてください」と報告して終了する。

### 3. open な Issue を確認

ラベル問わず全 open Issue を対象とする（`/vibecorp:diagnose` 起票分も `/vibecorp:issue` 起票分も同じパイプで処理する）。

```bash
gh issue list --state open --json number,title --jq '.[] | "#" + (.number | tostring) + ": " + .title'
```

### 4. Issue がない場合 → diagnose 実行

open な Issue が 0 件の場合（ラベル問わず全 open Issue を対象に判定）、`/vibecorp:diagnose` を実行して Issue を起票する。起票後、そのままステップ 5 に進む（起票した Issue を ship する）。

### 5. SM による並列判定

SM エージェントに Issue 群の並列実行可否を判定させる（`/vibecorp:ship-parallel` のステップ 3 と同じ）。

SM の分析結果に基づき、並列グループ・直列チェーン・保留に分類する。保留と判定された Issue は候補から除外する。

### 6. ship 確認・実行

#### 6a. デフォルト（確認あり）

SM の分析結果と候補一覧をユーザーに提示する。

```text
## /vibecorp:autopilot 改善候補

| # | Issue | タイトル |
|---|-------|---------|
| 1 | #218 | block-api-bypass.sh の専用テスト |
| 2 | #219 | install.sh の lock ファイル空リスト |

ship する Issue の番号を指定してください（例: 1,2）。
全て ship: all / スキップ: skip
```

AskUserQuestion でユーザーの選択を取得する。

- `skip` → 「スキップしました」で終了
- 番号指定 or `all` → 選択された Issue を `/vibecorp:ship-parallel` で実行

#### 6b. `--auto` モード

ユーザー確認なしで、SM の分析で通過した全候補（ラベル問わず）を `/vibecorp:ship-parallel` に渡す。

### 7. knowledge/buffer の収集 → PR 化

ship 実行（またはスキップ）後、蓄積されたレビュー指摘と会話差分を main に反映する。

```bash
/vibecorp:review-harvest    # 前回収集以降のマージ済み PR からレビュー指摘を収集
/vibecorp:knowledge-pr      # knowledge/buffer の差分を Issue 起票 → PR 作成 → auto-merge
```

- いずれも失敗しても autopilot 全体は成功扱い（main 直接 push は発生しない）
- `/vibecorp:review-harvest` が exit 3（push 失敗）した場合は `/vibecorp:knowledge-pr` を skip して人手復旧を促す
- `/vibecorp:knowledge-pr` は重複 Issue チェックで自動 skip される

### 8. 結果報告

```text
## /vibecorp:autopilot 完了

- 対象 Issue: {n}件（うち diagnose 起票: {n}件 / 手動起票: {n}件）
- ship 実行: {n}件
- スキップ: {n}件
- review-harvest: {処理 PR 数 / skip 理由}
- knowledge-pr: {PR 番号 / skip 理由}
```

## 制約

- `--force`、`--hard`、`--no-verify` は使用しない
- ユーザーの明示的な指示なしに force push しない
- **jq では string interpolation `\(...)` を使わない** — 必ず `+` で結合する（[根拠](docs/design-philosophy.md#jq-string-interpolation-の禁止)）
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）
- デフォルトでは ship 前にユーザー確認を挟む（`--auto` で解除可能）

## 🔗 関連ルール

- 起票側 3 者承認ゲート: `/vibecorp:diagnose` / `/vibecorp:issue`
- 並列 ship: `/vibecorp:ship-parallel`
- knowledge 反映: `/vibecorp:review-harvest` / `/vibecorp:knowledge-pr`
- ガードレール領域: `.claude/rules/autonomous-restrictions.md`
- CEO 報告向け文面規約: `.claude/rules/communication.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
