---
name: performance-optimizer
description: This skill should be used when the user asks to "optimize queries", "fix slow queries", "improve performance", "detect N+1", "add indexes", or when writing Django ORM queries that access related objects. Detects and fixes performance issues.
---

# Performance Optimizer

Auto-detects and fixes Django ORM performance issues before they reach production.

## Activation Triggers

This skill activates when:
- Writing ORM queries
- Accessing related objects (foreign keys, M2M)
- Creating views that fetch data
- Mentioning "slow", "performance", "optimization"
- Looping over querysets
- Creating list/detail views

## Performance Targets

- ✅ NO N+1 queries
- ✅ Appropriate indexes on frequently queried fields
- ✅ Pagination for list endpoints
- ✅ `select_related()` for foreign keys
- ✅ `prefetch_related()` for reverse foreign keys and M2M
- ✅ Caching for expensive operations

## Auto-Detection Patterns

### Pattern 1: N+1 Query Detection

**❌ INEFFICIENT (N+1 query):**
```python
# Bad: 1 query for users + N queries for organizations
users = User.objects.all()  # 1 query
for user in users:  # N queries
    print(user.organization.name)  # Hits DB each time!
```

**✅ OPTIMIZED:**
```python
# Good: 2 queries total (1 for users + 1 JOIN for organizations)
users = User.objects.select_related('organization').all()
for user in users:
    print(user.organization.name)  # No DB hit!
```

### Pattern 2: Reverse Foreign Key N+1

**❌ INEFFICIENT:**
```python
# Bad: 1 + N queries
organizations = Organization.objects.all()  # 1 query
for org in organizations:  # N queries
    users = org.users.all()  # Hits DB each time!
    print(f"{org.name}: {users.count()} users")
```

**✅ OPTIMIZED:**
```python
# Good: 2 queries total
organizations = Organization.objects.prefetch_related('users').all()
for org in organizations:
    users = org.users.all()  # Pre-fetched!
    print(f"{org.name}: {users.count()} users")
```

### Pattern 3: Many-to-Many N+1

**❌ INEFFICIENT:**
```python
# Bad: 1 + N queries
users = User.objects.all()  # 1 query
for user in users:  # N queries
    roles = user.roles.all()  # Hits DB each time!
```

**✅ OPTIMIZED:**
```python
# Good: 2 queries total
users = User.objects.prefetch_related('roles').all()
for user in users:
    roles = user.roles.all()  # Pre-fetched!
```

### Pattern 4: Missing Indexes

**❌ SLOW:**
```python
# Frequent query without index
User.objects.filter(email='test@example.com')  # Table scan if no index!
```

**✅ FAST:**
```python
# Model with index
class User(models.Model):
    email = models.EmailField(unique=True)  # Unique creates index
    # OR
    class Meta:
        indexes = [
            models.Index(fields=['email']),  # Explicit index
        ]
```

### Pattern 5: Missing Pagination

**❌ DANGEROUS:**
```python
# Returns ALL records - memory issues with large tables
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # No pagination!
```

**✅ SAFE:**
```python
# Paginated automatically
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination  # DRF auto-paginates
```

## Auto-Fix Process

### Step 1: Detect Anti-Pattern

When detecting:
```python
def get_users_with_organizations(self):
    users = User.objects.all()
    return [
        {'user': u.email, 'org': u.organization.name}
        for u in users
    ]
```

### Step 2: Analyze Query Pattern

Identify:
- Queryset: `User.objects.all()` (1 query)
- Foreign key access: `u.organization.name` (N queries)
- **Total:** 1 + N queries = N+1 problem!

### Step 3: Suggest Optimization

Provide:

> **N+1 Query Detected!**
>
> **Problem:**
> - Query: `User.objects.all()` → 1 query
> - Loop accesses `user.organization.name` → N queries
> - **Total:** 1 + N queries (inefficient!)
>
> **Impact:**
> - 100 users = 101 queries 😱
> - 1000 users = 1001 queries 🔥
>
> **Fix:**
> ```python
> users = User.objects.select_related('organization').all()
> # Now only 2 queries total!
> ```
>
> **Why:**
> - `select_related()` performs SQL JOIN
> - Fetches related data in single query
> - 500x faster for 1000 records!

### Step 4: Auto-Apply Fix

```python
# Optimized version
def get_users_with_organizations(self):
    users = User.objects.select_related('organization').all()
    return [
        {'user': u.email, 'org': u.organization.name}  # No DB hit!
        for u in users
    ]
```

## Common Optimization Patterns

### Foreign Key (One-to-One, Many-to-One)

```python
# Use select_related() for foreign keys
User.objects.select_related('organization', 'created_by')

# Multiple levels
User.objects.select_related('organization__country')
```

### Reverse Foreign Key (One-to-Many)

```python
# Use prefetch_related() for reverse FK
Organization.objects.prefetch_related('users')

# With filtering
from django.db.models import Prefetch
Organization.objects.prefetch_related(
    Prefetch('users', queryset=User.objects.filter(is_active=True))
)
```

### Many-to-Many

```python
# Use prefetch_related() for M2M
User.objects.prefetch_related('roles', 'permissions')
```

### Combined Optimization

```python
# Optimize multiple relations
users = User.objects.select_related(
    'organization',  # FK
    'created_by'     # FK
).prefetch_related(
    'roles',         # M2M
    'permissions'    # M2M
)
```

