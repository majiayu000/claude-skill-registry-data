---
name: backend-development
description: バックエンド開発の基礎。API設計、データベース設計、認証・認可、エラーハンドリング、セキュリティなど、堅牢なバックエンドシステム構築のベストプラクティス。
---

# Backend Development Skill

## 📋 目次

1. [概要](#概要)
2. [詳細ガイド](#詳細ガイド)
3. [いつ使うか](#いつ使うか)
4. [API設計](#api設計)
5. [認証・認可](#認証認可)
6. [エラーハンドリング](#エラーハンドリング)
7. [セキュリティ](#セキュリティ)
8. [実践例](#実践例)
9. [Agent連携](#agent連携)

---

## 概要

このSkillは、バックエンド開発の基礎をカバーします：

- **API設計** - RESTful API, GraphQL
- **認証・認可** - JWT, OAuth, Session
- **データベース設計** - スキーマ設計、マイグレーション
- **エラーハンドリング** - 適切なエラーレスポンス
- **セキュリティ** - SQL Injection, XSS, CSRF対策
- **パフォーマンス** - キャッシング、クエリ最適化

---

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: API設計パターン、セキュリティ原則、エラーハンドリング戦略
**公式で確認すべきこと**: 最新セキュリティ脆弱性、OWASP Top 10、フレームワーク最新機能

### 主要な公式ドキュメント

- **[REST API Design](https://restfulapi.net/)** - RESTful API設計ガイド
- **[GraphQL](https://graphql.org/learn/)** - GraphQL公式ドキュメント
- **[OWASP](https://owasp.org/)** - Webセキュリティ標準
  - [OWASP Top 10](https://owasp.org/www-project-top-ten/) - 主要脆弱性
  - [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - セキュリティ対策集

### フレームワーク

- **[Express.js](https://expressjs.com/)** - Node.js Webフレームワーク
- **[NestJS](https://docs.nestjs.com/)** - TypeScriptエンタープライズフレームワーク
- **[FastAPI](https://fastapi.tiangolo.com/)** - Python高速APIフレームワーク
- **[Django REST Framework](https://www.django-rest-framework.org/)** - Django API

### 関連リソース

- **[HTTP Status Codes](https://httpstatuses.com/)** - HTTPステータスコード一覧
- **[JWT.io](https://jwt.io/)** - JWT仕様・デバッガー
- **[API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)** - セキュリティチェックリスト

---

## 詳細ガイド

以下の完全ガイドで、堅牢なバックエンド構築を学べます：

### 1. [API設計完全ガイド](./guides/api/api-design-complete.md)

**27,000文字 | Node.js 20.0+ | Express 4.18+ | GraphQL 16.8+**

- REST/GraphQL/gRPC API設計の全て
- Express + TypeScriptでの実装（Controllers, Services, Routes）
- HTTPステータスコード、エラーレスポンス形式の統一
- APIバージョニング戦略（URLバージョニング、ヘッダーバージョニング）
- 認証・認可（JWT、RBAC、リソースベースアクセス制御）
- **10のトラブルシューティング事例**
- 実測データ（レスポンスタイム -86%、エラー率 -91%、N+1問題 -100%）

### 2. [エラーハンドリング完全ガイド](./guides/error-handling/error-handling-complete.md)

**27,000文字 | Winston 3.11+ | Sentry 7.100+**

- カスタムエラークラス設計（Operational vs Programmer Error）
- Express/NestJSでのグローバルエラーハンドラー
- データベースエラー処理（Prismaエラーマッピング）
- 構造化ログ戦略（Winston + ローテーション）
- エラー監視（Sentry統合、カスタムトラッキング）
- リトライ戦略（指数バックオフ）
- サーキットブレーカーパターン
- **10のトラブルシューティング事例**
- 実測データ（エラー解決時間 -81%、サーバークラッシュ -100%）

### 3. [セキュリティ完全ガイド](./guides/security/security-complete.md)

**27,000文字 | Helmet 7.1+ | bcrypt 5.1+ | OWASP ZAP 2.14+**

- 認証（JWT、リフレッシュトークン、2要素認証）
- 認可（RBAC、リソースベースアクセス制御）
- **OWASP Top 10完全対策**
- SQL/NoSQL Injection対策
- XSS対策（CSP、サニタイズ）
- CSRF対策（トークン、SameSite Cookie）
- レート制限（express-rate-limit + Redis）
- セキュアヘッダー（Helmet設定）
- **10のトラブルシューティング事例**
- 実測データ（脆弱性 -97%、ブルートフォース攻撃 -99%、不正ログイン -100%）

**合計**: 81,000文字 | 3ガイド

---

## いつ使うか

### 🎯 必須のタイミング

- [ ] 新規APIエンドポイント作成時
- [ ] データベーススキーマ設計時
- [ ] 認証機能実装時
- [ ] セキュリティレビュー時

---

## API設計

### RESTful API設計

#### リソースベース設計

```
GET    /api/users          # ユーザー一覧取得
GET    /api/users/:id      # 特定ユーザー取得
POST   /api/users          # ユーザー作成
PUT    /api/users/:id      # ユーザー更新
DELETE /api/users/:id      # ユーザー削除

GET    /api/users/:id/posts # 特定ユーザーの投稿一覧
```

#### レスポンス形式

```json
// ✅ 成功レスポンス（200 OK）
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// ✅ リストレスポンス
{
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "perPage": 20
  }
}

// ✅ エラーレスポンス（400 Bad Request）
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

#### HTTPステータスコード

| コード | 説明 | 使用例 |
|--------|------|--------|
| **200** | OK | 成功（GET, PUT） |
| **201** | Created | リソース作成成功（POST） |
| **204** | No Content | 削除成功（DELETE） |
| **400** | Bad Request | バリデーションエラー |
| **401** | Unauthorized | 認証失敗 |
| **403** | Forbidden | 権限不足 |
| **404** | Not Found | リソースが存在しない |
| **500** | Internal Server Error | サーバーエラー |

---

## 認証・認可

### JWT（JSON Web Token）

```typescript
// トークン生成
import jwt from 'jsonwebtoken'

function generateToken(userId: string) {
  return jwt.sign(
    { userId },
    process.env.JWT_SECRET!,
    { expiresIn: '7d' }
  )
}

// トークン検証
function verifyToken(token: string) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!)
  } catch (error) {
    throw new Error('Invalid token')
  }
}

// ミドルウェア
async function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '')

  if (!token) {
    return res.status(401).json({ error: 'No token provided' })
  }

  try {
    const decoded = verifyToken(token)
    req.userId = decoded.userId
    next()
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' })
  }
}
```

### パスワードハッシュ化

```typescript
import bcrypt from 'bcrypt'

// パスワードハッシュ化
async function hashPassword(password: string) {
  return bcrypt.hash(password, 10)
}

// パスワード照合
async function comparePassword(password: string, hash: string) {
  return bcrypt.compare(password, hash)
}

// 使用例
const hashedPassword = await hashPassword('mypassword')
const isValid = await comparePassword('mypassword', hashedPassword)
```

### ロールベースアクセス制御（RBAC）

```typescript
// ユーザーロール
enum Role {
  USER = 'user',
  ADMIN = 'admin',
  MODERATOR = 'moderator'
}

// 権限チェックミドルウェア
function requireRole(...roles: Role[]) {
  return async (req, res, next) => {
    const user = await prisma.user.findUnique({
      where: { id: req.userId }
    })

    if (!user || !roles.includes(user.role)) {
      return res.status(403).json({ error: 'Forbidden' })
    }

    next()
  }
}

// 使用例
router.delete('/api/users/:id', authMiddleware, requireRole(Role.ADMIN), deleteUser)
```

---

## エラーハンドリング

### カスタムエラークラス

```typescript
// エラークラス定義
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: any
  ) {
    super(message)
    this.name = 'AppError'
  }
}

class ValidationError extends AppError {
  constructor(message: string, details?: any) {
    super(400, 'VALIDATION_ERROR', message, details)
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`)
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(401, 'UNAUTHORIZED', message)
  }
}
```

### グローバルエラーハンドラー

```typescript
// Express エラーハンドラー
function errorHandler(err: Error, req, res, next) {
  console.error(err)

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details
      }
    })
  }

  // 予期しないエラー
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  })
}

// 使用例
app.use(errorHandler)
```

---

## セキュリティ

### SQL Injection対策

```typescript
// ❌ 悪い例（SQL Injection脆弱）
const userId = req.params.id
const user = await db.query(`SELECT * FROM users WHERE id = ${userId}`)

// ✅ 良い例（Prisma使用）
const user = await prisma.user.findUnique({
  where: { id: userId }
})

// ✅ 良い例（プリペアドステートメント）
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId])
```

### CORS設定

```typescript
import cors from 'cors'

app.use(cors({
  origin: process.env.CLIENT_URL, // 本番環境では特定のドメインのみ
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))
```

### レート制限

```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 100, // 最大100リクエスト
  message: 'Too many requests'
})

app.use('/api/', limiter)
```

### 入力バリデーション

```typescript
import { z } from 'zod'

// スキーマ定義
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  password: z.string().min(8)
})

// バリデーション
async function createUser(req, res) {
  try {
    const data = createUserSchema.parse(req.body)

    // ユーザー作成処理
    const user = await prisma.user.create({
      data: {
        ...data,
        password: await hashPassword(data.password)
      }
    })

    res.status(201).json({ data: user })
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new ValidationError('Invalid input', error.errors)
    }
    throw error
  }
}
```

---

## 実践例

### Example 1: ユーザーCRUD API

```typescript
// routes/users.ts
import express from 'express'
import { prisma } from '../lib/prisma'
import { authMiddleware } from '../middleware/auth'
import { z } from 'zod'

const router = express.Router()

// GET /api/users
router.get('/', authMiddleware, async (req, res) => {
  const users = await prisma.user.findMany({
    select: { id: true, name: true, email: true }
  })

  res.json({ data: users })
})

// GET /api/users/:id
router.get('/:id', authMiddleware, async (req, res) => {
  const user = await prisma.user.findUnique({
    where: { id: req.params.id },
    select: { id: true, name: true, email: true }
  })

  if (!user) {
    throw new NotFoundError('User')
  }

  res.json({ data: user })
})

// POST /api/users
router.post('/', async (req, res) => {
  const schema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8)
  })

  const data = schema.parse(req.body)

  const user = await prisma.user.create({
    data: {
      ...data,
      password: await hashPassword(data.password)
    },
    select: { id: true, name: true, email: true }
  })

  res.status(201).json({ data: user })
})

// PUT /api/users/:id
router.put('/:id', authMiddleware, async (req, res) => {
  const schema = z.object({
    name: z.string().min(1).optional(),
    email: z.string().email().optional()
  })

  const data = schema.parse(req.body)

  const user = await prisma.user.update({
    where: { id: req.params.id },
    data,
    select: { id: true, name: true, email: true }
  })

  res.json({ data: user })
})

// DELETE /api/users/:id
router.delete('/:id', authMiddleware, requireRole(Role.ADMIN), async (req, res) => {
  await prisma.user.delete({
    where: { id: req.params.id }
  })

  res.status(204).send()
})

export default router
```

### Example 2: 認証API

```typescript
// routes/auth.ts
router.post('/register', async (req, res) => {
  const schema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8)
  })

  const data = schema.parse(req.body)

  // メール重複チェック
  const existing = await prisma.user.findUnique({
    where: { email: data.email }
  })

  if (existing) {
    throw new ValidationError('Email already exists')
  }

  // ユーザー作成
  const user = await prisma.user.create({
    data: {
      ...data,
      password: await hashPassword(data.password)
    }
  })

  // トークン生成
  const token = generateToken(user.id)

  res.status(201).json({
    data: { user: { id: user.id, name: user.name, email: user.email } },
    token
  })
})

router.post('/login', async (req, res) => {
  const schema = z.object({
    email: z.string().email(),
    password: z.string()
  })

  const { email, password } = schema.parse(req.body)

  // ユーザー検索
  const user = await prisma.user.findUnique({
    where: { email }
  })

  if (!user || !(await comparePassword(password, user.password))) {
    throw new UnauthorizedError('Invalid credentials')
  }

  // トークン生成
  const token = generateToken(user.id)

  res.json({
    data: { user: { id: user.id, name: user.name, email: user.email } },
    token
  })
})

router.get('/me', authMiddleware, async (req, res) => {
  const user = await prisma.user.findUnique({
    where: { id: req.userId },
    select: { id: true, name: true, email: true }
  })

  res.json({ data: user })
})
```

---

## Agent連携

### 📖 Agentへの指示例

**CRUD API作成**
```
/api/posts のCRUD APIを作成してください。
以下を含めてください：
- GET /api/posts（一覧取得）
- GET /api/posts/:id（詳細取得）
- POST /api/posts（作成）
- PUT /api/posts/:id（更新）
- DELETE /api/posts/:id（削除）
- Zodでバリデーション
- 認証ミドルウェア
```

**認証機能実装**
```
JWT認証を実装してください。
以下を含めてください：
- POST /api/auth/register（登録）
- POST /api/auth/login（ログイン）
- GET /api/auth/me（現在のユーザー取得）
- パスワードハッシュ化（bcrypt）
```

---

## まとめ

### バックエンド開発のベストプラクティス

1. **API設計** - RESTful, 適切なHTTPステータスコード
2. **認証・認可** - JWT, RBAC
3. **セキュリティ** - 入力バリデーション, SQL Injection対策
4. **エラーハンドリング** - 適切なエラーレスポンス

---

## 関連Skills

- **nodejs-development** - Node.js/Express詳細
- **python-development** - Python/FastAPI詳細
- **database-design** - データベース設計詳細
- **api-design** - API設計詳細

---

_Last updated: 2025-12-24_
