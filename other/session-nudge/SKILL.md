---
name: session-nudge
description: 別の稼働中セッションについて相談したいときに使う。対象セッションを選んで相談したいことを伝えると、その履歴を読んで外から客観視し、簡単に答える。相談の結果、対象セッションへ送ることになったら人間の裁可を経て SendMessage で送る。tmux M-m のポップアップ端末から呼び出す想定。
disable-model-invocation: true
---

# session-nudge

対象セッション（以下 A）を、この場（以下 B）から外部の読み手として客観視するための**相談の場**。
判定機ではない。ズレの有無を裁定するのではなく、user が持っている違和感に付き合う。

`M-m` 経由なら fzf での対象選択だけが済んでおり、`/session-nudge target=<name>` の形で渡ってくる。
相談内容の入力はポップアップでは行わない（素のシェルの `read` では日本語が打てない）。

## 手順

### 1. 対象を選ぶ（`target` が無い場合のみ）

`ListAgents` で peer 一覧を出し、選ばせる。自分自身は除外する。
`sessionId` が要るときは
`claude agents --json | jq -r '.[] | select(.kind=="interactive") | [.name,.status,.cwd,.sessionId] | @tsv'`。

### 2. 何について相談したいかを聞く

`target` が渡っていても**必ず聞く**。「A の何について相談したいですか」と一言尋ねて待つ。
履歴を読むのはその後。ここが手順3以降のレンズになる。

### 3. 相談内容をレンズに履歴を読む

`sessionId` がそのままファイル名になる。

```sh
jq -r 'select(type=="object" and (.type=="user" or .type=="assistant"))
       | (.type[0:1]) + "| " + ((.message.content // "") | if type=="string" then . else
           ([.[] | if .type=="text" then .text
                   elif .type=="tool_use" then "<TOOL "+.name+" "+((.input|tostring)[0:200])+">"
                   elif .type=="tool_result" then "<RESULT "+(((.content//"")|tostring)[0:250])+">"
                   else "" end] | join(" ")) end)' \
  ~/.claude/projects/*/<sessionId>.jsonl | grep -v '^.| *$'
```

長ければ `head` / `tail` で冒頭と直近を押さえる。**user の生の発言を優先して読む**
（A が何を頼まれたかは、A の要約ではなく user の原文にしかない）。
`tool_result` も `user` 型で入るので、絞るときは `text` ブロックの有無で判定する。

`ctx` は使わない。`ctx_events.occurred_at_ms` はインポート時刻で埋まり、
全セッションが同一値になるため「直近」の並べ替えに使えない。

B も同じモデル・同じ規則で動くので、放っておけば A と同じ穴に落ちる。担保は1つ:
**A の結論を根拠に使わない。A が見た一次情報（user の原文・ファイル・コマンド出力）に自分で当たる。**

### 4. 軽く客観視して返す

ここが本体。返すのは次の2つだけ。

- A の現在地を外から見て数行
- 相談内容への簡単な答え

**「ズレている / いない」の判定を結論として出さない。判定表・長文の分析を最初から出さない。**
深掘りは user が聞いてから。ここで止めて user と話す。

### 5. A に送ることになったら

相談の結果として方針が決まったときだけ。文案は短く、指示ではなく気づきとして書く
（「〜のようだが確認してほしい」であって「〜しろ」ではない）。
B の結論そのものより、**A が自分で確かめられる問い**の形にする方が精度が高い。

文案を user に提示し、送るか・直すかを確認する。ここを飛ばさない。OK が出たら送る。

```
SendMessage(to: "<A の name>", message: "<確定した文面>", summary: "<5-10語の要約>")
```

受信側には「user ではなく別セッションからの入力」だと構造的に伝わるので、本文に断り書きは要らない。
`crossSessionInbound` が `hold` なら相手側でも承認が要る（二重ゲート・害はない）。

送ったら B の仕事は終わり。A の答えは A の画面で user に返るものなので、返信を待たない
（返信が来ること自体はあるが、来る前提で話を止めない）。
