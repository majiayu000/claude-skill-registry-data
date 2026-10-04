---
name: literature-search
version: 1.1.1
description: 研究課題の設定時・文献調査フェーズにおいて、OpenAlex/arXiv/Crossref/Semantic Scholar から多角的論文検索・対立陣営探索・係争ステータス付きマトリクス作成を行うスキル
---

# 多プロバイダー対応 文献自動検索スキル (Multi-Provider Literature Search)

## 目的
設定ファイル [`config/literature_providers.json`](../../../config/literature_providers.json) に定義されたオープンアクセス論文サイト（arXiv, OpenAlex, Crossref, Semantic Scholar 等）から、研究課題に関連する論文を横断検索し、適合度評価を行って `docs/literature/literature-matrix.md` へ自動挿入する。

## 発動タイミング
- 新しい研究テーマ・論文テーマの設定時
- 新しい論点や概念に関連する文献が必要になった時
- 査読者から追加の参考文献を求められた時

通時的論文（概念史・系譜学・制度史等）では、API 検索の前に [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) を発動する。古典デジタルライブラリ・J-STAGE・CiNii などプロバイダー外チャネルは同スキル Step 3。

## 設定によるプロバイダー拡張
`config/literature_providers.json` に新しいAPIエンドポイント（または独自の論文検索サーバー）を追加・有効化/無効化できます：

```json
{
  "default_provider": "openalex",
  "contact_email": "",
  "providers": {
    "openalex": { "name": "OpenAlex", "type": "openalex_json", "base_url": "https://api.openalex.org/works", "enabled": true },
    "arxiv": { "name": "arXiv", "type": "arxiv_atom", "base_url": "https://export.arxiv.org/api/query", "enabled": true },
    "crossref": { "name": "Crossref", "type": "crossref_json", "base_url": "https://api.crossref.org/works", "enabled": true },
    "semanticscholar": { "name": "Semantic Scholar", "type": "semanticscholar_json", "base_url": "https://api.semanticscholar.org/graph/v1/paper/search", "enabled": true }
  }
}
```

OpenAlex / Crossref の polite pool のため、実行者本人の連絡先を環境変数で渡す。git に書かない。`example.com` などのダミーは拒否される。

```bash
export SCHOLARLY_CONTACT_EMAIL="firstname.lastname@university.ac.jp"
export SEMANTIC_SCHOLAR_API_KEY="your-key"   # 任意。Semantic Scholar を頻繁に使う場合
```

未設定・空・ダミーのまま実行すると、スクリプトは HTTP を送らず終了コード 1 で止まり、stderr に設定手順を出す。エージェントはその指示に従い、ユーザーに実メールを確認してから再実行する。

## 実行手順

### Step 1: 検索スクリプトの実行
全プロバイダー横断検索、または特定プロバイダーを指定して実行：

```bash
# 全有効プロバイダーを横断検索 (サブモジュール導入時: python3 .scholarly-agent-skills/scripts/search_literature.py ...)
python3 scripts/search_literature.py --query "hermeneutics AND 'large language models'" --provider all --max-results 5

# OpenAlex（人文学・全領域カバー）を指定検索
python3 scripts/search_literature.py --query "hermeneutics" --provider openalex --max-results 5
```

> [!NOTE]
> サブモジュール導入先のリポジトリから実行する場合は、スクリプトパス頭に `.scholarly-agent-skills/` を付与してください。

### Step 1.5: 対立陣営の探索 (Faction Discovery)

主要な主張・理論（特に本論の屋台骨となるもの）を発見した場合、以下の方法で**対立する査読済み文献を能動的に探索**する：

1. **反証系クエリ**: 主張 X に対して `"X" AND (critique OR criticism OR replication OR "failed to replicate" OR comment OR reply)` 等のクエリで、反論・追試・コメント文献を検索する。
2. **被引用ネットワーク**: 中核文献の被引用先（OpenAlex の `cited_by` 等）から "Comment on" / "Reply to" / Retraction Note / メタ分析・系統的レビューを探す。
3. **撤回・訂正の確認**: 中核文献が Retracted / Expression of Concern 対象でないか確認する（OpenAlex ではタイトルに "RETRACTED ARTICLE" と付く）。撤回済み文献を確立済み知見として扱う事故を防ぐ。
4. **陣営の同定**: 対立が見つかった場合、各陣営の代表文献・提唱者を特定し、マトリクスの「立場・陣営」列に記録する。

> `counter-argument-tdd` の想定反論は「想像の反論」に依存する。本ステップは「実在の反論」を文献から発掘し、査読対策・断定トーン調整・新規性の位置づけの根拠にする。

### Step 2: 論文の構造化とマトリクス反映
検索結果から適合度が高い論文を `docs/literature/literature-matrix.md` に追記し、`literature-gap-analysis`（先行研究ギャップ分析）へ引き継ぐ。

#### マトリクス記録フォーマット（v1.1.0 拡張）

各文献を以下の列構成で記録する：

```markdown
| # | 文献 | 適合度 | 立場・陣営 | 係争ステータス | 本テーマとの関連 |
```

- **立場・陣営**: 当該文献が属する学派・理論的立場・アプローチ（例: 機能主義的説明／副産物理論、計量実証派／史料批判派）
- **係争ステータス**: 以下のラベルのいずれか
  - `consensus`: 分野内で広く受容されている
  - `replicated`: 独立した追試・再現が存在する
  - `contested`: 対立する査読済み反論・反証が存在する（**本文での併記義務の対象**）
  - `contradicted`: 大規模反証・否定的メタ分析が存在する（**断定引用は不可**）
  - `retraction-watch`: 撤回・訂正・懸念表明（Expression of Concern）の監視対象
  - `unknown`: 未調査（デフォルト。本論の屋台骨となる主張は Step 1.5 で調査してから記入）

> `claim-evidence-gate` の Field Disagreement 軸は本列を参照して断定トーンの妥当性を判定する。

## 成果物
- `docs/literature/literature-matrix.md` (検索結果・適合度評価マトリクス)

