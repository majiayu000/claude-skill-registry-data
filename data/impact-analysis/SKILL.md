---
name: impact-analysis
description: |
  コード変更の影響範囲分析スキル。変更が引き起こし得る影響を影響面（code/interface/data/external/config/runtime/security/observability）ごとに整理し、「どこをレビューし、何をテストし、何を観測すべきか」を根拠つきで提示する。

  トリガー条件:
  - 「影響範囲を分析して」「この変更の影響は？」「どこまで波及する？」
  - PRレビュー依頼時、リファクタ/仕様変更時
  - 障害対応で「原因箇所の周辺影響」を確認したい時

  注意: 変更の是非の最終判断は行わない。実行時にしか分からない挙動は推定と不確実性を提示する。
---

# Impact Analysis（影響範囲分析）

コード変更（差分・設計変更・設定変更）が引き起こし得る影響を、影響面ごとに漏れにくく整理し、「どこをレビューし、何をテストし、何を観測すべきか」を**根拠つき**で提示する。

## Non-Goals（このスキルがやらないこと）

- 変更の是非の最終判断（意思決定は人間が行う）
- 実行時にしか分からない挙動の断定（断定ではなく推定と不確実性を提示）
- すべてのファイルを無差別に列挙（探索境界と優先度ルールに従う）

## 設計原則

| 原則 | 説明 |
|------|------|
| **Traceability** | 各impactに根拠（参照種別・該当箇所）を付ける |
| **Uncertainty-aware** | 静的に断定できない影響は "推定" として出す |
| **Surface-based** | 呼び出し関係＋公開IF＋データ＋設定＋外部＋非機能を同列に扱う |
| **Actionable** | テスト/観測/ロールアウトまで落とし込む（根拠とセット） |
| **Bounded** | 探索の深さ/優先ルールを定義し、境界を明示 |

## 入力

```yaml
impact_analysis_input:
  change_set:
    diff: optional<string>           # 可能ならdiff
    changed_files: optional<list>    # 変更ファイル一覧
    commit_or_pr: optional<string>   # コミットSHA or PR番号
    change_summary: optional<string> # 変更の説明

  target:                            # 指定があれば優先
    - file: optional<string>
      symbol: optional<string>
      kind: optional<function|class|method|module|endpoint|sql|config>
      location: optional<string>     # "path:line"

  context:
    language: optional<string>       # ts/go/java...
    framework: optional<string>      # express/nest/next...
    architecture: optional<string>   # monolith/microservices...
    entrypoints_hint: optional<list> # routes, handlers, jobs
    risk_profile: optional<string>   # "auth/payment" 等の重要領域
    constraints:
      max_graph_depth: optional<int> # default 3
      max_items_per_section: optional<int> # default 20
```

## 出力

詳細なスキーマは [references/output-schema.md](references/output-schema.md) を参照。

### 出力構造概要

```yaml
impact_analysis:
  meta:
    schema_version: "2.0"
    confidence:
      overall: 0.0-1.0
      notes: ["静的解析で追えないDIがある"]

  change_overview:
    summary: "<何が変わるか>"
    change_type: <behavior_change|refactor|bugfix|perf|security|config|data_migration|unknown>
    risk_domain_tags: ["auth", "session"]
    blast_radius_hint: <local|module|service|system|unknown>

  targets: [...]           # 変更対象のエンティティ

  impacts:
    code:                  # 呼び出し関係
      direct: [...]
      transitive: [...]
    interface:             # 公開IF・契約
      exports: [...]
      api_endpoints: [...]
    data:                  # データストア
      stores: [...]
    external:              # 外部依存
      dependencies: [...]
    config:                # 設定・環境
      items: [...]
    runtime_quality:       # 性能・可用性
      performance: [...]
      availability: [...]
    security_privacy:      # セキュリティ
      concerns: [...]

  risk_assessment:         # リスク評価（因子ベース）
    overall:
      level: <high|medium|low>
      score: 0-100
    applied_factors: [...]
    matrix: {high: N, medium: N, low: N}

  recommended_verification:  # 検証計画
    tests_to_run: [...]
    tests_to_add_or_update: [...]
    rollout_and_safety: [...]

  observation_plan:          # 観測計画
    logs: [...]
    metrics: [...]
    traces: [...]

  unknowns_and_assumptions:  # 不確実性
    unknowns: [...]
    assumptions: [...]
    suggested_followups: [...]
```

## 影響面（Impact Surfaces）

詳細は [references/impact-surfaces.md](references/impact-surfaces.md) を参照。

### 8つの影響面

| 影響面 | 説明 | 分析対象 |
|--------|------|----------|
| `code` | 呼び出し関係 | caller/callee/importer/override/implements |
| `interface` | 公開IF・契約 | export/API/イベント/型 |
| `data` | データストア | DB/キャッシュ/ファイル |
| `external` | 外部依存 | 外部API/SaaS/メッセージング |
| `config` | 設定・環境 | env/feature flag/権限/timeout |
| `runtime_quality` | 性能・可用性 | レイテンシ/障害時挙動 |
| `security_privacy` | セキュリティ | 認証/認可/PII/インジェクション |
| `observability` | 観測性 | ログ/メトリクス/トレース |

## リスク評価

詳細は [references/risk-scoring.md](references/risk-scoring.md) を参照。

### スコアリング因子

