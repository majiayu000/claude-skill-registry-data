---
name: issue-ref-freshness
description: コード・docs・Issue 本文にある他リポジトリの issue/PR 参照のうち、書かれた当時は Open 前提だったものの現状を照合し、参照先の裁定(close・merge・not planned)を読んで言及元の記述を現状に合わせて書き直す手順。「upstream が対応したら落とす」「drop once ... lands」「upstream 対応待ち」「Remove once ... is fixed」「〜の修正を待っている」型の記述に作業中に触れたとき、自分が upstream に起票した issue が閉じられていたと気づいたとき、「参照の鮮度点検」「外部 issue 参照を点検」を頼まれたときに使う。stale upstream reference, drop once lands, workaround waiting on upstream, upstream issue closed, check referenced issues、といった英語の文脈でも使う。Issue 本文を正本として保つ一般習慣は living-description、裁定に気づくための通知の可視化はこのスキルの対象外。
---

参照先の issue/PR が閉じても、それを「まだ Open」とみなした記述は自動では変わらない。「upstream が対応したら消す」と書いた一時パッチが、upstream に却下された後も「いずれ消える」ものとして残り続ける。このスキルは、そうした記述を参照先の現状に追随させる。

## 1. 対象

次の 2 条件を両方満たす記述が対象。

- 他リポジトリ(自分の別リポジトリを含む)の issue/PR を、URL または `owner/repo#N` 形で参照している
- 参照先が Open であることを前提にしている。例: 「〜が land したら落とす」「upstream 対応待ち」「〜が直るまでの回避策」「Remove once ... ships」

参照先が閉じていても、経緯の引用(「#N で修正済み」「#N の議論を踏まえて」)は対象外。書き直す必要はない。

## 2. 機会発動: 触れたときに照合する

作業中に §1 の記述を読んだら、その場で参照先の現状を確かめる。

```bash
gh issue view <N> --repo <owner/repo> --json state,stateReason,closedAt,title
gh pr view <N> --repo <owner/repo> --json state,mergedAt,closedAt,title   # PR の場合
```

Open のままなら何もしない。Open でなくなっていたら §4 に進む。

## 3. 一括点検: 「参照の鮮度点検して」と頼まれたとき

入口は 2 つある。どちらも、見つけた参照の本文を §4 で読み分ける。

**A. 作業ツリーからの走査。** 作業ツリー内の参照を列挙し、Open でないものだけを出す。

```bash
rg -o --no-filename --hidden -g '!.git' \
  -e 'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(issues|pull)/[0-9]+' \
  -e '\b[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+\b' . \
| sed -E 's#^github\.com/##; s#/(issues|pull)/#\##' | sort -u \
| while IFS= read -r ref; do
    nwo="${ref%#*}" n="${ref##*#}"
    st="$(gh api "repos/$nwo/issues/$n" \
      --jq '[.state, (.state_reason // ""), (.pull_request.merged_at // "")] | @tsv' 2>/dev/null)" \
      || continue   # 解決できない参照(テスト用の例示・typo)は飛ばす
    [[ ${st%%$'\t'*} == open ]] || printf '%s\t%s\n' "$ref" "$st"
  done
```

issues API は PR も返す。3 列目に merge 日時があれば merge 済みの PR。出力された参照ごとに、言及箇所を開いて §1 の条件を満たすか読む。

```bash
rg -n -e '<owner/repo>#<N>\b' -e '<owner/repo>/(issues|pull)/<N>\b'
```

**B. 自分が起票した upstream issue からの逆引き。** 最近閉じられた自分の issue を出し、それを参照している箇所を探す。

```bash
gh search issues --author @me --state closed --sort updated --limit 30 \
  --json repository,number,title,closedAt \
  --jq '.[] | "\(.repository.nameWithOwner)#\(.number)\t\(.closedAt)\t\(.title)"'
```

自分のリポジトリの open Issue 本文も言及元になる。`gh issue list --state open --json number,body` の本文に同じ正規表現をかけて拾う。

## 4. 裁定を読んでから書き直す

状態だけで書き直さない。close の理由で次の手が逆になる。

| 参照先の状態 | 読むもの | 言及元の典型的な書き直し |
|---|---|---|
| closed (completed) / merged | どのリリースに入ったか、修正の範囲 | 回避策を外せるか確かめる。外せるなら外す作業を始めるか Issue にする |
| closed (not planned) | メンテナの最終コメント | 「いずれ消える一時策」を「恒久的なローカル策」に書き換え、却下の日付と参照を残す |
| closed (duplicate) | 重複先の issue | 参照を重複先に張り替え、重複先について §2 をやり直す |

書き直しでは、参照そのものは消さない。「#N は YYYY-MM-DD に not planned で閉じられた」のように、状態と日付を添えて残す。次に読む人が同じ照合を繰り返さずに済む。

書き直した結果、判断や作業が残るとき(一時パッチを恒久化するか、回避策を外すか)は、その判断をこの場で下さない。言及元の記述から Issue を参照させ、判断は Issue に委ねる。

## 5. 書き直しの置き場所

- **Issue 本文**: living-description の流儀で本文を直接編集する。コメントに書いて終わりにしない
- **コード・docs**: 現在の作業と無関係なら、数行の事実更新でも現在の PR には混ぜない。requirements-inventory の隣接負債の判定に従い、stack に積むか wrap-up inbox に送る
- **自分の起票が閉じられた場合**: upstream 側でやることが残っていれば(再提案・別案の提示)、ローカルの Issue として起票する

## 6. 新しく参照を書くときの予防

§3 の走査が拾えるように、Open 前提の参照は次の 3 点を併記して書く。

- 参照先の URL または `owner/repo#N`
- 起票日または参照した日(`filed YYYY-MM-DD`)
- 何が起きたら何をするか(「land したらこのパッチを落とす」)

裸の「upstream の修正待ち」は照合の手がかりがなく、このスキルでは拾えない。
