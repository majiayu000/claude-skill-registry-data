---
name: auto-resolve-conflict
description: 先にマージされた別の PR と衝突して止まった PR に、デフォルトブランチを取り込んで衝突を解き、push し直すところまでを人間への確認なしに行う。`npm run auto-programmer` が AI 専用 clone の中で起動する。
argument-hint: '<Issue番号>'
disable-model-invocation: true
---

# /auto-resolve-conflict

Issue番号: $ARGUMENTS

この Issue の PR が、先にマージされた別の PR と衝突して止まっている。デフォルトブランチを取り込んで衝突を解き、**push を1回するところまで**を人間への確認なしに行う。push した後の CI を待つのも、落ちたら `/auto-fix-ci` に直させるのも起動側（auto-programmer）が担う。

## 前提

- **作業ツリーは AI 専用の clone で、起動側が PR のブランチへ切り替えてから起動する。** 切り替える先は、起動側が最後に CI を待ったコミットで、その後に他の push が無いことを確かめてある。このスキルはブランチを作らない・切り替えない・ボードの Status を動かさない（CLAUDE.md の着手ルールのコマンドも打たない）。
- **人間はこの実行を見ていない。** 確認を待たずに最後まで進める。進めないと分かったら「離脱手順」で痕跡を残して終了する。
- **PR は既にある。** 作り直さない・閉じない・本文を書き換えない・auto-merge に触れない。Issue も閉じない。
- **取り込むのはデフォルトブランチ（GitHub のリポジトリ設定）で、merge で取り込む。** rebase はしない。push 済みの履歴を書き換えると、force push が要るからである。CLAUDE.md の「`git push` する前に、デフォルトブランチの最新を取り込み、`npm run gen:adr-index` を実行する」は、このスキルの Phase 2 と Phase 5 が担う。
- **デフォルトブランチ側の変更は消さない。** すでにレビューを経てマージされた変更だからである。この PR の変更を、その上に載せ直す。

## 処理フロー

### Phase 1: Issue を読む

```bash
gh issue view $ARGUMENTS --json title,body,state
```

state が `OPEN` でなければ直す意味が無いので、離脱手順の痕跡も残さず、理由だけを表示して終了する。本文は「対応方針」と「対象箇所」を読む。衝突した箇所で、この PR が何をしたかったのかを知るためである。

### Phase 2: デフォルトブランチを取り込む

デフォルトブランチ名は `gh` で GitHub から引く（`origin/HEAD` は clone した時点の値のまま残り、使い回す clone では古くなるため使わない）。シェル変数は Bash ツールの呼び出しをまたいで残らないので、1回で実行し、出力した名前を以降の `<デフォルトブランチ>` に入れる。

```bash
base=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name) && git fetch origin "$base" && echo "デフォルトブランチ: $base" && git merge --no-edit "origin/$base"
```

出力で行き先を決める。

- **衝突した**（`CONFLICT (content): Merge conflict in <パス>` と `Automatic merge failed; fix conflicts and then commit the result.` が出る）：Phase 3 へ進む
- **衝突せずに取り込めた**（`Merge made by the 'ort' strategy.` が出る。GitHub の判定が古かった）：解いたファイルが無いので、Phase 3〜5 を飛ばす。git が自動で作った merge コミットでは pre-commit hook が走らないので、`npm run gen:adr-index` を実行し、差分が出たら `git add docs/adr/adr-index.md` して `/git-commit stage` でコミットしてから、Phase 6 へ進む
- **`Already up to date.` と出た**：取り込むものが無く、push するものも無い。離脱手順へ進む
- **上のどれでもない**（`Fast-forward` など）：離脱手順へ進む

### Phase 3: 衝突を解く

```bash
git diff --name-only --diff-filter=U
```

出たファイルを1つずつ解く。

1. 衝突した箇所の両側を読む。デフォルトブランチ側の変更が何のためかは、`git log --oneline HEAD..origin/<デフォルトブランチ> -- <パス>` で、取り込んだ側にだけあるコミットの件名を引いて読む（merge を閉じる前の HEAD は、この PR の先頭である）。ここに出たコミットが、Phase 4 で照らすデフォルトブランチ側の変更である。件名末尾の `(#番号)` がその変更の Issue なので、足りなければ `gh issue view <番号>` で本文を読む
2. **両方の変更を残す。** デフォルトブランチ側の変更はそのまま活かし、この PR の変更をその上に載せ直す。両方が同じ一覧に項目を足したなら、両方の項目を残す
3. 両立しない（同じ値を別々の値に変えた・一方が消した箇所を他方が書き換えた、など）なら、どちらを採るかをこのスキルは決めない。離脱手順へ進む
4. 生成物は中身を手で直さず、生成するコマンドで作り直す（`docs/adr/adr-index.md` は `npm run gen:adr-index`、`package-lock.json` は `package.json` を解いた後に `npm install --package-lock-only`）

