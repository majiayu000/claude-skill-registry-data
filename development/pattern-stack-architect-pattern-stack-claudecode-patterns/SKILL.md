---
name: pattern-stack-architect
description: Expert in Pattern Stack framework architecture. Auto-activates when writing backend code using Pattern Stack's Atomic Architecture, Field abstraction, and pattern composition system.
---

# Pattern Stack Architect Skill

Provides expert guidance on Pattern Stack framework architecture, ensuring correct usage of patterns, Field abstraction, layer boundaries, and architectural best practices.

## When This Skill Activates

- Writing SQLAlchemy models with Pattern Stack patterns
- Creating services, entities, or workflows
- Designing domain models for new features
- Reviewing code for Pattern Stack compliance
- Questions about pattern composition or layer structure
- Any mention of "pattern stack", "atomic architecture", "Field()", patterns

## Core Principles

### 1. Atomic Architecture (v2.5)

Pattern Stack uses a four-layer architecture:

```
Atoms (Foundation)
  ↓
Features (Data Services)
  ↓
Molecules (Business Logic)
  ↓
Organisms (API Layer)
```

**Layer Responsibilities:**

**Atoms**: Foundation infrastructure
- Patterns (BasePattern, CatalogPattern, ActorPattern, etc.)
- Database setup and connections
- Cache subsystem
- Event system
- Configuration
- Shared utilities

**Features**: Data-focused services (one per model)
- CRUD operations
- Data validation
- Database queries
- Service-level logic
- **NO cross-domain orchestration**

Example:
```python
# features/user_service.py
class UserService(BaseService):
    async def create(self, data: UserCreate) -> User:
        # Single-domain CRUD
        user = User(**data.model_dump())
        self.db.add(user)
        await self.db.commit()
        return user
```

**Molecules**: Business logic layer
- **Entities**: Single-domain business logic
- **Workflows**: Multi-domain orchestration
- Validation rules
- Business calculations
- Cross-service coordination

Example:
```python
# molecules/entities/user_entity.py
class UserEntity(BaseEntity):
    def _init_services(self):
        self.user_service = UserService(self.db)

    async def activate_user(self, user_id: UUID) -> User:
        # Single-domain business logic
        user = await self.user_service.get(user_id)
        user.status = "active"
        await self.user_service.update(user_id, user)
        return user

# molecules/workflows/onboarding_workflow.py
class OnboardingWorkflow:
    def _init_services(self):
        self.user_entity = UserEntity(self.db)
        self.notification_service = NotificationService(self.db)

    async def complete_onboarding(self, user_id: UUID) -> dict:
        # Multi-domain orchestration
        user = await self.user_entity.activate_user(user_id)
        await self.notification_service.send_welcome_email(user.email)
        return {"user": user, "email_sent": True}
```

**Organisms**: API and external interfaces
- FastAPI routers and endpoints
- Request/response models (Pydantic schemas)
- Authentication/authorization checks
- Thin layer - delegates to Molecules

### 2. Field Abstraction - NEVER Use mapped_column

**❌ WRONG - Don't do this:**
```python
from sqlalchemy.orm import Mapped, mapped_column

class User(BasePattern):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True)
```

**✅ CORRECT - Use Field():**
```python
from pattern_stack.atoms.patterns.fields import Field

class User(BasePattern):
    name = Field(str, required=True, max_length=255)
    email = Field(str, unique=True, max_length=320, index=True)
```

**Field() Benefits:**
- **Progressive enhancement**: Start simple, add constraints as needed
- **Type inference**: Python types → SQLAlchemy types automatically
- **Validation**: Built-in min/max, choices, length constraints
- **Cleaner syntax**: Less boilerplate

**Field() Examples:**

```python
# Simple fields
name = Field(str, required=True)
age = Field(int, min=0, max=150)
is_active = Field(bool, default=True)

# With validation
email = Field(str, max_length=320, unique=True, index=True)
price = Field(Decimal, min=0)
status = Field(str, choices=["draft", "published", "archived"])

# Relationships
user_id = Field(UUID, foreign_key="users.id", required=True)
category_id = Field(UUID, foreign_key="categories.id", nullable=True)

# JSON fields with defaults
tags = Field(list, default=[])  # Field() handles mutable defaults safely!
metadata = Field(dict, default={})
profile_data = Field(dict, default=dict)  # Also works

# Dates and times
created_at = Field(datetime, required=True)
birth_date = Field(date, nullable=True)
```

