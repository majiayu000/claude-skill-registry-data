---
name: backend-workflow
description: api/（FastAPI / Python 3.13）実装時に守る規約と検証手順。スクリーナー・チャット・Jobs・LLMプロバイダ等のサービス層実装時に必ず使う。LangGraphエージェント（api/app/services/agents/）のグラフ・ノード設計は langgraph-agent-design スキルを使う。
---

# バックエンド実装ワークフロー（api/）

## ディレクトリ構成

```
api/app/servers/api.py            エンドポイント
api/app/services/screener/        株式スクリーニング（yfinance + SQLite スナップショット）
api/app/services/chat/            チャット履歴（会話・メッセージ）
api/app/services/jobs/            汎用バックグラウンドジョブ基盤
api/app/services/agents/          AIエージェント（LangGraph。langgraph-agent-design スキル参照）
api/app/services/llm/             LLMプロバイダ（Bedrock / Ollama 切替）
api/app/services/tracing/         Langfuseトレーシング
api/app/types/                    Pydantic / TypedDict の型定義
```

## 型の使い分け

- **Pydantic**: API境界（リクエスト/レスポンス）。`app/types/api.py` 等。
- **TypedDict**: エージェント内部状態等、API境界に出ない型。

## エラーハンドリング / キャッシュ / ログ方針

- **リトライは `utils/retry.py` に集約**。LLM・重要I/Oは指数バックオフの
  `ainvoke_with_retry`、同期処理のレートリミットは判定付きの
  `invoke_with_retry_sync(should_retry=...)` を使う。
- **「失敗＝機能縮退」の外部呼び出し（Web検索・EDINET等）はリトライしない**。
  空結果を返して呼び出し側が続行できるようにする（過剰リトライで応答を
  遅くしない）。
- **短期キャッシュは `utils/cache.py` の `async_ttl_cache`**（企業概要1h、
  EDINET 30min 等の実例あり）。株価・指標はスクリーナーのスナップショット
  （`ScreenerRepository`）が正なので、そちらをキャッシュの代わりに使う。
- **Prompt/応答の詳細トレースはLangfuseが正**。アプリログは概況（所要時間・
  文字数・job_id）に留め、詳細を二重に持たない。

## 検証手順（完了前に必ず実行、`api/` で）

```bash
uv run pytest -q                   # テスト（mock でネットワーク非依存）
uv run ruff check app/ tests/      # Lint（E/W/F/I/B/UP）
uv run mypy app/                   # 型チェック（strict）
```

- テストは必ず mock 前提。`.env` が live でもテスト内で mock を明示する。
- 開発時の動作確認は `EXTERNAL_API_MODE=mock` で起動し、合成データで
  ネットワーク非依存に確認する。

## コーディング規約

- コメント・docstringは日本語。
- 変更は既存コードのスタイル・粒度に合わせる。

## 完了時

作業が一区切りついたら `git-workflow` スキルに従い commit + push する。