解いたら、衝突の印が残っていないことを確かめる。何か出たら、そのファイルを解き直す。

```bash
git diff --name-only --diff-filter=U | xargs grep -n -E '^(<<<<<<<|=======|>>>>>>>)( |$)'
```

### Phase 4: 確かめる

**デフォルトブランチ側の変更を消していないかを確かめる。** Phase 3 で解いたファイルごとに、取り込んだデフォルトブランチとの差分を読む。

```bash
git diff origin/<デフォルトブランチ> -- <パス>
```

出るのは、この PR が Issue の対応方針に沿って変えた行だけのはずである。次のような行が出たら、Phase 3 でデフォルトブランチ側を落としている。Phase 3 の手順1で読んだデフォルトブランチ側のコミットの変更（`git show <コミット> -- <パス>`）と照らして見分け、解き直す。

- デフォルトブランチ側が一覧に足した行 `- /auto-fix-ci` が、差分に `-` を付けて出る（足された行を消している）
- デフォルトブランチ側が `60` に変えた値が、`-60` と `+30` の組で出る（書き戻している）

次に、Phase 3 で解いたファイルのパスに応じて検査を実行する。1つのファイルが複数の行に当たれば、当たる行をすべて実行する。

| 解いたファイルのパス                                                  | 実行するもの          |
| --------------------------------------------------------------------- | --------------------- |
| `*.md`（`.claude/` のプロンプト定義を含む）                           | `npm run check:links` |
| `infra/**`                                                            | `/cdk-ci`             |
| `.claude/hooks/**`                                                    | `npm run test:hooks`  |
| 上のどれにも当たらない（`app/**`・`scripts/**`・`package.json` など） | `/code-ci`            |

検査が落ちたら、解いたファイルの「中」か「外」かで扱いを分ける。エラーが指す行が Phase 3 で解いたファイルにあるとき、または落ちたテストが Phase 3 で解いたファイルを検査するもの（`foo.mjs` を解いて `foo.test.mjs` が落ちた、など）のときを「中」とし、それ以外を「外」とする。

- **中**：直して、同じ検査を通し直す。2回直しても通らないなら、離脱手順へ進む
- **外**（デフォルトブランチ側の変更とこの PR の変更が、文字の衝突なしに噛み合わないなど）：ここでは直さず、Phase 5 へ進む。push の後に CI が落ち、起動側が `/auto-fix-ci` に直させる

テストや検査の側を緩めて通すこと（テストの削除・`skip`・ルールの無効化・閾値の引き下げ）はしない。

### Phase 5: コミットする

Phase 3・4 で変えたファイルだけを `git add <パス>` でステージし、merge を閉じる。**`/git-commit` は使わない。** `/git-commit` はパスを指定してコミットするが、git は merge の途中でパスを指定したコミットを断る（`fatal: cannot do a partial commit during a merge.`）。AI 専用 clone には他のセッションの変更が無いので、index ごとコミットしてよい。

```bash
git commit --no-edit
```

件名は git が付ける `Merge remote-tracking branch 'origin/<デフォルトブランチ>' into <ブランチ>` のままにする。このコミットでは pre-commit hook が走り、`docs/adr/adr-index.md` を作り直してステージする。

### Phase 6: push する

```bash
git push
```

pre-push hook の整形検査（`npm run format:check`）で拒否されたら（出力に `整形崩れがあるため push を止めました` が出る）、`npm run format` で整形し、変わったファイルを `git add <パス>` して `/git-commit stage` でコミットし、push し直す（merge は閉じているので、`/git-commit` が使える）。件名末尾の `(#<Issue番号>)` には引数の Issue 番号を使う。`--no-verify` で飛ばさない。

### Phase 7: 報告する

衝突したファイル・どう解いたか・実行した検査を表示して終了する。

## 離脱手順

次のどれかに当たったら、**以降の Phase へ進まずに**終了する。

- Phase 2 で、取り込むものが無かったか、想定していない出力が出た
- Phase 3 で、両側の変更が両立しない
- Phase 4 で、解いたファイルの「中」で落ちた検査が、決めた回数まで直しても通らない
- push が拒否される（整形検査以外の理由で）

人間が気付ける形にするため、終了前に次の2つを必ず行う。

```bash
gh issue comment $ARGUMENTS --body "<PR の URL・衝突したファイル・どこまでやって何で止まったか>"
gh issue edit $ARGUMENTS --add-label "needs-human-check"
```

`gh` の認証が切れていてコメントも投稿できないときは、最後のメッセージに理由を出して終了する。

**押し戻しはしない。** 途中の merge・未コミットの変更・作ったコミットは、どれも消さずに残してよい。次の `npm run auto-programmer` が clone を切り替える前に、未コミットの変更を stash へ退避する。`needs-human-check` が付いた Issue の PR は、人間が外すまで起動側が解かせ直さない。
