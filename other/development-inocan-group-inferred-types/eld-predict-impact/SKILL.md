---
name: eld-predict-impact
description: |
  ELD（Evidence-Loop Development）のPredict（予測）フェーズスキル。
  変更の影響を因果タイプで分類し、段階化戦略と停止条件を確定する。
  「賢く動く」よりも「壊さずに収束する」を優先。
  使用タイミング: (1) 実装前の影響分析、(2) 「影響予測して」「段階化計画を立てて」、
  (3) Phase 2: Designで変更計画を策定する時、(4) 複雑な変更前のリスク評価
---

# ELD Predict Impact

変更の影響を事前に分類・評価し、安全な変更計画を策定する。

## 目的

- **「壊さずに収束する」を最優先**: 賢く動くよりも安全に進める
- 変更の影響を事前に分類・評価
- 安全上限を持った自律編集の設計
- 停止条件の明確化

## 因果タイプ分類

変更の影響を5つのタイプで分類する：

| タイプ | 説明 | リスク | 対策 |
|--------|------|--------|------|
| **互換性** | API/スキーマの破壊 | High | 段階リリース、deprecation |
| **性能** | レスポンスタイム、スループット | Medium | ベンチマーク、負荷テスト |
| **信頼性** | 障害耐性、復旧時間 | High | フェイルセーフ、Circuit Breaker |
| **セキュリティ** | 認証/認可、データ保護 | Critical | セキュリティレビュー |
| **可観測性** | ログ、メトリクス、トレース | Low | 監視設定の確認 |

### リスクマトリクス

```
            影響範囲
         狭い     広い
発   低  [Low]   [Medium]
生
確   高  [Medium] [High/Critical]
率
```

## 影響予測プロセス

### Step 1: 変更スコープの特定

変更対象を明確化する：

```yaml
change_scope:
  target_files:
    - path: <変更対象ファイル>
      change_type: modify | add | delete
      symbols: [<変更するシンボル>]

  related_laws:
    - <関連するLaw ID>

  related_terms:
    - <関連するTerm ID>
```

### Step 2: 直接影響の分析

このファイル・モジュールの変更による直接的な影響：

```yaml
direct_impact:
  - change: <変更内容>
    causal_type: 互換性 | 性能 | 信頼性 | セキュリティ | 可観測性
    risk: Low | Medium | High | Critical
    affected_components: [<影響を受けるコンポーネント>]
    mitigation: <リスク緩和策>
```

### Step 3: 間接影響の分析

依存先への伝播を追跡：

```yaml
indirect_impact:
  - dependent: <依存先ファイル/モジュール>
    impact_type: <影響内容>
    risk: Low | Medium | High | Critical
    verification: <確認方法（テスト名等）>
```

### Step 4: unknown（未確認）の特定

静的に追跡困難な影響を明示：

```yaml
unknown_impacts:
  - description: <追跡困難な理由>
    possible_risk: <潜在的リスク>
    investigation: <調査方法>
```

**よくあるunknown**:
- DI/IoC経由の呼び出し
- 設定ファイルからの参照
- コード生成による参照
- リフレクションによる呼び出し
- 動的インポート

## 段階化戦略

### 危険度に応じた段階化

```
危険度:    Low → Medium → High → Critical
段階数:     1      2-3      3-5     5+
```

### 段階化の原則

1. **最小単位で変更**: 1ステップ = 1概念の変更
2. **即時検証**: 各ステップ後に静的診断 + テスト
3. **ロールバック可能**: 各ステップで戻せる状態を維持
4. **観測可能**: 各ステップの成功/失敗が検証可能

### 段階化計画テンプレート

```markdown
## 段階化計画

### Step 1: <ステップ名>
- **変更内容**: <具体的な変更>
- **因果タイプ**: <互換性/性能/信頼性/セキュリティ/可観測性>
- **検証方法**: <静的診断/テスト名>
- **成功条件**: <このステップの完了条件>
- **ロールバック**: <戻し方>

### Step 2: <ステップ名>
...

### Step N: 統合検証
- **変更内容**: 全体の統合テスト
- **検証方法**: <統合テスト名>
- **成功条件**: <全体の完了条件>
```

