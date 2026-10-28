---
name: auto-fix-ci
description: push した後に落ちた CI を、人間への確認なしに直して push し直す。無人では `npm run auto-programmer` が AI 専用 clone の中で起動する。対話では、CI の失敗を知らせる hook（wake-on-ci-failure）に起こされたセッションが、その文面の指示で実行する。
argument-hint: '<Issue番号> <run ID>'
---

# /auto-fix-ci

引数: $ARGUMENTS（1つ目が Issue 番号、2つ目が落ちた CI の run ID）

push した PR の CI が落ちたとき、落ちた原因を直して **push を1回するところまで**を人間への確認なしに行う。push した後の CI を待つのも、もう一度直させるかを決めるのも起動側が担う（無人では auto-programmer、対話では `wake-on-ci-failure` hook）。

## 前提

- **最初に、無人か対話かを確かめる。** 以降の「無人」「対話」はこの結果を指す。

  ```bash
  printenv AUTO_PROGRAMMER_UNATTENDED_SESSION
  ```

  `1` が出れば無人（auto-programmer が起動した）。何も出なければ対話。

- **無人は、AI 専用の clone で動く。** 起動側が `/auto-dev` の push したトピックブランチの上でこのスキルを起動する。
- **対話は、人間と共有する作業ツリーで動く。** hook は push の数分〜数十分後に起こすので、人間が次の作業を始めていることがある。Phase 1 で、人間の作業を壊さないか確かめる。
- **ブランチを作らない・切り替えない・ボードの Status を動かさない**（どちらも。ブランチとボードは起動側が扱う）。
- **確認を待たずに最後まで進める。** 進めないと分かったら「離脱手順」に従って終了する。
- **PR は既にある。** 作り直さない・閉じない。Issue も閉じない。
- **push 前の取り込みは Phase 5 の手順で行う。** CLAUDE.md の「`git push` する前に、デフォルトブランチの最新を取り込む」は、このスキルでは Phase 5 で置き換える。PR はデフォルトブランチ（GitHub のリポジトリ設定）宛てなので、取り込む先もデフォルトブランチにする。

## 処理フロー

### Phase 1: 対話では、人間の作業を壊さないか確かめる

無人は飛ばして Phase 2 へ進む。

```bash
gh run view <run ID> --json headBranch --jq .headBranch
git branch --show-current
git status --porcelain
```

次のどちらかなら、直さずに離脱手順へ進む。

- 現在のブランチが、落ちた run のブランチと違う
- `git status --porcelain` に出力がある（未コミットの変更がある）

### Phase 2: 落ちた箇所を読む

```bash
gh issue view <Issue番号> --json title,body,state
gh run view <run ID> --log-failed
```

Issue の state が `OPEN` でなければ直す意味が無いので、離脱手順の痕跡も残さず、理由だけを表示して終了する。本文は「対応方針」と「対象箇所」を読む。直すのは CI を落とした箇所だけで、本文の「対応方針」から外れる直し方（対応方針が採ったライブラリを、型エラーを消すために別のものへ差し替えるなど）はしない。

ログからは、落ちたジョブ名・落ちたステップのコマンド・エラーの出た箇所を読み取る。

### Phase 3: 原因がこの PR にあるか確かめる

デフォルトブランチ名は `gh` で GitHub から引く（`origin/HEAD` は clone した時点の値のまま残り、使い回す clone では古くなるため使わない）。シェル変数は Bash ツールの呼び出しをまたいで残らないので、1回で実行し、出力した名前を以降の `<デフォルトブランチ>` に入れる。

```bash
base=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name) && git fetch origin "$base" && echo "デフォルトブランチ: $base" && git diff --name-only "origin/$base...HEAD"
```

次のどれかなら、この PR の差分では直せないので離脱する。

- エラーの出た箇所が差分に無く、かつ次のいずれかに当てはまる（`git log origin/<デフォルトブランチ> -- <該当ファイル>` でそのエラーが本 PR の作成前から発生している＝デフォルトブランチ側で既に落ちている／依存の脆弱性の公開日が本 PR の作成日より後）
- GitHub や外部サービスの一時障害で落ちている（ランナーの起動失敗・ネットワークエラーなど）

