---
name: api-endpoint-creator
description: 新しいAPIエンドポイントを追加する際に使用。Huma API、Echo、Handler/Service/Repositoryの3層構成、エンドポイント登録パターンを適用。REST API、新規エンドポイント、CRUD APIを追加する場合に使用。
allowed-tools: Read, Glob
---

# API エンドポイント作成パターン

このプロジェクトのAPI実装パターンを定義します。

## アーキテクチャ

3層構成:

```
Handler (API層) → Service (ビジネスロジック) → Repository (データアクセス)
```

## 使用フレームワーク

- **Echo**: HTTPルーター
- **Huma v2**: OpenAPI対応のAPIフレームワーク
- **humaecho**: EchoとHumaのアダプター

## ディレクトリ構成

```
server/internal/
├── api/
│   ├── handler/
│   │   ├── user_handler.go
│   │   └── post_handler.go
│   ├── huma/
│   │   └── types.go         # Huma用の入出力型定義
│   └── router/
│       └── router.go        # ルーター設定
├── service/
│   ├── user_service.go
│   └── post_service.go
└── repository/
    ├── user_repository.go
    └── post_repository.go
```

## 参照ファイル

Handler:
- `server/internal/api/handler/user_handler.go`
- `server/internal/api/handler/post_handler.go`

Huma型定義:
- `server/internal/api/huma/types.go`

ルーター:
- `server/internal/api/router/router.go`

Service:
- `server/internal/service/user_service.go`

## Handler パターン

### 構造体定義

```go
package handler

import (
    "context"
    "net/http"

    "github.com/danielgtaylor/huma/v2"
    humaapi "github.com/example/go-webdb-template/internal/api/huma"
    "github.com/example/go-webdb-template/internal/model"
    "github.com/example/go-webdb-template/internal/service"
)

// EntityHandler はエンティティAPIのハンドラー
type EntityHandler struct {
    entityService *service.EntityService
}

// NewEntityHandler は新しいEntityHandlerを作成
func NewEntityHandler(entityService *service.EntityService) *EntityHandler {
    return &EntityHandler{
        entityService: entityService,
    }
}
```

### エンドポイント登録

```go
// RegisterEntityEndpoints はHuma APIにエンティティエンドポイントを登録
func RegisterEntityEndpoints(api huma.API, h *EntityHandler) {
    // POST /api/entities - エンティティ作成
    huma.Register(api, huma.Operation{
        OperationID:   "create-entity",
        Method:        http.MethodPost,
        Path:          "/api/entities",
        Summary:       "エンティティを作成",
        Tags:          []string{"entities"},
        DefaultStatus: http.StatusCreated,
    }, func(ctx context.Context, input *humaapi.CreateEntityInput) (*humaapi.EntityOutput, error) {
        req := &model.CreateEntityRequest{
            Name: input.Body.Name,
        }

        entity, err := h.entityService.CreateEntity(ctx, req)
        if err != nil {
            return nil, huma.Error500InternalServerError(err.Error())
        }

        resp := &humaapi.EntityOutput{}
        resp.Body = *entity
        return resp, nil
    })

    // GET /api/entities/{id} - エンティティ取得
    huma.Register(api, huma.Operation{
        OperationID: "get-entity",
        Method:      http.MethodGet,
        Path:        "/api/entities/{id}",
        Summary:     "エンティティを取得",
        Tags:        []string{"entities"},
    }, func(ctx context.Context, input *humaapi.GetEntityInput) (*humaapi.EntityOutput, error) {
        entity, err := h.entityService.GetEntity(ctx, input.ID)
        if err != nil {
            return nil, huma.Error404NotFound(err.Error())
        }

        resp := &humaapi.EntityOutput{}
        resp.Body = *entity
        return resp, nil
    })

    // GET /api/entities - エンティティ一覧取得
    huma.Register(api, huma.Operation{
        OperationID: "list-entities",
        Method:      http.MethodGet,
        Path:        "/api/entities",
        Summary:     "エンティティ一覧を取得",
        Tags:        []string{"entities"},
    }, func(ctx context.Context, input *humaapi.ListEntitiesInput) (*humaapi.EntitiesOutput, error) {
        entities, err := h.entityService.ListEntities(ctx, input.Limit, input.Offset)
        if err != nil {
            return nil, huma.Error500InternalServerError(err.Error())
        }

        resp := &humaapi.EntitiesOutput{}
        resp.Body = entities
        return resp, nil
    })

    // PUT /api/entities/{id} - エンティティ更新
    huma.Register(api, huma.Operation{
        OperationID: "update-entity",
        Method:      http.MethodPut,
        Path:        "/api/entities/{id}",
        Summary:     "エンティティを更新",
        Tags:        []string{"entities"},
    }, func(ctx context.Context, input *humaapi.UpdateEntityInput) (*humaapi.EntityOutput, error) {
        req := &model.UpdateEntityRequest{
            Name: input.Body.Name,
        }

        entity, err := h.entityService.UpdateEntity(ctx, input.ID, req)
        if err != nil {
            return nil, huma.Error500InternalServerError(err.Error())
        }

        resp := &humaapi.EntityOutput{}
        resp.Body = *entity
        return resp, nil
    })

    // DELETE /api/entities/{id} - エンティティ削除
    huma.Register(api, huma.Operation{
        OperationID:   "delete-entity",
        Method:        http.MethodDelete,
        Path:          "/api/entities/{id}",
        Summary:       "エンティティを削除",
        Tags:          []string{"entities"},
        DefaultStatus: http.StatusNoContent,
    }, func(ctx context.Context, input *humaapi.DeleteEntityInput) (*struct{}, error) {
        err := h.entityService.DeleteEntity(ctx, input.ID)
        if err != nil {
            return nil, huma.Error500InternalServerError(err.Error())
        }

        return nil, nil
    })
}
```

