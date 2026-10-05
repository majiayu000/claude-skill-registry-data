---
name: claude
description: |
  Claude Code CLI（Anthropic）を使用してコードや文言について相談・レビューを行う。
  トリガー: "claude", "claudeと相談", "claudeに聞いて", "コードレビュー", "レビューして"
  使用場面: (1) 文言・メッセージの検討、(2) コードレビュー、(3) 設計の相談、(4) バグ調査、(5) 解消困難な問題の調査
---

# Claude

Claude Code CLIを使用してコードレビュー・分析を実行するスキル。

## 実行コマンド（現行CLI対応）

```bash
cd <project_directory> && claude -p --dangerously-skip-permissions --output-format text "<request>"
```

### 任意オプション

- `--model <model_name>` でモデル指定可能（例: `sonnet`, `opus`）。
- `-r, --resume <session_id>` で既存セッションを再開可能。
- `-c, --continue` で直近セッションを継続可能。
- `--output-format json|stream-json` で機械可読出力に変更可能。
- `--allowed-tools ""` でツールを無効化してテキスト応答のみに制限可能。

## プロンプトのルール

**重要**: Claudeに渡すリクエストには、以下の指示を必ず含めること：

> 「確認や質問は不要です。具体的な提案・修正案・コード例まで自主的に出力してください。」

## パラメータ

| パラメータ | 説明 |
|-----------|------|
| `cd <dir>` | 対象プロジェクトのディレクトリへ移動（Claude CLIに `--cwd` 相当はないため） |
| `-p, --print` | 非対話モードで応答を出力して終了 |
| `--dangerously-skip-permissions` | 権限確認をスキップ（自動実行・サンドボックス環境向け） |
| `--output-format text` | テキスト形式で出力（既定値だが明示推奨） |
| `"<request>"` | 依頼内容（日本語可） |
| `--model <model_name>` | 任意。モデル指定 |
| `-r, --resume <session_id>` | 任意。既存セッション再開 |

## 使用例

**注意**: 各例では末尾に「確認不要、具体的な提案まで出力」の指示を含める。

### コードレビュー
```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "このプロジェクトのコードをレビューして、改善点を指摘してください。確認や質問は不要です。具体的な修正案とコード例まで自主的に出力してください。"
```

### バグ調査
```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "認証処理でエラーが発生する原因を調査してください。確認や質問は不要です。原因の特定と具体的な修正案まで自主的に出力してください。"
```

### アーキテクチャ分析
```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "このプロジェクトのアーキテクチャを分析して説明してください。確認や質問は不要です。改善提案まで自主的に出力してください。"
```

### リファクタリング提案
```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "技術的負債を特定し、リファクタリング計画を提案してください。確認や質問は不要です。具体的なコード例まで自主的に出力してください。"
```

### デザイン相談（UI/UX）
```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "あなたは世界トップクラスのUIデザイナーです。以下の観点からこのプロジェクトのUIを評価してください: (1) 視覚的階層構造とタイポグラフィ、(2) 余白・スペーシングのリズム、(3) カラーパレットのコントラストとアクセシビリティ、(4) インタラクションパターンの一貫性、(5) ユーザーの認知負荷の軽減。確認や質問は不要です。具体的な改善案をコード例付きで提示してください。"
```

```bash
cd /path/to/project && claude -p --dangerously-skip-permissions --output-format text "UXリサーチャー兼デザイナーとして、このフォームのユーザビリティを分析してください。Nielsen の10ヒューリスティクスに基づき、(1) エラー防止の仕組み、(2) ユーザーの制御と自由度、(3) 一貫性と標準、(4) 認識vs記憶の負荷、(5) 柔軟性と効率性を評価してください。確認や質問は不要です。改善したTailwind CSSコードまで自主的に提示してください。"
```

## 実行手順

1. ユーザーから依頼内容を受け取る
2. 対象プロジェクトのディレクトリを特定する（現在のワーキングディレクトリまたはユーザー指定）
3. **プロンプトを作成する際、末尾に「確認や質問は不要です。具体的な提案まで自主的に出力してください。」を必ず追加する**
4. 上記コマンド形式でClaudeを実行
5. 結果をユーザーに報告する
