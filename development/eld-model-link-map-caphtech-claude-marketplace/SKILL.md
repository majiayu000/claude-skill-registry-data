---
name: eld-model-link-map
description: |
  LDE（Law-Driven Engineering）のLink Map（連結表）管理スキル。
  Law ↔ Term の相互参照関係を可視化し、孤立の検出と影響分析を行う。
  使用タイミング: (1) Law Cardを作成した後、(2) Term Cardを作成した後、
  (3) 「Link Mapを更新して」「孤立チェックして」、(4) 変更影響分析時
---

# LDE Link Map管理

## Link Mapとは

**相互拘束（mutual constraint）** を実現するための連結表。

- **Lawは参照するTermを明示**: 各LawはTerms欄に参照先を記載
- **重要TermはRelated Lawsを保持**: S0/S1 Termは関連Lawを最低1つ持つ
- **孤立禁止**: 孤立Law・孤立Termを検出してアラート

## Link Mapテンプレート

```md
# Link Map

## Law → Term 参照

| Law ID | Type | Terms |
|--------|------|-------|
| LAW-inv-available-balance | Invariant | TERM-inventory-available, TERM-inventory-total, TERM-inventory-reserved |
| LAW-pre-order-quantity | Pre | TERM-order-quantity, TERM-inventory-available |

## Term → Law 逆引き

| Term ID | Importance | Related Laws |
|---------|------------|--------------|
| TERM-inventory-available | S1 | LAW-inv-available-balance, LAW-pre-order-quantity |
| TERM-inventory-total | S1 | LAW-inv-available-balance |
| TERM-inventory-reserved | S2 | LAW-inv-available-balance |
| TERM-order-quantity | S2 | LAW-pre-order-quantity |
```

## 孤立チェック

### 孤立Law検出

Terms欄が空のLawを検出：

```yaml
orphan_check:
  type: orphan_law
  law_id: LAW-xxx
  issue: "Terms欄が空です"
  action: "参照するTermを最低1つ追加してください"
```

### 孤立Term検出

Related Lawsが空のS0/S1 Termを検出：

```yaml
orphan_check:
  type: orphan_term
  term_id: TERM-xxx
  importance: S1
  issue: "Related Lawsが空です"
  action: "関連するLawを追加するか、重要度を見直してください"
```

## 失敗パターン検出

### 名辞インフレ（Noun Inflation）

**症状**: Term/型が増えるがLawが増えない

```yaml
pattern_detection:
  type: noun_inflation
  indicator: "Termが5件以上追加されたがLawが0件"
  terms_added: [TERM-a, TERM-b, TERM-c, TERM-d, TERM-e]
  laws_added: []
  recommendation: "追加したTermに関連するLawを検討してください"
```

### 関係スープ（Relation Soup）

**症状**: Lawは増えるが主要語彙が曖昧

```yaml
pattern_detection:
  type: relation_soup
  indicator: "Lawが5件以上追加されたがTermが1件以下"
  laws_added: [LAW-a, LAW-b, LAW-c, LAW-d, LAW-e]
  terms_added: [TERM-x]
  recommendation: "Lawが参照する語彙を明確化してTermカード化してください"
```

## 影響分析

### Term変更時

```yaml
impact_analysis:
  changed: TERM-inventory-available
  change_type: definition | type | constraint
  affected_laws:
    - LAW-inv-available-balance
    - LAW-pre-order-quantity
  action_required:
    - "各Lawの整合性を確認"
    - "テストを更新"
    - "ドキュメントを更新"
```

### Law変更時

```yaml
impact_analysis:
  changed: LAW-inv-available-balance
  change_type: statement | constraint | exception
  affected_terms:
    - TERM-inventory-available
    - TERM-inventory-total
    - TERM-inventory-reserved
  action_required:
    - "各Termの意味と整合性を確認"
    - "境界検証ロジックを更新"
```

## 更新手順

### Law Card作成後

1. Law CardのTerms欄を確認
2. Link MapのLaw → Term参照表に追加
3. 各TermのRelated Lawsを更新
4. 孤立チェックを実行

### Term Card作成後

1. Term CardのRelated Lawsを確認
2. Link MapのTerm → Law逆引きに追加
3. 各LawのTerms欄を確認（必要なら更新）
4. 孤立チェックを実行

## チェックリスト

### 作成時
- [ ] 新規Lawにはすべて参照Termがある
- [ ] 新規S0/S1 TermにはRelated Lawsがある
- [ ] Link Mapが更新されている

### レビュー時
- [ ] 孤立Lawがない
- [ ] 孤立S0/S1 Termがない
- [ ] 名辞インフレの兆候がない
- [ ] 関係スープの兆候がない

### 変更時
- [ ] 変更Termの影響Lawを列挙した
- [ ] 変更Lawの影響Termを列挙した
- [ ] 影響範囲のテスト更新方針がある

## 使用例

```
User: Link Mapの孤立チェックをして

Claude:
## Link Map孤立チェック実行中...

### Law → Term 参照チェック
- LAW-inv-available-balance: ✅ Terms: 3件
- LAW-pre-order-quantity: ✅ Terms: 2件
- LAW-policy-discount: ❌ **孤立Law検出**
  - Terms欄が空です
  - Action: 参照するTermを追加してください

### Term → Law 逆引きチェック
- TERM-inventory-available (S1): ✅ Laws: 2件
- TERM-inventory-total (S1): ✅ Laws: 1件
- TERM-user-role (S1): ❌ **孤立Term検出**
  - Related Lawsが空です
  - Action: 関連Lawを追加するか重要度を見直してください

### パターン検出
✅ 名辞インフレなし
✅ 関係スープなし

### Summary
- 孤立Law: 1件 (要対応)
- 孤立Term: 1件 (要対応)
```

## 視覚化（参考）

複雑なプロジェクトではグラフで可視化：

```
              ┌─────────────────────────┐
              │    LAW-inv-balance      │
              └──────────┬──────────────┘
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │available │  │  total   │  │ reserved │
    └──────────┘  └──────────┘  └──────────┘
           │
           ▼
    ┌─────────────────────────┐
    │   LAW-pre-order-qty     │
    └─────────────────────────┘
```
