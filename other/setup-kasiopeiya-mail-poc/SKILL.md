---
name: setup
description: テンプレートから作ったリポジトリの立ち上げを、1コマンドで進める。GitHub の設定を変え、ファイルを消すので、人間が `/setup` と打ったときだけ動く。
disable-model-invocation: true
---

# /setup

立ち上げの手順の正はこの Skill である。

## この Skill で使う語

- **`/setup` の変更**：各手順が書き換えるパス（`docs/adr/`・`docs/project-context/project-claude.md`・`docs/project-context/core-parts.md`・`docs/project-context/issue-destinations.md`・`scripts/auto-programmer/config.mjs`）のうち、`git status --porcelain -- docs/adr/ docs/project-context/project-claude.md docs/project-context/core-parts.md docs/project-context/issue-destinations.md scripts/auto-programmer/config.mjs` に出るもの。前回の `/setup` が書き換えて、まだコミットしていない変更も含む（途中で止まって流し直しても、取りこぼさないため）
- **立ち上げの Issue**：`/setup` の変更をリポジトリへ入れる Issue。タイトルに目印の語「立ち上げの準備をリポジトリへ入れる」を含む。次で探す

  ```bash
  gh issue list --state all --limit 100 --search '立ち上げの準備をリポジトリへ入れる in:title' --json number,title,state --jq '.[] | select(.title | contains("立ち上げの準備をリポジトリへ入れる"))'
  ```

- **手作業の Issue**：人間の手作業が済まなかったときに起票する Issue。タイトルに「/setup の手作業：<手順の見出し>」を含む（例：「/setup の手作業：リポジトリ設定を入れる」）。次で探す

  ```bash
  gh issue list --state open --label ready-for-human --limit 100 --search '"/setup の手作業" in:title' --json number,title --jq '.[] | select(.title | contains("/setup の手作業：<手順の見出し>"))'
  ```

- **Bedrock 切り替えの Issue**：Claude の認証方式に Bedrock を選んだときに起票する Issue。タイトルに目印の語「pr-ai-triage を Bedrock 認証に切り替える」を含む。次で探す

  ```bash
  gh issue list --state open --limit 100 --search 'pr-ai-triage を Bedrock 認証に切り替える in:title' --json number,title --jq '.[] | select(.title | contains("pr-ai-triage を Bedrock 認証に切り替える"))'
  ```

## すべての手順に効く決まり

- **済んだ手順は飛ばす**：各手順は、まず済んでいるかを確かめ、済んでいれば飛ばす。途中で止まっても、もう一度 `/setup` を流せば続きから進む（例外は「ボードを作る」で、作りかけのボードを消してから流し直す）。何度流しても同じ結果になるスクリプトを流す手順（「ラベルを作る」「リポジトリ設定を入れる」）は、確かめをスクリプトに任せる
- **人間の手作業は、済まなければ Issue にして進む**：人間にしかできない作業は、何をするかを案内し、`AskUserQuestion` で済ませたかを聞く。済ませたなら確かめ直して次へ進む。その場で済まなければ、手作業の Issue を `/quick-issue` で起票し、次の手順へ進む。ラベルは `ready-for-human` にし、人間のタスクの頭に「（人間）」と書く。同じ手順の手作業の Issue が open で残っていれば、起票し直さない。例外は次の2つで、どちらも Issue にせずに止める
  - 「ラベルを作る」が済むまでの手作業が済まなかった：gh かラベルが無く、Issue を起票できない
  - テンプレート本体のリポジトリで流された：手作業として聞かずに止める（続けると、本体の ADR や設定を消す）
- **変更は、立ち上げの Issue の PR で入れる**：手順が書き換えたファイルは、その場でコミットしない。最後に「立ち上げの Issue を起票する」と「ブランチでコミットして push する」が、まとめてリポジトリへ入れる

## 手順

上から順に進める。

### 前提を確かめる

