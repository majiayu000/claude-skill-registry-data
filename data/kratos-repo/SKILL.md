---
name: kratos-repo
description: Implements go-kratos data layer repositories following Clean Architecture patterns with GORM, transactions, pagination, and error handling. Use when adding new data access layers to kratos microservices that need database persistence.
---

# Kratos Repository Implementation Skill

## Purpose

Generate repository implementations that handle data persistence using GORM while adhering to Clean Architecture principles. Repositories implement interfaces defined in the business layer (\`biz\`).

## Essential Patterns

### 1. Repository Structure

```go
package repo

import (
    "context"
    "platform/pagination"
    "{service}/internal/biz/domain"
    "{service}/internal/data/model"
    "github.com/go-kratos/kratos/v2/log"
    "gorm.io/gorm"
)

// Constructor function
func New{Entity}Repo(db *gorm.DB, tx common.Transaction, logger log.Logger) domain.{Entity}Repo {
    return &{entity}Repo{
        db:  db,
        tx:  tx,
        log: log.NewHelper(logger),
    }
}

// Private struct
type {entity}Repo struct {
    db  *gorm.DB
    tx  common.Transaction
    log *log.Helper
}
```

### 2. CRUD Operations Pattern

#### Create Operation
```go
func (r *{entity}Repo) Create(ctx context.Context, s *domain.{Entity}) (*domain.{Entity}, error) {
    entity := toEntity{Entity}(s)
    
    // Use FullSaveAssociations for nested relationships
    if err := r.db.WithContext(ctx).Session(&gorm.Session{FullSaveAssociations: true}).Create(entity).Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to save {entity}: %v", err)
        return nil, r.mapGormError(err)
    }
    
    return toDomain{Entity}(entity), nil
}
```

#### Update Operation
```go
func (r *{entity}Repo) Update(ctx context.Context, entity *domain.{Entity}) (*domain.{Entity}, error) {
    // Transform to GORM entity
    e := toEntity{Entity}(entity)
    
    // Update with FullSaveAssociations
    result := r.db.WithContext(ctx).Session(&gorm.Session{FullSaveAssociations: true}).Model(&model.{Entity}{}).Where("id = ?", entity.Id).Updates(e)
    if result.Error != nil {
        return nil, r.mapGormError(result.Error)
    }
    if result.RowsAffected == 0 {
        return nil, biz.ErrNotFound
    }
    
    // Return fresh data
    return r.FindByID(ctx, entity.Id)
}
```

#### FindByID Operation
```go
func (r *{entity}Repo) FindByID(ctx context.Context, id uint64) (*domain.{Entity}, error) {
    var entity *model.{Entity}
    
    err := r.db.WithContext(ctx).
        Preload("{RelationshipField}").  // Preload relationships
        Where("id = ?", id).
        First(&entity).Error
    
    if err != nil {
        r.log.WithContext(ctx).Errorf("Failed to find {entity} by ID %d: %v", id, err)
        return nil, r.mapGormError(err)
    }
    
    return toDomain{Entity}(entity), nil
}
```

#### List with Pagination and Filters
```go
func (r *{entity}Repo) List{Entities}(ctx context.Context, offset uint64, limit uint32, filter map[string]interface{}) ([]*domain.{Entity}, *pagination.Meta, error) {
    var entities []*model.{Entity}
    var totalCount int64
    
    // Base query
    query := r.db.WithContext(ctx).Model(&model.{Entity}{})
    
    // Apply filters BEFORE count and find
    if filter != nil && len(filter) > 0 {
        query = query.Where(filter)
    }
    
    // Count with filters applied
    if err := query.Count(&totalCount).Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to count: %v", err)
        return nil, nil, r.mapGormError(err)
    }
    
    // Apply pagination
    query = query.Limit(int(limit)).Offset(int(offset))
    
    // Execute query
    if err := query.Find(&entities).Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to list: %v", err)
        return nil, nil, r.mapGormError(err)
    }
    
    // Transform to domain
    results := make([]*domain.{Entity}, 0, len(entities))
    for _, e := range entities {
        results = append(results, toDomain{Entity}(e))
    }
    
    // Build metadata
    meta := &pagination.Meta{
        TotalCount:      uint64(totalCount),
        Offset:          offset,
        Limit:           limit,
        HasNextPage:     offset+uint64(len(entities)) < uint64(totalCount),
        HasPreviousPage: offset > 0,
    }
    
    return results, meta, nil
}
```

#### Delete Operation
```go
func (r *{entity}Repo) Delete(ctx context.Context, id uint64) error {
    result := r.db.WithContext(ctx).Delete(&model.{Entity}{}, id)
    if result.Error != nil {
        r.log.WithContext(ctx).Errorf("Failed to delete: %v", result.Error)
        return r.mapGormError(result.Error)
    }
    if result.RowsAffected == 0 {
        return domain.ErrDataNotFound
    }
    return nil
}
```

### 3. Error Mapping Pattern

CRITICAL: Always map GORM errors to data layer errors (not business errors)

```go
func (r *{entity}Repo) mapGormError(err error) error {
    if err == nil {
        return nil
    }

    // Map GORM errors to data layer errors
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return domain.ErrDataNotFound
    }

    if r.isDuplicateKeyError(err) {
        return domain.ErrDataDuplicateEntry
    }

    // Wrap other database errors
    return domain.ErrDataDatabase
}

