---
name: auto-implement
description: |-
  実装したい課題（GitHub issue / 自由記述の要望 / 既存ドキュメント / URL 等、あらゆる入力）を起点として、まずユーザーへのヒアリングで対象を確定し、Spec 作成（要件→技術設計）→PLAN 作成→実装（STDD）→QA→コードレビュー→Figma 更新→PR 作成までを、メインのセッションが skill を順に使って進める。レビューと QA は独立した reviewer の subagent に任せる。
when_to_use: |-
  「auto implement」「自動実装」「これを実装して」「PR まで作って」「issue から実装」「#123 を実装して」など、課題・要望（issue に限らず自由記述やドキュメントでも可）を起点とした包括的な自動実装の依頼があったとき。入力が曖昧でも、最初のヒアリングで対象を具体化してから進める。
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# 自動実装オーケストレーション

実装したい課題（GitHub issue / 自由記述の要望 / 既存ドキュメント / Slack・Notion などの参照 / URL）を受け取り、ヒアリングで対象を確定したうえで、Spec作成→実装→QA→コードレビュー→PR作成までを自動で実行するオーケストレーションスキル。

**入力は GitHub issue に限らない。** issue 番号があればそれを使うが、無くてもよい。入力が無い / 曖昧な場合は **Step 1 のヒアリング**で対象を具体化してから進める。

## 引数

**形式**: `[<入力>] [--mode <full|spec-only|impl-only|quick>]`

- `<入力>`（任意）: `#<issue番号>` / issue URL / 自由記述のタスク説明 / ドキュメントのパス・URL のいずれでも可。省略可能。
- `--mode`（任意）: 実行モード。

## Step 1: 入力のヒアリングと確定

auto-implement の対象（実装したい issue / 課題 / 要望）を確定するフェーズ。**いきなり実装に進まず、まずここで対象を明確にする。**

1. **初期入力の取り込み**: 引数で入力が与えられていれば、その種別を判定する。
   - `#<番号>` または issue URL → **GitHub issue**（Step 2 で `gh` 取得）
   - 自由記述のテキスト → **タスク記述**としてそのまま扱う
   - ファイルパス / ドキュメント URL → 読み込んで**タスク記述**の素材にする
2. **ヒアリング**: 入力が無い、または上記だけでは auto-implement を始めるのに不十分な場合は、ユーザーに以下を確認する（`AskUserQuestion` 等で簡潔に）:
   - **何を実装したいか**（目的・背景・解決したい課題）
   - **入力ソース**（GitHub issue / 自由記述 / 既存ドキュメント / その他）— issue なら番号を聞く
   - **スコープ・制約**（対象アプリ / 機能、含める・含めないもの、既知の制約）
3. **確定**: 課題内容が「Spec 作成に着手できる程度」に具体化できたら、要点をユーザーに復唱して確認を取る。曖昧なまま先に進まない。

このヒアリングの結果（タスクのタイトル相当・本文相当・スコープ）を、以降のフェーズの**入力（タスク記述）**として扱う。

## Step 2: 入力情報の取得・正規化

Step 1 で確定した入力を、以降のフェーズが扱える**タスク記述**（タイトル相当・本文相当・補足）に正規化する。

- **GitHub issue の場合**: GitHub MCP tools または `gh issue view` で取得する。
  - タイトル / 本文（description） / ラベル / コメント
- **issue 以外の場合**（自由記述・ドキュメント等）: ヒアリング結果や参照ドキュメントから、タイトル相当・本文相当・スコープを構成する。ラベルは無いものとして扱う。

以降のステップで「issue」と記載がある箇所は、issue 以外の入力ではこの正規化済みタスク記述に読み替える。

## Step 3: 実行モード判定

`--mode` が指定されている場合はそのモードを使用。未指定の場合は以下のロジックで自動判定する（issue 以外の入力では「ラベル」条件は対象外。タイトル・本文の内容で判定する）:

| 条件                                                                                        | モード      |
| ------------------------------------------------------------------------------------------- | ----------- |
| （issue の場合）ラベルに `bug` を含む / 不具合の修正が主目的                                 | `impl-only` |
| ラベルに `documentation` を含む、またはタイトルに「Spec」「リバースエンジニアリング」を含む | `spec-only` |
| タイトルに「typo」「修正」を含む、または本文が短い（200文字以下）                           | `quick`     |
| 上記いずれにも該当しない                                                                    | `full`      |

