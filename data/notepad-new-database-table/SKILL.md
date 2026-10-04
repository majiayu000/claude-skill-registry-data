---
name: notepad-new-database-table
description: "Reference doc: New Database Table Checklist"
---

# New Database Table Checklist

Use this notepad when adding a new database table/model to simpler-grants-gov.

## Model Definition

```python
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import ApiSchemaTable, TimestampMixin

class MyEntity(ApiSchemaTable, TimestampMixin):
    __tablename__ = "my_entity"  # ALWAYS singular

    my_entity_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)  # Boolean prefix: is_*

    # Relationships — ALWAYS use back_populates (never backref)
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("api.parent.parent_id"), nullable=False, index=True
    )
    parent: Mapped["Parent"] = relationship(back_populates="my_entities")
```

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Table name | Singular | `"user"` not `"users"` |
| Primary key | `<singular_table>_id` | `user_id` |
| Lookup table | `lk_` prefix | `"lk_status"` |
| Link/junction table | `link_` prefix | `"link_role_privilege"` |
| Boolean column | `is_*`, `has_*`, `can_*` | `is_deleted`, `has_attachment` |

## Column Syntax

ALWAYS use SQLAlchemy 2.0 syntax:
```python
# Correct — Mapped[T] with mapped_column()
name: Mapped[str] = mapped_column(sa.Text, nullable=False)
optional_field: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

# WRONG — legacy Column() syntax
name = Column(String, nullable=False)  # NEVER do this
```

## Lookup Table Pattern (four layers)

```python
# 1. StrEnum
class EntityStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# 2. LookupConfig
ENTITY_STATUS_CONFIG = LookupConfig([
    LkEntityStatus(description="Active"),
    LkEntityStatus(description="Inactive"),
])

# 3. LookupTable model
class LkEntityStatus(LookupTable):
    __tablename__ = "lk_entity_status"

# 4. LookupColumn on parent model
status: Mapped[EntityStatus] = mapped_column(
    "status", LookupColumn(LkEntityStatus), nullable=False
)
```

New enum values do NOT need a migration — they sync automatically.

## Migration

```python
"""Add my_entity table"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        "my_entity",
        sa.Column("my_entity_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.true()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        schema="api",  # ALWAYS specify schema
    )

def downgrade():
    op.drop_table("my_entity", schema="api")
```

## Factory

```python
class MyEntityFactory(BaseFactory):
    class Meta:
        model = MyEntity

    my_entity_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("company")
    is_active = True
```

## Soft Deletes

For user-facing deletion, use soft delete pattern:
```python
is_deleted: Mapped[bool] = mapped_column(default=False)
```
Filter in queries: `.where(MyEntity.is_deleted == False)`

## Don't Forget

- [ ] Inherits `ApiSchemaTable` + `TimestampMixin`
- [ ] UUID primary key with `default=uuid.uuid4`
- [ ] Singular table name
- [ ] `Mapped[T]` syntax (not legacy `Column()`)
- [ ] Relationships use `back_populates=`
- [ ] Migration specifies `schema="api"`
- [ ] Migration has both `upgrade()` and `downgrade()`
- [ ] Factory created in test factories
- [ ] Booleans use `is_*`/`has_*` prefixes
