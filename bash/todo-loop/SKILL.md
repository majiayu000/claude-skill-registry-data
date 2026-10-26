---
name: todo-loop
description: プロジェクトの TODO.md を、無人のセッションで 1 SP ずつ消化するループを起動・確認・停止する。実行できるストーリーが尽きたら lens-next で 10 案を出し、上位 3 件を 1 SP ずつに分解して積み足して続ける。時刻を指定した連続実行（「14 時の着手で終わり」）と、利用上限が明けたら同じ SP から再開する機能つき。「TODO 作って消化して」「〇時まで回して」「TODO 消化ループ」「上限明けも復帰して」と言われたとき、または「ループ止めて」「ループどうなってる」に使う。引数 = <プロジェクトのパス> [until=HH:MM] [end=HH:MM] [lens=<観点のファイル / URL / 文>] | status <パス> | stop <パス>
---

# todo-loop

`<プロジェクト>/TODO.md` のストーリーを、1 SP = 1 セッションの無人の `claude -p` で上から消化する。
runner の本体は `scripts/run.sh`、各セッションへの指示書は `scripts/story-prompt.md`（消化）と `scripts/refill-prompt.md`（積み足し）。
報告 PDF は `scripts/report.py`、材料台帳は `scripts/ledger.py`、定時の雛形は `scripts/schedule.sh` と `templates/launchd.plist.tmpl`。
状態は `<プロジェクト>/.local/todo-loop/`（以下 `<状態>`。`runs/` に回ごとのログと `history.log`、`progress/` に進捗ファイル、`reports/` に報告、`ledger/` に台帳、`running.pid`、`drive.out`）。

## プロジェクトごとの設定（すべて `<状態>/` に置く。どれも無ければ従来の動作）

プロジェクト固有の値・処理はここに置き、本体（`plugins/todo-loop/`）には書かない。

| ファイル | 役割 | いつ使われるか |
|---|---|---|
| `lens` | 1 行目が積み足しの観点（パス・URL・文）。`TODO_LOOP_LENS` が優先 | 積み足し（`passes/` が無いとき） |
| `passes/<NN>_<名前>/lens` | 観点の複数回。番号順に 1 回ずつ lens-next を回す。回ごとに TODO.md を検査し、崩れた回だけその回の前に戻す | 積み足し（あれば `lens` より優先） |
| `passes/<NN>_<名前>/prompt-addon.md` | その回の指示書の末尾に足す | その回 |
| `passes/<NN>_<名前>/pre.sh` | その回の直前にプロジェクトのディレクトリで実行（観点を作り直す）。失敗しても前の観点で続ける | その回の直前 |
| `pre-refill.sh` | 積み足しの直前に 1 回実行（passes の前） | 積み足しの直前 |
| `pre-run.sh` | 起動ごとに 1 回、ストーリーを選ぶ前に実行（別の実行先への送り出し・戻りの取り込みの受け口）。失敗しても続ける。DRY では実行しない | 起動の最初 |
| `story-addon.md` | 消化の指示書（story-prompt.md）の末尾に足す | 各ストーリー |
| `refill-addon.md` | 積み足しの指示書（refill-prompt.md）の末尾に足す | 積み足しの各回 |
| `collect.sh` | 材料台帳の材料を JSON 行（`{"text", "kind"?, "id"?, "at"?}`）で標準出力に出す。これか `ledger/` があると台帳を使う | 積み足しの直前 |
| `send.sh` | 送信。`send.sh <run\|create> <PDF のパス or 空>` に本文を標準入力で渡す。無ければ repo の `.local/todo-loop/notify.sh`（本文だけ）、それも無ければ送らない | 起動の終わり・利用上限の待ち |
| `launchd/` | `scripts/schedule.sh` が書き出す定時の plist（登録は人が行う） | — |

## 同梱の観点（`lenses/`）

どのプロジェクトにも当てられる観点。プロジェクトの観点とは別の回として `passes/` に足す（既存の `lens` は `passes/01_<名前>/lens` へ移す。passes があると `lens` は読まれない）。

| ファイル | 探索の向き |
|---|---|
| `lenses/sources.md` | 信頼できる情報源を増やし、1 本の情報源への依存を減らす（判断ごとの情報源の偏りを数え、性質の違う 2 本目を道具に組み込む） |

付け方: `passes/<NN>_sources/lens` の 1 行目に `lenses/sources.md` のパス（repo ルートからの相対）を書き、そのプロジェクトの今の情報源の置き場・既知の偏りを `passes/<NN>_sources/prompt-addon.md` に書く（本体の観点にはプロジェクト固有の名前を書かない）。足したら `TODO_LOOP_DRY=1 TODO_LOOP_REFILL_ONLY=1` で回の一覧を出して確かめる（DRY は回と観点を出すだけで、前処理も claude も走らせない）。