作成済みの機能の改修なら、Spec の更新は `revising-specs` で行い、直し終えてから `impl-only` で進める。

判定結果を表示し、**`--mode` が未指定の場合はユーザーに確認を求める**:

```
実行モード: <mode>（自動判定理由: <reason>）

このモードで実行してよろしいですか？（y/n、または別のモードを指定: full / spec-only / impl-only / quick）
```

承認されるまで次のステップに進まないこと。

### 作業モード（通常 / 緊急）

実行モードとは別に、作業モードがある。**既定は通常モード**で、以下のフェーズをそのまま通す。

- 依頼文に「緊急モード」と明示されているとき（または `/choosing-work-mode` で選ばれたとき）だけ、`choosing-work-mode` skill に
  従って Step 4 のブランチ作成のあとで緊急モードを宣言する。**自分の判断で緊急モードに切り替えない。**
  「急ぎで」など速度の表現だけなら、作業モードを 1 問だけユーザーに確かめる。
- 緊急モードのブランチでは、どのフェーズを必須にしないかを `choosing-work-mode` §3 の表に従って決める
  （Spec → テスト → 実装の順序と、人間レビューゲートは省かない）。省いたフェーズは完了報告で `SKIP（緊急モード）` と書く。

## Step 4: ブランチ作成・Worktree準備

`.stdd.config.yml` の `project.primary_branch` を統合先ブランチとして読み取る。

```bash
# <primary_branch> は .stdd.config.yml の project.primary_branch
git fetch origin <primary_branch>
```

タスク記述のタイトル（issue タイトル、または Step 1 で確定したサマリ）からブランチ名を生成（`<branch_prefix><kebab-case-summary>`。`branch_prefix` は `.stdd.config.yml` の `workflow.branch_prefix`、既定 `claude/`）。
Worktree作成スクリプトを実行:

```bash
./scripts/create-worktree.sh -b claude/<branch-name> -i <instance-id>
```

devcontainerを起動:

```bash
devcontainer up --workspace-folder ../worktree-<instance-id> --override-config ../worktree-<instance-id>/.devcontainer/devcontainer.override.json
```

以降の作業はすべてworktree内のdevcontainerで実行する。

作業ツリーで作業するときは、subagent を起動する前に、作業する作業ツリーを宣言する。宣言すると、
フック `worktree-lock-guard.sh` が subagent の書き込み先と実行先を宣言と突き合わせる（宣言しなければ確かめない）。

```bash
# <skill-dir> はこの skill のディレクトリ（Claude は .claude/skills/auto-implement、Codex は .agents/skills/auto-implement）
bash <skill-dir>/scripts/worktree-lock.sh lock --root <作業ツリーの絶対パス>
```

subagent に一時ディレクトリを使わせるときは `--allow <ディレクトリ>` を足す。作業を終えたら `unlock` で外す。

## Step 5: フェーズ実行

Spec の作成・実装・修正は、このスキルを使っているメインのセッションが行う。会話の経緯を踏まえて順に進める作業なので、
subagent には分けない。subagent に任せるのは、書いた経緯を見ていない目でのレビューと、長い出力の隔離だけである
（基準は STDD 方法論の `packages/core/docs/skill-and-agent.md`）。

| 担当 | 使うもの | 対象の Phase |
| --- | --- | --- |
| メインのセッション | `documenting-requirements`・`generating-wireframes` | 1a 要件 |
| メインのセッション | `documenting-tech-specs` | 1b 技術設計 |
| メインのセッション | `documenting-plans` | 1.5 PLAN |
| メインのセッション | [references/implementation.md](references/implementation.md) | 2 テスト・実装 |
| 別の文脈（並列） | `requirements-reviewer` / `tech-specs-reviewer` | 1a / 1b のレビュー |
| 別の文脈（並列） | `test-reviewer` | 2.5 テストレビュー |
| メインのセッション + 別の文脈（並列） | `reviewing-changes`（`qa-engineer`・`code-reviewer`・差分に応じた reviewer） | 3・4 PR 前レビュー |
| メインのセッション | Figma の更新・`recording-dev-feedback`・`create-pr` | 4.5・4.8・5 |

