---
name: Installing Plugins Manually
description: Manually install Claude Code plugin components when official plugin installation fails. Use when `/plugin install` succeeds but plugins don't load, when verifying plugin installation, or when user mentions plugin installation issues.
allowed-tools: Read, Bash, Edit, Write
---

# Installing Plugins Manually

このSkillは、公式の`/plugin install`コマンドが失敗した場合に、プラグインのコンポーネント（Sub-agents、Commands、Skills）を手動で抽出・インストールする方法を提供します。

## いつ使うか

以下の状況で使用してください：

- `/plugin install`が成功メッセージを表示するが、実際にプラグインがロードされない
- `~/.claude/plugins/config.json`が空のまま（`repositories: {}`）
- プラグインが正しくインストールされているか検証したい
- ユーザーがプラグインのインストール問題について言及している

## 診断フロー

### ステップ1: インストール状況の確認

まず、プラグインが実際にインストールされているか確認します：

```bash
# プラグイン設定を確認
cat ~/.claude/plugins/config.json

# インストール済みプラグインを確認
ls -la ~/.claude/plugins/repos/
```

**判定基準**:
- `config.json`が`{"repositories": {}}`の場合 → インストール失敗
- `repos/`ディレクトリが空の場合 → インストール失敗

### ステップ2: マーケットプレイスの確認

マーケットプレイスが正しく追加されているか確認します：

```bash
# 登録済みマーケットプレイスを確認
cat ~/.claude/plugins/known_marketplaces.json

# マーケットプレイスの実体を確認
ls -la ~/.claude/plugins/marketplaces/
```

### ステップ3: プラグインの構造を解析

対象プラグインの構造を確認します：

```bash
# プラグインディレクトリの内容を確認
ls -la ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/

# 各コンポーネントを確認
ls -la ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/agents/
ls -la ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/commands/
ls -la ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/skills/
```

## 手動インストール手順

プラグインのインストールが失敗した場合、以下の手順で手動インストールを実行します。

### ステップ1: コンポーネントの特定

マーケットプレイスの`marketplace.json`を確認して、プラグインに含まれるコンポーネントを特定します：

```bash
# marketplace.jsonから対象プラグインの定義を抽出
grep -A 30 '"name": "[plugin-name]"' ~/.claude/plugins/marketplaces/[marketplace-name]/.claude-plugin/marketplace.json
```

### ステップ2: Sub-agentsのコピー

```bash
# Sub-agentsをグローバルディレクトリにコピー
cp ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/agents/*.md ~/.claude/agents/
```

**確認**:
```bash
ls -la ~/.claude/agents/ | grep [agent-name]
```

### ステップ3: Commandsのコピー

```bash
# スラッシュコマンドをグローバルディレクトリにコピー
cp ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/commands/*.md ~/.claude/commands/
```

**確認**:
```bash
ls -la ~/.claude/commands/ | grep [command-name]
```

### ステップ4: Skillsのコピー

```bash
# Skillsをグローバルディレクトリにコピー（ディレクトリごと）
cp -r ~/.claude/plugins/marketplaces/[marketplace-name]/plugins/[plugin-name]/skills/* ~/.claude/skills/
```

**確認**:
```bash
ls -la ~/.claude/skills/ | grep [skill-name]
```

### ステップ5: インストールの検証

すべてのコンポーネントが正しくコピーされたか確認します：

```bash
# 各コンポーネントの存在確認
ls -la ~/.claude/agents/[agent-name].md
ls -la ~/.claude/commands/[command-name].md
ls -la ~/.claude/skills/[skill-name]/
```

## 実例: javascript-typescript プラグイン

以下は`claude-code-workflows`マーケットプレイスから`javascript-typescript`プラグインを手動インストールする実例です。

### コンポーネントの確認

```bash
# プラグインの構造を確認
ls -la ~/.claude/plugins/marketplaces/claude-code-workflows/plugins/javascript-typescript/
# 出力例:
# agents/
# commands/
# skills/
```

### 手動インストールの実行

```bash
# Sub-agentsをコピー
cp ~/.claude/plugins/marketplaces/claude-code-workflows/plugins/javascript-typescript/agents/javascript-pro.md ~/.claude/agents/
cp ~/.claude/plugins/marketplaces/claude-code-workflows/plugins/javascript-typescript/agents/typescript-pro.md ~/.claude/agents/

# Commandsをコピー
cp ~/.claude/plugins/marketplaces/claude-code-workflows/plugins/javascript-typescript/commands/typescript-scaffold.md ~/.claude/commands/

# Skillsをコピー
cp -r ~/.claude/plugins/marketplaces/claude-code-workflows/plugins/javascript-typescript/skills/* ~/.claude/skills/
```

