---
name: eloquent-patterns
description: Laravel guidance to keep Eloquent models explicit, query shapes intentional, relationship loading visible, and production data access bounded.
tags:
  - laravel
  - php
---

# Eloquent Patterns

Keep models explicit, query shape intentional, and relationship loading visible near the code that renders or returns data.

## Model Contracts

Models should declare mass-assignment boundaries, casts, and concrete relationship return types.

```php
class Record extends Model
{
    protected $fillable = [
        'owner_id',
        'number',
        'total',
        'issued_at',
        'is_active',
    ];

    protected function casts(): array
    {
        return [
            'issued_at' => 'date',
            'total' => 'decimal:2',
            'is_active' => 'boolean',
            'metadata' => 'array',
        ];
    }

    public function owner(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

Use accessors sparingly for simple derived values. Move heavy behavior into Actions or Services.

## Relationship Loading

Prevent N+1 queries by eager loading the relations a surface needs.

Before rendering Blade reports, printable views, exports, or PDFs, explicitly load the relation graph.

```php
public function show(Record $record): View
{
    $record->load([
        'owner',
        'items.product',
        'approvals.user',
    ]);

    return view('records.show', ['record' => $record]);
}
```

Do not add new relation dependencies inside templates without updating the load list and render tests.

## Query Volume

Do not process unbounded production datasets with `all()` or broad `get()` calls.

Use:

- `paginate()` for normal UI/API lists;
- cursor pagination for large append-only lists;
- `chunkById()` or `lazyById()` when updating rows during iteration;
- `cursor()` or lazy collections for streaming;
- selected columns and indexed filters for high-volume paths.

## Bounded Values

Keep bounded validation/display values in one source of truth.

Prefer enums when supported.

```php
enum RecordStatus: string
{
    case Draft = 'draft';
    case Approved = 'approved';
    case Cancelled = 'cancelled';

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Draft',
            self::Approved => 'Approved',
            self::Cancelled => 'Cancelled',
        };
    }
}
```

Use config files for deployment-level options and constants for small legacy/model-owned maps.

## Historical Data

Use soft deletes with `withTrashed()` when historical records must remain readable after related reference data is removed from active use.

Do not use this as a blanket rule for personal data or records subject to hard-delete compliance.

Snapshot attributes that must remain true for a historical document.

```php
DocumentLine::create([
    'reference_id' => $reference->id,
    'reference_snapshot' => $reference->only(['code', 'name']),
]);
```

Store only fields needed for historical correctness and avoid unnecessary sensitive data.

## Context Efficiency

Layer: 3 (Implementation)

Load this skill only when models or queries need review. Do not load with unrelated skills. Keep changes minimal: explicit casts, eager-loaded relations, paginated queries, no unbounded `all()` or broad `get()` in production paths.