## 起動するとき

1. **引数を決める。** 足りない値は聞かずに既定で埋め、報告に書く。
   - `until`: この時刻を過ぎたら新しいセッションを始めない（その直前に始まった回が最後）。無ければ 1 件だけ実行して終わる。
   - `end`: 各セッションをこの時刻で打ち切る。無ければ `until` の 1 時間後。
   - `lens`: 積み足しの観点。`<状態>/passes/` か `<状態>/lens` があれば、それを runner が読むので `TODO_LOOP_LENS` を渡さない（上の表）。無ければ、プロジェクトに `TODO-lens.md` があればそれ。無ければ user の言葉から 1 枚書く（「何を良くしたいか」を 3〜10 行。user が観点を言っていなければ、プロジェクトの CLAUDE.md の目的から書き、`<プロジェクト>/TODO-lens.md` に置く）。
2. **TODO.md を用意する。** 無ければ `templates/TODO.md` を写し、`{{目的}}` と「積まない物」をそのプロジェクトの CLAUDE.md から埋める。あれば運用節の見出しの書式（`## S-NN — <項目> | <調査|実装> | <fable|opus> | <状態>`）が runner と同じかだけ確かめる。
3. **二重起動を避ける。** `<プロジェクト>/.local/todo-loop/running.pid` の pid が生きていれば起動しない（status を返す）。別のセッションが同じ TODO.md に積んでいる最中なら、`python3 heaven/tools/peers.py --grep <プロジェクト名>` で確かめ、積み終わるまで待つ（積み足しと番号がぶつかる）。
4. **dry-run で最初の 1 件を確かめる**: `TODO_LOOP_DRY=1 bash <skill>/scripts/run.sh <プロジェクト>`。
5. **起動する**（端末を閉じても残るように nohup。セッションの終了で止まらない）:
   ```bash
   mkdir -p <プロジェクト>/.local/todo-loop && touch <プロジェクト>/.local/todo-loop/drive.out
   nohup env TODO_LOOP_UNTIL=<until> TODO_LOOP_END=<end> TODO_LOOP_LENS=<lens> \
     bash <skill の絶対パス>/scripts/run.sh <プロジェクトの絶対パス> \
     >> <プロジェクトの絶対パス>/.local/todo-loop/drive.out 2>&1 &
   ```
6. **動いたことを確かめてから報告する**: 10 秒後に `running.pid` の pid が生きていて親が 1 になっていること、`runs/` に最初の回のログがあること、TODO.md の該当ストーリーが選ばれていること（`drive.out` の「選択:」行）。報告には pid・最初のストーリー・終わる条件・止め方を書く。

## status / stop

- status: `running.pid` の生死、`drive.out` の末尾、`runs/history.log` の末尾 5 行、TODO.md の状態ごとの件数を出す。
- stop: `running.pid` の pid を `kill` し、走っている回の `claude -p` は `pgrep -fl "ストーリー ID: S-"` で該当 pid を見て `kill <pid>`（名前で一括に止めない）。止めた回のストーリーは `doing` のまま残り、次の起動で進捗ファイルから続く。

## 定時にするとき

- **既定は時刻での自動起動なし。** runner は明示して呼んだときだけ動く（この Skill の起動・手で打つ `run.sh`）。定時は、欲しいプロジェクトが user の指示で有効にするときだけ設定する。user が定時を頼んでいないのに、起動のついでに定時を書き出したり勧めたりしない。
- `bash <skill>/scripts/schedule.sh <プロジェクト> <HH[:MM],...> [--refill-only] [--env KEY=VALUE ...]` で `<状態>/launchd/<ラベル>.plist` を書き出す。
  `--refill-only` は積み足しだけの定時（`TODO_LOOP_REFILL_ONLY=1`。passes があれば全部の回を回す）。消化の定時は `--env TODO_LOOP_UNTIL=HH:MM` 等を足す。
- 道具は launchctl を呼ばない。表示された登録の手順は常駐登録なので、user が行う（無人セッションでは `launchctl` を止めている）。

## 採点（opt-in）

無人セッションが書いた 証跡 を、作業者と別のモデルに再実行させて確かめる（`scripts/grade.sh`）。既定は off。

