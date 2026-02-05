---
name: orm-reviewer
description: |
  WHEN: ORM code review, Prisma/TypeORM/SQLAlchemy/GORM patterns, lazy loading, transactions
  WHAT: Query efficiency + Lazy/eager loading + Transaction handling + N+1 prevention + Model design
  WHEN NOT: Raw SQL → sql-optimizer, Schema design → schema-reviewer
---

# ORM Reviewer Skill

## Purpose
Reviews ORM code for query efficiency, loading strategies, transactions, and best practices.

## When to Use
- ORM code review
- Prisma/TypeORM/SQLAlchemy patterns
- N+1 query detection
- Transaction handling review
- Model relationship design

## Project Detection
- `schema.prisma` (Prisma)
- `@Entity` decorators (TypeORM)
- `models.py` (Django/SQLAlchemy)
- GORM struct tags

## Workflow

### Step 1: Analyze ORM
```
**ORM**: Prisma / TypeORM / SQLAlchemy
**Database**: PostgreSQL
**Models**: 15
**Relationships**: HasMany, BelongsTo, ManyToMany
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full ORM review (recommended)
- Query efficiency
- Loading strategies (N+1)
- Transaction handling
- Model design
multiSelect: true
```

## Detection Rules

### Prisma Patterns

#### N+1 Prevention
```typescript
// BAD: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
    const orders = await prisma.order.findMany({
        where: { userId: user.id }
    });
    // N+1 queries!
}

// GOOD: Include related data
const users = await prisma.user.findMany({
    include: {
        orders: true
    }
});

// GOOD: Selective include
const users = await prisma.user.findMany({
    include: {
        orders: {
            where: { status: 'pending' },
            take: 5,
            orderBy: { createdAt: 'desc' }
        }
    }
});
```

#### Select Optimization
```typescript
// BAD: Fetching all fields
const users = await prisma.user.findMany();

// GOOD: Select only needed fields
const users = await prisma.user.findMany({
    select: {
        id: true,
        name: true,
        email: true
    }
});

// GOOD: Combining select with relations
const orders = await prisma.order.findMany({
    select: {
        id: true,
        total: true,
        user: {
            select: {
                name: true,
                email: true
            }
        }
    }
});
```

#### Transactions
```typescript
// BAD: No transaction for related operations
await prisma.order.create({ data: orderData });
await prisma.orderItem.createMany({ data: items });
await prisma.inventory.updateMany({ ... });
// If inventory update fails, order is orphaned!

// GOOD: Interactive transaction
const result = await prisma.$transaction(async (tx) => {
    const order = await tx.order.create({ data: orderData });

    await tx.orderItem.createMany({
        data: items.map(item => ({ ...item, orderId: order.id }))
    });

    await tx.inventory.updateMany({
        where: { productId: { in: items.map(i => i.productId) } },
        data: { quantity: { decrement: 1 } }
    });

    return order;
});
```

### TypeORM Patterns

#### Eager vs Lazy Loading
```typescript
// BAD: Lazy loading causing N+1
@Entity()
class User {
    @OneToMany(() => Order, order => order.user)
    orders: Order[];  // Lazy by default
}

// Triggers N+1:
const users = await userRepo.find();
for (const user of users) {
    console.log(user.orders);  // Each access = query!
}

// GOOD: Eager loading with relations
const users = await userRepo.find({
    relations: ['orders']
});

// GOOD: QueryBuilder for complex queries
const users = await userRepo
    .createQueryBuilder('user')
    .leftJoinAndSelect('user.orders', 'order')
    .where('order.status = :status', { status: 'pending' })
    .getMany();
```

#### Query Optimization
```typescript
// BAD: Multiple queries
const user = await userRepo.findOne({ where: { id } });
const orders = await orderRepo.find({ where: { userId: id } });
const reviews = await reviewRepo.find({ where: { userId: id } });

// GOOD: Single query with joins
const user = await userRepo.findOne({
    where: { id },
    relations: ['orders', 'reviews']
});

// GOOD: Select specific columns
const users = await userRepo.find({
    select: ['id', 'name', 'email'],
    where: { status: 'active' }
});
```

