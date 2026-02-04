---
name: graphrag
description: PostgreSQL + pgvector + PGroonga で GraphRAG を構築。自然言語でプロジェクトを説明すると、最適なEntity/Edge型、スキーマ、クエリパターンを設計・生成。Use when the user mentions "GraphRAG", "knowledge graph", or wants to build RAG with relationships.
---

# GraphRAG PostgreSQL Skill

PostgreSQL単体（pgvector + PGroonga拡張）でGraphRAGを構築するためのスキル。
**自然言語でプロジェクトを説明すると、最適なGraphRAGスキーマを設計・生成する。**

## How It Works

```
/graphrag 小説のキャラクター関係を管理したい。時系列で関係が変化する
```

↓ Claude が分析

```
Entity型: Character, Location, Organization, Event, Item
Edge型: friend_of, enemy_of, ally_of, family_of, participates_in
追加機能: 時系列サポート（events テーブル）
```

↓ ユーザー確認後、生成

```
sql/schema.sql, sql/indexes.sql, sql/queries/*.sql, docs/
```

## Output Location

```
{project}/
├── sql/
│   ├── schema.sql              # カスタマイズされたスキーマ
│   ├── indexes.sql             # インデックス定義
│   └── queries/
│       ├── local_search.sql    # Entity中心検索
│       ├── global_search.sql   # 全体俯瞰検索
│       ├── hybrid_search.sql   # Hybrid Search
│       └── custom_*.sql        # 要件固有のクエリ
└── docs/
    ├── graphrag-guide.md       # 運用ガイド
    └── prompts/
        ├── entity_extraction.md
        └── edge_extraction.md
```

## Execution Flow

### Phase 1: Analyze User Requirements

**ユーザーの自然言語の説明を分析**:

1. **データの種類**: 何を管理したいか（小説、技術文書、FAQ、障害報告...）
2. **追跡したい関係**: どんな関係が重要か（人間関係、依存関係、因果関係...）
3. **検索・分析の要件**: どんなクエリが必要か（関連検索、パス検索、影響分析...）
4. **特別な要件**: 時系列、ネタバレ制御、承認フロー、重要度など

### Phase 2: Read Reference Documents

以下のリファレンスを参照して設計:

- [references/use-cases.md](references/use-cases.md) - 既存パターンを参考に
- [references/architecture.md](references/architecture.md) - アーキテクチャ基本
- [references/schema-design.md](references/schema-design.md) - スキーマ設計
- [references/entity-extraction.md](references/entity-extraction.md) - Entity/Edge抽出

### Phase 3: Design Entity/Edge Types

**ユーザー要件に最適なEntity型とEdge型を設計**:

参考パターン（use-cases.md より）:

| パターン | Entity型例 | Edge型例 |
|----------|-----------|----------|
| 物語・コンテンツ | Character, Location, Item | friend_of, enemy_of, possesses |
| 技術文書 | Technology, API, Component | depends_on, implements, extends |
| ナレッジベース | Concept, Process, Document | defines, precedes, references |
| 障害・トラブル | Symptom, Cause, Solution | causes, solved_by, affects |
| 法務・規約 | Clause, Requirement, Exception | refers_to, overrides, exception_of |

**これらを参考に、ユーザー要件に合わせてカスタム設計する。**

### Phase 4: Confirm Design with User

AskUserQuestionで設計を確認:

1. **プロジェクト名**
2. **Entity型の確認**: 「以下のEntity型を提案します。追加/削除があれば教えてください」
3. **Edge型の確認**: 「以下のEdge型を提案します」
4. **オプション**:
   - Embedding dimension: 1536 / 768 / Custom
   - Primary language: Japanese / English
   - 時系列サポート: Yes / No
   - Global Search (Community): Yes / No

### Phase 5: Generate Schema

1. Read `templates/schema-core.sql`
2. **設計したEntity/Edge型をスキーマに反映**:
   - コメントとして型定義を追加
   - 必要な拡張テーブルを追加
3. Write to `sql/schema.sql`

### Phase 6: Generate Indexes

参照: [references/indexing-strategies.md](references/indexing-strategies.md)

- pgvector: HNSW（推奨）
- PGroonga: Japanese → TokenMecab / English → TokenBigram

### Phase 7: Generate Custom Queries

参照: [references/query-patterns.md](references/query-patterns.md)

**ユーザーの検索要件に基づいてクエリを生成**:

- `local_search.sql` - Entity中心のn-hop展開
- `global_search.sql` - Community reports検索
- `hybrid_search.sql` - PGroonga + pgvector (RRF)
- `custom_*.sql` - 要件固有（依存ツリー、因果パス、類似検索等）

### Phase 8: Generate Entity Extraction Prompts

参照: [references/entity-extraction.md](references/entity-extraction.md)

**設計したEntity/Edge型に基づいてLLM抽出プロンプトを生成**:

- `docs/prompts/entity_extraction.md` - Entity抽出用
- `docs/prompts/edge_extraction.md` - Edge抽出用

### Phase 9: Generate Documentation

参照: [references/chunking-strategies.md](references/chunking-strategies.md)

- `docs/graphrag-guide.md`:
  - Entity/Edge型の定義と説明
  - Chunking戦略
  - クエリの使い方
  - パフォーマンスチューニング

### Phase 10: Completion Report

生成完了を報告:
1. 設計したEntity/Edge型のサマリー
2. 生成されたファイル一覧
3. 次のステップ

## Reference Files

共通:
- [references/architecture.md](references/architecture.md) - 全体アーキテクチャ
- [references/schema-design.md](references/schema-design.md) - テーブル設計詳細
- [references/indexing-strategies.md](references/indexing-strategies.md) - インデックス戦略
- [references/query-patterns.md](references/query-patterns.md) - 検索パターン

ユースケース固有:
- [references/use-cases.md](references/use-cases.md) - **ユースケース別Entity/Edge型定義**
- [references/chunking-strategies.md](references/chunking-strategies.md) - ユースケース別Chunking
- [references/entity-extraction.md](references/entity-extraction.md) - 抽出プロンプト

オプション:
- [references/community-detection.md](references/community-detection.md) - コミュニティ検出

## Template Files

- [templates/schema-core.sql](templates/schema-core.sql) - コアテーブル
- [templates/schema-extensions.sql](templates/schema-extensions.sql) - 拡張テーブル
- [templates/indexes.sql](templates/indexes.sql) - インデックス
- [templates/query-local.sql](templates/query-local.sql) - Local Search
- [templates/query-global.sql](templates/query-global.sql) - Global Search
- [templates/query-hybrid.sql](templates/query-hybrid.sql) - Hybrid Search
