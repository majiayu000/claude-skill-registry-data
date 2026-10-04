---
name: release-epic
description: >
  親エピック Issue 配下の子 Issue が全て close されていることを確認した上で、
  feature/epic-* → main のリリース PR を作成し、子 Issue タイトルから自動生成したリリースノートを PR 本文に記載する。
  full プリセット専用。
  「/release-epic」「エピックをリリースして」「feature ブランチを main にマージするPR作って」と言った時に使用。
---

# 🚀 エピックリリーススキル

> [!IMPORTANT]
> このスキルは **親エピック配下の子 Issue が全 close 済みである場合のみ** `feature/epic-*` → `main` のリリース PR を作成する。
> **`gh pr merge --auto` は呼ばない**（承認フロー非介入思想）。マージは Branch Protection + CodeRabbit approve に委ねる。
> **コード変更は一切行わない** — PR 作成と親 Issue 更新のみ。タグ打ち・バージョニング・デプロイは扱わない。
> 結果のみを簡潔に返す（途中経過は不要）。介入ポイントでは CEO の指示を待つ（自動でスキップしない）。

CEO が `/vibecorp:release-epic <親エピック Issue 番号>` を実行すると、エピック配下の子 Issue が全て完了していることを GitHub API で検証してから、`feature/epic-*` → `main` のリリース PR を作成する。子 Issue タイトルを束ねたリリースノートを PR 本文に自動生成し、親エピック Issue にリリース PR の予告リンクを貼る。

## 📝 本文の書き方

PR タイトル・PR 本文・親 Issue へのコメントは CEO が読むため `.claude/rules/communication.md` に従って**動作主語**で書く（「〜になった／〜できるようになった」）。関数名・ファイルパスを並べるのではなく、ソフトウェアのふるまいの変化を 30 秒で掴める形にする。

## 使用方法

```bash
/vibecorp:release-epic <親エピック Issue 番号>
```

`<親エピック Issue 番号>` が省略された場合は CEO にヒアリングする（複数エピック並走時の曖昧性を避けるため必須）。

## 前提条件

- **full プリセット専用**（エピック運用は full プリセットでのみ整備されているため）
- GitHub CLI (`gh`) が認証済みであること
- 親エピック Issue が既に存在すること（`/vibecorp:plan-epic` で起票されている前提）
- `feature/epic-<親番号>_*` ブランチが origin に push されていること
- リポジトリが GitHub 上にあり、sub-issue API が利用可能であること

## ワークフロー

### 1. プリセット確認

vibecorp.yml の preset を確認する。full 以外の場合は以下を出力して終了する。

```text
/vibecorp:release-epic は full プリセット専用です。現在のプリセット: <preset>
```

```bash
awk '/^preset:/ { print $2 }' "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml"
```

### 2. 引数検証

引数が空の場合は CEO にヒアリングする。複数エピックの並走時に親 Issue を曖昧にしないよう、番号は必須引数とする。

### 3. 親エピック Issue の取得

```bash
gh issue view <親番号> --json number,title,body,state,labels
```

- Issue が存在しない場合は中断する
- `state == "closed"` の場合は中断する（既にリリース済みの可能性、CEO に確認する）

### 4. エピック判定

タイトルに `🎯 epic:` プレフィックス、または `epic` ラベルが付与されていることを確認する。どちらも無い場合は「指定 Issue はエピックではありません」と中断する。

### 5. sub-issue 一覧の取得

GitHub 公式の sub-issue API で子 Issue 一覧を取得する。

```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  --paginate \
  "/repos/<owner>/<repo>/issues/<親番号>/sub_issues"
```

- `<owner>/<repo>` は `gh repo view --json owner,name --jq '.owner.login + "/" + .name'` で取得する
- `--paginate` を必ず付けて全件取得する（既定 30 件超のエピック対応）

公式仕様: https://docs.github.com/en/rest/issues/sub-issues

子 Issue が 0 件の場合は中断する（リリース対象なし）。

### 6. 未 close 子 Issue の検証

子 Issue 一覧から `state == "open"` のものを抽出する。1 件でも残っていれば中断する。

```text
⚠️ 未 close の子 Issue が <n> 件あります:
- #<番号> <タイトル>
- #<番号> <タイトル>

完了してから再実行してください。
```

全て `closed` の場合のみ次に進む。

### 7. feature ブランチの存在確認

`feature/epic-<親番号>_*` ブランチが origin に push されていることを確認する。Issue #346 で確立した命名規約に準拠する。

```bash
git ls-remote --heads origin "feature/epic-<親番号>*"
```

| 検出件数 | 挙動 |
|---|---|
| 0 件 | 中断（「ブランチが未作成」と CEO に報告） |
| 2 件以上 | 中断（「複数候補があります」と CEO に列挙報告） |
| 1 件 | そのブランチ名を **完全一致の文字列**（例: `feature/epic-349_release_epic`）として保持し、後段の重複確認・PR 作成で同じ値を再利用する |