### 検証

```bash
# コピーされたコンポーネントを確認
ls -la ~/.claude/agents/ | grep -E "(javascript|typescript)"
ls -la ~/.claude/commands/ | grep typescript
ls -la ~/.claude/skills/ | grep -E "(javascript|typescript|nodejs)"
```

**期待される出力**:
```
javascript-pro.md
typescript-pro.md
typescript-scaffold.md
javascript-testing-patterns/
modern-javascript-patterns/
nodejs-backend-patterns/
typescript-advanced-types/
```

## よくある問題と対処法

### 問題1: `.claude-plugin/plugin.json`が存在しない

一部のマーケットプレイス（特に`claude-code-workflows`）では、個別のプラグインに`.claude-plugin/plugin.json`が存在せず、マーケットプレイスの`marketplace.json`で一括管理しています。

**対処法**: 手動インストールを使用してください。プラグインシステムを経由せず、直接コンポーネントをコピーします。

### 問題2: インストール成功メッセージが出るが実際にはインストールされない

`/plugin install`が`✓ Installed`と表示しても、`config.json`が空のままの場合があります。

**対処法**:
1. 診断フローで実際のインストール状況を確認
2. 失敗している場合は手動インストールに切り替え

### 問題3: コピー後もClaude Codeが認識しない

コンポーネントをコピーしても認識されない場合があります。

**対処法**:
1. Claude Codeを再起動
2. `/help`でコマンドが表示されるか確認
3. `/agents`でエージェントが表示されるか確認

## チェックリスト

手動インストール完了前に以下を確認：

- [ ] マーケットプレイスが正しく追加されている
- [ ] プラグインの構造を確認した
- [ ] すべてのSub-agentsをコピーした
- [ ] すべてのCommandsをコピーした
- [ ] すべてのSkillsをコピーした
- [ ] コピーしたファイルの存在を確認した
- [ ] Claude Codeを再起動した
- [ ] `/help`でコマンドが表示されることを確認した

## プロジェクトローカルへのインストール

グローバルではなく、プロジェクトローカルにインストールしたい場合：

```bash
# プロジェクトルートに.claude/ディレクトリを作成
mkdir -p .claude/agents .claude/commands .claude/skills

# コンポーネントをプロジェクトローカルにコピー
cp [source]/agents/*.md .claude/agents/
cp [source]/commands/*.md .claude/commands/
cp -r [source]/skills/* .claude/skills/
```

## 注意事項

### ライセンスと著作権

マーケットプレイスからプラグインをコピーする際は、各プラグインのライセンスを確認してください。ほとんどのプラグインはMITライセンスですが、商用利用の制限がある場合があります。

### 更新管理

手動インストールしたコンポーネントは、マーケットプレイスの更新を自動で取得できません。定期的にマーケットプレイスを確認し、必要に応じて手動で更新してください。

```bash
# マーケットプレイスを最新化
cd ~/.claude/plugins/marketplaces/[marketplace-name]
git pull

# 更新されたコンポーネントを再コピー
```

## 自動化スクリプト

手動コピーが面倒な場合は、自動化スクリプトを使用できます：

```bash
# 使い方
~/.claude/skills/plugin-fallback-installer/scripts/install-plugin-manually.sh [marketplace] [plugin]

# 例: javascript-typescriptをインストール
~/.claude/skills/plugin-fallback-installer/scripts/install-plugin-manually.sh claude-code-workflows javascript-typescript

# プロジェクトローカルにインストール
~/.claude/skills/plugin-fallback-installer/scripts/install-plugin-manually.sh claude-code-workflows javascript-typescript --local

# ドライラン（プレビューのみ）
~/.claude/skills/plugin-fallback-installer/scripts/install-plugin-manually.sh claude-code-workflows javascript-typescript --dry-run
```

このスクリプトは以下を自動的に実行します：
- プラグインの構造を解析
- すべてのコンポーネントをコピー
- インストール結果をサマリー表示

## さらに詳しい情報

### より多くの実例
様々なマーケットプレイスとプラグインタイプの実例は [examples.md](examples.md) を参照してください。

### チェックリストテンプレート
手動インストールを追跡するためのチェックリストは [templates/plugin-install-checklist.md](templates/plugin-install-checklist.md) を参照してください。

## まとめ

公式のプラグインシステムが失敗した場合でも、この手動インストール方法を使用することで、確実にプラグインの機能を利用できます。

**主なメリット**:
- 確実にコンポーネントがインストールされる
- プラグインシステムのバグを回避できる
- 必要なコンポーネントだけを選択的にインストールできる
- 自動化スクリプトで効率化できる

**注意点**:
- 手動で更新管理が必要
- ライセンスの確認が必要
- 再起動が必須
