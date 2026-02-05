---
name: .claude/skills/command-activation-mechanisms/SKILL.md
description: |
  コマンドの起動メカニズムを専門とするスキル。
  ユーザー明示起動、モデル自動起動（SlashCommand Tool）、Extended Thinkingトリガー、
  実行フローの完全図解を提供します。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/command-activation-mechanisms/resources/slashcommand-tool-guide.md`: SlashCommandツール詳細ガイド
  - `.claude/skills/command-activation-mechanisms/resources/user-explicit-activation.md`: ユーザー明示的起動パターン
  - `.claude/skills/command-activation-mechanisms/resources/execution-flow-diagrams.md`: コマンド実行フロー図解
  - `.claude/skills/command-activation-mechanisms/resources/extended-thinking-triggers.md`: Extended Thinkingトリガー設計
  - `.claude/skills/command-activation-mechanisms/templates/auto-invocation-template.md`: 自動起動コマンドテンプレート
  - `.claude/skills/command-activation-mechanisms/templates/extended-thinking-template.md`: Extended Thinking活用テンプレート
  - `.claude/skills/command-activation-mechanisms/scripts/validate-activation.mjs`: 起動メカニズム検証スクリプト

  使用タイミング:
  - SlashCommand Toolによる自動起動を理解したい時
  - Extended Thinkingを活用したい時
  - コマンド実行フローを設計する時

  Use proactively when understanding command activation, implementing auto-invocation,
  or designing execution flows.
version: 1.0.0
---

# Command Activation Mechanisms

## 概要

このスキルは、Claude Codeコマンドの起動メカニズムを提供します。
ユーザー明示起動、SlashCommand Toolによる自動起動、Extended Thinkingトリガー、
実行フローの完全理解により、効率的なコマンド設計ができます。

**主要な価値**:

- 2つの起動モードの完全理解
- SlashCommand Tool活用方法
- Extended Thinking統合
- 実行フロー最適化

**対象ユーザー**:

- コマンドを作成するエージェント（.claude/agents/command-arch.md）
- 自動起動を実装したい開発者
- 実行フローを理解したいチーム

## リソース構造

```
command-activation-mechanisms/
├── SKILL.md                                    # 本ファイル
├── resources/
│   ├── user-explicit-activation.md            # ユーザー明示起動詳細
│   ├── slashcommand-tool-guide.md             # SlashCommand Tool完全ガイド
│   ├── extended-thinking-triggers.md          # Extended Thinking詳細
│   └── execution-flow-diagrams.md             # 実行フロー図解集
└── templates/
    ├── auto-invocation-template.md            # 自動起動テンプレート
    └── extended-thinking-template.md          # Extended Thinkingテンプレート
