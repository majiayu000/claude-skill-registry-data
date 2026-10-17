---
name: langgraph-agent-design
description: api/app/services/agents/ 配下でLangGraphエージェント（親/子グラフ・ノード・State）を新規作成/変更する際に必ず使う。スパゲティ化を防ぐための設計8原則のチェックリスト。
---

# LangGraph エージェント設計チェックリスト（api/app/services/agents/）

エージェント実装はスパゲティ化しやすい。着手前・実装後にこのチェックリストで
自己点検する。詳細な根拠は CLAUDE.md「LangGraph / LLM エージェント設計方針」
節を参照（本スキルはそれを実装時に使える形にしたもの）。

## 8原則チェックリスト

1. **1エージェント = 1モジュール = 1グラフ** になっているか。
   各子エージェントは自分の `build_graph()` で完結させ、`run()` は
   `graph.ainvoke(new_state(...), config)` を呼ぶだけの薄いラッパにする
   （[company.py](../../../api/app/services/agents/company.py)・
   [market.py](../../../api/app/services/agents/market.py) が実例）。
   共有 `BaseAgent` は作らない（エージェントごとにノード構成が異なるため）。
2. **親と子の責務が分離されているか**。親（[orchestrator.py](../../../api/app/services/agents/orchestrator.py)）
   は「意図判定 → 委任」だけを行い、実処理は子グラフに閉じ込める。親の
   ノードから子グラフを呼ぶときは必ず `ainvoke(state, config)` で呼び、
   `config`（Langfuseコールバック付き）をそのまま渡す（子runが親runに
   ネストするため）。
3. **ノードが小さく単一責務になっているか**。1ノード1目的、名前で役割が
   分かるようにする（`resolve` / `collect` / `analyze` / `report` の
   4ノード構成が company.py / market.py の型）。分岐ロジックはノード内に
   埋め込まず `route_*` のような条件関数に切り出す（`orchestrator.py` の
   `_route` が実例）。
4. **State が `state.py` の1箇所で定義されているか**。新しいフィールドが
   要る場合は `AgentState`（reducer付きTypedDict）にフィールドを足す形で
   拡張し、他のTypedDictをネストしない（langgraphの型解決が壊れるため）。
   エージェント固有の「事実情報」型（`CompanyFacts` / `MarketFacts` 等）は
   state.py に定義してよいが、AgentState 本体へのネストはしない。
5. **LLMアクセスが `runtime.py` の `invoke_llm` 経由か**。直接LLMクライアント
   を呼ばない。失敗時は必ず `fallback` 文字列（ルールベースの
   `rule_based_analysis` 等）を渡し、オフライン/テストでも動くようにする。
6. **副作用（DB・ネットワーク）がノードの外か、明示した収集ノード
   （`_collect` 系）に限定されているか**。純粋な整形・判定ロジック
   （`build_report` / `_facts_to_prompt` 等）はテスト可能な純粋関数として
   切り出す（会話生成部分にDB呼び出しを混ぜない）。
7. **RunnableConfig（Langfuseコールバック付き）がトップで1度組み立てられ、
   親→子へそのまま伝播しているか**。子グラフ呼び出しのたびに新しい
   configを作り直さない。
8. **応答がJob非同期＋ポーリングになっているか**。長時間処理は
   `services/jobs` のジョブとして実行し、進捗は `AgentStep`（phase）で
   表現する（API層の責務。エージェント自体はこれを意識せず、進捗が要る
   場合は呼び出し元がジョブの `progress` を更新する形にする）。

## 新規エージェント追加時の型（company.py / market.py が雛形）

```
resolve/select（対象確定）→ collect（収集・副作用はここに限定）
  → analyze（LLM分析・invoke_llm使用）→ report（整形・純粋関数）
```

- 収集ソースが複数ある場合は `asyncio.gather` で並列取得する
  （`_collect_one` の実例を参照）。
- 外部呼び出しの失敗方針は `backend-workflow` スキルのリトライ/キャッシュ
  節に従う（「失敗＝機能縮退」系はリトライしない、TTLキャッシュは
  `async_ttl_cache`）。
- 新エージェントを親（orchestrator）から呼び出す場合は、意図判定
  （`classify_intent_llm`）とルーティング（`_route`）の追加が必要になる。
  親のノード自体を太らせず、委任ロジックのみ追加する。

## 完了時

- `backend-workflow` スキルの検証コマンド（`uv run pytest -q` /
  `uv run ruff check app/ tests/` / `uv run mypy app/`）を通す。
- 一区切りついたら `git-workflow` スキルに従い commit + push する。
