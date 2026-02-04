---
name: supabase-rls
description: Supabase RLS パフォーマンス最適化。セキュリティ境界と最適化フィルタの区別、および堅牢な関数定義を規定。
metadata:
  short-description: 完全同期版：Supabase RLS 実装規約
---

# Supabase RLS パフォーマンス & ベストプラクティス

このスキルは、Supabase の Row Level Security (RLS) を安全かつ高効率に実装するための「唯一の正解 (SSoT)」を定義します。

## 命名規則・実装ガイドライン

### 1. パフォーマンス最適化

- **インデックス**: `USING` 句で使用されるカラム（`user_id`, `org_id` 等）には必ず B-tree インデックスを作成してください。
- **initPlan (キャッシュ)**: `auth.uid()` 等の JWT 関数を `(SELECT auth.uid())` でラップし、実行計画での値のキャッシュを有効にすることを推奨してください。

### 2. セキュリティ境界の定義

- **重要**: コード上（`SupabaseService` 等）での `.eq()` フィルタは「パフォーマンス最適化とクエリの意図明示」のためであり、**セキュリティ境界は常に RLS 側で担保**されなければなりません。

### 3. SECURITY DEFINER の安全策

- [WARNING] 権限昇格を防ぐため、以下の措置を必須としてください。
  - `SET search_path = public` を明示的に指定する。
  - 関数内での参照は `public.table_name` のように**スキーマ名で修飾**する。
  - **入力検証の使い分け**:
    - **RETURN false**: 値の欠損（NULL 等）や権限のないデータへのアクセスなど、通常の「許可しない」結果として扱える場合に使用。
    - **RAISE EXCEPTION**: セキュリティ上の重大な違反や、予期しない致命的な不正値など、処理を即座に中断すべき場合に使用。

### 4. マイグレーションフロー

- RLS の変更は必ず `supabase/migrations/` 配下に SQL ファイルとして隔離し、ロールバック（`DROP POLICY ...`）の手順をコメントで残してください。

## 安全な実装例

```sql
-- 1. 最適化されたポリシー
CREATE POLICY "Secure item access" ON public.items
  FOR SELECT USING (
    user_id = (SELECT auth.uid())
  );

-- 2. 堅牢な SECURITY DEFINER 関数
CREATE OR REPLACE FUNCTION public.check_access(target_id uuid)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  -- 1. 基本的な入力検証（運用リスク回避のため false を返す）
  IF target_id IS NULL THEN
    RETURN false;
  END IF;

  -- 2. ロジック実行（明示的なスキーマ修飾と initPlan 活用）
  RETURN EXISTS (
    SELECT 1 FROM public.records
    WHERE id = target_id
    AND owner_id = (SELECT auth.uid())
  );
EXCEPTION
  -- 3. 予期せぬ致命的エラーのみ例外を投げる
  WHEN OTHERS THEN
    RAISE EXCEPTION 'Internal security function error: %', SQLERRM;
END;
$$;
```
