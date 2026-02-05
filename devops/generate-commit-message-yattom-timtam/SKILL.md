---
name: generate-commit-message
description: Generates clear, concise git commit messages in Japanese from staged changes. Use when the user asks to create a commit, write a commit message, or review staged changes for committing.
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

# Git コミットメッセージ生成

## 説明

このスキルは、ステージングされた変更から明確で簡潔な日本語のコミットメッセージを生成します。

## 指示

コミットメッセージの作成を求められたら：

1. **変更を確認**：
   - `git status` でステージングされたファイルを確認
   - `git diff --staged` で実際の変更内容を詳細に分析
   - `git log -3 --oneline` で最近のコミットメッセージのスタイルを確認

2. **変更を分析**：
   - 何が変更されたか（what）
   - なぜ変更したか（why）
   - どのコンポーネントが影響を受けるか

3. **メッセージを生成**：以下のフォーマットに従う

## フォーマット

```
<type>: <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### type（必須）

- `feat`: 新機能、既存機能の変更
- `fix`: 問題への対応
- `refactor`: リファクタリング（機能変更なし）
- `test`: テスト追加・修正
- `doc`: ドキュメント更新
- `style`: コードフォーマット（ロジック変更なし）
- `perf`: パフォーマンス改善
- `env`: ビルドや開発環境、生成AIの設定変更

### subject（必須）

- **日本語で**簡潔に（50文字以内推奨）
- 現在形または過去形（「追加」「変更した」など）
- 何をしたかを明確に

### body（推奨）

- **日本語で**詳細な説明
- 変更の理由（why）を重視し、全体の変更のねらいを記述する
- 変更内容 (what) は関連する複数の変更をひとつの変更として抽象度を高く記述する
- 変更した内容に応じて説明の量を合わせる。単純な内容であればbodyは不要。軽微な変更ならbodyも1行ていど。多量の変更をコミットする場合はbodyもひとつひとつの変更を丁寧に説明する。
- 関連のない複数の変更がある場合は箇条書き（`-` で始める）
- 72文字で折り返し

### footer（必須）

常に以下を含める：
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 例

### 例1: シンプルなリファクタリング

```
refactor: 無効入力テストをコンパクト化（YAML可視性を保持）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 例2: 詳細な機能追加

```
feat: Grasp設定のYAMLパーサーを実装

- GraspDefinitionとGraspGroupDefinitionの型定義
- js-yamlを使用したYAMLパース機能
- 必須フィールド（nodeId, promptTemplate, intervalSec, outputHandler）の
  バリデーション
- Vitestによるテストケース追加

YAMLベースの設定ファイルからGrasp定義を読み込むための基盤実装。
docs/grasp-config.mdで定義された仕様に準拠。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 例3: 名前変更のリファクタリング

```
refactor: cooldownMs を intervalSec に変更（ユーザーフレンドリー化）

cooldownという名前は制約のニュアンスがあり、ユーザーが望む実行頻度を
指定するという本質が伝わりにくい。より直感的なintervalSecに変更。

変更内容:
- cooldownMs → intervalSec（ミリ秒→秒でより読みやすく）
- Graspインターフェースとバリデーションを更新
- テストケースを更新（intervalSec validation追加）
- docs/grasp-config.md を全面更新
- docs/multi-llm-orchestration-plan.md のGrasp設定部分を更新

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## ベストプラクティス

- ✅ **日本語を使用**（このプロジェクトの標準）
- ✅ **簡潔に**：小さな変更は1行、複雑な変更は詳細を記述
- ✅ **理由を説明**：「なぜ」を重視（「何を」だけでなく）
- ✅ **一貫性**：既存のコミットログのスタイルに合わせる
- ✅ **フッター必須**：Claude Codeフッターを常に含める
- ❌ **絵文字は不要**：フッター以外では使わない

## このスキルを使うタイミング

- 変更をステージングした後、コミットメッセージが必要なとき
- 複雑な変更を明確に説明したいとき
- プロジェクトのコミットメッセージスタイルに従いたいとき