```

### リソース種別

- **起動詳細** (`resources/*-activation.md`, `*-guide.md`): 各起動モードの詳細
- **Extended Thinking** (`resources/extended-thinking-triggers.md`): キーワードとパターン
- **実行フロー** (`resources/execution-flow-diagrams.md`): フロー図解集
- **テンプレート** (`templates/`): 起動モード別のテンプレート

## いつ使うか

### シナリオ1: 自動起動の実装

**状況**: CLAUDEmdから自動でコマンドを起動したい

**適用条件**:

- [ ] 特定のキーワードで自動起動したい
- [ ] SlashCommand Toolの仕組みを理解したい
- [ ] descriptionの最適化が必要

**期待される成果**: 自動起動可能なコマンド

### シナリオ2: Extended Thinkingの活用

**状況**: 深い思考を必要とするコマンドを作成したい

**適用条件**:

- [ ] 複雑な判断が必要
- [ ] 詳細な分析が必要
- [ ] 段階的な推論が必要

**期待される成果**: Extended Thinking活用コマンド

### シナリオ3: 実行フローの理解

**状況**: コマンド実行の内部動作を理解したい

**適用条件**:

- [ ] デバッグが必要
- [ ] パフォーマンス最適化が必要
- [ ] トラブルシューティングが必要

**期待される成果**: 実行フローの完全理解

## モード1: ユーザー明示起動

### 基本的な起動

```bash
# 直接入力
> /commit

# 引数付き
> /fix-issue 123

# 名前空間付き
> /project:create-feature user-authentication
```

### 実行フロー

```
┌──────────────────────────────────────┐
│ ユーザー入力: /commit "feat: add X" │
└───────────────┬──────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Claude Code がコマンドファイル検索     │
│ 1. .claude/commands/commit.md         │
│ 2. ~/.claude/commands/commit.md       │
│ 3. MCP プロンプト                      │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ コマンドファイル読み込み                │
│ - Frontmatter 解析                    │
│ - $ARGUMENTS 置換                     │
│ - 本文をプロンプトとして使用           │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Claude 実行                            │
│ - 指定モデル使用（デフォルト: Sonnet） │
│ - allowed-tools 制約適用              │
│ - ツール呼び出し実行                   │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ 結果返却                               │
│ - 標準出力へ表示                       │
│ - ファイル変更適用                     │
│ - 完了メッセージ                       │
└────────────────────────────────────────┘
```

## モード2: モデル自動起動

### SlashCommand Tool の仕組み

**重要な制約**:

```yaml
SlashCommand Tool が起動できるのは: ✓ カスタムコマンド（.claude/commands/）
  ✗ ビルトインコマンド（/compact, /init等）

条件:
  - description frontmatter が必須
  - disable-model-invocation: true の場合は起動不可
```

### CLAUDE.md での設定

```markdown
# ワークフローキーワード

以下のキーワードを検出したら、対応するコマンドを実行:

## コミット関連

- "commit", "コミット", "変更を保存"
  → `/commit` を実行

## レビュー関連

- "review", "レビュー", "コードチェック"
  → `/code-review` を実行

## テスト関連

- "test", "テスト", "動作確認"
  → `/run-tests` を実行

## デプロイ関連

- "deploy", "デプロイ", "本番反映"
  → 環境を確認してから `/deploy:staging` または `/deploy:production`
```

### 実行フロー

```
┌──────────────────────────────────────┐
│ ユーザー: "コードをレビューして"      │
└───────────────┬──────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ Claude が CLAUDE.md 参照              │
│ "コードレビュー時は /code-review" 発見│
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ SlashCommand Tool 起動判断            │
│ - description フィールド確認          │
│ - disable-model-invocation チェック   │
│ - コマンドの関連性評価                │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│ /code-review 自動実行                 │
│ （以降はユーザー明示起動と同じ）      │
└────────────────────────────────────────┘
```

### description の最適化

**悪い例**:

```yaml
description: Commit code
```

**良い例**:

```yaml
description: |
  Create a git commit following Conventional Commits specification.
  Automatically stages changes, analyzes diff, generates descriptive message,
  and pushes to current branch. Use when you want to commit and push changes
  in one command. Ideal for rapid development cycles.

  Keywords: commit, save changes, git commit
```

**最適化のポイント**:

1. 詳細な説明（4-8行）
2. トリガーキーワードを含める
3. 使用タイミングを明記
4. 期待される結果を記述

## Extended Thinking トリガー

### キーワード

コマンド内に以下のキーワードを含めると、Claudeは深い思考モードに入ります:

- `"think carefully"`
- `"consider thoroughly"`
- `"analyze deeply"`
- `"reason about"`
- `"evaluate carefully"`
- `"examine in detail"`

### 実装例

```markdown
---
description: Refactor code with careful analysis
---

# Intelligent Refactoring

## Analysis Phase

**Think carefully** about the code structure:

1. Identify code smells
2. Consider design patterns
3. Analyze dependencies
4. Evaluate maintainability

## Reasoning Phase

**Reason about** the best refactoring approach:

- What patterns would improve the code?
- What are the risks?
- What's the migration path?
- How will this affect existing functionality?

## Planning Phase

**Consider thoroughly** the implementation plan:

- Step-by-step refactoring steps
- Testing strategy
- Rollback plan

## Implementation

Apply the refactoring carefully with:

- Incremental changes
- Continuous testing
- Documentation updates
```

### 効果

```
通常実行:
→ 即座に実装開始
→ 浅い分析
→ リスク見落とし

Extended Thinking:
→ 深い分析フェーズ
→ 複数の選択肢を評価
→ リスクの詳細な検討
→ より良い実装判断
```

## 自然言語トリガー

### パターン1: 直接的なキーワード

```markdown
# CLAUDE.md

## Workflow Rules

When user says:

- "commit" → Execute `/commit`
- "test" → Execute `/run-tests`
- "deploy" → Execute `/deploy`
```

**実行例**:

```
ユーザー: "変更をコミットして"
↓
Claude: CLAUDE.md 参照 → "commit" キーワード検出
↓
SlashCommand Tool: /commit 実行
```

### パターン2: コンテキスト依存

```markdown
# CLAUDE.md

## Contextual Triggers

When user mentions deployment:

- If mentioning "staging" → `/deploy:staging`
- If mentioning "production" → `/deploy:production` (ask confirmation)
- If no environment specified → Ask which environment
```

**実行例**:

```
ユーザー: "ステージングにデプロイして"
↓
Claude: "staging" 検出
↓
SlashCommand Tool: /deploy:staging 実行
```

### パターン3: 意図推論

```markdown
# CLAUDE.md

## Intent-based Triggers

Analyze user intent:

- If discussing code quality → Suggest `/code-review`
- If discussing bugs → Suggest `/analyze-bug`
- If discussing features → Suggest `/plan-feature`
```

## デバッグとトラブルシューティング

### コマンドが見つからない

**症状**: `/mycommand` を実行しても "Command not found"

**確認事項**:

1. ファイルが存在するか？
   ```bash
   ls .claude/commands/mycommand.md
   ```
2. description が設定されているか？
3. ファイル名が正しいか？（kebab-case）

### 自動起動しない

**症状**: CLAUDE.md で設定したが自動起動しない

**確認事項**:

1. description が詳細か？（4-8行推奨）
2. トリガーキーワードを含んでいるか？
3. disable-model-invocation: true になっていないか？
4. CLAUDE.md の設定が正確か？

### Extended Thinking が機能しない

**症状**: Extended Thinking キーワードを使っても深い思考にならない

**確認事項**:

1. キーワードが正確か？（"think carefully" 等）
2. コマンドの複雑度が十分か？
3. モデルが適切か？（Haiku では効果が薄い）

## 詳細リソースの参照

### ユーザー明示起動

詳細は `resources/user-explicit-activation.md` を参照

### SlashCommand Tool ガイド

完全ガイドは `resources/slashcommand-tool-guide.md` を参照

### Extended Thinking トリガー

詳細は `resources/extended-thinking-triggers.md` を参照

### 実行フロー図解

図解集は `resources/execution-flow-diagrams.md` を参照

### テンプレート

- 自動起動: `templates/auto-invocation-template.md`
- Extended Thinking: `templates/extended-thinking-template.md`

## コマンドリファレンス

このスキルで使用可能なリソース、テンプレートへのアクセスコマンド:

### リソース読み取り

```bash
# ユーザー明示起動の詳細
cat .claude/skills/command-activation-mechanisms/resources/user-explicit-activation.md

# SlashCommand Tool完全ガイド
cat .claude/skills/command-activation-mechanisms/resources/slashcommand-tool-guide.md

# Extended Thinking詳細
cat .claude/skills/command-activation-mechanisms/resources/extended-thinking-triggers.md

# 実行フロー図解集
cat .claude/skills/command-activation-mechanisms/resources/execution-flow-diagrams.md
```

### テンプレート参照

```bash
# 自動起動テンプレート
cat .claude/skills/command-activation-mechanisms/templates/auto-invocation-template.md

# Extended Thinkingテンプレート
cat .claude/skills/command-activation-mechanisms/templates/extended-thinking-template.md
```

### 他のスキルのスクリプトを活用

```bash
# 知識ドキュメントの品質検証
node .claude/skills/knowledge-management/scripts/validate-knowledge.mjs .claude/skills/command-activation-mechanisms/resources/slashcommand-tool-guide.md

# トークン見積もり
node .claude/skills/context-optimization/scripts/estimate-tokens.mjs .claude/skills/command-activation-mechanisms/SKILL.md

# ドキュメント構造分析
node .claude/skills/documentation-architecture/scripts/analyze-structure.mjs .claude/skills/command-activation-mechanisms
```

## 関連スキル

- `.claude/skills/command-structure-fundamentals/SKILL.md` - description最適化
- `.claude/skills/command-security-design/SKILL.md` - disable-model-invocation

## 更新履歴

- v1.0.0 (2025-11-24): 初版作成