`gh pr list --head` および `gh pr create --head` はワイルドカードをサポートしないため（[公式ドキュメント](https://cli.github.com/manual/gh_pr_list)）、ステップ 7 で確定した完全一致のブランチ名を変数として保持しておくことが必須となる。

### 8. リリースノートの生成

子 Issue タイトルを束ねた PR 本文を生成する。子 Issue の絵文字プレフィックス（✨ / 🐛 / 🔄 / 📖 / 🔒 / 🚀 等）はそのまま流用する。

```markdown
## 🚀 エピックリリース

エピック #<親番号> <親タイトル> がリリース可能になった。

## 📦 含まれる変更（子 Issue ベース）

- ✨ #<子1番号> <子1タイトル>
- 🐛 #<子2番号> <子2タイトル>
- 🔄 #<子3番号> <子3タイトル>

## ✅ 完了確認

- 子 Issue が全て close されていることを確認した
- feature ブランチへのマージは GitHub の auto-merge で完結している

## 🔗 関連

- 親エピック Issue: #<親番号>

Closes #<親番号>
```

PR 本文末尾に `Closes #<親番号>` を必ず記載する（GitHub auto-close キーワード）。リリース PR が main にマージされると、親エピック Issue が自動 close される。`#N` 形式必須（URL 形式は `close-on-feature-merge.yml` の抽出対象外）。詳細は `.claude/rules/workflow.md` の「PR 本文の Issue リンク（auto-close キーワード）」を参照する。

PR タイトルは `🚀 release: epic #<親番号> <親タイトル>` の形式とする。

### 9. 既存 PR の重複確認

同一 head（feature ブランチ）→ base（main）の open PR が既に存在しないか確認する。ステップ 7 で確定した完全一致のブランチ名（例: `feature/epic-349_release_epic`）を `--head` に渡す（ワイルドカードは利用不可）。

```bash
gh pr list --base main --head "<ステップ7で確定した完全一致のブランチ名>" --state open --json number,title,url
```

- 既存 PR が見つかった場合は新規作成せず CEO に報告して中断する（auto-merge 機構と衝突させないため）

### 10. リリース PR の作成

ステップ 7 で確定した完全一致のブランチ名を `--head` にそのまま渡す。

```bash
gh pr create \
  --base main \
  --head "<ステップ7で確定した完全一致のブランチ名>" \
  --title "🚀 release: epic #<親番号> <親タイトル>" \
  --body "<生成したリリースノート>"
```

- `gh pr merge --auto` は **呼ばない**（承認フロー非介入思想）
- マージは Branch Protection + CodeRabbit approve に委ねる

### 11. 親エピック Issue の更新

親エピック Issue 本文の末尾に「リリース PR を作成しました: #<PR番号>」を追記する。

```bash
gh issue edit <親番号> --body "<更新後の本文>"
```

または既存本文末尾に追記する形でコメントを残す。

```bash
gh issue comment <親番号> --body "🚀 リリース PR を作成しました: #<PR番号>"
```

本文編集とコメント追記のどちらかを選択する。本文に「## 🚀 リリース PR」セクションを追加するのが既定動作とする（後から見たときに親 Issue 単体でリリース状況が分かるため）。

### 12. 結果報告

```text
## /vibecorp:release-epic 完了

### 🚀 リリース PR
- <PR URL>: <PR タイトル>

### 📦 リリース対象
- 親エピック: #<親番号> <親タイトル>
- 子 Issue: <n> 件（全て close 済み）
- feature ブランチ: feature/epic-<親番号>_<要約>
- base ブランチ: main

### ✅ 次のアクション
- マージは GitHub の auto-merge（Branch Protection + CodeRabbit approve）で完結する
- 本スキルは PR 作成のみで auto-merge は設定していない（承認フロー非介入）
```

## 🚦 介入ポイント

以下の状況では CEO に報告して判断を委ねる。

| 状況 | タイミング |
|------|-----------|
| full プリセットでない | ステップ 1 |
| 引数が空 | ステップ 2 |
| 親 Issue が存在しない / closed | ステップ 3 |
| 親 Issue がエピックでない（ラベル / プレフィックスなし） | ステップ 4 |
| sub-issue が 0 件 | ステップ 5 |
| 未 close 子 Issue がある | ステップ 6 |
| feature ブランチが未作成 / 複数候補 | ステップ 7 |
| 同一 head / base の既存 PR がある | ステップ 9 |
| gh CLI が認証されていない | 全ステップ共通 |

## 制約

- **コード変更は一切行わない** — PR 作成と Issue 更新のみ
- **auto-merge 設定はスコープ外** — `gh pr merge --auto` は呼ばない（承認フロー非介入思想）
- **タグ打ち・バージョニング・デプロイは扱わない** — 別 Issue で扱う
- `--force`、`--hard`、`--no-verify` は使用しない
- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない
- **Bash は 1 コマンド 1 呼び出しに分割する** — `cd ... && cmd | head 2>/dev/null` のように cd + パイプ + リダイレクトを含む compound command は Claude Code 本体の built-in security check（path resolution bypass 検出）で止められるため
- 介入ポイントでは CEO の指示を待つ（自動でスキップしない）

## 🔗 関連ルール

- 設計判断: `.claude/knowledge/cpo/decisions/2026-Q2.md` 2026-04-18 「Issue 親子関係・大規模リリース支援」
- 関連 Issue: #345 (`/plan-epic` スキル新設) / #346 (`/ship` base 判定) / #347 (GHA 自動 close)
- GitHub sub-issue API: https://docs.github.com/en/rest/issues/sub-issues
- ブランチ命名・auto-close キーワード: `.claude/rules/workflow.md`
- CEO 報告向け文面規約: `.claude/rules/communication.md`
- 自律実行不可領域: `.claude/rules/autonomous-restrictions.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