1. gh が使えるかと、どのリポジトリで流されたかを確かめる。テンプレート本体の場所は `scripts/sync-template.sh` の `TEMPLATE_URL` から引く。

   ```bash
   template=$(sed -n "s/^readonly TEMPLATE_URL='\(.*\)'$/\1/p" scripts/sync-template.sh) && { test -n "$template" || { echo 'scripts/sync-template.sh から TEMPLATE_URL を引けない' >&2; false; }; } && origin=$(git remote get-url origin) && gh repo view "$template" --json nameWithOwner --jq .nameWithOwner && gh repo view "$origin" --json nameWithOwner --jq .nameWithOwner
   ```

   - **失敗した**：gh が無い・未認証・origin が無い・`TEMPLATE_URL` を引けない、のどれか。エラーを見せ、人間の手作業として扱う（gh を入れる・`gh auth login` する・自分のリポジトリを origin に足す・`scripts/sync-template.sh` の `readonly TEMPLATE_URL='…'` の行をテンプレートの形に戻す）。認証は `gh auth status` で確かめない（どれか1つのホストのトークンが切れているだけで失敗する）
   - **2行が同じ**：テンプレート本体のリポジトリである。何もせずに止め、自分のリポジトリを作って origin をそこへ向けてから流し直すよう案内する

2. `node_modules` が無ければ `npm ci` を流す。「テンプレートの ADR を消す」の `npm run gen:adr-index` と、コミット時の git hook が prettier を使う

### ラベルを作る

`./scripts/setup-labels.sh` を流す。

失敗したら、エラーを見せ、人間の手作業として扱う。

### リポジトリ設定を入れる

`./scripts/setup-repo-settings.sh` を流す。最初の push で PR が作られ、CI が動くための設定を入れる。

終了コードが 1 なら、「失敗した」と表示された段を人間の手作業として扱う（管理者権限・組織の設定・プランの制約など、AI には直せない原因のため）。直し方は各段のエラーに添えてある。確かめ直すときは、スクリプトを流し直す。

### ボードを作る

GitHub Projects のボードを API で作る。Auto-Programmer が拾う `Ready` と、レビュー待ちの `In Review` が、新しいボードの Status には無いためである。持ち主はリポジトリの持ち主、名前はリポジトリ名にする。組織が持つリポジトリでも同じステップを流す。失敗したら、末尾の扱いに従う。

1. `project` スコープ（ボードを読み書きする権限）を確かめる。失敗してエラーに `scopes` を含む文が出たら、スコープ不足である。`! gh auth refresh -s project` を案内し、人間の手作業として扱う（「すべての手順に効く決まり」）。それ以外のエラーは、エラーを見せて人間の手作業として扱う。済まなければ、この節の残りを飛ばす。

   ```bash
   gh api graphql -f query='{viewer{projectsV2(first:1){totalCount}}}'
   ```

2. 済んでいれば、この節の残りを飛ばす。**済んでいる**とは、`config.mjs` の `repository` が origin のリポジトリで、`board.owner`・`board.number` のボードが引け、その Status に、ステップ4で入れる選択肢が全部あることである。

   ```bash
   origin=$(gh repo view "$(git remote get-url origin)" --json nameWithOwner --jq .nameWithOwner) && node -e "import('./scripts/auto-programmer/config.mjs').then(({config})=>{if(config.repository!==process.argv[1])process.exit(1);console.log(config.board.owner,config.board.number)})" "$origin"
   ```

   `repository` が違えば何も出ず、終了コード 1 で終わる（テンプレートから作った直後はこうなる）。`<owner> <番号>` が出たら、Status の選択肢を見る。

   ```bash
   gh project field-list <番号> --owner <owner> --format json --jq '.fields[] | select(.name=="Status") | [.options[].name] | join(",")'
   ```

   - `Todo,Ready,In progress,In Review,Done` が出たら、済んでいる
   - 作りたてのボードの `Todo,In Progress,Done` のように足りなければ、済んでいない（`In Progress` は P が大文字で、`In progress` とは別の表記である）
   - `Could not resolve to a ProjectV2 with the number <番号>` のエラーで終わったら、ボードが引けないので、済んでいない

