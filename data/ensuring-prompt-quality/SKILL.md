---
name: ensuring-prompt-quality
description: Validates prompt files against best practices. Use after creating or editing rules, skills, agents, commands in .agents/ for quality review.
compatibility: Claude Code
allowed-tools: Read Grep Glob WebFetch WebSearch
---

# Prompt Quality Skill

プロンプトファイルの品質を検証するスキルです。

## 記載ルール

**作成・編集時は以下のルールを参照**:

- **[writing-skills.md](../../rules/writing-skills.md)**: Skills の記載ルール
- **[writing-rules.md](../../rules/writing-rules.md)**: Rules の記載ルール
- **[writing-agents.md](../../rules/writing-agents.md)**: Agents の記載ルール
- **[writing-commands.md](../../rules/writing-commands.md)**: Commands の記載ルール

## 検証観点

| # | 観点 | 概要 |
|---|------|------|
| 1 | 明確性と具体性 | 曖昧な表現を避け、具体的な指示 |
| 2 | 構造化と可読性 | 適切な見出し、500行以下 |
| 3 | 具体例の提供 | Before/After 形式のコード例 |
| 4 | スコープの適切性 | タスク非依存、リポジトリレベル |
| 5 | Progressive Disclosure | 参照1階層、100行超は目次 |
| 6 | 重複と矛盾の回避 | DRY原則 |
| 7 | Workflow & Feedback Loops | チェックリスト、検証ループ |
| 8 | 命名とパス適用 | gerund形式、paths/globs |
| 9 | アクション指向 | 動詞から始まる指示 |
| 10 | メタデータの完全性 | 第三人称、トリガー含む |
| 11 | トーンと文体 | 命令形、一貫性 |
| 12 | テンプレートと例 | 出力形式テンプレート |
| 13 | アンチパターン検出 | Windows パス、時間依存 |
| 14 | 簡潔性 | 既知情報の繰り返しなし |

詳細は参照ファイルを確認:
- **[validation-criteria.md](references/validation-criteria.md)**: 観点1-7の詳細
- **[validation-criteria-technical.md](references/validation-criteria-technical.md)**: 観点8-14の詳細

## Workflow

品質検証時にこのチェックリストをコピー:

```
Quality Validation:
- [ ] Step 1: ファイルタイプを特定（skill/rule/agent/command）
- [ ] Step 2: 対応するルールを参照
- [ ] Step 3: メタデータを検証
- [ ] Step 4: コンテンツを検証（14観点）
- [ ] Step 5: ファイルサイズを確認
- [ ] Step 6: レポートを生成
```

### Step 1: ファイルタイプを特定

```bash
# パスからタイプを判定
.agents/skills/    → Skill
.agents/rules/     → Rule
.agents/agents/    → Agent
.agents/commands/  → Command
```

### Step 2: 対応するルールを参照

```bash
Read: .agents/rules/writing-{type}.md
```

### Step 3: メタデータを検証

```bash
# 一人称・二人称チェック
grep -n "I can\|I will\|You can\|You should" [file]

# 第三人称 + トリガー確認
grep -n "description:" [file]
```

**チェック項目**:
- [ ] name: 64文字以内、小文字・数字・ハイフン
- [ ] description: 第三人称、トリガー含む、1024文字以内
- [ ] paths/globs/allowed-tools: 適切に設定

### Step 4: コンテンツを検証

```bash
# 曖昧表現
grep -i "できれば\|なるべく\|maybe\|perhaps" [file]

# Windows パス
grep -n "\\\\" [file]

# 時間依存情報
grep -ni "before.*20[0-9][0-9]\|after.*20[0-9][0-9]" [file]

# Workflow チェックリスト
grep -n "- \[ \]" [file]
```

### Step 5: ファイルサイズを確認

```bash
wc -l [file]
# 500行以下推奨
```

### Step 6: レポートを生成

[report-template.md](references/report-template.md) 形式で出力。

If validation fails, identify issues and recommend fixes.

## クイック検証

単一ファイルの簡易チェック:

```bash
# 行数
wc -l [file]

# メタデータ
head -10 [file]

# アンチパターン
grep -n "I can\|You can\|\\\\" [file]
```

## 参照ファイル

- **[validation-criteria.md](references/validation-criteria.md)**: コンテンツ品質（1-7）
- **[validation-criteria-technical.md](references/validation-criteria-technical.md)**: 技術要件（8-14）
- **[best-practices.md](references/best-practices.md)**: 公式推奨事項
- **[examples.md](references/examples.md)**: 良い例・悪い例
- **[report-template.md](references/report-template.md)**: レポート形式