## Index Recommendations

Suggest indexes for:

### Frequently Filtered Fields

```python
class User(models.Model):
    email = models.EmailField()
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=['email']),    # WHERE email = ...
            models.Index(fields=['status']),   # WHERE status = ...
        ]
```

### Composite Indexes

```python
class Order(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    class Meta:
        indexes = [
            # Composite index for common query pattern
            models.Index(fields=['user', 'status']),
            # Index for time-based queries
            models.Index(fields=['-created_at']),  # DESC order
        ]
```

### Foreign Key Indexes

```python
# Django automatically creates indexes for:
# - Primary keys
# - Unique fields
# - Foreign keys

# Manual indexes needed for:
# - Composite queries
# - Ordering fields
# - Search fields
```

## Caching Strategies

### Query Caching

```python
from django.core.cache import cache

def get_active_users():
    cache_key = 'active_users'
    users = cache.get(cache_key)

    if users is None:
        users = list(User.objects.filter(is_active=True).values())
        cache.set(cache_key, users, 300)  # Cache 5 minutes

    return users
```

### Model Method Caching

```python
from django.utils.functional import cached_property

class User(models.Model):
    @cached_property
    def full_name(self):
        """Expensive computation cached per instance."""
        return f"{self.first_name} {self.last_name}".strip()
```

## Pagination Patterns

```python
# DRF Pagination
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
```

## Database Query Analysis

Check queries using Django Debug Toolbar patterns:

```python
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test_user_list_queries(self):
    """Test that user list doesn't have N+1 queries."""
    with self.assertNumQueries(2):  # Should be exactly 2 queries
        response = self.client.get('/api/users/')
        # 1 query: Fetch users
        # 1 query: Fetch organizations (prefetched)
```

## Performance Checklist

For every queryset, verify:

- ✅ `select_related()` for accessed foreign keys
- ✅ `prefetch_related()` for reverse FKs and M2M
- ✅ `.only()` or `.defer()` if fetching many fields
- ✅ Indexes on filtered/ordered fields
- ✅ Pagination for lists
- ✅ `.count()` instead of `len(queryset)`
- ✅ `.exists()` instead of `if queryset`
- ✅ Bulk operations instead of loops

## Before/After Examples

### Example 1: User List with Organization

**❌ Before (N+1):**
```python
# views.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # 1 query
    # serializer accesses user.organization.name → N queries
```

**✅ After (Optimized):**
```python
# views.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('organization').all()  # 2 queries total
```

### Example 2: Organization with Users

**❌ Before (N+1):**
```python
def organization_summary(self):
    orgs = Organization.objects.all()  # 1 query
    return [
        {
            'name': org.name,
            'user_count': org.users.count()  # N queries!
        }
        for org in orgs
    ]
```

**✅ After (Optimized):**
```python
from django.db.models import Count

def organization_summary(self):
    orgs = Organization.objects.annotate(
        user_count=Count('users')  # Single query with aggregation
    ).all()
    return [
        {
            'name': org.name,
            'user_count': org.user_count  # No DB hit!
        }
        for org in orgs
    ]
```

## Async ORM Queries (Django 5+)

In ASGI applications or async view contexts, **never** execute synchronous ORM operations (`.get()`, `.create()`, `.first()`, iterating querysets) as they block the event loop. Always use Django's native async ORM methods:

```python
# ❌ WRONG: Blocks event loop in async view
async def get_user_profile(request, user_id):
    user = _users_models.User.objects.get(id=user_id)  # Synchronous blocking call!
    return JsonResponse({'name': user.name})

# ✅ CORRECT: Native async ORM methods
async def get_user_profile(request, user_id):
    user = await _users_models.User.objects.aget(id=user_id)
    return JsonResponse({'name': user.name})

# Async iterations & operations:
# await queryset.afirst()
# await queryset.acount()
# await queryset.aexists()
# async for item in queryset: ...
```

### Connection Health Checks
In `settings.py`, enable health checks with connection pooling to reuse connections safely:
```python
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,       # Keep connections open for 10 minutes
        'CONN_HEALTH_CHECKS': True, # Test connection before reusing (avoids dead connection errors)
    }
}
```

## Integration with Testing

```python
# Test that optimizations work
@pytest.mark.django_db
def test_user_list_performance(django_assert_num_queries):
    """User list should use select_related to avoid N+1."""
    UserFactory.create_batch(100)  # Create 100 users

    with django_assert_num_queries(2):  # Only 2 queries allowed
        users = list(User.objects.select_related('organization').all())
        for user in users:
            _ = user.organization.name  # Should not hit DB
```

## Success Criteria

✅ NO N+1 queries in codebase
✅ All foreign key access uses `select_related()`
✅ All reverse FK/M2M use `prefetch_related()`
✅ Appropriate indexes on all models
✅ Pagination on all list endpoints
✅ Bulk operations used instead of loops

## Behavior

**Proactive enforcement:**
- Detect N+1 queries automatically
- Suggest optimizations immediately
- Calculate performance impact (queries before/after)
- Add indexes to models
- Explain WHY the optimization matters

**Never:**
- Require explicit "optimize queries" request
- Wait for production slowness
- Just warn without fixing

**Block completion if:**
- N+1 queries detected
- Missing indexes on frequently queried fields
- No pagination on list endpoints
- Bulk creates/updates done in loops

This ensures code is performant from day one.
