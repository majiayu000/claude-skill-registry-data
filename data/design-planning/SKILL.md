---
name: design-planning
description: |
  ソフトウェア設計計画スキル。要件分析、アーキテクチャ設計、API設計、データベース設計、
  実装ロードマップの作成を体系的に行います。Clean Architectureに準拠した設計を
  サブエージェントとの並列作業で効率的に実施します。
---

# Design Planning Skill

ソフトウェアプロジェクトの包括的な設計計画を作成するスキル。

## 対応領域

| 領域 | フォーカス | 詳細ガイド |
|------|-----------|-----------|
| Architecture | システム構成, レイヤー構造, コンポーネント設計 | `./agents/architecture-designer.md` |
| API | RESTful API, エンドポイント定義, リクエスト/レスポンス仕様 | `./agents/api-designer.md` |
| Database | ER図, テーブル設計, マイグレーション計画 | `./agents/database-designer.md` |

## 判断フロー

```
設計が必要な状況は？
│
├─ 新機能の包括的設計 ─────────────→ ✅ サブエージェント並列設計
│
├─ 複数レイヤーにまたがる変更 ────→ ✅ サブエージェント並列設計
│
├─ 単一領域の設計（APIのみ等）───→ ✅ 直接設計（該当領域のみ）
│
├─ 小規模変更（1カラム追加等）───→ ✅ 直接設計（軽量）
│
├─ バグ修正・スタイル修正 ────────→ ❌ 設計不要
│
└─ ドキュメント更新のみ ──────────→ ❌ 設計不要
```

## サブエージェント並列設計

大規模な設計が必要な場合、専門サブエージェントを並列起動。

```
┌──────────────────────────────────────────────────────────────┐
│ 1. 要件分析フェーズ                                          │
│    └── 機能要件・非機能要件を整理                            │
├──────────────────────────────────────────────────────────────┤
│ 2. 並列設計フェーズ（サブエージェント起動）                  │
│    ├── Architecture Designer → システム構成の設計            │
│    ├── API Designer         → API仕様の設計                  │
│    └── Database Designer    → データモデルの設計             │
├──────────────────────────────────────────────────────────────┤
│ 3. 統合フェーズ                                              │
│    └── 各設計の整合性確認と調整                              │
├──────────────────────────────────────────────────────────────┤
│ 4. 計画策定フェーズ                                          │
│    └── 実装ロードマップの作成                                │
└──────────────────────────────────────────────────────────────┘
```

## 設計ワークフロー（5ステップ）

```
    ┌───────────────────────────────────────────────────────┐
    │                                                       │
    ▼                                                       │
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐         │
│要件    │──→│アーキ  │──→│詳細    │──→│実装    │         │
│分析    │   │テクチャ│   │設計    │   │計画    │         │
└────────┘   └────────┘   └────────┘   └────────┘         │
                                            │              │
                                            ▼              │
                                       ┌────────┐         │
                                       │レビュー│─────────┘
                                       │& 承認  │
                                       └────────┘
```

### Step 1: 要件分析

**整理する項目**:

| カテゴリ | 内容 |
|---------|------|
| 機能要件 | ユーザーストーリー, 必須/追加機能, 入出力 |
| 非機能要件 | パフォーマンス, セキュリティ, スケーラビリティ |
| 制約条件 | 技術的制約, ビジネス制約, スケジュール |

**成果物例**:
```markdown
### 機能要件
- FR-001: [機能名] - [説明]

### 非機能要件
- NFR-001: [要件名] - [説明]

### 制約条件
- CON-001: [制約名] - [説明]
```

### Step 2: アーキテクチャ設計

**設計項目**:

| 項目 | 内容 |
|------|------|
| システム構成 | コンポーネント特定, 関係定義, 外部連携 |
| レイヤー構造 | API層, UseCase層, Domain層, Infrastructure層 |
| 技術選定 | フレームワーク, ライブラリ, インフラ |

**成果物例**:
```markdown
### レイヤー構造
| レイヤー | 責務 | 主要コンポーネント |
|---------|------|------------------|
| API | HTTPリクエスト処理 | Router, Controller |
| UseCase | ビジネスロジック調整 | Service, UseCase |
| Domain | ビジネスルール | Entity, ValueObject |
| Infrastructure | 外部システム連携 | Repository, Client |
```

### Step 3: 詳細設計

**設計項目**:

| 項目 | 内容 |
|------|------|
| API設計 | エンドポイント, リクエスト/レスポンス, エラー |
| DB設計 | テーブル定義, リレーション, インデックス |
| クラス設計 | インターフェース, クラス図, シーケンス図 |

**API設計例**:
```markdown
### POST /api/v1/users
**Request**:
{ "name": "string", "email": "string" }

**Response** (201):
{ "id": 1, "name": "string", "email": "string" }
```

