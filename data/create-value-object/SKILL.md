---
name: create-value-object
description: Create Value Object for domain modeling following DDD patterns. Use when you need to encapsulate primitive values with validation, business rules, and immutability. Creates reusable VOs like PriceField, EmailField, QuantityField with validation and domain logic.
---

# Create Value Object

Generate immutable Value Object with validation and business rules.

---

## When to Use

- Encapsulate primitive values (string, int, float)
- Add validation to domain values
- Avoid primitive obsession
- Create reusable domain concepts

---

## Inputs/Outputs

| Input | Example | Output |
|-------|---------|--------|
| name | PriceField | `Shared/Entities/VO/ValueObjectName.php` (if shared) |
| type | string, int | `BC/Entities/VO/ValueObjectName.php` (if BC-specific) |
| validation | ['min' => 0] | - |
| location | Shared, Admin | - |

---

## Process

| Step | Action |
|------|--------|
| **Create** | Use template: `value-object.php.tpl` |
| **Validate** | `make cs-fixer && make stan` |

---

## Structure

**Value Object** (`final readonly`, private constructor, static factory):
```php
final readonly class ValueObjectName {
    private function __construct(private TypeHere $value) {}

    public static function fromString(string $value): self {
        if (empty($value)) {
            throw InvalidValueObject::empty();
        }
        return new self($value);
    }

    public function toString(): string { return $this->value; }
    public function equals(self $other): bool { return $this->value === $other->value; }
}
```

**See**: `docs/GLOSSARY.md#value-object` for detailed definition

---

## Rules

**Class Structure**:
- `final readonly` class, private constructor
- Static factory: `fromString()`, `fromInt()`, `fromCents()`, etc.
- Immutable (no setters)

**Validation**:
- In factory method
- Throw domain exceptions (not generic)
- Clear error messages

**Methods**:
- Getter: `toString()`, `toInt()`, `toFloat()`
- Comparison: `equals()`, `isGreaterThan()`, etc.
- Business logic if needed (e.g., `add()`, `multiply()`)

**Location Decision**:
- `Shared/Entities/VO/` if used across multiple BCs (ResourceUuid, EmailField, NameField, PriceField)
- `BC/Entities/VO/` if BC-specific only (ArticleReference, SupplierCode, TaxRate)

---

## Templates

- `value-object.php.tpl`

**Location**: `.claude/templates/`

---

## References

- Value Object definition: `docs/GLOSSARY.md#value-object`
- Value Object pattern: `docs/QUICK_REF.md#value-object-pattern`
- Architecture: `docs/architecture.md#value-objects`
- Shared VOs: `src/Shared/Entities/VO/`

---

## Related Skills

- `create-entity` - Use VOs in entities
- `create-use-case` - Pass VOs in requests
