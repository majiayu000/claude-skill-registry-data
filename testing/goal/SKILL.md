---
name: goal
description: アプリの「全機能 → ユーザーストーリー＋期待挙動 → テスト」を1枚のカバレッジ台帳(CSV)で一元管理しながら自走する2段階ループ。Phase1=機能を読み込み台帳を作る(設計)、Phase2=全ストーリーをテストし結果/不具合/再テストを台帳に書き戻す(検証)。RED-first + 自律完了。引数 = <対象 project/app パス ＋ (任意)スコープ>
---

# goal — 2段階カバレッジ・テストループ（設計 → 検証 を自走）

`$ARGUMENTS` で指定された対象アプリに対し、**「全機能をユーザーストーリー化して1枚の台帳で管理し、その全ストーリーをテストする」**を
自走で回す。Codex の `/goal` に「2段階ループ」を渡す手法（出典: x.com/so_ainsight/status/2069065387866747075）を
この harness の primitive（autorun / RED-first / bug-fix / Workflow）に載せ替えたもの。

`$ARGUMENTS` の解釈:
- 先頭トークン = 対象 project/app（例 `projects/dashboard` / `projects/dashboard/apps/dashboard`）。省略時は1つだけ確認する。
- 残り = スコープ限定（任意。例 `--scope api` `--area Anomaly` `--max 12`）。指定が無ければ**全機能**が対象（重い場合は下の「規模ゲート」参照）。

この skill を呼んだ時点で、下の autorun 契約は standing 承認とみなしてよい（毎回の確認は不要）。

---

## 成果物: カバレッジ台帳（1枚の CSV）

対象の `outputs/coverage-ledger.csv` に**1機能=1行**で書く（既存があれば追記/更新。新規なら header から作る）。
列はツイートの台帳と同じ18列（スプレッドシートとして Numbers/Excel で開ける）:

```
story_id,kind,area,feature,route_api,source_files,user_story,expected_behavior,priority,test_type,feature_status,baseline_status,baseline_evidence,defect_id,defect_summary,fix_status,retest_status,retest_evidence,dependencies
```

| 列 | 意味 | 取りうる値 / 書き方 |
|---|---|---|
| `story_id` | 一意ID | `API-001` `PAGE-001` `MOD-001` `CLI-001` `WIDGET-001`（kind 別連番） |
| `kind` | 機能の種別 | `api` `page` `cli` `module` `widget` `manual` |
| `area` | 機能ドメイン | 自由（例 `Anomaly` `Cost` `Sessions` `Pending`） |
| `feature` | 機能名（短く） | 例 `weekly digest` |
| `route_api` | 入口 | `GET /api/snapshot` 等。module なら関数/クラス名 |
| `source_files` | 実装ファイル | `;` 区切り。repo-root 相対 |
| `user_story` | 利用者視点 | `<利用者>として、<X>したい。なぜなら<Y>` |
| `expected_behavior` | **検証可能**な期待挙動 | 観測できる具体（「200 と {keys:...} を返す」「stale 時に最終取得時刻を出す」） |
| `priority` | 重要度 | `P0`(壊れると致命) `P1` `P2` |
| `test_type` | テスト種別 | `unit` `integration` `e2e` `manual` |
| `feature_status` | 実装状況 | `implemented` `partial` `missing` `documented` |
| `baseline_status` | 現状のテスト結果 | `pass` `fail` `untested` `no-coverage`（テスト自体が無い） |
| `baseline_evidence` | 根拠 | test 名 / curl 出力要約 / 観測。**捏造禁止・実観測のみ** |
| `defect_id` | 不具合ID | `DEF-001` or 空 |
| `defect_summary` | 不具合要約 | 1行 |
| `fix_status` | 修正状況 | `n/a` `open` `fixed` `wontfix` |
| `retest_status` | 再テスト | `n/a` `pass` `fail` |
| `retest_evidence` | 再テスト根拠 | 実観測のみ |
| `dependencies` | 依存 | 他 `story_id` / 外部サービス |

CSV エスケープ: 値に `,` `"` 改行が入るなら `"` で括り内部の `"` は `""`。`user_story` / `expected_behavior` は必ず括る前提でよい。

---

## Phase 1 — DISCOVER（設計: 機能 → ストーリー → 台帳）

**手を止めず**、対象の全機能を洗い出して台帳の行を作る。テストはまだしない（baseline_status は全行 `untested` か `no-coverage`）。

1. **機能の棚卸し**（種別ごとに網羅）:
   - `api`: route/endpoint 定義を grep（FastAPI なら `@app.(get|post|...)`、他 framework は router 定義）。
   - `page` / `widget`: テンプレート・フロント・UI コンポーネント。
   - `cli`: `__main__` / argparse / `Taskfile` / `tools/*.sh` のサブコマンド。
   - `module`: 公開関数/クラスのうち**利用者価値を持つ振る舞い**（内部ヘルパは1機能に畳む）。
