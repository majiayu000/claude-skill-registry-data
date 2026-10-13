---
name: db-access
description: 本番DB・ローカルDB接続の規約。DBデータを参照・更新する際に必ず確認すること。
---

# DB接続規約

## 重要：ローカルAdminは本番DBに接続済み

ローカルの Admin アプリは `.env.production` を使って**本番 Supabase DB** に接続している。

- 本番 Supabase URL: `https://bdfkjdanycpxtoljxeho.supabase.co`
- 認証情報: `.env.production` を参照（`.gitignore` 対象のため非公開）

## DBを操作する際のルール

- DB の確認・更新は**本番 URL に対して行う**（ローカルの `127.0.0.1` は使わない）
- REST API でアクセスする場合は `.env.production` の `SUPABASE_URL` と `SUPABASE_SERVICE_ROLE_KEY` を使用
- `npx supabase db query` ではなく `curl` + REST API で本番 DB に直接クエリする

## 接続例

```bash
# council_sessions 一覧取得
curl -s "$SUPABASE_URL/rest/v1/council_sessions?select=*" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
```

環境変数は `.env.production` から読み込むか、直接値を参照すること。
