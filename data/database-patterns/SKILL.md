---
name: database-patterns
description: SQLite veritabani yapisi ve CRUD pattern referansi. Use when working with database operations, queries, or understanding the data model.
---

# Database Patterns

**Database:** `data/content.db` (SQLite)

## Tables

| Table | Purpose |
|-------|---------|
| posts | Icerik, durum, platform ID'leri |
| analytics | Post performans metrikleri |
| content_calendar | Planlanan icerikler |
| strategy | AI ogrenmis stratejiler |
| hook_performance | Hook type performanslari |
| ab_test_results | A/B test sonuclari |
| prompt_history | Video/image prompt tracking |

## Connection Pattern

```python
from app.database.models import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
row = cursor.fetchone()
conn.close()
return dict(row) if row else None
```

## Common CRUD Functions

```python
from app.database.crud import (
    get_post, create_post, update_post,
    get_published_posts, get_analytics_summary,
    get_best_performing_hooks, get_current_strategy
)

# Get post
post = get_post(post_id)

# Published posts (last N days)
posts = get_published_posts(days=30)

# Analytics summary
stats = get_analytics_summary(days=30)

# Best hooks
hooks = get_best_performing_hooks(limit=5)

# Current strategy (JSON fields auto-parsed)
strategy = get_current_strategy()
```

## Update Post

```python
from app.database.crud import update_post

update_post(post_id,
    status="published",
    instagram_post_id="17901234567890123",
    published_at=datetime.now()
)
```

## Viral Score Formula

```python
viral_score = (saves * 2) + (shares * 3) + engagement + (non_follower_reach * 0.015)
```

## JSON Field Handling

```python
import json

# Save JSON
best_days = json.dumps(["monday", "wednesday"])
cursor.execute("UPDATE strategy SET best_days = ?", (best_days,))

# Load JSON (auto in get_current_strategy)
strategy = get_current_strategy()
best_days = strategy['best_days']  # Already parsed
```

## Timezone

```python
def get_kktc_now():
    return datetime.utcnow() + timedelta(hours=2)  # UTC+2
```

## Key Status Values

**posts.status:** draft → scheduled → approved → published | rejected
**content_calendar.status:** planned → content_created → published

## Deep Links

- `app/database/models.py` - Schema, init
- `app/database/crud.py` - All CRUD functions
- `DATABASE.md` - Full schema reference
