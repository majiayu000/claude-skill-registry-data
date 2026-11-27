---
name: pr-description
description: PRの本文(Description)を標準スケルトンで書き、見た目に影響する変更にはBefore/After証跡(画像またはコード対比)を必ず添える習慣。PR作成・PR本文・Description作成・pull request description・PRを作って・スクリーンショット添付・Before/After・gh pr create・gh pr edit・--attach・視覚証跡、といった文脈で使う。attach before/after images to a PR, PR body skeleton, No-Visual escape hatch、といった英語の文脈でも使う。
---

PRの本文は、リポジトリごとにまちまちな自由記述ではなく、次の標準スケルトンで書く。リポジトリ固有の `PULL_REQUEST_TEMPLATE.md` がある場合は、その見出し構造に従いつつ、下記の内容要素を漏れなく埋める(見出しは譲るが、内容要素は譲らない)。

## 0. 投稿の正準形(bleep の文法)

`gh` で本文を投稿するときは、次の形だけが通る(`tarotene/bleep` の ADR-0003。
文法の外は PreToolUse で deny され、理由文が書き直し方を案内する):

1. 本文を **Write ツールでファイルにする**(絶対パス)。heredoc やコマンド
   置換で本文を組み立てない。置き場は、非公開リポジトリの作業中でも
   公開リポジトリ宛てなら**プロジェクト名を含まないパス**
   (`${XDG_RUNTIME_DIR:-/tmp}/gh-body-<YYYYMMDD>-<用途>-<乱数 4 桁>.md`)にする。セッションの
   scratchpad はプロジェクトのパスを平らにした名前を含むため、bleep の
   denylist が本文でなくパスに一致して拒否する(#712。bleep 側の修正が
   入るまでの暫定)。この置き場は別のセッションと共有で、前のセッションの同名ファイルが
   残っていることがある(`d4` のような短い id は衝突した。Write が「ファイルがまだ読まれて
   いない」で失敗する。#996)。名前には日付・用途・乱数を入れて衝突しにくくする。同名の
   ファイルが既にあるときは、別名にする(上書きしたいときは、先に Read してから Write する)。
2. 宛先を **リテラルの `-R OWNER/REPO`** で書く(`pr|issue` は PR/Issue の URL でも
   よい)。cwd の origin からの推測や変数は使えない。
3. 本文は **`--body-file <絶対パス>`**(release は `--notes-file`)で渡す。
   `--body`・`-b`・`close|reopen` の `--comment`・stdin(`-`)・相対パス・`~`・
   変数・コマンド置換は文法の外。

```
gh pr create -R OWNER/REPO --base main --title "..." --body-file /abs/path/pr-body.md
```

`--title` は `type(scope)?!?: subject` の形で、type は
`feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert` のいずれか
(ADR-0031)。契約の workflow(`.github/workflows/pr-title.yml`)を持つリポジトリ
では、`pr-title-guard` がこれを作成時に検査する。stacked PR の最下段で
外れると全段がやり直しになるので、`gh pr create` の前に確かめる。

本文ファイルは `git commit` と同様、`gh` を呼ぶ前に別の呼び出しで作っておく
(複合コマンドの 1 本目が deny されると前段の生成も消える。#668)。

本文ファイルの Write と、それを読む `gh` の投稿は**同じ応答で並列に出さない**。
Write が失敗(「読み込み後にファイルが変更された」など)しても、並列の
`gh pr edit --body-file` はそのまま走り、ディスクに残っていた古い本文で
上書きする。投稿は通知を伴い取り消せない。Write の成功を見てから、次の応答で
投稿する(#701)。

本文ファイルを持つ投稿(`gh issue|pr create|edit|comment`)は、**その投稿だけを 1 回の
コマンドにする**。`&&`・`;`・`|`(`| tail -2` のような出力を整える後段を含む)で、他の
コマンドと並べない(`... --body-file <絶対パス> | tail -2` は `gh-noncanonical` に拒否された。
拒否の文言も、その投稿だけを 1 回で実行するよう案内している。#981)。結果の整形が要る
ときは、投稿を実行してから、別の呼び出しで読む。

## 1. 本文スケルトン

```
Closes #N / No-Issue: <理由>
Stack: base #<親PR番号>  ← stacked PR のときだけ(ADR-0027 によりセッション内 2 本目以降の PR は既定で該当する)

## 課題
解決したい問題を簡潔に(経緯の全列挙はしない)

## 解決策
採用案 + 棄却した代替案とのトレードオフ
既存手段: <path> — 採用|拡張|自前 — ...  ← 新しい道具・単位を追加したときだけ(ADR-543、書式は technology-selection スキル §4)

## Before / After
画像(--attach)またはコードブロック対比。なければ No-Visual: <理由>

## 検証
LLM が実施・確認済みのこと(コマンドと結果)。未実施の項目を `- [ ]` の
task list で書かない — 実施済みの列挙にだけ `- [x]` を使う

## 要確認
払い出した後続 Issue へのポインタのみ、1項目1行で書く:
- #<Issue番号> — <一言>
手順・完了条件は Issue 側(handoff スキル §5 の Human テンプレ)に書く。
Claude が引き続き担当する残作業はここに入れず「検証」または専用の
説明に書く。両方とも無ければセクションごと省略
```

1行目(`Closes #N` / `No-Issue:`)は既存の pr-gate(`G_link`)が機械的に強制する。`## Before / After` の証跡有無は `G_visual` が機械的に強制する(いずれもこのリポジトリの `crates/pr-gate`)。本文に未チェックの task list(`- [ ]`)が無いこと、`## 要確認` の各項目に Issue 参照(`#N` または issues URL)があることは `pr-followup-guard`(`crates/pr-followup-guard`、設計は `docs/agents/pr-followup-guard.md`)が作成時に機械強制する。それ以外(課題・解決策・検証・要確認の払い出し先の妥当性、および `Stack:` 行)はゲートの検査対象ではなく、この本文スケルトンが唯一の規律。`Stack:` 行は stacked PR のときだけ書く(手順は `stacked-pr` スキルを参照。ADR-0027 によりセッション内 2 本目以降の PR は既定でこれに該当する)。最下段は `Stack: base main` と書く(段番号・総段数は書かない、#657)。`既存手段:` 行も含め、既存の `## 解決策` 節の規律は変更していない(`G_prior` は既に pr-gate に実装済み)。

**マージしても閉じたくない追跡 Issue**(例: 「stable が追いついたら overlay を畳む」のように、
条件が満たされるまで開けておく Issue)を参照するときは、`Closes #N` と書かない。マージで
追跡 Issue が閉じてしまう。1 行目は `No-Issue: <理由>(参照: #N)` の形で書く。同じ誤りが
繰り返されるなら、`G_link` で `Closes` 先が `tracking` ラベルや「畳む」系の題名のときに
警告する昇格を検討する(ADR-543 の昇格型。#825)。

**`Closes #N` を書くためだけに、PR の直前に Issue を立てない**(ADR-1529、共有 AGENTS.md
「Issue に置くのは…」)。PR で完結する仕事は `No-Issue: <理由>` で出す。理由の例: 「この
セッションで見つけて、この PR で直した」「計画の段 k」。PR の直前に起票して同じ日に閉じた Issue
(累計 31 件、中央値 30 分)は、PR 本文に書ける内容を先に Issue に書いただけだった。`promotion-detect`
が、PR で 1 日以内に閉じたコメントの無い Issue を日次で数え、wrap-up inbox に流す。

## 2. Visual の範囲

「見た目に影響する変更」は GUI/Web の画面変化に限らない。ターミナル/TUI の見た目(プロンプト、statusline、サイドバー、コマンドのレンダリング結果)も含む広義で判断する。テキストの差分だけで変化が十分伝わる場合(設定ファイルの数値変更など)は、画像の代わりに `## Before / After` 見出し配下へ fenced code block で対比を書いてよい。

## 3. `gh --attach` で画像を貼る(gh 2.99.0 以降)

`gh pr create|edit|comment`(および `gh issue create|edit|comment`)に repeatable な `--attach <path>` フラグが使える。`--attach './after.png#Alt text'` の `#` 以降が alt テキストになる。本文中に同じローカルパスの画像記法が既にあれば、その位置がアップロード後の URL に書き換わる。無ければ本文末尾に追記される。

制約: 画像・動画のみ(画像は10MB上限)、対象リポジトリへの write 権限が必要、GitHub.com / GitHub Enterprise Cloud のみ(GHES 非対応)。プライベートリポジトリの添付 URL は閲覧に認証が必要(public リポジトリでは無関係)。

```
gh pr create -R OWNER/REPO --title "..." --body-file /abs/path/pr-body.md \
  --attach './before.png#Before' --attach './after.png#After'
```

## 4. Before の取り方

Before は変更を当てる**前**に撮る。変更後に「そういえば」と気づいても、変更前の状態はもう手元に無い。次のいずれかで確保する:

- 変更に着手する前に、対象コマンド/画面を先に撮っておく
- 変更前の状態が別 worktree(main のチェックアウト)に残っているなら、そちらで撮る
- 作業中の変更を一時的に退避してから撮る(このリポジトリでは `git shelve` / `git unshelve`)
- 変更前の SHA を一時 checkout して撮る

新規追加などBeforeが存在しない正当なケースでは、After単独でよい。その場合は本文に「Before: なし(<理由>)」と明記する(省略ではなく明記。ゲートは検査しないが、レビュアーが「撮り忘れ」と「元から無い」を区別できるようにする)。

## 5. 面ごとの撮り方

| 見た目の面 | 手段 |
|---|---|
| Web / HTML(ブラウザで見る画面) | **§5b の固定の手順**(`scripts/visual_diff.py`)で撮る。Before | After | Diff を並べ、本人に見せる。下の 2 行は、このスクリプトが使えない環境の代替 |
| (§5b が使えないとき)Web / HTML(Playwright が `file:` を拒否する環境。`Access to "file:" protocol is blocked`) | スクラッチのディレクトリに HTML を置き、`python3 -m http.server <port> --bind 127.0.0.1` を別の呼び出しでバックグラウンドに立て、`http://127.0.0.1:<port>/<ファイル>` を `browser_navigate` で開く。db などを呼ぶページは、スクラッチ側のコピーの先頭に疑似の差し込み(例: `window.claude` の疑似)を足し、リポジトリの本物のファイルは変えない。スクリーンショットの保存先は、許可された範囲(作業ツリーと `.playwright-mcp/`)に限られ、スクラッチの絶対パスは拒否されるので、作業ツリー内の相対パスで撮る。`gh --attach` でアップロードしたら、サーバーを止め、撮った画像と `.playwright-mcp/` の中身(ページの本文や電話番号などの本人情報を含みうる)を消し、`git status` に未追跡のファイルが無いことを確かめる。**sandbox の中で立てたサーバーに、Playwright のブラウザが届かないことがある**(2026-11-19、`NS_ERROR_CONNECTION_REFUSED` で、`file:` も拒否された。3 回試して node での実行に替えた)。サーバーを sandbox の外で立てれば届くかは未確認。届かないときは、立てた手順と拒否を記録して、別の手段(下の Chrome の行、または後続 Issue への払い出し)へ進む |
| (§5b が使えないとき)Web / HTML(Playwright が使えない環境) | headless Chrome 直叩きにフォールバックする。Chrome は sandbox の中では Unix ソケットを作れず落ちるので、`google-chrome --headless=new *` は sandbox の除外コマンドで、外で動く(`home/modules/claude.nix`、#1334)。外では全権限で動くので、毎回 ask の確認が出る。承認を待つ前提で呼ぶ。除外は呼び出し全体の一致で決まるので、`google-chrome` は単体で呼ぶ(`mktemp` や `rm` を連結しない)。プロファイルの置き場は先に別の Bash 呼び出しで `mktemp -d` して、出力されたパスを次の呼び出しへ文字で渡す: `google-chrome --headless=new --screenshot=out.png --window-size=W,H --hide-scrollbars --user-data-dir=<mktemp の出力> file:///path/to/page.html`。`--hide-scrollbars` を忘れるとビューポートより大きい要素でスクロールバーが写り込む。`--user-data-dir` は毎回 `mktemp -d` で使い捨てにする — 固定プロファイルを使い回すと、ファイル更新後に撮り直しても古い内容がキャッシュされたまま再レンダリングされることがある。`$(mktemp -d)` をコマンド行に直接埋め込まない: シェルを介さない呼び出し(Python の `subprocess` に渡す引数リスト、Node の `spawn` の引数配列、Playwright の `launch` の `args` など)では展開されず、`$(mktemp -d)` という名前のディレクトリがカレントに作られて、Cookie や履歴を含むプロファイルごとコミットされる事故になる。撮影後は `rm -rf <プロファイルのパス>` で消し、`git status` に未追跡のディレクトリが出ていないことを確かめる |
| 図(SVG)を PNG にして添付したい | `rsvg-convert -o out.png in.svg`(librsvg。`home/modules/packages.nix`、#1334)。ブラウザを使わないので sandbox の中で動き、承認も要らない。幅を指定するなら `-w <px>`、背景を白にするなら `-b white`。`rsvg-convert` が無い機体(darwin、`hms` 前)は、下の SVG の行のとおり SVG のまま添付するか、上の Chrome の行を使う |
| ローカルの画像/SVG ファイル(実描画範囲がキャンバス全体より小さい場合を含む) | ファイルが最終成果物ならそのまま添付する。SVG で余白が大きい場合は `viewBox`/`width`/`height` から実寸を読み取って撮影ウィンドウを合わせるか、実描画内容のバウンディングボックスを計算して Pillow 等で最終クロップする(bbox 計算手段がリポジトリ側にあればそれを流用する) |
| ターミナル出力の見た目(プロンプト、statusline、コマンド出力の色/レイアウト) | ANSI 出力を画像化するツール(`cmd \| freeze -l txt -o out.svg` のように、パイプで受けた出力を画像化できるものを選ぶ — 変更前に保存しておいた出力から後で画像化できるのが利点。出力形式は SVG か WebP を使う。charm-freeze はホストによっては PNG エンコーダがクラッシュすることがある) |
| 対話的 GUI(実機の画面操作が要るもの) | LLM では撮れないため、後続 Issue に払い出し(ユーザーにスクリーンショットを依頼)、`## 要確認` からその Issue を参照する |

LLM で撮り切れる範囲は極力撮り切り、「要確認」は人間にしかできない残作業だけに絞る。

### 5a. リポジトリ外の Artifact が成果物のとき

成果物が、リポジトリの外の非公開 Artifact(Slides など)のとき、Artifact 種別の手順が
「依頼がない限り、描画の確認(読み戻し、スクリーンショット、画面を開くこと)をしない」と
定めていて、この節の Before / After の要求とぶつかる。次の 2 つを両方行う。

- **公開する前に、描画の確認をしてよいかを、本人に 1 回聞く。** 種別の手順の禁止は「依頼が
  ない限り」なので、本人が確認を頼んだ(許可した)なら、禁止の対象外になる。許可が出たら、
  撮って `## Before / After` に添える。
- **確認しない(許可が出ない、聞けない)ときは、本文の冒頭で「描画は確認していない」と
  述べる。** `No-Visual:` と理由を書くだけで済ませない。作成者が一度も画面を見ないまま
  渡すと、受け取った人が「意味が取れない」と指摘する事例があった。本人が見るべき確認
  (内容が伝わるか、言い過ぎが無いか)を後続 Issue に払い出してよいが、作成者の確認の
  代わりにしない。

### 5b. 見た目の変更は、固定の手順で撮り、Before | After | Diff を本人に見せる(ADR-1698)

画面(HTML・Artifact の雛形)の見た目を変える変更は、散文の手順でなく、次の固定の手順で撮る。撮影・差分・並べたページの生成は
`scripts/visual_diff.py`(`uv run --script`。PEP 723 で依存を宣言する。使い方は冒頭の docstring)が担う。理由は、手で撮ると
(1) 変更の後に Before を撮り損ねる、(2) 明が効かない・幅が 0.75 倍になる Firefox の制約(`docs/agents/personal-web-app.md` §7)に
当たる、(3) 初期状態だけを撮って失敗・押下の状態の問題を拾えない、(4) 差が小さくて本人が読めない、からである。

1. **着手前に Before を撮る。** 面のデータの隣に撮影定義 `visual.toml` を置き(無ければ、先に書く。例は裁定ページの
   `reference/verdict-page/visual/visual.toml`)、`visual_diff.py capture --spec <visual.toml> --ref <基準の ref> --out <dir>/before`。
   画面のファイルは**基準の ref から取り出す**ので、変更後に Before を撮れない。stacked PR では、基準 = 直前の段のブランチ。
2. 実装する。
3. **After を撮り、Diff を出す。** `capture --ref WORKTREE --out <dir>/after`、続けて `diff --before <dir>/before --after <dir>/after --out <dir>/diff`。
   撮る行列は固定: 明・暗 × 幅 390px・1280px × 撮影定義の状態(初期・データあり・押下・失敗・空)。**初期状態だけで撮り終えない。**
   画面に差し込むデータは合成データだけ(実データを撮影定義に置かない)。出力: セルごとの Before | After | Diff(赤が変わった画素)と、
   高い画像には変更箇所の切り出し、`report.json`。差の無いセルは「差なし」と出る(見た目を変えない整理の証跡にもなる)。
4. **本人に見せる。** `page --report <dir>/diff/report.json --title <題> --out <公開用の置き場>/index.html` で並べたページを作り、
   画像(`*.png`)と一緒に `publish_files` で非公開の Artifact として公開し、**リンクをチャットに出す**。公開用の置き場は、パスに
   ユーザー名を含まない場所(`$TMPDIR` の直下など。`publish_files` は非公開名を含むパスを拒否する)。リンクを出したあとは、本人の
   返事を待たずに次へ進む(NG は PR 上で受ける)。リポジトリ外の Artifact の描画確認(§5a)は、この手順で本人が許可している。
5. **PR に添付する。** `## Before / After` に、差があるセルの画像(切り出し)を `gh --attach` で貼り、Artifact のリンクと、差なしのセルの
   一覧を書く。基準が無い新規の面は「Before: なし(理由)」。
6. 撮影中に出た注意(遮断した第三者への要求・ページのエラー・横スクロール)は、報告に載せる。
7. **ページの型の要件を検査する。** 撮影定義の面に、当てはまる型を `types = ["common", "form"]` のように宣言し(省略は common だけ。型は
   `config/web/page-types.toml`)、`visual_diff.py audit --spec <visual.toml>` を走らせる。描画した HTML で測れる要件(文書の基本・コントラスト・
   操作部の大きさ・横スクロール・第三者への要求・ボタンのキー操作・主操作の数・初期の選択・`confirm`)を、撮影と同じ行列で検査し、違反を
   要件の ID と出たセルつきで出す(違反があれば終了コード 1)。**機械で測れない要件は「未検査(人が見る)」として並ぶ。通ったことにしない。**
   見た目の変更では、違反が増えていないことを、Before(基準の ref)と After(作業ツリー)の `audit` の出力で比べ、PR の「検証」に書く(ADR-1701)。

撮影は Chromium で行い、sandbox の中で動く(2026-11-24、`--selftest --browser` で、決定的な再現・明暗の描き分け・幅を確かめた)。
`visual_diff.py --selftest`(ブラウザ無し)は CI が走らせる。設計の根拠と限界は `docs/agents/visual-diff.md`。

## 6. 要確認の粒度と後続 Issue への払い出し

PR 作成後に残作業(マージ後の適用・外部サービスでの操作・動作確認など)がある
とき、それを機械的に全部「要確認」へ流さない。マージは CI とレビューだけで
決め、人の確認が要る残作業はマージの条件にしない。書く前に必ず次の順で
処理する:

1. **残作業を列挙**する(このスケルトンの「検証」を書く過程で自然に出てくる
   はず)。
2. **各項目を「Claude が実行できるか」で仕分ける**。実行できるなら今すぐ
   実行する — 依存関係(例: ユーザー操作の完了を待たないと着手できない)が
   無い限り、着手を待たない。「後で書けばいい」は理由にならない。
3. **ブロッキング理由を持つ項目だけ**を後続 Issue に払い出す。ブロッキング
   理由は次のいずれかに限る(このリポジトリの ADR-0003 が YubiKey 挿入・鍵の
   手動 import を「hardware-bound で宣言化できない」と切り分けた判断と同型):
   - 資格情報の発行・認証(外部サービスへの人間のログインが要る。
     ブラウザ操作中の未ログイン検知そのものへの対処手順は
     `browser-login-handoff` skill を参照)
   - ハードウェア操作(実機の抜き差し・ボタン操作)
   - secrets 衛生(生の値を Claude の tool-call 経由・会話ログに通すべき
     でない — 復号や配置自体は技術的に代行できても、値の受け渡し経路として
     不適切ならブロッキング側に倒す)
   - GUI/対話的操作で LLM から撮れない・操作できないもの
   - 人間の判断・選好が要る意思決定
   - 上記のいずれにも当たらない「単に面倒/時間がかかる」は該当しない —
     それは Claude が今すぐ実行する。
4. **ブロッキング項目の払い出し先を決める。実機確認は台帳 Issue に追記し、
   それ以外は項目ごとに後続 Issue を1件起票する**(`handoff` スキル §5
   の「残タスク1件 = 子Issue1件」と同じ発想。実機確認の例外は後述):

   **実機確認は 1 項目 1 Issue にしない(#1506、ADR-1529 の置き場 6)。** 同じ機体・同じ接続で
   1 回の作業で確かめられる実機確認は、その単位の「台帳 Issue」(ベンチ 1 セッション =
   1 Issue)の本文に、閉じた形の 1 行で足す。機体の台帳は、題を `verify-ledger: <host>`
   (`<host>` は `~/.config/dotfiles/host` の値)にした常設の Issue で、機体ごとに 1 件だけ持つ。
   1 行の形は次のとおり(`issue-index` が SessionStart にこの形を読み、その機体で着手できる
   項目を注入する。`docs/agents/issue-index.md`「確認の台帳」):
   ```
   - [ ] after:#<この PR の番号> <machine|human> — <何を確かめるか> — check: `<コマンド>`
   ```
   待つ PR の無い確認(機器の使い勝手、本人の操作だけで済む導入)は `after:-` と書く(いつでも着手できる)。
   `machine` はコマンドの終了コードと出力で判定できる項目(エージェントがその機体で実行する)、
   `human` は本人の感覚・操作が要る項目(表示の見た目・LED・音・資格情報の入力・再起動)。
   `human` の行も、手順と完了確認を行の中か、すぐ下の字下げした行に書く。
   1. 台帳を探す: `gh issue list -R <owner/repo> --state open --search "verify-ledger in:title"
      --json number,title,body` で、題が `verify-ledger: <host>` に完全に一致する Issue を読む。
      ベンチや接続の単位の台帳(機体でない単位)も、同じ接頭辞と形で持つ。
   2. あれば、新しく起票せず、その Issue の本文に行を `gh issue edit --body-file` で足す。
      Issue 本文が正本なので、コメントだけに書かない(`living-description`)。3 ホストで確かめる
      項目は、3 つの台帳にそれぞれ 1 行ずつ足す(ホストをまとめた 1 件にしない。#682・#990 は
      altair の分だけが残って、40 日 open のままだった)。
   3. 無いときだけ、題 `verify-ledger: <host>`・ラベル `handoff:human` で起票し、それを
      その機体の台帳にする。
   4. 実装の Issue の close 条件には、実機確認を入れない(実装は PR のマージで閉じる。
      マージ後に実機確認だけが残る Issue を作らない)。
   5. 確かめたら、その行を `- [x]` にして、行の末尾に結果(終了コード・出力の要点・日付・機体)を
      書く。行の削除はしない(済んだ記録として残す)。「変化なし」のコメントは書かない。
      変換は `~/.claude/hooks/issue-index ledger <機体> --mark <語> --result <結果> --out <ファイル>`(新しい行は
      `--add <行> --section <節>`)に任せる(sandbox の外で実行。出力された
      `gh issue edit <番号> --body-file <ファイル>` で反映する。`docs/agents/issue-index.md`)。
   6. build の検査(`home.checks` の canary など)で確かめられる項目は、台帳に積まず、検査の
      fixture を足す(機体ごとの確認が要らなくなる)。
   `## 要確認` のポインタは、これまでどおり `- #N — <一言>` だけで、`pr-followup-guard`
   の検査は変わらない。実例は `cases.md`。

   台帳に束ねない項目(別の機体、別の接続、人の判断、資格情報の発行)は、次の
   とおり1件起票する:
   ```
   gh issue create -R <owner/repo> --title "<やること>" \
     --body-file <絶対パス> [--label handoff:human] [--assignee <確認者>]
   ```
   本文は Write でファイルにしてから渡す(§0)。
   本文は `handoff` スキル §5 の Human テンプレ(`## やること` / `## なぜ
   人手か` / `## 手順` / `## 完了条件`)を使い、生成元フッターを付ける。
   `handoff:human` ラベルは、対象リポジトリに存在するときだけ付ける
   (`bash config/agents/skills/handoff/scripts/handoff.sh labels-missing
   <owner/repo>` で確認。存在しないリポジトリでラベルを新設しない)。
   親 Issue は、この PR が `Closes` する Issue があればそれを `--parent` に
   使い、無ければ親無しで単独起票する。PR 本文の `## 要確認` にはその Issue
   番号だけを `- #N — <一言>` の形で書く — 手順・完了条件は Issue 側にある
   ので本文への重複は書かない。Issue を PR より先に起票し、本文で `#N` を
   参照すれば GitHub の cross-reference が Issue 側に自動で PR を表示する
   ので、Issue 側からの追記は不要。払い出した Issue が軽い人手タスク(`handoff:light`)なら、
   同じセッションで `handoff` スキル §7 まで進めて予定に入れる(待ちがあっても待たない)。
5. **手順を接地する**: Issue の `## 手順` を書く前に、対象リポジトリ/Issue に
   既存の runbook が無いか、操作対象が UI なら公式ドキュメントに正確な画面名・
   項目名の記載が無いかを検索し、見つけたら URL(または Issue/PR 番号)と
   取得日を手順の完了条件の近くに引用する。手順の中で人間に選択を委ねない
   —「該当するものを選んでください」ではなく、値・項目名・画面遷移を
   すべて具体的に書き切る。値そのものが機密で本文に書けない場合は、値を
   取得するコマンド(クリップボードへ直接パイプする等、生値を端末に残さない
   形)を書く。この規律は PR 本文に限らず、チャット・Issue・docs で人に
   依頼する手順すべてに掛かる(共有 `AGENTS.md`「人に依頼する手順は、場所を
   問わず『フル』で書く」が正本)。
6. **ブロッキングでない残作業がまだ完了していない場合**(依存関係で待って
   いるだけ)は、「要確認」に入れず、「検証」の末尾か本文の短い1段落で
   「これは自分が引き続き担当する」と明記する。ユーザーから見て「誰も
   拾っていない宙に浮いた作業」に見えないようにする。

`## 要確認` の各項目に Issue 参照(`#N` または issues URL)があること、
本文全体に未チェックの task list(`- [ ]`)が無いことは `pr-followup-guard`
(`crates/pr-followup-guard`)が `gh pr create/edit` の呼び出し時に機械検査する——払い出し先の Issue が
妥当か・手順が実際に正しいかまでは検査しない(`G_visual` と同じ二層分担)。

この規律に違反した実例(粒度): esa MCP のトークン供給を切り替えた PR
(tarotene/dotfiles#239)で、Claude が実行可能な「登録の適用」「動作確認」
「旧リポジトリの archive」をすべて「要確認」に書き、ユーザーに「これは
私がやることですか」と指摘された。再仕分けした結果、真にブロッキングな
項目は「外部サービスでの資格情報発行」1件だけで、残りは Claude が並行して
実行できた。

この規律に違反した実例(接地): 別の事例は `cases.md` を参照(ブロッキング
理由は正しく絞れていたが、手順が「クラウド環境の credentials に登録する」
としか書かれておらず画面遷移も完了確認も無かった)。

この規律に違反した実例(要確認と未チェック task list の混同): 実機確認を
`## Test plan` の未チェック `- [ ]` としてそのまま残し、確認者の予定を
マージ条件にした事例は `cases.md` を参照。

## 6a. 検証に「消費者の確認」を含める

PR 本文の「検証」には、編集したファイルを入力にする CI の検査(消費者)を引いた結果も書く。
`ci-consumers <編集したパス>...`(リポジトリの根で呼ぶ)が、そのパスを読む workflow の step・
composite action・scripts・crates の tests を列挙する。出た step を手元で走らせた結果(または、
消費者が無いこと)を、コマンドと結果で書く。ファイルを一括編集する前に引かないと、配布元
テンプレートとのバイト一致の検査のように、そのファイルを入力にする CI が、CI で初めて落ちる
(`docs/agents/ci-consumers.md`)。

`ci-consumers` は home-manager が `~/.local/bin` に置くので、どのリポジトリの根でも呼べる。PATH に
無くて終了コード 127 になる(まだ `hms` していない機体など)ときは、次の代替で同じ問いに答える:

```
git grep -n -F -- '<編集したパス>' -- .github/
```

出た workflow の step を読み、そのパスを入力にする検査(`run:` のコマンド、`paths:` の絞り込み、
composite action の入力)を列挙して、検証に書く。リポジトリに `scripts/` や `crates/*/tests/` が
あるときは、`-- .github/ scripts/ 'crates/*/tests/'` のように範囲を足す。`git grep` は固定文字列の
検索なので、パスを組み立てて参照する消費者は拾えない(拾えないことと、無いことは別)。

## 7. 完成の定義(二層)

- **意味的完成**(この本文の完成条件): ビジュアルが絡む変更では、Before と After の**両方**の証跡を載せる。コードブロック対比でも同様に両方を含める。Before が存在しない正当ケースのみ、After単独 + 「Before: なし(<理由>)」の明記で足りるとする。
- **機械的下限**(`G_visual` が実際に検査する条件、3択のOR): (a) アップロード済み画像(ローカルパスのままの画像記法は数えない)、(b) `## Before / After` 見出し配下の fenced code block、(c) `No-Visual: <理由>`。この3つのいずれかを満たせば `G_visual` は通る。

`G_visual` を通ることは必要条件であって、完成の定義そのものではない。ペア性(Before/Afterが揃っているか)はゲートが検査しないので、上の意味的完成の基準を自分で満たす。画面の変更では、§5b の固定の手順が「揃っている」の定義になる(Before は基準の ref から取り出したもの、After は作業ツリー、Diff と差なしの一覧、本人に見せた Artifact のリンク)。

事例は `cases.md` を参照。追記時のサニタイズ規則は `agent-tooling-authoring` を参照。

## CI 障害の調査

CI の失敗を扱うときは `reference/ci-failures.md` を必ず読み、環境障害と実行済みテストの失敗を区別する。

フォーム保存・アクセス障害を扱うときは `reference/browser-operations.md` を必ず全文読む。ログイン引き継ぎは `browser-login-handoff` に従う。
