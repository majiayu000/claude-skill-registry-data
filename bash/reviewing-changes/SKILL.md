---
name: reviewing-changes
description: |-
  PR を作る前に、差分に応じて reviewer を起動してレビューを回し、指摘を台帳に記録して直す。処置は指摘の 4 項目（発生条件・頻度・影響・影響先）からスクリプトが決め、PR 作成の直前に 3 条件のゲートを通す。PR 番号を渡せば作成済みの PR にも使える。
when_to_use: |-
  実装を終えて PR を作る前（auto-implement の Phase 3・4）。「レビューして」「PR の前にレビューを回して」「PR #123 をレビューして」「マージ前チェック」と依頼されたとき。
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# PR 前レビュー

PR を作る**前に**、差分をレビューし、指摘を直してから PR を作る。考え方と、取り込まなかったものは
STDD 方法論の `packages/core/docs/review-process.md` を参照。

- `<skill-dir>` はこの skill のディレクトリ（Claude は `.claude/skills/reviewing-changes`、Codex は `.agents/skills/reviewing-changes`）。
- 台帳と担当の決定、処置の導出、ゲートは `<skill-dir>/scripts/review-ledger.sh` が受け持つ（`--help` で一覧）。
  台帳は作業ツリーの外に置かれ、コミットには入らない。
- **作成済みの PR をレビューするとき**は、PR のブランチの作業ツリーで同じ手順を使う（`gh pr checkout <番号>`）。
  直したら push し、`create-pr` §5 の工程テレメトリを投稿し直す。

## 1. 情報を 1 回だけ集める

担当ごとに集め直させず、メインのセッションが 1 回だけ集めて全担当に配る。

```bash
git fetch origin <primary_branch>    # .stdd.config.yml の project.primary_branch
git log --oneline origin/<primary_branch>...HEAD
git diff --stat origin/<primary_branch>...HEAD
bash .claude/hooks/trace-audit.sh --changed $(git diff --name-only origin/<primary_branch>...HEAD)
```

集めるもの: 変更したファイル、紐づく要件・設計の ID と Spec のパス、作業ツリーのパス。
書いたときの判断の理由は渡さない（書いた側と同じ見方でしか確かめられなくなる）。

## 2. ラウンドを始める

変更をすべてコミットしてから始める。レビューは、始めた時点のコミットに対して行う。

```bash
bash <skill-dir>/scripts/review-ledger.sh round start --independent <yes|no> [--skip <担当>=<理由>] [--add <担当>]
bash <create-pr>/scripts/pr-telemetry.sh mark review start   # create-pr skill のディレクトリ。工程の所要の記録
```

- 起動する担当は差分から決まる（条件は `.stdd.config.yml` の `review.triggers`）。起動しない担当と理由も台帳に残る。
  直前の工程で同じ文書を承認済みなら `--skip requirements=Phase 1a で承認済み` のように理由を付けて外す。
- 担当と agent の対応は `round start` の出力に出る。`code-reviewer` は 3 つの観点（規約と品質・性能とエラー処理・
  セキュリティ）に分けて起動する。セキュリティは `code-reviewer` のセキュリティの観点が受け持つ。
- **並列が既定**: 互いの結果を必要としないので、起動する担当はすべて同時に起動する。agent teams を使うか subagent にするかは
  `auto-implement` の `scripts/review-runner.sh` で決める（`skill-and-agent.md` §2）。名前は agent の名前で始める
  （例: `code-reviewer-security`）。
- **独立レビュー（推奨）**: 別のモデル（別のエージェントの CLI など）でレビューできる環境なら、少なくとも 1 担当を
  別のモデルで回し、`--independent yes` にする。できなければ同じモデルで回し、`--independent no` を記録する。

## 3. 依頼する

各担当に、1 の情報と、担当の観点 1 つと、報告の書式 [references/reporting.md](references/reporting.md) のパスを渡す。
ほかの観点は見ないよう伝える。

## 4. 報告を台帳に記録する

報告を受け取るたびに、報告をファイルに保存して末尾の ID の一覧を記録する。

