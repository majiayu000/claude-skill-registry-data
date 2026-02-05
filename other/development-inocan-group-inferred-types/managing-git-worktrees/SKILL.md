---
name: managing-git-worktrees
description: Manages Git Worktree parallel development. Required when starting new work. Creates worktrees with wt- prefix for parallel development. User confirmation required before creation.
---

# Git Worktree並行開発ガイド

## 📖 このスキルについて

Git Worktreeを使用した並行開発の完全ガイドです。複数のブランチを同時に作業でき、Claude Codeの制約を考慮した実用的な運用方法を提供します。

## 🎯 使用タイミング

- **新規作業開始時（必須確認）**
- **並行開発が必要な時**
- **PO Agentのworktree管理時**
- **Developer Agentのworktree作業時**
- **Submoduleを含むプロジェクトでの並行開発**

## 🚨 最重要ルール：新規作業時のWorktree使用

### 必須の確認フロー

**新しい、今までの作業と関係ない作業だと判断した場合：**

#### Step 1: Submoduleの有無を最初に確認（必須）
```bash
ls -la .gitmodules
git submodule status
```

#### Step 2: Submoduleの有無に応じた分岐

##### 【Submoduleがない場合】
通常のworktree作成フローに従う：
1. ユーザーに確認してworktree作成
2. プロジェクトルート直下に`wt-xxx`を作成

##### 【Submoduleがある場合】→ 🚨最重要判断

**⚠️ 絶対ルール: submodule内のコードを変更する場合、親gitにworktreeを作成してはいけない**

1. **変更対象を厳密に明確化すること**
   - 何を変更するのか具体的に特定
   - **親git自体のコード**（プロジェクトルートの設定ファイル、親gitのsrc/など）？
   - **submodule内のコード**？

2. **変更対象に基づいてworktree作成場所を決定**
   - **親git自体のコード変更**: 親gitルートでworktree作成
   - **Submodule内のコード変更**:
     - 🚫 **親gitにはworktreeを絶対に作らない**
     - ✅ 対象submoduleディレクトリに移動してからworktree作成
     - worktreeパスは`submodule名/wt-xxx`形式

3. **必ずユーザーに確認を取ってから実行すること**
   - どういう名前のworktreeで作業するか提案
   - Submodule内変更の場合は、どのsubmoduleにworktreeを作成するか明記
   - **🚫 Submodule内変更の場合、親gitにはworktreeを作らないことを明示**
   - ユーザーの承認を得てから作成
   - **勝手にworktreeを作成して作業開始してはいけない**

4. **現在作業しているworktreeでの作業であれば確認不要**
5. **このworktreeを使った作業フローは絶対に遵守すること**

### 判断基準フローチャート

```
新しいタスク受信
    ↓
現在の作業と関連？
    ├─ Yes → 現在のworktreeで作業継続（確認不要）
    └─ No → 新規worktree必要
        ↓
        Step 1: Submoduleの有無を確認
        ├─ Submoduleなし → AskUserQuestionで作業場所を確認
        └─ Submoduleあり → AskUserQuestionで変更対象と作業場所を確認
```

## 🎯 AskUserQuestion形式の選択肢（必須）

**すべてのworktree確認はAskUserQuestion形式の選択肢で行う**

### Step 0: 作業場所の選択（最初に必ず確認）

```python
AskUserQuestion(
    questions=[{
        "question": "新しい作業を開始します。作業場所を選択してください",
        "header": "作業場所",
        "options": [
            {
                "label": "現在のブランチで作業",
                "description": f"現在のブランチ `{current_branch}` で直接作業を開始"
            },
            {
                "label": "新規worktreeを作成",
                "description": "独立したworktreeで作業（並行開発向け）"
            }
        ],
        "multiSelect": False
    }]
)
```

### Step 1: Submoduleがない場合のworktree作成確認