**DB設計例**:
```markdown
### users テーブル
| カラム | 型 | NULL | 説明 |
|--------|-----|------|------|
| id | SERIAL | NO | 主キー |
| name | VARCHAR(100) | NO | ユーザー名 |
| email | VARCHAR(255) | NO | メールアドレス |
```

### Step 4: 実装計画

**策定項目**:

| 項目 | 内容 |
|------|------|
| タスク分解 | 設計→実装タスク, 依存関係, 優先順位 |
| 見積もり | 工数, リスク特定 |
| マイルストーン | フェーズ分け, デモポイント |

**成果物例**:
```markdown
### Phase 1: 基盤構築
- [ ] DBスキーマ作成
- [ ] エンティティ・リポジトリ実装

### Phase 2: API実装
- [ ] エンドポイント実装
- [ ] バリデーション実装
```

### Step 5: レビューと承認

- セルフレビュー（チェックリスト確認）
- レビュー依頼（観点を明示）
- フィードバック反映

## 設計パターン

### Clean Architecture

```
┌─────────────────────────────────────────────┐
│                   API層                      │
│  (Router, Controller, Request/Response)      │
├─────────────────────────────────────────────┤
│                UseCase層                     │
│      (Service, UseCase, Input/Output)        │
├─────────────────────────────────────────────┤
│                Domain層                      │
│    (Entity, ValueObject, DomainService)      │
├─────────────────────────────────────────────┤
│            Infrastructure層                  │
│  (Repository実装, ExternalClient, ORM)       │
└─────────────────────────────────────────────┘
```

**依存関係ルール**:
- 上位層 → 下位層への依存はOK
- 下位層 → 上位層への依存はNG
- Domain層は他のどの層にも依存しない

### Repository Pattern

```python
# Domain層: インターフェース定義
class UserRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

# Infrastructure層: 実装
class SQLAlchemyUserRepository(UserRepositoryInterface):
    def find_by_id(self, user_id: int) -> Optional[User]:
        model = self._session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        return self._to_entity(model) if model else None
```

## プロジェクト固有ガイドライン

### Backend (Python/FastAPI)

```python
# API層: HTTPリクエストの処理のみ
@router.post("/users", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    usecase: CreateUserUseCase = Depends(get_create_user_usecase)
):
    return await usecase.execute(request.to_input())

# UseCase層: ビジネスロジックの調整
class CreateUserUseCase:
    async def execute(self, input: CreateUserInput) -> CreateUserOutput:
        user = User.create(input.name, input.email)
        saved = await self._repo.save(user)
        return CreateUserOutput.from_entity(saved)

# Domain層: ビジネスルール
class User:
    @classmethod
    def create(cls, name: str, email: Email) -> "User":
        if not name:
            raise DomainError("Name is required")
        return cls(name=name, email=email)
```

### Frontend (TypeScript/SvelteKit)

```typescript
// Presentational Component（表示専用）
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
  onDelete: (id: number) => void;
}

// 型安全性の確保
interface ApiResponse<T> {
  data: T;
  error: ApiError | null;
}
```

## 設計チェックリスト

### 🔴 必須

- [ ] 要件が明確になっている
- [ ] Clean Architectureに準拠している
- [ ] 依存関係の方向が正しい
- [ ] API仕様が定義されている
- [ ] DBスキーマが正規化されている

### 🟡 推奨

- [ ] 非機能要件を考慮している
- [ ] エラーレスポンスが定義されている
- [ ] インデックスが適切に設計されている
- [ ] マイグレーション計画がある
- [ ] テスト計画がある

### 🟢 Nice to have

- [ ] 拡張性を考慮している
- [ ] トレードオフを文書化している
- [ ] 将来の変更点を予測している

## ベストプラクティス

### DO ✅

- 要件を明確にしてから設計を始める
- 既存アーキテクチャとの整合性を確認
- 小さな単位で設計・レビューを実施
- 設計と実装のギャップを継続的に埋める
- YAGNI原則（必要になるまで作らない）

### DON'T ❌

- 要件が曖昧なまま設計を進める
- 過剰な抽象化をする
- 将来の要件に過度に対応する
- 設計ドキュメントを放置する
- 実装可能性を無視した設計

## 設計ドキュメント構成

```markdown
# [機能名] 設計書

## 1. 概要
- 目的
- スコープ

## 2. 要件
- 機能要件（FR-xxx）
- 非機能要件（NFR-xxx）

## 3. アーキテクチャ設計
- システム構成図
- コンポーネント一覧

## 4. 詳細設計
- API設計
- データベース設計

## 5. 実装計画
- タスク一覧
- マイルストーン

## 6. リスクと対策
```

## 参照ファイル

| ファイル | 説明 |
|---------|------|
| `./agents/architecture-designer.md` | アーキテクチャ設計詳細 |
| `./agents/api-designer.md` | API設計詳細 |
| `./agents/database-designer.md` | データベース設計詳細 |
| `.claude/rules/backend/layer-rules.md` | Backendレイヤールール |
| `.claude/rules/backend/database-rules.md` | データベース設計規約 |
