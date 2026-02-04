---
name: eld-model-law-discovery
description: |
  コードベースや要件からVocabulary（語彙）とLaw（守るべき条件）を自動発見するスキル。
  名辞抽象（Term/Type）と関係抽象（Law/制約）の両方を抽出し、
  /lde-term-card および /lde-law-card への入力を生成する。
  使用タイミング: (1) 新規プロジェクトでVocabulary/Lawを洗い出す時、
  (2) 既存コードからLaw/Termを抽出する時、(3) 「Lawを発見して」「語彙を抽出して」、
  (4) LDEをレトロフィットする時、(5) Phase A-Bで初期Catalogを作る時
---

# LDE Law/Vocabulary Discovery

コードベースや要件からVocabulary候補とLaw候補を自動発見する。

## 発見の二軸

| 抽象 | 発見対象 | 成果物 |
|------|---------|--------|
| **名辞抽象** | Term/Type/Value/Context | Vocabulary Catalog → Term Card |
| **関係抽象** | Law/制約/写像 | Law Catalog → Law Card |

## Vocabulary発見（名辞抽象）

### 発見ソース

| ソース | 発見対象 | 抽出方法 |
|--------|---------|---------|
| 型定義 | Entity/Value Object | interface/type/classを検索 |
| Zodスキーマ | 値制約 | z.object/z.string等を解析 |
| Brand型 | 意味的区別 | Brand/Newtype定義を検索 |
| ドメインモデル | 概念 | domain/models配下を分析 |
| API定義 | I/O境界の語彙 | Request/Response型を解析 |

### 発見プロセス

#### Step 1: 型・語彙の収集

```bash
# 型定義を検索
grep -r "interface\|type\|class\|Brand" src/
# Zodスキーマを検索
grep -r "z\.object\|z\.string\|z\.number" src/
```

#### Step 2: Term候補生成

```yaml
term_candidate:
  id: TERM-<domain>-<name>
  source:
    file: <発見元ファイル>
    line: <行番号>
  meaning: <推定される意味>
  type_shape: <型表現>
  context: <使用文脈>
  io_boundaries: <I/O境界>
  confidence: high | medium | low
  needs_review: <確認が必要な点>
```

## Law発見（関係抽象）

### 発見ソース

| ソース | 発見対象 | 抽出方法 |
|--------|---------|---------|
| Zodスキーマ | 入力制約 | スキーマ定義を解析 |
| アサーション | 不変条件 | assert/invariant文を検索 |
| テスト期待値 | 事後条件 | expect/assertを解析 |
| catch節 | 例外ポリシー | エラーハンドリングを抽出 |
| ビジネスロジック | ドメインルール | 条件分岐を分析 |
| 障害履歴 | 防御すべき条件 | 過去のバグから抽出 |

### 発見プロセス

#### Step 1: 制約の収集

```bash
# バリデーション・アサーションを検索
grep -r "assert\|invariant\|validate" src/
grep -r "throw new.*Error\|reject\|fail" src/
```

#### Step 2: Law候補生成

```yaml
law_candidate:
  id: LAW-<domain>-<name>
  type: Pre | Post | Invariant | Policy
  source:
    file: <発見元ファイル>
    line: <行番号>
    pattern: <検出パターン>
  statement: <自然言語での記述>
  formal_ish: <疑似式>
  terms: [<関連するTerm候補>]
  confidence: high | medium | low
  needs_review: <確認が必要な点>
```

## パターン分類

### Vocabulary（名辞）パターン

| パターン | Term種別 | 例 |
|---------|----------|-----|
| `interface Entity` | Term（エンティティ） | `interface Order` |
| `type Brand<T>` | Type（ブランド型） | `type OrderId = Brand<string>` |
| `z.number().min().max()` | Value（値制約） | `z.number().min(1).max(100)` |
| `// Context: XXX` | Context（文脈） | コメントから抽出 |

### Law（関係）パターン

| パターン | Law Type | 例 |
|---------|----------|-----|
| `if (!condition) throw` | Pre | 入力検証 |
| `assert(a === b)` | Invariant | 状態整合性 |
| `expect(result).toBe(x)` | Post | 出力保証 |
| `if (role === 'admin')` | Policy | 権限判断 |

## 発見例

### Zodからの抽出

```typescript
// 発見元
const OrderSchema = z.object({
  quantity: z.number().min(1).max(100),
  price: z.number().positive(),
});

// 抽出されるTerm候補
// TERM-order-quantity: 注文数量（1〜100の整数）
// TERM-order-price: 注文価格（正の数）

// 抽出されるLaw候補
// LAW-pre-order-quantity: 1 ≤ quantity ≤ 100
//   Terms: [TERM-order-quantity]
// LAW-pre-order-price: price > 0
//   Terms: [TERM-order-price]
```

### アサーションからの抽出