## 停止条件

### 標準停止条件

以下が発生したら**即座に停止**し、追加計測またはスコープ縮小：

#### 1. 予測と現実の継続的乖離
- 想定外のテスト失敗が**3回以上**
- 想定外の依存関係が発見された
- 影響範囲が当初の予測を**50%以上**超過

#### 2. 観測不能な変更の増加
- 物差し（テスト/メトリクス）で検証できない変更が増える
- 「動いているはず」という推測が増える
- Evidence Ladderの低いレベル（L0のみ）が続く

#### 3. ロールバック線の崩壊
- 戻せない変更が発生
- 依存関係が複雑化して部分的な戻しが困難
- データマイグレーションが不可逆に

### カスタム停止条件

Issue Contractで定義した追加の停止条件：

```yaml
custom_stop_conditions:
  - condition: <条件>
    action: <停止時のアクション>
    owner: <責任者>
```

## 反射の選択

変更後の診断結果に応じて、適切な反射を選択：

### 機械反射（自動対応）

即座に修正可能な問題：
- 型エラー → 型を修正
- lint警告 → フォーマット修正
- 未使用変数 → 削除

### 設計反射（判断が必要）

方針決定が必要な問題：
- テスト失敗 → 原因分析と修正方針決定
- 依存関係の問題 → アーキテクチャ検討
- 性能劣化 → 最適化戦略の検討

### 停止反射（ユーザー確認）

停止条件に達した問題：
- セキュリティ脆弱性発見
- 重大な設計変更が必要
- スコープ外の影響が判明

```
軽微な問題 → 機械反射で即修正
中程度の問題 → 設計反射で方針決定
重大な問題 → 停止反射、ユーザーに確認
```

## 出力形式

### Impact Prediction Report

```markdown
# Impact Prediction Report

## Summary

| 項目 | 値 |
|------|-----|
| 変更対象 | <ファイル数> files, <シンボル数> symbols |
| 直接影響 | <件数> components |
| 間接影響 | <件数> dependents |
| 未確認(unknown) | <件数> items |
| リスクレベル | Low / Medium / High / Critical |
| 推奨段階数 | <N> steps |

---

## 変更スコープ

### 対象ファイル
| ファイル | 変更タイプ | 変更シンボル |
|----------|-----------|-------------|
| src/orders/service.ts | modify | `createOrder`, `validateOrder` |
| src/orders/types.ts | modify | `OrderInput` |

### 関連Law/Term
- **Laws**: LAW-pre-order-quantity, LAW-inv-stock-balance
- **Terms**: TERM-order-quantity, TERM-inventory-available

---

## 直接影響

| 変更 | 因果タイプ | リスク | 緩和策 |
|------|-----------|--------|--------|
| createOrder引数変更 | 互換性 | High | 段階リリース |
| バリデーション追加 | 信頼性 | Medium | テスト追加 |

---

## 間接影響

| 依存先 | 影響内容 | リスク | 検証方法 |
|--------|----------|--------|----------|
| src/api/orders.ts | 引数変更の伝播 | High | test_api_orders |
| src/batch/process.ts | 型変更の影響 | Medium | test_batch_process |

---

## 未確認(unknown)

| 説明 | 潜在リスク | 調査方法 |
|------|-----------|----------|
| DI経由の呼び出し | 実行時エラー | 実行時テスト |
| 設定ファイル参照 | 環境依存 | 設定レビュー |

---

## 段階化計画

### Step 1: 型定義の更新 (Low)
- **変更内容**: OrderInput型に新フィールド追加
- **因果タイプ**: 互換性
- **検証方法**: tsc --noEmit
- **成功条件**: 型エラーなし
- **ロールバック**: git checkout -- src/orders/types.ts

### Step 2: バリデーション追加 (Medium)
- **変更内容**: validateOrder関数の強化
- **因果タイプ**: 信頼性
- **検証方法**: npm test -- orders.validation
- **成功条件**: 全テストパス
- **ロールバック**: git checkout -- src/orders/validation.ts

### Step 3: サービス実装 (High)
- **変更内容**: createOrder関数の修正
- **因果タイプ**: 互換性 + 信頼性
- **検証方法**: npm test -- orders.service
- **成功条件**: 全テストパス + カバレッジ80%以上
- **ロールバック**: git checkout -- src/orders/service.ts

### Step 4: 統合検証 (High)
- **変更内容**: E2Eテスト実行
- **検証方法**: npm run test:e2e -- orders
- **成功条件**: 全E2Eテストパス
- **ロールバック**: git revert HEAD~3

---

## 停止条件

### 標準停止条件
- [ ] 想定外のテスト失敗が3回発生
- [ ] ロールバック不可能な状態になった
- [ ] 観測不能な変更が増加

### カスタム停止条件
- [ ] セキュリティ脆弱性が発見された場合
- [ ] 性能が20%以上劣化した場合

---

## 次のアクション

1. [ ] Step 1から順次実行
2. [ ] 各ステップで検証を実施
3. [ ] 停止条件をモニタリング
4. [ ] 完了後 `/eld-ground-check` で接地確認
```

