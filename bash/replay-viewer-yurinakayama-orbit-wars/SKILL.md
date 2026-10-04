---
name: replay-viewer
description: Orbit Wars の対戦ログをブラウザで再生するスキル。ローカルの self-play ログ (data/lake/selfplay) と Kaggle スクレイピング済みエピソード (data/lake/kaggle_episodes) を対象に、a concise user question でソース・フィルタ条件・対戦を選択させ、kaggle_environments の HTML プレーヤーで再生する。`/replay-viewer` で明示起動されたとき、または「リプレイを見たい」「対戦ログを再生」「self-play の試合を可視化」「Kaggle のエピソードを見たい」「match_id ◯◯ を再生」など、収録済みマッチを目で見たいというニュアンスのリクエストで起動する。1試合ずつのインタラクティブな確認用途。
---

# replay-viewer

このスキルは、収録済みの Orbit Wars 対戦を 1 試合選んでブラウザで再生する。
明示起動 (`/replay-viewer`) または「リプレイを見せて」系のリクエストで起動する。

## 前提

- インデックスとリプレイは DVC 管理。最初に `data/lake/selfplay/matches/` または `data/lake/kaggle_episodes/matches/` が空なら、ユーザーに `uv run --directory backend dvc pull` を案内する
- 再生は `kaggle_environments.Environment.render(mode="html")` をそのまま使う。新しい可視化は書かない
- スクリプトは `backend/` 配下で動く必要があるため、必ず `uv run --directory backend python <script>` の形で呼ぶ

## 動作シーケンス

ユーザーから「リプレイ見たい」と言われたら、以下を上から実行する。
途中の判断はユーザーに聞かず、a concise user question で出した選択肢の答えだけを根拠に進める。

### Step 1 — ソース選択

最初の a concise user question で「どのデータソースを見るか」を 1 問聞く。

| label | 中身 |
|-------|------|
| `selfplay` | `data/lake/selfplay` 配下の self-play ログ |
| `kaggle` | `data/lake/kaggle_episodes` 配下の Kaggle スクレイピング済みエピソード |
| `both` | 両方を時刻順にマージ |

### Step 2 — フィルタ条件

2 問目の a concise user question で、絞り込み条件を multi-select で聞く。
すべて省略可。指定された項目だけスクリプト引数に渡す。

- `mode` — 例: `1v1` / `ffa`。Other で自由入力
- `agent` — agent 名の部分一致（例: `baseline_v4`、`case4`）
- `winner` — 勝者の player index (0..3)
- `limit` — 表示件数 (デフォルト 20)

ユーザーが「特に絞らない」を選んだ場合は limit=20 だけで進む。

### Step 3 — 一覧取得と match_id 選択

`scripts/list_matches.py` を呼んで、フィルタ済みの上位 N 件を JSON で取得する。

```bash
uv run --directory backend python ../.agents/skills/replay-viewer/scripts/list_matches.py \
    --source <source> [--mode <mode>] [--agent <substr>] [--winner <idx>] --has-replay --limit <N>
```

**`--has-replay` の使い分け**:
- 一般的な「最新リプレイ見たい」系: `--has-replay` を付ける（デフォルト）。replay payload が無いマッチを
  選ばせて Step 4 で詰むのを防ぐ
- ただし *特定の agent / 勝者条件* を満たすリプレイをユーザーが要求していて、`--has-replay` を付けると
  0 件になる場合（古い self-play で payload が DVC に上がっていないケース）は、`--has-replay` を **外す**。
  index に matchup と seed さえ残っていれば Step 5 のフォールバックで再生可能

候補が 0 件のときは `--has-replay` を外して再試行 → それでも 0 件なら DVC pull かフィルタ緩和を案内

返ってきた JSON を読みやすい表（番号 / started_at / mode / agents / winner / turns）で表示し、
3 問目の a concise user question で再生したい match を 1 つ選ばせる。

候補が 4 件以下なら a concise user question の選択肢にそのまま入れる。
5 件以上なら、上位 3 件 + 「番号で指定」のように分岐し、Other 経由で番号または match_id 直接入力を受ける。

候補が 0 件なら、フィルタを緩めるか DVC pull が必要かを案内して終了する。

### Step 4 — 再生

選ばれた `match_id` と `source` を `scripts/render_replay.py` に渡す。

```bash
uv run --directory backend python ../.agents/skills/replay-viewer/scripts/render_replay.py \
    --match-id <match_id> --source <source>
```

スクリプトは `/tmp/replay-viewer/<match_id>.html` を書き出して既定ブラウザで開く。
最終行に出力されたパスをユーザーに伝える（ブラウザが自動で開かない環境向け）。

HTML 上部には agent 識別バナーが固定表示される: `P1 / P2` の seat ラベルと agent 名・version・score、
勝者には 👑、各 player の色は plate の色 (P1=magenta / P2=teal / P3=orange / P4=blue) と一致する。
これは公式 Kaggle プレーヤーが seat を `Player 1 / Player 2` としか出さないので、
どっちがどの agent かを一目で分かるようにするためのもの。
rerun_match.py 経由で再生した場合は `source=selfplay (rerun)` 表記 + recorded vs observed winner の note も出る。

### Step 5 — replay 欠損時のフォールバック (selfplay のみ)

