---
name: rule-api-database
description: MANDATORY when editing files matching ["api/src/db/**/*.py"]. When working on database models, migrations, or queries in api/src/db/
---

# API Database Rules

## Model Definition

ALWAYS inherit from both `ApiSchemaTable` and `TimestampMixin` for every model in the `api` schema.

Example from codebase:
```python
# From api/src/db/models/
class ExcludedOpportunityReview(ApiSchemaTable, TimestampMixin):
    __tablename__ = "excluded_opportunity_review"
    opportunity_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
```

## UUID Primary Keys

ALWAYS use `uuid.UUID` primary keys with `default=uuid.uuid4` for new tables. NEVER use `BigInteger` primary keys for new API-schema tables. ALWAYS name the primary key `<singular_table_name>_id`.

Example from codebase:
```python
class Role(ApiSchemaTable, TimestampMixin):
    __tablename__ = "role"
    role_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
```

## Table Naming

ALWAYS use singular table names. ALWAYS prefix lookup tables with `lk_` and many-to-many link tables with `link_`.

Example from codebase:
```python
__tablename__ = "sam_extract_file"      # singular
__tablename__ = "lk_privilege"          # lookup prefix
__tablename__ = "link_role_privilege"   # link prefix
```

## Column Annotations

ALWAYS use SQLAlchemy 2.0 `Mapped[T]` with `mapped_column()`. Use `Mapped[T | None]` for nullable columns. NEVER use legacy `Column()` syntax.

Example from codebase:
```python
user_id: Mapped[uuid.UUID] = mapped_column(
    UUID, ForeignKey("api.user.user_id"), nullable=False, index=True
)
target_user_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID, ForeignKey("api.user.user_id"), index=True
)
```

## Relationships

ALWAYS use `back_populates=` for bidirectional relationships. NEVER use `backref=`. Parent-to-children MUST include `uselist=True` and `cascade="all, delete-orphan"`.

Example from codebase:
```python
organization_audits: Mapped[list[OrganizationAudit]] = relationship(
    "OrganizationAudit", uselist=True, back_populates="organization",
    cascade="all, delete-orphan",
)
```

## Foreign Key Columns

ALWAYS include `index=True` on foreign key columns. NEVER add `index=True` on primary key columns.

## Lookup Tables

ALWAYS implement lookups using the four-layer pattern: (1) `StrEnum` in `lookup_constants.py`, (2) `LookupConfig` with `LookupStr` entries in `lookup_models.py`, (3) `LookupTable` model with `@LookupRegistry.register_lookup()`, (4) `LookupColumn` on referencing models. NEVER create Alembic migrations for new lookup values -- `sync_lookup_values()` handles this automatically.

Example from codebase:
```python
# Layer 1: api/src/constants/lookup_constants.py
class SamGovProcessingStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"

# Layer 4: referencing model
processing_status: Mapped[SamGovProcessingStatus] = mapped_column(
    "processing_status_id",
    LookupColumn(LkSamGovProcessingStatus),
    ForeignKey(LkSamGovProcessingStatus.sam_gov_processing_status_id),
    index=True,
)
```

## Boolean Comparisons

ALWAYS use `Model.column.is_(True)` or `Model.column.is_(False)`. NEVER use `== True` or `== False`.

Example from codebase:
```python
existing_workflow = db_session.scalar(
    select(Workflow).where(
        Workflow.workflow_type == workflow_type,
        Workflow.is_active.is_(True),
    )
)
```

## Timestamps

ALWAYS use `datetime_util.utcnow()` for timestamps. NEVER use `datetime.now()` or `datetime.utcnow()`.

Example from codebase:
```python
from src.util import datetime_util
current_date = datetime_util.utcnow().date()
```

## UUID Assignment

ALWAYS set UUID primary keys explicitly at object creation. NEVER call `db_session.flush()` solely to get auto-generated IDs.

Example from codebase:
```python
extract = SamExtractFile(
    extract_type=SamGovExtractType.MONTHLY,
    sam_extract_file_id=uuid.uuid4(),
)
```

## Transaction Wrapping

ALWAYS wrap database operations in `with db_session.begin():`. NEVER perform DB reads or writes outside an explicit transaction context.

## ORM Relationships

ALWAYS set SQLAlchemy relationships (e.g., `application.submitted_by_user = user`). NEVER directly set foreign keys (e.g., `application.submitted_by = user.user_id`).

## Association Proxy

ALWAYS use `association_proxy` for many-to-many relationships through link/lookup tables.

Example from codebase:
```python
privileges: AssociationProxy[set[Privilege]] = association_proxy(
    "link_privileges", "privilege",
    creator=lambda obj: LinkRolePrivilege(privilege=obj),
)
```

## Migration File Naming

ALWAYS name migrations as `YYYY_MM_DD_<descriptive_slug>.py`. ALWAYS specify `schema="api"` or `schema="staging"` in all migration operations. ALWAYS use `op.f()` for constraint names.

Example from codebase:
```python
op.create_table(
    "role",
    sa.Column("role_id", sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint("role_id", name=op.f("role_pkey")),
    schema="api",
)
```

## Data Migrations

ALWAYS use `op.execute(text("...").params(...))` with bind parameters. ALWAYS use `NOT EXISTS` guards for idempotency.

## Composite Keys

NEVER add a separate unique constraint on a composite primary key -- it already enforces uniqueness.

## Legacy Data

NEVER make legacy integer ID columns foreign keys. Store them as plain indexed columns.

## Model Registration

ALWAYS register new model files in `api/src/db/models/__init__.py`. Unregistered models will not be detected by Alembic.

## Testing

ALWAYS define factories in `api/tests/src/db/models/factories.py`. Use `factory.SubFactory()` for relationships, `Generators.UuidObj` for UUIDs, and `factory.Trait()` for variants.

Example from codebase:
```python
class OrganizationAuditFactory(BaseFactory):
    class Meta:
        model = entity_models.OrganizationAudit
    organization_audit_id = Generators.UuidObj
    user = factory.SubFactory(UserFactory, with_profile=True)
    user_id = factory.LazyAttribute(lambda u: u.user.user_id)
```

---

## Context Enrichment

When generating significant database code (new model, new migration, complex queries), enrich your context:
- Call `get_architecture_section("database")` from the `simpler-grants-context` MCP server to understand database architectural principles
- Call `get_rule_detail("api-services")` for service layer query patterns that interact with models
- Consult **Compound Knowledge** for indexed documentation on schema evolution patterns, migration history, and database ADRs

## Related Rules

When working on database models and migrations, also consult these related rules:
- **`api-services.mdc`** — service layer query patterns, `scalar_one_or_none()`, relationship loading
- **`api-error-handling.mdc`** — error patterns for database-related failures
- **`api-search.mdc`** — OpenSearch index models that mirror database models
- **`cross-domain.mdc`** — boolean naming (`is_*`, `has_*`), structured logging, factory patterns

## Specialist Validation

When generating or significantly modifying database code:

**For simple changes (< 20 lines, adding a column):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new model, new relationship, lookup table):**
Invoke `codebase-conventions-reviewer` to validate against database conventions.

**For complex changes (new table with relationships, migration with data transforms, schema refactor):**
Invoke the following specialists (run in parallel where possible):
- `data-integrity-guardian` — validate data safety, relationship correctness, foreign key integrity
- `schema-drift-detector` — validate schema consistency between model, migration, and Marshmallow schemas
- `kieran-python-reviewer` — Python-specific quality review for SQLAlchemy patterns

<!-- Hook enforcement: convention-checker validates Mapped[T]/mapped_column(), no raw SQL, back_populates, schema='api' in migrations -->