### 3. Pattern Composition

Pattern Stack provides 5 core patterns that compose via **multiple inheritance**:

**BasePattern** (Always included via inheritance)
- Provides: `id` (UUID), `created_at`, `updated_at`
- Change tracking and event emission
- Validation hooks

**CatalogPattern** - Inventory/resource management
- Provides: `name`, `sku`, `stock_quantity`, `reserved_quantity`, `price` fields
- Methods: `available_quantity`, `is_low_stock()`, `reserve_stock()`
- Use for: Products, equipment, digital assets

**ActorPattern** - Entities that perform actions
- Provides: `display_name`, `actor_type`, `email`, `phone`, `profile_data`
- Methods: `record_activity()`, `is_contactable()`, `get_activity_metrics()`
- Use for: Users, organizations, systems, services

**EventPattern** - State machines
- Provides: `state`, state transition validation, state history
- Define states in Pattern.states configuration
- Use for: Workflows, approval processes, lifecycle management

**TemporalPattern** - Time-based versioning
- Provides: `valid_from`, `valid_to`, `is_current`, version tracking
- Methods: Version queries, historical lookups
- Use for: Pricing history, deal stages, audit trails

**HierarchicalPattern** - Tree structures
- Provides: `parent_id`, `path`, `depth`, tree traversal
- Methods: `get_ancestors()`, `get_descendants()`, `get_siblings()`
- Use for: Categories, org charts, folder structures

**Composition Example:**

```python
# Single pattern
class Product(CatalogPattern):
    __tablename__ = "products"

    class Pattern:
        entity = "product"

    # CatalogPattern provides: name, sku, stock_quantity, etc.
    brand = Field(str, max_length=100, nullable=True)

# Multiple patterns
class User(ActorPattern, EventPattern):
    __tablename__ = "users"

    class Pattern:
        entity = "user"
        # EventPattern configuration
        states = {
            "pending": ["active", "rejected"],
            "active": ["suspended", "archived"],
            "suspended": ["active", "archived"]
        }
        initial_state = "pending"
        # ActorPattern configuration
        field_defaults = {"actor_type": "user"}

    # ActorPattern provides: display_name, email, phone, profile_data
    # EventPattern provides: state, state transitions
    role = Field(str, choices=["user", "admin", "moderator"], default="user")
```

### 4. Pattern Configuration

The `Pattern` inner class configures pattern behavior:

```python
class MyModel(BasePattern):
    class Pattern:
        # Entity name (used for events, table naming)
        entity = "my_model"

        # Reference number prefix (from ReferenceNumberMixin)
        reference_prefix = "MDL"

        # Change tracking
        track_changes = True  # Default: True
        change_retention = "365d"  # "365d", "2y", "forever"
        track_changes_fields = ["*"]  # Or specific fields
        track_changes_exclude = ["updated_at", "metadata"]

        # Field defaults (applied during __init__)
        field_defaults = {
            "status": "draft",
            "priority": 1,
            "created_date": lambda: datetime.now(UTC)  # Callable defaults
        }

        # Activity tracking (for ActorPattern)
        activity_triggers = ["login", "purchase", "upload"]

        # Typed JSON profiles (advanced)
        profile_type = "user_profile"  # Use built-in profile schema
        # OR
        profile_schema = MyPydanticSchema  # Custom Pydantic model
```

### 5. Automatic Features

Pattern Stack automatically provides:

**Change Tracking** (via EventPattern integration)
```python
# Changes are tracked automatically
user.name = "New Name"
await db.commit()  # Change event emitted automatically

# Query changes
changes = await user.get_changes(fields=["name"], limit=50)
history = await user.get_field_history("name")
```

**Event Emission**
```python
# Events fired automatically on create/update/delete
# Custom events via EventPattern
user.emit_event("user.login", metadata={"ip": "1.2.3.4"})
```

**Reference Numbers** (via ReferenceNumberMixin)
```python
# Automatically generated from prefix + sequential number
user.reference_number  # "USR-00001"
product.reference_number  # "PRD-00042"
```

**Validation** (always called before save)
```python
class MyModel(BasePattern):
    def validate(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
```

## Common Patterns

### Creating a New Model