3. ボードを作る。`repositoryId` を渡すので、作成と同時にリポジトリへ紐づく。出力の `<ボードID> <番号>` を以降で使う。

   ```bash
   repo=$(gh repo view "$(git remote get-url origin)" --json nameWithOwner --jq .nameWithOwner) && ids=$(gh api graphql -f query='query($o:String!,$n:String!){repository(owner:$o,name:$n){id owner{id}}}' -f o="${repo%/*}" -f n="${repo#*/}" --jq '.data.repository | "\(.owner.id) \(.id)"') && gh api graphql -f query='mutation($o:ID!,$r:ID!,$t:String!){createProjectV2(input:{ownerId:$o,repositoryId:$r,title:$t}){projectV2{id number}}}' -f o="${ids% *}" -f r="${ids#* }" -f t="${repo#*/}" --jq '.data.createProjectV2.projectV2 | "\(.id) \(.number)"'
   ```

4. Status の選択肢を `Todo`・`Ready`・`In progress`・`In Review`・`Done` にする（表記は [issue-policy](../../../docs/policy/issue-policy.md)「ボードの Status の意味」と同じ）。`updateProjectV2Field` は渡した値で選択肢を上書きするので、残す選択肢には `id` を渡す。まず Status のフィールド ID と選択肢の ID を引く。

   ```bash
   gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{fields(first:30){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}' -f p=<ボードID> --jq '.data.node.fields.nodes[] | select(.name=="Status")'
   ```

   `Todo`・`In Progress`・`Done` の `id` を、次の `<…の id>` に入れて流す（`In Progress` は `In progress` へ改名される）。

   ```bash
   gh api graphql -f query='mutation($f:ID!){updateProjectV2Field(input:{fieldId:$f,singleSelectOptions:[{id:"<Todo の id>",name:"Todo",color:GREEN,description:"ボードに積まれただけ"},{name:"Ready",color:BLUE,description:"着手してよい"},{id:"<In Progress の id>",name:"In progress",color:YELLOW,description:"着手した"},{name:"In Review",color:ORANGE,description:"PR が出た"},{id:"<Done の id>",name:"Done",color:PURPLE,description:"完了した"}]}){projectV2Field{... on ProjectV2SingleSelectField{options{id name}}}}}' -f f=<Status のフィールド ID>
   ```

5. 表ビューを整える。新しいボードには表形式のビュー（`View 1`）が1つあるので、名前を `Backlog` にし、フィルタを `-status:Done`、列を Title・Status・Labels・Assignees にする。`visibleFieldIds` は `configuration` の中に置く。まずビューの ID と、4つのフィールドの ID を引く。

   ```bash
   gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{views(first:5){nodes{id name}} fields(first:30){nodes{... on ProjectV2FieldCommon{id name}}}}}}' -f p=<ボードID>
   ```

   ```bash
   gh api graphql -f query='mutation($v:ID!){updateProjectV2View(input:{viewId:$v,name:"Backlog",layout:TABLE_LAYOUT,filter:"-status:Done",configuration:{visibleFieldIds:["<Title の id>","<Status の id>","<Labels の id>","<Assignees の id>"]}}){projectV2View{name filter}}}' -f v=<ビューの ID>
   ```

