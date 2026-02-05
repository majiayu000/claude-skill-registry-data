---
name: copilot-customization
description: 'GitHub Copilotカスタマイゼーションファイル（プロンプト、エージェント、インストラクション、スキル）の作成ガイド。.prompt.md、.agent.md、.instructions.md、SKILL.mdファイルをVS Codeのベストプラクティスに従って作成する際に使用してください。'
---

# GitHub Copilot Customization Files

このスキルは、GitHub Copilotのカスタマイゼーションファイル（プロンプト、エージェント、インストラクション、スキル）の作成を支援します。

## いつこのスキルを使用するか

以下の場合に本スキルを活用してください:

- 再利用可能なプロンプトファイル（`.prompt.md`）を作成する
- カスタムエージェント（`.agent.md`）を定義する
- ファイル固有のインストラクション（`.instructions.md`）を設定する
- Agent Skills（`SKILL.md`）を実装する
- プロジェクト固有の開発ワークフローを自動化する

## ファイルタイプ別ガイド

### 1. プロンプトファイル（.prompt.md）

**用途**: 再利用可能な質問・タスクのテンプレート

**作成場所**: `.github/prompts/`

**必須要素**:
- Markdown front matter（YAML）
- `description`: プロンプトの説明（シングルクォート）

**オプション要素**:
- `agent`: 実行エージェント（`ask`、`edit`、`agent`、またはカスタムエージェント名）
- `name`: UI表示名（未指定時はファイル名）
- `argument-hint`: チャット入力欄に表示するヒント
- `tools`: 利用可能なツール一覧
- `model`: 使用するAIモデル

**テンプレート**: [prompt-template.md](./templates/prompt-template.md)

**例**:
```markdown
---
description: 'コードレビューを実行し、品質とセキュリティの問題を特定'
agent: 'ask'
name: 'code-review'
argument-hint: 'レビュー対象のファイルまたはコードを入力'
tools: ['codebase', 'terminalCommand']
model: 'claude-sonnet-4.5'
---

# コードレビュープロンプト

指定されたファイルについて、以下の観点でレビューを実行してください:

1. コード品質
2. セキュリティ脆弱性
3. パフォーマンス最適化の機会
4. ベストプラクティス遵守

レビュー結果は優先度別に整理して報告してください。
```

### 2. エージェントファイル（.agent.md）

**用途**: 特定タスクに特化した自律エージェント

**作成場所**: `.github/agents/`

**必須要素**:
- Markdown front matter（YAML）
- `description`: エージェントの説明（シングルクォート）

**オプション要素**:
- `name`: UI表示名（未指定時はファイル名）
- `tools`: 利用可能なツール一覧
- `model`: 使用するAIモデル
- `infer`: サブエージェントとして使用（デフォルト: true）
- `target`: 対象環境（`vscode` または `github-copilot`）
- `mcp-servers`: MCPサーバー設定（JSON形式）
- `handoffs`: エージェント間の遷移定義

**テンプレート**: [agent-template.md](./templates/agent-template.md)

**例**:
```markdown
---
description: 'TypeScript MCPサーバー開発の専門アシスタント'
name: 'typescript-mcp-expert'
tools: ['codebase', 'terminalCommand', 'editFiles', 'search']
model: 'claude-sonnet-4.5'
infer: true
target: 'vscode'
handoffs:
  - label: 'プロンプトを実行'
    agent: 'generate-typescript-mcp-server'
    prompt: 'TypeScript MCPサーバーの包括的な実装を生成'
    send: false
---

# TypeScript MCP エキスパート

あなたは、TypeScript SDKを使用してMCPサーバーを構築する専門家です。

## 専門領域
- TypeScript/Node.js開発
- zodバリデーション
- Express統合
- MCP Inspector使用
```

### 3. インストラクションファイル（.instructions.md）

**用途**: ファイルタイプ別のコーディング規約・ガイドライン

**作成場所**: `.github/instructions/`

**必須要素**:
- Markdown front matter（YAML）
- `description`: インストラクションの説明（シングルクォート）

**オプション要素**:
- `name`: UI表示名（未指定時はファイル名）
- `applyTo`: 適用対象ファイルパターン（globパターン）。未指定時は手動追加のみ

**テンプレート**: [instructions-template.md](./templates/instructions-template.md)

**例**:
```markdown
---
description: 'Python MCPサーバー開発のコーディング規約'
name: 'python-mcp-guidelines'
applyTo: '**/*.py, **/pyproject.toml'
---

# Python MCP Server 開発ガイドライン

## 必須要件

- Python 3.10以上を使用
- uvでプロジェクト管理
- 型ヒントは必須
- Pydanticモデルで構造化出力
```

### 4. Agent Skills（SKILL.md）

**用途**: ツール、スクリプト、リソースを含む専門的なワークフロー

**作成場所**: `.github/skills/<skill-name>/SKILL.md`

**必須要素**:
- Markdown front matter（YAML）
- `name`: スキル名（小文字、ハイフン区切り、最大64文字）
- `description`: スキルの説明（最大1024文字）

