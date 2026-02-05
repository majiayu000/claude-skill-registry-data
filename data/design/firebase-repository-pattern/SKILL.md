---
name: "Firebase Repository Pattern"
description: "Generate Firebase Repository classes following the project's three-layer architecture (UI → Service → Repository). Use this skill when creating data access layers for Firestore collections, implementing CRUD operations with proper error handling, exponential backoff retry logic, and type-safe entity mapping. This skill ensures repositories extend FirestoreBaseRepository, inject @angular/fire services directly (no FirebaseService wrapper), and follow the Result Pattern for async operations."
license: "MIT"
---

# Firebase Repository Pattern Skill

This skill helps create Firebase Repository classes that follow the ng-lin project's architectural standards.

## Core Principles

### Architecture Compliance
- **Three-Layer Architecture**: UI → Service → Repository
- **Direct Injection**: Use `@angular/fire` services (Firestore, Auth, Storage) directly
- **No Wrappers**: Never create FirebaseService or similar wrappers
- **Repository Responsibility**: Only handle data access, no business logic

### Key Requirements

1. **Extend FirestoreBaseRepository<T>**
   - All repositories must extend the base repository class
   - Provides built-in retry logic with exponential backoff
   - Automatic error handling and logging
   - Performance tracking

2. **Use inject() for Dependency Injection**
   - Angular 20+ pattern: `private firestore = inject(Firestore)`
   - Never use constructor injection
   - Follow modern Angular DI patterns

3. **Type Safety**
   - Define TypeScript interfaces for domain entities
   - Implement toEntity() and toDocument() methods
   - Use DocumentData for Firestore documents

4. **Error Handling**
   - Use executeWithRetry() for all operations
   - Implement proper error logging
   - Return Result Pattern for service layer

## Repository Template Structure

```typescript
import { Injectable, inject } from '@angular/core';
import { Firestore, collection, query, where, getDocs, addDoc, updateDoc, deleteDoc, doc } from '@angular/fire/firestore';
import { FirestoreBaseRepository } from '../base/firestore-base.repository';
import { YourEntity } from '@core/domain/models/your-entity.model';

@Injectable({ providedIn: 'root' })
export class YourEntityRepository extends FirestoreBaseRepository<YourEntity> {
  protected collectionName = 'your_collection';
  
  private firestore = inject(Firestore);
  
  /**
   * Convert Firestore document to domain entity
   */
  protected toEntity(data: DocumentData, id: string): YourEntity {
    return {
      id,
      // Map Firestore fields to entity properties
      // Handle snake_case to camelCase conversion
      // Convert Timestamp to Date
      createdAt: this.toDate(data['created_at']),
      updatedAt: this.toDate(data['updated_at']),
      deletedAt: data['deleted_at'] ? this.toDate(data['deleted_at']) : null
    };
  }
  
  /**
   * Convert domain entity to Firestore document
   */
  protected override toDocument(entity: Partial<YourEntity>): DocumentData {
    const doc: DocumentData = {};
    
    // Map entity properties to Firestore fields
    // Handle camelCase to snake_case conversion
    // Convert Date to Timestamp
    
    return doc;
  }
  
  /**
   * Find by Blueprint ID (multi-tenancy pattern)
   */
  async findByBlueprintId(blueprintId: string): Promise<YourEntity[]> {
    return this.executeWithRetry(async () => {
      const q = query(
        collection(this.firestore, this.collectionName),
        where('blueprint_id', '==', blueprintId),
        where('deleted_at', '==', null)
      );
      return this.queryDocuments(q);
    });
  }
  
  // Additional query methods as needed
}
```

## Common Patterns

### Query with Filters
```typescript
async findByStatus(blueprintId: string, status: string): Promise<YourEntity[]> {
  return this.executeWithRetry(async () => {
    const q = query(
      collection(this.firestore, this.collectionName),
      where('blueprint_id', '==', blueprintId),
      where('status', '==', status),
      where('deleted_at', '==', null),
      orderBy('created_at', 'desc')
    );
    return this.queryDocuments(q);
  });
}
```

### Batch Operations
```typescript
async createBatch(entities: Array<Omit<YourEntity, 'id'>>): Promise<{
  succeeded: YourEntity[];
  failed: Array<{ entity: typeof entities[0]; error: string }>;
}> {
  const succeeded: YourEntity[] = [];
  const failed: Array<{ entity: typeof entities[0]; error: string }> = [];
  
  for (const entity of entities) {
    try {
      const created = await this.create(entity);
      succeeded.push(created);
    } catch (error) {
      failed.push({
        entity,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
  
  return { succeeded, failed };
}
```

## Multi-Tenancy (Blueprint Pattern)

All queries MUST include Blueprint context:

```typescript
// ✅ CORRECT: Include blueprint_id filter
where('blueprint_id', '==', blueprintId)

// ✅ CORRECT: Exclude soft-deleted items
where('deleted_at', '==', null)

// ❌ WRONG: Global queries without blueprint context
// This violates multi-tenancy security
```

## File Location

Place repositories in:
- **Shared**: `src/app/core/data-access/shared/{entity}.repository.ts`
- **Module-specific**: `src/app/core/data-access/{module}/{entity}.repository.ts`

## Security Integration

Repositories work with Firestore Security Rules:

1. **Repository**: Handles data access only
2. **Security Rules**: Validates permissions server-side
3. **Service**: Contains business logic and permission checks

```typescript
// Repository - No permission checks
async delete(id: string): Promise<void> {
  return this.executeWithRetry(async () => {
    return this.deleteDocument(id, false); // Soft delete
  });
}
```

```javascript
// Security Rules - Permission validation
match /your_collection/{docId} {
  allow delete: if isAuthenticated() 
                && isBlueprintMember(resource.data.blueprint_id)
                && hasPermission(resource.data.blueprint_id, 'entity:delete');
}
```

## Testing

```typescript
describe('YourEntityRepository', () => {
  let repository: YourEntityRepository;
  
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [YourEntityRepository]
    });
    repository = TestBed.inject(YourEntityRepository);
  });
  
  it('should create entity with timestamps', async () => {
    const entity = { blueprintId: 'test', name: 'Test' };
    const result = await repository.create(entity);
    
    expect(result.id).toBeDefined();
    expect(result.createdAt).toBeInstanceOf(Date);
    expect(result.updatedAt).toBeInstanceOf(Date);
  });
});
```

## Checklist

When creating a repository:

- [ ] Extends FirestoreBaseRepository<T>
- [ ] Uses inject() for Firestore
- [ ] Defines collectionName
- [ ] Implements toEntity() method
- [ ] Overrides toDocument() if needed
- [ ] Includes blueprint_id in all queries
- [ ] Filters deleted_at for active records
- [ ] Uses executeWithRetry() for operations
- [ ] No business logic in repository
- [ ] Proper TypeScript typing
- [ ] Unit tests included

## References

- [Repository Pattern Instructions](.github/instructions/ng-gighub-firestore-repository.instructions.md)
- [Architecture Guide](.github/instructions/ng-gighub-architecture.instructions.md)
- [Security Rules](.github/instructions/ng-gighub-security-rules.instructions.md)
