---
name: migrating-supabase
description: |-
  Supabaseマイグレーション作成・実行・修正の包括ガイド。新テーブル作成、カラム追加・変更（ALTER TABLE）、RLSポリシー設計、権限設定（GRANT）、パフォーマンス最適化のベストプラクティスを提供。マイグレーション失敗時のロールバック・修正方法もカバー。「migration」「マイグレーション」「テーブル作成」「カラム追加」「ALTER TABLE」「RLS」「Row Level Security」「Supabase」「データベース」「DB設計」「権限設定」「GRANT」「RLSポリシー修正」「403エラー」に関する作業では必ずこのスキルを参照すること。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Supabase Migration Skill

対象プロジェクトにおけるSupabaseマイグレーションの作成・実行・修正ガイド。

## Quick Start

### 新テーブル作成

```bash
cd supabase
# ファイル名は必ず現在時刻の時分秒まで含める
touch supabase/migrations/$(date +%Y%m%d%H%M%S)_add_table_name.sql
```

[テーブル作成テンプレート](templates/table-creation.md)に従い、以下を**必ず全て**記述:

1. CREATE TABLE
2. インデックス作成（RLSで使うカラム）
3. RLS有効化
4. authenticatedユーザー用ポリシー
5. service_role用ポリシー
6. GRANT ALL TO service_role

### 既存テーブルの変更

```bash
touch supabase/migrations/$(date +%Y%m%d%H%M%S)_alter_table_name.sql
```

