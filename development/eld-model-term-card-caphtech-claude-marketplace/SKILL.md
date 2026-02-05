---
name: eld-model-term-card
description: |
  LDE（Law-Driven Engineering）のTerm Card作成スキル。
  ドメインの語彙（Vocabulary）を標準フォーマットで文書化し、名辞抽象を具体化する。
  使用タイミング: (1) 新しいTermを追加する時、(2) 既存Termを更新する時、
  (3) Vocabulary Catalogに新規エントリを追加する時、(4) Phase Dでカード化する時
---

# LDE Term Card作成

## Term分類

| 種別 | 定義 | 例 |
|------|------|-----|
| **Term（用語）** | ビジネス上の概念・名詞 | 「利用可能在庫」「注文」 |
| **Type（型）** | 技術的な型・構造 | `OrderId`, `Quantity` |
| **Value（値制約）** | 値の範囲・形式 | `1 ≤ qty ≤ 100` |
| **Context（文脈）** | 用語が使われる文脈 | 「在庫管理」「注文処理」 |

### 分類時の注意

- **Term**: 「言葉」ではなく「運用単位」として定義する
- **Type**: Brand/Newtype/ADTで意味的区別を強制
- **Value**: 境界での検証・正規化を必須化
- **Context**: 同じ言葉でも文脈で意味が変わる場合を明確化

## Term Cardテンプレート

```md
## TERM-<domain>-<name> (ID)

### 基本情報
- Meaning: <定義（1〜2文）>
- Context: <使用される文脈・ドメイン>
- Synonyms: <同義語があれば列挙>
- Non-goals: <この用語が意味しないもの>

### 型・形状
- Type/Shape: <技術的な型表現>
- Constraints: <値制約>
- Example Values: <具体例>

### 境界と接地
- IO Boundaries: <どこで入力/出力されるか>
- Validation: <境界での検証方法>
- Normalization: <正規化処理>
- Observable Fields: <ログ/テレメトリで観測するフィールド>

### 関連Law
- Related Laws (at least one for S0/S1 Terms):
  - <関連するLaw ID>
```

## 相互拘束ルール

- **重要Termは孤立禁止**: S0/S1 TermはRelated Lawsを最低1つ持つ
- **Related LawsはLink Mapと連動**: `/lde-link-map` で Term ↔ Law の関係を管理

## 作成手順

1. **Term同定**: ドメインで使う語彙を特定
2. **分類**: Term / Type / Value / Context に分類
3. **Meaning記述**: 定義を1〜2文で明確に記述
4. **Context定義**: どの文脈で使われるかを明確化
5. **Type/Shape定義**: 技術的な型表現を決定
6. **Boundaries定義**: IO境界での検証・正規化を設計
7. **Observable Fields設定**: ログ/テレメトリで観測するフィールド
8. **Related Laws紐付け**: 関連するLawを明示（S0/S1は必須）
9. **Link Map更新**: `/lde-link-map` で Term ↔ Law の関係を記録

## 実例：利用可能在庫

```md
## TERM-inventory-available

### 基本情報
- Meaning: 現時点で注文に割り当て可能な在庫数量
- Context: 在庫管理、注文処理
- Synonyms: 有効在庫、販売可能在庫
- Non-goals: 物理的な在庫数（予約済みを含む）

### 型・形状
- Type/Shape: `AvailableStock = Brand<number, 'AvailableStock'>`
- Constraints: `available ≥ 0`, `available ≤ total`
- Example Values: 0, 50, 1000

### 境界と接地
- IO Boundaries:
  - Input: 在庫API、管理画面
  - Output: 注文API、商品詳細
- Validation: `z.number().nonnegative().max(MAX_STOCK)`
- Normalization: 小数点以下切り捨て
- Observable Fields: `inventory.available`, `inventory.available_diff`

### 関連Law
- Related Laws:
  - LAW-inv-available-balance（利用可能在庫の計算式）
  - LAW-pre-order-quantity（注文数量上限）
```

## 実例：注文数量

```md
## TERM-order-quantity

### 基本情報
- Meaning: 1回の注文で指定される商品数量
- Context: 注文処理
- Synonyms: 購入数量、オーダー数
- Non-goals: カート内の合計数量

### 型・形状
- Type/Shape: `OrderQuantity = Brand<number, 'OrderQuantity'>`
- Constraints: `1 ≤ qty ≤ 100`
- Example Values: 1, 5, 10

### 境界と接地
- IO Boundaries:
  - Input: 注文API、購入画面
  - Output: 確認画面、注文履歴
- Validation: `z.number().int().min(1).max(100)`
- Normalization: 整数化（Math.floor）
- Observable Fields: `order.quantity`, `order.total_items`

### 関連Law
- Related Laws:
  - LAW-pre-order-quantity（注文数量上限）
  - LAW-policy-bulk-order（大量注文ポリシー）
```

## Vocabulary Catalog更新

Term Card作成後、Vocabulary Catalogに追加：

```md
| ID | Meaning | Context | Type | Owner | Status |
|----|---------|---------|------|-------|--------|
| TERM-inventory-available | 利用可能在庫 | 在庫管理 | S1 | inventory-team | Active |
| TERM-order-quantity | 注文数量 | 注文処理 | S2 | order-team | Active |
```

## よくある失敗パターン

### 名辞インフレ（Term/型だけ増える）
- **症状**: Term/型が増えるがRelated Lawsが空
- **対策**: S0/S1 TermはRelated Lawsを必須化

### 型の過信
- **症状**: Brand/Newtypeがあるが境界検証が薄い
- **対策**: IO BoundaryとValidationを必須化

## 品質チェック

| チェック項目 | 確認内容 |
|-------------|---------|
| 意味明確性 | Meaningが1〜2文で明確か |
| 境界定義 | IO Boundariesが具体的か |
| 検証実装 | Validationが実装されているか |
| 観測可能 | Observable Fieldsが設定されているか |
| Law紐付け | S0/S1 TermにRelated Lawsがあるか |
