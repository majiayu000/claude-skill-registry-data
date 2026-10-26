---
name: limit-resume
description: 利用上限（5 時間の区切り・週の上限・モデル別の上限）で止まったセッションを、解除後に同じ窓で自動再開させる仕組みの状態を見る・止める・説明する。「上限で止まったら再開して」「自動再開の予約を見せて」「自動再開を止めて」「limit-resume どうなってる」と言われたときに使う。引数 = status | cancel [session_id の先頭] | 説明
---

# limit-resume — 上限で止まったセッションを、解除後に同じ窓で再開する

フック（`StopFailure`・`rate_limit`）は入れた時点で常に効いている。この skill は状態を見る・取り消す・説明するための入口。

## 何が起きるか

1. ターンが利用上限で終わると、そのセッションでだけ `StopFailure` が発火する。user のプロンプトへの返事が上限だった場合も、動いていたエージェントが途中で止められた場合も同じ。開いているだけで止まっている別の窓には発火しないので、そちらは起こさない。
2. 上限の文言（`You've hit your … · resets 4:30pm (Asia/Tokyo)`）から解除時刻を読む。**解除が 12 時間より先なら捨てる**（週の上限の大半はここで捨てられる）。
3. 切り離した待ち役が解除時刻 + 90 秒まで待つ。そのあと、次の 3 つを全部満たすときだけ、そのセッションの郵便受け（`~/.claude/sessions/<pid>.json` の `messagingSocketPath`）へ「続けて」を送る。
   - 同じセッションがまだ開いている
   - 待機中である
   - 会話記録の最後がまだ上限のエラーである（user が自分で再開していない）

   送り手は画面なしの `claude -p --model haiku` で、SendMessage を 1 回呼ぶだけ。届いた伝言で、同じ窓の会話に新しいターンが始まる。
4. 窓が閉じていたら捨てる（別の窓や画面なしで再開はしない）。再開してすぐまた上限、が 6 時間に 3 回続いたら、それ以上は再開しない。

## 操作

- 状態: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/limit_resume.py" status`
- 取り消し: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/limit_resume.py" cancel [session_id の先頭]`（省略すると全部取り消す）
- 記録: `~/.claude/limit-resume/log.jsonl`（`LIMIT_RESUME_HOME` で変えられる）。event は `scheduled` / `resumed` / `drop_far_reset` / `drop_window_closed` / `drop_user_resumed` / `drop_loop_guard` / `send_failed` / `skip_*`。

## 較正（環境ごとに変えてよい値）

| 環境変数 | 既定 | 意味 |
|---|---|---|
| `LIMIT_RESUME_MAX_WAIT_HOURS` | 12 | これより先の解除は捨てる |
| `LIMIT_RESUME_SENDER_MODEL` | haiku | 伝言を送る役のモデル |
| `LIMIT_RESUME_MARGIN_S` | 90 | 解除時刻から送るまでの余裕（秒） |

文言の書式・名簿の形式は Claude Code の内部仕様（2.1.281 で確認）。版が変わって読めなくなったら `skip_unparsed` が記録に出るので、`parse_limit_message` と `find_registry` を見直す。

## 限界

- 待ち役は普通のプロセスなので、Mac を再起動すると予約は消える（スリープは平気。壁時計で測り直す）。
- 送り手の `claude -p` も同じアカウントの利用量を少し使う。解除後に送るので、上限に当たったままにはならない。