## Huma 入出力型パターン

```go
// server/internal/api/huma/types.go

// 入力型
type CreateEntityInput struct {
    Body struct {
        Name  string `json:"name" required:"true"`
        Email string `json:"email" required:"true"`
    }
}

type GetEntityInput struct {
    ID int64 `path:"id"`
}

type ListEntitiesInput struct {
    Limit  int `query:"limit" default:"10"`
    Offset int `query:"offset" default:"0"`
}

type UpdateEntityInput struct {
    ID   int64 `path:"id"`
    Body struct {
        Name  string `json:"name"`
        Email string `json:"email"`
    }
}

type DeleteEntityInput struct {
    ID int64 `path:"id"`
}

// 出力型
type EntityOutput struct {
    Body model.Entity
}

type EntitiesOutput struct {
    Body []*model.Entity
}
```

## Service パターン

```go
package service

import (
    "context"

    "github.com/example/go-webdb-template/internal/model"
    "github.com/example/go-webdb-template/internal/repository"
)

type EntityService struct {
    entityRepo *repository.EntityRepository
}

func NewEntityService(entityRepo *repository.EntityRepository) *EntityService {
    return &EntityService{
        entityRepo: entityRepo,
    }
}

func (s *EntityService) CreateEntity(ctx context.Context, req *model.CreateEntityRequest) (*model.Entity, error) {
    return s.entityRepo.Create(ctx, req)
}

func (s *EntityService) GetEntity(ctx context.Context, id int64) (*model.Entity, error) {
    return s.entityRepo.GetByID(ctx, id)
}

// ListEntities, UpdateEntity, DeleteEntity も同様...
```

## ルーターへの登録

`router.go` でエンドポイントを登録:

```go
// Humaエンドポイントの登録
handler.RegisterUserEndpoints(humaAPI, userHandler)
handler.RegisterPostEndpoints(humaAPI, postHandler)
handler.RegisterEntityEndpoints(humaAPI, entityHandler)  // 新規追加
```

## エラーレスポンス

```go
// 404 Not Found
return nil, huma.Error404NotFound(err.Error())

// 500 Internal Server Error
return nil, huma.Error500InternalServerError(err.Error())

// 400 Bad Request
return nil, huma.Error400BadRequest("Invalid input")
```