### SQLAlchemy Patterns

#### Loading Strategies
```python
# BAD: Lazy loading N+1
users = session.query(User).all()
for user in users:
    print(user.orders)  # N queries!

# GOOD: Eager loading
from sqlalchemy.orm import joinedload, selectinload

# For one-to-many: selectinload (2 queries)
users = session.query(User).options(
    selectinload(User.orders)
).all()

# For many-to-one: joinedload (1 query)
orders = session.query(Order).options(
    joinedload(Order.user)
).all()

# Combined
users = session.query(User).options(
    selectinload(User.orders).selectinload(Order.items),
    joinedload(User.profile)
).all()
```

#### Session Management
```python
# BAD: Long-lived session
session = Session()
# ... many operations over time
session.close()  # Objects may be stale

# GOOD: Context manager
with Session() as session:
    user = session.query(User).first()
    # Session auto-closes

# GOOD: Scoped session in web apps
from sqlalchemy.orm import scoped_session

Session = scoped_session(sessionmaker(bind=engine))

# In request handler
def handle_request():
    try:
        # Use Session()
        Session.commit()
    except:
        Session.rollback()
        raise
    finally:
        Session.remove()  # Clean up for this thread
```

### Django ORM Patterns

#### N+1 Prevention
```python
# BAD: N+1 queries
orders = Order.objects.all()
for order in orders:
    print(order.user.name)  # N queries!

# GOOD: select_related for ForeignKey
orders = Order.objects.select_related('user').all()

# GOOD: prefetch_related for reverse FK / M2M
users = User.objects.prefetch_related('orders').all()

# GOOD: Combined with Prefetch for filtering
from django.db.models import Prefetch

users = User.objects.prefetch_related(
    Prefetch(
        'orders',
        queryset=Order.objects.filter(status='pending')
    )
).all()
```

#### Query Optimization
```python
# BAD: .count() after .all()
count = len(Order.objects.all())  # Loads all objects!

# GOOD: Database count
count = Order.objects.count()

# BAD: Multiple queries
user = User.objects.get(id=user_id)
order_count = Order.objects.filter(user=user).count()

# GOOD: Annotation
from django.db.models import Count

user = User.objects.annotate(
    order_count=Count('orders')
).get(id=user_id)

# values() for specific columns only
emails = User.objects.values_list('email', flat=True)
```

### GORM (Go) Patterns
```go
// BAD: N+1 queries
var users []User
db.Find(&users)
for _, user := range users {
    var orders []Order
    db.Where("user_id = ?", user.ID).Find(&orders)
}

// GOOD: Preload
var users []User
db.Preload("Orders").Find(&users)

// GOOD: Preload with conditions
db.Preload("Orders", "status = ?", "pending").Find(&users)

// GOOD: Nested preload
db.Preload("Orders.Items").Find(&users)

// Select specific columns
var users []User
db.Select("id", "name", "email").Find(&users)
```

## Response Template
```
## ORM Code Review Results

**ORM**: Prisma
**Database**: PostgreSQL
**Models**: 12

### N+1 Queries
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | userService.ts:45 | Loop with findMany causing N+1 |

### Loading Strategy
| Status | File | Issue |
|--------|------|-------|
| HIGH | orderController.ts:23 | Missing include for user relation |

### Transactions
| Status | File | Issue |
|--------|------|-------|
| HIGH | checkoutService.ts:67 | Related operations without transaction |

### Query Efficiency
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | reportService.ts:12 | Selecting all columns |

### Recommended Fixes
```typescript
// Fix N+1 in userService.ts
const users = await prisma.user.findMany({
    include: { orders: true }
});

// Add transaction in checkoutService.ts
await prisma.$transaction(async (tx) => {
    // ... atomic operations
});
```
```

## Best Practices
1. **Loading**: Eager load known relations
2. **N+1**: Always include/preload in lists
3. **Select**: Only needed columns
4. **Transactions**: Wrap related operations
5. **Batching**: Use createMany, bulk operations

## Integration
- `sql-optimizer`: Raw query optimization
- `schema-reviewer`: Model design
- `perf-analyzer`: Application performance