- 1 件: `bash <skill>/scripts/grade.sh <プロジェクト> story <S-NN> [--note]`。前回の採点以降に done になった全件: `bash <skill>/scripts/grade.sh <プロジェクト> batch`（常に `--note` 相当）。
- runner から: `TODO_LOOP_GRADE=1` を付けて起動すると、`done` になった回ごとに `grade.sh story <ID> --note` を呼び、結果の 1 行を報告の本文に `（採点）…` として足す（stderr は `<状態>/runs/grade.err`）。定時にするなら `schedule.sh` に `--env TODO_LOOP_GRADE=1`。
- 採点者: 既定は Codex（`codex exec`）。見つからなければ作業者（見出し 4 列目）と違う Claude モデル（opus → sonnet、それ以外 → opus）。`TODO_LOOP_GRADER=codex|claude` と `TODO_LOOP_GRADE_MODEL` で差し替える（作業者と同じモデルは終了コード 3）。
- 結果: `<状態>/audits/<YYYY-MM-DD>_<ID>[_<TAG>].md`。最終行が `判定: 合格|不一致|判定不能`、終了コードは 0 / 1 / 2（3 は引数・ストーリーの誤り）。batch の台帳は `audits/graded.tsv`。
- `--note` では、不一致のとき 引き継ぎ 欄に `採点: 不一致（<監査ファイル>）。` を 1 回だけ追記する。見出しの状態は変えない（直すかどうかは人が決める）。
- そのほかの環境変数（`TODO_LOOP_GRADE_*`）は `grade.sh` の先頭コメントにある。

## runner の振る舞い（説明を求められたとき・設定を変えるとき）

- 選び方: `doing` があればそれ → 無ければ上から、`todo` / `approved` で依存がすべて済んだもの。`blocked` / `needs-user` / `awaiting-approval` は飛ばす。
- 1 セッションの打ち切り 3600 秒（`TODO_LOOP_LIMIT_SEC`）、`end` までの残りに縮める。打ち切り・途中終了は `doing` に戻して次の回が進捗ファイルから続ける。2 回続いたら残りを分け直させ、4 回で `blocked`。時刻指定が無ければ `TODO_LOOP_COUNT` 件（既定 1）で終わる。
- 利用上限: メッセージの「resets 3pm」の時刻（読めなければ 3 時間後）＋2 分まで待ち、同じストーリーを続きから。再開が `until` 以降なら止める。上限の回は中断回数に数えない。passes の途中で上限に当たったら、残りの回は見送る。
- 積み足し: 回ごとに、末尾追記・見出しが読める・ID の重複 0・U+FFFD 0・1 件以上増えた、のどれかが崩れたら TODO.md をその回の前に戻す（`history.log` に `refill <回> ok|fail|limit`）。積み足しの後に 1 件も実行できなければ止まる（空回りしない）。
- 報告: 各セッションは `<状態>/reports/<run|create>/<起動の時刻>/` に 8 項目の JSON（課題・やったこと・まとめ・つまづいたこと・工夫したところ・何が嬉しいのか・発展可能性・完了したかどうか）を書き、`report.py check` が OK になるまで直す。runner は起動の終わりに `report.py build` で PDF にする（報告の無いストーリーは TODO.md から補完し「報告なし」と明記。末尾に毎回、承認待ちの一覧と各ストーリーの 外部作用 欄）。Chrome は `TODO_LOOP_CHROME` → macOS の標準の位置 → PATH の chromium / google-chrome の順に探し、無ければ HTML だけ作る。`TODO_LOOP_NO_REPORT=1` で作らない。
- 材料台帳（育つ機構の入力）: `collect.sh` の材料と、`history.log` から本体が足す材料（同じストーリーの中断 2 回以上・blocked 化・積み足しの失敗）を `<状態>/ledger/pending.jsonl` に番号つきで貯める（`ledger.py`）。積み足しのセッションは `ledger/pending.md` を観点と合わせて読み、ストーリーの `- 範囲:` に材料の番号を書く。書かれた番号は次の sweep で `resolved.jsonl` に移る。ランナー自身（設定・足し書き・道具）の直しは `awaiting-approval` のストーリーとして積み、外部作用 欄に差分を書く（本体に効く直しはそう明記）。
- 無人セッションでは commit・push・gh・launchctl・crontab・sudo・公開・Discord 投稿を `--disallowedTools` で止める。外部に出る操作は `awaiting-approval` で止まり、user が見出しを `approved` に書き換えた回だけ実行する。
- 採点: `TODO_LOOP_GRADE=1` のときだけ、`done` になった回の直後に別のモデルで採点する（上の「採点（opt-in）」）。不一致でも状態は変えず、引き継ぎ 欄に追記するだけ。
- 試験: `bash <skill>/tests/run_tests.sh`（偽の claude と一時ディレクトリだけで全機能を確かめる。実の TODO.md・claude には触れない）。