// isDuplicateKeyError checks if error is a duplicate key violation
func (r *{entity}Repo) isDuplicateKeyError(err error) bool {
    errMsg := err.Error()
    return strings.Contains(errMsg, "Error 1062") ||
        strings.Contains(errMsg, "Duplicate entry") ||
        strings.Contains(errMsg, "UNIQUE constraint failed")
}
```

**Data Layer Error Types:**
- `domain.ErrDataNotFound` - Record not found
- `domain.ErrDataDuplicateEntry` - Unique constraint violation
- `domain.ErrDataTransactionFailed` - Transaction operation failed
- `domain.ErrDataDatabase` - Generic database error

**NOTE**: These are data layer errors. The business layer (use case) will map these to domain-specific errors (e.g., `domain.ErrSymbolNotFound`, `domain.ErrDuplicateSymbol`)

### 4. Mapper Functions

Always provide bidirectional mappers between domain and entity:

```go
// Domain to Entity
func toEntity{Entity}(d *domain.{Entity}) *model.{Entity} {
    if d == nil {
        return nil
    }
    
    entity := &model.{Entity}{
        ProjectID: d.Project,
        Field1:    d.Field1,
        Field2:    d.Field2,
    }
    
    // Handle nested relationships
    if d.RelatedData != nil {
        entity.RelatedData = &model.RelatedData{
            Field: d.RelatedData.Field,
            Data:  d.RelatedData.Data,
        }
    }
    
    return entity
}

// Entity to Domain
func toDomain{Entity}(e *model.{Entity}) *domain.{Entity} {
    if e == nil {
        return nil
    }
    
    domain := &domain.{Entity}{
        Id:      e.ID,
        Project: e.ProjectID,
        Field1:  e.Field1,
        Field2:  e.Field2,
    }
    
    // Handle nested relationships
    if e.RelatedData != nil {
        domain.RelatedData = &domain.RelatedData{
            Id:      e.RelatedData.ID,
            Project: e.RelatedData.ProjectID,
            Field:   e.RelatedData.Field,
            Data:    e.RelatedData.Data,
        }
    }
    
    return domain
}
```

## Critical Rules

### Context Propagation
ALWAYS use \`WithContext(ctx)\` for all database operations:
```go
r.db.WithContext(ctx).Find(&entities)  // ✅ Correct
r.db.Find(&entities)                    // ❌ Wrong - no context
```

### FullSaveAssociations
Use for Create/Update operations with nested relationships:
```go
Session(&gorm.Session{FullSaveAssociations: true})
```

### Filter Application
Apply filters BEFORE both count and find queries:
```go
query := r.db.WithContext(ctx).Model(&model.Entity{})
if filter != nil && len(filter) > 0 {
    query = query.Where(filter)  // Apply first
}
query.Count(&totalCount)          // Count filtered results
query.Limit(...).Find(&entities)  // Find filtered results
```

### Error Handling
1. Log all errors with context
2. Map GORM errors to business errors
3. Check RowsAffected for Update/Delete operations

### Logging Pattern
```go
r.log.WithContext(ctx).Errorf("Failed to {operation}: %v", err)
```

## File Structure

```
services/{service}/internal/data/repo/
├── {entity}.go              # Repository implementation
├── {entity}_test.go         # Repository tests
└── mapper.go or helpers     # Optional separate mapper file
```

## Validation Checklist

- [ ] Constructor function returns interface type (\`domain.{Entity}Repo\`)
- [ ] All DB operations use \`WithContext(ctx)\`
- [ ] Create/Update use \`FullSaveAssociations\` if nested data exists
- [ ] Update checks \`RowsAffected == 0\` for not found
- [ ] Delete checks \`RowsAffected == 0\` for not found
- [ ] All errors are logged with context
- [ ] GORM errors are mapped to data layer errors (\`domain.ErrData*\`)
- [ ] FindByID preloads related entities
- [ ] List applies filters before count and find
- [ ] List returns pagination metadata
- [ ] Mappers handle nil inputs safely
- [ ] Mappers transform nested relationships

## Anti-Patterns

❌ **DON'T:**
- Return GORM errors directly (must map to \`domain.ErrData*\`)
- Forget context propagation (\`WithContext\`)
- Apply filters only to find, not count
- Ignore \`RowsAffected\` in Update/Delete
- Use value receivers (use pointer receivers)
- Forget to preload relationships in FindByID
- Return business errors from repo (return data layer errors instead)

✅ **DO:**
- Implement interface defined in \`biz/domain/interfaces.go\`
- Always map GORM errors to data layer errors (\`domain.ErrData*\`)
- Use context for all database operations
- Apply filters to both count and find queries
- Check \`RowsAffected\` for Update/Delete
- Use pointer receivers for struct methods
- Preload relationships when needed
- Let business layer map data errors to domain errors

## Success Criteria

Repository MUST:
1. Implement all methods from business layer interface
2. Pass all unit tests with proper error handling
3. Support soft deletes (via BaseModel)
4. Handle pagination correctly with accurate metadata
5. Transform all data between entity and domain models
6. Log errors appropriately with context
7. Map all GORM errors to business errors