## 失敗パターン（必ず回避）

### 静的整合だけで完了扱い

**NG**: 「型エラーが消えたので完了」
**OK**: 「型エラー解消 + テスト通過 + 影響範囲確認」

### 表層エラーを消すための無理な対応

**NG**:
- 無理なキャスト（`as any`）
- 例外の握り潰し（`catch {}`）
- 警告の無効化（`// @ts-ignore`）

**OK**: 根本原因の解決

### 参照がないから安全と判断

**NG**: 「grep で参照がないから安全」
**OK**: 以下も確認:
- DI/IoC経由の呼び出し
- 設定ファイルからの参照
- コード生成による参照
- リフレクションによる呼び出し

### 物差し不足なのに意味の正しさを断言

**NG**: 「テストはないけど正しく動くはず」
**OK**: 「テストがないため意味の正しさは検証未完了」

## チェックリスト

- [ ] 変更の影響を因果タイプで分類したか
- [ ] 直接影響と間接影響を分析したか
- [ ] unknown（未確認）を明示的にマークしたか
- [ ] 危険度に応じた段階化計画を立てたか
- [ ] 各ステップでロールバック可能か確認したか
- [ ] 停止条件を明確に定義したか
- [ ] 失敗パターンに該当していないか確認したか

## 使用例

```
User: 注文作成機能の変更について影響予測して

Claude:
## Impact Prediction実行中...

### Step 1: 変更スコープ特定
- 対象: src/orders/service.ts (createOrder)
- 関連Law: LAW-pre-order-quantity, LAW-inv-stock-balance
- 関連Term: TERM-order-quantity

### Step 2: 直接影響分析
- API引数変更 → 互換性リスク(High)
- バリデーション強化 → 信頼性向上

### Step 3: 間接影響分析
- src/api/orders.ts → 引数伝播(High)
- src/batch/process.ts → 型変更影響(Medium)

### Step 4: unknown特定
- DI経由呼び出し: 要実行時確認

---

## Impact Prediction Report

### Summary
| 項目 | 値 |
|------|-----|
| リスクレベル | High |
| 推奨段階数 | 4 steps |

### 段階化計画

**Step 1**: 型定義更新 (Low)
**Step 2**: バリデーション追加 (Medium)
**Step 3**: サービス実装 (High)
**Step 4**: 統合検証 (High)

### 停止条件
- 想定外テスト失敗3回
- セキュリティ脆弱性発見

この計画で進めますか？
```

## 関連スキル

- `/eld-model-law-card` - 関連Lawの確認
- `/eld-model-term-card` - 関連Termの確認
- `/eld-ground-check` - 変更後の接地検証
- `/eld-record-collection` - 変更履歴の記録
