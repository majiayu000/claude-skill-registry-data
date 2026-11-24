---
name: create-pr
description: |-
  現在のブランチから主ブランチ（`.stdd.config.yml` の `project.primary_branch`）への Pull Request を作成する。差分情報の収集→変更内容の分析→PR description の自動生成→`gh pr create` 実行までを一括で行う。
when_to_use: |-
  「PR作成」「プルリクエスト」「pull request」「PR出して」「create PR」「マージリクエスト」など、ブランチを主ブランチにマージするための PR 作成依頼があったとき。
allowed-tools: Bash, Read, Grep
---

# Pull Request 作成

現在のブランチから主ブランチ（`.stdd.config.yml` の `project.primary_branch`）へのPRを作成する。差分を分析し、適切なtitle/descriptionを自動生成する。

以降のコマンド例では `<primary_branch>` を `.stdd.config.yml` の `project.primary_branch` の値に置き換えて実行する。

## 1. 差分情報の収集

```bash
# <primary_branch> は .stdd.config.yml の project.primary_branch
git fetch origin <primary_branch>
```

以下を並列で実行:

```bash
git log --oneline origin/<primary_branch>...HEAD
git diff origin/<primary_branch>...HEAD --name-only
git diff origin/<primary_branch>...HEAD --stat
git branch --show-current
```

必要に応じて変更内容の詳細も確認:

```bash
git diff origin/<primary_branch>...HEAD
```

## 2. 変更内容の分析

1. **変更の種類を特定**: feat / fix / refactor / docs / test / style / perf / chore
2. **影響範囲を特定**: `.stdd.config.yml` の各 `apps[].id` / supabase / e2e / docs（apps[] を読み、変更があったアプリを列挙する）
3. **主要な変更点を抽出**: 新規ファイル、削除ファイル、大幅変更ファイル

## 3. Issue情報の確認

引数やコミットメッセージからissue番号（`#123`形式）を検出した場合:

- PR descriptionの末尾に `Closes #123` を追記してissueを自動クローズする
- 複数ある場合は `Closes #123, Closes #456` のように列挙する
- **`Closes` を付けるのは、この PR が実際に解決・反映する issue だけ**。`recording-dev-feedback` がこの作業中に起票した issue（備考に並べる番号）には付けない（この PR では反映されないので、マージで閉じてはいけない）

## 4. PRの作成

`gh pr create` を使ってPRを作成する。**作る前に、PR 前レビューのゲートを通す**（`reviewing-changes` skill §6）。

```bash
# <reviewing-changes> は reviewing-changes skill のディレクトリ
bash <reviewing-changes>/scripts/review-ledger.sh gate
```

- 不合格なら、表示された対処（台帳の更新か、レビューのラウンド）を済ませてから作る。フック `review-gate.sh` も
  `gh pr create` の直前に同じゲートを呼ぶ（強さは `.stdd.config.yml` の `workflow.enforce_review_gate`）。
- レビューの要らない PR（誤字の修正だけなど）は、`STDD_REVIEW_GATE_SKIP_REASON="<理由>"` を `gh pr create` の前に置く。
  §5 では同じ理由の区分を `--exempt` で申告する。
- 合格したら、`review-ledger.sh summary` の出力を備考に貼る。

### タイトル

- 70文字以内
- 変更の種類をprefixに付ける（例: `feat: ユーザー一覧のフィルター機能を追加`）

### Description テンプレート

緊急モードのブランチ（`choosing-work-mode` で宣言したもの。`work-mode.sh status` で確かめられる）では、本文の**冒頭**に
「## 緊急モード」の節を置く。§5 の `pr-telemetry.sh` がこの見出しを確かめる。通常モードでは節ごと削除する。