- reviewer には、対象のファイルと基準の Spec のパスを渡し、書いたときの判断の理由は渡さない。
- 互いの結果を必要としないレビュー（QA とコードレビューの観点ごと、文書ごと）は、既定で同時に起動する。agent teams が使えれば既定でそれを使う（phases.md「起動の仕方」）。
- **人間レビューゲートを尊重する**: Phase 1a（要件）と Phase 1b（技術設計）は、reviewer のレビューで「直す」の指摘が 0 件になった後に**ユーザーの確認**を求めて止まる（詳細は phases.md）。
- 長い会話になるので、進捗は PLAN とコミットに残す。会話が圧縮されても、ファイルから続きを再開できるようにする。

各フェーズの詳細な手順は [references/phases.md](references/phases.md) を参照。
各 Phase の開始と終了では工程の記録（`pr-telemetry.sh mark`）を付ける（phases.md「工程の記録」）。
モードに応じて以下のフェーズを順次実行する:

| Phase      | 名称                          | full | spec-only | impl-only | quick |
| ---------- | ----------------------------- | ---- | --------- | --------- | ----- |
| Phase 1a   | 要件作成 → 人間レビューゲート①  | ✓    | ✓         |           |       |
| Phase 1b   | 技術設計作成 → 人間レビューゲート② | ✓    | ✓         |           |       |
| Phase 1.5  | PLAN作成                      | ✓    |           | ✓         |       |
| Phase 2   | 実装                   | ✓    |           | ✓         | ✓     |
| Phase 2.5 | テストレビュー         | ✓    |           | ✓         |       |
| Phase 3–4 | PR 前レビュー（QA・コードレビュー） | ✓    |           | ✓         |       |
| Phase 4.5 | Figma更新              | ✓    |           | ✓         |       |
| Phase 4.8 | フィードバックの棚卸し | ✓    | ✓         | ✓         | ✓     |
| Phase 5   | PR作成                 | ✓    | ✓         | ✓         | ✓     |

## Step 6: 完了報告

以下の形式で結果を報告:

```
## 実行完了

- **対象**: <GitHub issue なら `#<issue番号> <タイトル>`、それ以外はタスクのサマリ>
- **モード**: <mode>（作業モード: 通常 / 緊急）
- **ブランチ**: <branch-name>
- **PR**: <PR URL>

### フェーズ実行結果
| フェーズ | 状態 | 備考 |
|---------|------|------|
| 要件作成（REQUIREMENTS） | OK / SKIP | |
| 要件レビュー | OK / SKIP | |
| 人間レビューゲート①（要件） | OK / SKIP | |
| 技術設計作成（TECH_DESIGN+TEST_PLAN） | OK / SKIP | |
| 技術設計レビュー | OK / SKIP | |
| 人間レビューゲート②（技術設計） | OK / SKIP | |
| PLAN作成 | OK / SKIP | |
| テスト作成 | OK / SKIP | |
| テストレビュー | OK / SKIP | |
| 実装 | OK / SKIP | |
| PR 前レビュー | OK / SKIP | ラウンド数・指摘の処置の内訳（`review-ledger.sh summary`） |
| Figma更新 | OK / SKIP | |
| レビューの実行 | agent teams / subagent | |
| フィードバックの棚卸し | OK / SKIP | 起票・再発・上限で起票しなかった件数 |
| PR作成 | OK | |
| 工程テレメトリ | OK / SKIP | |
```

## エラーハンドリング

- Spec とテストの各フェーズ（1a / 1b / 2.5）で3回の修正ループを超えた場合、そのフェーズで停止し、現状をコミット・pushしてdraft PRを作成する（PR 前レビューのゲートは通らないので、`STDD_REVIEW_GATE_SKIP_REASON` に理由を前置して作る）
- PR descriptionに未解決の問題を記載し、手動対応を依頼する
- PR 前レビュー（Phase 3–4）のラウンドには上限を設けない。同じ論点の指摘が繰り返すときはユーザーに判断を仰ぐ（`reviewing-changes` の `references/fixing.md`）

## 注意事項

- 書く作業は agent teams を使わず、メインのセッションで順に進める（基準は `skill-and-agent.md` §2）
- reviewer は対象の変更があるときだけ起動する（条件は phases.md）
- 広い検索・ログの要約は `models.mechanical` のモデルの subagent に任せる（`packages/core/docs/model-selection.md`）
- Worktreeベースの開発フローに従う
- AGENTS.md / CLAUDE.mdのすべてのルールを遵守する
