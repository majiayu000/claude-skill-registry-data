---
name: performance-budget-checker
description: Detects performance anti-patterns like N+1 queries, nested loops, large file operations, and inefficient algorithms. Suggests fast fixes before issues reach production.
---

# Performance Budget Checker Skill

**Purpose**: Catch performance killers before they slow production.

**Trigger Words**: query, database, loop, for, map, filter, file, read, load, fetch, API, cache

---

## Quick Decision: Check Performance?

```python
def needs_perf_check(code_context: dict) -> bool:
    """Fast performance risk evaluation."""

    # Performance-critical patterns
    patterns = [
        "for ", "while ", "map(", "filter(",  # Loops
        "db.", "query", "select", "fetch",  # Database
        ".all()", ".filter(", ".find(",  # ORM queries
        "open(", "read", "readlines",  # File I/O
        "json.loads", "pickle.load",  # Deserialization
        "sorted(", "sort(",  # Sorting
        "in list", "in array",  # Linear search
    ]

    code = code_context.get("code", "").lower()
    return any(p in code for p in patterns)
```

---

## Performance Anti-Patterns (Quick Fixes)

### 1. **N+1 Query Problem** (Most Common) ⚠️
```python
# ❌ BAD - 1 + N queries (slow!)
def get_users_with_posts():
    users = User.query.all()  # 1 query
    for user in users:
        user.posts = Post.query.filter_by(user_id=user.id).all()  # N queries!
    return users
# Performance: 101 queries for 100 users

# ✅ GOOD - 1 query with JOIN
def get_users_with_posts():
    users = User.query.options(joinedload(User.posts)).all()  # 1 query
    return users
# Performance: 1 query for 100 users

# Or use prefetch
def get_users_with_posts():
    users = User.query.all()
    user_ids = [u.id for u in users]
    posts = Post.query.filter(Post.user_id.in_(user_ids)).all()
    # Group posts by user_id manually
    return users
```

**Quick Fix**: Use `joinedload()`, `selectinload()`, or batch fetch.

---

### 2. **Nested Loops** ⚠️
```python
# ❌ BAD - O(n²) complexity
def find_common_items(list1, list2):
    common = []
    for item1 in list1:  # O(n)
        for item2 in list2:  # O(n)
            if item1 == item2:
                common.append(item1)
    return common
# Performance: 1,000,000 operations for 1000 items each

# ✅ GOOD - O(n) with set
def find_common_items(list1, list2):
    return list(set(list1) & set(list2))
# Performance: 2000 operations for 1000 items each
```

**Quick Fix**: Use set intersection, dict lookup, or hash map.

---

### 3. **Inefficient Filtering** ⚠️
```python
# ❌ BAD - Fetch all, then filter in Python
def get_active_users():
    all_users = User.query.all()  # Fetch 10,000 users
    active = [u for u in all_users if u.is_active]  # Filter in memory
    return active
# Performance: 10,000 rows transferred, filtered in Python

# ✅ GOOD - Filter in database
def get_active_users():
    return User.query.filter_by(is_active=True).all()
# Performance: Only active users transferred
```

**Quick Fix**: Push filtering to database with WHERE clause.

---

### 4. **Large File Loading** ⚠️
```python
# ❌ BAD - Load entire file into memory
def process_large_file(filepath):
    with open(filepath) as f:
        data = f.read()  # 1GB file → 1GB memory!
    for line in data.split('\n'):
        process_line(line)

# ✅ GOOD - Stream line by line
def process_large_file(filepath):
    with open(filepath) as f:
        for line in f:  # Streaming, ~4KB at a time
            process_line(line.strip())
```

**Quick Fix**: Stream files instead of loading fully.

---

### 5. **Missing Pagination** ⚠️
```python
# ❌ BAD - Return all 100,000 records
@app.route("/api/users")
def get_users():
    return User.query.all()  # 100,000 rows!

# ✅ GOOD - Paginate
@app.route("/api/users")
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    return User.query.paginate(page=page, per_page=per_page)
```

**Quick Fix**: Add pagination to list endpoints.

---

### 6. **No Caching** ⚠️
```python
# ❌ BAD - Recompute every time
def get_top_products():
    # Expensive computation every request
    products = Product.query.all()
    sorted_products = sorted(products, key=lambda p: p.sales, reverse=True)
    return sorted_products[:10]

# ✅ GOOD - Cache for 5 minutes
from functools import lru_cache
import time

@lru_cache(maxsize=1)
def get_top_products_cached():
    cache_key = int(time.time() // 300)  # 5 min buckets
    return _compute_top_products()

def _compute_top_products():
    products = Product.query.all()
    sorted_products = sorted(products, key=lambda p: p.sales, reverse=True)
    return sorted_products[:10]
```

