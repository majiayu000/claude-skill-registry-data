---
name: ai-code-maintainability
description: Write production-safe code that survives maintenance — avoid the 15 patterns AI agents commonly generate that work on day 1 but break 3 months later; enforce error handling, logging, type safety, no magic values, and testable structure before writing any code.
triggers:
  - "ai code maintenance"
  - "code maintainability"
  - "production ready code"
  - "ai generated code problems"
  - "code quality gate"
  - "avoid technical debt"
  - "code review checklist"
  - "prevent maintenance bugs"
  - "ai code anti-patterns"
  - "sustainable code"
  - "code that lasts"
  - "avoid magic numbers"
  - "proper error handling"
do_not_use_for:
  - Quick prototypes explicitly marked as throwaway
  - Test fixtures and mock data
see_also:
  - verification
  - golden-principles
  - agent-code-constraints
---

# AI Code Maintainability — Write Code That Survives

**The core problem:** AI agents optimize for "works on first run." Maintenance bugs appear 3–6 months later when context is gone, requirements shift, or edge cases hit prod.

---

## The 15 Patterns That Kill Maintainability

### 1. Silent Error Swallowing (most dangerous)

```python
# ❌ AI generates this — crashes silently in prod
try:
    result = call_external_api(data)
except:
    pass

# ✅ Always log + re-raise or return error state
import logging
logger = logging.getLogger(__name__)

try:
    result = call_external_api(data)
except ExternalAPIError as e:
    logger.error("API call failed: %s | data=%s", e, data, exc_info=True)
    raise  # or: return Result.error(str(e))
except Exception as e:
    logger.critical("Unexpected error in call_external_api: %s", e, exc_info=True)
    raise
```

### 2. Bare `except` / Pokémon Exception Handling

```python
# ❌ Catches KeyboardInterrupt, SystemExit, MemoryError — everything
try:
    do_work()
except Exception:  # still too broad
    return None    # swallowed silently

# ✅ Catch specific exceptions, handle each explicitly
try:
    do_work()
except ValueError as e:
    logger.warning("Invalid input: %s", e)
    return default_value
except NetworkError as e:
    logger.error("Network failure: %s", e)
    raise RetryableError(f"Network unavailable: {e}") from e
```

### 3. Magic Numbers and Strings

```python
# ❌ What is 300? What is "active"?
if user.age > 300:
    status = "active"
time.sleep(300)

# ✅ Named constants with explanations
MAX_VALID_AGE_YEARS = 150  # ISO 8601 human lifespan upper bound
ACTIVE_STATUS = "active"
CACHE_REFRESH_INTERVAL_SECONDS = 300  # 5-minute cache TTL per SLA

if user.age > MAX_VALID_AGE_YEARS:
    status = ACTIVE_STATUS
time.sleep(CACHE_REFRESH_INTERVAL_SECONDS)
```

### 4. print() Instead of Structured Logging

```python
# ❌ No timestamp, no level, no context, can't filter in prod
print(f"Processing user {user_id}")
print("ERROR: something failed")

# ✅ Structured logging — searchable in Datadog/CloudWatch/Grafana
import logging
logger = logging.getLogger(__name__)

logger.info("Processing user", extra={"user_id": user_id, "action": "process"})
logger.error("Processing failed", extra={"user_id": user_id}, exc_info=True)
```

### 5. Missing Type Hints (Python / TypeScript)

```python
# ❌ Future maintainer has no idea what this accepts/returns
def process_data(data, config, mode=None):
    ...

# ✅ Self-documenting — IDE and mypy catch errors immediately
from typing import Optional
from dataclasses import dataclass

def process_data(
    data: list[dict[str, str]],
    config: ProcessConfig,
    mode: Optional[ProcessMode] = None,
) -> ProcessResult:
    ...
```

```typescript
// ❌ any disables the type system
function processUser(data: any): any {
  return data.profile.name;
}

// ✅ Full types — TypeScript catches data.profile?.name at compile time
interface User { id: string; profile: { name: string; email: string } }
interface ProcessResult { displayName: string; emailHash: string }

function processUser(data: User): ProcessResult {
  return { displayName: data.profile.name, emailHash: hash(data.profile.email) };
}
```

### 6. Mutable Default Arguments (Python silent bug)

```python
# ❌ Classic Python bug — list shared across ALL calls
def add_item(item, items=[]):  # same [] object forever
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"]  ← not ["b"]!

# ✅ None sentinel pattern
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 7. Hardcoded Paths and Environment Values

```python
# ❌ Breaks in Docker, in CI, on another dev's machine
DATA_PATH = "/home/user/projects/myapp/data"
API_URL = "http://localhost:8000"

# ✅ Environment-driven — works everywhere
import os
from pathlib import Path

DATA_PATH = Path(os.environ.get("DATA_PATH", "./data")).resolve()
API_URL = os.environ.get("API_URL", "http://localhost:8000")

if not os.environ.get("API_URL"):
    raise EnvironmentError("API_URL must be set. Example: export API_URL=https://api.prod.com")
```

### 8. No Retry / Timeout on External Calls

```python
# ❌ Hangs forever if service is slow; crashes on first transient error
response = requests.get(f"{API_URL}/users/{user_id}")
data = response.json()

# ✅ Timeout + retry with exponential backoff
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    stop=stop_after_attempt(3),
)
def fetch_user(user_id: str) -> dict:
    response = requests.get(
        f"{API_URL}/users/{user_id}",
        timeout=(3.05, 27),   # (connect_timeout, read_timeout)
    )
    response.raise_for_status()
    return response.json()
```

### 9. Unvalidated External Input

```python
# ❌ Crashes or does wrong thing on unexpected input
def create_user(data: dict) -> User:
    return User(
        name=data["name"],
        email=data["email"],
        age=data["age"],
    )

