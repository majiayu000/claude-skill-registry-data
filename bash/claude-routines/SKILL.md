---
name: claude-routines
description: Claude Code routine(claude.ai 上の scheduled cloud agent)を、各対象リポジトリの `.claude/routines/<name>.{json,md}` を正本として as-code で扱う手順。routine を作る・routine を編集・cron を変更・routine を移行・既存の routine を宣言に取り込む・routine が UI で編集された、といった文脈で使う。schedule a routine, declare a routine as code, adopt an existing routine, routine drift、といった英語の文脈でも使う。クラウド側の定期監査手順は auditor.md を参照(このファイルはローカルセッションでの create/adopt/apply を扱う)。
---

Claude Code routine は今のところ `claude.ai/code/routines` の Web UI /
`/schedule` / `RemoteTrigger` で個別に作るしかなく、定義(prompt・cron・
対象 repo)がどこにも版管理されない。このスキルは、routine の設定と
prompt 本体を対象リポジトリの `.claude/routines/` 配下のファイルに正本化し、
live 側(claude.ai)をその宣言に追従させる。

設計と根拠: `docs/adr/519-routines-declaration-in-repo.md`、
`docs/claude/claude-routines.md`。差分計算は
`scripts/routines-plan.sh`(bash + jq、決定的)に固定している — 手で
JSON body を組み立てない。

## 宣言スキーマ

対象リポジトリの `.claude/routines/<name>.json` + 同名の `.md`:

```json
{
  "name": "daily-brief",
  "id": "trig_…",
  "state": "enabled",
  "cron_utc": "0 22 * * *",
  "model": "claude-sonnet-5",
  "environment_id": "env_…",
  "home_repo": "owner/repo",
  "sources": ["owner/repo"],
  "allowed_tools": ["Bash"],
  "role": "worker"
}
```

- `id` は初回 create 後にこのスキルが書き戻す値。手で作らない。
- `state` は閉語彙 `enabled|disabled|retired`。`retired` は
  `enabled:false` を維持したまま宣言ファイルを残す(delete API が
  無いため — D8)。
- `cron_utc` は UTC 解釈の 5 フィールド cron。run-once/webhook trigger は
  このスキーマで表現できない(意図的 — D11)。
- `home_repo` は宣言が住む repo。`sources` からは導出しない —
  `sources` が空(prompt 内で手動 clone する routine)の実例があるため。
- `auto_mode_allow`/`auto_mode_environment` は任意(文字列の配列)。cloud routine の auto mode の
  分類器に、共有の資源への書き込みなどを許す散文の規則を渡す。値の順序を保ち、**`"$defaults"` を
  先頭に置く**(置かないと、その節の組み込みの規則がすべて置き換わる)。空なら射影に載せない
  (既存の宣言のハッシュが変わらない)。**live は、この経路を受け付けない**(2026-10-22 に実測。update の
  あとの `get` で `session_request.config.auto_mode_allow` が `[]` のまま)。受理される経路が分かる
  まで、宣言に書かない(書くと `classify` が毎回 declared-ahead になる)。設計と実測は
  `docs/claude/claude-routines.md`。
- `connectors`/`mcp_connections` は宣言に含めない —
  アカウント全体で共通の既定セットで、routine ごとの管理対象ではない。
- `<name>.md` は prompt 本体(routine-spec 注記行は書かない — build-body が
  自動で付ける)。live prompt からは `Read and follow
  .claude/routines/<name>.md in <home_repo>.` という薄いポインタに
  展開される。

## 新規 routine を作る

1. `.claude/routines/<name>.json`(`id` は書かない)と `<name>.md` を書く。
2. body を組み立てる:
   ```
   bash scripts/routines-plan.sh build-body \
     --declaration .claude/routines/<name>.json --md .claude/routines/<name>.md
   ```
3. その body をそのまま `RemoteTrigger`(action: create)に渡す。
   加工しない — 決定的 CLI の出力を信じる。
4. 応答の `trigger.id` を宣言ファイルの `id` に書き戻し、同じ commit に含める。
5. この repo が private なら、Claude GitHub App の install 先に含まれて
   いるか確認する(`docs/claude/claude-routines.md`「クラウド到達範囲」
   節)。含まれていなければ cloud routine はこの repo を clone できない。

## 既存の routine を宣言に取り込む(adopt)

Web UI や旧来のやり方で作った routine を正本化するとき。

1. `RemoteTrigger get <id>` で現在の内容を取得する。
2. その内容から `.claude/routines/<name>.json`(`id` はこの既存 ID)と
   `<name>.md`(prompt 本体。live 側に routine-spec 注記があれば除いた本文)
   を書き起こす。`sources`/`allowed_tools`/`model`/`cron_expression`
   (→ `cron_utc`)/`environment_id` はそのまま転記する。
3. 現状を反映させる update を送る(下記「宣言を適用する」と同じ手順)。
   これで live の prompt に routine-spec 注記が付き、以後は差分検出の
   対象になる。

## 宣言を適用する(update)

1. 現在の live を取得する: `RemoteTrigger get <id>` → ファイルに保存。
2. 分類する:
   ```
   bash scripts/routines-plan.sh classify \
     --declaration .claude/routines/<name>.json --md .claude/routines/<name>.md \
     --live <get の生 JSON>
   ```
   `get` の応答は `{"trigger": {...}}` の形。そのまま保存して渡してよい
   (`classify` が `.trigger` を取り出す)。
3. 出力の1行目が分類名。
   - `in-sync`: 何もしない。
   - `declared-ahead`: 2行目以降が update body。そのまま `RemoteTrigger`
     (action: update)に渡す。
   - `live-drift`: live 側が UI 等で編集されている。宣言へ上書きしない —
     人が「宣言に取り込む(adopt し直す)」か「live を戻す」かを判断する。
   - `conflict`: 宣言と live の両方が注記から乖離している。同上、人が判断する。
   - `suspended`: `suspension_reason`/`ended_reason` が非空。自動で
     再有効化しない — 原因を確認してから手で対処する。
   - `refuse`: 注記が無い、または live の `name` が
     `<home_repo>:<name>` と一致しない。adopt からやり直す。理由(注記が無い /
     名前の不一致 / 入力の形)は標準エラーに 1 行出る。
   - `new`: 宣言に `id` が無い。「新規 routine を作る」の手順に進む。

## 廃止する(retire)

`state` を `retired` に変え、上記「宣言を適用する」で update する
(`enabled:false` になる)。宣言ファイルは消さない — delete API が
無いため、消すと live 側に孤児が残る(D8)。

## ローカルの宣言外書き込みは guard が塞ぐ

`crates/routines-write-guard`(PreToolUse、`RemoteTrigger` の cron 付き
create/update を対象)が、名前空間キー + routine-spec 注記という構造を
満たさない body を deny する。このスキルの `build-body`/`classify` が
出す body は常にこの構造を満たすため、正規の手順では guard に当たらない。