```python
AskUserQuestion(
    questions=[{
        "question": f"worktree `wt-{feature_name}` を作成しますか？",
        "header": "Worktree作成",
        "options": [
            {
                "label": "作成する",
                "description": f"ブランチ `feature/{feature_name}` を作成して作業開始"
            },
            {
                "label": "作成しない",
                "description": "現在のブランチで作業を継続"
            }
        ],
        "multiSelect": False
    }]
)
```

### Step 2: Submoduleがある場合の変更対象選択

```python
AskUserQuestion(
    questions=[{
        "question": "変更対象を選択してください",
        "header": "変更対象",
        "options": [
            {
                "label": "親git側のコード",
                "description": "プロジェクトルートの設定ファイルや親gitのソースコード"
            },
            {
                "label": f"Submodule: {submodule_name}",
                "description": f"{submodule_name}内のコードを変更"
            }
            # 複数submoduleがある場合は各submoduleを選択肢として追加
        ],
        "multiSelect": False
    }]
)
```

### Step 3: Submodule内変更時のworktree作成確認

```python
AskUserQuestion(
    questions=[{
        "question": f"{submodule_name}内にworktreeを作成しますか？",
        "header": "Submodule Worktree",
        "options": [
            {
                "label": "作成する",
                "description": f"{submodule_name}/wt-{feature_name} を作成（親gitには作成しません）"
            },
            {
                "label": "作成しない",
                "description": f"{submodule_name}の現在のブランチで作業"
            }
        ],
        "multiSelect": False
    }]
)
```

### 複合選択肢の例（効率化）

複数の確認を1回で行う場合：

```python
AskUserQuestion(
    questions=[
        {
            "question": "作業場所を選択してください",
            "header": "作業場所",
            "options": [
                {"label": "現在のブランチ", "description": f"`{current_branch}` で作業"},
                {"label": "新規worktree", "description": "独立した作業環境を作成"}
            ],
            "multiSelect": False
        },
        {
            "question": "変更対象を選択してください（worktree作成時のみ）",
            "header": "変更対象",
            "options": [
                {"label": "親git", "description": "親リポジトリのコード"},
                {"label": f"{submodule_name}", "description": "Submodule内のコード"}
            ],
            "multiSelect": False
        }
    ]
)

## 📚 詳細ドキュメント

### [基本概念と制約](./CONCEPTS.md)
- Git Worktreeとは
- Claude Codeの制約と解決策
- 推奨ディレクトリ構造
- Agent階層との統合

### [ワークフロー](./WORKFLOWS.md)
- Worktreeの作成方法
- Worktreeでの作業手順
- Worktreeの管理と削除
- 実践的な操作コマンド

### [命名規則](./NAMING.md)
- 基本フォーマット
- カテゴリ別の命名例
- パラメータの詳細説明
- 命名のベストプラクティス

### [トラブルシューティング](./TROUBLESHOOTING.md)
- よくある問題と解決方法
- ベストプラクティス（DO/DON'T）
- serena連携の設定
- gwqツールの活用

## 🚀 クイックスタート

### 0. 変更対象の確認（最重要）
```bash
# 何を変更するか明確化
# - 親git側のコード変更？
# - Submodule内のコード変更のみ？

# Submoduleの有無を確認
ls -la .gitmodules
git submodule status
```

### 1. 新規Worktree作成

#### ケース1: 親git側のコード変更
```bash
# 親gitルートで実行
# 既存worktreeを確認
git worktree list

# 新規worktreeを作成（ユーザー確認後）
git worktree add -b feature/new-feature wt-feat-new-feature main
```

#### ケース2: Submodule内のコード変更のみ
```bash
# ⚠️ 重要: 親gitにはworktreeを作らない

# 対象submodule内でworktreeを作成（ユーザー確認後）
cd submodule1
git worktree add -b feature/new-feature wt-feat-new-feature main

# 作業対象のsubmoduleのworktreeに移動
cd wt-feat-new-feature
```

### 2. Worktreeで作業

#### ケース1: 親git側のコード変更
```bash
# 親gitのworktreeに移動
cd wt-feat-new-feature

# 環境設定をコピー
cp ../.env .env
cp -r ../.serena .serena