6. API で設定できない Workflows と階層表示を、画面で案内する。ボードの URL は `https://github.com/users/<owner>/projects/<番号>`（組織なら `orgs`）。`AskUserQuestion` で済ませたかを聞く。

   - Workflows の「Auto-add to project」を有効にする（対象はこのリポジトリ）。新しいボードには無く、無いと Issue がボードに載らない
   - Workflows の「Pull request linked to issue」の移し先を `In Review` にする。有効にはなっているが、移し先は既定のままで、API では変えられず読めもしない
   - 表ビュー（`Backlog`）で、sub-issue の階層表示を有効にする。API で設定も確認もできない

   済んだと答えたら、Workflows が有効かだけ API で確かめる。移し先と階層表示は確かめられないので、答えを信じる。

   ```bash
   gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{workflows(first:20){nodes{name enabled}}}}}' -f p=<ボードID> --jq '.data.node.workflows.nodes[] | select(.name=="Auto-add to project" or .name=="Pull request linked to issue")'
   ```

   両方が `"enabled":true` で出れば済んでいる。作りたてのボードでは `{"enabled":true,"name":"Pull request linked to issue"}` の1行だけが出る。「Auto-add to project」の行が出ないか `"enabled":false` なら、済んでいない。

ステップ3〜5の API が失敗したら、エラーを見せ、人間の手作業として扱う。作りかけのボードを残すと、流し直しで2つ目のボードができるので、`gh project delete <番号> --owner <owner>` で消すよう案内する。消したと答えたら、ステップ3からやり直す。済まなければ、この節の残りと「`config.mjs` にボードを書く」を飛ばす。

### `config.mjs` にボードを書く

「ボードを作る」を飛ばしたか、そのステップ3〜5が失敗して済まなかったなら、これも飛ばす。

`scripts/auto-programmer/config.mjs` を書き換える。

- `repository`（ファイル先頭の定数）：origin の `owner/repo`
- `board.owner`：作ったボードの持ち主
- `board.number`：作ったボードの番号
- `board.statusFieldName`・`todoStatusName`・`readyStatusName`・`inProgressStatusName`：ボードの Status のフィールド名と、ステップ4で入れた「積まれただけ」「着手してよい」「着手した」の選択肢の表記。すでに同じなら触らない

書き換えたら、「ボードを作る」ステップ2の2本のコマンドを流して確かめる。`<owner> <番号>` が出て、Status が全部揃っていれば終わり。出なければ、`config.mjs` の書き換えを見直す。

### Claude の認証方式を決める

`pr-ai-triage.yml` は、シークレット `CLAUDE_CODE_OAUTH_TOKEN` で Claude を呼ぶ。無いと `pr-ai-triage` が落ち、PR が auto-merge されない。Bedrock のプロジェクトは、このトークンを使わない。

次のどちらかなら飛ばす。

- **`gh secret list` に `CLAUDE_CODE_OAUTH_TOKEN` がある**
- **Bedrock 切り替えの Issue が open である**

飛ばさないなら、`AskUserQuestion` で方式を聞く（選択肢は「Claude サブスクリプションの OAuth トークン」「Bedrock」。最初を既定にする）。

- **OAuth**：次を案内する。トークンの値は会話に貼らせない。人間が自分で登録する
  1. `claude setup-token` でトークンを発行する
  2. Settings → Secrets and variables → Actions で、シークレット `CLAUDE_CODE_OAUTH_TOKEN` に登録する

  済ませたかを `AskUserQuestion` で聞き、済んだなら `gh secret list` に名前があるかだけを確かめる。無い、または済ませていないなら、手作業の Issue（見出しは「Claude の認証方式を決める」）を起票して次へ進む

- **Bedrock**：その場では `pr-ai-triage.yml` を切り替えない。立ち上げ時は `infra/` が空で、GitHub Actions から AWS に入るための IAM ロールがまだ無いため。代わりに Bedrock 切り替えの Issue を `/quick-issue` で起票して次へ進む。Issue には次を書く
  - **タイトル**：Bedrock 切り替えの Issue の目印の語「pr-ai-triage を Bedrock 認証に切り替える」を含める
  - **理由**：`pr-ai-triage.yml` は `CLAUDE_CODE_OAUTH_TOKEN` で Claude を呼ぶ。Bedrock のプロジェクトはこのトークンを使わず、シークレットが無いと `pr-ai-triage` が落ちて PR が auto-merge されない
  - **対応方針**：`pr-ai-triage.yml` を Bedrock 認証に切り替える。`.github/` はテンプレート同期の対象外なので、書き換えても戻らない
  - **ブロッカー**：先に `infra/` で、GitHub Actions から AWS に入るための IAM ロールを作る

