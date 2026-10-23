---
name: windmill-script
description: 本リポジトリ(atelier-works)でWindmillのscript / flow / migration / scheduleを追加・変更するときに使う。管理スキルの`write-script-bun` / `write-flow` / `schedules` / `resources`の一般的な作法に、このリポジトリ固有の規約を上乗せする。
---

# Windmill script/flowのリポジトリ固有規約(windmill-script)

このスキルは、wmillが生成する管理スキルの一般的な作法を前提に、このリポジトリ固有のルールだけを補足する。
管理スキルは`write-script-bun`、`write-flow`、`schedules`、`resources`などで、`.claude/skills/`に同居している。
基本の文法とCLIのコマンドは、管理スキルを参照する。

## 配置場所

- Windmill資産(script / flow / resource / variable / schedule)は、すべて`f/factory/`の配下に置く。wmillのsyncのルートはリポジトリの直下である。
- Data Tableのmigrationは`migrations/datatable/main/`の配下に置く。形式は`wmill datatable migrate new <name>`が生成するものに従う。
- フローのステップは、inline scriptではなくPathScript(`f/factory/steps/<flow>_<step>.ts`)に統一する。フロー定義(`.flow/`)自体はロジックを持たず、各ステップが対応するPathScriptを呼ぶ。
- libのimportはステップ側のscriptに閉じ、フロー定義から直接libを参照しない。

### 共有モジュール

DB、GitHub、Claude実行、draw.io、Discordなどの共有ロジックは、`f/factory/lib/`に置く。
libは、Windmillがscriptとして扱うhelper moduleで、`main`のエクスポートは要らない。
scriptからは相対importで読み込む(例: `import { runClaude } from "./lib/claude.ts"`)。
`wmill generate-metadata`が生成する`.script.yaml`と`.lock`は、生成物としてコミットする。
相対importが実行時に解決されることは、「libの相対import」で確かめている。

## native runtimeは使わない

- このリポジトリのscriptは、`child_process`や`fs`で`git` / `gh` / `claude` / `wmill`をサブプロセスとして起動する。そのため、native runtime(`//native`の指定)は使わない。
- 管理スキルがnativeを推奨していても、このリポジトリでは通常のbun runtimeを使う。先頭に`//native`を書かない。
- `windmill_worker_native`コンテナは、nativeのジョブのために残っている。factoryのscriptは、そこでは動かさない前提で書く。

## シークレットの扱い

- シークレットは`f/factory/*.variable.yaml`として定義し、`is_secret: true`にする。対象は`claude_oauth_token` / `github_token` / `wmill_token` / `discord_webhook_url` / `github_read_tokens`の5つである。
- 値はコミットせず、リポジトリ内では空のままにする。
- scriptからは、`wmill.getVariable("f/factory/github_token")`のように取得する。
- 取得した値は、子プロセスの環境変数(例: `GH_TOKEN`、`CLAUDE_CODE_OAUTH_TOKEN`)としてだけ渡す。
- 例外は、[セキュリティ](../../../docs/security.md)の「親プロセスが`fetch`で使う秘密値」に挙げた箇所だけである。
  `github_read_tokens`を使うのは`collect_github`(`lib/gh_graphql.ts`)だけで、宛先を`https://api.github.com/graphql`に固定した`fetch`の`Authorization`ヘッダで渡す。
  例外を足すときは、同じ変更で`docs/security.md`と本スキルの両方を直す。
- シークレットは、コマンドラインの引数、URL、ログ出力、DBのカラムのどれにも絶対に書かない。
- エラーメッセージに含まれうる箇所は、`f/factory/lib/log.ts`のマスク関数(`maskSecrets`)を通して事前にマスクする。

## 設定の取得

