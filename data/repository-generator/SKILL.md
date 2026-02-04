---
name: repository-generator
description: 新しいRepository層のコードを作成する際に使用。標準SQL版とGORM版、GroupManager/TableSelector使用、シャーディング対応、CRUDメソッドのパターンを適用。Repositoryの新規作成、データアクセス層の実装時に使用。
allowed-tools: Read, Glob
---

# Repository 生成パターン

このプロジェクトのRepository層実装パターンを定義します。

## ファイル構成

新しいエンティティ `{Entity}` を追加する場合:

```
server/internal/repository/
├── {entity}_repository.go       # 標準SQL版
└── {entity}_repository_gorm.go  # GORM版
```

## 参照ファイル

Repository実装の参照:
- `server/internal/repository/user_repository.go` - 標準SQL版
- `server/internal/repository/user_repository_gorm.go` - GORM版
- `server/internal/repository/post_repository.go` - 別エンティティの例

モデル定義:
- `server/internal/model/user.go`
- `server/internal/model/post.go`

## 構造体パターン

### 標準SQL版

```go
package repository

import (
    "context"
    "database/sql"
    "fmt"
    "time"

    "github.com/example/go-webdb-template/internal/db"
    "github.com/example/go-webdb-template/internal/model"
)

// EntityRepository は{Entity}のデータアクセスを担当
type EntityRepository struct {
    groupManager  *db.GroupManager
    tableSelector *db.TableSelector
}

// NewEntityRepository は新しいEntityRepositoryを作成
func NewEntityRepository(groupManager *db.GroupManager) *EntityRepository {
    return &EntityRepository{
        groupManager:  groupManager,
        tableSelector: db.NewTableSelector(32, 8),
    }
}
```

### GORM版

```go
package repository

import (
    "context"
    "fmt"

    "github.com/example/go-webdb-template/internal/db"
    "github.com/example/go-webdb-template/internal/model"
)

// EntityRepositoryGORM は{Entity}のGORM版データアクセスを担当
type EntityRepositoryGORM struct {
    groupManager  *db.GroupManager
    tableSelector *db.TableSelector
}

// NewEntityRepositoryGORM は新しいEntityRepositoryGORMを作成
func NewEntityRepositoryGORM(groupManager *db.GroupManager) *EntityRepositoryGORM {
    return &EntityRepositoryGORM{
        groupManager:  groupManager,
        tableSelector: db.NewTableSelector(32, 8),
    }
}
```

## CRUDメソッドパターン

### Create

```go
func (r *EntityRepository) Create(ctx context.Context, req *model.CreateEntityRequest) (*model.Entity, error) {
    now := time.Now()
    entity := &model.Entity{
        // フィールド設定
        CreatedAt: now,
        UpdatedAt: now,
    }

    // IDを生成（タイムスタンプベース）
    entity.ID = now.UnixNano()

    // テーブル名の生成
    tableName := r.tableSelector.GetTableName("entities", entity.ID)

    // 接続の取得
    conn, err := r.groupManager.GetShardingConnectionByID(entity.ID, "entities")
    if err != nil {
        return nil, fmt.Errorf("failed to get sharding connection: %w", err)
    }

    // INSERT実行
    // ...

    return entity, nil
}
```

### GetByID

```go
func (r *EntityRepository) GetByID(ctx context.Context, id int64) (*model.Entity, error) {
    tableName := r.tableSelector.GetTableName("entities", id)

    conn, err := r.groupManager.GetShardingConnectionByID(id, "entities")
    if err != nil {
        return nil, fmt.Errorf("failed to get sharding connection: %w", err)
    }

    // SELECT実行
    // ...

    if err == sql.ErrNoRows {
        return nil, fmt.Errorf("entity not found: %d", id)
    }

    return &entity, nil
}
```

### List (クロステーブルクエリ)

```go
func (r *EntityRepository) List(ctx context.Context, limit, offset int) ([]*model.Entity, error) {
    connections := r.groupManager.GetAllShardingConnections()
    entities := make([]*model.Entity, 0)

    for _, conn := range connections {
        sqlDB, err := conn.DB.DB()
        if err != nil {
            return nil, fmt.Errorf("failed to get sql.DB for shard %d: %w", conn.ShardID, err)
        }

        // このDBに含まれるテーブル（8つずつ）
        startTable := (conn.ShardID - 1) * 8
        endTable := startTable + 7

        for tableNum := startTable; tableNum <= endTable; tableNum++ {
            tableName := fmt.Sprintf("entities_%03d", tableNum)
            // クエリ実行...
        }
    }

    return entities, nil
}
```

### Update

```go
func (r *EntityRepository) Update(ctx context.Context, id int64, req *model.UpdateEntityRequest) (*model.Entity, error) {
    tableName := r.tableSelector.GetTableName("entities", id)

    conn, err := r.groupManager.GetShardingConnectionByID(id, "entities")
    if err != nil {
        return nil, fmt.Errorf("failed to get sharding connection: %w", err)
    }

    // UPDATE実行
    // ...

    // 更新後のエンティティを取得
    return r.GetByID(ctx, id)
}
```

### Delete

```go
func (r *EntityRepository) Delete(ctx context.Context, id int64) error {
    tableName := r.tableSelector.GetTableName("entities", id)

    conn, err := r.groupManager.GetShardingConnectionByID(id, "entities")
    if err != nil {
        return fmt.Errorf("failed to get sharding connection: %w", err)
    }

    // DELETE実行
    // ...

    if rowsAffected == 0 {
        return fmt.Errorf("entity not found: %d", id)
    }

    return nil
}
```

## エラーハンドリング

```go
// エラーラップのパターン
return nil, fmt.Errorf("failed to create entity: %w", err)

// Not Found エラー
if err == sql.ErrNoRows {
    return nil, fmt.Errorf("entity not found: %d", id)
}
```

## 必要なモデル定義

```go
// server/internal/model/entity.go
package model

import "time"

type Entity struct {
    ID        int64     `json:"id"`
    // 他のフィールド
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}

type CreateEntityRequest struct {
    // 作成時の入力フィールド
}

type UpdateEntityRequest struct {
    // 更新時の入力フィールド
}
```