# 開発作業
git status
git add .
git commit -m "feat: implement new feature"
```

#### ケース2: Submodule内のコード変更のみ
```bash
# 対象submoduleのworktreeに移動（既に移動済みの場合はスキップ）
cd submodule1/wt-feat-new-feature

# 環境設定をコピー（submoduleの親ディレクトリから、必要に応じて）
cp ../.env .env 2>/dev/null || echo "No .env in submodule"
cp -r ../.serena .serena 2>/dev/null || echo "No .serena in submodule"

# 開発作業
git status
git add .
git commit -m "feat: implement new feature in submodule"
```

### 3. 作業完了後

#### ケース1: 親git側のコード変更
```bash
# 親gitルートに戻る
cd ..

# Worktree削除（ユーザーまたはManagerが実行）
git worktree remove wt-feat-new-feature
```

#### ケース2: Submodule内のコード変更のみ
```bash
# submoduleのルートに戻る
cd ..  # submodule1/wt-feat-new-feature から submodule1 へ

# submodule内のWorktree削除（ユーザーまたはManagerが実行）
git worktree remove wt-feat-new-feature

# プロジェクトルートに戻る
cd ..
```

## ⚠️ 重要な注意事項

### DO（必須事項）
- ✅ **Step 1: Submoduleの有無を最初に確認**
- ✅ 新規worktree作成時は**必ずユーザー確認**
- ✅ **変更対象を明確化**（親git自体のコード vs submodule内のコード）
- ✅ `wt-`プレフィックスを使用
- ✅ Submoduleなし：プロジェクトルートに作成
- ✅ 親git自体のコード変更：親gitルートに作成
- ✅ Submodule内のコード変更：対象submodule内にのみ作成（`submodule名/wt-xxx`）
- ✅ `.env`と`.serena`をコピー

### DON'T（禁止事項）
- ❌ 勝手にworktreeを作成
- ❌ 勝手にworktreeを削除
- ❌ Submoduleの有無確認をスキップ
- ❌ 変更対象の確認をスキップ

### 🚫 絶対禁止（Submodule関連）
- ❌ **Submodule内のコード変更なのに親gitにworktree作成**（🚨最重要禁止事項）
- ❌ **Submodule内変更でworktreeパスが`wt-xxx`（親gitルート直下）**
  - ✅ 正しいパス: `submodule名/wt-xxx`
- ❌ 親ディレクトリ（`../`）への作成
- ❌ serenaの再初期化

## 🔗 関連スキル

- **using-serena**: Worktree内でのコード分析・編集
- **managing-agent-hierarchy**: PO AgentによるWorktree管理、Developer AgentによるWorktree作業

## 📋 チェックリスト

新規worktree作成時：
- [ ] **Step 1: Submoduleの有無を確認**（`.gitmodules`と`git submodule status`）
- [ ] **Step 2: Submoduleの有無に応じた分岐**
  - **Submoduleなし**: プロジェクトルートにworktree作成
  - **Submoduleあり**: 変更対象を厳密に判断
- [ ] **変更対象を明確化**（親git自体のコード vs submodule内のコード）
- [ ] ユーザーに確認を取得（作成場所を明記）
- [ ] `wt-`プレフィックスで命名
- [ ] `git worktree add`で作成
  - Submoduleなし：プロジェクトルートで実行
  - 親git自体の変更：親gitルートで実行
  - Submodule内変更：対象submodule内でのみ実行
    - 🚫 **親gitには絶対に作らない**
    - ✅ worktreeパス: `submodule名/wt-xxx`
- [ ] worktreeに移動
- [ ] `.env`をコピー（必要に応じて）
- [ ] `.serena`をコピー
- [ ] 作業開始

作業完了時：
- [ ] すべての変更をコミット
- [ ] リモートにプッシュ
- [ ] 元のディレクトリに戻る
- [ ] Worktree削除（ユーザーまたはManagerが実行）
  - 親git側変更：親gitルートで削除
  - Submodule内変更：対象submodule内で削除

---

**次のステップ**: [基本概念と制約](./CONCEPTS.md)で詳細を確認してください。
