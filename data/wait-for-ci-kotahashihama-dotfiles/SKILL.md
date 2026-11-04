---
description: 【他スキルから呼ばれる部品】GitHub Actions のワークフロー完了をバックグラウンドで待つ。「起動したか」と「終わったか」を両方の条件で判定し、古い run を掴んで即座に抜ける事故を防ぐ。PR に push した後や slash command でワークフローを起動した後、完了を待ちたいときに使う。
argument-hint: "[ワークフロー名 または PR 番号] [--event イベント名]"
user-invocable: false
allowed-tools: Bash(gh run list:*) Bash(gh run view:*) Bash(gh pr checks:*) Bash(gh pr view:*) Bash(git branch:*) Bash(sleep:*) Bash(while:*) Bash(until:*)
---

GitHub Actions の完了を待ちます。**待てているつもりで待てていない**のがこのタスクの唯一かつ最大の失敗モードで、それを潰すのがこのスキルの目的です。

## 待機の述語 (ここを間違えると全部壊れる)

### 起動前に「直前の run ID」を控える

**「最新 run が completed か」だけを見てはいけない。** 過去の run が既に完了していると、その場で条件を満たして即座に抜けます。**新しく発火した run かどうか**を ID で判別します。

```bash
prev=$(gh run list --workflow "<name>" --event <event> --limit 1 --json databaseId -q '.[0].databaseId')
```

run が1件も無ければ空文字でよい。**ワークフローを起動する前に取る**のが要点です。

### `--branch` で絞らない (イベントによって headBranch が変わる)

| 起動のしかた | `headBranch` |
| --- | --- |
| push / PR の作成・更新 | feature ブランチ |
| **PR コメントの slash command (`issue_comment`)** | **base ブランチ (`main`)** |
| `workflow_dispatch` | 指定したブランチ |

`issue_comment` 起点を feature ブランチで絞ると**永久に引っかかりません**。`--event` で絞るのが確実です。

### `issue_comment` 起点は、対象 PR の run だけを待つ

**`issue_comment` は、リポジトリのどの PR へのコメントでも起動します。** slash command 以外のコメントで起動した run は、すぐ `skipped` で終わります。「直前の run ID と違う、最新の完了した run」を探すと、ほかの PR のコメントで走った `skipped` の run を掴み、待てたつもりで抜けます。

実際に、slash command を投稿した直後にほかの PR へコメントが付き、その `skipped` の run を自分の PR の結果として読みました。自分の PR の run はまだ実行中でした。この節を足した後も、下の「2. バックグラウンドで待つ」のループのコードが最新の run を見たままだったので、そのコードを使い回して同じ取り違えをもう一度しています。

`gh run list` の JSON には PR 番号が出ないので、`displayTitle` （ `issue_comment` の run では PR のタイトル）で絞ります。

```bash
title=$(gh pr view <PR> --json title -q .title)
gh run list --workflow "<name>" --event issue_comment --limit 20 \
  --json databaseId,status,conclusion,displayTitle |
  jq --arg t "$title" --argjson p "${prev:-0}" '[.[] | select(.displayTitle == $t and .databaseId > $p)][0]'
```

`gh` の `-q` は `--arg` を受け取らないので、`jq` に渡します。起動前の run ID（ `$prev` ）より大きいものに絞るので、同じ PR の前の周の run も外れます。

**見つけたら、その run ID で待つ。** 以降は `gh run view <id> --json status,conclusion` で、その run だけを見ます。

### 時刻でのカットオフは使わない

「起動時刻より後の run」を条件にすると、時計のずれや `createdAt` の粒度で対象を取り逃がし、**永久に待ちます**。ID の比較で判定します。

## 進め方

### 1. 対象の特定

- ワークフロー名は `.github/workflows/` の `name:` と一致させる（リポジトリごとに揺れる）
- イベントは起動のしかたから決める。slash command なら `issue_comment`、push なら `push` / `pull_request`
- 起動前に**直前の run ID** を控える（上記）

### 2. バックグラウンドで待つ

**Bash ツールを `run_in_background: true` で1回だけ起動する。** ポーリング用に Bash を何度も打つのは、通知機構を使わずに手で待つのと同じで無駄です。

```bash
prev=<起動前の run ID>
title=$(gh pr view <PR> --json title -q .title)   # issue_comment 起点のとき。push などで PR に絞らないなら title=""
while true; do
  row=$(gh run list --workflow "<name>" --event <event> --limit 20 \
    --json databaseId,status,conclusion,displayTitle |
    jq -r --arg t "$title" --argjson p "${prev:-0}" \
      '[.[] | select(.databaseId > $p) | select($t == "" or .displayTitle == $t)][0] // empty
       | "\(.databaseId) \(.status) \(.conclusion // "-")"')
  st=$(echo "$row" | cut -d' ' -f2)
  if [ -n "$row" ] && [ "$st" = "completed" ]; then echo "$row"; break; fi
  sleep 20
done
```

**`issue_comment` 起点では `title` を空にしない。** 空にすると、上の「対象 PR の run だけを待つ」の絞り込みが外れ、ほかの PR の run を掴みます。

**待っている間、メインループは他の作業に手を出さない。** 完了通知で再開します。

### 3. 結果の解釈

`conclusion` をそのまま報告せず、**意味まで見る**。

| conclusion | 見るべきこと |
| --- | --- |
| `success` | そのまま次へ |
| `failure` | **原因がコードかどうか**。`gh run view <id> --log-failed` の末尾を読む。レビュー承認待ち (`approval required`) 等、コードと無関係な失敗がある |
| `cancelled` | 後続の run に置き換わった可能性。再度 run list を見る |
| `skipped` | **条件で除外された**。draft PR では走らない設定のことがある。待つ対象を間違えていないか疑う |

### 4. 報告

run ID / conclusion / URL を1行で返す。`failure` なら**原因の分類**（コード起因 / 承認待ち / インフラ）まで添える。

## 出力の目安

- 成功時: 1〜2行（run ID と conclusion、次に何ができるか）
- 失敗時: conclusion + 原因の分類 + ログの該当行。**ログ全文は貼らない**

## してはいけないこと

- **`--branch <feature>` で絞ること**（ `issue_comment` 起点を取りこぼす）
- **「最新 run が completed か」だけで判定すること**（古い run で即座に抜ける）
- 時刻をカットオフに使うこと（取り逃がして永久に待つ）
- フォアグラウンドで待つこと（メインループが長時間ブロックされる）
- 完了通知を待たずに自前ポーリングを繰り返すこと
- `failure` を原因を見ずに「壊れている」と報告すること
- タイムアウトを設けずに待ち続けること。**30分を超えたら中断**して状況を報告する
