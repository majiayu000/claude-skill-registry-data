---
name: personal-creating-git-branch
description: Git リポジトリの慣習に則って新しいブランチを作成します。ユーザーがブランチの作成を求めたときや、エージェントがブランチを作成するときに必ず使用してください。
allowed-tools: Bash(git branch:*), Bash(grep:*), Bash(head:*), Bash(sed:*), Bash(cut:*), Bash(sort:*), Bash(xargs:*)
---

# Git ブランチ作成

## 前提

`README.md` やメモリファイル（`AGENTS.md` や `CLAUDE.md` など）にブランチ名の規約がある場合、それに従う。

以下のワークフローは、明確な規約がない場合に実行します。

## ワークフロー

### 1. 情報収集

既存のブランチ名を取得：

```bash
git branch --sort=-committerdate | grep -v -E '^\*?\s*(main|master)\s*$' | head -10
```

### 2. 判定

#### スタイル判定

既存ブランチから以下を判定します。

- **シンプル形式**: `add-feature`、`fix-bug` などスラッシュなし
- **プレフィックス付き**: `feature/xxx`、`fix/xxx` などスラッシュを含む

##### 例外

- 複数スタイルが混在する場合、最も使用頻度の高いスタイルを採用
- 既存ブランチがない場合は、どのスタイルを使用するかユーザーに確認

#### プレフィックス判定

プレフィックス付きスタイルの場合、以下のコマンドでプレフィックス一覧を取得します：

```bash
git branch --all | head -100 | grep -v -E 'HEAD|main\s*$|master\s*$' | sed -E 's/^\*?\s*//; s|remotes/origin/||' | grep '/' | cut -d'/' -f1 | sort -u | xargs | sed 's/ /, /g'
```

### 3. ブランチ名生成

判定したスタイルに基づき、2〜5 単語程度のブランチ名を生成します。

- 動詞始まり（`add`、`update`、`fix`、`remove` など）
- ハイフン区切り
- 変更内容を簡潔に表現

### 4. ブランチ作成

生成されたブランチ名を表示し、ブランチを作成します。

```bash
git switch -c <branch-name>
```