**Quick Fix**: Add caching for expensive computations.

---

### 7. **Linear Search in List** ⚠️
```python
# ❌ BAD - O(n) lookup
user_ids = [1, 2, 3, ..., 10000]  # List
if 9999 in user_ids:  # Scans entire list
    pass

# ✅ GOOD - O(1) lookup
user_ids = {1, 2, 3, ..., 10000}  # Set
if 9999 in user_ids:  # Instant lookup
    pass
```

**Quick Fix**: Use set/dict for lookups instead of list.

---

### 8. **Synchronous I/O in Loop** ⚠️
```python
# ❌ BAD - Sequential API calls (slow)
def fetch_user_data(user_ids):
    results = []
    for user_id in user_ids:  # 100 users
        data = requests.get(f"/api/users/{user_id}").json()  # 200ms each
        results.append(data)
    return results
# Performance: 100 × 200ms = 20 seconds!

# ✅ GOOD - Parallel requests
import asyncio
import aiohttp

async def fetch_user_data(user_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, uid) for uid in user_ids]
        results = await asyncio.gather(*tasks)
    return results

async def fetch_one(session, user_id):
    async with session.get(f"/api/users/{user_id}") as resp:
        return await resp.json()
# Performance: ~200ms total (parallel)
```

**Quick Fix**: Use async/await or threading for I/O-bound operations.

---

## Performance Budget Guidelines

| Operation | Acceptable | Warning | Critical |
|-----------|-----------|---------|----------|
| API response time | <200ms | 200-500ms | >500ms |
| Database query | <50ms | 50-200ms | >200ms |
| List endpoint | <100 items | 100-1000 | >1000 |
| File operation | <1MB | 1-10MB | >10MB |
| Loop iterations | <1000 | 1000-10000 | >10000 |

---

## Output Format

```markdown
## Performance Report

**Status**: [✅ WITHIN BUDGET | ⚠️ ISSUES FOUND]

---

### Performance Issues: 2

1. **[HIGH] N+1 Query in get_user_posts() (api.py:34)**
   - **Issue**: 1 + 100 queries (101 total)
   - **Impact**: ~500ms for 100 users
   - **Fix**:
     ```python
     # Change this:
     users = User.query.all()
     for user in users:
         user.posts = Post.query.filter_by(user_id=user.id).all()

     # To this:
     users = User.query.options(joinedload(User.posts)).all()
     ```
   - **Expected**: 500ms → 50ms (10x faster)

2. **[MEDIUM] No pagination on /api/products (routes.py:45)**
   - **Issue**: Returns all 5,000 products
   - **Impact**: 2MB response, slow load
   - **Fix**:
     ```python
     @app.route("/api/products")
     def get_products():
         page = request.args.get('page', 1, type=int)
         return Product.query.paginate(page=page, per_page=50)
     ```

---

### Optimizations Applied: 1
- ✅ Used set() for user_id lookup (utils.py:23) - O(1) instead of O(n)

---

**Next Steps**:
1. Fix N+1 query with joinedload (5 min fix)
2. Add pagination to /api/products (10 min)
3. Consider adding Redis cache for top products
```

---

## When to Skip Performance Checks

✅ Skip for:
- Prototypes/POCs
- Admin-only endpoints (low traffic)
- One-time scripts
- Small datasets (<100 items)

⚠️ Always check for:
- Public APIs
- User-facing endpoints
- High-traffic pages
- Data processing pipelines

---

## What This Skill Does NOT Do

❌ Run actual benchmarks (use profiling tools)
❌ Optimize algorithms (focus on anti-patterns)
❌ Check infrastructure (servers, CDN, etc.)
❌ Replace load testing

✅ **DOES**: Detect common performance anti-patterns with quick fixes.

---

## Configuration

```bash
# Strict mode: check all loops and queries
export LAZYDEV_PERF_STRICT=1

# Disable performance checks
export LAZYDEV_DISABLE_PERF_CHECKS=1

# Set custom thresholds
export LAZYDEV_PERF_MAX_QUERY_TIME=100  # ms
export LAZYDEV_PERF_MAX_LOOP_SIZE=5000
```

---

## Quick Reference: Common Fixes

| Anti-Pattern | Fix | Time Complexity |
|--------------|-----|-----------------|
| N+1 queries | `joinedload()` | O(n) → O(1) |
| Nested loops | Use set/dict | O(n²) → O(n) |
| Load full file | Stream lines | O(n) memory → O(1) |
| No pagination | `.paginate()` | O(n) → O(page_size) |
| Linear search | Use set | O(n) → O(1) |
| Sync I/O loop | async/await | O(n×t) → O(t) |

---

**Version**: 1.0.0
**Focus**: Database, loops, I/O, caching
**Speed**: <3 seconds per file
