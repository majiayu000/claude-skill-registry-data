---
name: corder-code-templates
description: |
  Generate code templates for common patterns: REST API endpoints, React components, database models, authentication, error handling. Use when implementing new features or creating boilerplate code.

  This skill provides production-ready code templates:
  - REST API endpoints (Express, FastAPI)
  - React/Vue components with best practices
  - Database models (Sequelize, TypeORM, Mongoose)
  - Authentication middleware (JWT, OAuth)
  - Error handling patterns

  Triggers: "create API", "new component", "implement auth", "add model", "generate code", "コードテンプレート", "API作成", "コンポーネント作成"
allowed-tools:
  - Read
  - Write
  - Bash
---

# Corder Code Templates Skill

## 概要

このSkillは、corderエージェントが新機能を実装する際に使用するコードテンプレート集です。REST APIエンドポイント、Reactコンポーネント、データベースモデル、認証ロジック、エラーハンドリングなど、頻出パターンのテンプレートを提供します。

## 主な機能

1. **REST APIエンドポイント**: Express.js、FastAPIのテンプレート
2. **Reactコンポーネント**: 関数コンポーネント、Hooks、状態管理
3. **データベースモデル**: Sequelize、TypeORM、Mongoose
4. **認証ミドルウェア**: JWT、OAuth、セッション管理
5. **エラーハンドリング**: グローバルエラーハンドラー、カスタムエラークラス

## 使用方法

### テンプレート一覧

```
templates/
├── rest-api-endpoint.js      # Express REST APIエンドポイント
├── rest-api-endpoint.py      # FastAPI エンドポイント
├── react-component.jsx       # React関数コンポーネント
├── react-component-ts.tsx    # React + TypeScript
├── database-model.js         # Sequelize モデル
├── auth-middleware.js        # JWT認証ミドルウェア
└── error-handler.js          # エラーハンドリング
```

### 使用例

**1. REST APIエンドポイント作成**

テンプレートファイル `rest-api-endpoint.js` をコピーして、プロジェクトに追加します:

```javascript
// templates/rest-api-endpoint.js をベースに実装
const express = require('express');
const router = express.Router();

/**
 * @route   GET /api/users
 * @desc    Get all users
 * @access  Public
 */
router.get('/', async (req, res) => {
  try {
    const users = await User.findAll();
    res.json({ success: true, data: users });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
```

**2. Reactコンポーネント作成**

```jsx
// templates/react-component.jsx をベースに実装
import React, { useState, useEffect } from 'react';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users');
      const data = await response.json();
      setUsers(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};

export default UserList;
```

**3. データベースモデル作成**

```javascript
// templates/database-model.js をベースに実装
const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const User = sequelize.define('User', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        notEmpty: true,
        len: [2, 100]
      }
    },
    email: {
      type: DataTypes.STRING,
      unique: true,
      allowNull: false,
      validate: {
        isEmail: true
      }
    }
  });

  return User;
};
```

## テンプレートの特徴

### ✅ ベストプラクティス適用

- **エラーハンドリング**: try-catch、適切なHTTPステータスコード
- **バリデーション**: 入力値検証、型チェック
- **セキュリティ**: SQLインジェクション対策、XSS対策
- **パフォーマンス**: 非同期処理、N+1クエリ回避
- **保守性**: コメント、明確な変数名、DRY原則

### 📚 ドキュメント完備

- JSDocコメント
- API仕様（ルート、説明、アクセス制御）
- 使用例
- 受入基準

## テンプレート詳細

### REST API Endpoint (Express.js)

**ファイル**: `templates/rest-api-endpoint.js`

**機能**:
- CRUD操作（GET, POST, PUT, DELETE）
- バリデーション
- エラーハンドリング
- 認証ミドルウェア統合

### React Component

**ファイル**: `templates/react-component.jsx`

**機能**:
- 関数コンポーネント + Hooks
- 状態管理（useState）
- 副作用処理（useEffect）
- ローディング・エラー状態
- プロップスの型定義（PropTypes）

### Database Model

**ファイル**: `templates/database-model.js`

**機能**:
- Sequelizeモデル定義
- バリデーション
- アソシエーション（hasMany, belongsTo）
- フック（beforeCreate等）

### Authentication Middleware

**ファイル**: `templates/auth-middleware.js`

**機能**:
- JWT検証
- トークンリフレッシュ
- ロールベースアクセス制御（RBAC）
- セッション管理

### Error Handler

**ファイル**: `templates/error-handler.js`

**機能**:
- グローバルエラーハンドラー
- カスタムエラークラス
- ロギング統合
- 環境別エラーレスポンス

## カスタマイズ方法

1. **テンプレートをコピー**: プロジェクトの適切な場所にコピー
2. **プレースホルダーを置換**: `[RESOURCE]`, `[MODEL_NAME]` 等を実際の名前に変更
3. **ビジネスロジック追加**: TODO コメントに従って実装
4. **テスト作成**: corder-test-generation Skillを使用

## ベストプラクティス

### DO（推奨）

✅ **テンプレートをそのままコピー**: 最新のベストプラクティスが適用済み
✅ **プロジェクト規約に合わせる**: 命名規則、インデント等を統一
✅ **セキュリティを最優先**: 認証、バリデーション、エスケープ
✅ **テストを作成**: corder-test-generation Skillで自動生成

### DON'T（非推奨）

❌ **テンプレートの安全機能を削除**: エラーハンドリング、バリデーション等
❌ **古いパターンを使用**: async/awaitを使用、Promiseチェーンを避ける
❌ **セキュリティを軽視**: SQLインジェクション、XSS対策は必須

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約200行）です。詳細なテンプレートコードは `templates/` ディレクトリ内のファイルを参照してください。

## 関連Skill

- **corder-test-generation**: テンプレートから生成したコードのテスト作成
- **qa-code-review-checklist**: コード品質レビュー

## 関連リソース

- **templates/**: すべてのテンプレートファイル
- **reference.md**: テンプレート使用のベストプラクティス