ユーザーが `--has-replay` 不要の探し方をした、もしくは特定 match_id を直接指定したケースで、
`render_replay.py` が exit code 4 を返したら **スキップせず** 次のフォールバックに進む。
self-play は index に `seed` と `agent_*_name` が記録されているので、同一 seed で再走させれば
HTML を復元できる（`backend/src/dataset/selfplay/agents.py` の `resolve()` で agent コードを読む）。

```bash
uv run --directory backend python ../.agents/skills/replay-viewer/scripts/rerun_match.py \
    --match-id <match_id> --source selfplay
```

ユーザーの依頼に「特定 agent が勝った」など勝者条件が含まれていて、かつ最初の再走で
recorded_winner と observed_winner が食い違った場合は `--require-winner-name <agent>` を付ける。
スクリプトは同じ matchup の他 row を `started_at` 降順で当たり、勝者条件を満たす seed が出るまで
最大 `--max-attempts` 回（デフォルト 20）試行する。

```bash
uv run --directory backend python ../.agents/skills/replay-viewer/scripts/rerun_match.py \
    --match-id <match_id> --source selfplay --require-winner-name baseline_v4
```

注意点:
- 再走は agent コードが当時と同一であることを前提にする。コード差分が大きいと winner が変わるが、
  上記のリトライロジックで「現在のコードでも勝つ seed」を見つけて返す
- Kaggle episode (`source=kaggle`) は外部実行なのでローカルで再現不能。`render_replay.py` が
  exit 4 になったら DVC pull かマッチ変更を案内する

### Step 6 — 次の試合を提示

1 試合の再生 HTML を出した後、**そのまま終わらず** a concise user question で「次に何を見るか」を提示する。
ユーザーは大抵「もう 1 試合別の seed」「別の agent」「終了」のどれかを選ぶので、それを 4 択以下で渡す。

提示する選択肢は **その試合のコンテキストから具体的に作る** こと。汎用的な「もう 1 件見る / 終わる」だけだと
情報量がなく、ユーザーが選びづらい。Step 3 で取得した list_matches の残り候補や、
今見た試合から自然に派生する angle をベースに 2〜4 択を組み立てる。

例 (今見た試合: il_v1 vs baseline_v1, winner=baseline_v1):

| label | 中身 |
|-------|------|
| 同じ matchup の別 seed (例: seed298) | list_matches の 2 番目を再生 |
| 別 agent の試合 (baseline_v4 vs baseline_v5 など) | Step 3 から再開、agent フィルタを変えて再選択 |
| 同じ agent の勝ちパターンを見たい (例: il_v1 が勝った試合) | フィルタに winner=0 を追加して Step 3 から再開 |
| 終了 | ここで停止 |

選択肢を作るときに見るべきもの:
- Step 3 で取得した list の残り候補（既に hit してるので最も安価）
- ユーザーが当初指定したフィルタの隣接条件（例: `winner=1` で見たなら `winner=0`、
  agent X で見たなら同じ matchup の別 agent、最新を見たなら 1 つ前）
- 今見た試合の興味深い特徴（極端に長い/短い、score 差が大きい、など）

ユーザーが「終了」を選んだ場合のみ停止する。それ以外は Step 3〜5 の該当ステップにジャンプして
ループを継続する。`/tmp/replay-viewer/` 配下の HTML は使い回しても良い（同じ match_id なら再生成不要）。

## list_matches.py の出力スキーマ

```json
[
  {
    "match_id": "selfplay_run_42_match_3",
    "source": "selfplay",
    "mode": "1v1",
    "started_at": "2026-04-19T03:11:08Z",
    "turns": 287,
    "winner": 0,
    "draw": false,
    "elapsed_sec": 11.4,
    "episode_id": -1,
    "agents": [
      {"idx": 0, "name": "baseline_v4", "version": "case4", "score": 32},
      {"idx": 1, "name": "baseline_v1", "version": "case1", "score": 8}
    ]
  }
]
```

`source = kaggle` の場合は `episode_id >= 0` で `match_id = kaggle_ep_<episode_id>` となる。

## エラーハンドリング

- list_matches.py が `[]` を返す:
  - まず `--has-replay` を外して再試行（古い self-play で payload が DVC に無いケース）。再試行で hit したら Step 5 (rerun_match.py) に直接進む
  - それでも `[]` ならフィルタ緩和か `uv run --directory backend dvc pull` を案内
- render_replay.py が exit 2 → data root 自体が無い。DVC pull を案内
- render_replay.py が exit 4 → match_id は index にあるが replay payload が無い。selfplay なら Step 5 の rerun_match.py へフォールバック、kaggle なら DVC pull か別マッチ
- rerun_match.py が exit 5 → `--require-winner-name` のリトライが上限到達。`--max-attempts` を増やすか agent コードが変わりすぎてる旨をユーザーに伝える
- ブラウザが開かない環境 → 出力された `/tmp/replay-viewer/<match_id>.html` のパスをそのまま伝える（macOS 以外、SSH 越し等）

## やらないこと

- 複数試合の同時再生・グリッド表示
- リプレイ HTML の見た目カスタマイズ（公式プレーヤーをそのまま使う）
- 新規ログの収集（self-play 実行 / Kaggle scrape は別スキル/CLI の責務）

将来必要になったらこのスキルを拡張する。今は「1 試合選んで開く」に集中する。
