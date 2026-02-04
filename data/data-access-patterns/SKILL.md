---
name: data-access-patterns
description: Guidelines for database interactions using raw SQL and idiomatic Go patterns
---

# Data Access Patterns Skill

Use this skill when writing or modifying database access code in `internal/models/`.

This project uses explicit SQL over ORMs for performance, readability, and fine-grained control.

---

## Core Principles

- **No ORM**: Use `database/sql` directly. Do NOT introduce or use any ORM.
- **PostgreSQL Driver**: The project uses `github.com/lib/pq` (imported in `internal/db/db.go`).
- **Raw SQL**: Write explicit, readable SQL queries. Use PostgreSQL-specific features (JSONB, ON CONFLICT) and `$1, $2` placeholders.
- **Transactional Integrity**: Use `*sql.Tx` when multiple operations must complete together or fail (atomicity).
- **Separation of Concerns**: Keep database models and access logic in `internal/models/`. Repository functions should focus on data retrieval and persistence.

---

## Repository Function Naming

| Pattern | Purpose | Example Signature |
|---------|---------|-------------------|
| `Get[Entity]ById` | Retrieve a single entity | `GetWeaponById(db *sql.DB, id string) (*Weapon, error)` |
| `Get[Entities]By[Field]` | Filtered retrieval | `GetTraderOffersByItemID(db *sql.DB, itemID string) ([]TraderOffer, error)` |
| `Upsert[Entity]` | Insert or update one record | `UpsertWeapon(tx *sql.Tx, weapon Weapon) error` |
| `UpsertMany[Entity]` | Batch insert/update | `UpsertManyWeapon(tx *sql.Tx, weapons []Weapon) error` |
| `Purge[Entity]` | Clean up records | `PurgeOptimumBuilds(db *sql.DB) error` |

---

## Writing Efficient Queries

### JSONB for Complex Trees
When fetching an entity with nested children (e.g., a weapon with many slots), use `jsonb_agg` and `jsonb_build_object` to minimize round-trips and simplify Go-side scanning.

```go
// Example: Single query to fetch weapon and all its slots
query := `
    SELECT w.name,
           w.item_id,
           jsonb_agg(jsonb_build_object(
               'slot_id', ws.slot_id, 
               'name', ws.name
           )) as slots
    FROM weapons w
    JOIN slots ws ON w.item_id = ws.item_id
    WHERE w.item_id = $1
    GROUP BY w.name, w.item_id;`
```

### Idempotent Writes (`ON CONFLICT`)
Prefer `ON CONFLICT` for upsert operations to ensure idempotency and handle existing records gracefully.

```go
query := `
    INSERT INTO weapons (item_id, name)
    VALUES ($1, $2)
    ON CONFLICT (item_id) DO UPDATE SET
        name = EXCLUDED.name;`
```

---

## Transaction Management Checklist

When implementing writes:

1.  **Composite Writes**: If a function calls multiple other write functions (e.g., `UpsertWeapon` calling `upsertManySlot`), it MUST accept a `*sql.Tx`.
2.  **Top-Level Orchestration**: Start the transaction at the highest possible level (usually in the importer or service layer).
3.  **Defer Rollback**: Defer a rollback immediately after starting a transaction to prevent leaks on error.

```go
tx, err := db.Begin()
if err != nil {
    return err
}
defer tx.Rollback() // Safe: does nothing if committed

if err := UpsertManyWeapon(tx, weapons); err != nil {
    return err
}

return tx.Commit()
```

---

## Developer Best Practices

- ✅ **Explicit Scanning**: Scan rows into structs carefully; match types exactly with the DB schema.
- ✅ **Resource Management**: `defer rows.Close()` immediately after a `Query` call.
- ✅ **Strict Errors**: Check errors after `rows.Scan()` AND after the loop with `rows.Err()`.
- ✅ **Clean Signatures**: Pass `*sql.DB` for read-only operations and `*sql.Tx` for multi-step write operations.
- ❌ **Avoid SELECT ***: Explicitly list required columns to prevent breakage from schema changes.
- ❌ **No Global DB**: Pass the database handle as an argument.
