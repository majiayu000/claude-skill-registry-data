---
name: commit
description: "Conventional Commits形式でのGitコミット自動化。変更を分析し、適切なコミットメッセージを生成してgit add + git commitを実行する。「/commit」「コミットして」と言った時に使用。"
---

# 💾 Git コミット自動化

> [!IMPORTANT]
> このスキルは変更を分析し、**Conventional Commits 11 種 + 絵文字 1:1 マッピング** で commit を作成する。
> 主従順は **intent ラベル（主）→ CC prefix（従）**。逆引きは行わない。
> 件名・本文は CEO が読むため `.claude/rules/communication.md` に従って **動作主語** で書く。
> 結果のみを簡潔に返す。途中経過は出力しない。

変更を分析し、Conventional Commits 形式でコミットを作成する。

## 🌳 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read/Write/Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継ぐ。
- 未指定時は従来通り CWD で実行する（後方互換）。

## 🔄 ワークフロー

### 1. リポジトリ情報の取得

```bash
gh repo view --json owner,name --jq '.owner.login + "/" + .name'
```

`REPO_OWNER/REPO_NAME` として Issue URL 組み立てに使用する。

### 2. 状態確認

```bash
git status
```

```bash
git diff --staged
```

```bash
git diff
```

```bash
git log --oneline -5
```

### 3. ステージング

特定ファイルを優先して `git add` する。`git add -A` は避ける。

### 4. コミットメッセージ生成と実行

#### 4a. CC 11 種から prefix を選ぶ（vibecorp 厳格定義）

Conventional Commits 11 種すべてを採用する。各 prefix の vibecorp 厳格定義は `docs/conventional-commits.md` を参照（`refactor` は挙動不変厳格化、`chore` は依存メジャー更新不可、`build` はランタイム挙動変更不可、等）。

| CC prefix | 用途 |
|-----------|------|
| `feat` | 新機能追加（観測可能な挙動が新たに加わる） |
| `fix` | バグ修正（セキュリティ脆弱性も含む） |
| `perf` | 性能改善（観測可能な性能特性が変わる） |
| `refactor` | 構造改善（**挙動不変**、公開 API リネーム不可） |
| `style` | フォーマット・スタイル修正のみ |
| `docs` | ドキュメントのみ（コード本体に影響しない） |
| `test` | テストコードのみ（本番コード触れない） |
| `ci` | CI 設定のみ |
| `chore` | 雑務（**挙動不変**、依存メジャー更新で API 変わるなら不可） |
| `build` | ビルドシステム（**挙動不変**、ランタイム挙動変えるなら不可） |
| `revert` | 過去 commit の差し戻し |

#### 4b. CC prefix → 絵文字 1:1 マッピング

`docs/conventional-commits.md` 確定の絵文字 11 種を必ず使う。

| CC prefix | 絵文字 |
|-----------|------|
| feat | ✨ |
| fix | 🐛 |
| perf | ⚡ |
| refactor | 🔄 |
| style | 💄 |
| docs | 📖 |
| test | 🧪 |
| ci | 🔧 |
| chore | ⚙️ |
| build | 📦 |
| revert | ⏪ |

#### 4c. intent 主導で prefix を選ぶ（主従関係）

Issue 駆動のブランチ（`dev/<番号>_*`）の場合、Issue のラベル（`intent/*`）が intent を示している。intent → CC prefix の主従順で対応 prefix を選ぶ（`.claude/rules/intent-labels.md` の絶対条件、逆引き禁止）。Issue ラベル未確認でもコミット内容から intent を先に確定し、対応 prefix を選ぶ。

#### 4d. ルール

- 件名・本文は CEO が読むため `.claude/rules/communication.md` に従って **動作主語** で書く（「〜になった／〜できるようになった」）。これは **コミットメッセージ本体（CEO 報告向け文面）** に対する規約であり、本 `SKILL.md` ファイル自体の文面に適用される **`prompt-writing.md` の LLM 行動主語ルール**（「〜する／〜しない／〜禁止」）とは対象が異なる（両規約は `prompt-writing.md` の「communication.md との違い」セクションで明示される）。
- 件名フォーマット: `<emoji> <CC prefix>: <動作主語の subject>`（scope を付ける場合は `<emoji> <CC prefix>(<scope>): <subject>`）。
- 件名は動作主語・ピリオドなし・推奨 50 文字以下。
- Issue 番号はブランチ名から抽出（例: `dev/12345_feature` → #12345）。
- 本文は変更内容を箇条書きで列挙する。
- `revert` PR は `intent/bugfix` ラベル付与済みのため、コミット側でも prefix `revert` + 絵文字 ⏪ を使う。

```bash
git commit -m "<emoji> <CC prefix>: <subject>

https://github.com/{REPO_OWNER}/{REPO_NAME}/issues/{ISSUE_NUMBER}

- 変更内容1
- 変更内容2"
```

**HEREDOC やサブシェル展開 `$(...)` は使わない**。`-m` に直接文字列を渡す。

### 5. 確認

```bash
git log --oneline -1
```

## ⚠️ 制約

- `--force`、`--hard`、`--no-verify` は使用しない。
- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
- `.env`、認証情報、シークレットはコミットしない。
- 明示的な要求なしに `--amend` や `push` を行わない。
- `git add -A` より特定ファイルのステージングを優先する。

## 📤 返却フォーマット

```text
<commit-hash> <emoji> <CC prefix>: <subject>
```

scope 付きの場合は `<emoji> <CC prefix>(<scope>): <subject>` 形式を使う（タイトル形式と統一）。

## 🔗 関連ルール

- CC prefix 厳格定義: `docs/conventional-commits.md`
- intent ラベル定義: `.claude/rules/intent-labels.md`
- CEO 報告向け文面規約: `.claude/rules/communication.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