**構造**:
```
.github/skills/
  └── my-skill/
      ├── SKILL.md          # メインスキルファイル
      ├── templates/        # テンプレートファイル
      ├── examples/         # サンプルコード
      └── scripts/          # 実行スクリプト
```

**テンプレート**: [skill-template.md](./templates/skill-template.md)

## ベストプラクティス

### 命名規約

**ファイル名**: 小文字、ハイフン区切り
- ✅ `generate-mcp-server.prompt.md`
- ✅ `python-best-practices.instructions.md`
- ❌ `GenerateMCP.prompt.md`
- ❌ `python_instructions.md`

**スキル名**: 小文字、ハイフン区切り、最大64文字
- ✅ `python-mcp-development`
- ✅ `cpp14-code-review`
- ❌ `PythonMCPDev`
- ❌ `python_mcp_development`

### Description フィールド

**要件**:
- シングルクォートで囲む
- 空でない
- 明確で具体的
- 使用タイミングを含める

**良い例**:
```yaml
description: 'Guide for building MCP servers using Python SDK. Use this when creating, debugging, or optimizing Python-based MCP servers.'
```

**悪い例**:
```yaml
description: "Python MCP"  # ダブルクォート、詳細不足
```

### Tools 指定（推奨）

プロンプト・エージェントで使用するツールを明示:

```yaml
tools: ['codebase', 'terminalCommand', 'editFiles', 'search']
```

MCPサーバーのツールを含める場合は `<server name>/*` 形式を使用:

```yaml
tools: ['codebase', 'my-mcp-server/*']
```

### Model 指定（強く推奨）

最適化されているモデルを指定:

```yaml
model: 'claude-sonnet-4.5'
```

## 段階的作成ワークフロー

### ステップ1: 要件定義

```markdown
質問:
- 何を自動化したいか?
- 誰が使うか?
- どのファイルに適用するか?
- 必要なツールは?
```

### ステップ2: ファイルタイプ選択

| タイプ | 用途 |
|--------|------|
| `.prompt.md` | 単発の質問・タスク |
| `.agent.md` | 複雑な自律タスク |
| `.instructions.md` | ファイル別のコーディング規約 |
| `SKILL.md` | スクリプト・リソースを含む専門ワークフロー |

### ステップ3: テンプレート使用

[テンプレート集](./templates/)から適切なテンプレートを選択し、カスタマイズ。

### ステップ4: 検証

- [ ] Front matterが正しいYAML形式
- [ ] 必須フィールドが存在（`description`など）
- [ ] ファイル名が命名規約に準拠
- [ ] `applyTo`（インストラクション）が正しいglobパターン
- [ ] 説明が具体的で有用

### ステップ5: テスト

- プロンプト: VS Code Copilot Chatで`#<prompt-name>`を実行
- エージェント: `@<agent-name>`で呼び出し
- インストラクション: 対象ファイルで動作確認
- スキル: Copilot Chatが自動的にスキルを提案することを確認

## 実装例

### 例1: テストコード生成プロンプト

[generate-tests.prompt.md](./templates/examples/generate-tests.prompt.md)

### 例2: ドキュメント生成エージェント

[doc-generator.agent.md](./templates/examples/doc-generator.agent.md)

### 例3: TypeScript コーディング規約

[typescript.instructions.md](./templates/examples/typescript.instructions.md)

### 例4: Python MCP開発スキル

[python-mcp-development/SKILL.md](./templates/examples/python-mcp-skill.md)

## トラブルシューティング

### 問題1: Front matterエラー

**症状**: YAMLパースエラー

**解決策**:
- ダブルクォートではなくシングルクォートを使用
- インデントをスペース2つで統一
- `---`の前後に余計な空白を入れない

### 問題2: プロンプトが認識されない

**症状**: `#<prompt-name>`で呼び出せない

**解決策**:
- ファイル名が`.prompt.md`で終わるか確認
- `.github/prompts/`ディレクトリに配置
- VS Code を再読み込み

### 問題3: インストラクションが適用されない

**症状**: 対象ファイルで有効にならない

**解決策**:
- `applyTo`のglobパターンを確認（`'**/*.py'`など）
- 複数パターンはカンマ区切り: `'**/*.ts, **/*.js'`

## 参考リソース

- [VS Code プロンプトファイル](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [VS Code カスタムエージェント](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code カスタムインストラクション](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Agent Skills 仕様](https://agentskills.io/)
- [Awesome Copilot](https://github.com/github/awesome-copilot)
- [テンプレート集](./templates/)

## 次のステップ

1. [テンプレート](./templates/)から開始
2. 要件に応じてカスタマイズ
3. `.github/`配下の適切なディレクトリに配置
4. VS Code Copilot Chatでテスト
5. チーム・コミュニティと共有

---

**カスタマイゼーションファイル作成のサポートが必要な場合は、関連エージェント `generate-customization-md` を使用してください。**
