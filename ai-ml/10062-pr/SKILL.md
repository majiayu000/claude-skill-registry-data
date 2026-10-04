---
name: pr
description: Generate a GitHub pull request title and body from the current branch, then let the user review before creation in manual mode or create it without confirmation in auto mode. Use when the user wants to create a pull request.
argument-hint: "[manual|auto]"
allowed-tools: AskUserQuestion, Bash(git status:*), Bash(konoka-pr-editor:*), Bash(prepare-editmsg:*), Bash(run-commit-msg-hook:*), Bash(sync-and-push:*), Edit, Read, Skill(pr-style), Write, mcp__github__create_pull_request, mcp__github__issue_write
model: opus
effort: low
---

GitHubのpull requestを作成します。
AIがタイトルと本文を生成し、
`manual`確認モードではユーザが確認してから作成します。
`auto`確認モードでは確認を省略してそのまま作成します。
このスキルは新規作成のみを扱います。
既存PRの更新は対象外です。

# 確認モードの決定

`$ARGUMENTS`を確認モードとして解釈してください。

- `manual`: ユーザにタイトルと本文を提示し、
  確認を取ってから作成します。
- `auto`: 確認を省略して、
  生成した内容でそのまま作成します。
  内容自体は`manual`と同じタイミングで提示します。

引数が省略された場合は`manual`として扱ってください。

`manual`とも`auto`とも解釈できない値が渡された場合は、
`manual`として扱った上で、
解釈できなかった値を完了報告で伝えてください。
勝手に`auto`とみなして確認を省略してはいけません。

以降の手順のうち、
対象の確認モードが明記されているセクションは、
決定した確認モードに対応するものだけを実行してください。
明記のないセクションはどちらの確認モードでも実行してください。

# スタイルガイドラインの適用

`Skill(pr-style)`を呼び出し、
スタイルガイドラインに従ってください。

このスキルがリポジトリ固有のCONTRIBUTINGとpull requestテンプレートを探索して読み込むため、
このスキル内で改めて読み込む必要はありません。

# baseとの同期とremoteへのpush

!`sync-and-push`

上記の埋め込みコマンドは、
baseブランチとの同期(必要ならrebase)に続けて、
headブランチをremoteへ同期します。

このスクリプトは以下を行います。

- 現在のブランチがbaseブランチでないことを確認します。
- baseブランチに切り替えてpullし、元のブランチに戻ります。
- baseブランチが進行していた場合は元のブランチをbaseの上にrebaseします。
  PR作成後にbaseが進行するとGitHub上でupdate baseの作業が必要になりますが、
  作成前にrebaseしておくことでこれを回避します。
  PR作成前なのでrebaseで履歴が書き換わっても他者に影響しません。
- upstream未設定なら`git push -u origin <current>`で初回pushします。
- upstreamと完全一致なら何もしません。
- ローカルが先行(fast-forward可能)なら`git push origin <current>`で通常pushします。
- 履歴が分岐(force pushが必要)なケースでは、
  まず同名ブランチをheadとするopen PRが存在しないことを`gh pr list`で確認し、
  存在しない場合のみ`git push --force-with-lease origin <current>`で上書きします。

スクリプトの出力は`key=value`形式で、

- `current`
- `base`
- `owner`
- `repo`
- `rebased`
- `action`

が1ブロックにまとまって含まれます。

`action`は、

- `none`
- `initial`
- `normal`
- `force`

のいずれかです。

これらの値を以降のステップで使用してください。

スクリプトの実行が失敗していた場合はエラーメッセージをそのままユーザに報告し、
PRの作成は中止してスキルを終了してください。

rebaseがコンフリクト等で失敗した場合は、
スクリプト内で`git rebase --abort`が呼ばれてrebase状態は巻き戻されています。

特にforce pushが必要だが対象ブランチに対してopen PRが既に存在するケースでは、
スクリプトはforce pushを行わずにエラー終了します。
このスキルは新規PR作成のみを扱うため、
既存PRがある場合はスキルの実行をキャンセルし、
ユーザに既存PRの更新を促してください。

# PR内容の準備

`pr-style`スキルのガイドラインに従い、
コミット履歴とdiffの把握、
タイトルと本文の生成、
アサインとラベルの決定を済ませてください。

PRに含まれるコミットが1つだけの場合は、
そのコミットメッセージのタイトルと本文をそのまま流用してください。

複数コミットがある場合は、
PR全体の変更を要約するタイトルと本文を新たに書いてください。

# 一時ファイルへの書き出し

以下のスクリプトでセッション固有の一時ディレクトリを作成し、
`PULLREQ_EDITMSG`ファイルのフルパスが取得されます。

!`prepare-editmsg`

スクリプトは`$XDG_RUNTIME_DIR/coding-agent-work/pr/`配下にディレクトリを作り、
存在しない場合は再帰的に作成します。
未設定環境では`os.tmpdir()`にフォールバックします。

得たパスに`Write`ツールで内容を書き出してください。
ファイルは1行目をタイトル、
空行を挟んで本文という構造にします。

# タイトルと本文の検査

書き出したら以下のコマンドで検査してください。

値は実際のファイルのパスに置き換えてください。

```bash
run-commit-msg-hook <PULLREQ_EDITMSGのパス>
```

このコマンドは`commit`プラグインが提供します。
`git commit`が起動するのと同じ`commit-msg`フックを同じ方法で起動します。
グローバル設定のフックも作業中のリポジトリのフックも対象です。
フックが設定されていない場合は何も検査せずに成功します。

