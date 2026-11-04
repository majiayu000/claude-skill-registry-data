---
description: 他の人の PR を approve する前の確認を行い、approve のコマンドを示す。approve そのものは人が打つ。人だけが /approve-pr で起動する。
argument-hint: "[PR 番号 または URL（省略時は現在のブランチの PR）]"
disable-model-invocation: true
allowed-tools: Bash(gh pr view:*) Bash(gh pr checks:*) Bash(gh api:*) Bash(gh repo view:*)
---

他の人の PR を approve してよい状態かを確かめ、**approve のコマンドを示すところまで**行います。

**approve は人が打ちます。** フック（ `block-known-footguns.sh` の5番目の検査）が、Claude からの `gh pr review --approve` を常に止めています。本スキルはその守りを外さず、判断材料をそろえて渡すだけです。

`disable-model-invocation: true` なので、本スキルは人が `/approve-pr` を打ったときだけ起動します。

## 進め方

### 1. 対象を特定する

- 引数の PR 番号 / URL から引く。**引数が無ければ止めて、PR を尋ねる**（現在のブランチの PR は、たいてい自分の PR なので approve の対象にならない）
- `OWNER/REPO` は URL から、無ければ `gh repo view --json nameWithOwner -q .nameWithOwner` で取る

```bash
gh pr view <PR> -R OWNER/REPO --json author,state,isDraft,headRefOid,url
gh api user -q .login
```

### 2. 4項目を確かめる

**止めるかどうかは人が決めます。** 本スキルは結果を並べるだけで、項目に引っかかってもコマンドは示します。ただし、作成者が自分のときは示しません（GitHub が拒むため）。

| 項目 | 確かめ方 | 引っかかったとき |
| --- | --- | --- |
| 作成者が自分でない | `author.login` と自分の login を比べる | **コマンドを示さずに終える**。自分の PR は approve できない |
| HEAD が動いていない | 自分の最後のレビューの `commit_id` と `headRefOid` を比べる（下記） | 動いた分のコミットを `path` 付きで並べる |
| CI の状態 | `gh pr checks <PR> -R OWNER/REPO` | `fail` / `pending` の行を並べる |
| 自分の指摘の残り | 自分が付けた `[must]` のスレッドのうち、未解決のもの（下記） | スレッドの URL を並べる |

自分の最後のレビューの `commit_id` を引く。

```bash
gh api "repos/OWNER/REPO/pulls/<PR>/reviews" \
  --jq '[.[] | select(.user.login=="<自分>")] | last | .commit_id'
```

レビューが1件も無ければ、「この PR はまだレビューしていない」と並べる。HEAD との比較はできない。

動いていたら差分のコミットを出す。

```bash
gh api "repos/OWNER/REPO/compare/<commit_id>...<headRefOid>" --jq '.commits[] | "\(.sha[0:9]) \(.commit.message | split("\n")[0])"'
```

自分の `[must]` で未解決のスレッドを引く。

```bash
gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){pullRequest(number:<PR>){reviewThreads(first:100){nodes{isResolved comments(first:1){nodes{author{login} body url}}}}}}}' \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved | not) | .comments.nodes[0] | select(.author.login=="<自分>" and (.body | test("(^|\n)\\[must\\]"))) | .url'
```

jq の `test` には複数行のフラグが無く、`^` は本文の先頭にしか当たらない。本文の1行目はメンションなので、改行を明示して2行目の prefix を拾う。

**総括コメントに置いた `[must]` はスレッドにならないので、この検索に出ない。** 自分のレビュー本文に `[must]` があれば、その本文の URL も並べ、直ったかは人が見ると添える。

### 3. 結果とコマンドを示す

4項目を1つの表で返し、最後にコマンドを1行で置く。**コマンドは `!` を付けた形で示す**（そのまま打てば、このセッションで実行される）。

```
| 項目 | 結果 |
| --- | --- |
| 作成者 | 自分ではない（<login>） |
| HEAD | 前回レビュー（<sha>）から動いていない |
| CI | 7本すべて pass |
| 自分の must | 未解決なし |

approve するなら:
! gh pr review <PR> -R OWNER/REPO --approve
```

## やってはいけないこと

- **approve を自分で打つこと**。フックが止めるが、止められる前提で打たない。人が打つまで待つ
- 引っかかった項目を理由に、コマンドを示さずに終えること。止めるかは人が決める（作成者が自分のときを除く）
- `gh api` で `"event":"APPROVE"` のレビューを投稿すること。フックの外の経路で、同じく人の判断を飛ばす
- 引数が無いときに、現在のブランチの PR を対象にすること

## 関連

- `/review-pr` （レビューの投稿）: 指摘を書いて投稿するのはあちら。approve の見立てもあちらが会話で渡す。本スキルは人が approve すると決めた後の確認だけを持つ
- `no_operating_on_others_prs.md` （他人の PR は触らない）: approve はレビューする側の行為で、作成者の領分には入らない。本スキルもコメント・本文には触れない
