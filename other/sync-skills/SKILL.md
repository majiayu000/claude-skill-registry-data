---
name: sync-skills
description: "Claude Codeプラグインのスキルを.agents/skills/にsymlinkし、Codexから発見可能にする。「sync-skills」「スキル同期」で起動。"
allowed-tools: Read, Bash, Glob, Grep
---

# sync-skills

Claude Codeプラグインのスキルを `.agents/skills/` にsymlinkし、Codexから発見可能にする。

## When to Use

- プラグイン更新後
- 新しいプロジェクトでCodexからスキルを使いたい時
- `.agents/skills/` のsymlinkが壊れた時

## Workflow

### Step 1: Read installed_plugins.json

```bash
cat ~/.claude/plugins/installed_plugins.json | jq -r '
  .plugins | to_entries[] | .value[] |
  [.scope, .installPath, (.projectPath // "")] | @tsv
'
```

各エントリのscope/installPath/projectPathを取得。

### Step 2: Filter plugins

- `scope=user`: 常に対象
- `scope=local`: projectPathが現在のプロジェクトと一致する場合のみ

### Step 3: Create symlinks

対象pluginごとに `installPath/skills/` 配下のディレクトリを `.agents/skills/` にsymlink。

```bash
mkdir -p .agents/skills
ln -s <installPath>/skills/<skill-name> .agents/skills/<skill-name>
```

- raw skill名を使用（prefix無し）
- 壊れたsymlink: 削除して再作成
- 正しいsymlink: スキップ
- 衝突: ユーザーに確認（上書き or スキップ）

### Step 4: Report

作成/スキップ/衝突の結果を報告。

## Reference

- 詳細手順: [reference.md](reference.md)
