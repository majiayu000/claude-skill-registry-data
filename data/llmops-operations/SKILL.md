---
name: llmops-operations
description: LLMアプリケーションの設計・運用・評価・最適化。プロンプト管理、RAG構築、ファインチューニング、評価パイプライン、コスト最適化、本番運用。「LLM」「プロンプト」「RAG」「ファインチューニング」「AI運用」「評価」に関する質問で使用。
---

# LLMOps 設計・運用

## クイックスタート

### LLMアプリケーション基本構成

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages: list[dict], system: str = None) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system or "You are a helpful assistant.",
        messages=messages
    )
    return response.content[0].text
```

### RAG基本パターン

```python
from anthropic import Anthropic
import chromadb

# ベクトルDB初期化
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("docs")

def rag_query(query: str, k: int = 5) -> str:
    # 関連ドキュメント検索
    results = collection.query(query_texts=[query], n_results=k)
    context = "\n\n".join(results["documents"][0])
    
    # LLMに回答生成
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="以下のコンテキストに基づいて質問に回答してください。",
        messages=[
            {"role": "user", "content": f"コンテキスト:\n{context}\n\n質問: {query}"}
        ]
    )
    return response.content[0].text
```

## LLMOps原則

1. **評価駆動**: デプロイ前に必ず評価
2. **プロンプトバージョン管理**: プロンプトをコードとして管理
3. **コスト監視**: トークン使用量を常に監視
4. **フォールバック設計**: モデル障害時の代替経路
5. **ガードレール**: 入出力のバリデーション

## 詳細ガイド

- **プロンプトエンジニアリング**: [reference/prompting.md](reference/prompting.md)
- **RAG設計**: [reference/rag.md](reference/rag.md)
- **評価パイプライン**: [reference/evaluation.md](reference/evaluation.md)
- **本番運用**: [reference/production.md](reference/production.md)

## ユーティリティスクリプト

```bash
# プロンプト評価実行
python scripts/evaluate_prompts.py prompts/ test_cases.jsonl

# トークンコスト計算
python scripts/estimate_cost.py --model claude-sonnet-4-20250514 --input-file data.jsonl

# RAGインデックス構築
python scripts/build_index.py --docs ./documents --output ./index
```

## ワークフロー: LLMアプリ構築

```
進捗チェックリスト:
- [ ] 1. ユースケース定義・要件整理
- [ ] 2. プロンプト設計・プロトタイピング
- [ ] 3. 評価データセット作成
- [ ] 4. 評価パイプライン構築
- [ ] 5. RAG/ツール統合（必要な場合）
- [ ] 6. ガードレール実装
- [ ] 7. 本番環境デプロイ
- [ ] 8. モニタリング設定
```
