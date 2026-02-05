---
name: eld-model-law-card
description: |
  LDE（Law-Driven Engineering）のLaw Card作成スキル。
  ビジネス上の「守るべき条件」を標準フォーマットで文書化する。
  使用タイミング: (1) 新しいLawを追加する時、(2) 既存Lawを更新する時、
  (3) Law Catalogに新規エントリを追加する時、(4) Grounding Mapを更新する時
---

# LDE Law Card作成

## Law分類

| 種別 | 定義 | 例 |
|------|------|-----|
| **Invariant** | どの状態でも常に成り立つ条件（状態制約） | `available = total - reserved` |
| **Pre** | 操作を受け付けるための条件（入力制約） | `orderQty ≤ available` |
| **Post** | 操作後に必ず成り立つ条件（出力制約） | `reserved' = reserved + orderQty` |
| **Policy** | 裁量・例外・外部状況を含む判断規則 | 「VIPは上限緩和」 |

### 分類時の注意

- **Invariant**: 「本当は手続き依存」なのにInvariantと言い張ると事故る
- **Pre**: UI/API境界でまず守る
- **Post**: 並行時の意味（同時実行）を別途定義することがある
- **Policy**: 純粋関数に落とすなら環境（Context）を入力化する

## Law Cardテンプレート

```md
## LAW-<domain>-<name> (ID)
- Type: Invariant | Pre | Post | Policy
- Scope: <module/usecase/endpoint/job>
- Statement: <自然言語 1〜3行>
- Formal-ish: <疑似式 / 型 / predicate（任意だが曖昧さ削減に有効）>

- Terms (required):
  - <このLawが参照するTerm ID。最低1つ必須>
  - 例: TERM-inventory-available, TERM-order-quantity

- Exceptions:
  - <例外条件と理由。無ければ "None">

- Violation Handling:
  - Severity: S0|S1|S2|S3
  - When Violated: reject | compensate | warn | quarantine | audit
  - Owner: <責任者/チーム>

- Verification (at least one):
  - Test: <unit/property/test-case>
  - Runtime Check: <assertion/guard>

- Observability (at least one):
  - Telemetry: law.<domain>.<law_name>.(applied|violated|latency_ms|coverage)
  - Log/Event: <event name / fields>
```

## 相互拘束ルール

- **Lawは孤立禁止**: すべてのLawは最低1つのTermを参照する必要がある
- **Terms参照はLink Mapと連動**: `/lde-link-map` で Law ↔ Term の関係を管理

## Severity（重要度）

| レベル | 説明 |
|--------|------|
| **S0** | ビジネス停止レベル |
| **S1** | 重大な機能障害 |
| **S2** | 部分的な機能劣化 |
| **S3** | 軽微・改善レベル |

## 作成手順

1. **Law同定**: ビジネス上の「守るべき条件」を特定
2. **分類**: Invariant / Pre / Post / Policy のいずれかに分類
3. **Scope定義**: 適用範囲（モジュール/エンドポイント/ジョブ）を明確化
4. **Statement記述**: 自然言語で1〜3行で記述
5. **Terms紐付け**: このLawが参照するTermを明示（最低1つ必須）
6. **Exceptions定義**: 例外条件があれば明記
7. **Handling決定**: Severity + 違反時動作 + Owner
8. **Verification設定**: Test または Runtime Check を最低1つ
9. **Observability設定**: Telemetry または Log/Event を最低1つ
10. **Link Map更新**: `/lde-link-map` で Law ↔ Term の関係を記録
11. **Grounding Map更新**: Law ↔ Test ↔ Telemetry の対応を記録

## 実例：在庫の不変条件

```md
## LAW-inv-available-balance
- Type: Invariant
- Scope: `inventory.reserveStock` / `inventory.releaseStock`
- Statement: 利用可能在庫は総在庫から予約済み在庫を引いた値に等しい
- Formal-ish: `∀t: available(t) = total(t) - reserved(t)`

- Terms:
  - TERM-inventory-available（利用可能在庫）
  - TERM-inventory-total（総在庫）
  - TERM-inventory-reserved（予約済み在庫）

- Exceptions:
  - None

- Violation Handling:
  - Severity: S1
  - When Violated: quarantine（出荷停止）| audit（反例保存）
  - Owner: inventory-team

- Verification:
  - Test: `prop_inventory_balance` (PBT)
  - Runtime Check: `assert_balance()` in post-commit hook

- Observability:
  - Telemetry: `law.inventory.available_balance.violated_total`
  - Log/Event: `inventory.balance.violation` with `{expected, actual, diff}`
```

## 実例：注文数量の事前条件

```md
## LAW-pre-order-quantity
- Type: Pre
- Scope: `order.create` API
- Statement: 注文数量は利用可能在庫を超えてはならない
- Formal-ish: `orderQty ≤ available`

- Terms:
  - TERM-order-quantity（注文数量）
  - TERM-inventory-available（利用可能在庫）

- Exceptions:
  - バックオーダー許可商品は例外（Policy LAW-policy-backorder 参照）

- Violation Handling:
  - Severity: S2
  - When Violated: reject（400 Bad Request）
  - Owner: order-team

- Verification:
  - Test: `test_order_quantity_exceeds_available`
  - Runtime Check: Zod schema validation

- Observability:
  - Telemetry: `law.order.quantity_limit.violated_total`
  - Log/Event: `order.validation.failed` with `{orderQty, available}`
```

## Law Catalog更新

Law Card作成後、Law Catalogに追加：

```md
| ID | Type | Scope | Severity | Owner | Status |
|----|------|-------|----------|-------|--------|
| LAW-inv-available-balance | Invariant | inventory.* | S1 | inventory-team | Active |
| LAW-pre-order-quantity | Pre | order.create | S2 | order-team | Active |
```

## Grounding Map更新

```md
| Law ID | Type | Test | Runtime Check | Telemetry | Notes |
|--------|------|------|---------------|-----------|-------|
| LAW-inv-available-balance | Invariant | prop_inventory_balance | assert_balance | law.inventory.* | - |
| LAW-pre-order-quantity | Pre | test_order_quantity | Zod validation | law.order.* | - |
```