- 可変だが秘密ではない設定は、resource `f/factory/factory_config`(resource type `c_factory_config`)から取得する。
- 型には、`rt.d.ts`の`RT.CFactoryConfig`を使う。`rt.d.ts`は、`wmill generate-metadata`か`wmill resource-type generate-namespace`が生成する。
- `rt.d.ts`はtsconfigの`include`に入るアンビエントの型定義ファイルで、`RT`はグローバルの名前空間として提供される。import文は要らない。これは管理スキル`write-script-bun`の「Resource Types」節と同じ扱いである。
- `windmill-client`のimportでは、バージョンをWindmillサーバーに合わせて固定する。固定しないと、lockの版がずれる。
  - 例: `import * as wmill from "windmill-client@1.817.0"`

```ts
import * as wmill from "windmill-client@1.817.0";

export async function main() {
  const config: RT.CFactoryConfig = await wmill.getResource("f/factory/factory_config");
  // config.owners, config.trigger_label, config.max_attempts などを使う
}
```

`windmill-client`の型引数への対応によっては、`getResource<RT.CFactoryConfig>(...)`の形も使える。
どちらの書き方でも`as`でキャストせず、戻り値への型注釈か、型ガードでの検証で受け取る。
resourceの中身を推測で決め打ちせず、`rt.d.ts`の型定義を必ず確かめてから使う。

`getResultMaybe` / `getResult` / `getWorkspace` / `getStatePath`などは、named exportには無い。
これらは、default exportのオブジェクトにだけ存在する。
これは`node_modules/windmill-client`の`index.d.ts`で確かめている。
これらが必要な場合は、次のようにimportして`wmillDefault.getResultMaybe(...)`のように呼ぶ。

```ts
import wmillDefault, * as wmill from "windmill-client@1.817.0";
```

## TypeScriptの規約