```markdown
## 緊急モード

- 理由: [work-mode.sh status に出る宣言の理由]
- 省いた工程: [例: コードレビュー、Spec の reviewer、Red の確認]
- 不合格のまま残した検査: [例: commands.test の失敗 2 件、トレーサビリティ監査の抜け漏れ。無ければ「なし」]
- 後追いが要るもの: [未レビューの範囲、不合格の解消、Figma の更新など]

## 概要

[変更の目的・背景を1-2文で説明]

## 変更内容

- [変更点1]
- [変更点2]
- [変更点3]

## 影響範囲

- [ ] <apps[].id>   <!-- .stdd.config.yml の apps[] を読み、apps[] の数だけ列挙する -->
- [ ] supabase
- [ ] e2e
- [ ] docs

## 確認手順

1. [確認手順1]
2. [確認手順2]

## 備考

[レビュアーへの補足事項があれば記載]
[recording-dev-feedback の triage が出力した「開発フィードバック: …」の 1 行（棚卸しをした場合）]
[PR 前レビューの review-ledger.sh summary の出力（レビューをした場合）]
[どちらもなければセクションごと削除]

Closes #[issue番号]
```

### 作成コマンド

bodyは一時ファイル経由で渡す（ヒアドキュメントは避ける）:

```bash
# <primary_branch> は .stdd.config.yml の project.primary_branch
gh pr create --base <primary_branch> --title "タイトル" --body-file /tmp/pr-body.md
```

## 5. 工程テレメトリを投稿する

**PR を作成した直後に、工程テレメトリを PR コメントとして投稿する。** レビューを省いた PR でも投稿する
（投稿されない PR が偏ると、集計の結論が歪む）。`.stdd.config.yml` の `telemetry.enabled` が `false` なら省く。
仕組みと項目の意味は `packages/core/docs/feedback-loop.md` を参照。

同梱の `scripts/pr-telemetry.sh`（この skill のディレクトリからの相対パス）を使う。手で書かない。

```bash
# レビューを通した PR（工程の記録 mark review start/end があれば回数は自動で数える）
bash <skill_dir>/scripts/pr-telemetry.sh post

# 記録は無いが、レビューを N 回行った PR
bash <skill_dir>/scripts/pr-telemetry.sh post --review-rounds <N>

# レビューをしなかった PR は理由の区分を申告する
#   typo_format_only / link_fix_only / regenerate_only / user_waived
bash <skill_dir>/scripts/pr-telemetry.sh post --exempt <区分>

# 緊急モードのブランチは、レビューをしたかどうかに関わらずこの区分で投稿する（回数はそのまま記録される）
bash <skill_dir>/scripts/pr-telemetry.sh post --exempt emergency
```

- 緊急モードのブランチで `--exempt emergency` を付けないと `post` は止まる。宣言していないブランチでは使えない。
  `--exempt emergency` のときは、PR 本文に「## 緊急モード」の節が無いと止まる。

- `post` は投稿のあとに PR を読み直し、head の SHA と一致する記録が載っているかを確かめる（`verify`）。
  **ここで失敗したら PR 作成は完了していない**。原因（未 push、投稿の失敗）を直してから再実行する。
- レビューの記録も免除の申告も無いと `post` は止まる。どちらかを明示する。
- PR 前レビューの台帳（`reviewing-changes`）があれば、ラウンド数・指摘の処置の内訳・独立性・実行で確かめられなかった指摘の件数も
  自動で記録に入る。
- フィードバックの棚卸し（`recording-dev-feedback`）の記録が無いと警告が出る。棚卸しをしていなければ、ここで行ってから投稿し直す。
- PR を作ったあとにコミットを積んだり、追加のレビューをしたりしたら、もう一度 `post` する（追記のみ。前のコメントは消さない）。
- 免除の出典（誰の指示か）はコメントに入れない。必要なら PR の本文に書く。

## 6. 完了

作成したPRのURLを表示する。

## 注意事項

- 「何が変わったか」「なぜ変わったか」を日本語で端的に記述する
- 技術的な詳細より変更の目的を重視する
- 影響範囲のチェックボックスは該当するもののみチェックを入れる
- 確認手順には実際にレビュアーが確認すべき操作を具体的に記載する
- 機密情報（APIキー、パスワードなど）が含まれていないか確認する
- リモートにpushされていない場合は先にpushする
