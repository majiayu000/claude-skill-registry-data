---
name: migration-best-practices
description: |
  データベースマイグレーションのベストプラクティス。
  スキーマ変更時に自動適用される。
---

# Database Migration Best Practices

## 命名規則

- ファイル名: `YYYYMMDDHHMMSS_description.sql`
- 例: `20250121120000_add_user_email.sql`

## マイグレーションルール

### UP Migration（適用）
- 必ずトランザクション内で実行
- カラム追加は`NOT NULL`制約に注意（デフォルト値を設定）
- インデックス作成は大規模テーブルでは段階的に

### DOWN Migration（ロールバック）
- すべてのUPに対応するDOWNを必ず用意
- データ損失の可能性がある変更は警告コメント必須

## 禁止事項

- 既存マイグレーションファイルの変更禁止
- 本番環境で直接DDL実行禁止
- カラム削除前にデータ確認必須
