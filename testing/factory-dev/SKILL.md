---
name: factory-dev
description: 本リポジトリ(atelier-works)の開発環境をセットアップし、miseタスクで起動・検証・デプロイするときに使う。実装・レビュー・修正のループを回す際にも参照する。
---

# このリポジトリの開発手順(factory-dev)

このリポジトリで開発するときの手順を定める。環境の作り方、変更の進め方、E2Eでの確かめ方を書く。

## 環境を作る

手順は[セットアップ](../../../docs/setup.md)にある。資格情報の取得手順は[セキュリティ](../../../docs/security.md)にある。miseタスクの一覧は[README](../../../README.md)にある。

- ホストに要るのはDockerとmiseだけである。ほかのツールは`mise run setup`で入る。
- 秘密値は人が投入する。Claudeは`mise.local.toml.example`の更新までを行う。値が要るときは、[セットアップ](../../../docs/setup.md)の「秘密値を投入する」のコマンドを示し、止まらずに先へ進む。
- `docker compose`は`.env`を読まない。`mise run`を通して実行する。

## 実装、レビュー、修正のループ

このリポジトリの変更は、計画の確定、実装、レビュー、修正、再レビューのループで進める。

1. 対象のファイルと受入条件を決めてから実装を始める。
2. TDD(Red、Green、Refactor)で実装する。対象の外のファイルには触れない。
3. `mise run check`が通ることを、実装の完了の条件にする。
4. レビューと修正は、[review-loopスキル](../review-loop/SKILL.md)の手順で回す。人数、ラウンドの上限、設計レビューの要否は、変更の種類で決まる。

## コミットとPR

- コミットメッセージは`<type>: <日本語の説明>`の形にする(例: `feat: Issueを拾うpoll_issuesのスケジュールを追加`)。typeの一覧は[コーディング規約](../../../docs/coding-guidelines.md)にある。
- コードの変更に伴う文書とスキルの更新は、同じコミットに含める。
- PRの本文は`.github/PULL_REQUEST_TEMPLATE.md`の章立てに従う。Windmillへの反映(マージ後に`self_update`が反映するか、次の`mise run up`で反映されるか)を必ず書く。

## E2Eで確かめる

`mise run doctor`、`mise run up`、`mise run bootstrap`の後で、次を確かめる。PRの修正のE2Eは、本番のIssueやブランチではなく、捨てブランチと捨てPRで行う。

1. sandboxのリポジトリで、Issueのテンプレートを使ってIssueを作り、`factory`ラベルを付ける。
2. `poll_issues`の周期である5分以内に、Discordに通知が届き、Consoleの**要対応**に表示されることを確かめる。
3. 理由を付けて一度差し戻し、要件定義が作り直されて、もう一度通知が来ることを確かめる。
4. 承認し、IssueにConsoleへのリンクを含むコメントが1件だけ投稿されることを確かめる。要件定義の本文や図は転記されない。ラベルは起動のためだけに使うので、承認してもIssueのラベルは変わらない。
5. Consoleの**レポート**の分析に、コストとトークン数が出ることを確かめる。
6. 何かの変更をself cloneに反映させ、`self_update`のスケジュールが最新のSHAを取り込むことを確かめる。

## 実装フローをE2Eで確かめる

上の1から4の後で、sandboxで実装フローを確かめる。sandboxには、`factory_config`の`repo_allowlist`にあるsandboxのリポジトリを使う。`f/factory/factory_config`はgitで管理しないので、Windmillの画面で編集する。

1. `check_commands_by_repo`に、sandboxの検査コマンドを設定する。

   ```json
   {"<owner>/<repo>": ["bun install --frozen-lockfile", "bun test"]}
   ```

2. `implement_enabled`をtrueにする。
3. Issueを起票し、要件定義を作らせ、Consoleで承認する。
4. 実装フローが走ることを確かめる。Consoleの**作業項目**の表で状態が`implementing`になり、ブランチの列にブランチが出る。
5. PRができると状態が`pr_open`になり、PRの列にPRが出て、Discordに`pr_opened`の通知が届くことを確かめる。
6. PR本文の章立て(受入条件、動作確認結果、確認して欲しい点、`Closes #N`)を確かめる。
7. `poll_prs`がPRを拾い、`pr_review`が自動で走ることを確かめる。実装フローの`implement_finish`が`factory:review`のラベルを付けているので、ラベルを付け直さなくてよい。
8. 下の表の項目を確かめる。
9. PRを閉じ、ブランチを消し、`implement_enabled`をfalseに戻す。本番での有効化は、E2Eの結果を確かめてから別に行う。

検査コマンドについては、次の点に注意する。

- 検査の前に`git clean -fdX`が`node_modules/`などを消す。依存関係のあるリポジトリでは、先頭のコマンドでインストールする。`package.json`が無いリポジトリなら`bun test`だけでよい。
- 検査コマンドは、Claudeが書いたコードを非特権のユーザーで、コンテナの分離なしに実行する。Issueを信頼できる人だけが起票するリポジトリにだけ設定する。

`implement_enabled`については、次の点に注意する。

- falseのままだと、承認した作業項目は`approved`で止まる。`retry_work_item`での再実行も、falseなら拒否する。
- インスタンス全体の設定なので、trueの間は`repo_allowlist`のほかのリポジトリと`factory_repo`でも、承認すると実装フローが走る。pushとPRの作成、対象リポジトリのCIまで進むので、E2Eの間はsandbox以外を承認しない。

| 確かめること | 期待する結果 |
| --- | --- |
| 検査コマンド | ラウンドごとに実行され、`implement_rounds`に記録される |
| コスト | `agent_runs`にコストが記録される |
| `--restricted`の書き込み制限 | Claudeが`.git`、`.gitattributes`、`.gitleaksignore`、元の要件定義のディレクトリに書けない |
| Workflowsの権限 | PATにWorkflowsの権限が無く、`.github/workflows/`を含む変更のpushが拒否され、人の対応待ちの理由に載る |

`--restricted`の制限を破って書けた場合は、`--restricted`の欠陥として扱い、止めて報告する。書けたときの結果は、書いた先によって次のように違う。

- `.git`に書けたら、作業項目は人の対応待ち(`needs_human`)になる。
- `.gitattributes`と`.gitleaksignore`は保護パスなので、そのラウンドは検査を飛ばしてPRを作り、PR本文の保護パスの節に載るだけで止まらない。`.gitleaksignore`はgitleaksも読まない。
- 要件定義は、Claudeには書き込めるコピーを渡す。確かめるのは、元の要件定義のディレクトリのファイルが変わっていないことである。

Workflowsの権限は足さない。実装フローは`.github/`の変更を止めずに記録するので、pushの拒否が実質のガードになる。