```python
from pattern_stack.atoms.patterns.base import BasePattern
from pattern_stack.atoms.patterns.fields import Field
from uuid import UUID

class Account(BasePattern):
    __tablename__ = "accounts"

    class Pattern:
        entity = "account"
        reference_prefix = "ACC"
        track_changes = True
        change_retention = "365d"

    # Fields
    name = Field(str, required=True, max_length=255, index=True)
    stage = Field(str, default="prospect", choices=[
        "prospect", "qualifying", "demo", "proposal",
        "closing", "closed_won", "closed_lost"
    ])
    amount = Field(Decimal, min=0, nullable=True)
    owner_id = Field(UUID, foreign_key="users.id", required=True, index=True)
    metadata = Field(dict, default={})

    def validate(self):
        """Custom validation logic."""
        if self.stage == "closed_won" and self.amount is None:
            raise ValueError("Closed won deals must have an amount")
```

### Creating a Service (Features Layer)

```python
from pattern_stack.atoms.patterns.services.base import BaseService
from sqlalchemy import select

class AccountService(BaseService):
    """Data service for Account model."""

    model = Account  # Links service to model

    async def create(self, data: AccountCreate) -> Account:
        """Create new account."""
        account = Account(**data.model_dump())
        account.validate()  # Always validate
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

    async def list_by_stage(self, stage: str) -> list[Account]:
        """Get accounts by stage."""
        result = await self.db.execute(
            select(Account).where(Account.stage == stage)
        )
        return list(result.scalars().all())

    async def get_with_activities(self, account_id: UUID) -> dict:
        """Get account with related data."""
        account = await self.get(account_id)
        # Single domain - just fetch related activities
        result = await self.db.execute(
            select(Activity).where(Activity.account_id == account_id)
        )
        activities = list(result.scalars().all())
        return {"account": account, "activities": activities}
```

### Creating an Entity (Molecules Layer)

```python
from pattern_stack.molecules.entities.base import BaseEntity

class AccountEntity(BaseEntity):
    """Business logic for accounts (single domain)."""

    def _init_services(self):
        """Initialize required services."""
        self.account_service = AccountService(self.db)
        self.activity_service = ActivityService(self.db)

    async def transition_stage(
        self, account_id: UUID, new_stage: str
    ) -> Account:
        """Move account to new stage with validation."""
        account = await self.account_service.get(account_id)

        # Business rule: Can't skip stages
        stage_order = ["prospect", "qualifying", "demo",
                      "proposal", "closing", "closed_won"]
        current_idx = stage_order.index(account.stage)
        new_idx = stage_order.index(new_stage)

        if abs(new_idx - current_idx) != 1:
            raise ValueError("Cannot skip stages")

        # Apply change
        account.stage = new_stage
        await self.account_service.update(account_id, account)

        # Create activity log
        activity = Activity(
            account_id=account_id,
            type="stage_change",
            title=f"Stage changed to {new_stage}",
            occurred_at=datetime.now(UTC)
        )
        self.db.add(activity)
        await self.db.commit()

        return account
```

### Creating a Workflow (Molecules Layer)

```python
class SalesWorkflow:
    """Multi-domain orchestration for sales processes."""

    def __init__(self, db: AsyncSession):
        self.db = db
        # Initialize entities (not services directly)
        self.account_entity = AccountEntity(db)
        self.user_entity = UserEntity(db)
        self.notification_service = NotificationService(db)

    async def close_deal(
        self, account_id: UUID, amount: Decimal
    ) -> dict:
        """Close a deal - orchestrates multiple domains."""
        # 1. Update account
        account = await self.account_entity.transition_stage(
            account_id, "closed_won"
        )
        account.amount = amount
        await self.account_entity.account_service.update(account_id, account)

        # 2. Update owner's metrics
        owner = await self.user_entity.user_service.get(account.owner_id)
        owner.total_sales += amount
        owner.deals_closed += 1
        await self.user_entity.user_service.update(owner.id, owner)

        # 3. Send notifications
        await self.notification_service.send(
            user_id=owner.id,
            message=f"Congratulations! {account.name} closed at ${amount}"
        )

        # 4. Create celebration activity
        activity = Activity(
            account_id=account_id,
            type="deal_closed",
            title=f"Deal closed: ${amount}",
            occurred_at=datetime.now(UTC)
        )
        self.db.add(activity)
        await self.db.commit()

        return {
            "account": account,
            "owner": owner,
            "notification_sent": True
        }
```