PRのタイトルはコミットメッセージと同じくConventional Commits準拠なので、
`PULLREQ_EDITMSG`はコミットメッセージと同じ構造として検査できます。

コマンドが失敗した場合は、
出力された指摘に従ってタイトルと本文を修正し、
このコマンドを再実行してください。

ただしリポジトリのpull requestテンプレートに由来する部分への指摘など、
PRとして必要な内容を壊さないと直せない指摘もあります。
その場合は無理に修正せず、
指摘の内容をユーザに報告して指示を仰いでください。

3回修正しても検査を通らない場合も同様にユーザに報告してください。

フックはメッセージファイルを書き換えることがあるため、
検査を通ったら`Read`ツールでファイルを読み直して、
以降のステップではその内容を使ってください。

# ユーザによる確認

`manual`確認モードのみのステップです。
`auto`確認モードでは`PR内容の提示`へ進んでください。

`AskUserQuestion`ツールを使って、
生成したタイトル、本文、アサイン、ラベルの扱いをユーザに確認してください。

質問文にはタイトルと本文の全文に加えて、
アサインするユーザと付与するラベルも含めてください。
本文が長い場合でも省略せず全文を提示してください。
ユーザが内容を見て判断できるようにするためです。

選択肢は以下を設定してください。

1. このまま作成する(Recommended): 生成された内容で作成する。
2. テキストエディタで編集する: エディタで編集してから作成する。

`AskUserQuestion`ツールはこれらに加えて`Other`(自由テキスト入力)の選択肢を自動的に追加します。
`Other`が選ばれた場合はユーザの修正指示に従って内容を修正し、
確認ステップに戻ってください。

## このまま作成する場合

一時ファイルの内容をそのまま使用して、
PR作成に進んでください。

## テキストエディタで編集する場合

以下のコマンドでユーザに編集してもらいます。
タイムアウトは最大の600秒に設定してください。

```bash
konoka-pr-editor <PULLREQ_EDITMSGのパス>
```

エディタが正常終了したら、
`Read`ツールでファイルを読み直して内容を取得し、
PR作成に進んでください。

エディタが異常終了した場合、
ユーザがPR作成をキャンセルしたいという意思表示であると解釈して、
作業をキャンセルしてください。

## 選択がキャンセルされた場合

ユーザがPR作成をキャンセルしたいという意思表示であると解釈して、
作業をキャンセルしてください。

# PR内容の提示

`auto`確認モードのみのステップです。
`manual`確認モードでは`PRの作成`へ進んでください。

生成したタイトルと本文の全文に加えて、
アサインするユーザと付与するラベルをテキストメッセージとして出力してください。
本文が長い場合でも要約や省略をせず、
そのまま全文を出力してください。

`AskUserQuestion`ツールは呼び出さず、
ユーザの応答も待たずにPRの作成に進んでください。

確認は取らないのに内容を提示するのは、
`manual`確認モードと同じタイミングで内容が目に入るようにするためです。
PRの作成後に報告されるより、
作成の直前に流れているほうが読み手の追いやすさで一貫します。

# PRの作成

`mcp__github__create_pull_request`を使ってPRを作成してください。

引数は以下の通りです。

- `owner`: `sync-and-push`の出力の`owner`
- `repo`: `sync-and-push`の出力の`repo`
- `head`: `sync-and-push`の出力の`current`
- `base`: `sync-and-push`の出力の`base`
- `title`: 生成したタイトル
- `body`: 生成した本文
- `maintainer_can_modify`: `true`
- `draft`: ユーザが明示的に指示した場合のみ`true`、それ以外は省略

`maintainer_can_modify`は、
GitHubの`Allow edits and access to secrets by maintainers`に対応します。
forkからのPRでもmaintainerがブランチを直接修正できるように、
常に有効化します。

organizationが所有するforkからのPRなど、
`maintainer_can_modify`が原因で作成が失敗した場合は、
`maintainer_can_modify`を省略して作成し直してください。

GitHubのPR作成APIはassigneesとlabelsの同時設定に対応していないため、
これらは作成後に別ステップで設定します。

作成に成功するとPR番号とURLが返ります。
それらを次のステップで使用してください。

# アサインとラベルの一括設定

PR作成からアサイン/ラベル設定までのタイムラグを最小化するため、
このステップとPRの作成の間に他の処理を挟まないでください。
アサインとラベルの選定は事前に済ませている前提です。

`mcp__github__issue_write`を`update`メソッドで呼び出し、
作成したPRの番号を`issue_number`に渡し、
`assignees`と`labels`を1回で設定してください。

- `method`: `"update"`
- `owner`: `sync-and-push`の出力の`owner`
- `repo`: `sync-and-push`の出力の`repo`
- `issue_number`: 作成したPRの番号
- `assignees`: `pr-style`スキルで決定したloginの配列
- `labels`: 選定したラベル(該当なしの場合は省略可)

# 権限不足の場合

他人のリポジトリにPRを作成しようとしている場合など、
権限不足でアサイン設定やラベルの設定が出来ない場合があります。
その場合はエラーを検知して、
PR自体は作成されたことを報告してください。

# 完了報告

PRのURL、アサインしたユーザ、付与したラベルを含めて完了報告してください。

`auto`確認モードでも作成の直前にタイトルと本文を出力しているため、
報告で全文を繰り返す必要はありません。