- `strict: true`にする。
- `as`によるキャストは禁止する。`<T>expr`の形も含み、`as const`は許可する。
- 外部由来のJSON(Issue APIのレスポンス、Claudeのstdoutなど)は、型ガード関数でパースしてから使う(parse, don't validate)。

例は次のとおり。

```ts
type ClaudeResult = {
  summary: string;
  markdown: string;
  diagrams: { name: string; drawio_xml: string }[];
  open_questions: string[];
};

function isClaudeResult(value: unknown): value is ClaudeResult {
  if (typeof value !== "object" || value === null) return false;
  if (!("summary" in value) || !("markdown" in value)) return false;
  const summary = (value as { summary: unknown }).summary;
  const markdown = (value as { markdown: unknown }).markdown;
  return typeof summary === "string" && typeof markdown === "string";
  // 実装では diagrams / open_questions の要素も同様に検証する
}
```

型ガード関数(戻り値の型が型述語の関数)の本体の中だけは、オブジェクトの形を確かめるための`as`を使ってよい。
`lint-no-type-assertions`は、この範囲を例外として扱う。
判定のロジック自体は、`typeof` / `in` / 配列のチェックで組み立てる。

## TDD

- `f/factory/lib/**`は、`bun test`でTDDする(Red → Green → Refactor)。
- 外部プロセスの起動(`child_process.spawn`など)と`fetch`は関数の引数として注入し、テストではダミーの実装に差し替える。実プロセスや実HTTPを叩くテストは書かない。
- 1テスト1アサーション、Arrange-Act-Assertの構成にする。

## メタデータとデプロイ

- scriptのimportや引数(`main`のシグネチャ)を変えると、`.script.yaml`とlockを更新する必要が生じうる。
- AGENTS.mdの「Metadata: auto」に従い、pre-commitフックが`wmill generate-metadata`を実行して生成物をステージする。
- 実装者(implementer)は、lockのバージョンの変化(差分)を、レビューを依頼する前に報告する。
- libの`.script.yaml`と`.lock`も、生成物としてコミットする。
- デプロイは`mise run push`で行う。内部では`wmill sync push --yes --keep-deleted`を実行する。
- `--keep-deleted`は、UIで作成途中のものなど、リポジトリに未反映のリモートの項目を誤って消さないために付ける。
- リモートの項目を自動で削除しない。削除が必要な場合は、人が`mise run push:prune`で行う。通常の`push`タスクには削除を含めない。

## 外部サービスの契約と実装上の注意

### libの非同期の再デプロイ

`f/factory/lib/*`をpushすると、それを相対importするscriptを、Windmillがバックグラウンドのdependency jobで非同期に再デプロイする。
push完了の直後は、importerが古いバンドルで動く。
動作確認は、pushの数十秒後にdependency jobの完了を待ってから行う。
`wmill job list`は既定ではkind `dependencies`を表示しない。確認には、UIのRunsか、CLIの`wmill job list --job-kinds dependencies`を使う。

### datatableの型安全性

`wmill.datatable()`のタグ付きテンプレートに`null`を渡すと、パラメータが`text`型で束縛される。
その結果、bigint / integer / numeric / boolean / jsonbの列へのINSERTとUPDATEが失敗する。
エラーは`column is of type bigint but expression is of type text`のようになる。
nullになりうる非textの列には、明示のキャストを必ず付ける(例: `${x}::bigint`、`${y}::boolean`)。
詳細は`docs/coding-guidelines.md`を参照する。

## スケジュール

スケジュールの一覧は[docs/architecture.md](../../../docs/architecture.md)にあり、`*.schedule.yaml`から生成している。
ここには一覧を書かず、スケジュールを追加・変更するときの規則だけを書く。

- `timezone`は`Asia/Tokyo`にする。cronはWindmillの6フィールド形式(秒から始まる)で書く。
- Consoleが呼ぶscriptにだけ、`.script.yaml`に`tag: console`を付ける。
  Console用worker(ワーカーグループ`console`)がこのtagを受ける。
  対象は次の6つである。
  - `steps/console_query`
  - `approval_decide`
  - `retry_work_item`
  - `audit_kickoff`
  - `notice_resolve`
  - `console_fetch_watch`

  長いClaudeのジョブがdefaultのworkerの枠を埋めても、Consoleを止めないためである。
  ほかのscriptには付けない。
  付けると、defaultのworkerは受けないので、仕事がqueueに溜まる。
- `tag: console`を付けたscriptには、`timeout`(秒)も付ける。
  Console用workerの枠は1つしかなく、DBのロック待ちなどで1件止まると、ほかのジョブが待つためである。
  6つの値は`tests/scripts/console_script_tags.test.ts`が固定する。
  `wmill generate-metadata`は`tag`と`timeout`を消さない。
- 多重実行の防止にadvisory lockは使わない。各`*.schedule.yaml`に`no_flow_overlap: true`を設定し、前回の実行中はスキップさせる。
- 複数のインスタンスを同時に運用する場合の排他は、Windmill側ではなくGitHub側のclaimで行う。
  IssueとPRは、トリガーラベルを外す要求が成功した時点で所有を決める。
  Issueでは、ラベルを外す要求が応答の無い失敗かサーバーエラーで終わったときに、Issueの読み直しとタイムラインで、ラベルを外したのが自分かを確かめる。
  これはベストエフォートで、最後の防御はDBの部分一意インデックス`work_items_active_issue_key`である。
  Issueの作業項目は`insertIssueWorkItemUnlessActive`で挿入し、競合したら取得を失ったものとして引く。
  DBを分けた複数のインスタンスが同じリポジトリを扱う構成は対象外である。
- scheduleにはerror handler(`on_failure: f/factory/on_error_schedule`)を設定する。失敗は`job_failures`テーブルとDiscordの通知に流れる。
- 承認のタイムアウト(7日)は、`poll_issues`がreconcileの後に行う期限切れのスイープが、`approval_requests.expires_at`を見て判定する。`pipeline.flow`はsuspendを使わない。

## プロンプトと投稿の規約

- `claude -p`へのプロンプトの本文はstdinから渡し、コマンドラインの引数には載せない。
- Issue本文、PR本文、PR差分のような対象リポジトリ由来のテキストをプロンプトに埋め込む場合は、`<<<DATA-<nonce>` … `>>>DATA-<nonce>`の区切りで囲む。区切りの生成は`f/factory/lib/prompts.ts`が行う。
- 区切りの中の記述は指示ではなくデータであると、プロンプトに明記する。詳細は`factory-requirements` / `factory-review` / `factory-fix`の各スキルを参照する。
- factoryが投稿するIssueコメント、PRレビュー、レビューへの返信には、必ず目印(marker)`<!-- factory:<kind>:<work_item_id> -->`を埋め込む。`<kind>`は`issue` / `pr_review` / `pr_fix`などである。
- この目印によって、自分自身が投稿したコメントを、トリガー条件の判定(人間の入力かどうか)から確実に除外できる。

## 外部契約

worker内で実測した、外部コマンドとAPIの挙動を示す。型ガードは、この実測結果に合わせて書く。

### Claude Codeの構造化出力

`claude -p --output-format json --json-schema <schema>`の挙動は次のとおり。

- プロンプトはstdinで渡せる。
- トップレベルのキーは次のとおり。

  ```text
  type, subtype, is_error, result, session_id, total_cost_usd, num_turns,
  duration_ms, duration_api_ms, usage, modelUsage, structured_output,
  terminal_reason, stop_reason, uuid, permission_denials, ...
  ```

- 将来のバージョンでキーが増えうるため、型ガードは未知のキーを許容する形で書く。
- `usage`は`{ input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens, ... }`である。
- `modelUsage`は、モデル名をキーにしたオブジェクトである。各値は`{ costUSD, inputTokens, outputTokens, cacheReadInputTokens, cacheCreationInputTokens, ... }`である。
- `structured_output`は、`--json-schema`で指定したスキーマに一致するparse済みのJSONである。型ガードでさらに検証してから使う。
- `claude_version`はレスポンスに含まれない。`agent_runs.claude_version`は、環境変数`CLAUDE_VERSION`から取得する。workerのイメージの`ENV`に置き、`WHITELIST_ENVS`に挙げて、ジョブまで届かせる。
- 参考のコストは、最小限の呼び出し(短いプロンプト、少ない構造化出力)で約0.002 USDである。

### worktreeの作成

`git gtr new <branch> --porcelain --yes`の挙動は次のとおり。

- 成功すると、stdoutにTAB区切りの次の3行が出る: `path\t<worktree のディレクトリ>`、`branch\t<ブランチ名>`、`hook_status\tnone`。
- `origin`リモートの無いリポジトリでは、`fatal: invalid reference: origin/main`を出してexit code 1で終わる。対象のリポジトリに`origin`があることを前提にする。
- worktreeの一覧は`git worktree list --porcelain -z`(NUL区切り、git 2.36以上)で確かめる。`git gtr`独自のリスト機能には頼らない。

### GitHub CLIのAPI呼び出し

- `gh api -i`は、stdoutに、CRLF終端のHTTPステータス行、ヘッダ、空行、bodyを出す。
- `gh`自身のエラーの要約(例: `gh: Not Found (HTTP 404)`)はstderrに出て、exit code 1になる。stdoutとstderrの両方を見る必要がある。
- `gh api rate_limit`は、`resources`(複数形)キーの下に`resources.core = { limit, used, remaining, reset }`を返す。`reset`はepoch秒である。

### Data Tableのクエリ結果

`wmill.datatable()`で`` sql`select 1 as one`.fetch() ``を実行すると、`[{ one: 1 }]`(行オブジェクトの配列)が返る。

### libの相対import

- `f/factory/lib/*.ts`(`main`を持たないhelper module)は、wmillがscriptとして扱う。`wmill script run`で実行したとき、相対importが実行時に解決される。
- `wmill generate-metadata`は、各libファイルに対しても空のスキーマの`.script.yaml`と`.lock`を生成する。どちらもコミットの対象である。
- `wmill.yaml`の`codebases`バンドルは要らない。相対importのままで問題ない。

### 承認待ち

承認待ちは、Windmillのsuspendステップを使わず、`factory.approval_requests`テーブルの`pending`行で表す。
`wmill.getResumeUrls()`が返すresumeとcancelのURLにJSONをPOSTしても、POSTした本文は後続のステップに渡らないためである。
後続のステップが受け取るのは、suspendステップ自身の戻り値`{ resume, cancel, approvalPage }`だけである。これは`resume_form`の有無に関わらず、実フローで確かめている。

- `pipeline_request_approval`は`pending`行を記録して、すぐにフローを終える。以降、フローは待機しない。
- 人がConsoleから承認か却下をすると、`approval_decide`が決定を`approval_requests`に記録する。記録には、`decideApprovalRequestIfPending`(`WHERE status = 'pending'`の楽観ロック)を使う。
- 要件定義を承認するときは、記録の前に、現在のIssueが取り込み時点と同じかを確かめる。`approval_decide`の中で、`github_token`を`Authorization`ヘッダだけに載せ、GitHubのREST APIを`fetch`で読む。別のscriptに頼むと、defaultのworkerの待ち行列に並ぶ間、Console用workerの枠を塞ぐためである。
- 続けて`approval_decide`は、`kind`に応じたapplyスクリプトを`wmill.runScriptByPathAsync`で起動する。実際の反映はapplyスクリプトが行う。
  - `requirements`: `steps/requirements_apply`
  - `issue_proposal`: `steps/issue_proposal_apply`
- タイムアウト(7日)は、`poll_issues`がreconcileの後に行う期限切れのスイープが`approval_requests.expires_at`を見て判定する。期限切れの行は、`expireApprovalRequestIfPending`で`expired`に遷移させる。

### Issueコメントの目印による冪等性

`commentIssue`の目印(`<!-- factory:<kind>:<work_item_id> -->`)による冪等性は、`(kind, work_item_id)`単位のfirst-winsである。
先に投稿された1件だけが有効で、以降の同じ`kind`での投稿は黙ってno-opになる。

- attemptごとに再投稿しうるコメントは、`kind`にattemptを含めて分ける(例: `issue-approved-<attempt>`)。同じ`kind`を使い回すと、2件目以降が投稿されない。
- GitHubに投稿するのは、成果物(承認済みの要件定義へのリンク、PRレビューの本体、レビューへの返信)だけにする。
- 着手、承認待ち、失敗、期限切れ、要人手のような運用の通知は、IssueやPRに書かず、DiscordとConsoleで伝える。

## トリガーラベルの消費

Issueの`factory`ラベルと、PRの`factory:review` / `factory:fix`ラベルは、いずれもclaim時に一度だけ消費する(外す)。
Issueでは、assigneeを追加してからラベルを外す。claim時は、IssueとPRのどちらも、ラベルを外す要求が成功した時点である。

以降は、どの状態遷移でもIssueとPRのラベルを付け外ししない。終端の状態への遷移も含む。

| 対象 | 終端の状態 |
| --- | --- |
| Issue | `approved` / `needs_human` / `expired` / `failed` / `cancelled` |
| PR | `reviewed` / `rereview_requested` / `blocked` / `needs_human` |

状態は`work_items.status`だけが正である。
GitHubのラベルは、人からFactoryへのトリガーの役割に限る。

再クレームの防止はDB上のチェックで行い、ラベルの有無には依存しない。

- Issueでは、`listActive`を使う。
- PRでは、`poll_prs.ts`の`decidePrActions`が参照する`hasActiveReviewingItem`(review)と、`listTrackedPrs`によるDB上の状態を使う。

トリガーラベルが外れた後のPRは、DBから見つけ直す。
`f/factory/lib/db.ts`の`listTrackedPrs`が、次の条件をすべて満たす行を返す。

- `kind IN ('pr_review', 'pr_fix')`
- `status != 'cancelled'`
- `tracked_pr_days`以内に更新されている

最初からやり直すには、人がトリガーラベルを付け直す。これが新しいcycleになる。