2. 各機能に **user_story** と**検証可能な** expected_behavior を書く（観測できない曖昧な期待は書かない）。
3. `priority` / `test_type` / `feature_status` / `dependencies` を埋める。
4. **既存テストとの突合**: 対象の `tests/` を見て、その機能を覆うテストが在るかで `baseline_status` を
   `untested`(在るが未実行) か `no-coverage`(テスト不在) に分ける。← **これが本手法の主産物（カバレッジ穴の可視化）**。
5. 台帳 CSV を書き出す。ここまでが Phase 1。

> **規模ゲート**: 対象が大きく（route+module が概ね40超）全機能を1セッションで回すとトークンが嵩むときは、
> (a) `--scope` / `--area` / `--max` でスライスして回すか、(b) Phase 2 の fan-out を `goal-loop` workflow に上げる。
> どちらも user の合図で。スライスして回したら**台帳に「未踏の area」を明記**して silent な打ち切りにしない。

---

## Phase 2 — TEST LOOP（検証: 全ストーリーをテストし台帳に書き戻す）

Phase 1 が終わったら**自動でこのループに切り替える**（user に戻さない）。台帳の各行を上から処理:

1. **既存自動テストがある行**（`test_type ∈ {unit, integration}` かつ覆うテストが存在）:
   対象の test コマンド（例 `pytest <該当>`）を実行し、結果を `baseline_status`(`pass`/`fail`) と `baseline_evidence`(test 名+結果) に記録。
   - 効率化: 行ごとに起動せず、**スイート/モジュール単位で1回走らせて結果を各行へマップ**してよい。
2. **テストが無い行**（`no-coverage`）= カバレッジ穴。RED-first で埋める:
   - 再現可能な入口（API は test client / curl、module は直接呼び出し）で**期待挙動を実観測**し、合否を `baseline_status` に記録。
   - 余力があり user が望むなら、その穴に**回帰テストを1本足す**（RED→GREEN、[[feedback_red_first_before_bugfix]]）。
3. **`fail` を観測した行** → `defect_id`/`defect_summary` を採番。修正まで行うなら `fix` skill / `bug-fix` workflow に委ね、
   RED→GREEN 後に `fix_status=fixed` / `retest_status`/`retest_evidence` を埋める。修正しない方針なら `open`/`wontfix` を残す。
4. 1行処理ごとに台帳 CSV を更新（途中で止まっても進捗が残る）。

---

## 自律契約（autorun と同じ — [[feedback_autonomous_loop_gate_completion_on_user_stated_condition]]）

- **止まらない / 自分で完結 / user に操作を投げ返さない**（役割逆転回避 [[feedback_minimize_user_actions_absolute]]）。
  テスト実行・curl・pytest・台帳書き込みは全部自分でやる。
- **baseline_evidence / retest_evidence は実観測のみ**。テスト結果・HTTP レスポンス・観測値を散文や echo で確定せず、
  実行 tool の出力を見てから書く（[[feedback_confirm_observation_before_asserting]]）。「pass」と書く前にその test を実際に走らせる。
- **完了ゲート**: 「Phase 2 完了」を書けるのは **台帳の全対象行が空でない `baseline_status` を持ち、`fail` 行が
  defect として採番済み（修正したなら `retest_status=pass` を実観測）**のとき。
  proxy・部分観測・「だいたい通った」で done と言わない（[[feedback_completion_means_user_visible_end_state]]）。
  スコープを絞って回したなら「絞った範囲で完了・未踏 area は X」と正直に範囲を出す。
- **停止してよい例外のみ**: (1) 情報不足で次手が決められない (2) permission gate 拒否 (3) 物理/本人認証
  (4) user の苛立ちサイン（[[feedback_never_anger_user_absolute]]）。それ以外は走り続ける。
- **heartbeat**: 長い Phase は「Phase1: N機能を台帳化」「Phase2: M/N 行テスト済み（pass A / fail B / gap C）」と1行ずつ可視化。

---

## 完了報告（user outcome 先頭 — [[feedback_completion_report_lead_with_user_outcome_not_internals]]）

最後に **(a) 台帳の場所**、**(b) 数字**（総機能数 / pass / fail / カバレッジ穴 / 採番した defect）、
**(c) 一番効く次の一手**（どの穴/不具合から潰すか）を3点で出す。関数名やビルド呪文で固めない。

---

## 規模が大きいとき: goal-loop workflow（Phase 2 の fan-out）

全機能が多く Phase 2 を並列化したいときは `.claude/workflows/goal-loop.js` を使う（Workflow ツールの explicit opt-in は
**user の合図が要る** — 勝手に大規模 fan-out しない）。workflow は Discover をカテゴリ別に並列 → ストーリーを merge →
各ストーリーを並列にテスト → 最後に1エージェントが台帳 CSV を書き出す、という形。詳細は同ファイル冒頭の設計コメント参照。