```typescript
// 発見元
class Inventory {
  reserve(qty: number) {
    assert(this.available >= qty, 'Insufficient stock');
    // ...
    assert(this.available === this.total - this.reserved);
  }
}

// 抽出されるTerm候補
// TERM-inventory-available: 利用可能在庫
// TERM-inventory-total: 総在庫
// TERM-inventory-reserved: 予約済み在庫

// 抽出されるLaw候補
// LAW-pre-reserve-stock: available >= qty
//   Terms: [TERM-inventory-available]
// LAW-inv-available-balance: available = total - reserved
//   Terms: [TERM-inventory-available, TERM-inventory-total, TERM-inventory-reserved]
```

## 出力形式

### Discovery Report

```markdown
# LDE Discovery Report

## Summary
- Vocabulary候補: 12件 (High: 8, Medium: 3, Low: 1)
- Law候補: 15件 (High: 9, Medium: 4, Low: 2)

---

## Vocabulary候補（名辞抽象）

### High Confidence (即座にTerm Card化可能)

#### TERM-order-quantity
- **Source**: src/orders/schema.ts:12
- **Meaning**: 注文数量
- **Type/Shape**: `z.number().min(1).max(100)`
- **Context**: 注文処理
- **Action**: → `/lde-term-card` でカード化

### Medium Confidence (確認推奨)

#### TERM-user-balance (要確認)
- **Source**: src/users/account.ts:45
- **Meaning**: ユーザー残高（推定）
- **Needs Review**: 一時的なマイナスを許可するか確認

---

## Law候補（関係抽象）

### High Confidence (即座にLaw Card化可能)

#### LAW-pre-order-quantity
- **Type**: Pre
- **Source**: src/orders/schema.ts:12
- **Statement**: 注文数量は1以上100以下
- **Formal**: 1 ≤ orderQty ≤ 100
- **Terms**: [TERM-order-quantity]
- **Action**: → `/lde-law-card` で正式化

### Medium Confidence (確認推奨)

#### LAW-inv-user-balance (要確認)
- **Type**: Invariant
- **Source**: src/users/account.ts:120
- **Statement**: ユーザー残高は非負
- **Terms**: [TERM-user-balance]
- **Needs Review**: 一時的なマイナス残高を許可するケースがあるか確認

---

## 相互拘束チェック

### 孤立リスク
- Law候補で参照Termが不明確: 2件
- Term候補で関連Lawがなし: 3件

### 推奨アクション
1. LAW-policy-discount: 参照するTermを明確化
2. TERM-customer-tier: 関連するLawを検討
```

## 既存Catalogとの照合

| チェック | 内容 |
|---------|------|
| 重複検出 | 既存TermやLawと重複していないか |
| 類似統合 | 類似した定義の統合を提案 |
| 矛盾検出 | 既存定義と矛盾していないか |

## 使用例

```
User: このプロジェクトからVocabularyとLawを発見して

Claude:
## LDE Discovery実行中...

### Step 1: ソース収集
- src/配下を走査中...
- 型定義: 35件検出
- バリデーション: 23件検出
- アサーション: 8件検出

### Step 2: Vocabulary候補生成
- Term候補: 12件生成

### Step 3: Law候補生成
- Law候補: 15件生成

### Step 4: 相互拘束チェック
- 孤立リスク: 5件検出

---

## Discovery Report

### High Confidence Vocabulary (8件)
1. TERM-order-quantity → `/lde-term-card`
2. TERM-inventory-available → `/lde-term-card`
...

### High Confidence Laws (9件)
1. LAW-pre-order-quantity → `/lde-law-card`
   Terms: [TERM-order-quantity]
2. LAW-inv-available-balance → `/lde-law-card`
   Terms: [TERM-inventory-available, TERM-inventory-total, TERM-inventory-reserved]
...

Vocabulary CatalogとLaw Catalogを初期化しますか？
```

---

## 品質優先原則（Superpowers統合）

### 核心原則

1. **Epistemic Humility**: 推測を事実として扱わない。`unknown`と言う勇気を持つ
2. **Evidence First**: 結論ではなく因果と証拠を中心にする
3. **Minimal Change**: 最小単位で変更し、即時検証する
4. **Grounded Laws**: Lawは検証可能・観測可能でなければならない
5. **Source of Truth**: 真実は常に現在のコード。要約はインデックス

### 「速さより質」の実践

- 要件の曖昧さによる手戻りを根本から排除
- テストなし実装を許さない
- 観測不能な変更を防ぐ

### 完了の定義

- [ ] Evidence Ladder目標レベル達成
- [ ] Issue Contractの物差し満足
- [ ] Law/Termが接地している（Grounding Map確認）
- [ ] Link Mapに孤立がない
- [ ] ロールバック可能な状態

### 停止条件

以下が発生したら即座に停止し、追加計測またはスコープ縮小：

- 予測と現実の継続的乖離（想定外テスト失敗3回以上）
- 観測不能な変更の増加（物差しで検証できない変更）
- ロールバック線の崩壊（戻せない変更の発生）