### project-context の3ファイルを書く

`docs/project-context/` の `project-claude.md`・`core-parts.md`・`issue-destinations.md` には、テンプレート本体の内容が入っている。残すと、AI が自分のプロジェクトをテンプレート本体だと思い込み、`/link-root-issue` はテンプレートのルート（構築・改善）を自分のプロジェクトに作る。3ファイルを書く機会は立ち上げのときしかないので、人間に聞いて、その場で書く。

3ファイルのどれにもテンプレート本体の説明が残っていなければ、済みとして飛ばす。テンプレート本体の説明とは、次をいう。書くときは、これらも消す。

- `project-claude.md` の「（テンプレート本体の記述。」で始まる段落
- `core-parts.md`・`issue-destinations.md` の注記にある「下の表はテンプレート本体のもの」の文
- `core-parts.md`・`issue-destinations.md` の、テンプレート本体の表の行

3ファイルごとに、`AskUserQuestion` で次を聞いて書く。

- **`project-claude.md`**：何を作るシステムか（一文）と、いまのフェーズ（立ち上げ段階など）。「このシステムは何か」と「現在のプロジェクトのフェーズ・状況」に書く
- **`issue-destinations.md`**：新規開発ガイドを使うか。使うなら、表の代わりに「issue-policy の標準のルートを使う」と書く。使わないなら、ルートと振り分け条件を聞いて表に書く
- **`core-parts.md`**：コア部分（壊れると全体が回らなくなる部分）が決まっていれば表に書く。まだなら表を空にする

答えられない項目は、空にして進む。Issue にはしない。「すべての手順に効く決まり」の「人間の手作業は、済まなければ Issue にして進む」は、この手順には当てない。質問への答えは人間の手作業ではなく、空でもハーネスは止まらないためである（`core-parts.md` には、空でも ADR の判定ができると書いてある）。

「立ち上げの Issue を起票する」は、この手順で書いた `issue-destinations.md` を前提にする（起票のとき `/link-root-issue` が読むため）。

`glossary.md` はこの手順で書かない。

### テンプレートの ADR を消す

テンプレートの ADR（`docs/adr/` の `NNN-*.md`）を消し、一覧を作り直す。残すと、テンプレートのハーネスについての ADR が、自分のプロジェクトの一覧に混ざり続ける（`docs/adr/` はテンプレート同期の対象外なので、一度消せば戻らない）。

次のどちらかなら飛ばす。

- **close 済みの立ち上げの Issue がある**：テンプレートの ADR は、その Issue の PR で消えている。いま `docs/adr/` にある ADR は、自分のプロジェクトが書いたものである
- **`docs/adr/` に `NNN-*.md` が無い**

飛ばさないなら、消すファイルを表示しながら消し、一覧を作り直す。`adr-template.md` と `adr-index.md` は消さない。

```bash
find docs/adr -maxdepth 1 -name '[0-9][0-9][0-9]-*.md' -print -delete && npm run gen:adr-index
```

### 立ち上げの Issue を起票する

立ち上げの Issue を探し、次で分ける。

- **open のものがある**：それを使う
- **open のものが無く、`/setup` の変更がある**：`/quick-issue` で起票する。ラベルとルート Issue への紐付けは `/quick-issue` の決まりに従う
- **open のものが無く、`/setup` の変更も無い**：リポジトリへ入れる変更が無い。この手順と「ブランチでコミットして push する」を飛ばす

起票する Issue には次を書く。