## Anti-Patterns to Avoid

### ❌ Don't: Use mapped_column
```python
# WRONG
from sqlalchemy.orm import mapped_column
name: Mapped[str] = mapped_column(String(255))
```

### ✅ Do: Use Field()
```python
# CORRECT
name = Field(str, max_length=255, required=True)
```

---

### ❌ Don't: Put business logic in services
```python
# WRONG - Service doing orchestration
class AccountService(BaseService):
    async def close_deal(self, account_id: UUID):
        account = await self.get(account_id)
        account.stage = "closed_won"
        # Calling other services - WRONG LAYER!
        owner = await self.user_service.get(account.owner_id)
        await self.notification_service.send(...)
```

### ✅ Do: Put orchestration in Workflows
```python
# CORRECT - Workflow orchestrates
class SalesWorkflow:
    async def close_deal(self, account_id: UUID):
        # Orchestrates across domains
        account = await self.account_entity.transition_stage(...)
        owner = await self.user_entity.update_metrics(...)
        await self.notification_service.send(...)
```

---

### ❌ Don't: Directly access db in Entities/Workflows
```python
# WRONG - Entity bypassing service
class AccountEntity:
    async def get_account(self, account_id: UUID):
        result = await self.db.execute(  # Don't query directly!
            select(Account).where(Account.id == account_id)
        )
        return result.scalar_one()
```

### ✅ Do: Use Services for all data access
```python
# CORRECT - Entity uses service
class AccountEntity:
    async def get_account(self, account_id: UUID):
        return await self.account_service.get(account_id)  # Via service
```

---

### ❌ Don't: Forget validation
```python
# WRONG - No validation
async def create(self, data: AccountCreate):
    account = Account(**data.model_dump())
    self.db.add(account)  # What if data is invalid?
    await self.db.commit()
```

### ✅ Do: Always validate
```python
# CORRECT - Validation before commit
async def create(self, data: AccountCreate):
    account = Account(**data.model_dump())
    account.validate()  # Always validate!
    self.db.add(account)
    await self.db.commit()
```

---

### ❌ Don't: Mix concerns across layers
```python
# WRONG - API logic in service
class AccountService:
    async def create_from_request(self, request: Request):
        user = request.user  # API concerns in service!
        data = await request.json()
        ...
```

### ✅ Do: Keep layers focused
```python
# CORRECT - API layer handles requests
# Organism layer
@router.post("/accounts")
async def create_account(
    data: AccountCreate,
    user: User = Depends(get_current_user)
):
    # Delegate to workflow/entity
    return await workflow.create_account(data, user.id)

# Service layer just handles data
class AccountService:
    async def create(self, data: AccountCreate):
        # Pure data operation
        ...
```

## Quick Reference

### Field Types
```python
Field(str, max_length=255)      # String
Field(int, min=0, max=100)      # Integer with range
Field(bool, default=False)       # Boolean
Field(Decimal, min=0)           # Decimal (for money)
Field(UUID, foreign_key="...")  # Foreign key
Field(datetime)                 # Datetime
Field(date)                     # Date only
Field(dict, default={})         # JSON object
Field(list, default=[])         # JSON array
```

### Pattern Selection
- Need inventory tracking? → `CatalogPattern`
- Need users/orgs? → `ActorPattern`
- Need state machine? → `EventPattern`
- Need version history? → `TemporalPattern`
- Need tree structure? → `HierarchicalPattern`
- None of the above? → Just `BasePattern`

### Layer Checklist
- **Atoms**: Database, cache, events, config ✓
- **Features**: CRUD, queries, data validation ✓
- **Molecules/Entities**: Single-domain business logic ✓
- **Molecules/Workflows**: Multi-domain orchestration ✓
- **Organisms**: APIs, auth, request/response ✓

## Final Reminders

1. **Always use Field()**, never mapped_column
2. **Compose patterns** via multiple inheritance
3. **Respect layer boundaries** - no shortcuts
4. **Services = data**, **Entities = single-domain**, **Workflows = multi-domain**
5. **Always validate** before committing
6. **Change tracking is automatic** - just modify and commit
7. **Events fire automatically** - leverage the event system

When in doubt, follow the examples above and trust the patterns. Pattern Stack handles the complexity so you can focus on business logic.
