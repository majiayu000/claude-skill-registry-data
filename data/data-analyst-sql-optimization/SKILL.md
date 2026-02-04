---
name: data-analyst-sql-optimization
description: |
  Apply SQL optimization patterns including index usage, query rewriting, JOIN optimization, and window functions. Use when improving query performance or analyzing slow queries.

  This skill provides comprehensive SQL optimization patterns and best practices:
  - N+1 query elimination
  - Index optimization strategies
  - JOIN vs subquery performance
  - Window functions for complex aggregations
  - Query execution plan analysis

  Triggers: "optimize SQL", "slow query", "improve performance", "SQL最適化", "クエリ改善", "パフォーマンス向上"
---

# Data Analyst SQL Optimization Skill

## 概要

このSkillは、data-analystエージェントがSQLクエリのパフォーマンスを改善する際に使用します。実績のある最適化パターンとベストプラクティスを提供し、遅いクエリを高速化します。

## 主な機能

1. **最適化パターンライブラリ**: 頻出の最適化パターンをカタログ化
2. **Before/After例**: 実際の改善例を多数掲載
3. **インデックス推奨**: 適切なインデックス戦略の提案
4. **実行計画解析ガイド**: EXPLAINの読み方と改善点の特定

## 使用方法

### 基本的な使い方

1. **遅いクエリを特定**: クエリ実行時間をログで確認
2. **該当する最適化パターンを探す**: reference.mdから適用可能なパターンを選択
3. **クエリを書き換え**: パターンに従ってクエリを最適化
4. **実行計画で検証**: EXPLAINで改善を確認
5. **パフォーマンス測定**: 実行時間の短縮を確認

### トリガーキーワード

以下のキーワードを含むユーザーリクエストで自動起動されます:
- "optimize SQL" / "SQL最適化"
- "slow query" / "遅いクエリ"
- "improve performance" / "パフォーマンス向上"
- "query tuning" / "クエリチューニング"

## 最適化パターン一覧

### 1. N+1クエリ削減
**問題**: ループ内で繰り返しSELECT文を実行
**解決**: JOINまたはサブクエリで1回のクエリに統合

### 2. インデックス活用
**問題**: WHERE句の列にインデックスがない
**解決**: 適切なインデックスを作成

### 3. JOIN最適化
**問題**: 不要な大規模テーブルのJOIN
**解決**: 必要な列のみ取得、結合順序の最適化

### 4. ウィンドウ関数活用
**問題**: 複雑なサブクエリの入れ子
**解決**: ROW_NUMBER(), RANK()等のウィンドウ関数を使用

### 5. DISTINCT削減
**問題**: 不要なDISTINCT使用
**解決**: GROUP BYまたは適切なJOINで代替

### 6. EXISTS vs IN
**問題**: サブクエリでINを使用
**解決**: EXISTSに変更（多くの場合高速）

### 7. LIMIT活用
**問題**: 全件取得後にアプリ側でフィルタ
**解決**: SQLでLIMIT/OFFSETを使用

### 8. 計算列のインデックス
**問題**: WHERE句で関数を列に適用
**解決**: 計算済み列を作成してインデックス

## リファレンス

詳細な最適化パターンとコード例は、以下のファイルを参照してください:
- `reference.md`: 各パターンの詳細説明
- `examples.md`: Before/Afterの実例

## 実装例

### 例1: N+1クエリの削減

**Before**:
```sql
-- ループで実行（N+1クエリ）
SELECT * FROM users WHERE id = ?;  -- N回実行
```

**After**:
```sql
-- 1回のクエリで取得
SELECT u.*, o.order_count
FROM users u
LEFT JOIN (
  SELECT user_id, COUNT(*) as order_count
  FROM orders
  GROUP BY user_id
) o ON u.id = o.user_id;
```

**改善**: N+1回 → 1回のクエリ、大幅な高速化

### 例2: インデックス活用

**Before**:
```sql
SELECT * FROM orders
WHERE created_at > '2023-01-01'
AND status = 'completed';
-- インデックスなし、フルスキャン
```

**After**:
```sql
-- インデックス作成
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- 同じクエリがインデックスを使用
SELECT * FROM orders
WHERE status = 'completed'
AND created_at > '2023-01-01';
-- ORDER BY の順序を逆にしてインデックス効率化
```

**改善**: フルスキャン → インデックススキャン、10倍以上高速化

### 例3: ウィンドウ関数活用

**Before**:
```sql
-- サブクエリの入れ子
SELECT u.name,
  (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
  (SELECT SUM(total) FROM orders o WHERE o.user_id = u.id) as order_total
FROM users u;
-- usersの各行でordersを2回スキャン
```

**After**:
```sql
-- ウィンドウ関数で1回のスキャン
SELECT u.name,
  COUNT(o.id) OVER (PARTITION BY u.id) as order_count,
  SUM(o.total) OVER (PARTITION BY u.id) as order_total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- 1回のJOINで完結
```

**改善**: 2N回スキャン → 1回のJOIN、大幅な高速化

## ベストプラクティス

### DO（推奨）

✅ **EXPLAINで実行計画を確認**: 最適化前後で必ず確認
✅ **インデックスは選択的に作成**: WHERE/JOIN/ORDER BYで使用される列
✅ **必要な列のみSELECT**: SELECT *は避ける
✅ **早期フィルタリング**: WHERE句を最初に適用
✅ **統計情報を更新**: ANALYZE TABLEで最新状態に

### DON'T（非推奨）

❌ **不要なDISTINCT**: データ構造を見直す
❌ **関数をWHERE句の列に適用**: インデックスが使用されない
❌ **過剰なJOIN**: 必要最小限に絞る
❌ **サブクエリの多用**: JOINやウィンドウ関数で代替
❌ **インデックスの作り過ぎ**: INSERT/UPDATEが遅くなる

## パフォーマンス測定

### 改善前後の比較

1. **実行時間測定**:
   ```sql
   -- BigQueryの場合
   SELECT CURRENT_TIMESTAMP();
   -- クエリ実行
   SELECT CURRENT_TIMESTAMP();
   ```

2. **スキャンバイト数確認**:
   - BigQuery: クエリ結果に表示
   - 改善後は大幅に削減されるはず

3. **実行計画比較**:
   ```sql
   EXPLAIN SELECT ...;
   ```

### 目標指標

- **実行時間**: 50%以上削減
- **スキャンバイト数**: 70%以上削減（BigQuery）
- **インデックス使用**: EXPLAINでtype=ref以上

## トラブルシューティング

### Q: 最適化したのに遅い
A: 以下を確認:
- インデックスが実際に使用されているか（EXPLAIN確認）
- 統計情報が最新か（ANALYZE TABLE実行）
- データ量が想定通りか

### Q: どのパターンを適用すべきか分からない
A: 以下の順で確認:
1. EXPLAINで実行計画を確認
2. フルスキャンがあればインデックス作成
3. N+1パターンがあればJOINに統合
4. サブクエリが複雑ならウィンドウ関数検討

### Q: インデックスを作成したら書き込みが遅くなった
A: インデックスの見直しが必要:
- 使用頻度の低いインデックスを削除
- 複合インデックスで統合できないか検討

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約200行）です。詳細な最適化パターンとコード例は別ファイル（reference.md, examples.md）に分離されています。

## 関連リソース

- **reference.md**: 最適化パターン詳細リファレンス
- **examples.md**: Before/After実例集
- **BigQuery公式ドキュメント**: ベストプラクティス
