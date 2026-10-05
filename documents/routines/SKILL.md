---
name: routines
description: >
  クラウドルーティン（/schedule で作成する RemoteTrigger 定期エージェント）を一覧・監査する。
  重複（同一成果物を生成する routine）・残骸 one-shot（self-disable 漏れ）・平文シークレット・
  cron 衝突・無効ルーティンを検出してレポートする。新規 routine を作る前の重複チェックにも使う。
  Use when user asks to [ルーティン一覧, ルーティン監査, クラウドルーティン確認, routine 重複チェック, スケジュール一覧, /routines].
domain: ops
---

クラウドルーティン（claude.ai の RemoteTrigger / `/schedule` で作る定期エージェント）を list して監査する Evaluator 系スキル。

状態は **repo にもローカルにも存在せず、唯一の真実源はクラウド側の `RemoteTrigger list`**。別セッションで作られた routine はコンテキストに痕跡を残さないため、能動的に取得して可視化しないと存在を把握できない。

## 最重要ルール（重複事故の再発防止）

**`/schedule` で routine を新規作成する前に、必ず本スキル（または `RemoteTrigger {action:"list"}`）で既存を確認する。** 同一 repo × 同一成果物（生成ファイルパス／目的）を作る routine が既にあれば、新規作成せず既存を `update` する。

> 背景: 2026-05-30 に既存の `doboku-note weekly PDCA` を確認せず `doboku-weekly-review` を新規作成し、`docs/reviews/weekly/*-review.md` を二重生成する重複を起こした。create 前の list-first を怠ったのが原因。

## ツール準備

`RemoteTrigger` は deferred tool。先に読み込む:

```
ToolSearch { query: "select:RemoteTrigger" }
```

## 手順

1. `RemoteTrigger { action: "list" }` で全ルーティンを取得。
2. 各ルーティンを解析する（`job_config.ccr.session_context.sources` の repo、`cron_expression`、`enabled`、`run_once_at` / `ended_reason`、`events[].data.message.content` の本文）。
3. 下記ルールで問題を検出する。
4. **repo（プロジェクト）別**にグルーピングして表で報告。cron は **JST 併記**（UTC+9）。問題は優先度付きで surface。

### 検出ルール

- **重複（最優先）**: 同一 repo かつ本文中の生成ファイルパス／目的が重なる（例: 複数 routine が `docs/reviews/weekly/*-review.md` を生成）。
- **残骸 one-shot**: `ended_reason == "run_once_fired"` なのに `enabled == true`、または本文に「one-off」「self-disable」「実行後に自分を disable」とあるのに `enabled == true` で次回 fire が将来日付。
- **平文シークレット**: 本文に `ACCESS_TOKEN` / `API_KEY` / `SECRET` / `PASSWORD` / `Bearer ` や 20 文字以上連続の英数字トークンらしき文字列。露出リスクとして警告。
- **cron 衝突 / 近接**: 同一 repo で同一時刻帯（同 UTC hour）に複数が fire。リソース競合・PR 衝突の懸念。
- **無効ルーティン**: `enabled == false` を棚卸し（不要なら手動削除候補）。

## 出力フォーマット

```markdown
## クラウドルーティン監査（YYYY-MM-DD）

### {repo} （N 個）
| ルーティン | cron(JST) | 役割 | 状態 |
|---|---|---|---|

### 検出された問題
- [重複] ...
- [残骸 one-shot] ...
- [平文シークレット] ...
- [cron 衝突] ...

### 推奨アクション
- ...
```

## 制約

- 本スキルは **surface のみ（Evaluator）**。`disable` / `update` の実行はユーザー承認後に行う。
- routine の **削除は API 不可**。https://claude.ai/code/routines で手動削除する。
- 修正が必要なら `RemoteTrigger {action:"update", trigger_id, body:{enabled:false}}` 等を別途ユーザー判断で実行。
- **平文シークレットは値そのものをレポートに転記しない**（「token らしき文字列を検出」とだけ書く）。

## 参照

- `.claude/skills/management/weekly-review/SKILL.md` — 重複事故の当事者（正典は `doboku-note weekly PDCA` routine）
- 新規作成は built-in の `/schedule` スキル。create 前に必ず本スキルで list-first する
