---
name: developing-backend
description: バックエンド API 実装、認証・認可、キャッシング戦略を支援します。セキュアな実装、パフォーマンス最適化、テスト戦略を提供します。API実装、バックエンドサービスの開発が必要な場合に使用してください。
disable-model-invocation: false
---

# バックエンド開発と信頼性エンジニアリング

## 概要

バックエンド開発、API設計、データベース設計、セキュリティ実装、信頼性構築を包括的に支援するスキルです。

## 実行フロー

### Step 1: システム設計の基礎

#### アーキテクチャ判断

```
モノリスを選ぶ場合:
- チームが小規模（<10人）
- ドメインが明確に分離されていない
- 初期MVP段階

マイクロサービスを選ぶ場合:
- 独立したスケーリングが必要
- チームが大規模で分散している
- ドメイン境界が明確
```

### Step 2: API設計

#### RESTful API設計原則

```
GET    /api/v1/users          # 一覧
POST   /api/v1/users          # 作成
GET    /api/v1/users/:id      # 取得
PUT    /api/v1/users/:id      # 更新
DELETE /api/v1/users/:id      # 削除
```

**HTTPステータスコード:**

| コード | 用途                     |
| ------ | ------------------------ |
| 200    | 成功                     |
| 201    | リソース作成成功         |
| 400    | クライアントエラー       |
| 401    | 認証エラー               |
| 403    | 認可エラー               |
| 404    | リソース不存在           |
| 500    | サーバーエラー           |

**エラーレスポンス標準化:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [...],
    "request_id": "req_abc123"
  }
}
```

### Step 3: データベース設計

#### インデックス戦略

```sql
-- 頻繁に検索されるカラム
CREATE INDEX idx_users_email ON users(email);

-- 複合インデックス
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
```

### Step 4: 認証・認可

#### JWT認証の実装

```javascript
function generateToken(userId) {
  return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: '24h' });
}
```

#### RBAC（Role-Based Access Control）

```javascript
function authorize(...allowedRoles) {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}
```

### Step 5: パフォーマンス最適化

#### キャッシング戦略

```javascript
async function getCachedUser(userId) {
  const cached = await redis.get(`user:${userId}`);
  if (cached) return JSON.parse(cached);

  const user = await db.users.findById(userId);
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
  return user;
}
```

#### 接続プーリング

```javascript
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Step 6: セキュリティ実装

#### 入力バリデーション（Zod）

```javascript
const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
});
```

#### SQLインジェクション防止

```javascript
// パラメータ化クエリ
const result = await db.query('SELECT * FROM users WHERE email = $1', [email]);
```

### Step 7: 監視とロギング

#### Four Golden Signals

| シグナル   | 説明               | 目標          |
| ---------- | ------------------ | ------------- |
| Latency    | レスポンスタイム   | p95 < 200ms   |
| Traffic    | リクエスト数       | 監視          |
| Errors     | エラー率           | < 0.1%        |
| Saturation | リソース使用率     | CPU < 70%     |

## 出力成果物

1. **API設計書**: OpenAPI/Swagger仕様書
2. **データベーススキーマ**: ER図、マイグレーションスクリプト
3. **実装コード**: API実装、ビジネスロジック
4. **テストコード**: ユニットテスト、統合テスト
5. **ドキュメント**: セットアップガイド、API使用例
6. **監視設定**: ログ、メトリクス、アラート設定

## ベストプラクティス

1. **信頼性優先**: データ整合性を何よりも重視
2. **セキュリティファースト**: すべての入力を検証・サニタイズ
3. **スケーラビリティ**: 水平スケーリングを念頭に設計
4. **観測可能性**: 構造化ロギング、メトリクス収集
5. **テスト駆動**: ユニット・統合・パフォーマンステスト

## 関連ファイル

- [PATTERNS.md](./PATTERNS.md) - 実装パターン集
- [SECURITY.md](./SECURITY.md) - セキュリティチェックリスト
