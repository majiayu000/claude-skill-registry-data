---
name: plan-epic
description: >
  CEO が指定したテーマを複数の子タスクに分解し、親 Issue（エピック）と子 Issue を一括起票して
  GitHub 公式の sub-issue API で親子関係を構築する。full プリセット専用。
  「/plan-epic」「エピック化」「Issue を分解して」と言った時に使用。
---

# 🎯 エピック化スキル

> [!IMPORTANT]
> **full プリセット専用**。CEO が指定したテーマを子タスクに分解し、親 Issue（エピック）+ 子 Issue 群を一括起票して GitHub 公式 sub-issue API で親子関係を構築する。
> コード変更は一切行わない（起票と紐付けのみ）。子 Issue 実装は `/vibecorp:ship` で別途実行する。
> 結果のみを簡潔に返す。途中経過は出力しない。

CEO が「このテーマをエピック化して」と依頼した時、plan mode で子タスク分解を提示し、承認後に親 Issue + 子 Issue 群を一括起票する。子 Issue は GitHub 公式 sub-issue API で親に紐付ける。

## 📝 本文の書き方

親 Issue・子 Issue のタイトル・本文は CEO が読むため `.claude/rules/communication.md` に従って **動作主語** で書く（「〜になった／〜できるようになった」）。関数名・ファイルパスを並べるのではなく、ソフトウェアのふるまいの変化を 30 秒で掴める形にする。

## 🛠️ 使用方法

```bash
/vibecorp:plan-epic <テーマ>           # plan mode で分解 → 親+子 Issue 起票 → sub-issue 紐付け
/vibecorp:plan-epic <テーマ> --dry-run # 分解と起票プレビューのみ（実際には起票しない）
```

`<テーマ>` が省略された場合は CEO にヒアリングする。

## 🧱 前提条件

- **full プリセット専用**（CISO/CPO/SM の 3 者承認ゲートを子 Issue 起票時に通すため、`/vibecorp:issue` が full プリセットの判定機能を要求する）
- GitHub CLI (`gh`) が認証済みであること
- リポジトリが GitHub 上にあり、sub-issue API が利用可能であること

## 📋 ワークフロー

### 1. プリセット確認

vibecorp.yml の preset を確認する。full 以外の場合は以下を出力して終了する:

```text
/vibecorp:plan-epic は full プリセット専用です。現在のプリセット: <preset>
```

```bash
awk '/^preset:/ { print $2 }' "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml"
```

### 2. テーマのヒアリング

引数でテーマが渡されていない場合は CEO に確認する。

- **テーマ**: エピックとして括る上位の目的（例: 「Issue 親子関係導入」「課金構造の総点検」）
- **背景**: なぜこのエピックが必要か（任意）
- **完了基準**: エピックの達成条件（任意）

### 3. plan mode で子タスクへの分解を提示

`EnterPlanMode` でプラン mode に入り、テーマを以下の観点で子タスクへ分解する。

- **独立性**: 子タスクは可能な限り並行実装できる粒度に分ける
- **テスト込み**: 各子タスクにテスト方針を含める
- **段階性**: 基盤 → 実装 → 統合 の流れを意識する
- **スコープ**: 1 子タスクは 1 PR で完結するサイズに収める

分解結果を以下のフォーマットで CEO に提示する。

```markdown
## 🎯 エピック: <テーマ>

### 📦 子タスク
| # | タイトル | 概要 | 依存 |
|---|---------|------|------|
| 1 | <子1> | <概要> | — |
| 2 | <子2> | <概要> | #1 |
| 3 | <子3> | <概要> | — |

### 🗺️ 実装順序
- 並行実装可能: <子1>, <子3>
- 直列: <子2>（<子1> 完了後）
```

`ExitPlanMode` で承認待ちにする。CEO が承認しなかった場合は終了する。

### 4. 親 Issue（エピック）の起票

承認後、親 Issue を `gh issue create` で直接起票する。

- **タイトル**: `🎯 epic: <テーマ>`
- **ラベル**: `epic`（リポジトリに存在する場合のみ付与）
- **本文**: 以下のテンプレート

```markdown
## 🎯 エピック概要

<テーマと背景>

## 📦 子 Issue（実装は /vibecorp:ship で別途）

- [ ] #<子1番号>
- [ ] #<子2番号>
- [ ] #<子3番号>

## ✅ 完了基準

<エピック全体の完了条件>

## 📍 関連ファイル

<!-- エピック全体で触れるファイル・モジュールのパス一覧（relevant file locations）。 -->
<!-- Anthropic 公式推奨の初回プロンプト 4 要素のうち relevant file locations を起票時点で揃える。 -->
- `<対象ファイル 1>`
- `<対象ファイル 2>`

---
この Issue は /vibecorp:plan-epic により起票されました。
```

子 Issue 番号は次のステップで決まるため、起票時点では空のチェックリスト（後段で更新）にしてもよい。実装上は「子 Issue 起票完了 → 親 Issue 本文を `gh issue edit` で更新」の順で構わない。

```bash
gh issue create --title "🎯 epic: <テーマ>" --body "<本文>" --label "epic"
```

`epic` ラベルがリポジトリに存在しない場合は `--label` を省略する（`gh label list` で確認）。

### 5. 親 feature ブランチの作成

親エピックの feature ブランチを作成し、origin に push する。`/ship` が `git ls-remote` で自動検出するために必要。

**5-1. default branch を取得:**

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

**5-2. ブランチを作成して push:**