| 因子 | 重み | 説明 |
|------|------|------|
| `security_critical_path` | 25 | 認証/認可/決済等のクリティカルパス |
| `data_write` | 20 | データ書き込み・更新・削除 |
| `public_interface_change` | 15 | 公開APIや型の変更 |
| `fanout_large` | 10 | 多数の呼び出し元がある |
| `low_test_coverage` | 15 | テストカバレッジが低い |
| `unknowns_present` | 15 | 静的解析で追えない経路がある |

### リスクレベル

| score | level |
|-------|-------|
| 70-100 | high |
| 40-69 | medium |
| 0-39 | low |

## 処理フロー

### Step 1: 入力の正規化

diff/変更ファイル/説明/ターゲットを統合し「変更集合」を作る。

### Step 2: ターゲット抽出

変更箇所からシンボル・公開IF・設定キー・SQLを候補化。

### Step 3: 依存グラフ探索（複線）

- 呼び出しグラフ（caller/callee）
- import/型依存（type_depends）
- ルーティング・ミドルウェア・DIなど"ランタイム経路"の推定

### Step 4: 副作用・データフロー分析

DB操作、キャッシュ、メッセージング、外部API、ファイルI/O。

### Step 5: 影響面ごとに分類

8つの影響面（code/interface/data/external/config/runtime/security/observability）に分類。

### Step 6: 根拠と確度付与

各impactに根拠（evidence）と確度（confidence）を付与。断定可能か推定かを明確化。

### Step 7: リスク評価

定義済み因子でスコア化し、上位因子を説明可能な形で出す。

### Step 8: 検証計画

テスト（層・優先度・目的）、ロールアウト安全策、観測プランへ接続。

### Step 9: 探索境界の明示

深さ上限、列挙上限、解析不能領域（unknowns）を必ず出す。

## 根拠（Evidence）の記載

各impactには必ず根拠を付与する。

```yaml
impact:
  ref: "src/middleware/auth.ts:45"
  relation: "caller"
  risk_level: "high"
  confidence: 0.85
  evidence:
    - "authenticateUser() を直接呼び出している"
    - "import { authenticateUser } from '../auth/login'"
```

### 関係タイプ（relation）

| relation | 説明 |
|----------|------|
| `caller` | 対象を呼び出している |
| `callee` | 対象から呼び出されている |
| `importer` | 対象をimportしている |
| `override` | 対象をオーバーライドしている |
| `implements` | 対象インターフェースを実装 |
| `type_depends` | 型として依存 |
| `route_maps_to` | ルーティングで対応 |
| `di_binds_to` | DIでバインド |

## 不確実性の明示

静的解析で追えない影響は必ずunknownsに記載。

```yaml
unknowns_and_assumptions:
  unknowns:
    - "動的ディスパッチによる呼び出し経路が追跡不能"
    - "文字列ベースのルーティングで静的解析不可"
    - "設定値依存の分岐は実行時まで不明"

  assumptions:
    - "DIコンテナの設定は本番と同一と仮定"
    - "Feature Flagは全てONと仮定"

  suggested_followups:
    - "DIバインディング設定の確認"
    - "実行時ログで呼び出し経路を確認"
```

## ガードレール

1. **根拠なしのimpactを出さない**: 必ずevidenceを付与
2. **過剰確信の禁止**: 静的解析の限界を認め、confidence/unknownsで表現
3. **探索境界の明示**: max_graph_depthを超えた探索は行わない
4. **網羅より精度**: 大量列挙より、根拠のある影響を優先

## 使用例

```
User: この変更の影響範囲を分析して
[diff: src/auth/login.ts の修正]

Claude:
## Impact Analysis

### Change Overview
- summary: "認証関数のnullチェック追加"
- change_type: bugfix
- risk_domain_tags: ["auth", "session"]
- blast_radius_hint: module

### Targets
| file | symbol | kind | role |
|------|--------|------|------|
| src/auth/login.ts | authenticateUser | function | modified |

### Impacts

#### Code (Direct)
| ref | relation | risk | confidence | evidence |
|-----|----------|------|------------|----------|
| src/middleware/auth.ts:45 | caller | high | 0.90 | authenticateUser()を直接呼び出し |
| src/api/session.ts:23 | caller | medium | 0.85 | ログイン時にセッション作成 |

#### Data
| store | entity | operation | risk | evidence |
|-------|--------|-----------|------|----------|
| postgres | users | read | medium | SELECT FROM users |
| redis | sessions | write | high | セッション書き込み |

### Risk Assessment
- overall: medium (score: 55)
- applied_factors:
  - security_critical_path: 25 (認証フロー)
  - data_write: 20 (セッション書き込み)
  - unknowns_present: 10 (DI経路)

### Recommended Verification
| test | layer | priority | purpose |
|------|-------|----------|---------|
| login.test.ts | unit | p0 | nullケースのカバー |
| auth.integration.ts | integration | p0 | E2Eログインフロー |

### Unknowns
- "DIコンテナ経由の呼び出しは静的解析不可"
- "Feature Flag状態による分岐は実行時依存"
```

## リファレンス

- [references/output-schema.md](references/output-schema.md) - 完全な出力スキーマ
- [references/impact-surfaces.md](references/impact-surfaces.md) - 影響面の詳細定義
- [references/risk-scoring.md](references/risk-scoring.md) - リスクスコアリング詳細
- [references/relation-types.md](references/relation-types.md) - 関係タイプ一覧