→ [カラム追加・変更](#カラム追加変更alter-table) セクション参照

### ローカルでテスト

```bash
# 実際のコマンドは .stdd.config.yml に従う
<commands.db_reset>   # マイグレーション再実行（DBリセット）
<commands.db_types>   # 型定義を再生成（全 apps[] 分）
```

## 主要コマンド

実際のコマンドは `.stdd.config.yml` の `commands.*` に従う。

| 用途 | config キー |
|------|------------|
| DBリセット（migration + seed再実行） | `commands.db_reset` |
| TypeScript型定義生成（全 apps[] 分） | `commands.db_types` |

ローカル環境の起動・停止やフルセットアップ（起動 + 型生成）など、上記以外のプロジェクト固有コマンドは各プロジェクトの npm scripts 等を参照すること。

## ファイル命名規則

**時分秒まで含める**（000000はファイル名衝突の原因になる）:

```
20251225103045_add_user_preferences.sql   -- OK
20251225000000_add_user_preferences.sql   -- NG: 衝突する
```

**プレフィックス**:
- `add_`: テーブル・カラム追加
- `update_`: カラム変更・型変更
- `alter_`: テーブル構造変更
- `create_`: インデックス・関数作成
- `fix_`: RLSポリシー修正・バグ修正
- `drop_`: 削除操作

## 新テーブル作成チェックリスト

```
□ 1. CREATE TABLE（id, user_id, created_at, updated_at, deleted_at を検討）
□ 2. RLSで使うカラムにインデックス作成
□ 3. ENABLE ROW LEVEL SECURITY
□ 4. authenticatedユーザー用RLSポリシー作成
□ 5. service_role用RLSポリシー作成
□ 6. GRANT ALL ON ... TO service_role（忘れると403エラー）
□ 7. `commands.db_reset`（.stdd.config.yml）でエラーなし
□ 8. `commands.db_types`（.stdd.config.yml）で型が生成される
```

詳細は [テーブル作成テンプレート](templates/table-creation.md) を参照。

## カラム追加・変更（ALTER TABLE）

プロジェクトで頻出する変更パターン:

### カラム追加

```sql
-- NULL許容のカラム追加（既存データに影響なし）
ALTER TABLE public.table_name ADD COLUMN new_column TEXT;

-- NOT NULLカラムの追加（既存行にはデフォルト値が入る）
ALTER TABLE public.table_name ADD COLUMN new_column TEXT DEFAULT '' NOT NULL;
```

### カラム名変更

```sql
ALTER TABLE public.table_name RENAME COLUMN old_name TO new_name;
```

### カラム型変更

```sql
ALTER TABLE public.table_name ALTER COLUMN column_name TYPE VARCHAR(20);
```

### カラム削除

```sql
ALTER TABLE public.table_name DROP COLUMN column_name;
```

### ALTER後のチェックリスト

```
□ `commands.db_reset`（.stdd.config.yml）でマイグレーション成功
□ `commands.db_types`（.stdd.config.yml）で型定義が更新される
□ domain/models/ のEntity型を更新
□ domain/repository/ のCRUD関数を更新
□ 関連するServer Action・コンポーネントを確認
□ `commands.typecheck`（.stdd.config.yml）で型チェック
```

## RLSポリシー設計

### 基本パターン: ユーザー所有データ

ユーザーが自分のデータのみアクセスするパターン（users, careers, skills等）:

```sql
-- SELECT: 自分のデータ + 論理削除されていないもの
CREATE POLICY "Users can view own data" ON public.table_name
    FOR SELECT TO authenticated
    USING ((SELECT auth.uid()) = user_id AND deleted_at IS NULL);

-- INSERT/UPDATE/DELETE: 自分のデータのみ
CREATE POLICY "Users can insert own data" ON public.table_name
    FOR INSERT TO authenticated
    WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can update own data" ON public.table_name
    FOR UPDATE TO authenticated
    USING ((SELECT auth.uid()) = user_id AND deleted_at IS NULL)
    WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can delete own data" ON public.table_name
    FOR DELETE TO authenticated
    USING ((SELECT auth.uid()) = user_id AND deleted_at IS NULL);
```

### 公開参照パターン

全ユーザーが参照できるが変更はservice_roleのみ（agents, opportunities等）:

```sql
-- 認証済みユーザーは参照のみ
CREATE POLICY "Authenticated users can view" ON public.table_name
    FOR SELECT TO authenticated
    USING (deleted_at IS NULL);

-- service_roleのみフルアクセス
CREATE POLICY "Service role can manage" ON public.table_name
    FOR ALL TO service_role
    USING (true) WITH CHECK (true);
```

### RLSポリシー修正（DROP + CREATE）

既存のポリシーを変更する場合、ALTER POLICYではなく**DROP→CREATE**パターンを使う:

```sql
-- 旧ポリシーを削除
DROP POLICY IF EXISTS "Old policy name" ON public.table_name;

-- 新ポリシーを作成
CREATE POLICY "New policy name" ON public.table_name
    FOR SELECT TO authenticated
    USING ((SELECT auth.uid()) = user_id AND deleted_at IS NULL);
```

### RLSパフォーマンスの3原則

1. **`auth.uid()`は`(SELECT auth.uid())`でラップ** — 行ごとの関数呼び出しがキャッシュされ10〜50倍高速
2. **RLSで使うカラムにはインデックス必須** — Seq ScanがIndex Scanになり100倍以上高速
3. **クライアント側でもフィルタリング** — `.eq('user_id', userId)`を明示的に追加

詳細は [RLSパフォーマンス最適化ガイド](guides/rls-optimization.md) を参照。

## service_roleとGRANT権限

service_roleでREST API経由（Edge Function、Server Action）でアクセスする場合、**RLSポリシーとGRANT権限の両方**が必要。片方だけでは403エラーになる:

```sql
-- 1. RLSポリシー（アクセス制御のルール）
CREATE POLICY "Service role full access" ON public.table_name
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- 2. GRANT権限（テーブルへの操作権限そのもの）
GRANT ALL ON public.table_name TO service_role;
```

## マイグレーション失敗時の対処

### ローカル環境での失敗

ローカルでは`commands.db_reset`（.stdd.config.yml）がDB全体を再作成するため、SQLを修正して再実行すればよい:

```bash
# 1. マイグレーションファイルのSQLエラーを修正
# 2. リセットして再適用（実際のコマンドは .stdd.config.yml に従う）
<commands.db_reset>
```

### 本番/STG環境で失敗した場合

本番に適用済みのマイグレーションは直接編集できない。**新しいマイグレーションファイル**で修正する:

```bash
# 修正用マイグレーションを作成
touch supabase/migrations/$(date +%Y%m%d%H%M%S)_fix_previous_migration.sql
```

```sql
-- 例: 誤って追加したカラムを削除
ALTER TABLE public.table_name DROP COLUMN IF EXISTS wrong_column;

-- 例: 誤ったRLSポリシーを修正
DROP POLICY IF EXISTS "Wrong policy" ON public.table_name;
CREATE POLICY "Correct policy" ON public.table_name
    FOR SELECT TO authenticated
    USING ((SELECT auth.uid()) = user_id AND deleted_at IS NULL);
```

### デバッグ方法

```sql
-- RLSポリシーの確認
SELECT * FROM pg_policies WHERE tablename = 'your_table_name';

-- RLSが有効か確認
SELECT relname, relrowsecurity FROM pg_class WHERE relname = 'your_table_name';

-- GRANT権限の確認
SELECT grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name = 'your_table_name';
```

詳細は [トラブルシューティングガイド](guides/troubleshooting.md) を参照。

## Entity・Repository更新チェックリスト

DB変更後にアプリケーションコードも更新する:

```
□ domain/models/XXX.ts でEntityを更新
□ domain/repository/XXX.ts のcreateXXX関数を更新
□ domain/repository/XXX.ts のupdateXXX関数を更新
□ 関連するServer Actionを確認
□ `commands.typecheck`（.stdd.config.yml）で型チェック
```

## 参照ファイル

| 参照先 | 読むタイミング |
|--------|--------------|
| [テーブル作成テンプレート](templates/table-creation.md) | 新テーブル作成時 |
| [RLSパフォーマンス最適化](guides/rls-optimization.md) | RLSポリシー設計・パフォーマンス問題時 |
| [トラブルシューティング](guides/troubleshooting.md) | エラー発生時 |

## When NOT to Use This Skill

- **データの参照のみ**: SQLクエリの実行（マイグレーション不要）
- **アプリケーションコードの変更のみ**: DB変更を伴わない場合
- **型定義の修正のみ**: `commands.db_types`（.stdd.config.yml）で自動生成される

## よくあるミス

| ミス | 影響 | 対策 |
|------|------|------|
| インデックス作成忘れ | RLSが遅い | RLSで使うカラムには必ずインデックス |
| `auth.uid()`を直接使用 | パフォーマンス低下 | `(SELECT auth.uid())`でラップ |
| service_roleのGRANT忘れ | 403エラー | RLSポリシーと**両方**設定 |
| 時分秒が000000 | ファイル名衝突 | `$(date +%Y%m%d%H%M%S)`を使用 |
| deleted_at条件の漏れ | 論理削除データが見える | SELECTポリシーに`deleted_at IS NULL`を追加 |
| 本番マイグレーション直接編集 | 適用済みファイルは変更不可 | 新しいfixマイグレーションを作成 |
