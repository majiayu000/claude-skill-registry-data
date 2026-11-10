---
name: continuous-delivery
description: GitHubで継続的デリバリーを実践するために、Actionsの設定、ワークフロー、アクション、ツールを整備するときに使う。PR・マージキューの検証、mainへのpush、デプロイとリリースの分離、バージョン計算の組み込み、検証済み成果物の再利用を設計・改善する。
---

# GitHubで継続的デリバリーを実践する

変更を継続的に検証し、検証済みの成果物を必要なタイミングでリリースできる状態にする。ワークフローとアクション、対応するGitHubの設定、実行に必要なツールを整える。

## デプロイとリリース

デプロイはビルド成果物を本番環境へ展開することで、機能の追加・変更・削除を必ずしも伴わない。mainへ統合したコミットごとに行い、全自動かボタン一つで任意の環境へ展開できるようにする。CLIでは、コミットごとのビルド成果物をGitHub ActionsのArtifactsに保存することをデプロイとする。

リリースはサービスの挙動を変えることで、機能の追加・変更・削除・修正を含む。デプロイを伴わず、フィーチャーフラグなどで公開を切り替えてもよい。バグ修正などは複雑な制御を増やさず、デプロイと同時にリリースしてもよい。CLIでは `release.yml` を起動し、正式バージョンを付けてGitHub Releaseを作成する。

## リリースバージョン

バージョン番号には[Semantic Versioning](https://semver.org/spec/v2.0.0.html)、コミットメッセージには[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)を強く推奨する。公開APIの互換性を基準に番号を更新し、変更の種類と破壊的変更をコミットへ記録する。

リリースでは採用した規則に従い、コミットログから次のバージョンを自動決定する。計算のタイミングと成果物への反映は[ワークフロー設計](references/workflow-design.md#リリースバージョン)に従う。

## 構成の基本

| レイヤー | 例 | 責務 |
| --- | --- | --- |
| ワークフロー | `pr.yml`、`push.yml`、`release.yml` | イベント、入力、ジョブの構成 |
| ジョブ | `screening`、`inspection`、`deployment`、`release` | ランナー、権限、依存関係、マトリクス、環境、実行条件、タイムアウト |
| アクション | `.github/actions/screening/action.yml` など | フェーズの共通処理と入出力 |
| ステップ | `build`、`lint`、`test` など | `run` によるコマンド実行、`uses` によるアクション呼び出し |

ジョブ内のステップからフェーズのComposite Actionを呼び、その内部に基本操作のステップを置く。ジョブは実行条件、アクションは処理内容を持つ。OS・権限・並列実行・承認条件が異なる処理はジョブを分ける。

## 基本ワークフローとフェーズ

| ワークフロー | トリガー | ジョブ |
| --- | --- | --- |
| `pr.yml` | `pull_request` | `screening` |
| `push.yml` | `push`、`branches: [main]` | `screening` → `inspection` → `deployment` |
| `release.yml` | `workflow_dispatch` | 成果物を使う場合は再利用判定 → `screening`・`inspection`（再利用時は省略）→ `release` |

- `screening`: lint、単体テスト、型検査、ビルドなど、プロジェクトに必要な基本検証と候補成果物の生成。
- `inspection`: 候補成果物に対する統合・受け入れ・動作確認。
- `deployment`: 検証済み成果物の展開・保存によるデプロイ。
- `release`: 機能の公開切り替えや正式版の公開によるリリース。
- `prlint`、`settings-pr`、`settings-apply`、`labeler`、`codex-review` などの補助ワークフローは目的と権限に応じて必要なものを用意する。

`push.yml` の検証済み成果物を `release.yml` で再利用する。配備済み機能の公開切り替えだけなら `release` を実行し、ビルドやデプロイをやり直さない。再利用できない場合の生成・検証と停止条件は[ワークフロー設計](references/workflow-design.md)に従う。手動でリリースを開始し、開始後の処理を自動化する。

## マージキューを使う構成

組織所有リポジトリの公開範囲・プランなどで利用可否を確認し、使える場合は次の構成を選べる。`pr.yml` は基本構成と共通とする。

| ワークフロー | トリガー | ジョブ |
| --- | --- | --- |
| `merge-queue.yml` | `merge_group`、`types: [checks_requested]`、`branches: [main]` | `screening` → `inspection` |
| `push.yml` | mainへの `push` | キューの検証結果・成果物を照合 → `deployment` |
| `release.yml` | `workflow_dispatch` | キューで検証した成果物を再利用 → `release` |

キューで両フェーズが成功し、mainに統合された内容と対応する成果物を確認できる場合、pushでは両フェーズを省略する。キュー不使用時は基本構成で検証する。キューとの対応、必須チェック、再利用できない場合の扱いは[ワークフロー設計](references/workflow-design.md)に従う。

## 再利用の単位

- 共通フェーズの処理は一つのComposite Actionにまとめる。各ワークフローには呼び出しを置く。
- 一つのコマンドだけの処理はステップに直接書く。ビルド、lint、テスト、パッケージングは別ステップにする。
- アクションの入力は必要な値に絞る。イベントの判別や多数のスキップフラグで処理を切り替えない。
- 複数ジョブの構成自体を共有する場合は `workflow_call` を使う。

## 設定と実装の詳細

- [ワークフロー設計](references/workflow-design.md): 入出力、実行環境、バージョン計算の組み込み、キュー検証、成果物の再利用、デプロイ・リリース条件、必須チェック。
- [安全性と設定](references/hardening.md): Actionsの実行許可、権限、配備先の環境、信頼境界、外部入力、依存先の固定。
- [効率化](references/efficiency.md): キャッシュ、並列化、マトリクス、同時実行、重複実行の抑制。
- [ツールと実行環境](references/tooling.md): 検査・更新・公開ツールの選定、バージョン固定、ランタイムとランナーの互換性。