```bash
bash <skill-dir>/scripts/review-ledger.sh report --role <担当> --file <報告のファイル>
```

指摘ごとに、**現物で裏を取ってから**台帳に載せる（`ファイル:行` が実在し、書かれた状態になっているか）。

- 確かめた段階を `--evidence`（`assessing-change-impact` §1 の確信の段階）に書いて載せる。
- **テストとコードの担当（`test` / `code-*` / `security`）の「直す」**: 確信の段階 4 以上（実行して確かめた）が要る。
  reviewer が自分の作業ツリーで実行した再現の手順を、メインのセッションがもう一度実行し、意図した出力と違う結果が出たら
  `--evidence 4` で載せる。作業ツリーを分けられなかった reviewer（Codex など）の手順は、メインのセッションが、レビューした
  コミットから作った使い捨ての作業ツリーで実行する（`git worktree add --detach <一時ディレクトリ> <コミット>`。終わったら
  `git worktree remove`）。確かめられなければ段階をそのまま書いて載せる。処置は「未確認」になり、終わりの条件に数えない。

```bash
bash <skill-dir>/scripts/review-ledger.sh add --id <ID> --role <担当> --trigger "<発生条件>" \
  --frequency <常時|条件付き|稀> --impact <致命|支障|軽微> --target "<影響先>" --evidence <1-5>
```

- 処置（直す・起票・見送り可）は `add` が表示する。reviewer は評価だけを書き、処置は決めない。
- 4 項目と確信の段階は、裏を取った結果に応じて `raise` で上げてよい（未確認の指摘を後で確かめたら `raise --evidence 4`）。
  **下げることはできない**（スクリプトが拒否する）。
- 複数の担当が同じ箇所を指摘したときも、それぞれの ID で載せる（修正のコミットは同じでよい）。

## 5. ラウンドを終えて直す

```bash
bash <skill-dir>/scripts/review-ledger.sh round end
bash <create-pr>/scripts/pr-telemetry.sh mark review end
```

直し方は [references/fixing.md](references/fixing.md)。要点:

- **ラウンドの途中で修正をコミットしない。** 報告がそろってから直す（違反は `round end` が警告する）。
- 処置が「直す」は直し、修正のコミットを `fixed --id <ID> --commit <SHA>` で対応づける。
- 処置が「起票」は issue にして `filed --id <ID> --issue <番号>`。プロダクトの不具合として起票し、
  `recording-dev-feedback`（プロセスの課題）とは分ける。
- 処置が「見送り可」は、直すか、`defer --id <ID> --reason <理由>` で見送る。
- 修正が局所的（1 つの論点で、ほかの振る舞いに及ばない）なら、回し直さずに 6 へ進んでよい。
  修正が複数の論点にまたがる、設計を変えた、新しいファイルを足した、のどれかなら、**修正の受け入れ検査**を
  してから 2 に戻る。ラウンドの数に上限は設けない。

## 6. ゲートを通して PR を作る

```bash
bash <skill-dir>/scripts/review-ledger.sh gate      # 3 条件。満たさなければ不合格の理由と対処を表示する
bash <skill-dir>/scripts/review-ledger.sh summary   # PR の備考に貼る
```

不合格なら、表示された対処に従ってから再実行する。合格したら `create-pr` で PR を作る。
フック `review-gate.sh` が `gh pr create` の直前に同じゲートを呼ぶ（強さは `workflow.enforce_review_gate`）。
テストと機械検査の結果はゲートの条件にしない（CI に任せる）。

## 緊急モード

緊急モードのブランチ（`choosing-work-mode`）では、ラウンドを省くか 1 回で打ち切ってよく、ゲートの不合格は警告にとどまる。
省いた範囲は PR 本文の「緊急モード」の節に書く。

## やらないこと

- reviewer に処置や重大度（Critical / Major / Minor）を書かせない。
- 処置の表を文書や依頼文に書き写さない（正本は `review-ledger.sh`。`review-ledger.sh table` で表示できる）。
- 未確認の指摘を「直す」として数えない。直すと決めたら、先に実行で確かめる。