### Phase 4: 直して確かめる

落ちたステップのコマンドを、そのステップの `working-directory`（指定が無ければリポジトリ直下）で手元で実行し、落ちることを確かめてから直す。ステップの定義は `.github/workflows/` の下で探す。ほかのジョブの結果を集めて判定するだけのステップは再現の対象にせず、落ちた上流のジョブのほうを見る。

手元で落ちなければ、原因が差分に無いものとして離脱手順へ進む（離脱の知らせには手元で通ったことを書く）。直したら同じコマンドを通るまで回す（2回直しても同じ箇所で落ちるなら離脱手順へ）。

テストや検査の側を緩めて通すこと（テストの削除・`skip`・ルールの無効化・閾値の引き下げ）はしない。

### Phase 5: コミットする

**先に、最新のデフォルトブランチを取り込む。** ステージする前に行う（ステージ済みの変更があると、git が取り込みを断る）。取り込みから push までを短くし、その間にデフォルトブランチが進んで衝突するのを減らすため、コミットの直前に置く。

```bash
git fetch origin <デフォルトブランチ> && git merge --no-edit origin/<デフォルトブランチ>
```

- 衝突したら、衝突したファイルを解く。生成物は中身を手で直さず、`npm run gen:adr-index` で作り直して `git add` する。解いたファイルを `git add <パス>` し、`git commit --no-edit` で merge を閉じる（`/git-commit` はパスを指定するので、merge の途中では使えない）。解けなければ離脱手順へ進む
- 「Your local changes ... would be overwritten」で止まったら、取り込みが未コミットの変更と重なっている。先に下の手順でコミットし、そのあとで取り込む。自動で完了する merge コミットでは pre-commit hook が走らないので、取り込んだ後に `npm run gen:adr-index` を実行し、差分が出たら `git add` して `/git-commit stage` でコミットする

直したファイルだけを `git add <パス>` でステージし、`/git-commit stage` を実行する。ワーキングツリー全体を対象にしてはならない。

件名末尾の `(#<Issue番号>)`（git-commit Skill が必須としている）には、引数の Issue 番号を使う。

### Phase 6: push する

```bash
git push
```

pre-push hook の整形検査（`npm run format:check`）で拒否されたら（出力に `整形崩れがあるため push を止めました` が出る）、`npm run format` で整形し、変わったファイルを `git add <パス>` して `/git-commit stage` でコミットし、push し直す。`--no-verify` で飛ばさない。

### Phase 7: 報告する

落ちたジョブ・原因・直したファイル・手元で通したコマンドを表示して終了する。

## 離脱手順

次のどれかに当たったら、**以降の Phase へ進まずに**終了する。

- 対話で、Phase 1 の確かめに引っかかった（別のブランチにいる・未コミットの変更がある）
- Phase 3 で、原因がこの PR の差分に無いと分かった
- Phase 4 で、落ちたステップが手元では落ちない
- Phase 4 の確かめが通らず、2回直しても同じ箇所で落ちる
- 直すには、本文の「対象箇所」の外へ手を広げるか、「対応方針」を変える必要がある（Phase 5 の取り込みで衝突を解いた変更は数えない）
- push が拒否される（整形検査以外の理由で）

終了前に、人間が気付ける形にする。

- **無人**：次の2つを必ず行う。

  ```bash
  gh issue comment <Issue番号> --body "<落ちた run の URL・落ちたジョブ・原因の見立て・どこまでやって何で止まったか>"
  gh issue edit <Issue番号> --add-label "needs-human-check"
  ```

  `gh` の認証が切れていてコメントも投稿できないときは、最後のメッセージに理由を出して終了する。

- **対話**：Issue にコメントもラベルも付けない（人間がその場に居るため）。落ちた run の URL・落ちたジョブ・原因の見立て・どこまでやって何で止まったかを、このセッションで報告して終了する。

**押し戻しはしない。** 未コミットの変更・作ったコミットは消さずに残してよい。無人では、次の `npm run auto-programmer` が clone をデフォルトブランチの状態まで戻す。