```bash
git switch -c "feature/epic-<親番号>_<要約>" "origin/<default_branch>"
git push -u origin "feature/epic-<親番号>_<要約>"
```

- ブランチ名は `feature/epic-{親Issue番号}_{要約}` 形式（`docs/specification.md` のブランチ命名規約に準拠）
- `<要約>` は親 Issue タイトルからスラッシュ・スペースを `_` に置換し、英数字・アンダースコア・ハイフンのみにサニタイズする
- push まで完了させることで `/ship` の `git ls-remote --heads origin "feature/epic-<親番号>_*"` で確実に検出される

### 6. 子 Issue の起票（/vibecorp:issue 経由）

ステップ 3 で分解した子タスクを 1 件ずつ `/vibecorp:issue` スキル経由で起票する。

子タスクの本文末尾に親エピックへの参照として **`Refs #<親番号>`** を必ず含める。`Closes` ではなく `Refs` を使うことで、子 PR がマージされても親エピックは auto-close されず、`/vibecorp:release-epic` のリリース PR で最終的に close される（`Refs #<親エピック番号>` 形式も等価）。

```text
/vibecorp:issue を使って以下の子 Issue を起票してください:

タイトル: <子タスクのタイトル>
本文: <子タスクの本文>

---

## 📍 関連

Refs #<親エピック番号>
```

- `/vibecorp:issue` の 3 者承認ゲート（CISO + CPO + SM）が自動で走る
- いずれかの子 Issue が「除外」判定された場合は、その子 Issue だけスキップして CEO に報告する（親 Issue は残し、後から手動で追加可能とする）
- `Closes #N` / `Refs #N` の運用は `.claude/rules/workflow.md`「PR 本文の Issue リンク（auto-close キーワード）」を参照

### 7. sub-issue API で親に紐付け

各子 Issue を GitHub 公式の sub-issue API で親 Issue に紐付ける。

```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/<owner>/<repo>/issues/<親番号>/sub_issues" \
  -f sub_issue_id=<子の数値ID>
```

- `<owner>/<repo>` は `gh repo view --json owner,name --jq '.owner.login + "/" + .name'` で取得
- `<子の数値ID>` は `gh issue view <子番号> --json id --jq '.id'` で取得（issue 番号ではなく内部 ID が必要）
- API エラー時はその子のみ紐付け失敗として記録し、最終レポートに明記する（処理は継続）

公式仕様: https://docs.github.com/en/rest/issues/sub-issues

### 8. 親 Issue 本文の更新

親 Issue の本文のチェックリストを実際の子 Issue 番号に書き換える。

```bash
gh issue edit <親番号> --body "<更新後の本文>"
```

### 9. 結果報告

```text
## /vibecorp:plan-epic 完了

### 🎯 親 Issue（エピック）
- <親 URL>: <タイトル>

### 📦 子 Issue
| # | タイトル | URL | sub-issue 紐付け |
|---|---------|-----|------------------|
| 1 | <子1> | <URL> | ✅ |
| 2 | <子2> | <URL> | ✅ |
| 3 | <子3> | <URL> | ⚠️ 失敗（要手動紐付け） |

### サマリ
- 起票: <親1 + 子N> 件
- スキップ（3 者承認ゲートで除外）: <n> 件
- sub-issue 紐付け失敗: <n> 件
```

## 🚦 介入ポイント

以下の状況では CEO に報告して判断を委ねる（自動でスキップしない）。

| 状況 | タイミング |
|------|-----------|
| full プリセットでない | ステップ 1 |
| CEO が plan を承認しない | ステップ 3 |
| 子 Issue 起票で 3 者承認ゲートが「除外」と判定 | ステップ 6 |
| sub-issue API がエラーを返した | ステップ 7 |
| gh CLI が認証されていない | 全ステップ共通 |

## 🪶 --dry-run モード

`--dry-run` が指定された場合は以下のみ実行する。

1. プリセット確認
2. テーマヒアリング
3. plan mode で子タスク分解を提示
4. 起票プレビュー（親 Issue 本文と子 Issue タイトル一覧をレポート出力）

ステップ 4 以降の起票・ブランチ作成・API 呼び出しは行わない。

## ⚠️ 制約

- **コード変更は一切行わない** — Issue 起票と sub-issue 紐付けのみ。
- 子 Issue 実装は CEO が `/vibecorp:ship` で別途起動する（本スキルでは ship を呼ばない）。
- `--force` / `--hard` / `--no-verify` は使用しない。
- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈されパースエラーを引き起こす。必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null` / `|| echo` / `; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- 介入ポイントでは CEO の指示を待つ（自動でスキップしない）。
- 親 Issue 自体は不可領域変更を直接含まないため 3 者承認ゲートを通さない（メタ情報）。子 Issue 側で個別に走る `/vibecorp:issue` のゲートに依存する。

## 🔗 関連

| 種別 | 参照先 |
|------|--------|
| 設計判断 | `.claude/knowledge/cpo/decisions/2026-Q2.md` 2026-04-18 「Issue 親子関係: 条件付き Go」 |
| GitHub sub-issue API | https://docs.github.com/en/rest/issues/sub-issues |
| 自律実行不可領域 | `.claude/rules/autonomous-restrictions.md` |
| CEO 向け文面規約 | `.claude/rules/communication.md` |
| プロンプト作成基準 | `.claude/rules/prompt-writing.md` |
| マークダウン規約 | `.claude/rules/markdown.md` |
| 関連スキル | `/vibecorp:issue`（子 Issue 起票）/ `/vibecorp:ship`（子 Issue 実装）/ `/vibecorp:release-epic`（親エピック close） |