# ✅ Validate at system boundary — fail fast with clear message
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

def create_user(raw_data: dict) -> User:
    req = CreateUserRequest.model_validate(raw_data)  # raises ValidationError with details
    return User(name=req.name, email=req.email, age=req.age)
```

### 10. Uncaught Promise Rejections (TypeScript/JS)

```typescript
// ❌ Unhandled rejection crashes Node.js silently in some versions
async function loadData() {
  const data = await fetchFromAPI();  // what if this throws?
  return data;
}
// Caller: loadData()  ← no await, no .catch()

// ✅ Always handle async errors
async function loadData(): Promise<Result<Data, AppError>> {
  try {
    const data = await fetchFromAPI();
    return { ok: true, data };
  } catch (error) {
    logger.error("Failed to load data", { error });
    return { ok: false, error: new AppError("DATA_LOAD_FAILED", String(error)) };
  }
}

// Caller always handles:
const result = await loadData();
if (!result.ok) return handleError(result.error);
```

### 11. Resource Leaks (File/DB/Connection)

```python
# ❌ File not closed if exception thrown
f = open("data.csv")
data = f.read()
process(data)
f.close()  # never reached if process() throws

# ✅ Context manager guarantees cleanup
with open("data.csv", "r", encoding="utf-8") as f:
    data = f.read()

# ✅ Async version
async with aiofiles.open("data.csv") as f:
    data = await f.read()
```

### 12. N+1 Query Problem (AI loves loops over DB)

```python
# ❌ N queries for N users — kills prod at scale
users = db.query(User).all()
for user in users:
    orders = db.query(Order).filter(Order.user_id == user.id).all()  # N queries
    send_summary(user, orders)

# ✅ Eager load with JOIN — 1 query total
from sqlalchemy.orm import joinedload

users = db.query(User).options(joinedload(User.orders)).all()
for user in users:
    send_summary(user, user.orders)  # already loaded
```

### 13. Sleeping Instead of Polling with Backoff

```python
# ❌ Fixed sleep — either too fast (hammers API) or too slow
while True:
    status = check_job_status(job_id)
    if status == "done":
        break
    time.sleep(5)

# ✅ Exponential backoff with max cap
import time

def wait_for_job(job_id: str, max_wait: int = 300) -> JobResult:
    delay = 1
    elapsed = 0
    while elapsed < max_wait:
        status = check_job_status(job_id)
        if status.is_terminal():
            return status
        logger.debug("Job %s status=%s, retrying in %ds", job_id, status, delay)
        time.sleep(delay)
        elapsed += delay
        delay = min(delay * 2, 30)   # cap at 30s
    raise TimeoutError(f"Job {job_id} did not complete within {max_wait}s")
```

### 14. Implicit Dependencies Between Modules

```python
# ❌ Module A depends on global state set by module B — breaks on import order change
# in config.py
DATABASE_URL = None

# in main.py
from config import *
DATABASE_URL = os.environ["DATABASE_URL"]  # set globally

# in users.py — only works if main.py ran first
from config import DATABASE_URL
db = connect(DATABASE_URL)  # None if imported before main.py init

# ✅ Explicit dependency injection
class UserRepository:
    def __init__(self, db_url: str):
        self.db = connect(db_url)

# main.py wires everything
db_url = os.environ["DATABASE_URL"]
user_repo = UserRepository(db_url=db_url)
```

### 15. No Idempotency on Write Operations

```python
# ❌ Double-click / retry creates duplicate records
def create_order(user_id: str, items: list) -> Order:
    order = Order(user_id=user_id, items=items)
    db.add(order)
    db.commit()
    return order

# ✅ Idempotency key prevents duplicates
def create_order(user_id: str, items: list, idempotency_key: str) -> Order:
    existing = db.query(Order).filter(
        Order.idempotency_key == idempotency_key
    ).first()
    if existing:
        return existing   # same result, no duplicate

    order = Order(user_id=user_id, items=items, idempotency_key=idempotency_key)
    db.add(order)
    db.commit()
    return order
```

---

## Pre-Write Checklist (run mentally before every function)

```
□ What happens when the external call fails? (error path written?)
□ What happens with empty input / null / zero?
□ Will this work in 6 months without the original context? (self-documenting?)
□ Are all "magic" values named constants?
□ Does every exception get logged with context?
□ Are all required env vars validated at startup, not at use time?
□ If this function is called twice, does it produce the same result?
□ Can this be tested without the real DB/API/filesystem?
```

---

## Self-Review Protocol (before handing off code)

```python
# Run this mental filter on every file written:

MAINTAINABILITY_CHECKLIST = {
    "error_handling": "Every try block has a specific except with logging",
    "type_safety":    "All function params and returns are typed",
    "constants":      "No unexplained numeric or string literals",
    "logging":        "Structured logger used, not print()",
    "env_config":     "All config comes from env vars with startup validation",
    "timeouts":       "All external calls have explicit timeout values",
    "idempotency":    "Write operations are safe to retry",
    "resource_mgmt":  "All file/db/connection handles use context managers",
    "no_globals":     "No mutable global state; deps injected explicitly",
    "testability":    "Can I unit-test this without real external systems?",
}
```

---

## Anti-Fake-Pass Checks

- [ ] Code runs ≠ code is production-safe — always apply checklist
- [ ] Catching `Exception` is still too broad for most cases — catch specific types
- [ ] `logger.error("failed")` with no context is nearly useless — log IDs, inputs, stack
- [ ] Type hints on just the happy path but `Optional` not handled = hidden None crashes
- [ ] Passing tests doesn't mean idempotency — tests usually don't test double-submit
- [ ] "Works in dev" with env vars from `.env` file ≠ works in prod with missing vars