- **タイトル**：立ち上げの Issue の目印の語を含める
- **対応方針**：`/setup` の変更を、ブランチと PR でリポジトリへ入れる
- **タスク一覧**：`/setup` の変更の内容を1つずつ並べ、済んだものにチェックを入れる
- **ラベル**：`ai-fixable`。`/setup` の変更にテンプレートの ADR の削除があるなら、「不可逆・外部に出る」に当たるので `issue:decided` を重ね、人間の発言には「/setup」と書く
- **実装フロー（使用するSkill）**：該当なし（`/setup` が直接編集した）

### ブランチでコミットして push する

立ち上げの Issue の番号を `<番号>` とする。

1. 立ち上げのブランチ `chore/issue-<番号>` に移る。ローカルにあれば `git switch chore/issue-<番号>` で移る。無ければ、デフォルトブランチの最新から作る。デフォルトブランチ名は、origin を名指しして GitHub から引く（upstream など別の remote と取り違えない）。シェル変数は Bash ツールの呼び出しをまたいで残らないので、1回で実行する。

   ```bash
   base=$(gh repo view "$(git remote get-url origin)" --json defaultBranchRef --jq .defaultBranchRef.name) && git fetch origin "$base" && git switch -c chore/issue-<番号> --no-track "origin/$base"
   ```

   git が「Your local changes ... would be overwritten」で断ったら、人間の未コミットの変更と重なっている。メッセージを見せ、人間の手作業（コミットか stash で片付ける）として扱う。済まなければ、この手順の残りを飛ばす

2. `/setup` の変更だけを `git add <パス>` でステージし、`/git-commit stage` でコミットする。ワーキングツリー全体はステージしない（人間の作業中の変更を混ぜないため）。`/setup` の変更が無ければ（前回の `/setup` でコミット済みなど）飛ばす
3. push の前に、デフォルトブランチの最新を取り込む。`npm run gen:adr-index` で差分が出たら、`git add docs/adr/adr-index.md` して `/git-commit stage` でコミットする

   ```bash
   base=$(gh repo view "$(git remote get-url origin)" --json defaultBranchRef --jq .defaultBranchRef.name) && git fetch origin "$base" && git merge --no-edit "origin/$base" && npm run gen:adr-index
   ```

4. `git push -u origin HEAD` で push し、`/pr-body <番号>` を流す。`/pr-body` が「PR が現れない」で止まったら、PR を作る `pipeline.yml` の実行を引き、落ちたジョブのログを見る。

   ```bash
   gh run list --workflow pipeline.yml --branch chore/issue-<番号> --limit 1 --json databaseId,url --jq '.[] | "\(.databaseId) \(.url)"'
   gh run view <run ID> --log-failed
   ```

   - **`create-pull-request` ジョブが `GitHub Actions is not permitted to create or approve pull requests` で落ちた**：Actions に PR の作成が許されていない。人間の手作業として扱う（Settings → Actions → General の Workflow permissions で、Actions に PR の作成と承認を許す。組織所有なら組織の設定も）。確かめ直すときは、`./scripts/setup-repo-settings.sh` を流し、`gh run rerun <run ID> --failed` で落ちたジョブを流し直してから、`/pr-body <番号>` をもう一度流す
   - **ほかの原因**：エラーと実行の URL を報告に載せ、「次にやることを案内する」へ進む

### 次にやることを案内する

次を人間に伝える。

- 新規に立ち上げるなら、[新規開発ガイド](../../../docs/guide/new-development-guide.md) に従い、要件定義から始める
- 要件定義書（`docs/requirements.md`）と設計書（`docs/design/`）は、空から書く
- 実装は `app/`・`infra/` に書く。どちらも空なので、`samples/` の参照実装を手本にして写す（`samples/` 自体は書き換えない）

あわせて、手順ごとの結果（済ませた／済んでいたので飛ばした／Issue にした番号）を報告する。PR を作ったなら、その URL も添える。
