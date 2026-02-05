---
name: arch-review
description: |
  新機能やコード変更時にアーキテクチャの妥当性を検証する。
  簡易DDD構成、レイヤー分離、依存方向の正しさをチェック。
---

# Architecture Review Skill

コード変更時にアーキテクチャの妥当性を検証する。

## レイヤー構成（簡易 DDD）

```text
┌─────────────────────────────────────────────────┐
│              Presentation Layer                 │
│         (app/**/*.tsx - Pages/UI)               │
└────────────────────┬────────────────────────────┘
                     │ 呼び出し可
┌────────────────────▼────────────────────────────┐
│              Application Layer                  │
│      (app/api/**/*.ts - Route Handlers)         │
└────────────────────┬────────────────────────────┘
                     │ 呼び出し可
┌────────────────────▼────────────────────────────┐
│               Domain Layer                      │
│     (src/modules/**/service.ts - Services)      │
└────────────────────┬────────────────────────────┘
                     │ 呼び出し可
┌────────────────────▼────────────────────────────┐
│            Infrastructure Layer                 │
│  (src/db/drizzle.ts, src/lib/auth.ts - DB/Auth) │
└─────────────────────────────────────────────────┘
```

## ディレクトリと責務

| ディレクトリ | 責務 | 配置するもの |
| ----------- | ---- | ----------- |
| `app/(app)/**/*.tsx` | Presentation | ページ、UI コンポーネント |
| `app/api/**/*.ts` | Application | Route Handlers、認可チェック |
| `src/modules/**/` | Domain | サービス、型定義、ビジネスロジック |
| `src/db/` | Infrastructure | スキーマ、DB クライアント |
| `src/lib/` | Infrastructure | 認証、共通ユーティリティ |
| `src/components/` | Presentation | 共通 UI コンポーネント |
| `src/hooks/` | Presentation | カスタムフック |

## 検証チェックリスト

### 1. レイヤー違反がないか

- [ ] Presentation → Infrastructure への直接依存がない
- [ ] Domain Layer が Presentation に依存していない
- [ ] API Route が DB を直接操作せず Service を経由している

### 2. モジュール構成が正しいか

新規機能の場合、以下の構成になっているか：

```text
src/modules/{feature}/
├── service.ts      # ビジネスロジック
├── types.ts        # 型定義
└── __tests__/      # テスト
```

### 3. API エンドポイントの配置

```text
app/api/
├── me/{feature}/           # 認証必須の個人リソース
│   ├── route.ts           # GET（一覧）, POST（作成）
│   └── [id]/route.ts      # GET, PUT, DELETE（個別）
└── {feature}/              # 公開リソース
```

### 4. 依存の方向

```text
許可される依存:
  app/api/* → src/modules/*/service.ts → src/db/*
  app/(app)/* → src/hooks/* → app/api/*

禁止される依存:
  src/modules/* → app/*
  src/db/* → src/modules/*
  src/lib/* → app/*
```

## 違反パターンと修正例

### NG: API Route で DB 直接操作

```typescript
// app/api/me/cards/route.ts - NG
import { db } from "@/db/drizzle";
const cards = await db.select().from(cardsTable);
```

### OK: Service 経由

```typescript
// app/api/me/cards/route.ts - OK
import { getCards } from "@/modules/cards/service";
const cards = await getCards(userId);
```

### NG: コンポーネントで DB アクセス

```typescript
// app/(app)/cards/page.tsx - NG
import { db } from "@/db/drizzle";
```

### OK: API 経由またはフック経由

```typescript
// app/(app)/cards/page.tsx - OK
import { useCards } from "@/hooks/use-cards";
```

## 新機能追加時の確認事項

1. **配置場所は適切か**
   - ビジネスロジック → `src/modules/{feature}/service.ts`
   - 型定義 → `src/modules/{feature}/types.ts`
   - API → `app/api/me/{feature}/route.ts`

2. **依存方向は正しいか**
   - 上位レイヤーから下位レイヤーへの一方向

3. **責務が分離されているか**
   - API: 認証・認可、リクエスト検証、レスポンス整形
   - Service: ビジネスロジック、トランザクション
   - DB: データアクセスのみ

## 参照

- [docs/architecture.md](../../docs/architecture.md)
- [.claude/agents/arch.md](../agents/arch.md)
