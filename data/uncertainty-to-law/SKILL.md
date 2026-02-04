---
name: uncertainty-to-law
description: |
  resolving-uncertaintyで検証された仮説をLDE（Law-Driven Engineering）のLawに昇格させるスキル。
  検証済みの不確実性からビジネス上の「守るべき条件」を抽出し、Law Catalogに追加する。
  使用タイミング: (1) 仮説が検証された後のLaw化、(2) 「検証結果をLawにして」、
  (3) 複数セッションで確認されたパターンの正式化、(4) 障害対応後の再発防止策のLaw化
---

# Uncertainty to Law

検証済みの不確実性（仮説）をLawに昇格させる。

## 昇格条件

仮説がLawに昇格するための条件：

| 条件 | 説明 | 必須 |
|------|------|------|
| Validated | 観測タスクで検証済み | ✅ |
| Reproducible | 複数回/セッションで再確認 | ✅ |
| Impactful | ビジネス影響度 ≥ 3 | ✅ |
| Enforceable | 検証・観測手段が定義可能 | ✅ |
| Documented | 証拠が記録されている | ✅ |

## 昇格プロセス

### Step 1: 検証済み仮説の収集

```yaml
# resolving-uncertainty の出力から抽出
validated_hypotheses:
  - id: U-001
    hypothesis: "在庫更新は原子的に行う必要がある"
    status: Validated
    evidence: "並行テストで競合条件を確認"
    impact: 4
    sessions_confirmed: 3

  - id: U-002
    hypothesis: "注文数量は在庫を超えてはならない"
    status: Validated
    evidence: "本番ログで47件の違反を確認"
    impact: 5
    sessions_confirmed: 2
```

### Step 2: Law Type判定

| 仮説の性質 | Law Type | 判定基準 |
|-----------|----------|---------|
| 常に成り立つべき条件 | Invariant | 状態に関する制約 |
| 操作の前提条件 | Pre | 入力に関する制約 |
| 操作の結果保証 | Post | 出力に関する制約 |
| 状況依存の判断規則 | Policy | 条件分岐を含む |

### Step 3: Law Card生成

検証済み仮説からLaw Cardを生成：

```yaml
law_card_draft:
  id: LAW-<domain>-<name>
  type: <判定されたType>
  scope: <適用範囲>
  statement: <仮説を法則形式に変換>
  formal_ish: <疑似式>

  evidence:
    source: <証拠の出典>
    validation_method: <検証方法>
    confirmed_in: <確認セッション数>

  verification:
    test: <テスト案>
    runtime_check: <実行時チェック案>

  observability:
    telemetry: <メトリクス案>
    log_event: <イベント案>
```

### Step 4: レビュー・正式化

1. 生成されたLaw Card案を人間がレビュー
2. `/lde-law-card` で正式なLaw Cardとして作成
3. Law CatalogとGrounding Mapを更新
4. pce-memoryに昇格履歴を記録

## 変換パターン

### 仮説 → Law変換例

**仮説**: 「在庫更新は原子的に行う必要がある」
**↓**
```markdown
## LAW-inv-atomic-update
- Type: Invariant
- Scope: inventory.updateStock
- Statement: 在庫更新は単一トランザクション内で完結し、中間状態が外部から観測されない
- Formal-ish: ∀t: visible(stock(t)) ∈ {before, after} (not intermediate)
```

**仮説**: 「VIPユーザーは在庫切れでも予約できる」
**↓**
```markdown
## LAW-policy-vip-backorder
- Type: Policy
- Scope: order.create
- Statement: VIPユーザー（tier >= gold）は利用可能在庫を超えてバックオーダー可能
- Formal-ish: if (user.tier >= gold) then orderQty > available is allowed
```

## 出力形式

### 昇格レポート

```markdown
# Uncertainty to Law Report

## 昇格候補

### U-001 → LAW-inv-atomic-update (推奨: 昇格)

**元の仮説**: 在庫更新は原子的に行う必要がある
**検証状態**: ✅ Validated
**証拠**: 並行テストで競合条件を確認 (tests/concurrent.test.ts)
**影響度**: 4/5
**確認セッション**: 3回

**生成Law Card**:
- Type: Invariant
- Scope: inventory.updateStock
- Statement: 在庫更新は単一トランザクション内で完結
- Severity案: S1

**接地案**:
- Test: prop_atomic_update (PBT)
- Runtime: トランザクション境界アサーション
- Telemetry: law.inventory.atomic_update.*

→ `/lde-law-card` で正式化しますか？

### U-003 (昇格保留)

**元の仮説**: キャンセルは24時間以内のみ可能
**検証状態**: Partially Validated
**理由**: ビジネス要件の確認が必要（例外ケースの扱い）

→ 追加の観測タスクを作成しますか？
```

## pce-memory連携

### 昇格履歴の記録

```
pce_memory_upsert:
  category: law_promotion
  content: |
    U-001 → LAW-inv-atomic-update
    - 昇格日: 2024-12-21
    - 元仮説: 在庫更新は原子的に行う必要がある
    - 検証方法: 並行テスト
    - 証拠: tests/concurrent.test.ts
  tags: ["law-promotion", "uncertainty", "inventory"]
```

### 過去の昇格パターン参照

```
pce_memory_activate:
  tags: ["law-promotion"]

# 類似の昇格事例を検索して参考にする
```

## 使用例

```
User: さっき検証した仮説をLawにして

Claude:
## Uncertainty to Law実行中...

### 検証済み仮説の収集
resolving-uncertaintyの結果から3件のValidated仮説を検出

## 昇格候補分析

### 1. U-001 → LAW-inv-atomic-update ✅ 昇格推奨

**元の仮説**: 在庫更新は原子的に行う必要がある
**検証**: ✅ Validated (並行テストで確認)
**影響度**: 4/5
**セッション**: 3回確認

**Law Card案**:
- Type: Invariant
- Severity: S1
- Statement: 在庫更新は単一トランザクション内で完結

### 2. U-002 → LAW-pre-order-limit ✅ 昇格推奨
...

### 3. U-003 ⚠️ 昇格保留
**理由**: ビジネス要件の最終確認が必要

---

昇格を進めますか？
1. すべて昇格（2件）
2. 個別に確認
3. 保留項目の追加観測タスク作成
```
